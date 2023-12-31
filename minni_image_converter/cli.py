import argparse

from minni_image_converter.converter import batch_convert

parser = argparse.ArgumentParser(
    prog="IMAGE CONVERTER",
    description="Multiprocessing tool for fast resize and compress photos.",
)
parser.add_argument("-s", "--src", required=True)
parser.add_argument("-d", "--dst", required=True)
args = parser.parse_args()

if __name__ == "__main__":
    batch_convert(args.src, args.dst)
