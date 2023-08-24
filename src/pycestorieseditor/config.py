# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2023 bicobus <bicobus@keemail.me>

import contextlib
import logging
import os

logger = logging.getLogger(__name__)
__pkg_dir = os.path.dirname(__file__)

__pkg_config = {
    'icons': os.path.join(__pkg_dir, "icons")
}


def get_config(name):
    with contextlib.suppress(KeyError):
        return __pkg_config[name]

    logger.warning("Trying to access non existing config attribute '%s'", name)
    return None
