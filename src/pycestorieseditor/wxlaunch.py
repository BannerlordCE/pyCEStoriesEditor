# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2023 bicobus <bicobus@keemail.me>
import logging
import os
from itertools import count

import wx
import wx.lib.stattext as wxst
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin
from wx.lib.scrolledpanel import ScrolledPanel

from pycestorieseditor import PORTABLE, APPNAME
from pycestorieseditor.ceevents import (
    init_xsdfile,
    populate_children,
    create_ebucket,
    get_ebucket,
    process_xml_files, NotBannerLordModule, NotCeSubmodule, CePath,
)
from pycestorieseditor.config import get_config
from pycestorieseditor.wxui import MainWindow

logger = logging.getLogger(__name__)


class CeListPathItem(wx.ListItem):
    _wid = count()

    def __init__(self, item: CePath):
        super().__init__()
        self._cepath = item
        self.SetText(item.name)
        self.SetId(next(CeListPathItem._wid))


class CeListBox(wx.ListCtrl, ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, style=wx.LC_REPORT | wx.LC_NO_HEADER | wx.LC_SINGLE_SEL)
        ListCtrlAutoWidthMixin.__init__(self)
        self.InsertColumn(0, "Path")
        self.setResizeColumn(0)

    def reset(self):
        self.ClearAll()
        self.InsertColumn(0, "Path")
        # self.setResizeColumn(0)


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

        self._paths: dict[str, CePath] = {}
        self._conffile = conffile

        panel = wx.Panel(self)
        window = ScrolledPanel(panel, wx.ID_ANY)
        window.SetupScrolling(scroll_x=False)
        window.SetAutoLayout(1)
        self._bsizer = bsizer = wx.BoxSizer(wx.VERTICAL)
        fsizer = wx.FlexGridSizer(3, gap=(5, 5))
        fsizer.AddGrowableCol(1)
        addremovesizer = wx.BoxSizer(wx.VERTICAL)

        self._warningtxt = wxst.GenStaticText(panel, wx.ID_ANY, label="Sample text")
        self._warningtxt.SetForegroundColour((255, 0, 0))
        self._warningtxt.Hide()
        self._flist = CeListBox(window, wx.ID_ANY)
        buttonadd = wx.Button(window, wx.ID_ANY, "+", (50, 50))
        buttonrem = wx.Button(window, wx.ID_ANY, "-", (50, 50))
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
        bsizer.Add(window, 1, wx.EXPAND, 0)

        self.Bind(wx.EVT_BUTTON, self._button_add_folder_pressed, buttonadd)
        self.Bind(wx.EVT_BUTTON, self._button_rem_folder_pressed, buttonrem)
        self.Bind(wx.EVT_BUTTON, self._button_validate_pressed, btnvalidate)
        self.Bind(wx.EVT_BUTTON, self._button_xsd_pressed, xsdbutton)
        self.Bind(wx.EVT_BUTTON, self._button_save_pressed, btnsave)
        self._warningtxt.Bind(wx.EVT_ENTER_WINDOW, self._on_mouse_event, self._warningtxt)
        self._warningtxt.Bind(wx.EVT_LEAVE_WINDOW, self._on_mouse_event, self._warningtxt)
        self._warningtxt.Bind(wx.EVT_LEFT_DOWN, self._on_mouse_event, self._warningtxt)

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

    def _button_validate_pressed(self, evt):
        create_ebucket()

        for module in self._paths.values():
            process_xml_files([str(f) for f in module.events])
        errs = populate_children(get_ebucket())
        print(errs)

        # errs = populate_children()
        # if errs > 0:
        #     self._flist.reset()
        #     CeListPathItem._wid = count()
        #     for path in self._paths.values():
        #         self._flist.InsertItem(CeListPathItem(path))

    def _button_save_pressed(self, evt):
        if not self._paths or not self.xsdentry.GetValue():
            return
        fconf = wx.FileConfig(APPNAME, localFilename=self._conffile, style=wx.CONFIG_USE_LOCAL_FILE)
        fconf.SetPath("/general")
        fconf.Write("CE_XSDFILE", self.xsdentry.GetValue())
        n = count()
        for path in self._paths.values():
            key = "CeModulePath%s" % next(n)
            fconf.Write(key, str(path._path))
        fconf.WriteInt("CeModulePathAmount", next(n))
        fconf.Flush()

    def _load_conf(self):
        conf = wx.FileConfig(APPNAME, localFilename=self._conffile, style=wx.CONFIG_USE_LOCAL_FILE)
        conf.SetPath("/general")
        path_amount = conf.ReadInt("CeModulePathAmount")
        for n in range(path_amount):
            p = conf.Read("CeModulePath%i" % n)
            self._paths[p] = CePath(p)
            self._flist.InsertItem(CeListPathItem(self._paths[p]))
        self.xsdentry.SetValue(conf.Read("CE_XSDFILE"))
        init_xsdfile(conf.Read("CE_XSDFILE"))

    def _on_mouse_event(self, evt: wx.MouseEvent):
        obj: wxst.GenStaticText = evt.GetEventObject()
        if evt.Entering():
            obj.SetForegroundColour((200, 0, 0))
        elif evt.Leaving():
            obj.SetForegroundColour((255, 0, 0))
        else:
            obj.SetLabel("")
            obj.Hide()
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
        self.SetAppName(APPNAME)
        if PORTABLE:
            conf = get_config("settings")
            if os.path.exists(conf):
                window = MainWindow(conf)
            else:
                window = CeSettingsWindow(None, conf)
            # window = CeSettingsWindow(None, conf)
        else:
            raise Exception("Non portable version not written yet.")

        window.Show()
        self.SetTopWindow(window)
        return True


def launch():
    app = CeStoriesViewer()
    app.MainLoop()
