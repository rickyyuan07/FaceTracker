import cv2
import os

def detect_faces_in_video(video_path, output_folder="output", cascade_path="haarcascade_frontalface_default.xml"):
    """
    Perform face detection on a video and save the processed video with bounding boxes.

    Args:
        video_path (str): Path to the input video file.
        output_folder (str): Folder to save the output video.
        cascade_path (str): Path to the Haar Cascade XML file for face detection.
    """
    # Load the Haar cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + cascade_path)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video.")
        return

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for output video

    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Output video path
    output_video_path = os.path.join(output_folder, "output_with_faces.mp4")
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Draw bounding boxes around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Write the processed frame to the output video
        out.write(frame)

        # Optionally display the frame (for debugging)
        cv2.imshow('Face Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    print(f"Face detection complete. Processed video saved at: {output_video_path}")

if __name__ == "__main__":
    # Input video path (replace with your video file path)
    video_path = "./sample_data/Nvidia CEO Huang New Chips, AI, Musk, Meeting Trump.mp4"

    # Perform face detection
    detect_faces_in_video(video_path)
