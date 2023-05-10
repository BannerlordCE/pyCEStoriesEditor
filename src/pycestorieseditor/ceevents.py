# -*- coding: utf-8 -*-
# © 2023 bicobus <bicobus@keemail.me>
#
# to xml:
#   from xml.etree import ElementTree
#   ElementTree.tostring(xsd['CEEvents'].encode(doctree))
from __future__ import annotations

import logging

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


class ElementNotFound(Exception):
    ...


class TypeNotFound(Exception):
    ...


class EventNotFound(Exception):
    ...


def find_by_name(name):
    global ebucket
    for cevent in ebucket.values():
        if cevent.name == name:
            return cevent
    return None


def populate_children():
    global ebucket
    for cevent in ebucket.values():
        for outboundevent in cevent.outboundevents:
            child = find_by_name(outboundevent)
            if not child:
                # raise EventNotFound(
                logger.error(
                    "Cannot find event with name '%s' in the bucket.",
                    outboundevent
                )
                continue
            cevent.set_child_node(child)


def process_file(xmlfile, xsdfile):
    parser = XmlParser()
    xsd = xmlschema.XMLSchema(xsdfile)
    xsobjects = xsd.to_objects(xmlfile)
    create_ebucket()
    for event in xsobjects:
        string = event.tostring()
        ceevent = parser.from_string(string, Ceevent)
        ceevent.xmlsource = string
        if ceevent.name.value in ebucket.keys():
            return
        ebucket[ceevent.name.value] = ceevent

    populate_children()
