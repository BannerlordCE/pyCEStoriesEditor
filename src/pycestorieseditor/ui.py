# -*- coding: utf-8 -*-
# © 2023 bicobus <bicobus@keemail.me>
from __future__ import annotations

import logging
import os
import tkinter as tk
from contextlib import suppress
from idlelib.tooltip import Hovertip
from tkinter import ttk, font
from tkinter.scrolledtext import ScrolledText

from attrs import astuple
from pygments import lex
from pygments.lexers.html import XmlLexer
from pygments.styles import get_style_by_name

from . import CE_XSD_FILE
from .ceevents import get_ebucket, process_file
from .ceevents_template import RestrictedListOfFlagsType, Ceevent
from .config import get_config

logger = logging.getLogger(__name__)


def label_entry(parent, label, content, row=0, column=0):
    label = ttk.Label(parent, text=label)
    label.grid(row=row, column=column, sticky="nsew")
    entrytxt = tk.StringVar(parent, content)
    entry = ttk.Entry(parent, textvariable=entrytxt)
    entry.textref = entrytxt  # create a reference to avoid the GC
    entry.grid(row=row, column=column + 1, columnspan=3, sticky="nw")
    return label, entry


def label_mentries(parent, label, content, row):
    if not isinstance(content, list):
        logger.warning(
            "Trying to build a multi dimensional entry without a list."
        )
    label = ttk.Label(parent, text=label)
    label.grid(row=row, rowspan=len(content), column=0, sticky="nw")
    entries = []
    for i, c in enumerate(content):
        i = i - 1
        entrytxt = tk.StringVar(parent, c)
        entry = ttk.Entry(parent, textvariable=entrytxt)
        entry.textref = entrytxt  # create a reference to avoid the GC
        entry.grid(row=row + i, column=1, columnspan=3, sticky="nw")
        entries.append(entry)
    return label, entries


def label_backgrounds(parent, label, bg, row):
    frame = ttk.Frame(parent)
    frame.grid(row=row, column=0, columnspan=2, sticky="nsew")

    label = ttk.Label(frame, text=label)
    label.pack(fill=tk.X)

    columns = ("name", "weight", "use_conditions")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=5)
    tree.pack(side=tk.LEFT, fill="both", expand=True, padx=(10, 0))
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)
    tree.heading("name", text="Name")
    tree.heading("weight", text="Weight")
    tree.heading("use_conditions", text="Use Conditions")
    tree.column("name", width=300, stretch=tk.YES)
    tree.column("weight", minwidth=0, width=50, stretch=tk.NO)
    tree.column("use_conditions", minwidth=100, width=300, stretch=tk.YES)
    for c in bg:
        tree.insert("", tk.END, values=astuple(c))


def label_background_names(parent, label, bg, row, animation=None):
    frame = ttk.Frame(parent)
    frame.grid(row=row, column=0, columnspan=2, sticky="nw")
    if animation:
        label = f"{label} (animation speed={animation})"
    label = ttk.Label(frame, text=label)
    label.grid(row=0, column=0, sticky="nw")

    listb = tk.Listbox(selectmode=tk.SINGLE)
    scrollbar = ttk.Scrollbar(parent, command=listb.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listb.configure(yscrollcommand=scrollbar.set)
    listb.pack(side=tk.LEFT, fill=tk.BOTH)
    for c in bg:
        listb.insert(tk.END, c)


def label_text(parent, label, content, row=0):
    label = ttk.Label(parent, text=label)
    label.grid(row=row, column=0, sticky="nw")
    text = ScrolledText(parent, height=8, wrap=tk.WORD, padx=5)
    text.grid(row=row, column=1, columnspan=3, sticky="nw")
    text.insert("1.0", content)
    text["state"] = "disabled"
    return label, text


class HighlightText(ScrolledText):
    _w: str

    """Highlighter shamelessly sourced from https://github.com/rdbende/chlorophyll"""
    def __init__(self, parent):
        super().__init__(parent, height=24, wrap=tk.WORD, padx=5)
        self.grid(row=0, column=0)
        self.lexer = XmlLexer
        self.style = get_style_by_name("default")
        self.fonts = {}
        self.define_fonts()
        self.create_tags()
        self._orig = f"{self._w}_widget"
        # Although the following may not be necessary for this software needs,
        # it remains a neat trick nonetheless. Effectively rename the current
        # widget, then install a proxy function call whenever tk.call is
        # involved.
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        """Thanks to Bryan Oakley on StackOverflow: https://stackoverflow.com/a/40618152/"""
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        # Generate a <<ContentChanged>> event if the widget content was modified
        if command in {"insert", "replace", "delete"}:
            self.event_generate("<<ContentChanged>>")

        return result

    def define_fonts(self):
        self.fonts = {
            "bold_font": font.Font(self, self.cget("font")),
            "italic_font": font.Font(self, self.cget("font")),
            "bold_italic_font": font.Font(self, self.cget("font"))
        }
        self.fonts["bold_font"].configure(weight=font.BOLD)
        self.fonts["italic_font"].configure(slant=font.ITALIC)
        self.fonts["bold_italic_font"].configure(weight=font.BOLD, slant=font.ITALIC)

    def create_tags(self):
        for token, ndef in self.style:
            bold = "_bold" if ndef["bold"] else ""
            italic = "_italic" if ndef["italic"] else ""
            txtfont = self.fonts[f"{bold}{italic}_font"] if bold and italic else None
            foreground = f"#{ndef['color']}" if ndef["color"] else None
            self.tag_configure(str(token), foreground=foreground, font=txtfont)

    def highlighter(self):
        lines = self.get("1.0", "end")
        line_offset = lines.count("\n") - lines.lstrip().count("\n")
        start_token = str(self.tk.call(self._orig, "index", f"1.0 + {line_offset} lines"))

        for token, text in lex(lines, self.lexer()):
            token = str(token)
            end_token = self.index(f"{start_token} + {len(text)} chars")
            if token not in {"Token.Text.Whitespace", "Token.Text"}:
                self.tag_add(token, start_token, end_token)
            start_token = end_token


class DetailWindow(tk.Toplevel):
    def __init__(self, parent, ceevent: Ceevent):
        super().__init__(parent)
        self.geometry("800x600+100+100")
        self.title(ceevent.name.value)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=3)
        label_entry(self, "Name", ceevent.name.value, row=0)

        with suppress(AttributeError):
            label_text(self, "Text", ceevent.text.value, row=self.row_size() + 1)

        with suppress(AttributeError):
            label_entry(self, "Background Name", ceevent.background_name.value, row=self.row_size() + 1)

        with suppress(AttributeError):
            label_backgrounds(self, "Backgrounds", ceevent.backgrounds.background, row=self.row_size() + 1)

        with suppress(AttributeError):
            label_background_names(
                self,
                "Background Animation",
                ceevent.background_animation.background_name,
                row=self.row_size() + 1,
                animation=ceevent.background_animation_speed.value
            )

        self._xml_rowspan = self.row_size()
        self._hidden = True
        self.xml_frame = ttk.Frame(self)
        xml_content = HighlightText(self.xml_frame)
        xml_content.insert("1.0", ceevent.xmlsource)
        xml_content.highlighter()
        xml_content["state"] = "disabled"

        col, row = self.grid_size()
        endframe = ttk.Frame(self)
        endframe.grid(row=row + 1, columnspan=2)
        ttk.Button(endframe, text='close', command=self.destroy).grid(row=0, column=0)
        self.toggle_button = ttk.Button(endframe, text="Show XML", command=lambda: self.toggle_xml())
        self.toggle_button.grid(row=0, column=1)

    def toggle_xml(self):
        if self._hidden:
            self.toggle_button.configure(text="Hide XML")
            self.xml_frame.grid(row=0, column=2, rowspan=self._xml_rowspan)
            self.geometry("1600x600+100+100")
        else:
            self.toggle_button.configure(text="Show XML")
            self.xml_frame.grid_remove()
            self.geometry("800x600+100+100")
        self._hidden = not self._hidden

    def row_size(self):
        _, row = self.grid_size()
        return row


def label_click(event):
    event.widget.config(background="green")
    print("I am label clicked")
    print(dir(event.widget))
    print(event.widget.ce_event_name)


class CeListBox(tk.Listbox):
    def __init__(self, parent):
        super().__init__(parent, selectmode=tk.SINGLE)
        self._prevlen = 0
        scrollbar = ttk.Scrollbar(parent, command=self.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.config(yscrollcommand=scrollbar.set)
        self.populate()
        self.bind("<<ListboxSelect>>", self.on_selected_event)

    def populate(self, filterstr=None):
        items = get_ebucket()
        if not filterstr:
            iterme = items.values()
        else:
            iterme = filter(lambda x: filterstr in x.name, items.values())
        for entry in iterme:
            self.insert(tk.END, entry.name.value)
            if entry.has_restricted_flag(RestrictedListOfFlagsType.CAN_ONLY_BE_TRIGGERED_BY_OTHER_EVENT):
                self.itemconfig(tk.END, bg="#007500")
            elif entry.has_restricted_flag(RestrictedListOfFlagsType.WAITING_MENU):
                self.itemconfig(tk.END, bg="#11d116")
            else:
                print(f"Restricted Flags ({entry.name.value}):", end="\n  ")
                print(entry.restricted_flags)

    def on_selected_event(self, event):
        # List item is unselected as a soon as the user interact with a child window,
        # thus throwing an empty selection event.
        if not self.curselection():
            return

        ebucket = get_ebucket()
        ceeventobj = ebucket[self.get(self.curselection())]
        dw = DetailWindow(self, ceeventobj)
        dw.wait_visibility()  # Can only grab window if visible.
        dw.grab_set()  # Grab window, prevent interaction with parent (self).

    def on_filter_event(self, stringvar):
        string = stringvar.get()
        if len(string) < 3 and self._prevlen == 0:
            return
        self._prevlen = len(string)
        self.delete(0, tk.END)
        self.populate(string)

    def reset_filter(self):
        self.delete(0, tk.END)
        self.populate()


class CeLegendFrame(tk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Flags Legend")
        Hovertip(self, "Flags are colored and displayed by order of importance.")
        self.add_legend(
            text=RestrictedListOfFlagsType.CAN_ONLY_BE_TRIGGERED_BY_OTHER_EVENT.value,
            icon="007500"
        )
        self.add_legend(text=RestrictedListOfFlagsType.WAITING_MENU.value, icon="11d116")

    def add_legend(self, text, icon):
        ico = tk.PhotoImage(file=os.path.join(get_config('icons'), f"legend_{icon}.png"))
        lab = ttk.Label(
            self,
            text=text,
            image=ico,
            justify=tk.LEFT,
            padding=(10, 0, 0, 0),
            compound="left"
        )
        lab.image = ico  # "anchor" a reference of the icon to the label
        lab.pack(anchor=tk.W)


def main(xmlfile):
    process_file(xmlfile, CE_XSD_FILE)
    root = tk.Tk()
    root.title("CE Events Visualizer")
    # width x height + horizontal + vertical
    root.geometry("800x400+50+50")
    main_frame = ttk.Frame(root)
    left_frame = ttk.Frame(main_frame, width=300)
    left_frame.pack_propagate(False)  # Disable automatic resizing of the frame
    right_frame = ttk.Frame(main_frame)
    celb = CeListBox(right_frame)
    legend_frame = CeLegendFrame(left_frame)
    search_frame = ttk.LabelFrame(left_frame, text="Search")

    searchlabel = ttk.Label(search_frame, text="Names:")
    sv = tk.StringVar()
    sv.trace_add(("write", "read"), lambda *x: celb.on_filter_event(sv))
    search = ttk.Entry(search_frame, width=20, textvariable=sv)

    def reset_clicked(widget):
        widget.delete(0, tk.END)
        celb.reset_filter()

    searchreset = ttk.Button(
        search_frame, text="Clear", command=lambda: reset_clicked(search)
    )

    main_frame.grid(row=0, column=0, sticky=tk.NSEW)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=5)
    main_frame.grid_rowconfigure(0, weight=1)  # TODO add more weights if more row are needed
    left_frame.grid(row=0, column=0, sticky=tk.NSEW)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky=tk.NSEW)

    celb.pack(expand=True, fill=tk.BOTH)
    legend_frame.pack(anchor=tk.NW, fill=tk.BOTH, padx=10, pady=10)
    search_frame.pack(fill=tk.BOTH, padx=10, pady=10)
    searchlabel.pack(anchor=tk.W, padx=10)
    search.pack(anchor=tk.W, side=tk.LEFT, fill=tk.X, padx=(10, 0))
    searchreset.pack(side=tk.LEFT, fill=tk.X, padx=(10, 0))
    main_frame.pack(expand=True, fill=tk.BOTH)

    search.focus()
    # lbl = ttk.Label(root, text="I am label")
    # lbl.ce_event_name = "I am name"
    # lbl.bind("<Button-1>", label_click, add="+")
    # lbl.pack()
    # btn = ttk.Button(root, text="I am button", command=lambda: print("I am button pressed"))
    # btn.pack()
    tk.mainloop()
