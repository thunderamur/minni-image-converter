import functools
import hashlib
from multiprocessing import Pool, cpu_count
from pathlib import Path
from minni_image_converter.find import find_files


BUFFER_SIZE = 2^16


def get_hash(path: Path, hash_type=hashlib.blake2s):
    func = hash_type()
    with open(path, "rb") as f:
        while (block := f.read(BUFFER_SIZE)):
            func.update(block)
    return func.hexdigest()


def check_hash(src_dir: str, dst_dir: str, file: Path):
    if (get_hash(Path(src_dir) / file)) != get_hash(Path(dst_dir) / file):
        print(f"File {file} do not match")


def check(src_dir: str, dst_dir: str) -> None:
    src_files = set(find_files(src_dir))
    dst_files = set(find_files(dst_dir))

    if not_found_dst := src_files - dst_files:
        print(f"Not found in {dst_dir}:")
        for number, file in enumerate(not_found_dst):
            print(number, str(file))

    if not_found_src := dst_files - src_files:
        print(f"Not found in {src_dir}:")
        for number, file in enumerate(not_found_src):
            print(number, str(file))

    if not_found_dst or not_found_src:
        return

    print("All the filenames match. Started to compare hash sum")

    partial_check_hash = functools.partial(check_hash, src_dir, dst_dir)

    with Pool(cpu_count()) as p:
        p.map(partial_check_hash, src_files)