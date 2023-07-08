import logging
import multiprocessing as mp
import os
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from queue import Empty
from typing import Generator

from PIL import Image

from minni_image_converter.size import Size, get_new_size

IMAGE_TYPES = ("*.jpg",)


@dataclass
class Options:
    src: str = None
    dst: str = None


options = Options()


def find_images(dir_path: str) -> Generator[Path, None, None]:
    cwd = Path.cwd()
    os.chdir(dir_path)
    for image_type in IMAGE_TYPES:
        yield from Path().rglob(image_type.lower())
        yield from Path().rglob(image_type.upper())
    os.chdir(cwd)


def convert(image_path: Path):
    src = Path(options.src, image_path)
    dst = Path(options.dst, image_path)
    dst.parent.mkdir(parents=True, exist_ok=True)
    image = Image.open(src)
    if new_size := get_new_size(Size(image.width, image.height)):
        image = image.resize(new_size, resample=Image.Resampling.LANCZOS)
    image.save(dst.with_suffix(".webp"))


def convert_task(image_queue: mp.Queue) -> None:
    while True:
        try:
            convert(image_queue.get_nowait())
        except Empty:
            break
        except Exception as e:
            logging.exception(str(e))


def progress_task(image_queue: mp.Queue, total: int) -> None:
    print("Starting convertation...")
    while True:
        print(f"{total - image_queue.qsize()}/{total}")
        if image_queue.empty():
            break
        time.sleep(1)


def batch_convert(src_dir: str, dst_dir: str) -> None:
    options.src = src_dir
    options.dst = dst_dir
    image_queue = mp.Queue()

    for count, image_path in enumerate(find_images(src_dir), start=1):
        print(f"Found image {count}: {image_path}")
        image_queue.put(image_path)

    image_count = image_queue.qsize()
    if not image_count:
        print(f"Images not found in {options.src}")
        return

    progress_thread = threading.Thread(
        target=progress_task, args=(image_queue, image_queue.qsize())
    )
    progress_thread.start()

    processes = []

    process_count = min(mp.cpu_count(), image_count)
    for _ in range(process_count):
        p = mp.Process(target=convert_task, args=(image_queue,))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    progress_thread.join()
