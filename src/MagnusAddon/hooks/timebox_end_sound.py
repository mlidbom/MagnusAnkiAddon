from __future__ import annotations

from os.path import dirname

from aqt.reviewer import Reviewer
from aqt.sound import av_player
from aqt.utils import askUserDialog
from PyQt6.QtWidgets import QMessageBox
from sysutils import timeutil

addon_path: str = dirname(__file__)
sound_file: str = addon_path + "/timebox_complete.mp3"

def _check_timebox(self: Reviewer) -> bool:
    elapsed = self.mw.col.timeboxReached()
    if elapsed:
        av_player.play_file(sound_file)
        assert not isinstance(elapsed, bool)
        cards_studied = elapsed[1]
        seconds_studied = elapsed[0]
        seconds_per_card = float(seconds_studied) / cards_studied

        dialog = askUserDialog(f"""
Studied {cards_studied} cards in {timeutil.format_seconds_as_hh_mm_ss(seconds_studied)}.
{seconds_per_card:.2f} seconds per card.
""", ["OK"])
        dialog.setIcon(QMessageBox.Icon.Information)
        dialog.exec()
        self.mw.moveToState("deckBrowser")
        return True
    return False

Reviewer.check_timebox = _check_timebox  # type: ignore