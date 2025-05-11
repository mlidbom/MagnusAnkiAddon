"""
Anki Add-on: Refresh Media References

Adds an entry in the Tools menu that clears the webview cache.
This will effectively refresh all media files used by your cards
and templates, allowing you to display changes to external files
without having to restart Anki.

The add-on will also update the modification time of your media
collection which will force an upload of any updated files
on the next synchronization with AnkiWeb.

Note: Might lead to increased memory consumption if used excessively

Copyright: (c) Glutanimate 2017 <https://glutanimate.com/>
License: GNU AGPLv3 or later <https://www.gnu.org/licenses/agpl.html>
"""

import os

from ankiutils import app
from aqt import mw, qconnect
from aqt.utils import tooltip
from PyQt6.QtGui import QAction, QKeySequence


def refresh_media() -> None:
    # write a dummy file to update collection.media modtime and force sync
    media_dir = app.anki_collection().media.dir()
    fpath = os.path.join(media_dir, "syncdummy.txt")
    if not os.path.isfile(fpath):
        with open(fpath, "w") as f:
            f.write("anki sync dummy")
    os.remove(fpath)
    # reset Anki
    app.main_window().reset()
    tooltip("Media References Updated")


# Set up menus and hooks
refresh_media_action = QAction("Refresh &Media", mw)
refresh_media_action.setShortcut(QKeySequence("Ctrl+Alt+M"))
qconnect(refresh_media_action.triggered, refresh_media)
app.main_window().form.menuTools.addAction(refresh_media_action)
