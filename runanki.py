#!/usr/bin/env python3
# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
from __future__ import annotations

import os
import sys
from typing import cast

import aqt


def is_pycharm_debugger() -> bool:
    return "pydevd" in sys.modules


anki_config_dir = os.path.join(cast(str, os.getenv('APPDATA')), 'Anki2')
anki_config_file = os.path.join(anki_config_dir, 'gldriver6')

with open(anki_config_file, 'w') as f:
    f.write('d3d11' if is_pycharm_debugger() else 'auto')

try:
    if not os.environ.get("ANKI_IMPORT_ONLY"):
        aqt.run()
finally:
    with open(anki_config_file, 'w') as f:
        f.write('auto')
