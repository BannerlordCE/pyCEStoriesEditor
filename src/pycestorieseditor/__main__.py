# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2023 bicobus <bicobus@keemail.me>

import argparse

from pycestorieseditor.wxlaunch import launch


def main():
    parser = argparse.ArgumentParser(
        prog="pycestorieseditor",
    )
    parser.add_argument(
        "-g", "--gui", action="store_true", required=False,
        help="Launch the GUI, ignore all other argument."
    )
    parser.add_argument(
        "-s", "--settings", action="store_true", required=False,
        help="Launch the settings window. Implies -g."
    )
    args = parser.parse_args()
    launch(args.settings)


if __name__ == '__main__':
    main()
