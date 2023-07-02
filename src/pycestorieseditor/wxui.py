# -*- coding: utf-8 -*-
# © 2023 bicobus <bicobus@keemail.me>

import wx
import wx.lib.mixins.inspection
from wx import stc
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from PIL import Image, ImageDraw
from pygments.styles import get_style_by_name
from pygments import token

from . import CE_XSD_FILE
from .ceevents import get_ebucket, process_file, Ceevent
from .ceevents_template import RestrictedListOfFlagsType

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
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


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
    return (x.value for x in modalitem)


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


class DwTabOne(wx.Panel):
    def __init__(self, parent, ceevent: Ceevent):
        super().__init__(parent)
        core = wx.BoxSizer(wx.VERTICAL)

        name = wx.StaticText(self, wx.ID_ANY, label=ceevent.name.value)
        text = wx.TextCtrl(
            self,
            wx.ID_ANY,
            value=ceevent.text.value,
            style=wx.BORDER_NONE | wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_WORDWRAP
        )

        core.Add(name, 0, wx.EXPAND)
        core.Add(text, 1, wx.EXPAND, 0)
        self.SetSizer(core)


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
            "back:{back},fore:{fore},face:{mono},size:{size}".format(**faces)
        )
        t.StyleClearAll()
        for pygtoken, spec in pygment2scite(style.styles):
            t.StyleSetSpec(pygtoken, spec)
        t.SetText(source.replace("    ", "\t"))
        t.Colourise(0, -1)
        t.SetEditable(False)
        core.Add(t, 1, wx.EXPAND | wx.ALL, 2)
        self.SetSizer(core)


class DetailWindow(wx.Dialog):
    def __init__(self, ceevent: Ceevent, *args, **kwargs):
        title = ceevent.name.value
        kwargs['style'] = kwargs.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        super().__init__(title=title, *args, **kwargs)
        self.SetSizeHints(600, 400, 1024, 640)
        self.SetSize((600, 400))

        nb = wx.Notebook(self, wx.ID_ANY, style=wx.NB_LEFT)

        tabone = DwTabOne(nb, ceevent)
        tabxml = DwTabXml(nb, ceevent.xmlsource)

        nb.AddPage(tabone, "Main")
        nb.AddPage(tabxml, "Xml Source")

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, 1, wx.EXPAND | wx.ALL)

        closebutton = wx.StdDialogButtonSizer()
        self.button_close = wx.Button(self, wx.ID_CLOSE, "")
        closebutton.AddButton(self.button_close)
        sizer.Add(closebutton, 0, wx.ALIGN_RIGHT | wx.ALL, 4)
        closebutton.Realize()

        self.SetSizer(sizer)
        sizer.Fit(self)

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
        img = wx.StaticBitmap(parent, wx.ID_ANY, wximage2bitmap(pil2wximage(create_icon(color))))
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
        super().__init__(*args, **kwargs, style=wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)
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
            self.window_1_pane_1, wx.ID_ANY, "Legend",  # style=wx.BORDER_SIMPLE
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
            RestrictedListOfFlagsType.CAN_ONLY_BE_TRIGGERED_BY_OTHER_EVENT.color
        )
        lg_two = Legend(
            self.panel_leg,
            RestrictedListOfFlagsType.WAITING_MENU.value,
            RestrictedListOfFlagsType.WAITING_MENU.color
        )
        # - End Legend ---
        searchlbl = wx.StaticText(
            self.panel_search,
            wx.ID_ANY,
            label="Search:",
            style=wx.ALIGN_CENTER_HORIZONTAL
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
            self.searchent,
            1,
            wx.ALIGN_CENTER_VERTICAL | wx.ALL | wx.FIXED_MINSIZE,
            0
        )
        searchsizer.Add(searchbnt, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 1)
        rightsizer.Add(self.celb, 1, wx.EXPAND, 0)

        self.window_1_pane_2.SetSizer(rightsizer)
        self.panel_search.SetSizer(searchsizer)
        self.panel_leg.SetSizer(legendsizer)
        self.window_1_pane_1.SetSizer(leftsizer)
        self.window_1.SplitVertically(
            self.window_1_pane_1, self.window_1_pane_2, 200
        )
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
