import os
from pathlib import Path
from typing import Generator


def find_files(dir_path: str, file_types: tuple[str]) -> Generator[Path, None, None]:
    cwd = Path.cwd()
    os.chdir(dir_path)
    for image_type in file_types:
        yield from Path().rglob(image_type.lower())
        yield from Path().rglob(image_type.upper())
    os.chdir(cwd)
