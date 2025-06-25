import cv2
import os
import time
from ultralytics import YOLO
import torch
import numpy as np
from collections import deque
import csv
import pytesseract
from PIL import Image

# Set Tesseract path for Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def main():
    # Paths
    model_path = "data/best.pt"
    video_path = "data/15sec_input_720p.mp4"
    output_path = "output/output_video.mp4"
    tracker_path = "botsort.yaml"  # Switched to BoT-SORT for more stable tracking

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Load the YOLO model
    try:
        model = YOLO(model_path)
        print("Model class names:", model.names)
        # Get class IDs for 'player' and 'goalkeeper'
        player_id = None
        goalkeeper_id = None
        for k, v in model.names.items():
            if v == "player":
                player_id = k
            if v == "goalkeeper":
                goalkeeper_id = k
        if player_id is None and goalkeeper_id is None:
            print("Error: Could not find 'player' or 'goalkeeper' class in model.names.")
            return
        class_ids = []
        if player_id is not None:
            class_ids.append(player_id)
        if goalkeeper_id is not None:
            class_ids.append(goalkeeper_id)
    except Exception as e:
        print(f"Error loading model: {e}")
        return

    # Load the video
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    # Get video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # for MPEG-4 encoded MP4 (widely supported)
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Confidence threshold to reduce false positives
    CONF_THRESH = 0.4

    print("\nPress 'q' in the video window to quit early.")

    # --- Post-processing smoothing state ---
    # Store last seen positions and frame numbers for each ID
    last_seen = {}  # id: (frame_idx, center_x, center_y)
    disappeared = deque(maxlen=30)  # recently disappeared tracks: (old_id, last_frame, last_x, last_y)
    id_remap = {}  # new_id: old_id (for reassigning IDs)
    MAX_DISAPPEAR_FRAMES = 15  # how long to keep a disappeared track for reconnection
    MAX_RECONNECT_DIST = 80    # max pixel distance to reconnect

    # Prepare CSV logging for tracking results
    log_path = "output/tracking_log.csv"
    log_file = open(log_path, mode="w", newline="")
    csv_writer = csv.writer(log_file)
    csv_writer.writerow(["frame", "id", "x1", "y1", "x2", "y2", "class", "conf"])

    # Frame processing loop
    current_frame = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        current_frame += 1
        print(f"Processing frame {current_frame}/{frame_count}", end="\r")

        # Run YOLO + BoT-SORT on all objects (no class restriction)
        try:
            results = model.track(frame, persist=True, tracker=tracker_path)
        except Exception as e:
            print(f"\nError during tracking: {e}")
            break

        # Extract tracking info
        try:
            boxes = results[0].boxes
            if boxes is not None and hasattr(boxes, 'id') and boxes.id is not None:
                def to_numpy(x):
                    if isinstance(x, torch.Tensor):
                        return x.cpu().numpy()
                    return x
                xyxy = to_numpy(boxes.xyxy)
                ids = to_numpy(boxes.id)
                clss = to_numpy(boxes.cls)
                confs = to_numpy(boxes.conf)

                # Track which IDs are present this frame
                current_ids = set()
                centers = {}
                for box, track_id, cls_id, conf in zip(xyxy, ids, clss, confs):
                    class_name = model.names[int(cls_id)]
                    if class_name in ["player", "goalkeeper"] and conf >= CONF_THRESH:
                        x1, y1, x2, y2 = map(int, box)
                        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                        current_ids.add(int(track_id))
                        centers[int(track_id)] = (cx, cy)
                        # Log to CSV (use remapped ID if available)
                        display_id = id_remap.get(int(track_id), int(track_id))
                        csv_writer.writerow([current_frame, display_id, x1, y1, x2, y2, class_name, float(conf)])

                # --- Smoothing: Reconnect IDs ---
                # 1. Check for new IDs that might be reconnected
                for new_id in current_ids:
                    if new_id in id_remap:
                        # Already remapped
                        continue
                    # If this ID was not seen last frame, try to reconnect
                    if new_id not in last_seen or last_seen[new_id][0] < current_frame - 1:
                        cx, cy = centers[new_id]
                        # Search for a disappeared track nearby
                        for old_id, last_frame, last_x, last_y in list(disappeared):
                            if current_frame - last_frame <= MAX_DISAPPEAR_FRAMES:
                                dist = np.hypot(cx - last_x, cy - last_y)
                                if dist < MAX_RECONNECT_DIST:
                                    id_remap[new_id] = old_id
                                    disappeared.remove((old_id, last_frame, last_x, last_y))
                                    print(f"Reconnected ID {old_id} to new ID {new_id} at frame {current_frame}")
                                    break

                # 2. Draw boxes and update last_seen
                for box, track_id, cls_id, conf in zip(xyxy, ids, clss, confs):
                    class_name = model.names[int(cls_id)]
                    if class_name in ["player", "goalkeeper"] and conf >= CONF_THRESH:
                        x1, y1, x2, y2 = map(int, box)
                        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
                        # Use remapped ID if available
                        display_id = id_remap.get(int(track_id), int(track_id))
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        # --- Jersey Number Recognition ---
                        crop = frame[max(0, y1):max(0, y2), max(0, x1):max(0, x2)]
                        jersey_number = ""
                        if crop.shape[0] > 10 and crop.shape[1] > 10:
                            try:
                                # Preprocess: grayscale, resize, adaptive threshold
                                gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
                                # Enlarge if small
                                scale = 2 if min(gray.shape) < 40 else 1
                                if scale > 1:
                                    gray = cv2.resize(gray, (gray.shape[1]*scale, gray.shape[0]*scale), interpolation=cv2.INTER_CUBIC)
                                # Adaptive threshold
                                threshed = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
                                pil_crop = Image.fromarray(threshed)
                                ocr_result = pytesseract.image_to_string(pil_crop, config='--psm 8 -c tessedit_char_whitelist=0123456789')
                                digits = ''.join([c for c in ocr_result if c.isdigit()])
                                if digits:
                                    jersey_number = digits
                                    cv2.putText(frame, f"# {jersey_number}", (x1, y1 - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
                            except Exception as ocr_e:
                                pass
                        cv2.putText(frame, f"ID: {display_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        last_seen[display_id] = (current_frame, cx, cy)

                # 3. Update disappeared list
                # Any ID in last_seen but not in current_ids is considered disappeared
                for prev_id in list(last_seen.keys()):
                    if prev_id not in [id_remap.get(int(i), int(i)) for i in current_ids]:
                        last_frame, last_x, last_y = last_seen[prev_id]
                        if current_frame - last_frame <= MAX_DISAPPEAR_FRAMES:
                            disappeared.append((prev_id, last_frame, last_x, last_y))
                        del last_seen[prev_id]
        except Exception as e:
            print(f"\nError parsing results: {e}")

        # Show the frame in a window
        cv2.imshow("Player Tracking", frame)
        # Write frame to output
        out.write(frame)

        # Allow user to quit early
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\nQuitting early as requested.")
            break

    print(f"\n✅ Processing complete. Output saved to: {output_path}")

    # Release resources
    cap.release()
    out.release()
    log_file.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
