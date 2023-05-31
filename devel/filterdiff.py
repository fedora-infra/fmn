#!/usr/bin/env python3

# SPDX-FileCopyrightText: Contributors to the Fedora Project
#
# SPDX-License-Identifier: MIT

"""
Implement some parts of filterdiff in Python

The reason is that we can't install patchutils in the s2i container, it's not
running as root.
"""

import fileinput
from argparse import ArgumentParser
from fnmatch import fnmatch

import unidiff


def get_diff(files=None):
    diff = []
    for line in fileinput.input(files=files):
        diff.append(line)
    return "".join(diff)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-i", "--include", metavar="PAT", help="include only files matching PAT")
    parser.add_argument(
        "-p",
        "--strip-match",
        metavar="N",
        help="initial pathname components to ignore",
        type=int,
        default=0,
    )
    parser.add_argument("files", nargs="*")
    return parser.parse_args()


def main():
    args = parse_args()
    diff = get_diff(files=args.files)
    patch = unidiff.PatchSet(diff)
    for patched_file in patch[:]:
        filenames = [patched_file.source_file, patched_file.target_file]
        filenames = ["/".join(fn.split("/")[args.strip_match :]) for fn in filenames]
        if args.include and not all(fnmatch(fn, args.include) for fn in filenames):
            patch.remove(patched_file)
    print(patch)


if __name__ == "__main__":
    main()
