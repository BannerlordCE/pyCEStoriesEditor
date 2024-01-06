import sys
from cx_Freeze import setup, Executable

base = 'Win32GUI' if sys.platform == 'win32' else None

executables = [
    Executable('src/pycestorieseditor/__main__.py', base=base, target_name='pce')
]
buildexe = {
    'excludes': [
        "tkinter", "gi", "gtk", "PyQt4", "PyQt5", "PyQt6",
        "PySide2", "PySide6", "shiboken2", "shiboken6", "lib2to3"
    ],
    'packages': ["xsdata_attrs.hooks"],
    'include_msvcr': False
}

setup(
    executables=executables,
    options={
        "build_exe": buildexe
    }
)
