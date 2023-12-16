# pyCEStoriesEditor

Simple project to visualize event nodes for stories created for Captivity Events.

Requires python 3.11 and [poetry](https://python-poetry.org/docs/).

To install and launch:

```
~$ poetry install
~$ poetry run python -m pycestorieseditor
```

The first launch will invite you to create a configuration file. You'll have to
save and launch the software again, until I figure out how to automate that
process.

## Build for windows

It is relatively simple to create an executable for the Windows system, thanks
to [cxFreeze](https://cx-freeze.readthedocs.io/en/stable/). The following
commands will generate the necessary files under the `build` folder. You'll
find a `pce.exe` executable amongst the subfolders.

```
~$ poetry install --with=dev
~$ poetry run python setup.py build 
```
