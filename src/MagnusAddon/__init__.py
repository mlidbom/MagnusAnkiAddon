from __future__ import annotations

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import _lib # noqa NOTE: this line sets up lib paths, lib imports before here do not work when running in anki  # pyright: ignore[reportUnusedImport]

from jaslib import app # noqa
if app.config().enable_automatic_garbage_collection.get_value():
    import gc
    gc.enable()
