from typing import NamedTuple


class Size(NamedTuple):
    width: int
    height: int


UHD = Size(3840, 2160)
DO_NOT_RESIZE_RATIO = 1.1


def get_new_size(size: Size) -> Size | None:
    ratio_width = size.width / UHD.width
    ratio_height = size.height / UHD.height
    ratio = max(ratio_width, ratio_height)
    if ratio < DO_NOT_RESIZE_RATIO:
        return
    width = round(size.width / ratio)
    height = round(size.height / ratio)
    return Size(width, height)
