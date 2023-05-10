# -*- coding: utf-8 -*-
# © 2023 bicobus <bicobus@keemail.me>
import logging
import os

CE_BASE_PATH = os.getenv("CE_BASE_PATH") or ""
CE_EXT_PATH = "ModuleLoader/CaptivityRequired/Events/"
CE_XSD_FILE = "CEEventsModal.xsd"
CE_TARGET_PATH = os.getenv("CE_TARGET_PATH")


logging.basicConfig(
    level=logging.ERROR,  # DEBUG,
)
logger = logging.getLogger(__name__)
