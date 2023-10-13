# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2023 bicobus <bicobus@keemail.me>
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
)
logger = logging.getLogger(__name__)
