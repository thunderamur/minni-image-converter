import os
from pathlib import Path
from typing import Generator


def find_files(dir_path: str, file_types: tuple[str] | None = None) -> Generator[Path, None, None]:
    cwd = Path.cwd()
    os.chdir(dir_path)
    if file_types is None:
        for path in Path().rglob("*"):
            if path.is_file():
                yield path
    else:
        for image_type in file_types:
            yield from Path().rglob(image_type.lower())
            yield from Path().rglob(image_type.upper())
    os.chdir(cwd)
