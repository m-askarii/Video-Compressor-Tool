# python -m pip install ffmpeg-python -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn --timeout 120 --retries 10

import ffmpeg
import os
import sys
import shutil

def check_ffmpeg():
    if shutil.which("ffmpeg") is None:
        print("ERROR: FFmpeg is not installed or not in PATH.")
        return False
    return True

def compress_video(input_path, output_path, crf=28, preset="medium"):
    if not os.path.exists(input_path):
        print(f"ERROR: File not found → {input_path}")
        return False

    try:
        (
            ffmpeg
            .input(input_path)
            .output(
                output_path,
                vcodec="libx264",
                crf=crf,
                preset=preset,
                acodec="aac",
                audio_bitrate="128k"
            )
            .overwrite_output()
            .run(quiet=True)
        )
        return True
    except ffmpeg.Error as e:
        print("ERROR: Failed to process video:")
        print(e.stderr.decode())
        return False

def main():
    if not check_ffmpeg():
        return

    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else "output_compressed.mp4"
    else:
        input_file = input("📂 Input video path: ").strip().strip('"').strip("'")
        output_file = input("📁 Output path (empty = default): ").strip().strip('"').strip("'")
        if not output_file:
            output_file = "output_compressed.mp4"

    if not input_file:
        print("ERROR: No input file provided.")
        return

    print(f"Compressing: {input_file}")
    ok = compress_video(input_file, output_file)

    if ok:
        before = os.path.getsize(input_file) / (1024 * 1024)
        after = os.path.getsize(output_file) / (1024 * 1024)
        print("Finished 🔚")
        print(f"◀️ Before: {before:.2f} MB")
        print(f"⏭️ After: {after:.2f} MB")
        if before > 0:
            print(f"🤏 Decrease: {100 - (after/before*100):.1f}%")
    else:
        print("Compression failed.")