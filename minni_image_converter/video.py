from dataclasses import dataclass
from pathlib import Path
import subprocess

from minni_image_converter.find import find_files


VIDEO_TYPES = ("*.mp4",)


@dataclass
class Options:
    src: str = None
    dst: str = None


options = Options()


def convert(video_path: Path):
    src = Path(options.src, video_path)
    dst = Path(options.dst, video_path)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.is_file():
        if (input(f"{dst} already exists, overwrite it (y/n)? ")).lower() == "y":
            subprocess.run(f"ffmpeg -y -i {src} -c:v libx265 -c:a copy {dst}", shell=True)


def batch_convert(src_dir: str, dst_dir: str) -> None:
    options.src = src_dir
    options.dst = dst_dir
    files = list(find_files(src_dir, VIDEO_TYPES))
    total = len(files)

    for count, video_path in enumerate(files, start=1):
        print(f"Found video {count}/{total}: {video_path}")
        convert(video_path)
