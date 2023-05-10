# -*- coding: utf-8 -*-
# © 2023 bicobus <bicobus@keemail.me>

import argparse
import os
import sys

from . import CE_TARGET_PATH
from .graph import graph_file, list_elements, list_files
from .ui import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="pycestorieseditor",
    )
    parser.add_argument(
        'inputfile', metavar="file", nargs="?",
        help="input xml file to be parsed"
    )
    parser.add_argument(
        "-t", "--target", required=False,
        help="If unset, env variable CE_TARGET_PATH will be read. If empty, software "
             "will fail."
    )
    parser.add_argument(
        "-l", "--list", action="store_true", required=False,
    )
    parser.add_argument(
        "-g", "--gui", action="store_true", required=False,
    )
    args = parser.parse_args()

    if not args.target:
        if not CE_TARGET_PATH:
            print("err")
            sys.exit(0)
        target = CE_TARGET_PATH
    else:
        target = args.target
    if not os.path.exists(target):
        print(f"No such folder: '{target}'", file=sys.stderr)
        sys.exit(1)

    if args.list:
        list_files(target)
        sys.exit()

    if not args.inputfile:
        print("A xml file is required.", file=sys.stderr)
        sys.exit(1)

    if args.gui:
        main(os.path.join(target, args.inputfile))
        sys.exit()
    list_elements(os.path.join(target, args.inputfile))
    # print(events_list)
    graph_file(args.inputfile)
