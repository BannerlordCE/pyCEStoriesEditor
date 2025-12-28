# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2025-current bicobus <bicobus@keemail.me>

import argparse
import multiprocessing
import sys

from wx import version

from pycestorieseditor.wxlaunch import launch


def main():
    parser = argparse.ArgumentParser(
        prog="pycestorieseditor",
        epilog="Running wxPython %s" % version()
    )
    parser.add_argument(
        "-s", "--settings", action="store_true", required=False,
        help="Launch the settings window. Implies -g."
    )
    args = parser.parse_args()
    launch(args.settings)


if __name__ == '__main__':
    if getattr(sys, "frozen", False):
        multiprocessing.freeze_support()
    main()
