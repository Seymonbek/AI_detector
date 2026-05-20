# AI Detector

AI Detector is a local computer vision portfolio project built to demonstrate an end-to-end detection pipeline: video processing, object tracking, event generation, and a lightweight monitoring API.

This repository is intentionally prepared as a local showcase project rather than a public production deployment.

## Overview

The system monitors a video stream, tracks detected objects, and raises an alert when an object crosses a virtual line from right to left. Each alert can include a captured frame and is displayed in a simple live dashboard.

## Key Features

- YOLOv8-based object tracking on video frames
- Direction-based intrusion logic using a virtual line
- Local FastAPI server for alert collection
- Live dashboard for recent alert events
- Optional image upload together with each alert
- Simple event archiving in `history.json`

## Tech Stack

- Python
- OpenCV
- Ultralytics YOLOv8
- FastAPI
- Uvicorn
- Requests

## How It Works

1. `detector.py` loads the YOLO model and reads a local video source.
2. The detector tracks moving objects frame by frame.
3. When an object crosses the line from right to left, the detector sends an alert to the local API.
4. `server.py` receives the event, stores it, saves the image if provided, and shows it on the dashboard.

## Project Structure

- `detector.py` - local detection and alert-sending logic
- `server.py` - FastAPI server and dashboard
- `requirements.txt` - all dependencies needed for local usage
- `history.json` - archived sample alert history
- `test_video.mp4` and `test_video1.mp4` - local demo inputs
- `yolov8n.pt` - YOLO model file used by the detector

## Run Locally

Quick start:

```bash
./start.sh
```

If the script is not executable yet:

```bash
chmod +x start.sh
./start.sh
```

If you want to run the second demo video:

```bash
./start.sh test_video1.mp4
```

Manual option:

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Start the local server:

```bash
uvicorn server:app --host 0.0.0.0 --port 5000
```

3. Run the detector in another terminal:

```bash
python3 detector.py
```

4. Open the dashboard:

```text
http://127.0.0.1:5000
```

5. Open the API docs:

```text
http://127.0.0.1:5000/docs
```

## Optional Local Configuration

The detector supports environment variables for quick local testing:

- `SERVER_URL` - defaults to `http://127.0.0.1:5000/api/alert`
- `VIDEO_SOURCE` - defaults to `test_video.mp4`

Example:

```bash
SERVER_URL=http://127.0.0.1:5000/api/alert VIDEO_SOURCE=test_video1.mp4 python3 detector.py
```

## Portfolio Notes

This project is useful for demonstrating:

- practical computer vision integration
- backend API development with Python
- event-driven design
- local monitoring workflow
- ability to combine ML inference with application logic

## Current Limitations

- Designed for local demo usage, not hardened production deployment
- Uses a simple line-crossing rule instead of zone-based reasoning
- Uses sample video files by default instead of a real camera or RTSP stream
- Event storage is lightweight and file-based

## Future Improvements

- Real webcam or IP camera support
- Better filtering for person-only detection
- Persistent database storage
- Authentication for API endpoints
