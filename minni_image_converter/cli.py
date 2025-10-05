import argparse

from minni_image_converter import image, video, diff

parser = argparse.ArgumentParser(
    prog="IMAGE CONVERTER",
    description="Multiprocessing tool for fast resize and compress photos.",
)
parser.add_argument("--diff", action="store_true")
parser.add_argument("--src", required=True)
parser.add_argument("--dst", required=True)
args = parser.parse_args()

if __name__ == "__main__":
    if args.diff:
        diff.check(args.src, args.dst)
    else:
        image.batch_convert(args.src, args.dst)
        video.batch_convert(args.src, args.dst)
