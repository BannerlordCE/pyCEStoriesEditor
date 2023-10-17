# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2023 bicobus <bicobus@keemail.me>
#
# to xml:
#   from xml.etree import ElementTree
#   ElementTree.tostring(xsd['CEEvents'].encode(doctree))
from __future__ import annotations

import logging
import multiprocessing
import os
import time
from functools import lru_cache
from itertools import count
from pathlib import Path

from xsdata_attrs.bindings import XmlParser
import xmlschema

from .ceevents_template import Ceevent

logger = logging.getLogger(__name__)


def create_ebucket():
    global ebucket
    ebucket = {}
    return ebucket


def get_ebucket():
    global ebucket
    return ebucket


ebucket: dict[str, Ceevent] | None = None  # pylint: disable=invalid-name


def init_xsdfile(pathname):
    global xsdfile
    xsdfile = xmlschema.XMLSchema(pathname)
    return xsdfile


def get_xsdfile():
    global xsdfile
    return xsdfile


xsdfile: xmlschema.XMLSchema | None = None


class ElementNotFound(Exception):
    ...


class TypeNotFound(Exception):
    ...


class EventNotFound(Exception):
    ...


class ChildNotFound(Exception):
    def __init__(self, outboundevent, msg=None):
        super().__init__(msg)
        self.outboundevent = outboundevent


@lru_cache
def cpackage(size):
    return int(size / os.cpu_count()) - 1


def find_by_name(name: str):
    global ebucket
    for cevent in ebucket.values():
        if cevent.name.value == name:
            return cevent
    return None


def _outboundevents(cevent: Ceevent):
    for outboundevent in cevent.outboundevents:
        child = find_by_name(outboundevent.strip())
        if not child:
            raise ChildNotFound(outboundevent)
        yield child


def populate_children(bucket):
    print(f"start: {time.strftime('%X')}")
    errors = count()
    for cevent in bucket.values():
        try:
            for child in _outboundevents(cevent):
                cevent.set_child_node(child)
        except ChildNotFound as e:
            logger.error(
                "Child Not Found: Cannot find event with name '%s' in the bucket. (bound file '%s')",
                e.outboundevent, cevent.xmlfile
            )
    print(f"end: {time.strftime('%X')}")
    return next(errors)


def process_xml_files(xmlfiles: list):
    global ebucket

    parser = XmlParser()
    xsd = get_xsdfile()

    # Pool(processes) uses os.cpu_count() if none value is provided
    with multiprocessing.Pool(multiprocessing.cpu_count() - 1) as pool:
        res = pool.starmap(process_file, ((xmlfile, xsd, parser) for xmlfile in xmlfiles), chunksize=4)

    for bucket in res:
        for ceevent in bucket:
            if ceevent.name.value in ebucket.keys():
                logger.warning("Override of '%s' already present in bucket. (trigger: %s)", ceevent.name.value, ceevent.xmlfile)
            ebucket[ceevent.name.value] = ceevent


def process_file(xmlfile, xsd, parser) -> list[Ceevent]:
    x = Path(xmlfile)
    logger.info(f"-start- {x.name}: {time.strftime('%X')}")
    bucket = []
    try:
        xsobjects = xsd.to_objects(xmlfile)
    except xmlschema.validators.exceptions.XMLSchemaChildrenValidationError as e:
        logger.error("Invalid xml file: %s. Msg: %s", xmlfile, e.reason)
        return []
    for event in xsobjects:
        string = event.tostring()
        ceevent = parser.from_string(string, Ceevent)
        ceevent.xmlsource = string
        ceevent.xmlfile = xmlfile
        bucket.append(ceevent)
    logger.info(f"-stop- {x.name}: {time.strftime('%X')}")
    return bucket


def process_xml_events(xmlfile):
    parser = XmlParser()
    xmlfile = Path(xmlfile)
    xsd = get_xsdfile()
    if not xsd:
        logger.error("No xsd file exists. Was it saved?")
        return -1
    xsobjects = xsd.to_objects(xmlfile)
    ebucket = get_ebucket()
    for event in xsobjects:
        string = event.tostring()
        ceevent = parser.from_string(string, Ceevent)
        ceevent.xmlsource = string
        if ceevent.name.value in ebucket.keys():
            logger.warning("'%s' already present in bucket.", ceevent.name.value)
            return 0
        ebucket[ceevent.name.value] = ceevent
    return 1


class NotBannerLordModule(Exception):
    ...


class NotCeSubmodule(Exception):
    ...


class CePath:
    def __init__(self, path):
        self._path = Path(path)
        self._submodule = Path(self._path, "SubModule.xml")
        self._events = Path(self._path, "Events")
        self._name = None
        if not self._submodule.exists() and not self._events.exists():
            raise NotBannerLordModule(f"Directory '{self._path}' is not a BannerLord module.")

        if self._submodule.exists():
            if not self.validate_submodule():
                raise NotCeSubmodule(f"{self._path}")
        else:
            self._name = self._path.name

    def validate_submodule(self):
        xmlresource = xmlschema.XMLResource(self._submodule)
        self._name = xmlresource.find("//Name").attrib['value']
        return any(
            e.attrib["Id"] == "zCaptivityEvents"
            for e in xmlresource.iterfind("//DependedModules/DependedModule[@Id]")
        )

    def __str__(self):
        return str(self._path)

    @property
    def name(self):
        return self._name

    @property
    def events(self):
        for f in self._events.glob('*.xml'):
            yield str(f)
