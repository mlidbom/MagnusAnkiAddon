from anki.sound import AVTag
from aqt.sound import av_player
import threading


class AudioSuppressor:
    def __init__(self) -> None:
        self._av_player_play_tags_method = av_player.play_tags

    def restore_play_tags_method(self) -> None:
        av_player.play_tags = self._av_player_play_tags_method  # type: ignore

    def suppress_for_seconds(self, time: float) -> None:
        def null_op(_tags: list[AVTag]) -> None:
            pass

        av_player.play_tags = null_op  # type: ignore
        threading.Timer(time, self.restore_play_tags_method).start()

audio_suppressor: AudioSuppressor = AudioSuppressor()