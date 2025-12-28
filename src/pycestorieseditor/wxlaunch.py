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
    init_bigbagxml,
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

svgicon_details = b"""<?xml version="1.0" encoding="UTF-8"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->
<svg id="svg5" width="128" height="128" version="1.1" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
 <g id="layer4">
  <rect id="rect6787" x=".606" y=".57625" width="127.06" height="127.07" fill="#f1e9f1" fill-rule="evenodd" stroke="#f1e9f1" stroke-linejoin="round" stroke-width="1.0078"/>
 </g>
 <g id="layer1">
  <path id="path6326" d="m27.969-20.368a52.031 52.031 0 0 0-4.4509 0.31985l-1.633 9.4199a42.729 42.729 0 0 0-8.404 2.2119l-5.8519-7.7193a52.031 52.031 0 0 0-4.9487 2.4845l2.3448 9.2915a42.729 42.729 0 0 0-6.6561 5.3632l-8.4626-4.6581a52.031 52.031 0 0 0-3.5657 4.3473l5.9353 7.5526a42.729 42.729 0 0 0-3.818 7.4377l-9.6001-0.81314a52.031 52.031 0 0 0-1.5317 5.5118l8.5189 4.4982a42.729 42.729 0 0 0-0.59015 6.7912 42.729 42.729 0 0 0 0.09685 1.3628l-9.0752 3.1535a52.031 52.031 0 0 0 0.83117 5.7551l9.6384 0.64646a42.729 42.729 0 0 0 2.7458 7.512l-6.9894 6.557a52.031 52.031 0 0 0 3.1039 4.996l9.091-3.3382a42.729 42.729 0 0 0 5.4262 5.7281l-3.7098 8.814a52.031 52.031 0 0 0 4.8744 3.3584l6.9669-6.7665a42.729 42.729 0 0 0 7.2215 3.0341l0.19597 9.6113a52.031 52.031 0 0 0 5.8001 1.133l3.6242-9.0437a42.729 42.729 0 0 0 2.8922 0.20723 42.729 42.729 0 0 0 4.9555-0.35589l4.1175 8.7644a52.031 52.031 0 0 0 5.7236-1.2681l-0.3694-9.7645a42.729 42.729 0 0 0 7.2102-3.3607l7.3679 6.3678a52.031 52.031 0 0 0 4.6356-3.4688l-4.2865-8.7284a42.729 42.729 0 0 0 5.3249-6.1267l9.3658 2.8336a52.031 52.031 0 0 0 2.7323-5.005l-7.4197-6.1898a42.729 42.729 0 0 0 2.4124-7.9535l9.7375-1.2254a52.031 52.031 0 0 0 0.39868-5.5907l-9.2487-2.6241a42.729 42.729 0 0 0-1.0902-8.4355l8.3882-5.0748a52.031 52.031 0 0 0-1.9033-5.1875l-9.4875 1.3605a42.729 42.729 0 0 0-4.55-7.3679l5.5839-8.0233a52.031 52.031 0 0 0-3.8225-3.9193l-8.1022 5.0951a42.729 42.729 0 0 0-7.2552-4.8901l1.8313-9.5685a52.031 52.031 0 0 0-5.0726-2.0047l-5.3249 7.9445a42.729 42.729 0 0 0-8.6405-1.4596l-2.2119-9.4604a52.031 52.031 0 0 0-1.0204-0.07208zm0.01352 41.876a10.154 10.154 0 0 1 10.156 10.15v0.0045a10.154 10.154 0 0 1-10.154 10.154 10.154 10.154 0 0 1-10.154-10.152 10.154 10.154 0 0 1 10.152-10.156z" fill="#4b2d83" fill-rule="evenodd" stroke="#281845" stroke-linejoin="round" stroke-width="1.4474"/>
  <path id="path6328" d="m101.64 42.299a52.031 52.031 0 0 0-4.4509 0.31985l-1.633 9.4199a42.729 42.729 0 0 0-8.404 2.2119l-5.8519-7.7193a52.031 52.031 0 0 0-4.9487 2.4845l2.3448 9.2915a42.729 42.729 0 0 0-6.6561 5.3632l-8.4626-4.6581a52.031 52.031 0 0 0-3.5657 4.3473l5.9353 7.5526a42.729 42.729 0 0 0-3.818 7.4377l-9.6001-0.81314a52.031 52.031 0 0 0-1.5317 5.5118l8.5189 4.4982a42.729 42.729 0 0 0-0.59015 6.7912 42.729 42.729 0 0 0 0.09685 1.3628l-9.0752 3.1535a52.031 52.031 0 0 0 0.83117 5.7551l9.6384 0.64646a42.729 42.729 0 0 0 2.7458 7.512l-6.9894 6.557a52.031 52.031 0 0 0 3.1039 4.996l9.091-3.3382a42.729 42.729 0 0 0 5.4262 5.7281l-3.7098 8.814a52.031 52.031 0 0 0 4.8744 3.3584l6.9669-6.7665a42.729 42.729 0 0 0 7.2215 3.0341l0.19597 9.6113a52.031 52.031 0 0 0 5.8001 1.133l3.6242-9.0437a42.729 42.729 0 0 0 2.8922 0.20723 42.729 42.729 0 0 0 4.9555-0.3559l4.1175 8.7644a52.031 52.031 0 0 0 5.7236-1.2682l-0.36941-9.7645a42.729 42.729 0 0 0 7.2102-3.3607l7.3679 6.3678a52.031 52.031 0 0 0 4.6356-3.4688l-4.2865-8.7284a42.729 42.729 0 0 0 5.3249-6.1267l9.3658 2.8336a52.031 52.031 0 0 0 2.7323-5.005l-7.4197-6.1898a42.729 42.729 0 0 0 2.4124-7.9535l9.7375-1.2254a52.031 52.031 0 0 0 0.39869-5.5907l-9.2487-2.6241a42.729 42.729 0 0 0-1.0902-8.4355l8.3882-5.0748a52.031 52.031 0 0 0-1.9034-5.1875l-9.4874 1.3605a42.729 42.729 0 0 0-4.55-7.3679l5.5839-8.0233a52.031 52.031 0 0 0-3.8225-3.9193l-8.1022 5.0951a42.729 42.729 0 0 0-7.2552-4.8901l1.8313-9.5685a52.031 52.031 0 0 0-5.0726-2.0047l-5.3249 7.9445a42.729 42.729 0 0 0-8.6405-1.4596l-2.2119-9.4604a52.031 52.031 0 0 0-1.0204-0.07208zm0.0135 41.876a10.154 10.154 0 0 1 10.156 10.15v0.0045a10.154 10.154 0 0 1-10.154 10.154 10.154 10.154 0 0 1-10.154-10.152 10.154 10.154 0 0 1 10.152-10.156z" fill="#05285b" fill-rule="evenodd" stroke="#073984" stroke-linejoin="round" stroke-width="1.4474"/>
  <rect id="rect7373" x="2.3275" y="2.3233" width="123.35" height="123.35" fill="none" stroke="#000" stroke-width="8" style="paint-order:normal"/>
  <path id="path524" d="m6.4523 97v-24.622l1.9223-1.8985 2.0072 0.89437c1.104 0.4919 2.5325 1.0777 3.1746 1.3018l1.1673 0.4074 0.06272 4.6411c0.05177 3.8308 0.10902 4.6872 0.32789 4.9049 0.32439 0.32273 5.4523 1.3795 6.3326 1.305l0.63381-0.05362 3.5518-8.8388 6.8943-0.03072 1.9299 4.1283c1.0615 2.2706 2.0378 4.2179 2.1697 4.3273 0.17934 0.14884 0.6468 0.12033 1.8549-0.11313 2.5996-0.50238 4.773-1.0976 4.9484-1.3552 0.15545-0.22828 0.08911-3.8969-0.14204-7.8554l-0.1041-1.7826 0.59364-0.23157c0.3265-0.12736 1.7621-0.7874 3.1903-1.4667l2.5966-1.2352 3.4613 2.9842c2.1101 1.8192 3.6349 3.0062 3.906 3.0407 0.4826 0.06135 3.1249-1.7106 4.7651-3.1956l0.87516-0.79233-4.1918-8.6712 1.6423-1.8304c0.90326-1.0067 1.9247-2.2083 2.2698-2.6701 0.34513-0.46183 0.69662-0.83969 0.78108-0.83969 0.08447 0 2.1407 0.60324 4.5694 1.3405 2.4287 0.7373 4.528 1.2975 4.6651 1.2449 0.55237-0.21196 3.4025-5.5061 3.2201-5.9813-0.06002-0.15642-1.5662-1.4964-3.347-2.9777-1.7808-1.4813-3.3793-2.8254-3.5522-2.9869-0.30058-0.28079-0.29407-0.3474 0.14865-1.5212 0.25465-0.67515 0.73407-2.2152 1.0654-3.4223 0.33132-1.2071 0.62682-2.2191 0.65668-2.249 0.02985-0.02985 2.1085-0.31057 4.6192-0.62382 3.1919-0.39823 4.6646-0.65228 4.8962-0.84459 0.28305-0.23503 0.36208-0.71901 0.54326-3.3266 0.18274-2.6302 0.17657-3.0853-0.04467-3.2959-0.14118-0.13436-2.1659-0.77786-4.4993-1.43-2.3335-0.65214-4.3301-1.257-4.437-1.3441-0.1069-0.08711-0.24591-0.93419-0.30891-1.8824-0.10246-1.5422-0.51706-4.4184-0.7498-5.2016-0.06808-0.2291 0.83027-0.84574 3.9918-2.74 2.7141-1.6262 4.1101-2.5635 4.1704-2.8002 0.15186-0.59521-1.7844-5.8467-2.2522-6.1085-0.14229-0.07963-2.0745 0.12248-4.3999 0.46023-2.2804 0.33122-4.3551 0.6045-4.6104 0.60729-0.39592 0.0043-0.55813-0.1736-1.1022-1.209-0.35088-0.66774-1.1007-1.9206-1.6662-2.7842-0.56553-0.86358-1.0885-1.6696-1.1621-1.7911-0.10689-0.17642 5.7306-0.22097 28.956-0.22097h29.09v19.534c0 10.744-0.0303 19.534-0.0673 19.534s-0.60872-0.20377-1.2704-0.45283c-0.66168-0.24906-1.3672-0.40818-1.5678-0.3536-0.2273 0.06183-1.2171 1.3818-2.6263 3.5022-1.2438 1.8716-2.3973 3.5794-2.5633 3.7951l-0.30176 0.39206-2.1094-0.43005c-1.1602-0.23653-2.8773-0.52312-3.8159-0.63687l-1.7064-0.20682-1.0231-4.4398c-0.56273-2.4419-1.145-4.579-1.2938-4.7491-0.22358-0.25549-0.56606-0.30801-1.9669-0.3016-2.2658 0.01038-4.2421 0.2527-4.5469 0.55751-0.14657 0.14657-0.53592 1.9111-0.94996 4.3052-0.92674 5.3586-0.84183 5.029-1.2957 5.0293-0.54503 3.53e-4 -3.8307 0.80918-5.5492 1.3661-0.79923 0.259-1.482 0.4354-1.5173 0.392-0.03531-0.04341-1.3148-1.7296-2.8433-3.747-2.2118-2.9194-2.8627-3.6681-3.189-3.6681-0.46579 0-4.7321 2.0624-5.4046 2.6126l-0.44194 0.36162 1.1092 4.4791c0.61007 2.4635 1.1073 4.5356 1.1049 4.6047-0.0024 0.06909-0.5867 0.55629-1.2985 1.0826s-2.0002 1.5636-2.8633 2.3051c-0.86306 0.74142-1.6226 1.348-1.6879 1.348-0.06526 0-1.8489-0.95225-3.9637-2.1161-2.1148-1.1639-4.0002-2.1653-4.1898-2.2255-0.4085-0.12965-1.11 0.56053-3.0622 3.0126-1.2176 1.5294-1.3965 1.838-1.3448 2.3192 0.01153 0.10707 1.2901 1.8121 2.8413 3.789l2.8203 3.5943-0.6248 1.0723c-0.34364 0.58978-1.0995 2.0468-1.6798 3.2379-0.99306 2.0384-1.0855 2.1655-1.5741 2.1655-0.28552 0-2.3237-0.16019-4.5292-0.35597s-4.1505-0.31142-4.322-0.25696c-0.19144 0.06076-0.45194 0.52268-0.67431 1.1957-0.58474 1.7697-1.3668 4.9605-1.2954 5.2858 0.04053 0.18486 1.6396 1.1285 4.1647 2.4576 2.2544 1.1866 4.1263 2.1794 4.1597 2.2062 0.03347 0.02677-0.02695 0.75048-0.13427 1.6083-0.10732 0.85778-0.22797 2.4689-0.2681 3.5802l-0.07298 2.0206-8.7779 3.0595-0.06036 0.69226c-0.10715 1.2289 0.63081 5.9296 0.98678 6.2856 0.09173 0.0917 1.9493 0.2837 4.128 0.4266 2.1787 0.14289 4.2927 0.30253 4.6979 0.35476l0.73671 0.0949 0.38464 1.273c0.21155 0.70014 0.73941 2.1621 1.173 3.2487l0.78839 1.9758-1.4678 1.3944c-0.80729 0.76692-2.3031 2.1772-3.3239 3.1339-1.0769 1.0092-1.8787 1.9036-1.9098 2.1303-0.0295 0.21497 0.18926 0.80281 0.48614 1.3063 0.29688 0.5035 0.53978 0.95173 0.53978 0.99607 0 0.0443-11.256 0.0806-25.014 0.0806h-25.014z" fill="#32cd32" fill-rule="evenodd" stroke="#006400" stroke-width=".49498"/>
  <path id="path940" d="m26.163 40.832c-3.1435-0.62927-5.9232-3.0571-6.995-6.1096-1.9201-5.4682 1.7782-11.464 7.5942-12.311 4.4241-0.64482 8.9106 2.2883 10.201 6.6689 0.44479 1.5102 0.41775 3.7389-0.06443 5.3106-1.3857 4.5169-6.1299 7.3635-10.736 6.4415z" fill="#696969" fill-rule="evenodd" stroke="#696969" stroke-width=".49498"/>
  <path id="path1080" d="m98.726 103.19c-6.5767-2.2425-8.5315-10.54-3.6362-15.436 2.8677-2.8677 7.0859-3.5304 10.857-1.7058 2.1307 1.0308 4.2484 3.7093 4.7896 6.0581 0.30767 1.3352 0.23116 3.7163-0.16013 4.9832-0.86681 2.8064-3.3493 5.2852-6.1642 6.1552-1.6072 0.49672-4.1401 0.47218-5.6865-0.0551z" fill="#696969" fill-rule="evenodd" stroke="#696969" stroke-width=".49498"/>
 </g>
</svg>
"""

svgicon_preview = b"""<?xml version="1.0" encoding="UTF-8"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->
<svg id="svg5" width="128" height="128" version="1.1" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">
 <g id="layer4">
  <rect id="rect6787" x=".606" y=".57625" width="127.06" height="127.07" fill="#f1e9f1" fill-rule="evenodd" stroke="#f1e9f1" stroke-linejoin="round" stroke-width="1.0078"/>
 </g>
 <g id="layer1">
  <path id="path6326" d="m27.969-20.368a52.031 52.031 0 0 0-4.4509 0.31985l-1.633 9.4199a42.729 42.729 0 0 0-8.404 2.2119l-5.8519-7.7193a52.031 52.031 0 0 0-4.9487 2.4845l2.3448 9.2915a42.729 42.729 0 0 0-6.6561 5.3632l-8.4626-4.6581a52.031 52.031 0 0 0-3.5657 4.3473l5.9353 7.5526a42.729 42.729 0 0 0-3.818 7.4377l-9.6001-0.81314a52.031 52.031 0 0 0-1.5317 5.5118l8.5189 4.4982a42.729 42.729 0 0 0-0.59015 6.7912 42.729 42.729 0 0 0 0.09685 1.3628l-9.0752 3.1535a52.031 52.031 0 0 0 0.83117 5.7551l9.6384 0.64646a42.729 42.729 0 0 0 2.7458 7.512l-6.9894 6.557a52.031 52.031 0 0 0 3.1039 4.996l9.091-3.3382a42.729 42.729 0 0 0 5.4262 5.7281l-3.7098 8.814a52.031 52.031 0 0 0 4.8744 3.3584l6.9669-6.7665a42.729 42.729 0 0 0 7.2215 3.0341l0.19597 9.6113a52.031 52.031 0 0 0 5.8001 1.133l3.6242-9.0437a42.729 42.729 0 0 0 2.8922 0.20723 42.729 42.729 0 0 0 4.9555-0.35589l4.1175 8.7644a52.031 52.031 0 0 0 5.7236-1.2681l-0.3694-9.7645a42.729 42.729 0 0 0 7.2102-3.3607l7.3679 6.3678a52.031 52.031 0 0 0 4.6356-3.4688l-4.2865-8.7284a42.729 42.729 0 0 0 5.3249-6.1267l9.3658 2.8336a52.031 52.031 0 0 0 2.7323-5.005l-7.4197-6.1898a42.729 42.729 0 0 0 2.4124-7.9535l9.7375-1.2254a52.031 52.031 0 0 0 0.39868-5.5907l-9.2487-2.6241a42.729 42.729 0 0 0-1.0902-8.4355l8.3882-5.0748a52.031 52.031 0 0 0-1.9033-5.1875l-9.4875 1.3605a42.729 42.729 0 0 0-4.55-7.3679l5.5839-8.0233a52.031 52.031 0 0 0-3.8225-3.9193l-8.1022 5.0951a42.729 42.729 0 0 0-7.2552-4.8901l1.8313-9.5685a52.031 52.031 0 0 0-5.0726-2.0047l-5.3249 7.9445a42.729 42.729 0 0 0-8.6405-1.4596l-2.2119-9.4604a52.031 52.031 0 0 0-1.0204-0.07208zm0.01352 41.876a10.154 10.154 0 0 1 10.156 10.15v0.0045a10.154 10.154 0 0 1-10.154 10.154 10.154 10.154 0 0 1-10.154-10.152 10.154 10.154 0 0 1 10.152-10.156z" fill="#4b2d83" fill-rule="evenodd" stroke="#281845" stroke-linejoin="round" stroke-width="1.4474"/>
  <path id="path6328" d="m101.64 42.299a52.031 52.031 0 0 0-4.4509 0.31985l-1.633 9.4199a42.729 42.729 0 0 0-8.404 2.2119l-5.8519-7.7193a52.031 52.031 0 0 0-4.9487 2.4845l2.3448 9.2915a42.729 42.729 0 0 0-6.6561 5.3632l-8.4626-4.6581a52.031 52.031 0 0 0-3.5657 4.3473l5.9353 7.5526a42.729 42.729 0 0 0-3.818 7.4377l-9.6001-0.81314a52.031 52.031 0 0 0-1.5317 5.5118l8.5189 4.4982a42.729 42.729 0 0 0-0.59015 6.7912 42.729 42.729 0 0 0 0.09685 1.3628l-9.0752 3.1535a52.031 52.031 0 0 0 0.83117 5.7551l9.6384 0.64646a42.729 42.729 0 0 0 2.7458 7.512l-6.9894 6.557a52.031 52.031 0 0 0 3.1039 4.996l9.091-3.3382a42.729 42.729 0 0 0 5.4262 5.7281l-3.7098 8.814a52.031 52.031 0 0 0 4.8744 3.3584l6.9669-6.7665a42.729 42.729 0 0 0 7.2215 3.0341l0.19597 9.6113a52.031 52.031 0 0 0 5.8001 1.133l3.6242-9.0437a42.729 42.729 0 0 0 2.8922 0.20723 42.729 42.729 0 0 0 4.9555-0.3559l4.1175 8.7644a52.031 52.031 0 0 0 5.7236-1.2682l-0.36941-9.7645a42.729 42.729 0 0 0 7.2102-3.3607l7.3679 6.3678a52.031 52.031 0 0 0 4.6356-3.4688l-4.2865-8.7284a42.729 42.729 0 0 0 5.3249-6.1267l9.3658 2.8336a52.031 52.031 0 0 0 2.7323-5.005l-7.4197-6.1898a42.729 42.729 0 0 0 2.4124-7.9535l9.7375-1.2254a52.031 52.031 0 0 0 0.39869-5.5907l-9.2487-2.6241a42.729 42.729 0 0 0-1.0902-8.4355l8.3882-5.0748a52.031 52.031 0 0 0-1.9034-5.1875l-9.4874 1.3605a42.729 42.729 0 0 0-4.55-7.3679l5.5839-8.0233a52.031 52.031 0 0 0-3.8225-3.9193l-8.1022 5.0951a42.729 42.729 0 0 0-7.2552-4.8901l1.8313-9.5685a52.031 52.031 0 0 0-5.0726-2.0047l-5.3249 7.9445a42.729 42.729 0 0 0-8.6405-1.4596l-2.2119-9.4604a52.031 52.031 0 0 0-1.0204-0.07208zm0.0135 41.876a10.154 10.154 0 0 1 10.156 10.15v0.0045a10.154 10.154 0 0 1-10.154 10.154 10.154 10.154 0 0 1-10.154-10.152 10.154 10.154 0 0 1 10.152-10.156z" fill="#05285b" fill-rule="evenodd" stroke="#073984" stroke-linejoin="round" stroke-width="1.4474"/>
  <rect id="rect7373" x="2.3275" y="2.3233" width="123.35" height="123.35" fill="none" stroke="#000" stroke-width="8" style="paint-order:normal"/>
  <path id="path1528" d="m25.772 40.757c-3.9987-0.98208-6.8875-4.4649-7.1121-8.5745-0.15734-2.8793 0.8714-5.395 3.0309-7.4117 1.0754-1.0043 2.7082-1.8855 4.1213-2.224 1.1404-0.27322 3.2269-0.27589 4.3412-0.0055 3.3131 0.80376 5.9178 3.332 6.872 6.6702 0.22356 0.78212 0.2781 1.2868 0.27436 2.5387-0.0043 1.4369-0.03835 1.6618-0.42365 2.7978-1.3437 3.9616-4.8235 6.4729-8.9277 6.443-0.7606-0.0055-1.6245-0.09841-2.1763-0.23395z" fill="#696969" fill-rule="evenodd" stroke="#696969" stroke-width=".35"/>
  <path id="path1530" d="m100.43 103.63c-3.0835-0.43151-5.8117-2.4039-7.1623-5.1782-0.69218-1.4217-0.93155-2.4833-0.93247-4.1353-9.32e-4 -1.6726 0.21532-2.5877 0.9748-4.125 1.2617-2.554 3.3834-4.2532 6.1843-4.9531 1.5013-0.37516 3.6471-0.29482 5.0721 0.18991 1.4262 0.48515 2.6069 1.2244 3.6978 2.3154 1.0848 1.0848 1.8232 2.2604 2.3227 3.6978 0.31962 0.91991 0.34757 1.1502 0.34904 2.875 2e-3 1.7839-0.0173 1.9282-0.38832 2.9702-0.55882 1.5696-1.0785 2.3762-2.3667 3.6732-0.96747 0.97413-1.3098 1.2279-2.3125 1.7145-1.7746 0.86114-3.6983 1.1992-5.4384 0.95566z" fill="#696969" fill-rule="evenodd" stroke="#696969" stroke-width=".35"/>
  <path id="path1532" d="m6.375 97.004v-24.621l2.0573-1.9815 1.0651 0.5318c1.1476 0.57298 3.8678 1.6974 4.7038 1.9443l0.51371 0.15172 0.09175 4.6406c0.05047 2.5523 0.1434 4.7371 0.20651 4.855 0.14304 0.26727 0.52134 0.37552 3.1743 0.90832 2.7568 0.55366 3.4382 0.63048 3.7187 0.41925 0.12029-0.09059 0.99217-2.0952 1.9375-4.4546l1.7188-4.2899 3.0625-0.05277c1.6844-0.02903 3.2459-0.06733 3.47-0.08512l0.40753-0.03234 1.9604 4.1692c1.2344 2.6251 2.0604 4.2347 2.2304 4.3461 0.23815 0.15604 0.48952 0.13312 2.132-0.19445 2.4364-0.4859 4.32-0.9801 4.5315-1.1889 0.19718-0.19472 0.20116-1.4303 0.01772-5.507-0.06497-1.4438-0.1196-2.9952-0.1214-3.4477l-0.003281-0.82266 1.2188-0.48192c0.67031-0.26506 2.0905-0.91814 3.156-1.4513 1.8818-0.9416 1.9444-0.96296 2.1875-0.74598 0.13765 0.12286 1.7289 1.4977 3.5361 3.0552 2.6386 2.274 3.3566 2.8318 3.6453 2.8318 0.36133 0 2.0861-1.1515 4.0689-2.7164 1.096-0.86503 1.3125-1.1102 1.3125-1.4859 0-0.16481-0.6651-1.6351-1.478-3.2674-0.8129-1.6323-1.7203-3.484-2.0164-4.1149l-0.53842-1.1472 1.3025-1.4153c0.98458-1.0699 3.0428-3.5317 3.3081-3.9567 0.01421-0.02277 1.7885 0.49267 3.9428 1.1454 5.3645 1.6254 5.1324 1.5634 5.4305 1.4526 0.27709-0.10299 1.2475-1.6853 2.4777-4.0403 0.50702-0.97053 0.69893-1.4688 0.67174-1.744-0.0332-0.33618-0.49246-0.76533-3.6006-3.3645-1.9594-1.6386-3.549-3.0194-3.5326-3.0685 0.01645-0.0491 0.33422-0.98927 0.70614-2.0893 0.37192-1.1 0.83026-2.6337 1.0185-3.4082 0.28872-1.1877 0.38364-1.4171 0.60636-1.4651 0.14523-0.03128 2.1484-0.28664 4.4516-0.56748 2.3031-0.28083 4.3676-0.56722 4.5878-0.63642 0.22015-0.0692 0.43116-0.22312 0.46891-0.34204 0.16121-0.50793 0.32407-2.2276 0.39982-4.2218l0.08132-2.141-0.30016-0.18592c-0.16509-0.10226-2.2467-0.73243-4.6258-1.4004l-4.3256-1.2145-0.08128-1.2403c-0.09491-1.4482-0.38104-3.6412-0.65624-5.0295-0.10657-0.53762-0.16637-1.0489-0.13288-1.1362 0.03349-0.08727 1.8151-1.2182 3.9591-2.5133 2.144-1.295 3.986-2.4887 4.0934-2.6525 0.1825-0.27853 0.16507-0.38881-0.26825-1.6967-0.25489-0.76935-0.73238-2.0738-1.0611-2.8988-0.48486-1.2169-0.65657-1.5209-0.9099-1.6105-0.21622-0.07653-1.5777 0.06916-4.4269 0.47373-2.2631 0.32134-4.2886 0.61474-4.5012 0.652-0.37983 0.06656-0.39948 0.04417-1.125-1.2818-0.40613-0.74224-1.2306-2.0998-1.8322-3.0167-0.60156-0.91696-1.0938-1.6924-1.0938-1.7232 0-0.0308 13.106-0.056 29.125-0.056h29.125v19.563c0 10.759-0.0205 19.562-0.0455 19.562s-0.57346-0.1966-1.2188-0.43689c-1.9873-0.74003-1.5791-1.0475-4.5736 3.4448-2.2338 3.3511-2.6233 3.8731-2.844 3.811-0.92212-0.25946-4.162-0.84958-5.6307-1.0256-0.9625-0.11535-1.7652-0.22029-1.7838-0.2332-0.0186-0.01291-0.48487-1.9583-1.0362-4.323-1.0911-4.6801-1.1701-4.9499-1.4747-5.0383-0.64388-0.18672-1.5951-0.20827-3.4143-0.07737-2.4149 0.17377-2.9477 0.2882-3.1016 0.66616-0.0616 0.15122-0.42579 2.1312-0.80932 4.3999-0.38353 2.2688-0.72483 4.2491-0.75846 4.4008-0.04536 0.20459-0.18186 0.29573-0.52888 0.35308-1.0104 0.16698-4.5342 1.0633-5.7253 1.4563l-1.2575 0.4149-2.4925-3.2932c-3.0675-4.053-3.2501-4.2693-3.6043-4.2693-0.31738 0-4.8352 2.2124-5.3587 2.6241-0.2064 0.16235-0.34204 0.39047-0.34204 0.57523 0 0.1684 0.47812 2.2162 1.0625 4.5507 0.58438 2.3345 1.0625 4.2943 1.0625 4.3551 0 0.06083-0.60469 0.55377-1.3438 1.0954-1.3308 0.9753-3.6227 2.8876-4.0819 3.4058-0.13097 0.14779-0.31198 0.26871-0.40226 0.26871-0.09028 0-1.9516-0.98438-4.1363-2.1875-2.1847-1.2031-4.1018-2.1875-4.2604-2.1875-0.32785 0-0.7002 0.37023-2.2 2.1875-1.584 1.9192-2.076 2.6203-2.0694 2.9489 4e-3 0.19844 0.98149 1.5374 2.8662 3.9261l2.8602 3.625-0.32968 0.5625c-0.92969 1.5862-1.7134 3.0815-2.293 4.375-0.3543 0.79062-0.68579 1.4841-0.73666 1.5409-0.05086 0.0569-2.1521-0.07188-4.6693-0.28617-3.3422-0.28452-4.6435-0.35391-4.8241-0.25726-0.43253 0.23148-2.0067 5.7291-1.8356 6.4107 0.06835 0.27233 0.70375 0.64914 4.1746 2.4756 2.2517 1.1849 4.1142 2.1708 4.139 2.1908 0.02479 0.01999-0.04765 0.81293-0.16099 1.7621-0.11334 0.94917-0.23133 2.5691-0.26221 3.5999l-0.05614 1.8741-4.3454 1.51c-3.7225 1.2936-4.3659 1.5535-4.4888 1.8134-0.15313 0.32397 4e-3 2.0758 0.4029 4.4909 0.27757 1.6807 0.40381 2.1033 0.671 2.2463 0.12898 0.069 2.3011 0.26591 4.827 0.43752 2.5259 0.17162 4.5994 0.32703 4.6079 0.34537 0.0085 0.0183 0.28919 0.8771 0.62385 1.9084 0.33466 1.0312 0.873 2.501 1.1963 3.266l0.58782 1.391-3.3542 3.145c-1.9382 1.8173-3.3855 3.2697-3.4284 3.4404-0.05338 0.21269 0.08627 0.57349 0.49882 1.2887 0.31513 0.54634 0.57296 1.03 0.57296 1.0748s-11.278 0.0815-25.062 0.0815h-25.062z" fill="#f08080" fill-rule="evenodd" stroke="#800000" stroke-width=".35"/>
 </g>
</svg>
"""


class ArtProvider(wx.ArtProvider):
    def CreateBitmap(self, id_art, client, size):
        if size == wx.DefaultSize:
            size = wx.Size(32, 32)
        if id_art == 'ICON':
            return self._process_svg(svgicon, size)
        if id_art == "ICON_DETAILS":
            return self._process_svg(svgicon_details, size)
        if id_art == "ICON_PREVIEW":
            return self._process_svg(svgicon_preview, size)
        return wx.NullBitmap

    @staticmethod
    def _process_svg(svgstring, size):
        svg = wx.svg.SVGimage.CreateFromBytes(svgstring)
        return svg.ConvertToScaledBitmap(size)


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

        self.SetIcon(wx.ArtProvider.GetIcon('ICON'))
        self.SetSizeHints(800, 400)
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
        init_bigbagxml()
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
