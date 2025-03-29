import cv2
import os
import argparse
import subprocess

def resize_video(input_path, temp_output_path, width, height):
    cap = cv2.VideoCapture(input_path)

    if not cap.isOpened():
        print(f"❌ Error: Cannot open {input_path}")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 임시 파일은 기본 MP4 코덱
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_size = (width, height)

    out = cv2.VideoWriter(temp_output_path, fourcc, fps, frame_size)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        resized_frame = cv2.resize(frame, (width, height))
        out.write(resized_frame)

    cap.release()
    out.release()

def convert_to_h264(input_file, output_file):
    command = [
        "ffmpeg", "-i", input_file, "-c:v", "libx264", "-preset", "slow", "-crf", "23",
        "-c:a", "aac", "-b:a", "128k", output_file
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"✅ Converted to H.264: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Resize all MP4 videos and convert to H.264")
    parser.add_argument("folder", type=str, help="Folder containing videos")
    parser.add_argument("width", type=int, help="Target width")
    parser.add_argument("height", type=int, help="Target height")
    args = parser.parse_args()

    input_folder = os.path.abspath(args.folder)
    output_folder = os.path.join(input_folder, "resized_videos_h264")
    os.makedirs(output_folder, exist_ok=True)

    video_files = [f for f in os.listdir(input_folder) if f.endswith(".mp4")]

    if not video_files:
        print("⚠️ No MP4 files found in the folder.")
        return

    print(f"📂 Found {len(video_files)} videos. Resizing and converting to H.264...")

    for video in video_files:
        input_path = os.path.join(input_folder, video)
        temp_output_path = os.path.join(output_folder, f"temp_{video}")
        final_output_path = os.path.join(output_folder, f"resized_{video}")

        # Step 1: Resize with OpenCV
        resize_video(input_path, temp_output_path, args.width, args.height)

        # Step 2: Convert to H.264 using FFmpeg
        convert_to_h264(temp_output_path, final_output_path)

        # Step 3: Delete temporary file
        os.remove(temp_output_path)

    print("🎉 All videos resized and converted to H.264!")

if __name__ == "__main__":
    main()

