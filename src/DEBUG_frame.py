import cv2
import os

def extract_and_detect_frame(video_path, frame_number, output_folder="debug", cascade_path="haarcascade_frontalface_default.xml"):
    """
    Extract a specific frame from a video, run face detection on it, display the result,
    and save the processed frame as an image.

    Args:
        video_path (str): Path to the input video file.
        frame_number (int): The frame number to extract and process.
        output_folder (str): Folder to save the output image.
        cascade_path (str): Path to the Haar Cascade XML file for face detection.
    """
    # Load the Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascade_path)

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    # Get total frame count
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_number >= total_frames or frame_number < 0:
        print(f"Error: Frame number {frame_number} is out of range. Total frames: {total_frames}")
        cap.release()
        return

    # Set the video to the desired frame number
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = cap.read()
    if not ret:
        print(f"Error: Unable to read frame {frame_number}.")
        cap.release()
        return

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw bounding boxes around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save the processed frame as an image
    output_image_path = os.path.join(output_folder, f"frame_{frame_number}_detected.jpg")
    cv2.imwrite(output_image_path, frame)

    # Display the processed frame
    cv2.imshow("Face Detection Result", frame)
    print(f"Processed frame saved at: {output_image_path}")

    # Wait for user to close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Release video capture
    cap.release()

if __name__ == "__main__":
    video_path = "./sample_data/jensen_medium1.mp4"
    frame_number = 185

    extract_and_detect_frame(video_path, frame_number)
