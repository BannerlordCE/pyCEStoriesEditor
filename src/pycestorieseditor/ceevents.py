# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2023 bicobus <bicobus@keemail.me>
#
# to xml:
#   from xml.etree import ElementTree
#   ElementTree.tostring(xsd['CEEvents'].encode(doctree))
from __future__ import annotations

import inspect
import logging
import multiprocessing
import os
import time
from functools import lru_cache
from itertools import count, dropwhile
from pathlib import Path

from xsdata_attrs.bindings import XmlParser
import xmlschema

from pycestorieseditor.ceevents_template import Ceevent, SkillsRequired, SkillsToLevel
from pycestorieseditor.pil2wx import default_background

logger = logging.getLogger(__name__)


def create_ebucket():
    global ebucket
    ebucket = {}
    return ebucket


def get_ebucket():
    global ebucket
    return ebucket


def create_imgbucket():
    global imgbucket
    imgbucket = {None: default_background()}
    return imgbucket


def get_imgbucket():
    global imgbucket
    return imgbucket


def init_index():
    global indexes
    indexes = {'skills': {}}
    return indexes


def get_indexes():
    global indexes
    return indexes


ebucket: dict[str, Ceevent] | None = None  # pylint: disable=invalid-name
imgbucket: dict[str, os.PathLike] | None = None  # pylint: disable=invalid-name
indexes: dict[str, dict] | None = None  # pylint: disable=invalid-name


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
                e.outboundevent,
                cevent.xmlfile,
            )
    print(f"end: {time.strftime('%X')}")
    return next(errors)


def scan_for_images(module_path):
    module_path = Path(module_path)
    ibucket = get_imgbucket()
    for img in module_path.glob('Images/**/*.png'):
        key = img.name.replace('.png', '')
        if key in ibucket:
            logger.warning(
                "Override of key '%s' with file of module %s.", key, module_path.resolve().name
            )
        ibucket[key] = img


SKILLNAMES = (
    'req_captor_skill',
    'req_hero_skill',
    'skill_to_level',  # XXX: is a list in MenuOptions?!? Not used in the wild.
    'skills_required',
    'skills_to_level',
)
SKIPELEM = ('value', 'restricted_list_of_flags')


def get_skill_value(ceevent, skill):
    if elem := getattr(ceevent, skill):
        return elem


def get_skill_text_value(element):
    if isinstance(element, SkillsRequired):
        return (skill.id for skill in element.skill_required)
    if isinstance(element, SkillsToLevel):
        return (skill.id for skill in element.skill)
    raise Exception("element of type '%s' not handled" % type(element))


def filter_and_yield_skills(members, ceevent, cname):
    if any(x[0] in SKILLNAMES for x in members):
        for value in filter(
            lambda x: x is not None,
            (get_skill_value(ceevent, skillname) for skillname in SKILLNAMES),
        ):
            yield [x for x in get_skill_text_value(value)], cname


def filter_and_yield_from_options(members, ceevent, cname):
    name = ["options", "menu_options"]
    subname = {"options": "option", "menu_options": "menu_option"}
    for otree in (x[0] for x in filter(lambda x: x[0] in name, members)):
        options = getattr(ceevent, otree)
        if not options:
            return
        for option in getattr(options, subname[otree]):
            for value in filter(
                lambda x: x is not None,
                (get_skill_value(option, skillname) for skillname in SKILLNAMES),
            ):
                if otree == "menu_options":
                    for skill in value:
                        yield [x for x in get_skill_text_value(skill)], cname
                else:
                    yield [x for x in get_skill_text_value(value)], cname


def filter_ceevent(ceevent: Ceevent, ceeventname):
    if not ceevent or isinstance(ceevent, (str, int, list, float)):
        return None
    members = dropwhile(
        lambda x: x[0][0] == '_',
        inspect.getmembers_static(
            ceevent, lambda x: inspect.ismemberdescriptor(x) or isinstance(x, str)
        ),
    )
    members = list(members)
    for name, cname in filter_and_yield_skills(members, ceevent, ceeventname):
        yield name, cname
    for name, cname in filter_and_yield_from_options(members, ceevent, ceeventname):
        yield name, cname
    for name, cname in filter_and_yield_from_options(members, ceevent, ceeventname):
        yield name, cname


def process_xml_files(xmlfiles: list):
    global ebucket, indexes

    parser = XmlParser()
    xsd = get_xsdfile()

    # Pool(processes) uses os.cpu_count() if none value is provided
    with multiprocessing.Pool() as pool:
        res = pool.starmap(
            process_file, ((xmlfile, xsd, parser) for xmlfile in xmlfiles), chunksize=4
        )

    for bucket, skills in res:
        for ceevent in bucket:
            if ceevent.name.value in ebucket.keys():
                logger.warning(
                    "Override of '%s' already present in bucket. (trigger: %s)",
                    ceevent.name.value,
                    ceevent.xmlfile,
                )
            ebucket[ceevent.name.value] = ceevent
        for skill, eventname in skills:
            for s in skill:
                indexes['skills'].setdefault(s, [])
                indexes['skills'][s].append(eventname)


def process_file(xmlfile, xsd, parser) -> tuple[list[Ceevent], list] | list:
    x = Path(xmlfile)
    logger.info(f"-start- {x.name}: {time.strftime('%X')}")
    bucket = []
    try:
        xsobjects = xsd.to_objects(xmlfile)
    except xmlschema.validators.exceptions.XMLSchemaChildrenValidationError as e:
        logger.error("Invalid xml file: %s. Msg: %s", xmlfile, e.reason)
        return []
    skills = []
    for event in xsobjects:
        string = event.tostring()
        ceevent: Ceevent = parser.from_string(string, Ceevent)
        ceevent.xmlsource = string
        ceevent.xmlfile = xmlfile
        skills = skills + [x for x in filter_ceevent(ceevent, ceevent.name.value)]
        bucket.append(ceevent)
    logger.info(f"-stop- {x.name}: {time.strftime('%X')}")
    return bucket, skills


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
    def events_files(self):
        for f in self._events.glob('*.xml'):
            yield str(f)
