# -*- coding: utf-8 -*-
# © 2023 bicobus <bicobus@keemail.me>

import argparse
import os
import re
import sys
import textwrap

from graphviz import Digraph
from lxml import etree

CE_BASE_PATH = os.getenv("CE_BASE_PATH") or ""
CE_EXT_PATH = "ModuleLoader/CaptivityRequired/Events/"
CE_XSD_FILE = "CEEventsModal.xsd"
CE_TARGET_PATH = os.getenv("CE_TARGET_PATH")

events_list = []


class OptionNode:
    _shape = "diamond"
    _style = "filled"
    _color = "lightgrey"

    def __init__(self, name, parent, target_events):
        self.name = name
        self.parent = parent
        self.target_events = target_events

    def option_events_as_pair(self):
        return [(self.name, x) for x in self.target_events]


class EventNode:
    _shape = "ellipse"
    _style = None
    _color = None

    def __init__(self, name):
        self.name = name
        self.children = set()
        self.options = []

    def unfurl_options(self, options):
        for option in options:
            option_text = re.sub(r"\{=[^}]+\}", "", option.find("OptionText").text)
            option_events = option.xpath("TriggerEvents/TriggerEvent/EventName/text()")
            option_events.extend(option.xpath("TriggerEventName/text()"))
            self.options.append(OptionNode(option_text, self, option_events))
            self.children |= set(option_events)

    def children_as_nodes(self):
        output = []
        for node in filter(lambda x: x.name in self.children, events_list):
            output.append(node)
        return output

    def __repr__(self):
        return "{}: {}".format(self.name, list(self.children))


def list_files(path):
    "List xml files in path"
    for root, dirs, files in os.walk(path):
        print("\n".join(f"* {x}" for x in files))


def list_elements(xmlfile):
    "List event in xmlfile"
    tree = etree.parse(xmlfile)
    xmlevents = tree.xpath('/CEEvents/CEEvent')
    for xmlevent in xmlevents:
        name = xmlevent.find("Name").text
        event = EventNode(name)
        event.unfurl_options(xmlevent.xpath("Options/Option"))
        events_list.append(event)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog="pycestorieseditor",
    )
    parser.add_argument(
        'inputfile', metavar="file", nargs="?",
        help="input xml file to be parsed"
    )
    parser.add_argument(
        "-t", "--target", required=False,
        help="If unset, env variable CE_TARGET_PATH will be read. If empty, software "
             "will fail."
    )
    parser.add_argument(
        "-l", "--list", action="store_true", required=False
    )
    args = parser.parse_args()
    if not args.target:
        if not CE_TARGET_PATH:
            print("err")
            sys.exit(0)
        target = CE_TARGET_PATH
    else:
        target = args.target
    if not os.path.exists(target):
        print(f"No such folder: '{target}'", file=sys.stderr)
        sys.exit(1)

    if args.list:
        list_files(target)
        sys.exit()

    if not args.inputfile:
        print("A xml file is required.", file=sys.stderr)
        sys.exit(1)

    list_elements(os.path.join(target, args.inputfile))
    # print(events_list)
    g = Digraph("G", filename="out.gv")
    with g.subgraph(name=args.inputfile) as c:
        c.attr(color="black")
        for node in events_list:
            c.node(node.name, "\n".join(textwrap.wrap(node.name, 12)), shape=node._shape)
            if node.options:
                for option in node.options:
                    c.node(
                        option.name,
                        "\n".join(textwrap.wrap(option.name, 12)),
                        shape=option._shape,
                        color=option._color,
                        style=option._style,
                    )
                    c.edge(node.name, option.name)
                    c.edges(option.option_events_as_pair())
            # if node.children:
            #     for x in node.children_as_nodes():
            #         c.edge(node.name, x.name)

    g.view()
