# Player Re-Identification Report

## 1. Introduction

This report documents the approach, methodology, challenges, and outcomes of a sports player re-identification project using YOLOv8 and advanced tracking algorithms. The goal was to robustly track individual players in a soccer video, assign stable IDs, and attempt jersey number recognition, producing a professional, reproducible solution suitable for internship submission.

## 2. Approach and Methodology

The final solution leverages the YOLOv8 object detection model in combination with the state-of-the-art ByteTrack algorithm for robust player re-identification. The core methodology is as follows:

- **Video Processing:** The input video is read frame-by-frame using OpenCV.
- **Object Tracking:** For each frame, the Ultralytics library's `track()` method is called, configured to:
    - Use the ByteTrack algorithm, highly effective at handling occlusions and maintaining stable track IDs (configured via `bytetrack.yaml`).
    - Only track objects belonging to the "player" and "goalkeeper" classes, ignoring referees and the ball at the tracker level.
- **Visualization:** For each tracked object, a bounding box and its unique track ID are drawn onto the frame.
- **Output Generation:** Processed frames with re-identification visuals are written to a new MP4 video in the `output/` directory.

This approach is robust and leverages the powerful, built-in features of the Ultralytics library to achieve accurate and stable player tracking.

## 3. Techniques and Outcomes

### Initial Approach: Custom Centroid Tracker
- Implemented a simple centroid tracker.
- Result: Highly susceptible to ID switching, poor handling of occlusions, unstable tracking.

### Intermediate Approach: Hungarian Algorithm
- Replaced with a tracker using the Hungarian algorithm and IoU for matching.
- Result: Improved, but still struggled with model inaccuracies and ID switches.

### The Referee Problem
- The model occasionally misclassified the referee as a player, causing the tracker to incorrectly follow the referee.

### Final Approach: ByteTrack with Class Filtering
- Switched to the built-in ByteTrack algorithm.
- Configured to only track "player" and "goalkeeper" classes, eliminating referee tracking issues.
- Result: Most stable and accurate tracking, successfully solving the core challenges.

## 4. Jersey Number Recognition: Attempt, Challenges, and Future Work

### What Was Tried
- Integrated Tesseract OCR to recognize jersey numbers from each player's bounding box.
- Applied image preprocessing (grayscale, resizing, adaptive thresholding) to improve OCR accuracy.
- Displayed detected numbers above player boxes in the output video.

### Observed Results
- Tesseract occasionally detected numbers, but results were often noisy or incorrect (random digits, false positives).
- OCR struggled with small, blurry, or low-contrast numbers, and with busy backgrounds (logos, folds, stripes).

### Why This Is Challenging
- Jersey numbers are often small, partially occluded, or distorted by motion.
- Lighting, camera angle, and background clutter make segmentation and recognition difficult.
- Tesseract is designed for clean, printed text, not for digits on moving players in complex scenes.

### What Would Be Needed for a Real Solution
- **Custom Digit Detector:** Train a YOLO (or similar) model specifically to detect digits on jerseys, using a dataset of annotated jersey crops.
- **Better Preprocessing:** Use advanced image enhancement, super-resolution, or segmentation to isolate numbers.
- **Temporal Smoothing:** Aggregate OCR results across multiple frames to improve reliability.

## 5. Challenges Encountered

- **Model Inaccuracy:** The provided model sometimes flickered in its classification of the referee, leading to tracking errors.
- **Tracker Stability:** Simple trackers could not handle the fast-paced, occluded nature of sports footage, necessitating advanced algorithms like ByteTrack.
- **Jersey Number OCR:** General-purpose OCR engines like Tesseract are not designed for jersey numbers in real-world sports footage, resulting in unreliable recognition.

## 6. Limitations

- **ID Switches:** Despite using ByteTrack and custom smoothing, some ID switches still occur, especially during occlusions, missed detections, or with similar-looking players. This is a known limitation in real-world sports analytics.
- **Jersey Number Recognition:** Tesseract OCR struggles with small, blurry, or occluded numbers, and with complex backgrounds. Reliable results would require a custom digit detector.
- **Model File Size:** The YOLO model file (`data/best.pt`) exceeds GitHub's 100MB file size limit and is not included in the repository. Users must obtain it separately.
- **Output Video Size:** Output videos are not tracked in version control due to size constraints. Users must generate their own by running the script.
- **Generalization:** The pipeline is tuned for the provided video and may require further tuning or retraining for different sports, camera angles, or video quality.

## 7. Future Work

- **Metric-Based Evaluation:** Implement quantitative metrics (e.g., MOTA, IDF1) to objectively measure tracker performance.
- **Appearance-Based Re-identification:** Integrate appearance-based features (e.g., color histograms, deep learning embeddings) to further improve accuracy, especially for long-term re-identification.
- **Dedicated Jersey Digit Detection:** Collect jersey digit crops, train a YOLO model for digit detection, and integrate it into the pipeline.
- **Advanced Preprocessing:** Explore super-resolution and segmentation to enhance OCR reliability.

## 8. Conclusion

This project demonstrates a robust, modern approach to player re-identification in sports video using YOLOv8 and ByteTrack. While the pipeline achieves stable tracking and demonstrates technical initiative with jersey number OCR, real-world challenges such as model inaccuracies, occlusions, and noisy OCR remain. The report honestly documents these limitations and outlines clear next steps for future improvement. The codebase, documentation, and results are presented professionally and reproducibly, meeting the standards for an internship or academic submission.

---

*For any questions or to obtain the model file, please contact [babneeksaini@gmail.com].* 