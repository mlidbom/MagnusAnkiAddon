from aqt import mw
from aqt.sound import av_player
from os.path import dirname
from aqt.reviewer import Reviewer
from anki import hooks
from typing import Callable

addon_path: str = dirname(__file__)
sound_file: str = addon_path + "/timebox_complete.mp3"

def on_timebox(self: Reviewer, _old: Callable[[Reviewer], bool]) -> bool:
    if mw.col.timeboxReached():
        av_player.play_file(sound_file)

    return _old(self)

Reviewer.check_timebox = hooks.wrap(Reviewer.check_timebox, on_timebox, "around")  # type: ignore