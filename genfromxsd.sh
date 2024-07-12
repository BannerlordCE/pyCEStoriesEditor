#!/usr/bin/env bash

xsdata generate ./CEEventsModal.xsd
sed -i -e 's/import attr/from attrs import define, field, validators/g' \
    -e '/^from typing/a from xsdata.formats.dataclass.models.elements import XmlType' \
    -e 's/@attr\.s/@define/g' \
    -e 's/attr\.ib/field/g' ./generated/ceevents_modal.py

if command -v black > /dev/null; then
    black generated/ceevents_modal.py
fi

echo "Please merge ./generated/ceevents_modal.py with ./src/pycestorieseditor/ceevents_template/ceevents_modal.py"
echo "Be careful to not remove added code."
