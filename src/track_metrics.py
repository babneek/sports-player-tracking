import csv
from collections import defaultdict

# Path to the tracking log
log_path = "../output/tracking_log.csv"

# Read tracking data
tracks = defaultdict(list)  # id: list of (frame, bbox, class, conf)
with open(log_path, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        frame = int(row["frame"])
        tid = int(row["id"])
        bbox = (int(row["x1"]), int(row["y1"]), int(row["x2"]), int(row["y2"]))
        cls = row["class"]
        conf = float(row["conf"])
        tracks[tid].append((frame, bbox, cls, conf))

# Compute ID switches and track continuity
id_switches = 0
last_seen = {}  # frame: {bbox: id}
track_lengths = []

# For each frame, build a mapping of bbox to ID
frame_to_ids = defaultdict(list)
for tid, dets in tracks.items():
    for frame, bbox, cls, conf in dets:
        frame_to_ids[frame].append((tid, bbox))

# For each track, count how many times it disappears and reappears (ID switches)
for tid, dets in tracks.items():
    dets = sorted(dets)
    prev_frame = None
    for i, (frame, bbox, cls, conf) in enumerate(dets):
        if prev_frame is not None and frame - prev_frame > 1:
            id_switches += 1
        prev_frame = frame
    track_lengths.append(len(dets))

# Print summary
print("=== Tracking Metrics Summary ===")
print(f"Total unique IDs (tracks): {len(tracks)}")
print(f"Total ID switches (track lost and reappeared): {id_switches}")
print(f"Average track length (frames): {sum(track_lengths)/len(track_lengths):.2f}")
print(f"Longest track (frames): {max(track_lengths)}")
print(f"Shortest track (frames): {min(track_lengths)}")
print("===============================") 