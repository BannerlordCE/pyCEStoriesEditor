# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2024 bicobus <bicobus@keemail.me>
#
# to xml:
#   from xml.etree import ElementTree
#   ElementTree.tostring(xsd['CEEvents'].encode(doctree))
from __future__ import annotations

import inspect
import logging
import logging.handlers
import multiprocessing
import queue
import os
from collections import namedtuple
from xml.etree.ElementTree import ParseError as xmlParseError
from functools import lru_cache
from itertools import count, dropwhile
from pathlib import Path

from xsdata_attrs.bindings import XmlParser
import Refreshxmlschema

from pycestorieseditor.ceevents_template import Ceevent, SkillsRequired, SkillsToLevel, ReqHeroSkill
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
    return int(size / os.cpu_count()) + 1


event_ancestry_error = namedtuple("event_ancestry_error", ["source", "child", "filename"])


class EventAncestryErrors:
    def __init__(self):
        self._errors = []
        self._count = count()
        self._len = next(self._count)

    def register(self, error: event_ancestry_error):
        self._errors.append(error)
        self._len = next(self._count)

    def groupby(self, mode=None) -> list[event_ancestry_error]:
        if mode == "filename":
            return sorted(self._errors, key=lambda err: err.filename)
        return sorted(self._errors, key=lambda err: err.source)

    @property
    def len(self):
        return self._len


class AncestryNode:
    def __init__(self, ceeventref):
        self.name = ceeventref.name.value
        self._ceevent = ceeventref
        self._parents = []
        self._children = []

    def set_parent(self, node: AncestryNode):
        self._parents.append(node)

    def set_child(self, node: AncestryNode):
        if node in self._children:
            return
        self._children.append(node)
        node.set_parent(self)

    def is_graphable(self):
        return len(self._children) + len(self._parents) > 0

    @property
    def children(self):
        return self._children

    @property
    def parents(self):
        return self._parents

    @lru_cache
    def children_names(self):
        return [n.name for n in self._children]

    @lru_cache
    def parents_names(self):
        return [n.name for n in self._parents]


class Ancestry:
    def __init__(self):
        self._nodes: dict[str, AncestryNode] = {}

    def register(self, node: AncestryNode):
        """Register a Ceevent object, does nothing if it already exists"""
        if node.name not in self._nodes:
            self._nodes[node.name] = node

    def get(self, name: str) -> AncestryNode:
        return self._nodes[name]

    def set_child_node(self, name: str, node: AncestryNode):
        self._nodes[name].set_child(node)

    def set_child_node_from_name(self, name_parent: str, name_child: str):
        self._nodes[name_parent].set_child(self._nodes[name_child])


event_ancestry_errors = EventAncestryErrors()
ancestry_instance = Ancestry()


def find_by_name(name: str):
    global ebucket
    if name not in ebucket:
        return None
    return ebucket[name]


def _outboundevents(cevent: Ceevent, errors):
    """Yield outbout events from event ceevent"""
    for outboundevent in cevent.outboundevents:
        try:
            child = find_by_name(outboundevent.strip())
            if not child:
                raise ChildNotFound(outboundevent)
            yield child
        except ChildNotFound as e:
            event_ancestry_errors.register(
                event_ancestry_error(cevent.name.value, e.outboundevent, cevent.xmlfile)
            )
            next(errors)
            logger.error(
                "Child Not Found: Cannot find event with name '%s' in the bucket. (bound file '%s')",
                e.outboundevent,
                cevent.xmlfile,
            )


def populate_children():
    errors = count()
    bucket = get_ebucket()
    for cevent in bucket.values():
        for child in _outboundevents(cevent, errors):
            ancestry_instance.set_child_node_from_name(cevent.name.value, child.name.value)
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
    ('skills_to_level', "id"),
    ('skill', "id"),
)
SKIPELEM = ('value', 'restricted_list_of_flags')


def get_skill_value(ceevent, skill):
    if isinstance(skill, tuple):
        if not hasattr(ceevent, skill[0]):
            return None
        ceevent, skill = getattr(ceevent, skill[0]), skill[1]

    if hasattr(ceevent, skill):
        return getattr(ceevent, skill)
    return None


def get_skill_text_value(element):
    if isinstance(element, SkillsRequired):
        return [skill.id for skill in element.skill_required]
    if isinstance(element, SkillsToLevel):
        return [skill.id for skill in element.skill]
    if isinstance(element, ReqHeroSkill):
        return [element]
    raise Exception("element of type '%s' not handled" % type(element))


def filter_and_yield_skills(members, ceevent, cname):
    if any(x[0] in SKILLNAMES for x in members):
        for value in filter(
            lambda x: x is not None,
            (get_skill_value(ceevent, skillname) for skillname in SKILLNAMES),
        ):
            yield get_skill_text_value(value), cname


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
                        yield get_skill_text_value(skill), cname
                else:
                    yield get_skill_text_value(value), cname


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


def ce_module_name(path):
    p = Path(path)
    return p.parts[-3]


def ce_abbr_path(path):
    p = Path(path)
    return str(Path(*p.parts[-3:]))


class BigBagXml:
    def __init__(self):
        self._bad_xml = []

    def add_bad_xmlfile(self, xmlfile, msg):
        self._bad_xml.append((xmlfile, msg))

    def to_dict(self):
        return dict(zip(*zip(*self._bad_xml)))

    @property
    def bad_xml(self):
        return self._bad_xml

    def has_badxml(self):
        return False if not self._bad_xml else True

    def amount(self):
        return len(self._bad_xml)


def init_bigbadxml():
    global big_bad_xml
    big_bad_xml = BigBagXml()
    return big_bad_xml


def get_bigbadxml():
    global big_bad_xml
    return big_bad_xml


big_bad_xml: BigBagXml | None = None


def process_module(xmlfiles: list, cb=None):
    """Process the various xml files present in a given module

    Args:
        xmlfiles (list): list of paths leading to xml files
        cb: callback function
    """
    global ebucket, indexes

    parser = XmlParser()
    xsd = get_xsdfile()
    queuelog = multiprocessing.Manager().Queue(-1)
    queuecb = multiprocessing.Manager().Queue(-1)

    # Pool(processes) uses os.cpu_count() if none value is provided
    errcount = 0
    with multiprocessing.Pool() as pool:
        chunks = cpackage(len(xmlfiles))
        logger.info("Multiprocessing using %s chunks.", chunks)
        cb("Analyzing xml files...")
        res = pool.starmap_async(
            process_file,
            ((xmlfile, xsd, parser, queuelog, queuecb) for xmlfile in xmlfiles),
            chunksize=chunks,
        )
        try:
            timeout = None
            while fn := queuecb.get(timeout=timeout):
                timeout = 0.2
                cb(f"Processing {fn}...")
        except queue.Empty:
            ...

        qh = logging.handlers.QueueHandler(queuelog)
        mlogger = logging.getLogger(__name__)
        mlogger.addHandler(qh)

        for bucket, skills, errs in res.get():
            if errs:
                errcount += 1
                bbx = get_bigbadxml()
                bbx.add_bad_xmlfile(errs[0], errs[1])
                continue
            if cb:
                cb("Munching events ...")
            for ceevent in bucket:
                if ceevent.name.value in ebucket.keys():
                    mlogger.warning(
                        "Override of '%s' already present in bucket. (trigger: %s)",
                        ceevent.name.value,
                        ceevent.xmlfile,
                    )
                ebucket[ceevent.name.value] = ceevent
                ancestry_instance.register(AncestryNode(ceevent))
            if cb:
                cb("Munching skills...")
            for skill, eventname in skills:
                for s in skill:
                    skey = s.value if hasattr(s, 'value') else s
                    indexes['skills'].setdefault(skey, [])
                    indexes['skills'][skey].append(eventname)

    return errcount


def process_file(
    xmlfile, xsd, parser, queuelog, queuecb
) -> tuple[list[Ceevent], list, tuple | bool]:
    x = Path(xmlfile)
    qh = logging.handlers.QueueHandler(queuelog)
    mlogger = logging.getLogger(__name__)
    mlogger.addHandler(qh)
    mlogger.info("-start- %s", x.name)
    queuecb.put(x.name)
    bucket = []
    try:
        xsobjects = xsd.to_objects(xmlfile)
    except (
            xmlschema.validators.exceptions.XMLSchemaChildrenValidationError,
            xmlschema.validators.exceptions.XMLSchemaValidationError,
            xmlParseError
    ) as e:
        msg = e.reason if hasattr(e, 'reason') else e.msg
        # TODO: e.msg may not properly be displayed in wxString
        # print(e.msg)
        # print(e.path)
        # print(e.reason)
        mlogger.error("Invalid xml file: %s. Msg: %s", xmlfile, msg)
        mlogger.info("-stop- %s", x.name)
        return [], [], (xmlfile, msg)
    skills = []
    for event in xsobjects:
        string = event.tostring()
        ceevent: Ceevent = parser.from_string(string, Ceevent)
        ceevent.xmlsource = string
        ceevent.xmlfile = xmlfile
        skills = skills + list(filter_ceevent(ceevent, ceevent.name.value))
        bucket.append(ceevent)
    mlogger.info("-stop- %s", x.name)
    return bucket, skills, False


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
