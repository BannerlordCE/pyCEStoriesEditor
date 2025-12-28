# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2025-current bicobus <bicobus@keemail.me>

import contextlib
import logging
import os
from pathlib import Path

from platformdirs import user_config_path

logger = logging.getLogger(__name__)
__pkg_dir = os.path.dirname(__file__)

__pkg_config = {
    "confpath": Path(os.getcwd()),  # TODO might change when frozen
    "userconfpath": Path(user_config_path("pyCeStories")),
}
__pkg_config.update(
    {
        "settings": Path(__pkg_config["confpath"], "settings.conf"),
        "usersettings": Path(__pkg_config["userconfpath"], "settings.conf"),
    }
)


def get_config(name):
    with contextlib.suppress(KeyError):
        return __pkg_config[name]

    logger.warning("Trying to access non existing config attribute '%s'", name)
    return None
