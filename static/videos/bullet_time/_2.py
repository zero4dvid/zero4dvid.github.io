import os
import sys
import subprocess

def resize_with_ffmpeg(input_path, output_path, width, height):
    cmd = [
        'ffmpeg',
        '-i', input_path,
        '-vf', f'scale={width}:{height}',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        '-c:a', 'copy',  # 오디오 스트림은 그대로 복사
        output_path
    ]
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[✓] Resized: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"[✗] Failed: {input_path}")

def find_and_resize_videos(root_dir, width, height):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(".mp4"):
                input_file = os.path.join(dirpath, filename)
                name, ext = os.path.splitext(filename)
                output_file = os.path.join(dirpath, f"{name}_resized{ext}")
                resize_with_ffmpeg(input_file, output_file, width, height)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python resize.py <root_dir> <width> <height>")
        sys.exit(1)

    root_directory = sys.argv[1]
    width = int(sys.argv[2])
    height = int(sys.argv[3])

    find_and_resize_videos(root_directory, width, height)

