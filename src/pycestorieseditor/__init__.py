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

logging.basicConfig(
    level=logging.INFO,  # DEBUG,
    handlers=[
        logging.FileHandler(filename=os.path.join(os.getcwd(), "pce.log"), mode="w")
    ],
)
logger = logging.getLogger(__name__)
