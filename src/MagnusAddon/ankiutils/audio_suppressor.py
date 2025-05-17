from __future__ import annotations

import threading
from typing import TYPE_CHECKING

from aqt.sound import av_player
from autoslot import Slots

if TYPE_CHECKING:
    from anki.sound import AVTag


class AudioSuppressor(Slots):
    def __init__(self) -> None:
        self._av_player_play_tags_method = av_player.play_tags

    def restore_play_tags_method(self) -> None:
        av_player.play_tags = self._av_player_play_tags_method

    def suppress_for_seconds(self, time: float) -> None:
        def null_op(_tags: list[AVTag]) -> None:
            pass

        av_player.play_tags = null_op
        threading.Timer(time, self.restore_play_tags_method).start()

audio_suppressor: AudioSuppressor = AudioSuppressor()