# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2023 bicobus <bicobus@keemail.me>
from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass
from itertools import chain
from typing import Callable, TypeVar, Optional

import wx
import wx.grid
import wx.lib.mixins.inspection
import wx.lib.scrolledpanel as wx_scrolled
from PIL import Image, ImageDraw
from attrs import fields
from pygments import token
from pygments.styles import get_style_by_name
from wx import stc
from wx.lib import expando
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin, ColumnSorterMixin

from . import CE_XSD_FILE
from .ceevents import get_ebucket, process_file, Ceevent
from .ceevents_template import (
    RestrictedListOfFlagsType,
    Options,
    Option,
    RestrictedListOfConsequencesValue,
    ceevents_modal,
)

style = get_style_by_name("default")

if wx.Platform == '__WXMSW__':
    faces = {
        'times': 'Times New Roman',
        'mono': 'Courier New',
        'helv': 'Arial',
        'other': 'Comic Sans MS',
        'size': 10,
        'size2': 8,
    }
elif wx.Platform == '__WXMAC__':
    faces = {
        'times': 'Times New Roman',
        'mono': 'Monaco',
        'helv': 'Arial',
        'other': 'Comic Sans MS',
        'size': 12,
        'size2': 10,
    }
else:
    faces = {
        'times': 'Times',
        'mono': 'Courier',
        'helv': 'Helvetica',
        'other': 'new century schoolbook',
        'size': 11,
        'size2': 10,
    }
faces["back"] = style.background_color
faces["fore"] = style.styles[token.Token] or "#000"


# - Images ---
def hex2rgb(color: str):
    c = color.lstrip("#")
    return tuple(int(c[i : i + 2], 16) for i in (0, 2, 4))


def create_icon(color=None):
    if not color:
        color = "#2ecc71"
    img = Image.new('RGBA', (16, 16))
    draw = ImageDraw.Draw(img)
    draw.rectangle([(1, 1), (14, 14)], fill=color, outline="black")
    return img


def pil2wximage(img: Image.Image):
    """Convert a PIL image to wxImage"""
    wx_image = wx.Image(*img.size)
    wx_image.SetData(img.convert('RGB').tobytes())
    wx_image.InitAlpha()
    alpha = img.getchannel("A").tobytes()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            wx_image.SetAlpha(i, j, alpha[i + j * img.size[0]])
    return wx_image


def wximage2bitmap(img):
    return img.ConvertToBitmap()


# - End Images ---


def values_as_list(modalitem):
    return [x.value for x in modalitem]


# HACK around terrain types being multiple levels of list
def values_as_list_tt(tt):
    return [x.terrain_type[0].value for x in tt]


def get_label(attrelem, target):
    return getattr(fields(attrelem.__class__), target).metadata['name']


# - Detail Window ---
def pyg2sci_properties(properties: str) -> str:
    foretxt = "fore:{}"
    backtxt = "back:{}"
    properties = properties.split()
    for i, p in enumerate(properties):
        if p.startswith("#"):
            properties[i] = foretxt.format(p)
        elif p.startswith("bg:") and p != "bg:":  # Transparent bg, what's that?
            properties[i] = backtxt.format(p.strip("bg:"))
    return ','.join(properties)


# Resources:
# * https://github.com/ScintillaOrg/lexilla/blob/711c46e160352135d524e32b045c5aa7acbcca75/lexers/LexHTML.cxx#L912
# * https://github.com/pygments/pygments/blob/14cff613a681d2c95bf2c56f81833f645353bbe0/pygments/lexers/html.py#L194
# * https://wiki.wxpython.org/StyledTextCtrl%20Lexer%20Quick%20Reference#Xml
# * https://github.com/wxWidgets/wxWidgets/blob/3bd50638863a379570f7f93d27d91ba297995369/include/wx/stc/stc.h#L736-L747
def pygment2scite(styles):
    for pygtoken, properties in styles.items():
        match pygtoken:
            case token.Name.Tag:
                scitoken = [stc.STC_H_TAG, stc.STC_H_TAGEND, stc.STC_H_TAGUNKNOWN]
            case token.Name.Attribute:
                scitoken = [stc.STC_H_ATTRIBUTE, stc.STC_H_ATTRIBUTEUNKNOWN]
            case token.Name.Entity:
                scitoken = stc.STC_H_ENTITY
            case token.Literal.Number:
                scitoken = stc.STC_H_NUMBER
            case token.Literal.String:
                scitoken = [stc.STC_H_SINGLESTRING, stc.STC_H_DOUBLESTRING]
            case token.Operator:
                scitoken = stc.STC_H_OTHER
            case token.Comment:
                scitoken = stc.STC_H_COMMENT
            case token.Whitespace:
                scitoken = stc.STC_WRAP_WHITESPACE
            case _:
                continue

        properties = pyg2sci_properties(properties)
        if isinstance(scitoken, list):
            for t in scitoken:
                yield t, properties
        else:
            yield scitoken, properties


def wx_label_text(parent, sizer, label: str, text: str, multiline=None):
    if not text:
        text = ""
        return
    lbl = wx.StaticText(parent, wx.ID_ANY, label=label)

    if multiline:
        wtext = expando.ExpandoTextCtrl(
            parent, wx.ID_ANY, value=text, style=wx.TE_WORDWRAP | wx.TE_READONLY
        )
        wtext.SetMaxHeight(200)
    else:
        wtext = wx.TextCtrl(parent, wx.ID_ANY, value=text, style=wx.TE_READONLY)

    sizer.Add(lbl, 0, wx.LEFT, 5)
    sizer.Add(wtext, 1, wx.ALL | wx.EXPAND, 3)


def wx_label_list(parent, sizer, label, data):
    if not data:
        return
    lbl = wx.StaticText(parent, wx.ID_ANY, label=label)
    listbox = wx.ListBox(parent, wx.ID_ANY, style=wx.BORDER_NONE)
    listbox.AppendItems(data)

    sizer.Add(lbl, 0, wx.LEFT, 5)
    sizer.Add(listbox, 1, wx.ALL | wx.EXPAND, 3)


# -- Create a custom table - XXX: UNUSED
class BackgroundTable(wx.grid.GridTableBase):
    def __init__(self, data):
        super().__init__()
        self.col_labels = ("name", "weight", "use_conditions")
        self.data = []
        for row in data:
            self.data.append((row.name, row.weight, row.use_conditions))

    def GetNumberRows(self):
        return len(self.data) + 1

    def GetNumberCols(self):
        return len(self.data[0])

    def IsEmptyCell(self, row, col):
        try:
            return bool(self.data[row][col])
        except IndexError:
            return True

    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''

    def SetValue(self, row, col, value):
        return

    def GetColLabelValue(self, col):
        return self.col_labels[col]


class CustomGrid(wx.grid.Grid):
    def __init__(self, parent, data):
        super().__init__(parent, wx.ID_ANY)
        table = BackgroundTable(data)
        self.SetTable(table, True, wx.grid.Grid.GridSelectRows)
        self.SetRowLabelSize(0)
        self.SetMargins(0, 0)
        self.AutoSizeColumns(True)
        self.EnableEditing(False)


# -- End custom table - XXX: UNUSED


class ABCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, parent, data, headers):
        super().__init__(
            parent, wx.ID_ANY, style=wx.LC_REPORT | wx.LC_SINGLE_SEL | wx.BORDER_NONE
        )
        ListCtrlAutoWidthMixin.__init__(self)
        self._data = data
        for i, column in enumerate(headers):
            self.InsertColumn(i, column)

    def populate(self):
        raise NotImplementedError


class AttrNotFound(Exception):
    pass


def sanitize_attr_value(attr):
    # Don't sanitize lists, their content is sanitized later.
    if isinstance(attr, list):
        return attr
    return str(attr)


class GenericOptionCtrl(ABCtrl):
    def __init__(self, parent, data, headers, keys: list):
        super().__init__(parent, data, headers)
        self._keys = keys

    def getattr(self, i, attr):
        if hasattr(self._data[i], attr):
            return getattr(self._data[i], attr)
        return ""

    def populate(self):
        data = {}
        cols = len(self._keys)
        firstattr = self._keys.pop(0)
        for ri, rdata in enumerate(self._data):
            data[firstattr] = sanitize_attr_value(self.getattr(ri, firstattr))
            idx = self.InsertItem(ri, data[firstattr])
            for i, attr in enumerate(self._keys, 1):
                data[attr] = sanitize_attr_value(self.getattr(ri, attr))
                self.SetItem(idx, i, data[attr])
            yield ri, idx, [*data.values()]
        for col in range(cols):
            self.SetColumnWidth(col, wx.LIST_AUTOSIZE)


C = TypeVar('C', bound=ABCtrl)


class BackgroundListCtrl(ABCtrl):
    def populate(self):
        for ri, rdata in enumerate(self._data):
            idx = self.InsertItem(ri, rdata.name)
            self.SetItem(idx, 1, sanitize_attr_value(rdata.weight))
            self.SetItem(idx, 2, sanitize_attr_value(rdata.use_conditions))
            yield ri, idx, [
                rdata.name,
                sanitize_attr_value(rdata.weight),
                sanitize_attr_value(rdata.use_conditions),
            ]
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(1, 55)
        self.SetColumnWidth(2, wx.LIST_AUTOSIZE)


class ClanOptionCtrl(ABCtrl):
    def populate(self):
        for ri, rdata in enumerate(self._data):
            idx = self.InsertItem(ri, rdata.ref)
            self.SetItem(idx, 1, sanitize_attr_value(rdata.action))
            self.SetItem(idx, 2, sanitize_attr_value(rdata.clan))
            self.SetItem(idx, 3, sanitize_attr_value(rdata.hide_notification))
            yield ri, idx, [
                rdata.ref,
                rdata.action,
                rdata.clan,
                rdata.hide_notification,
            ]
        self.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        self.SetColumnWidth(3, wx.LIST_AUTOSIZE)


class ListCtrlPanel(wx.Panel, ColumnSorterMixin):
    def __init__(
        self,
        parent,
        data: list,
        headers: tuple[str, ...],
        lobject: Callable[[ListCtrlPanel, list, tuple, Optional[list]], C],
        keys=None,
    ):
        super().__init__(parent, wx.ID_ANY, style=wx.WANTS_CHARS)
        self.itemDataMap = {}
        if lobject is GenericOptionCtrl:
            self.blc = lobject(self, data, headers, keys)
        else:
            self.blc = lobject(self, data, headers)

        for ri, idx, rdata in self.blc.populate():
            self.itemDataMap[ri] = rdata
            self.blc.SetItemData(ri, idx)

        ColumnSorterMixin.__init__(self, 3)
        self.Bind(wx.EVT_LIST_COL_CLICK, self.on_col_click, self.blc)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.blc, 1, wx.EXPAND)

        self.SetSizerAndFit(sizer)
        self.SetAutoLayout(True)

    def GetListCtrl(self) -> ABCtrl:
        return self.blc

    def on_col_click(self, event):
        pass


class DataTypeNotValid(Exception):
    ...


@dataclass
class ComplexListData:
    lp_data: list
    lp_label: str
    lp_headers: tuple
    lp_keys: list


@dataclass
class SimpleListData:
    lp_data: list
    lp_label: str


class ABCCollapsiblePanel(wx.CollapsiblePane):
    def __init__(self, parent, label, cb):
        super().__init__(
            parent, label=label, style=wx.CP_DEFAULT_STYLE | wx.CP_NO_TLW_RESIZE
        )
        self.SetMinSize((600, -1))
        self.Bind(wx.EVT_COLLAPSIBLEPANE_CHANGED, cb, self)
        self._data = {}
        self._cld: list[ComplexListData | SimpleListData] = []
        self._post_init()
        self.populate()

    def _post_init(self):
        raise NotImplementedError

    def populate(self):
        raise NotImplementedError

    @staticmethod
    def build_data(option, attributes):
        return {
            get_label(option, x): sanitize_attr_value(
                getattr(option, x)
            )
            for x in attributes
        }


class CeCollapsiblePanel(ABCCollapsiblePanel):
    def populate(self):
        pane = self.GetPane()
        cp_box = wx.BoxSizer()
        cp_flex = wx.FlexGridSizer(2, (5, 5))
        cp_flex.AddGrowableCol(1)
        for label, value in self._data.items():
            if isinstance(value, list):
                wx_label_list(pane, cp_flex, label, value)
            else:
                wx_label_text(pane, cp_flex, label, value)
        cp_box.Add(cp_flex, 1, wx.EXPAND | wx.ALL, 5)
        pane.SetSizer(cp_box)
        cp_box.SetSizeHints(pane)


class CeCollapsible2ColPanel(ABCCollapsiblePanel):
    def populate(self):
        pane = self.GetPane()
        cp_box = wx.BoxSizer()
        cp_flex = wx.FlexGridSizer(4, (5, 5))
        cp_flex.AddGrowableCol(1)
        cp_flex.AddGrowableCol(3)
        for label, value in self._data.items():
            if isinstance(value, list):
                wx_label_list(pane, cp_flex, label, value)
            else:
                wx_label_text(pane, cp_flex, label, value)
        cp_box.Add(cp_flex, 1, wx.EXPAND | wx.ALL, 5)
        pane.SetSizer(cp_box)
        cp_box.SetSizeHints(pane)


class CeComplexCollapsiblePanel(ABCCollapsiblePanel):
    def _post_init(self):
        raise NotImplementedError()

    def _first_flex(self, pane):
        cp_flex = wx.FlexGridSizer(4, (5, 5))
        cp_flex.AddGrowableCol(1)
        cp_flex.AddGrowableCol(3)
        for label, value in self._data.items():
            if isinstance(value, list):
                wx_label_list(pane, cp_flex, label, value)
            else:
                wx_label_text(pane, cp_flex, label, value)

        return cp_flex

    def populate(self):
        pane = self.GetPane()
        cp_box = wx.BoxSizer(wx.VERTICAL)
        cp_box.SetMinSize((800, -1))
        cp_flex3 = wx.FlexGridSizer(2, (5, 5))
        cp_flex3.AddGrowableCol(1)
        if self._data:
            cp_box.Add(self._first_flex(pane), 0, wx.EXPAND | wx.ALL, 5)

        for data in self._cld:
            if isinstance(data, ComplexListData):
                cp_flex3.Add(
                    wx.StaticText(pane, wx.ID_ANY, label=data.lp_label),
                    0,
                    wx.LEFT,
                    5
                )
                cp_flex3.Add(
                    ListCtrlPanel(
                        pane,
                        data.lp_data,
                        data.lp_headers,
                        GenericOptionCtrl,
                        data.lp_keys,
                    ), 1, wx.EXPAND | wx.ALL, 5)
            elif isinstance(data, SimpleListData):
                wx_label_list(pane, cp_flex3, data.lp_label, data.lp_data)
            else:
                raise DataTypeNotValid(data)

        cp_box.Add(cp_flex3, 1, wx.EXPAND | wx.ALL, 5)
        pane.SetSizer(cp_box)
        cp_box.SetSizeHints(pane)


class CeCompanions(CeComplexCollapsiblePanel):
    def __init__(self, parent, cb, option: ceevents_modal.Companion):
        self._option = option
        super().__init__(parent, "Companions", cb)

    def _post_init(self):
        self._data = self.build_data(
            self._option,
            [
                "pregnancy_risk_modifier",
                "escape_chance",
                "gold_total",
                "captor_gold_total",
                "relation_total",
                "morale_total",
                "health_total",
                "renown_total",
                "id",
                "ref",
                "type_value",
                "location",
                "use_other_conditions"
            ]
        )
        with suppress(AttributeError):
            self._cld.append(
                SimpleListData(
                    values_as_list(self._option.multiple_restricted_list_of_consequences.restricted_list_of_consequences),
                    "Restricted List of Consequence",
                )
            )
        with suppress(AttributeError):
            self._cld.append(
                ComplexListData(
                    self._option.skills_to_level.skill,
                    "Skills to Level",
                    ("Id", "By Level", "By XP", "Ref", "Color", "Hide Notification"),
                    ["id", "by_level", "by_xp", "ref", "color", "hide_notification"],
                )
            )
        with suppress(AttributeError):
            self._cld.append(
                ComplexListData(
                    self._option.traits_to_level.trait,
                    "Traits to level",
                    ("Id", "By Level", "By XP", "Ref", "color", "Hide Notification"),
                    ["id", "by_level", "by_xp", "ref", "color", "hide_notification"],
                )
            )
        with suppress(AttributeError):
            self._cld.append(
                ComplexListData(
                    self._option.kingdom_options.kingdom_option,
                    "Kingdom Options",
                    ("Ref", "Action", "Kingdom", "Hide Notification"),
                    ["ref", "action", "kingdom", "hide_notification"],
                )
            )
        with suppress(AttributeError):
            self._cld.append(
                ComplexListData(
                    self._option.clan_options.clan_option,
                    "Clan Options",
                    ("Ref", "Action", "Clan", "Hide Notification"),
                    ["ref", "action", "clan", "hide_notification"],
                )
            )


class CeSpawnTroop(CeComplexCollapsiblePanel):
    def __init__(self, parent, cb, option: ceevents_modal.BattleSettings):
        self._option = option
        super().__init__(parent, "Battle Setting", cb)

    def _post_init(self):
        self._data = self.build_data(
            self._option,
            ["ref", "victory", "defeat", "enemy_name", "player_troops"]
        )
        self._cld = [
            ComplexListData(
                self._option.spawn_troops.spawn_troop,
                "Spawn Troops",
                ("Ref", "Id", "Number", "Wounded Number"),
                ["ref", "id", "number", "wounded_number"]
            )
        ]


class CeSpawnHero(CeComplexCollapsiblePanel):
    def __init__(self, parent, cb, option: ceevents_modal.SpawnHero):
        self._option = option
        super().__init__(parent, "Spawn Heroes", cb)

    def _post_init(self):
        self._data = self.build_data(
            self._option, ["ref", "culture", "gender", "clan"]
        )
        self._cld = [
            ComplexListData(
                self._option.skills_to_level.skill,
                "Skills to Level",
                ("Id", "By Level", "By XP", "Ref", "Color", "Hide Notification"),
                ["id", "by_level", "by_xp", "ref", "color", "hide_notification"]
            )
        ]


class CeOptReqs(CeCollapsible2ColPanel):
    def __init__(self, parent, cb, option: ceevents_modal.Option):
        self._option = option
        super().__init__(parent, "Requirements", cb)

    def _post_init(self):
        s = [
            "req_hero_health_%s_percentage",
            "req_hero_captor_relation_%s",
            "req_hero_prostitute_level_%s",
            "req_hero_slave_level_%s",
            "req_hero_trait_level_%s",
            "req_hero_skill_level_%s",
            "req_hero_troops_%s",
            "req_hero_captives_%s",
            "req_hero_female_troops_%s",
            "req_hero_female_captives_%s",
            "req_hero_male_troops_%s",
            "req_hero_male_captives_%s",
            "req_captor_trait_level_%s",
            "req_captor_skill_level_%s",
            "req_troops_%s",
            "req_captives_%s",
            "req_female_troops_%s",
            "req_female_captives_%s",
            "req_male_troops_%s",
            "req_male_captives_%s",
            "req_morale_%s",
            "req_gold_%s",
        ]
        attributes = chain(
            [
                "req_hero_party_have_item",
                "req_captor_party_have_item",
                "req_captor_skill",
                "req_captor_trait",
                "req_hero_skill",
                "req_hero_trait",
            ],
            chain.from_iterable(
                map(lambda x: [x % y for y in ("above", "below")], s)
            ),
        )

        self._data = self.build_data(
            self._option,
            attributes
        )


class CeEvtReqs(CeCollapsible2ColPanel):
    def __init__(self, parent, cb, ceevent: ceevents_modal.Ceevent):
        self._ceevent = ceevent
        super().__init__(parent, "Requirements", cb)

    def _post_init(self):
        s = [
            "req_hero_health_%s_percentage",
            "req_hero_captor_relation_%s",
            "req_hero_prostitute_level_%s",
            "req_hero_slave_level_%s",
            "req_hero_trait_level_%s",
            "req_hero_skill_level_%s",
            "req_hero_troops_%s",
            "req_hero_captives_%s",
            "req_hero_female_troops_%s",
            "req_hero_female_captives_%s",
            "req_hero_male_troops_%s",
            "req_hero_male_captives_%s",
            "req_captor_trait_level_%s",
            "req_captor_skill_level_%s",
            "req_troops_%s",
            "req_captives_%s",
            "req_female_troops_%s",
            "req_female_captives_%s",
            "req_male_troops_%s",
            "req_male_captives_%s",
            "req_morale_%s",
            "req_gold_%s",
        ]
        attributes = chain(
            [
                "req_custom_code",
                "req_hero_min_age",
                "req_hero_max_age",
                "req_hero_party_have_item",
                "req_captor_party_have_item",
                "req_captor_skill",
                "req_captor_trait",
                "req_hero_skill",
                "req_hero_trait",
            ],
            chain.from_iterable(
                map(lambda x: [x % y for y in ("above", "below")], s)
            ),
        )

        self._data = self.build_data(
            self._ceevent,
            attributes
        )


class CeTeleportSettings(CeCollapsiblePanel):
    def __init__(self, parent, cb, option):
        self.option = option
        super().__init__(parent, "Teleport Settings", cb)

    def _post_init(self):
        self._data = self.build_data(
            self.option,
            ["location", "location_name", "distance", "faction"]
        )


class CeDelayEvent(CeCollapsiblePanel):
    def __init__(self, parent, cb, option):
        self.option = option
        super().__init__(parent, "Delay Event", cb)

    def _post_init(self):
        self._data = self.build_data(
            self.option,
            ["use_conditions", "time_to_take", "trigger_event_name", "trigger_events"],
        )


class CeProgressEvent(CeComplexCollapsiblePanel):
    def __init__(self, parent, cb, option):
        self.option = option
        super().__init__(parent, "Progress Event", cb)

    def _post_init(self):
        self._data = self.build_data(
            self.option,
            [
                "should_stop_moving",
                "display_progress_mode",
                "time_to_take",
                "trigger_event_name",
                ""
            ],
        )
        self._cld = [
            ComplexListData(
                self.option.trigger_events,
                "Trigger Events",
                ("event_name", "event_weight", "event_use_condition"),
                ["event_name", "event_weight", "event_use_condition"]
            )
        ]


class CeStripSettings(CeCollapsiblePanel):
    def __init__(self, parent, cb, option):
        self.option = option
        super().__init__(parent, "Strip Settings", cb)

    def _post_init(self):
        self._data = self.build_data(
            self.option,
            [
                'custom_body',
                'custom_cape',
                'custom_gloves',
                'custom_legs',
                'custom_head',
                'clothing',
                'mount',
                'melee',
                'ranged',
                'forced',
                'quest_enabled',
            ]
        )


class DwTabOne(wx_scrolled.ScrolledPanel):
    def __init__(self, parent, ceevent: Ceevent):
        wx_scrolled.ScrolledPanel.__init__(self, parent, style=wx.TAB_TRAVERSAL)
        self.SetMinSize((800, -1))
        core = wx.BoxSizer(wx.VERTICAL)
        fsizer = wx.FlexGridSizer(2, gap=(5, 5))

        wx_label_text(self, fsizer, label="Event Name", text=ceevent.name.value)
        wx_label_text(self, fsizer, label="Text", text=ceevent.text.value, multiline=True)
        wx_label_text(self, fsizer, label="Order to Call", text=ceevent.order_to_call)

        with suppress(AttributeError):
            wx_label_text(
                self, fsizer, label="Notifiaction Name", text=ceevent.notification_name.value
            )
        with suppress(AttributeError):
            wx_label_text(
                self,
                fsizer,
                label="Sound Name",
                text=ceevent.sound_name.value,
                multiline=True,
            )
        with suppress(AttributeError):
            wx_label_text(
                self,
                fsizer,
                label="Background Name",
                text=ceevent.background_name.value,
                multiline=True,
            )
        with suppress(AttributeError):
            table = ListCtrlPanel(
                self,
                ceevent.backgrounds.background,
                ("Name", "Weight", "Use Conditions"),
                BackgroundListCtrl,
            )
            fsizer.Add(wx.StaticText(self, wx.ID_ANY, label="Backgrounds"), 0, wx.LEFT, 5)
            fsizer.Add(table, 1, wx.EXPAND | wx.ALL, 0)
        with suppress(AttributeError):
            wx_label_text(
                self,
                fsizer,
                label="Background Animation Speed",
                text=str(ceevent.background_animation_speed.value)
            )
        with suppress(AttributeError):
            wx_label_list(
                self,
                fsizer,
                label="Background Animation",
                data=ceevent.background_animation.background_name,
            )
        with suppress(AttributeError):
            wx_label_list(
                self,
                fsizer,
                label="Custom Flags",
                data=values_as_list(ceevent.multiple_list_of_custom_flags.custom_flag),
            )

        # FIXME: Terrain types are lists of lists of one enum upstream,
        #  that is rather impractical. Should behave like flags instead.
        if ceevent.terrain_types_requirements:
            wx_label_list(
                self,
                fsizer,
                label="Terrain Types Requirments",
                data=values_as_list_tt(ceevent.terrain_types_requirements.terrain_types)
            )

        wx_label_list(
            self,
            fsizer,
            label="Restricted Flags",
            data=values_as_list(
                ceevent.multiple_restricted_list_of_flags.restricted_list_of_flags
            ),
        )

        with suppress(AttributeError):
            wx_label_text(
                self,
                fsizer,
                label="CanOnlyHappenNrOfTimes",
                text=ceevent.can_only_happen_nr_of_times.value,
            )

        wx_label_text(
            self, fsizer, "Sexual Content", text=str(ceevent.sexual_content.value)
        )
        wx_label_text(self, fsizer, label="Pregnancy Risk Modifier", text=ceevent.pregnancy_risk_modifier)
        wx_label_text(self, fsizer, label="Escape Chance", text=ceevent.escape_chance)
        wx_label_text(self, fsizer, label="WeightedChanceOfOccurring", text=ceevent.weighted_chance_of_occurring)
        wx_label_text(self, fsizer, label="GoldTotal", text=ceevent.gold_total)
        wx_label_text(self, fsizer, label="CaptorGoldTotal", text=ceevent.captor_gold_total)
        wx_label_text(self, fsizer, label="RelationTotal", text=ceevent.relation_total)
        wx_label_text(self, fsizer, label="MoraleTotal", text=ceevent.morale_total)
        wx_label_text(self, fsizer, label="HealthTotal", text=ceevent.health_total)
        wx_label_text(self, fsizer, label="RenownTotal", text=ceevent.renown_total)
        wx_label_text(self, fsizer, label="ProstitutionTotal", text=ceevent.prostitution_total)
        wx_label_text(self, fsizer, label="SlaveryTotal", text=ceevent.slavery_total)

        if ceevent.skills_required:
            table = ListCtrlPanel(
                self,
                ceevent.skills_required.skill_required,
                ("Id", "Max", "Min", "Ref"),
                GenericOptionCtrl,
                ["id", "max", "min", "ref"],
            )
            fsizer.Add(wx.StaticText(self, wx.ID_ANY, label="Skills Required"), 0, 0, 0)
            fsizer.Add(table, 1, wx.EXPAND | wx.ALL, 0)

        if ceevent.skills_to_level and ceevent.skills_to_level.skill:
            table = ListCtrlPanel(
                self,
                ceevent.skills_to_level.skill,
                ("Id", "By Level", "By XP", "Ref", "Color", "Hide Notification"),
                GenericOptionCtrl,
                ["id", "by_level", "by_xp", "ref", "color", "hide_notification"],
            )
            fsizer.Add(
                wx.StaticText(self, wx.ID_ANY, label="Skills to level"), 0, wx.LEFT, 5
            )
            fsizer.Add(table, 1, wx.EXPAND | wx.ALL, 0)
        elif (
            RestrictedListOfConsequencesValue.CHANGE_SKILL
            in ceevent.multiple_restricted_list_of_flags.restricted_list_of_flags
        ):
            wx_label_text(self, fsizer, label="SkillTotal", text=ceevent.skill_total)
            wx_label_text(self, fsizer, label="SkillXPTotal", text=ceevent.skill_xptotal)
            wx_label_text(self, fsizer, label="SkillToLevel", text=ceevent.skill_to_level)

        if ceevent.traits_required:
            table = ListCtrlPanel(
                self,
                ceevent.traits_required.trait_required,
                ("Id", "Max", "Min", "Ref"),
                GenericOptionCtrl,
                ["id", "max", "min", "ref"],
            )
            fsizer.Add(
                wx.StaticText(self, wx.ID_ANY, label="Skills Required"), 0, wx.LEFT, 5
            )
            fsizer.Add(table, 1, wx.EXPAND | wx.ALL, 0)

        if ceevent.traits_to_level and ceevent.traits_to_level.trait:
            table = ListCtrlPanel(
                self,
                ceevent.traits_to_level.trait,
                ("Id", "By Level", "By XP", "Ref", "color", "Hide Notification"),
                GenericOptionCtrl,
                ["id", "by_level", "by_xp", "ref", "color", "hide_notification"],
            )
            fsizer.Add(wx.StaticText(self, wx.ID_ANY, label="Traits to level"), 0, wx.LEFT, 5)
            fsizer.Add(table, 1, wx.EXPAND | wx.ALL, 5)
        elif (
            RestrictedListOfConsequencesValue.CHANGE_TRAIT
            in ceevent.multiple_restricted_list_of_flags.restricted_list_of_flags
        ):
            wx_label_text(self, fsizer, label="TraitTotal", text=ceevent.trait_total)
            wx_label_text(self, fsizer, label="TraitXPTotal", text=ceevent.trait_xptotal)
            wx_label_text(self, fsizer, label="TraitToLevel", text=ceevent.trait_to_level)

        fsizer.AddGrowableCol(1)
        core.Add(fsizer, 1, wx.EXPAND)

        if ceevent.companions and ceevent.companions.companion:
            for companion in ceevent.companions.companion:
                cpc = CeCompanions(self, self.on_pane_toggle, companion)
                core.Add(cpc, 0, wx.EXPAND)

        if ceevent.progress_event:
            core.Add(
                CeProgressEvent(self, self.on_pane_toggle, ceevent.progress_event), 0, wx.EXPAND
            )

        core.Add(CeEvtReqs(self, self.on_pane_toggle, ceevent), 0, wx.EXPAND)

        self.SetSizerAndFit(core)
        self.SetupScrolling()

    def on_pane_toggle(self, evt):
        self.Fit()  # refit children inside canvas
        self.Layout()


class DwTabXml(wx.Panel):
    def __init__(self, parent, source: str):
        super().__init__(parent)
        core = wx.BoxSizer(wx.VERTICAL)
        t = stc.StyledTextCtrl(self, wx.ID_ANY, style=wx.TE_MULTILINE)
        t.SetWrapMode(stc.STC_WRAP_WORD)
        t.SetWrapIndentMode(stc.STC_WRAPINDENT_SAME)
        t.SetViewWhiteSpace(stc.STC_WS_INVISIBLE)
        t.SetMargins(0, 0)
        t.SetTabWidth(2)
        t.SetTabIndents(True)
        t.SetUseTabs(True)
        t.SetLexer(stc.STC_LEX_XML)
        t.SetSelBackground(True, style.highlight_color)
        t.StyleSetSpec(
            stc.STC_STYLE_DEFAULT,
            "back:{back},fore:{fore},face:{mono},size:{size}".format(**faces),
        )
        t.StyleClearAll()
        for pygtoken, spec in pygment2scite(style.styles):
            t.StyleSetSpec(pygtoken, spec)
        t.SetText(source.replace("    ", "\t"))
        t.Colourise(0, -1)
        t.SetEditable(False)
        core.Add(t, 1, wx.EXPAND | wx.ALL, 2)
        self.SetSizerAndFit(core)


class DwTabOption(wx_scrolled.ScrolledPanel):
    def __init__(self, parent, option: Option):
        wx_scrolled.ScrolledPanel.__init__(self, parent, -1)
        self.SetMinSize((800, -1))
        core = wx.BoxSizer(wx.VERTICAL)
        fsizer = wx.FlexGridSizer(2, gap=(5, 5))
        wx_label_text(self, fsizer, label="Option text", text=option.option_text)
        wx_label_list(
            self,
            fsizer,
            label="Consequences",
            data=values_as_list(
                option.multiple_restricted_list_of_consequences.restricted_list_of_consequences
            ),
        )
        wx_label_text(
            self, fsizer, label="Trigger Event Name", text=option.trigger_event_name
        )
        wx_label_text(self, fsizer, label="Sound Name", text=option.sound_name)
        wx_label_text(self, fsizer, label="Scene to play", text=option.scene_to_play)
        wx_label_text(
            self,
            fsizer,
            label="Pregnancy Modifier",
            text=option.pregnancy_risk_modifier,
        )
        wx_label_text(self, fsizer, label="Escape Chance", text=option.escape_chance)
        wx_label_text(self, fsizer, label="Captor Gold", text=option.captor_gold_total)
        wx_label_text(
            self, fsizer, label="Prostitution Total", text=option.prostitution_total
        )
        wx_label_text(self, fsizer, label="Gold Total", text=option.gold_total)
        wx_label_text(self, fsizer, label="Health Total", text=option.health_total)
        wx_label_text(self, fsizer, label="Morale Total", text=option.morale_total)
        wx_label_text(self, fsizer, label="Relation Total", text=option.relation_total)
        wx_label_text(self, fsizer, label="Renown Total", text=option.renown_total)
        wx_label_text(self, fsizer, label="Item to Give", text=option.item_to_give)

        if option.spawn_troops and option.spawn_troops.spawn_troop:
            table = ListCtrlPanel(
                self,
                option.spawn_troops.spawn_troop,
                ("Ref", "Id", "Number", "Wounded Number"),
                GenericOptionCtrl,
                ["ref", "id", "number", "wounded_number"],
            )
            fsizer.Add(wx.StaticText(self, wx.ID_ANY, label="Spawn Heroes"), 0, 0, 0)
            fsizer.Add(table, 1, wx.EXPAND | wx.ALL, 5)

        if option.trigger_events and option.trigger_events.trigger_event:
            table = ListCtrlPanel(
                self,
                option.trigger_events.trigger_event,
                ("Event Name", "Event Weight", "Event Use Conditions"),
                GenericOptionCtrl,
                ["event_name", "event_weight", "event_use_conditions"],
            )
            fsizer.Add(wx.StaticText(self, wx.ID_ANY, label="Trigger Events"), 0, 0, 0)
            fsizer.Add(table, 1, wx.EXPAND | wx.ALL, 5)

        with suppress(AttributeError):  # XXX: Can't find working example
            if option.kingdom_options.kingdom_option:
                table = ListCtrlPanel(
                    self,
                    option.kingdom_options.kingdom_option,
                    ("Ref", "Action", "Kingdom", "Hide Notification"),
                    GenericOptionCtrl,
                    ["ref", "action", "kingdom", "hide_notification"],
                )
                fsizer.Add(
                    wx.StaticText(self, wx.ID_ANY, label="Kingdom Options"), 0, 0, 0
                )
                fsizer.Add(table, 1, wx.EXPAND | wx.ALL, 5)

        if option.traits_to_level and option.traits_to_level.trait:
            table = ListCtrlPanel(
                self,
                option.traits_to_level.trait,
                ("Id", "By Level", "By XP", "Ref", "color", "Hide Notification"),
                GenericOptionCtrl,
                ["id", "by_level", "by_xp", "ref", "color", "hide_notification"],
            )
            fsizer.Add(wx.StaticText(self, wx.ID_ANY, label="Traits to level"), 0, wx.LEFT, 5)
            fsizer.Add(table, 1, wx.EXPAND | wx.ALL, 5)
        elif (
            RestrictedListOfConsequencesValue.CHANGE_TRAIT
            in option.multiple_restricted_list_of_consequences.restricted_list_of_consequences
        ):
            wx_label_text(
                self, fsizer, label="Traits to level", text=option.trait_to_level
            )
            if option.trait_total:
                wx_label_text(
                    self, fsizer, label="Trait Total", text=option.trait_total
                )
            elif option.trait_xptotal:
                wx_label_text(
                    self, fsizer, label="Trait XP Total", text=option.trait_xptotal
                )

        if option.traits_required:
            table = ListCtrlPanel(
                self,
                option.traits_required.trait_required,
                ("Id", "Max", "Min", "Ref"),
                GenericOptionCtrl,
                ["id", "max", "min", "ref"],
            )
            fsizer.Add(
                wx.StaticText(self, wx.ID_ANY, label="Skills Required"), 0, wx.LEFT, 5
            )
            fsizer.Add(table, 1, wx.EXPAND | wx.ALL, 0)

        if option.skills_to_level and option.skills_to_level.skill:
            table = ListCtrlPanel(
                self,
                option.skills_to_level.skill,
                ("Id", "By Level", "By XP", "Ref", "Color", "Hide Notification"),
                GenericOptionCtrl,
                ["id", "by_level", "by_xp", "ref", "color", "hide_notification"],
            )
            fsizer.Add(
                wx.StaticText(self, wx.ID_ANY, label="Skills to level"), 0, wx.LEFT, 5
            )
            fsizer.Add(table, 1, wx.EXPAND | wx.ALL, 0)
        elif (
            RestrictedListOfConsequencesValue.CHANGE_SKILL
            in option.multiple_restricted_list_of_consequences.restricted_list_of_consequences
        ):
            wx_label_text(
                self, fsizer, label="Skill to Level", text=option.skill_to_level
            )
            if option.skill_total:
                wx_label_text(
                    self, fsizer, label="Skill Total", text=option.skill_total
                )
            elif option.skill_xptotal:
                wx_label_text(
                    self, fsizer, label="Skill XP Total", text=option.skill_xptotal
                )

        if option.skills_required:
            table = ListCtrlPanel(
                self,
                option.skills_required.skill_required,
                ("Id", "Max", "Min", "Ref"),
                GenericOptionCtrl,
                ["id", "max", "min", "ref"],
            )
            fsizer.Add(
                wx.StaticText(self, wx.ID_ANY, label="Skills Required"), 0, wx.LEFT, 5
            )
            fsizer.Add(table, 1, wx.EXPAND | wx.ALL, 0)

        if option.clan_options:
            table = ListCtrlPanel(
                self,
                option.clan_options.clan_option,
                ("Ref", "Action", "Clan", "Hide Notification"),
                ClanOptionCtrl,
            )
            fsizer.Add(
                wx.StaticText(self, wx.ID_ANY, label="Clan Options"), 0, wx.LEFT, 5
            )
            fsizer.Add(table, 1, wx.EXPAND | wx.ALL, 0)

        fsizer.AddGrowableCol(1)
        core.Add(fsizer, 1, wx.EXPAND)

        creqs = CeOptReqs(self, self.on_pane_toggle, option)
        core.Add(creqs, 0, wx.EXPAND)
        if option.companions and option.companions.companion:
            for companion in option.companions.companion:
                cpc = CeCompanions(self, self.on_pane_toggle, companion)
                core.Add(cpc, 0, wx.EXPAND)

        if option.battle_settings:
            cpbs = CeSpawnTroop(self, self.on_pane_toggle, option.battle_settings)
            core.Add(cpbs, 0, wx.EXPAND)

        if option.spawn_heroes and option.spawn_heroes.spawn_hero:
            for spawnhero in option.spawn_heroes.spawn_hero:
                cpsh = CeSpawnHero(self, self.on_pane_toggle, spawnhero)
                core.Add(cpsh, 0, wx.EXPAND)

        if option.damage_party:
            dparty = wx.StaticBoxSizer(
                wx.StaticBox(self, wx.ID_ANY, "Damage party"), wx.HORIZONTAL
            )
            wx_label_text(self, dparty, label="Number", text=option.damage_party.number)
            wx_label_text(
                self,
                dparty,
                label="Wounded Number",
                text=option.damage_party.wounded_number,
            )
            wx_label_text(
                self,
                dparty,
                label="Include Heroes",
                text=option.damage_party.include_heroes,
            )
            wx_label_text(self, dparty, label="Ref", text=option.damage_party.ref)
            core.Add(dparty, 1, wx.EXPAND)

        if option.scene_settings:
            scenes = wx.StaticBoxSizer(
                wx.StaticBox(self, wx.ID_ANY, "Scene settings"), wx.HORIZONTAL
            )
            wx_label_text(
                self, scenes, label="Talk to", text=option.scene_settings.talk_to
            )
            wx_label_text(
                self, scenes, label="Scene name", text=option.scene_settings.scene_name
            )
            core.Add(scenes, 1, wx.EXPAND)

        if option.delay_event:  # XXX: Can't find working example
            cpde = CeDelayEvent(self, self.on_pane_toggle, option.delay_event)
            core.Add(cpde, 1, wx.GROW | wx.ALL, 5)

        if option.strip_settings:
            cpss = CeStripSettings(self, self.on_pane_toggle, option.strip_settings)
            core.Add(cpss, 0, wx.GROW | wx.ALL, 5)

        if option.teleport_settings:
            cpts = CeTeleportSettings(self, self.on_pane_toggle, option.teleport_settings)
            core.Add(cpts, 0, wx.GROW | wx.ALL, 5)

        self.SetSizerAndFit(core)
        self.SetupScrolling()

    def on_pane_toggle(self, evt):
        self.Fit()  # refit children inside canvas
        self.Layout()


class DwTabOptions(wx.Panel):
    def __init__(self, parent, options: Options):
        super().__init__(parent)
        nb = wx.Notebook(self, wx.ID_ANY, style=wx.NB_TOP | wx.NB_MULTILINE)
        for option in options.option:
            nb.AddPage(DwTabOption(nb, option), f"Order {option.order}")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, 1, wx.EXPAND | wx.ALL, 0)
        self.SetSizerAndFit(sizer)


class DetailWindow(wx.Dialog):
    def __init__(self, ceevent: Ceevent, *args, **kwargs):
        title = ceevent.name.value
        kwargs['style'] = (
            kwargs.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )
        super().__init__(title=title, *args, **kwargs)
        # self.SetSizeHints((800, 600), (1024, 800))
        self.SetMinSize((800, 600))

        nb = wx.Notebook(self, wx.ID_ANY, style=wx.NB_LEFT)

        tabone = DwTabOne(nb, ceevent)
        tabxml = DwTabXml(nb, ceevent.xmlsource)
        taboptions = DwTabOptions(nb, ceevent.options)

        nb.AddPage(tabone, "Main")
        nb.AddPage(tabxml, "Xml Source")
        nb.AddPage(taboptions, "Options")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, 1, wx.EXPAND | wx.ALL)

        closebutton = wx.StdDialogButtonSizer()
        self.button_close = wx.Button(self, wx.ID_CLOSE, "")
        closebutton.AddButton(self.button_close)
        sizer.Add(closebutton, 0, wx.ALIGN_RIGHT | wx.ALL, 4)
        closebutton.Realize()

        self.SetSizerAndFit(sizer)
        self.CenterOnScreen()

        self.SetEscapeId(self.button_close.GetId())

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, event):
        self.Destroy()


# - Main Window ---
class Legend(wx.BoxSizer):
    def __init__(self, parent, text, color, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._text = text
        self._color = color
        img = wx.StaticBitmap(
            parent, wx.ID_ANY, wximage2bitmap(pil2wximage(create_icon(color)))
        )
        label = wx.StaticText(parent, wx.ID_ANY, label=text)
        self.Add(img, 0, wx.ALIGN_CENTER_VERTICAL, 0)
        self.Add(label, 0, wx.EXPAND, 0)


class CeListItem(wx.ListItem):
    def __init__(self, item, wxid: int):
        super().__init__()
        self.SetText(item.name.value)
        self.SetId(wxid)
        if color := item.get_color():
            self.SetBackgroundColour(wx.Colour(hex2rgb(color)))


class CeListBox(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args, **kwargs, style=wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL
        )
        ListCtrlAutoWidthMixin.__init__(self)  # Using super() doesn't work?!
        self.InsertColumn(0, "Events")
        self.setResizeColumn(0)
        self.populate()

    def populate(self, filterstr=None):
        self.DeleteAllItems()
        items = get_ebucket()

        if filterstr:
            items = filter(lambda x: filterstr in x.name.value, items.values())
        else:
            items = items.values()

        # self.autocomplete_data = [item.name.value for item in items]
        for n, item in enumerate(items):
            self.InsertItem(CeListItem(item, n))

    def on_clicked_event(self, event):
        ebucket = get_ebucket()
        ceeventobj = ebucket[event.Text]
        displayframe = DetailWindow(ceeventobj, parent=self)
        displayframe.ShowWindowModal()


class MainWindow(wx.Frame):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        super().__init__(None, wx.ID_ANY, *args, title="CE Events Visualizer", **kwds)
        self.Center()
        self.SetSizeHints(800, 400, 800, 600)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        self.window_1 = wx.SplitterWindow(self.panel_1, wx.ID_ANY)
        self.window_1_pane_1 = wx.Panel(self.window_1, wx.ID_ANY)
        self.window_1_pane_2 = wx.Panel(self.window_1, wx.ID_ANY)
        self.window_1_pane_1.SetMinSize((300, -1))

        self.window_1.SetMinimumPaneSize(20)
        self.window_1.SetSashGravity(0.5)
        # Legend panel
        self.panel_leg = wx.StaticBox(
            self.window_1_pane_1,
            wx.ID_ANY,
            "Legend",  # style=wx.BORDER_SIMPLE
        )
        self.panel_search = wx.Panel(
            self.window_1_pane_1, wx.ID_ANY, style=wx.BORDER_SIMPLE
        )
        self.panel_search.SetMinSize((240, -1))

        topsizer = wx.BoxSizer(wx.VERTICAL)
        leftsizer = wx.BoxSizer(wx.VERTICAL)
        legendsizer = wx.WrapSizer(wx.HORIZONTAL)
        searchsizer = wx.BoxSizer(wx.HORIZONTAL)
        rightsizer = wx.BoxSizer(wx.VERTICAL)

        # - Legend ---
        lg_one = Legend(
            self.panel_leg,
            RestrictedListOfFlagsType.CAN_ONLY_BE_TRIGGERED_BY_OTHER_EVENT.value,
            RestrictedListOfFlagsType.CAN_ONLY_BE_TRIGGERED_BY_OTHER_EVENT.color,
        )
        lg_two = Legend(
            self.panel_leg,
            RestrictedListOfFlagsType.WAITING_MENU.value,
            RestrictedListOfFlagsType.WAITING_MENU.color,
        )
        # - End Legend ---
        searchlbl = wx.StaticText(
            self.panel_search,
            wx.ID_ANY,
            label="Search:",
            style=wx.ALIGN_CENTER_HORIZONTAL,
        )
        # TODO: create autocomplete see: 'https://wiki.wxpython.org/How%20to%20create%20a%20text%20control%20with%20autocomplete%20%28Phoenix%29'
        self.searchent = wx.SearchCtrl(self.panel_search, wx.ID_ANY, "")
        self.searchent.SetMinSize((250, -1))
        self.searchent.ShowCancelButton(True)
        self.searchent.SetDescriptiveText("Search")
        self.searchent.SetFocus()
        searchbnt = wx.Button(self.panel_search, label="Clear")

        self.celb = CeListBox(self.window_1_pane_2, wx.ID_ANY)

        topsizer.Add(self.window_1, 1, wx.EXPAND | wx.FIXED_MINSIZE, 0)
        leftsizer.Add(self.panel_leg, 2, wx.EXPAND | wx.ALL, 5)
        legendsizer.Add(lg_one, 0, wx.EXPAND | wx.LEFT, 5)
        legendsizer.Add(lg_two, 0, wx.EXPAND | wx.LEFT, 5)
        leftsizer.Add(self.panel_search, 0, wx.EXPAND | wx.ALL, 0)
        searchsizer.Add(searchlbl, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 4)
        searchsizer.Add(
            self.searchent, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.FIXED_MINSIZE, 0
        )
        searchsizer.Add(searchbnt, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 1)
        rightsizer.Add(self.celb, 1, wx.EXPAND, 0)

        self.window_1_pane_2.SetSizer(rightsizer)
        self.panel_search.SetSizer(searchsizer)
        self.panel_leg.SetSizer(legendsizer)
        self.window_1_pane_1.SetSizer(leftsizer)
        self.window_1.SplitVertically(self.window_1_pane_1, self.window_1_pane_2, 200)
        self.panel_1.SetSizer(topsizer)
        self.Layout()

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.celb.on_clicked_event, self.celb)
        self.Bind(wx.EVT_BUTTON, self.on_reset_event, searchbnt)
        self.Bind(wx.EVT_TEXT, self.on_text_event, self.searchent)
        self.Bind(wx.EVT_SEARCH_CANCEL, self.on_reset_event, self.searchent)

    def on_reset_event(self, event):
        if event.EventType != wx.EVT_SEARCH_CANCEL.typeId:  # not EVT_BUTTON
            self.searchent.SetValue("")
        self.celb.populate()
        event.Skip()

    def on_text_event(self, event):
        if self.searchent.IsEmpty() or len(self.searchent.Value) < 3:
            event.Skip()
            return
        self.celb.populate(self.searchent.Value)
        event.Skip()


class CeStoriesViewer(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):
        self.Init()  # inspector thing
        frame = MainWindow()
        frame.Show()
        self.SetTopWindow(frame)
        return True


def main(xmlfile):
    process_file(xmlfile, CE_XSD_FILE)
    myapp = CeStoriesViewer(redirect=False)
    myapp.MainLoop()
