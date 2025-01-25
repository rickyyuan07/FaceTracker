import os
from pytubefix import YouTube

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
        # Create output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Get the YouTube video
        yt = YouTube(video_url, 'WEB')

        # Get the highest resolution stream
        stream = yt.streams.get_highest_resolution()

        # Download the video
        print(f"Downloading video: {yt.title}")
        file_path = stream.download(output_folder)
        print(f"Video downloaded successfully: {file_path}")

        return file_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    # Example YouTube URL (replace with the video you want to download)
    # video_url = "https://www.youtube.com/watch?v=3iMc8uF46C0"
    # video_url = "https://www.youtube.com/watch?v=lXLBTBBil2U"
    video_url = "https://www.youtube.com/watch?v=EOZYI3F1g7c"

    # Call the download function
    download_youtube_video(video_url)
