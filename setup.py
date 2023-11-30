import sys
from cx_Freeze import setup, Executable

base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('src/pycestorieseditor/__main__.py', base=base, target_name = 'pce')
]

setup(executables = executables)
