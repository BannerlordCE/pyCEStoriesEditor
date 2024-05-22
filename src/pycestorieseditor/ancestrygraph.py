# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2024 bicobus <bicobus@keemail.me>
from itertools import chain
from textwrap import wrap

from pycestorieseditor.ceevents import ancestry_instance


def get_color(node, core):
    if node in core.parents_names():
        return "tab:red"
    if node in core.children_names():
        return "tab:blue"
    return "tab:green"


def nwrap(txt):
    if len(txt) > 20:
        return "\n".join(wrap(txt, 16))
    return txt


def build_graph(ceevent):
    core_node = ancestry_instance.get(ceevent.name.value)
    nodes = [core_node.name] + list(set(core_node.parents_names() + core_node.children_names()))
    colors = {i: get_color(node, core_node) for i, node in enumerate(nodes)}
    labels = {i: nwrap(lbl) for i, lbl in enumerate(nodes)}
    edges = [
        n
        for n in chain(
            [(nodes.index(core_node.name), nodes.index(x)) for x in core_node.children_names()],
            [(nodes.index(x), nodes.index(core_node.name)) for x in core_node.parents_names()],
        )
    ]
    return edges, nodes, colors, labels
