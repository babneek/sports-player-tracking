# Player Re-Identification

This project solves the player re-identification task in sports footage, as detailed in the assignment. It uses the YOLOv8 object detection model with the ByteTrack algorithm to identify and track players and goalkeepers in a video clip.

## Project Structure
- `data/`: Contains the input video (`15sec_input_720p.mp4`) and the YOLO model (`best.pt`).
- `output/`: The destination for the final processed video (`output_video.mp4`).
- `src/`: Contains the main Python script (`main.py`).
- `bytetrack.yaml`: The configuration file for the ByteTrack algorithm.
- `report.md`: The final project report.
- `requirements.txt`: A list of the required Python dependencies.

## Setup and Installation

1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/babneek/sports-player-tracking.git
   cd sports-player-tracking
   ```
2. **Create a Virtual Environment** (Recommended):  
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```
3. **Install Dependencies**:  
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Code

1.  **Ensure Data is Present**: Make sure the `15sec_input_720p.mp4` video and the `best.pt` model file are in the `data/` directory.

2.  **Run the Script**:
    ```bash
    python src/main.py
    ```

3.  **Find the Output**: The script will process the video and save the final result, with player IDs drawn on the frames, to `output/output_video.mp4`. A confirmation message will be printed to the console upon completion.

## Demo

- The output video (`output/output_video.mp4`) demonstrates player tracking, ID assignment, and attempted jersey number recognition.
- “The demo video shows the output of the tracking pipeline, with bounding boxes and IDs overlaid on each player.”
- Tracking metrics are computed using `src/track_metrics.py`.

## Note on Large Files

> **Note:** The model file `data/best.pt` is **not included** due to GitHub's file size limit.  
> Please contact me for access, or use your own YOLO weights.

## How to Reproduce

1. Place your YOLO model weights as `data/best.pt`.
2. Place your input video as `data/15sec_input_720p.mp4`.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the main script:
   ```
   python src/main.py
   ```
5. (Optional) Compute tracking metrics:
   ```
   python src/track_metrics.py
   ```

## Contact

For the model file or any questions, please contact babneeksaini@gmail.com. 
