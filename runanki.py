#!/usr/bin/env python3
# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os
from typing import cast

import aqt


anki_config_dir = os.path.join(cast(str, os.getenv('APPDATA')), 'Anki2')
anki_config_file = os.path.join(anki_config_dir, 'gldriver6')
with open(anki_config_file, 'w') as f:
    f.write('d3d11')

try:
    if not os.environ.get("ANKI_IMPORT_ONLY"):
        aqt.run()
finally:
    with open(anki_config_file, 'w') as f:
        f.write('auto')
