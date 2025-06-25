# Sports Player Re-Identification and Tracking

## Project Summary
This repository provides code and instructions for tracking and re-identifying soccer players in video footage using YOLOv8 for detection, ByteTrack for tracking, and Tesseract OCR for experimental jersey number recognition. The focus is on practical usage and reproducibility.

## File Structure
```
├── data/
│   ├── 15sec_input_720p.mp4      # Input video (not included)
│   └── best.pt                   # YOLOv8 model weights (not included)
├── output/
│   ├── output_video.mp4          # Annotated output video (generated)
│   └── tracking_log.csv          # Tracking results (generated)
├── src/
│   ├── main.py                   # Main tracking script
│   └── track_metrics.py          # Metrics computation script
├── bytetrack.yaml                # ByteTrack configuration
├── botsort.yaml                  # (Optional) BoT-SORT config
├── report.md                     # Project report (see for methodology, challenges, etc.)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Dependencies
- Python 3.8+
- [Ultralytics YOLOv8](https://github.com/ultralytics/ultralytics)
- OpenCV
- Tesseract OCR (system install)
- NumPy, pandas, PyYAML
- ffmpeg (optional, for video trimming)

Install Python dependencies:
```
pip install -r requirements.txt
```
Install Tesseract OCR:
- **Windows:** [Download here](https://github.com/tesseract-ocr/tesseract/wiki)
- **Linux:** `sudo apt-get install tesseract-ocr`

## Setup
1. Clone the repository:
   ```
   git clone https://github.com/babneek/sports-player-tracking.git
   cd sports-player-tracking
   ```
2. (Recommended) Create and activate a virtual environment:
   ```
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # macOS/Linux: source .venv/bin/activate
   ```
3. Install dependencies as above.
4. Download YOLOv8 weights (`best.pt`) and place in `data/` (not included).
5. Place your input video in `data/`.

## How to Run
1. Run player tracking:
   ```
   python src/main.py --video data/15sec_input_720p.mp4 --weights data/best.pt --output output/output_video.mp4
   ```
2. Compute tracking metrics:
   ```
   python src/track_metrics.py --log output/tracking_log.csv
   ```

## Configuration
- Edit `bytetrack.yaml` (or `botsort.yaml`) to adjust tracker parameters.
- Change detection classes or OCR preprocessing in `src/main.py` if needed.

## Demo Video
- The output video (output/output_video.mp4) demonstrates player tracking, ID assignment, and attempted jersey number recognition.
-The demo video shows the output of the tracking pipeline, with bounding boxes and IDs overlaid on each player.
-Tracking metrics are computed using src/track_metrics.py.


## Troubleshooting
- **Tesseract not found:** Ensure it is installed and in your system PATH.
- **Model file missing:** Download `best.pt` and place in `data/`.
- **Output video not playing:** Try a different player or re-encode with ffmpeg.

## Contact
For questions or access to the model file, contact:
- **Babneek Saini** (<babneeksaini@gmail.com>)

---
**For methodology, challenges, limitations, and future work, see `report.md`.**