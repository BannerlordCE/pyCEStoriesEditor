# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2024 bicobus <bicobus@keemail.me>
from __future__ import annotations

import logging
import os

CE_BASE_PATH = os.getenv("CE_BASE_PATH") or ""
CE_EXT_PATH = "ModuleLoader/CaptivityRequired/Events/"
CE_XSD_FILE = "CEEventsModal.xsd"
CE_TARGET_PATH = os.getenv("CE_TARGET_PATH")
PORTABLE = True
APPNAME = "pyCeStoriesViewer"

logging_file_handler = logging.FileHandler(filename=os.path.join(os.getcwd(), "pce.log"), mode="w")
logging.basicConfig(
    level=logging.INFO,  # DEBUG,
    handlers=[
        logging_file_handler,
        # logging.StreamHandler()
    ],
    format="%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s"
)
logger = logging.getLogger(__name__)
