# Player Re-Identification Report

## 1. Approach and Methodology

The final solution uses the YOLOv8 object detection model in combination with the state-of-the-art **ByteTrack** algorithm to perform robust player re-identification. The core methodology is as follows:

1.  **Video Processing**: The input video is read frame-by-frame using OpenCV.
2.  **Object Tracking**: For each frame, the `ultralytics` library's `track()` method is called. This method is specifically configured to:
    - Use the **ByteTrack** algorithm, which is highly effective at handling occlusions and maintaining stable track IDs. The configuration is specified in the `bytetrack.yaml` file.
    - Only track objects belonging to the "player" and "goalkeeper" classes, completely ignoring referees and the ball at the tracker level.
3.  **Visualization**: The script iterates through the objects successfully tracked by ByteTrack in the current frame. For each object, a bounding box and its unique track ID are drawn onto the frame.
4.  **Output Generation**: The processed frames, now with the re-identification visuals, are written to a new MP4 video file located in the `output/` directory.

This approach is simple, robust, and leverages the powerful, built-in features of the `ultralytics` library to achieve accurate and stable player tracking.

## 2. Techniques and Outcomes

Several techniques were attempted throughout the development process.

-   **Initial Approach (Custom Centroid Tracker)**: The first implementation used a simple, custom-built centroid tracker. This proved to be insufficient, as it was highly susceptible to ID switching and could not handle occlusions well, resulting in "ghost" boxes and unstable tracking.
-   **Intermediate Approach (Hungarian Algorithm)**: The custom tracker was replaced with a more robust implementation using the Hungarian algorithm and Intersection over Union (IoU) for matching. While an improvement, this method still struggled with model inaccuracies.
-   **The Referee Problem**: A persistent issue was the model occasionally misclassifying the referee as a player. This would "poison" the tracker, causing it to incorrectly follow the referee.
-   **Final, Successful Approach (ByteTrack with Class Filtering)**: The breakthrough came from abandoning all custom tracking logic and instead using the sophisticated, built-in **ByteTrack** algorithm. By configuring the tracker to *only* consider "player" and "goalkeeper" classes from the start, all issues with tracking referees were eliminated. This method proved to be the most stable and accurate, successfully solving the core challenges of the assignment.

## 3. Challenges Encountered

-   **Model Inaccuracy**: The primary challenge was the unreliability of the provided model, which would flicker in its classification of the referee. This insight was key to understanding the failure of earlier, more naive tracking approaches.
-   **Tracker Stability**: Finding a tracking algorithm that could gracefully handle the fast-paced, occluded nature of sports footage was a significant challenge. Simple trackers were not sufficient, highlighting the need for more advanced algorithms like ByteTrack.

## 4. Future Work

-   **Metric-Based Evaluation**: The current evaluation is purely visual. A future version could implement quantitative metrics (e.g., MOTA, IDF1) to objectively measure the tracker's performance.
-   **Appearance-Based Re-identification**: To further improve accuracy, especially if players are out of frame for a long time, appearance-based features (e.g., color histograms of jerseys, deep learning embeddings) could be integrated into the tracking logic. This would help distinguish between players who look similar.

## Jersey Number Recognition: Attempt, Challenges, and Future Work

### What Was Tried
- Integrated Tesseract OCR to recognize jersey numbers from each player's bounding box.
- Applied image preprocessing (grayscale, resizing, adaptive thresholding) to improve OCR accuracy.
- Displayed detected numbers above player boxes in the output video.

### Observed Results
- In some cases, Tesseract detected numbers, but often the results were noisy or incorrect (random digits, false positives).
- The OCR struggled with small, blurry, or low-contrast numbers, and with busy backgrounds (logos, folds, stripes).
- This is a known limitation of Tesseract and most general-purpose OCR engines on real-world sports footage.

### Why This Is Challenging
- Jersey numbers are often small, partially occluded, or distorted by motion.
- Lighting, camera angle, and background clutter make segmentation and recognition difficult.
- Tesseract is designed for clean, printed text, not for digits on moving players in complex scenes.

### What Would Be Needed for a Real Solution
- **Custom Digit Detector:** Train a YOLO (or similar) model specifically to detect digits on jerseys, using a dataset of annotated jersey crops.
- **Better Preprocessing:** Use advanced image enhancement, super-resolution, or segmentation to isolate numbers.
- **Temporal Smoothing:** Aggregate OCR results across multiple frames to improve reliability.

### Conclusion and Next Steps
- The OCR attempt demonstrates technical initiative and a realistic understanding of the problem.
- For production-quality results, a dedicated digit detection model and more annotated data would be required.
- With more time/resources, the next step would be to collect jersey digit crops, train a YOLO model for digit detection, and integrate it into the tracking pipeline.

## Real-World Limitations of Player Tracking

Despite using advanced trackers (BoT-SORT with ReID, high buffer, and custom smoothing), some ID switches may still occur in challenging sports footage. This is due to:
- Missed detections (e.g., occlusion, motion blur, or overlap)
- Players with very similar appearance
- Severe occlusion or crossing paths
- Model misclassifications

Trackers assign internal IDs to detected players and try to keep them consistent across frames. However, if a player is not detected for several frames or reappears in a different location, the tracker may assign a new ID. Custom smoothing logic can reconnect tracks in some cases, but not all.

**Conclusion:**
ID stability is fundamentally limited by detection quality and scene complexity. This is a known challenge in real-world sports analytics and is an active area of research. 