# FaceTracker

Take-home project for interviewing with HeyGen.

## Overview
FaceTracker is a tool designed to detect, track, and crop a specific target face from a video. The tool extracts exact video clips of the target face, along with metadata, including timestamps and face bounding box coordinates for each frame.

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```bash
    git clone https://github.com/rickyyuan07/FaceTracker
    cd FaceTracker
   ```

2. Create Conda environment and install dependencies:
   ```bash
    conda create -n FaceTracker python=3.12
    conda activate FaceTracker
    pip install -r requirements.txt
   ```

3. Ensure you have [Node.js](https://nodejs.org/en) installed if you wish to use `pytubefix` to download YouTube videos. For more details, see [this pull request](https://github.com/JuanBindez/pytubefix/pull/209).

## Data preparation
Run
```bash
python prepare_data.py
```

to download sample youtube videos.

### Data for Testing
Sample videos are categorized based on difficulty:
- **Easy:** One person speaking directly to the camera.
- **Medium:** Two people talking with transitions between them.
- **Hard:** A moving camera scenario, such as a TED Talk video.

## Usage

## License
This project is licensed under the MIT License. See the LICENSE file for details.