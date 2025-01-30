import cv2
import json
import face_recognition
from scipy.spatial import distance
import os
import argparse
from tqdm import tqdm
from moviepy.video.io.VideoFileClip import VideoFileClip
import numpy as np


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


def smooth_bounding_boxes(segment, smoothing_window=5):
    smoothed_segment = []
    boxes = np.array([box for _, box in segment])

    # Apply moving average for each coordinate
    smoothed_x = np.convolve(boxes[:, 0], np.ones(smoothing_window) / smoothing_window, mode='same')
    smoothed_y = np.convolve(boxes[:, 1], np.ones(smoothing_window) / smoothing_window, mode='same')
    smoothed_w = np.convolve(boxes[:, 2], np.ones(smoothing_window) / smoothing_window, mode='same')
    smoothed_h = np.convolve(boxes[:, 3], np.ones(smoothing_window) / smoothing_window, mode='same')

    for i, (frame_index, _) in enumerate(segment):
        smoothed_segment.append((frame_index, (int(smoothed_x[i]), int(smoothed_y[i]), int(smoothed_w[i]), int(smoothed_h[i]))))

    return smoothed_segment


def save_video(video_path, segment, output_path, fps):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    final_w = sum([w for _, (_, _, w, _) in segment]) // len(segment)
    final_h = sum([h for _, (_, _, _, h) in segment]) // len(segment)
    out = cv2.VideoWriter(output_path, fourcc, fps, (final_w, final_h))

    video_capture = cv2.VideoCapture(video_path)

    for frame_index, (x, y, w, h) in segment:
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = video_capture.read()
        if ret:
            cropped_face = frame[y:y+h, x:x+w]
            cropped_face = cv2.resize(cropped_face, (final_w, final_h))
            out.write(cropped_face)

    out.release()
    video_capture.release()

def save_video_with_audio(video_path, segment, output_path, fps):
    temp_output = "temp_video.mp4"

    # Initialize VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    final_w = sum([w for _, (_, _, w, _) in segment]) // len(segment)
    final_h = sum([h for _, (_, _, _, h) in segment]) // len(segment)
    out = cv2.VideoWriter(temp_output, fourcc, fps, (final_w, final_h))

    video_capture = cv2.VideoCapture(video_path)

    for frame_index, (x, y, w, h) in segment:
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = video_capture.read()
        if ret:
            cropped_face = frame[y:y+h, x:x+w]
            cropped_face = cv2.resize(cropped_face, (final_w, final_h))
            out.write(cropped_face)

    out.release()
    video_capture.release()

    # Extract audio and merge it with the video segment
    start_time = segment[0][0] / fps
    end_time = segment[-1][0] / fps
    with VideoFileClip(video_path) as video:
        clip = video.subclipped(start_time, min(end_time, video.duration))

    with VideoFileClip(temp_output) as video_clip:
        video_clip.audio = clip.audio
        video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    os.remove(temp_output)


def process_video(video_path, face_coordinates, reference_encoding, output_dir, match_threshold, debug):
    video_capture = cv2.VideoCapture(video_path)

    matched_frames = []
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    for face_data in (face_coordinates if debug else tqdm(face_coordinates, desc="Processing frames")):
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

            # face_recognition library requires RGB format, openCV uses BGR
            cropped_face_rgb = cv2.cvtColor(cropped_face, cv2.COLOR_BGR2RGB)

            face_encodings = face_recognition.face_encodings(cropped_face_rgb, [(0, w, h, 0)], model="small")
            if face_encodings:
                face_encoding = face_encodings[0]
                face_distance = distance.euclidean(reference_encoding, face_encoding)

                if debug:
                    print(f"Frame {frame_index}: Face {i + 1} - Distance: {face_distance}")

                # Check if the face matches the reference image
                if face_distance < match_threshold:
                    matched_frames.append((frame_index, (x, y, w, h)))

                    # Save the cropped face for debugging if enabled
                    if debug:
                        debug_path = os.path.join(output_dir, "debug")
                        os.makedirs(debug_path, exist_ok=True)
                        debug_file = os.path.join(debug_path, f"frame_{frame_index}.png")
                        cv2.imwrite(debug_file, cropped_face)

                    break

    segments = group_consecutive_frames(matched_frames)

    print(f"Detected {len(segments)} face segments:", [len(segment) for segment in segments])

    metadata = {'file_name': video_path, 'segments': []}
    # Save each segment as a video with audio
    for idx, segment in enumerate(segments):
        segment = smooth_bounding_boxes(segment)

        # Generate metadata for the segment
        start_time = segment[0][0] / fps
        end_time = segment[-1][0] / fps
        metadata['segments'].append({
            "start_time": start_time,
            "end_time": end_time,
            "face_coordinates": segment
        })

        output_path = os.path.join(output_dir, f"segment_{idx + 1}.mp4")
        # save_video_with_audio(video_path, segment, output_path, fps)
        save_video(video_path, segment, output_path, fps)

        if debug:
            print(f"Segment {idx + 1} contains {len(segment)} frames at {fps} FPS.")

        print(f"Saved video segment to {output_path}")
    
    # Save metadata to JSON file
    metadata_path = os.path.join(output_dir, "metadata.json")
    with open(metadata_path, "w") as file:
        json.dump(metadata, file, indent=4)


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
