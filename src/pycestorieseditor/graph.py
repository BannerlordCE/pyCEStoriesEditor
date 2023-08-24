# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2023 bicobus <bicobus@keemail.me>

import re
import textwrap
import os

from graphviz import Digraph
from lxml import etree

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
    """List xml files in path"""
    for root, dirs, files in os.walk(path):
        print("\n".join(f"* {x}" for x in files))


def list_elements(xmlfile):
    """List event in xmlfile"""
    tree = etree.parse(xmlfile)
    xmlevents = tree.xpath('/CEEvents/CEEvent')
    for xmlevent in xmlevents:
        name = xmlevent.find("Name").text
        event = EventNode(name)
        event.unfurl_options(xmlevent.xpath("Options/Option"))
        events_list.append(event)


def graph_file(inputfile):
    g = Digraph("G", filename="out.gv")
    with g.subgraph(name=inputfile) as c:
        c.attr(color="black")
        for node in events_list:
            c.node(
                node.name, "\n".join(textwrap.wrap(node.name, 12)), shape=node._shape
            )
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
