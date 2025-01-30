# FaceTracker

Take-home project for interviewing with HeyGen.

## Overview
FaceTracker is a tool designed to detect, track, and crop a specific target face from a video. The tool extracts exact video clips of the target face, along with metadata, including timestamps and face bounding box coordinates for each frame.

## Installation
This project is tested under WSL2, Ubuntu 22.04, and Python 3.10, NVIDIA RTX 3060 Ti. The CUDA vision is 12.6, and the CUDNN version is 9.7.0.
To set up the project, follow these steps:

1. Clone the repository:
   ```bash
    git clone https://github.com/rickyyuan07/FaceTracker
    cd FaceTracker
   ```

2. Make sure you have [Conda](https://docs.conda.io/en/latest/miniconda.html), CUDA, CUDNN, and FFmpeg installed on your system.

3. Create Conda environment and install dependencies:
   ```bash
    conda create -n FaceTracker python=3.10
    conda activate FaceTracker
    pip install -r requirements.txt
   ```

4. Ensure you have [Node.js](https://nodejs.org/en) installed if you wish to use `pytubefix` to download YouTube videos. For more details, see [this pull request](https://github.com/JuanBindez/pytubefix/pull/209).

## Data preparation
Run
```bash
python prepare_data.py
```

if you want to download youtube videos other than the sample videos in `/sample_data/`. This scripts downloads the highest quality Youtube Video, and the audio of the video, and combines them into a single video file. After that, it crops the video into a predefined length, and saves the cropped video into the `sample_data` folder. Please look into the script and modify if you want to test on different videos.

### Data for Testing
Sample videos are categorized based on difficulty:
- **Easy:** One person speaking directly to the camera.
- **Medium:** Two people talking with transitions between them.
- **Hard:** A moving camera scenario, such as a TED Talk video.

## Usage
The To run the face tracking tool, use the following commands:

1. Perform face detection, it would generate a json file containing the coordinates of the detected face(s) in each frame.:

```bash
python src/face_detection.py --video_path <path_to_video> --output_folder <path_to_save_output> --algorithm <algorithm_name> --debug
```

Example:
```bash
python src/face_detection.py --video_path ./sample_data/jensen_medium1.mp4 --output_folder ./output/jensen_medium1 --algorithm retinaface
```

2. Perform face recognition, it would generate a video containing the target face only, and a json file containing the metadata of the cropped video.:
```bash
python src/face_recog.py --video_path <path_to_video> --face_coordinates_path <path_to_save_face_coordinates> --reference_image_path <path_to_reference_image> --output_dir <path_to_save_output> --debug
```

Example:
```bash
python src/face_recog.py --video_path ./sample_data/jensen_medium1.mp4 --face_coordinates_path ./output/jensen_medium1/face_coordinates.json --reference_image_path ./sample_data/jensen_huang.png --output_dir ./output/jensen_medium1/videos/
```

## Future Work
- **Real-time performance:** Improve the tracker's performance to process videos in real-time.
    - GPU acceleration for both face detection and recognition.
- **Offline processing:** Implement a batch processing mode to process multiple videos or multiple frames at once.
    - The tool can be extended to process multiple videos or frames in parallel, which would be useful for batch processing.
- **Audio support:**  Add support for audio processing.
    - Video clips with audio have lots of small issues that need to be figured out. From downloading from Youtube, to cropping the video, to merging the audio back in. The code for generating segments with audio support also has lots of space for improvement and optimization.
- **Smoothing:** Implement a moving average to smooth the bounding box. (Done)
- **Hyperparameter tuning:** The matching threshold for face recognition can be tuned. (how?)
- **Refine README:** Go through the installation and usage instructions to ensure they are clear and concise.


## Clarifications
- **Real-time vs. Quality:** The tool prioritizes processing quality over real-time performance. (For now)
- **Face or Whole Head:** The tracker is designed to focus on the face specifically, excluding hair, neck, etc.
- **Timestamps:** Timestamps in the metadata refer to frame indices, not absolute time.
- **Audio support:**


## Features
- Detect and track all faces in a video.
- Identify and isolate the target face based on a reference image.
- Generate cropped video clips containing only the target face.
- Handle scene changes or occlusions by splitting the clips accordingly.
- Export metadata including:
  - File name of the cropped video.
  - Start and end timestamps of each clip.
  - Frame-wise face coordinates (e.g., `[x, y, width, height]`).