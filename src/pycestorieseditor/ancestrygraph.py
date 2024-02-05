# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2024 bicobus <bicobus@keemail.me>
from itertools import chain
from textwrap import wrap

import matplotlib.pyplot as plt
import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar2Wx
from netgraph import Graph

from pycestorieseditor.ceevents import ancestry_instance
from pycestorieseditor.ceevents_template import Ceevent


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


def graph_event(panel, ceevent: Ceevent):
    figure = plt.figure()
    canvas = FigureCanvas(panel, -1, figure)
    toolbar = NavigationToolbar2Wx(canvas)
    toolbar.Realize()

    core_node = ancestry_instance.get(ceevent.name)
    nodes = [core_node.name] + list(set(core_node.parents_names() + core_node.children_names()))
    colors = {i: get_color(node, core_node) for i, node in enumerate(nodes)}

    edges = [
        n
        for n in chain(
            [(nodes.index(core_node.name), nodes.index(x)) for x in core_node.children_names()],
            [(nodes.index(x), nodes.index(core_node.name)) for x in core_node.parents_names()],
        )
    ]
    labels = {i: nwrap(lbl) for i, lbl in enumerate(nodes)}

    G = Graph(
        edges,
        nodes=range(len(nodes)),
        node_layout="spring",
        node_labels=labels,
        node_label_offset=0.05,
        node_label_fontdict={'size': 10},
        node_color=colors,
        arrows=True,
        edge_layout="curved",
    )

    # G = nx.DiGraph()
    # G.add_nodes_from(range(len(nodes)))
    # G.add_edges_from(edges)
    # pos = nx.nx_pydot.pydot_layout(G, prog="dot")
    # nx.draw(G, pos=pos, node_color=colors, labels=labels, node_size=800, node_shape="D")

    sizer = wx.BoxSizer(wx.VERTICAL)
    sizer.Add(canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
    sizer.Add(toolbar, 0, wx.EXPAND)
    panel.SetSizer(sizer)
