# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2023 bicobus <bicobus@keemail.me>
import logging
import os
from collections import OrderedDict
from itertools import count

import wx
import wx.lib.stattext as wxst
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.scrolledpanel import ScrolledPanel

from pycestorieseditor import PORTABLE, APPNAME
from pycestorieseditor.ceevents import (
    init_xsdfile,
    create_ebucket,
    process_module,
    NotBannerLordModule,
    NotCeSubmodule,
    CePath,
    init_index,
)
from pycestorieseditor.config import get_config
from pycestorieseditor.wxui import MainWindow

logger = logging.getLogger(__name__)
LAUNCH_SETTINGS = False


class CeListPathItem(wx.ListItem):
    _wid = count()

    def __init__(self, item: CePath):
        super().__init__()
        self._cepath = item
        self.SetText(item.name)
        self.SetId(next(CeListPathItem._wid))

    @staticmethod
    def reset_wid():
        CeListPathItem._wid = count()


class CeListBox(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, style=wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)
        ListCtrlAutoWidthMixin.__init__(self)
        self.InsertColumn(0, "Path")
        self.setResizeColumn(0)

    def reset(self):
        self.ClearAll()
        CeListPathItem.reset_wid()
        self.InsertColumn(0, "Path")
        # force a column resize after clearing, otherwise the column doesn't expand
        self.resizeColumn(1)


class CeSettingsWindow(wx.Frame):
    def __init__(self, parent, conffile):
        super().__init__(
            parent,
            wx.ID_ANY,
            title="Settings window",
            pos=wx.DefaultPosition,
            size=wx.DefaultSize,
            style=wx.DEFAULT_FRAME_STYLE,
        )

        self._paths: dict[str, CePath] = OrderedDict()
        self._conffile = conffile

        panel = wx.Panel(self)
        window = ScrolledPanel(panel, wx.ID_ANY)
        window.SetupScrolling(scroll_x=False)
        window.SetAutoLayout(1)
        self._bsizer = bsizer = wx.BoxSizer(wx.VERTICAL)
        fsizer = wx.FlexGridSizer(3, gap=(5, 5))
        fsizer.AddGrowableCol(1)
        addremovesizer = wx.BoxSizer(wx.VERTICAL)

        self._warningtxt = wxst.GenStaticText(panel, wx.ID_ANY, label="")
        self._warningtxt.SetForegroundColour((255, 0, 0))
        self._warningtxt.Hide()
        self._noticetxt = wxst.GenStaticText(panel, wx.ID_ANY, label="Lorem ipsum dolor sit amet")
        self._noticetxt.SetForegroundColour((0, 255, 0))
        self._noticetxt.Hide()
        self._flist = CeListBox(window, wx.ID_ANY)
        buttonadd = wx.Button(window, wx.ID_ANY, "+", (50, 50))
        buttonrem = wx.Button(window, wx.ID_ANY, "-", (50, 50))
        buttonclr = wx.Button(window, wx.ID_ANY, "CLR", (50, 50))
        self.bup = buttonup = wx.Button(window, wx.ID_ANY, "↑", (50, 50))
        self.bdw = buttondw = wx.Button(window, wx.ID_ANY, "↓", (50, 50))
        btnvalidate = wx.Button(window, wx.ID_ANY, "Validate", (50, 50))
        btnvalidate.SetToolTip(
            "Will try to validate all xml file present in the listed folders.\n!!!It may take a while!!!"
        )
        btnsave = wx.Button(window, wx.ID_ANY, "Save", (50, 50))

        xsdlabel = wx.StaticText(window, wx.ID_ANY, label="XSD file")
        self.xsdentry = wx.TextCtrl(window, wx.ID_ANY, value="", style=wx.TE_READONLY)
        xsdbutton = wx.Button(window, wx.ID_ANY, "Select")

        addremovesizer.Add(buttonadd, 0, wx.ALL, 5)
        addremovesizer.Add(buttonrem, 0, wx.ALL, 5)
        addremovesizer.Add(buttonclr, 0, wx.ALL, 5)
        addremovesizer.Add(buttonup, 0, wx.ALL, 5)
        addremovesizer.Add(buttondw, 0, wx.ALL, 5)
        fsizer.Add(wx.StaticText(window, wx.ID_ANY, label="CE Modules"), 0, wx.LEFT, 5)
        fsizer.Add(self._flist, 1, wx.ALL | wx.EXPAND, 3)
        fsizer.Add(addremovesizer, 0, wx.RIGHT, 5)

        fsizer.Add((20, 20), 0, wx.LEFT, 3)
        fsizer.Add(btnvalidate, 1, wx.ALL | wx.EXPAND, 3)
        fsizer.Add((20, 20), 0, wx.RIGHT, 3)

        fsizer.Add((10, 10), 0, wx.LEFT, 3)
        fsizer.Add((10, 10), 0, wx.ALL | wx.EXPAND, 3)
        fsizer.Add((10, 10), 0, wx.RIGHT, 3)

        fsizer.Add(xsdlabel, 0, wx.LEFT, 3)
        fsizer.Add(self.xsdentry, 0, wx.ALL | wx.EXPAND, 3)
        fsizer.Add(xsdbutton, 0, wx.RIGHT, 3)

        fsizer.Add((10, 10), 0, wx.LEFT, 3)
        fsizer.Add((10, 10), 0, wx.ALL | wx.EXPAND, 3)
        fsizer.Add(btnsave, 0, wx.RIGHT, 3)

        bsizer.Add(self._warningtxt, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT, 3)
        bsizer.Add(self._noticetxt, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.LEFT | wx.RIGHT, 3)
        bsizer.Add(window, 1, wx.EXPAND, 0)

        self.Bind(wx.EVT_BUTTON, self._button_add_folder_pressed, buttonadd)
        self.Bind(wx.EVT_BUTTON, self._button_rem_folder_pressed, buttonrem)
        self.Bind(wx.EVT_BUTTON, self._button_clr_folder_pressed, buttonclr)
        self.Bind(wx.EVT_BUTTON, self._button_move_folder_pressed, buttonup)
        self.Bind(wx.EVT_BUTTON, self._button_move_folder_pressed, buttondw)
        self.Bind(wx.EVT_BUTTON, self._button_validate_pressed, btnvalidate)
        self.Bind(wx.EVT_BUTTON, self._button_xsd_pressed, xsdbutton)
        self.Bind(wx.EVT_BUTTON, self._button_save_pressed, btnsave)
        self._warningtxt.Bind(wx.EVT_ENTER_WINDOW, self._on_mouse_event, self._warningtxt)
        self._warningtxt.Bind(wx.EVT_LEAVE_WINDOW, self._on_mouse_event, self._warningtxt)
        self._warningtxt.Bind(wx.EVT_LEFT_DOWN, self._on_mouse_event, self._warningtxt)
        self._noticetxt.Bind(wx.EVT_ENTER_WINDOW, self._on_mouse_event, self._noticetxt)
        self._noticetxt.Bind(wx.EVT_LEAVE_WINDOW, self._on_mouse_event, self._noticetxt)
        self._noticetxt.Bind(wx.EVT_LEFT_DOWN, self._on_mouse_event, self._noticetxt)

        window.SetSizerAndFit(fsizer)
        panel.SetSizerAndFit(bsizer)
        self.SetSizeHints(bsizer.GetMinSize())

        self._load_conf()

        self.Layout()

    def _button_xsd_pressed(self, evt):
        """Show dialog to select xsd file, then validate"""
        with wx.FileDialog(
            self,
            "Select XSD file",
            wildcard="Xml Schema Document (*.xsd)|*.xsd",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
        ) as fd:
            if fd.ShowModal() == wx.ID_CANCEL:
                return
            pathname = fd.GetPath()
            try:
                init_xsdfile(pathname)
            except SyntaxError:
                self._show_warning("The selected file isn't a valid Xml Schema Document.")
                return
            self.xsdentry.SetValue(pathname)

    def _button_add_folder_pressed(self, evt):
        # FIXME wxpython doesn't support wx.DD_MULTIPLE just yet
        dlg = wx.DirDialog(
            self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST
        )

        if dlg.ShowModal() == wx.ID_OK:
            try:
                path = CePath(dlg.GetPath())
                self._paths[path.name] = path
                self._flist.InsertItem(CeListPathItem(path))
            except (NotBannerLordModule, NotCeSubmodule):
                self._show_warning("The selected folder isn't a valid path.")

        dlg.Destroy()

    def _button_rem_folder_pressed(self, evt):
        index = self._flist.GetFirstSelected()
        while index != -1:
            txt = self._flist.GetItem(index).GetText()
            try:
                self._paths.pop(txt)
            except KeyError:  # trying to be defensive
                logger.error(f"Trying to remove non-existing entry '{txt}'")
                return False
            self._flist.DeleteItem(index)
            # delete last item will raise an assertion error
            if not self._flist.GetItemCount() > 0:
                break
            index = self._flist.GetNextSelected(index)
        return True

    def _button_clr_folder_pressed(self, evt):
        self._flist.reset()
        for path in self._paths.values():
            self._flist.InsertItem(CeListPathItem(path))
        return True

    def _button_move_folder_pressed(self, evt):
        index = self._flist.GetFirstSelected()
        if index == -1:
            return
        obj = evt.GetEventObject()
        txt = None
        while index != -1:
            txt = self._flist.GetItem(index).GetText()
            index = self._flist.GetNextSelected(index)
        paths = self._paths.copy()
        names = list(paths.keys())
        idx = names.index(txt)
        if obj is self.bup:
            names[idx], names[idx - 1] = names[idx - 1], names[idx]
        elif obj is self.bdw:
            names[idx], names[idx + 1] = names[idx + 1], names[idx]
        self._paths = OrderedDict(zip(names, (paths[x] for x in names)))
        self._flist.reset()
        for path in self._paths.values():
            self._flist.InsertItem(CeListPathItem(path))

    def _button_validate_pressed(self, evt):
        create_ebucket()
        init_index()
        errs = 0
        for module in self._paths.values():
            err = process_module([str(f) for f in module.events_files])
            errs += err
        if errs > 0:
            self._show_warning(f"{errs} xml files couldn't be validated, please check the logs.")

    def _button_save_pressed(self, evt):
        if not self._paths or not self.xsdentry.GetValue():
            return
        fconf = wx.FileConfig(
            APPNAME, localFilename=str(self._conffile), style=wx.CONFIG_USE_LOCAL_FILE
        )
        fconf.SetPath("/general")
        fconf.Write("CE_XSDFILE", self.xsdentry.GetValue())
        n = count()
        for path in self._paths.values():
            key = "CeModulePath%s" % next(n)
            fconf.Write(key, str(path._path))
        fconf.WriteInt("CeModulePathAmount", next(n))
        fconf.Flush()
        self._show_notice("Settings properly saved.")

    def _load_conf(self):
        if not os.path.exists(self._conffile):
            return
        conf = wx.FileConfig(
            APPNAME, localFilename=str(self._conffile), style=wx.CONFIG_USE_LOCAL_FILE
        )
        conf.SetPath("/general")
        path_amount = conf.ReadInt("CeModulePathAmount")
        for n in range(path_amount):
            p = CePath(conf.Read("CeModulePath%i" % n))
            self._paths[p.name] = p
            self._flist.InsertItem(CeListPathItem(p))
        self.xsdentry.SetValue(conf.Read("CE_XSDFILE"))
        init_xsdfile(conf.Read("CE_XSDFILE"))

    def _on_mouse_event(self, evt: wx.MouseEvent):
        obj: wxst.GenStaticText = evt.GetEventObject()
        match obj, evt.Entering(), evt.Leaving():
            case self._warningtxt, True, False:
                obj.SetForegroundColour((200, 0, 0))
            case self._warningtxt, False, True:
                obj.SetForegroundColour((255, 0, 0))
            case self._noticetxt, True, False:
                obj.SetForegroundColour((0, 200, 0))
            case self._noticetxt, False, True:
                obj.SetForegroundColour((0, 255, 0))
            case _:
                obj.SetLabel("")
                obj.Hide()
                self._bsizer.Layout()

    def _show_notice(self, txt: str):
        """Show notice text. Empty 'txt' value hides widget."""
        self._noticetxt.SetLabel(txt)
        if not txt:
            self._noticetxt.Hide()
        else:
            self._noticetxt.ShowWithEffect(wx.SHOW_EFFECT_EXPAND)
        self._bsizer.Layout()

    def _show_warning(self, txt: str):
        """Show warning text. Empty 'txt' value hides widget."""
        self._warningtxt.SetLabel(txt)
        if not txt:
            self._warningtxt.Hide()
        else:
            self._warningtxt.ShowWithEffect(wx.SHOW_EFFECT_EXPAND)
        self._bsizer.Layout()


class CeStoriesViewer(wx.App):
    def OnInit(self):
        global LAUNCH_SETTINGS
        self.SetAppName(APPNAME)
        if PORTABLE:
            conf = get_config("settings")
            if os.path.exists(conf) and not LAUNCH_SETTINGS:
                window = MainWindow(conf)
            else:
                window = CeSettingsWindow(None, conf)
            # window = CeSettingsWindow(None, conf)
        else:
            raise Exception("Non portable version not written yet.")

        window.Show()
        self.SetTopWindow(window)
        return True


def launch(settings=False):
    global LAUNCH_SETTINGS
    LAUNCH_SETTINGS = settings
    app = CeStoriesViewer()
    app.MainLoop()
