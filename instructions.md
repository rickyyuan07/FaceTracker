# Task Description

## Inputs
- A video file containing one or more people.
- A reference image of the target face that needs to be tracked and cropped.

## Outputs
- **Exact video clips** of the target face.
- **Metadata** for each cropped clip, including:
  - Timestamps (start and end times of the clip in the original video).
  - Face coordinates (bounding box for the face in each frame of the clip).

## Requirements
1. **Detect and track all faces** in the video and identify the target face based on the reference image.
2. **Track the target face** across frames to create continuous clips.
   - The tracked clips should not contain scene cuts/changes or full occlusions. If a scene change or full occlusion occurs, the clip should be split.
3. **Extract video clips** to include only the target face in each clip.
4. **Save the cropped videos** as individual files.
5. **Generate a metadata file** (e.g., JSON or CSV) that includes:
   - File name of the cropped video.
   - Start and end timestamps of the clip.
   - Frame-wise face coordinates (e.g., [x, y, width, height]).

---

## Deliverables

### 1. Public GitHub Repository
Your solution must include:

- **All source code** for the solution.
- A `README.md` file containing:
  - Instructions to set up and run your code.
  - Dependencies and installation steps.
  - Any assumptions or limitations of your solution.
  - Example commands or scripts to test the functionality.
- A folder containing:
  - The cropped video files.
  - The metadata file (e.g., JSON/CSV) for sample input(s).
- Sample input videos and reference images to demonstrate the functionality of your code.

### 2. Submission Instructions
- Push your solution to a **public GitHub repository** and share the link.
- Include some sample input videos and reference images in the repository to demonstrate the functionality of your code.
- Ensure that all dependencies are clearly listed in the `README.md` file, and include setup instructions (e.g., `requirements.txt` or `Dockerfile`).
- Grant access to [https://github.com/CharlyLx](https://github.com/CharlyLx).

---

### FAQ

**Q: Can they use a pretrained model, or does everything need to be done from scratch?**  
**A:** Yes, pretrained models can be used.

