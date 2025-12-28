from cx_Freeze import setup, Executable

executables = [
    Executable('src/pycestorieseditor/__main__.py', base="gui", target_name='pce')
]
buildexe = {
    'excludes': [
        "tkinter", "gi", "gtk", "PyQt4", "PyQt5", "PyQt6",
        "PySide2", "PySide6", "shiboken2", "shiboken6", "lib2to3"
    ],
    'packages': ["xsdata_attrs.hooks"],
    'include_msvcr': True
}

setup(
    name="CE Stories Viz",
    executables=executables,
    options={
        "build_exe": buildexe
    }
)
