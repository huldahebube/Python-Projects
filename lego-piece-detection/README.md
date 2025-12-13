# LEGO Piece Counting & Detection (Computer Vision)

## Overview
This project explores computer vision methods to segment, count, and detect LEGO pieces in images. It combines classical image processing (OpenCV) with deep learning object detection (PyTorch).

## What I Did
- Cleaned and prepared images (including converting HEIC to JPG when needed)
- Phase 1: Tested segmentation approaches to separate LEGO pieces from the background:
  - Thresholding
  - Edge detection (Canny + contours)
  - Color-based segmentation (e.g., clustering-based ideas)
- Phase 2: Built an object detection pipeline using Faster R-CNN to detect LEGO pieces with bounding boxes

## Tools & Libraries
- Python, OpenCV (cv2), NumPy, Matplotlib
- PIL / pillow-heif (image handling + HEIC support)
- PyTorch + Torchvision (Faster R-CNN)
- Scikit-learn (supporting utilities)

## Files
- `lego_piece_counting_and_detection.ipynb` — main notebook with all steps and results
