import argparse
import sys

from transformations2log.transformations2log import transformations2log

try:
    from yaml import dump as dumper
except ImportError:
    dumper = print

parser = argparse.ArgumentParser(
    description="Extract the transformations from a PyTorch Training Script."
)

parser.add_argument("Path", metavar="path", type=str, help="Path to the script.")

parser.add_argument("-n", "--transformations_names", nargs="+", default=[])

args = parser.parse_args()

transformation_list = transformations2log(args.Path)

if args.transformations_names == []:
    data = {i: item for i, item in enumerate(transformation_list)}
else:
    data = {
        name: item
        for name, item in zip(args.transformations_names, transformation_list)
    }

dumper(data, sys.stdout)
