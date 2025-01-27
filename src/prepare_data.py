import os
from pytubefix import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip

def download_youtube_video(video_url, output_folder="sample_data"):
    """
    Downloads a YouTube video to the specified output folder.

    Args:
        video_url (str): The URL of the YouTube video to download.
        output_folder (str): The folder where the video will be saved (default: "sample_data").

    Returns:
        str: The file path of the downloaded video.
    """
    try:
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        yt = YouTube(video_url, 'WEB')

        stream = yt.streams.get_highest_resolution()

        print(f"Downloading video: {yt.title}")
        file_path = stream.download(output_folder)
        print(f"Video downloaded successfully: {file_path}")

        return file_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def crop_video(video_path, start_time, end_time, output_path):
    """
    Crops a video to the specified time range and saves the cropped video.

    Args:
        video_path (str): Path to the input video file.
        start_time (int): Start time in seconds for cropping.
        end_time (int): End time in seconds for cropping.
        output_path (str): Path to save the cropped video.
    """
    video = VideoFileClip(video_path)
    cropped_video = video.subclipped(start_time, end_time)
    cropped_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"Video cropped and saved as: {output_path}")


if __name__ == "__main__":
    video_url_easy = "https://www.youtube.com/watch?v=3iMc8uF46C0" # I'm 40. If You're In Your 20's or 30's, Watch This
    video_url_easy2 = "https://www.youtube.com/watch?v=RDkTgc1SeYU" # Why Chinese Students study so hard
    video_url_medium = "https://www.youtube.com/watch?v=EOZYI3F1g7c" # Nvidia CEO Huang New Chips, AI, Musk, Meeting Trump
    video_url_hard = "https://www.youtube.com/watch?v=6Af6b_wyiwI" # The next outbreak? We’re not ready | Bill Gates | TED
    # video_url = "https://www.youtube.com/watch?v=lXLBTBBil2U"

    download_youtube_video(video_url_easy)
    download_youtube_video(video_url_easy2)
    download_youtube_video(video_url_medium)
    download_youtube_video(video_url_hard)

    # Crop the downloaded video to a specific time range
    video_path_easy = "./sample_data/I'm 40. If You're In Your 20's or 30's, Watch This.mp4"
    crop_video(video_path_easy, start_time=15, end_time=32, output_path="./sample_data/simon_easy1.mp4")

    video_path_medium = "./sample_data/Nvidia CEO Huang New Chips, AI, Musk, Meeting Trump.mp4"
    crop_video(video_path_medium, start_time=0, end_time=32, output_path="./sample_data/jensen_medium1.mp4")
    crop_video(video_path_medium, start_time=0, end_time=130, output_path="./sample_data/jensen_medium2.mp4")

    video_path_hard = "./sample_data/The next outbreak? We’re not ready | Bill Gates | TED.mp4"
    # crop_video(video_path_hard, start_time=0, end_time=32, output_path="./sample_data/bill_gates_hard1.mp4")
