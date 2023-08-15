#!/usr/bin/env python3
# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html


import os
import sys

sys.path.append(f"c:\\Users\\magnu\\PycharmProjects\\MagnusAnkiAddon\\venv\\Lib\\site-packages\\")
sys.path.append(f"c:\\Users\\magnu\\PycharmProjects\\MagnusAnkiAddon\\venv\\Lib\\site-packages\\win32\\lib\\")
sys.path.append(f"c:\\Users\\magnu\\PycharmProjects\\MagnusAnkiAddon\\venv\\Lib\\site-packages\\win32\\")
sys.path.append("c:\\Users\\magnu\\PycharmProjects\\MagnusAnkiAddon\\src\\MagnusAddon\\")

import aqt

if not os.environ.get("ANKI_IMPORT_ONLY"):
    aqt.run()
