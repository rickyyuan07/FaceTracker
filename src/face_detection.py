import cv2
import os
import json
import argparse

def detect_faces_in_video(video_path, output_folder="output", cascade_path="haarcascade_frontalface_default.xml", debug=False):
    """
    Perform face detection on a video, save the processed video with bounding boxes,
    and generate a JSON file with frame-wise face coordinates.

    Args:
        video_path (str): Path to the input video file.
        output_folder (str): Folder to save the output video and JSON file.
        cascade_path (str): Path to the Haar Cascade XML file for face detection.
        debug (bool): If True, visualize face detection during processing.
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

    # JSON file path
    json_file_path = os.path.join(output_folder, "face_coordinates.json")
    face_data = []  # List to store face detection data

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5, minSize=(30, 30))

        # Store face data for the current frame
        frame_faces = []
        for (x, y, w, h) in faces:
            frame_faces.append({"x": int(x), "y": int(y), "width": int(w), "height": int(h)})
            # Draw bounding boxes around detected faces if debug mode is enabled
            if debug:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        face_data.append({"frame": frame_count, "faces": frame_faces})
        frame_count += 1
        out.write(frame)

        # Optionally display the frame (for debugging)
        if debug:
            cv2.imshow('Face Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Release resources
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    # Save face data to JSON file
    with open(json_file_path, "w") as json_file:
        json.dump(face_data, json_file, indent=4)

    print(f"Face detection complete. Processed video saved at: {output_video_path}")
    print(f"Face data saved to JSON file: {json_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Face detection on a video file.")
    parser.add_argument("--video_path", type=str, help="Path to the input video file.")
    parser.add_argument("--output_folder", type=str, default="output", help="Folder to save the output video and JSON file.")
    parser.add_argument("--cascade_path", type=str, default="haarcascade_frontalface_default.xml", help="Path to the Haar Cascade XML file.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode to visualize face detection.")

    args = parser.parse_args()

    detect_faces_in_video(
        video_path=args.video_path,
        output_folder=args.output_folder,
        cascade_path=args.cascade_path,
        debug=args.debug
    )
