# -*- coding: utf-8 -*-
# Licensed under the EUPL v1.2
# © 2024 bicobus <bicobus@keemail.me>
import logging
import os
from itertools import count

import wx
import wx.svg
import wx.lib.stattext as wxst
from wx.lib.agw.multidirdialog import MultiDirDialog
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
    get_xsdfile,
    init_bigbadxml,
)
from pycestorieseditor.config import get_config
from pycestorieseditor.wxui import MainWindow

logger = logging.getLogger(__name__)
LAUNCH_SETTINGS = False

svgicon = b"""\
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   width="128"
   height="128"
   viewBox="0 0 128 128"
   version="1.1"
   id="svg5"
   inkscape:version="1.2.2 (b0a8486541, 2022-12-01)"
   sodipodi:docname="icon.svg"
   xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
   xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <sodipodi:namedview
     id="namedview7"
     pagecolor="#ffffff"
     bordercolor="#999999"
     borderopacity="1"
     inkscape:showpageshadow="0"
     inkscape:pageopacity="0"
     inkscape:pagecheckerboard="0"
     inkscape:deskcolor="#d1d1d1"
     inkscape:document-units="px"
     showgrid="false"
     inkscape:zoom="5.6568543"
     inkscape:cx="52.679455"
     inkscape:cy="69.826794"
     inkscape:window-width="1920"
     inkscape:window-height="1011"
     inkscape:window-x="0"
     inkscape:window-y="40"
     inkscape:window-maximized="1"
     inkscape:current-layer="layer1" />
  <defs
     id="defs2" />
  <g
     inkscape:groupmode="layer"
     id="layer4"
     inkscape:label="Layer 2">
    <rect
       style="fill:#f1e9f1;fill-rule:evenodd;stroke:#f1e9f1;stroke-width:1.00779;stroke-linejoin:round;stroke-dasharray:none"
       id="rect6787"
       width="127.06355"
       height="127.07146"
       x="0.60600376"
       y="0.57624954" />
  </g>
  <g
     inkscape:label="Layer 1"
     inkscape:groupmode="layer"
     id="layer1">
    <path
       id="path6326"
       style="fill:#4b2d83;fill-rule:evenodd;stroke:#281845;stroke-width:1.44735;stroke-linejoin:round;stroke-dasharray:none"
       inkscape:transform-center-x="-0.19999032"
       inkscape:transform-center-y="-0.52014708"
       d="m 27.969293,-20.36815 a 52.031013,52.031013 0 0 0 -4.450902,0.319851 l -1.633049,9.419875 a 42.728813,42.728813 0 0 0 -8.404006,2.2119368 L 7.629391,-16.135738 a 52.031013,52.031013 0 0 0 -4.9486996,2.484485 l 2.3448323,9.2914833 a 42.728813,42.728813 0 0 0 -6.6560814,5.3631572 l -8.4625693,-4.6581309 a 52.031013,52.031013 0 0 0 -3.565677,4.34728767 l 5.9352859,7.55256913 a 42.728813,42.728813 0 0 0 -3.8179549,7.4376906 l -9.600072,-0.813145 a 52.031013,52.031013 0 0 0 -1.531687,5.51182 l 8.518881,4.498205 a 42.728813,42.728813 0 0 0 -0.590149,6.79123 42.728813,42.728813 0 0 0 0.09685,1.36275 l -9.075245,3.153473 a 52.031013,52.031013 0 0 0 0.831166,5.755089 l 9.638364,0.646461 a 42.728813,42.728813 0 0 0 2.745775,7.512024 l -6.989448,6.556971 a 52.031013,52.031013 0 0 0 3.103918,4.996002 l 9.0910129,-3.338176 a 42.728813,42.728813 0 0 0 5.42622604,5.728059 l -3.70983604,8.813957 a 52.031013,52.031013 0 0 0 4.8743679,3.35845 l 6.9669235,-6.766453 a 42.728813,42.728813 0 0 0 7.2214537,3.034091 l 0.195966,9.611334 a 52.031013,52.031013 0 0 0 5.800138,1.132996 l 3.624242,-9.043706 a 42.728813,42.728813 0 0 0 2.892184,0.207227 42.728813,42.728813 0 0 0 4.955458,-0.355891 l 4.117536,8.764403 a 52.031013,52.031013 0 0 0 5.723553,-1.268148 L 42.4167,71.767324 a 42.728813,42.728813 0 0 0 7.210191,-3.360702 l 7.367865,6.367764 a 52.031013,52.031013 0 0 0 4.63561,-3.468821 l -4.286471,-8.728363 a 42.728813,42.728813 0 0 0 5.324865,-6.126747 l 9.365815,2.83362 a 52.031013,52.031013 0 0 0 2.732262,-5.005012 l -7.419675,-6.189817 a 42.728813,42.728813 0 0 0 2.412407,-7.95351 l 9.737475,-1.22535 a 52.031013,52.031013 0 0 0 0.398685,-5.590657 l -9.248682,-2.62414 a 42.728813,42.728813 0 0 0 -1.090201,-8.435541 l 8.388242,-5.074838 a 52.031013,52.031013 0 0 0 -1.903345,-5.187464 l -9.487455,1.360498 a 42.728813,42.728813 0 0 0 -4.55001,-7.3678649 l 5.5839,-8.0233363 a 52.031013,52.031013 0 0 0 -3.82246,-3.919316 l -8.102174,5.09511069 A 42.728813,42.728813 0 0 0 48.408303,-5.7472979 l 1.831268,-9.5685381 a 52.031013,52.031013 0 0 0 -5.072587,-2.004708 l -5.324865,7.9445003 a 42.728813,42.728813 0 0 0 -8.640517,-1.4596073 l -2.211935,-9.46042 a 52.031013,52.031013 0 0 0 -1.020374,-0.07208 z m 0.01352,41.87587 a 10.154132,10.154132 0 0 1 10.156436,10.149679 v 0.0045 A 10.154132,10.154132 0 0 1 27.985062,41.81608 10.154132,10.154132 0 0 1 17.830878,31.664149 10.154132,10.154132 0 0 1 27.982809,21.507714 Z"
       inkscape:label="Gear" />
    <path
       id="path6328"
       style="fill:#05285b;fill-rule:evenodd;stroke:#073984;stroke-width:1.44735;stroke-linejoin:round;stroke-dasharray:none"
       inkscape:transform-center-x="-0.19999032"
       inkscape:transform-center-y="-0.52014708"
       d="m 101.64248,42.299103 a 52.031013,52.031013 0 0 0 -4.450899,0.319851 l -1.633049,9.419875 a 42.728813,42.728813 0 0 0 -8.404006,2.211937 l -5.851945,-7.719251 a 52.031013,52.031013 0 0 0 -4.9487,2.484485 l 2.344833,9.291483 a 42.728813,42.728813 0 0 0 -6.656082,5.363157 l -8.462569,-4.658131 a 52.031013,52.031013 0 0 0 -3.565677,4.347288 l 5.935286,7.552569 a 42.728813,42.728813 0 0 0 -3.817955,7.437691 l -9.600072,-0.813145 a 52.031013,52.031013 0 0 0 -1.531687,5.51182 l 8.518881,4.498205 a 42.728813,42.728813 0 0 0 -0.590149,6.79123 42.728813,42.728813 0 0 0 0.09685,1.36275 l -9.075245,3.153473 a 52.031013,52.031013 0 0 0 0.831166,5.75509 l 9.638364,0.64646 a 42.728813,42.728813 0 0 0 2.745775,7.51202 l -6.989448,6.55697 a 52.031013,52.031013 0 0 0 3.103918,4.99601 l 9.091013,-3.33818 a 42.728813,42.728813 0 0 0 5.426226,5.72806 l -3.709836,8.81396 a 52.031013,52.031013 0 0 0 4.874368,3.35845 l 6.966923,-6.76646 a 42.728813,42.728813 0 0 0 7.221454,3.03409 l 0.195966,9.61134 a 52.031013,52.031013 0 0 0 5.800138,1.13299 l 3.624242,-9.0437 a 42.728813,42.728813 0 0 0 2.892186,0.20723 42.728813,42.728813 0 0 0 4.95546,-0.3559 l 4.11753,8.76441 a 52.031013,52.031013 0 0 0 5.72356,-1.26815 l -0.36941,-9.7645 a 42.728813,42.728813 0 0 0 7.21019,-3.36071 l 7.36787,6.36777 a 52.031013,52.031013 0 0 0 4.63561,-3.46882 l -4.28647,-8.72837 a 42.728813,42.728813 0 0 0 5.32486,-6.12674 l 9.36582,2.83362 a 52.031013,52.031013 0 0 0 2.73226,-5.00501 l -7.41968,-6.18982 a 42.728813,42.728813 0 0 0 2.41241,-7.95351 l 9.73747,-1.22535 a 52.031013,52.031013 0 0 0 0.39869,-5.590658 l -9.24868,-2.62414 a 42.728813,42.728813 0 0 0 -1.0902,-8.435541 l 8.38824,-5.074838 a 52.031013,52.031013 0 0 0 -1.90335,-5.187464 l -9.48745,1.360498 a 42.728813,42.728813 0 0 0 -4.55001,-7.367865 l 5.5839,-8.023336 a 52.031013,52.031013 0 0 0 -3.82246,-3.919316 l -8.10218,5.09511 a 42.728813,42.728813 0 0 0 -7.25524,-4.890135 l 1.83127,-9.568538 a 52.031013,52.031013 0 0 0 -5.07259,-2.004708 l -5.32486,7.9445 a 42.728813,42.728813 0 0 0 -8.64052,-1.459607 l -2.21193,-9.46042 a 52.031013,52.031013 0 0 0 -1.02038,-0.07208 z m 0.0135,41.87587 a 10.154132,10.154132 0 0 1 10.15644,10.149679 v 0.0045 A 10.154132,10.154132 0 0 1 101.65825,104.48333 10.154132,10.154132 0 0 1 91.504068,94.331402 10.154132,10.154132 0 0 1 101.656,84.174967 Z"
       inkscape:label="Gear" />
    <rect
       style="fill:none;fill-rule:evenodd;stroke:#000000;stroke-width:8;stroke-linejoin:miter;stroke-miterlimit:4;stroke-dasharray:none;paint-order:normal"
       id="rect7373"
       width="123.34502"
       height="123.35346"
       x="2.3274918"
       y="2.3232689" />
  </g>
</svg>
"""


class ArtProvider(wx.ArtProvider):
    def CreateBitmap(self, id_art, client, size):
        if size == wx.DefaultSize:
            size = wx.Size(32, 32)
        if id_art == 'ICON':
            svg = wx.svg.SVGimage.CreateFromBytes(svgicon)
            return svg.ConvertToScaledBitmap(size)
        return wx.NullBitmap


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

        self._warningtxt = wxst.GenStaticText(panel, wx.ID_ANY, label="")
        self._warningtxt.SetForegroundColour((255, 0, 0))
        self._warningtxt.Hide()
        self._noticetxt = wxst.GenStaticText(panel, wx.ID_ANY, label="Lorem ipsum dolor sit amet")
        self._noticetxt.SetForegroundColour((0, 255, 0))
        self._noticetxt.Hide()

        self._flist = CeListBox(window, wx.ID_ANY)
        moduleinfo = wx.StaticText(
            window,
            wx.ID_ANY,
            "The order in which the modules are added determine the order\n"
            "duplicate events are overriden. The last most module takes\n"
            "precedence.",
            (20, 100),
        )
        buttonadd = wx.Button(window, wx.ID_ANY, "+", (50, 50))
        buttonadd.SetToolTip("Add a module to the list")
        buttonrem = wx.Button(window, wx.ID_ANY, "-", (50, 50))
        buttonrem.SetToolTip("Remove a module from the list")
        buttonclr = wx.Button(window, wx.ID_ANY, "CLR", (50, 50))
        buttonclr.SetToolTip("Clear the list of any entry")
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

        fsizer.Add((20, 20), 0, wx.LEFT, 5)
        fsizer.Add(moduleinfo, 0, wx.ALL | wx.EXPAND, 5)
        fsizer.Add((20, 20), 0, wx.RIGHT, 5)
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
            self.xsdentry.SetToolTip(pathname)

    def _button_add_folder_pressed(self, evt):
        # FIXME wxpython wx.DirDialog doesn't support wx.DD_MULTIPLE just yet
        #  Must use inferior MultiDirDialog instead. Shows non-native UI.
        dlg = MultiDirDialog(
            self,
            message="Chose one or more folder, they must be CEEvent story submodules.",
            agwStyle=wx.DD_MULTIPLE | wx.DD_DIR_MUST_EXIST,
        )

        if dlg.ShowModal() == wx.ID_OK:
            try:
                paths = dlg.GetPaths()
                for path in paths:
                    path = CePath(path)
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
        self._paths = {}
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
        names: list = list(paths.keys())
        idx = names.index(txt)
        if obj is self.bup:
            names[idx], names[idx - 1] = names[idx - 1], names[idx]
        elif obj is self.bdw:
            names[idx], names[idx + 1] = names[idx + 1], names[idx]
        self._paths = dict(zip(names, (paths[x] for x in names)))
        self._flist.reset()
        for path in self._paths.values():
            self._flist.InsertItem(CeListPathItem(path))
        # Reselect item
        idx = self._flist.FindItem(-1, txt)
        self._flist.Select(idx)

    def _button_validate_pressed(self, evt):
        if not get_xsdfile():
            self._show_warning("Please select a valid XSD file before validating.")
            return

        dialog = wx.ProgressDialog(
            "Validation",
            "Validating xml files...",
            maximum=100,
            style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE | wx.PD_ELAPSED_TIME | wx.PD_SMOOTH,
        )

        def pulse(m=None):
            dialog.Pulse(m or "")
            wx.MilliSleep(1)
            wx.Yield()

        create_ebucket()
        init_index()
        init_bigbadxml()
        errs = 0
        for module in self._paths.values():
            pulse("Processing module... {}".format(module.name))
            err = process_module([str(f) for f in module.events_files], pulse)
            errs += err
        if errs > 0:
            self._show_warning(f"{errs} xml files couldn't be validated, please check the logs.")
        else:
            self._show_notice("All modules successfully validated.")

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
        self.xsdentry.SetToolTip(conf.Read("CE_XSDFILE"))
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
        self.SetAppName(APPNAME)
        return True


def launch(settings=False):
    global LAUNCH_SETTINGS
    LAUNCH_SETTINGS = settings
    app = CeStoriesViewer()
    wx.ArtProvider.Push(ArtProvider())
    logger.info("Launching with wxPython %s" % wx.version())

    if PORTABLE:
        conf = get_config("settings")
        if os.path.exists(conf) and not LAUNCH_SETTINGS:
            window = MainWindow(conf)
        else:
            window = CeSettingsWindow(None, conf)
    else:
        raise Exception("Non portable version not written yet.")

    window.Show()
    app.SetTopWindow(window)
    app.MainLoop()
