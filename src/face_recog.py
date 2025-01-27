import cv2
import json
import face_recognition
from scipy.spatial import distance
import os
import argparse
from tqdm import tqdm

def load_face_coordinates(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def encode_reference_image(reference_image_path):
    reference_image = face_recognition.load_image_file(reference_image_path)
    return face_recognition.face_encodings(reference_image)[0]

def group_consecutive_frames(frames):
    segments = []
    current_segment = []

    for i, frame in enumerate(frames):
        if i == 0 or frame[0] == frames[i - 1][0] + 1:
            current_segment.append(frame)
        else:
            segments.append(current_segment)
            current_segment = [frame]

    if current_segment:
        segments.append(current_segment)

    return segments

def process_video(video_path, face_coordinates, reference_encoding, output_dir, match_threshold, debug):
    video_capture = cv2.VideoCapture(video_path)

    # Initialize variables
    matched_frames = []
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    for face_data in tqdm(face_coordinates, desc="Processing frames"):
        frame_index = face_data['frame']
        faces = face_data['faces']

        # Capture the specific frame from the video
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = video_capture.read()
        if not ret:
            print(f"Failed to read frame {frame_index}")
            continue

        for i, face in enumerate(faces):
            x, y, w, h = face['x'], face['y'], face['width'], face['height']

            # Crop the face from the frame
            cropped_face = frame[y:y+h, x:x+w]

            # Save the cropped face for debugging if enabled
            if debug:
                debug_path = os.path.join(output_dir, "debug")
                os.makedirs(debug_path, exist_ok=True)
                debug_file = os.path.join(debug_path, f"frame_{frame_index}_face_{i}.png")
                cv2.imwrite(debug_file, cropped_face)

            # Convert the cropped face to RGB for face_recognition
            cropped_face_rgb = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)

            # Encode the cropped face
            face_encodings = face_recognition.face_encodings(cropped_face_rgb)

            if face_encodings:
                face_encoding = face_encodings[0]
                face_distance = distance.euclidean(reference_encoding, face_encoding)

                # Check if the face matches the reference image
                if face_distance < match_threshold:
                    matched_frames.append((frame_index, (x, y, w, h)))
                    break

    segments = group_consecutive_frames(matched_frames)

    # Save each segment as a video
    for idx, segment in enumerate(segments):
        output_path = os.path.join(output_dir, f"segment_{idx + 1}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = None

        final_w = sum([w for _, (_, _, w, _) in segment]) // len(segment)
        final_h = sum([h for _, (_, _, _, h) in segment]) // len(segment)
        for frame_index, (x, y, w, h) in segment:
            video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            ret, frame = video_capture.read()
            if ret:
                cropped_face = frame[y:y+h, x:x+w]
                cropped_face = cv2.resize(cropped_face, (final_w, final_h))

                # Initialize VideoWriter with the cropped size if not already initialized
                if out is None:
                    out = cv2.VideoWriter(output_path, fourcc, fps, (final_w, final_h))

                out.write(cropped_face)

        if out:
            out.release()

        if debug:
            print(f"Segment {idx + 1} contains {len(segment)} frames at {fps} FPS.")

        print(f"Saved video segment to {output_path}")

    video_capture.release()

def main():
    parser = argparse.ArgumentParser(description="Process a video to extract matched face segments.")
    parser.add_argument("--video_path", type=str, required=True, help="Path to the input video file.")
    parser.add_argument("--face_coordinates_path", type=str, required=True, help="Path to the face detection JSON file.")
    parser.add_argument("--reference_image_path", type=str, required=True, help="Path to the reference image file.")
    parser.add_argument("--output_dir", type=str, required=True, help="Directory to save the output video segments.")
    parser.add_argument("--match_threshold", type=float, default=0.7, help="Threshold for face matching. Default is 0.7.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode to save matching faces as images.")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    face_coordinates = load_face_coordinates(args.face_coordinates_path)
    reference_encoding = encode_reference_image(args.reference_image_path)

    process_video(
        video_path=args.video_path,
        face_coordinates=face_coordinates,
        reference_encoding=reference_encoding,
        output_dir=args.output_dir,
        match_threshold=args.match_threshold,
        debug=args.debug
    )

if __name__ == "__main__":
    main()
