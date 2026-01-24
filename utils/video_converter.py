import imageio_ffmpeg
import subprocess

def convert_webm_to_mp4(input_path, output_path):
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg,
        "-y",
        "-i", input_path,
        "-movflags", "+faststart",
        "-pix_fmt", "yuv420p",
        output_path
    ]
    subprocess.run(cmd, check=True)
