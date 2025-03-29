import os
import cv2
import argparse
import imageio

def convert_mp4_to_gif(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    # 현재 폴더에서 모든 .mp4 파일 찾기
    mp4_files = [f for f in os.listdir(input_dir) if f.endswith('.mp4')]
    
    if not mp4_files:
        print("No MP4 files found.")
        return
    
    for mp4_file in mp4_files:
        mp4_path = os.path.join(input_dir, mp4_file)
        gif_filename = os.path.splitext(mp4_file)[0] + ".gif"
        gif_path = os.path.join(output_dir, gif_filename)
        
        cap = cv2.VideoCapture(mp4_path)
        frames = []
        success, frame = cap.read()
        
        while success:
            frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))  # 해상도 절반 축소
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # OpenCV는 BGR, GIF는 RGB 필요
            frames.append(frame)
            success, frame = cap.read()
        
        cap.release()
        
        if frames:
            imageio.mimsave(gif_path, frames, duration=0.1, loop=0, quantizer='nq')  # 프레임당 0.1초, 최적화 압축 적용
            print(f"Converted {mp4_file} to {gif_filename} with reduced size")
        else:
            print(f"No valid frames found in {mp4_file}")

def main():
    parser = argparse.ArgumentParser(description='Convert MP4 to GIF with size optimization')
    parser.add_argument('input_dir', type=str, help='Path to input directory')
    args = parser.parse_args()
    
    input_dir = os.path.abspath(args.input_dir)
    output_dir = os.path.join(input_dir, 'gif_output')
    
    convert_mp4_to_gif(input_dir, output_dir)

if __name__ == "__main__":
    main()

