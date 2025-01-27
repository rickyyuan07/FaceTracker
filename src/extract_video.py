# Extract a single frame from the video
from moviepy.video.io.VideoFileClip import VideoFileClip
import imageio

video_path = "./sample_data/Nvidia CEO Huang New Chips, AI, Musk, Meeting Trump.mp4"
# Load the video file
video = VideoFileClip(video_path)

# Get the frame at XXX seconds
frame = video.get_frame(32)

# Save the frame as an image file
image_path = "./sample_data/extracted_frame.jpg"
imageio.imwrite(image_path, frame)

print(f"Frame extracted and saved as: {image_path}")