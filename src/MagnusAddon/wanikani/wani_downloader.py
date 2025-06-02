from __future__ import annotations

import os
from typing import TYPE_CHECKING

import requests  # type: ignore
from ankiutils import app
from autoslot import Slots
from wanikani.wanikani_api_client import WanikaniClient

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

class FileDownloadError(Exception):
    pass

class WaniDownloader(Slots):
    @staticmethod
    def media_dir() -> str:
        return app.anki_collection().media.dir()

    @classmethod
    def download_file(cls, url: str, filename: str) -> str:
        response = requests.get(url)

        if response.status_code == 200:
            file_path = os.path.join(cls.media_dir(), filename)
            with open(file_path, "wb") as file:
                file.write(response.content)

            return filename
        raise FileDownloadError(f"{url} -> {cls.media_dir()}")

    @classmethod
    def fetch_audio_from_wanikani(cls, vocab: VocabNote) -> None:
        wani_client: WanikaniClient = WanikaniClient.get_instance()
        wani_vocab = wani_client.get_vocab(vocab.get_question())
        female_audio_mp3 = [audio for audio in wani_vocab.pronunciation_audios if audio.metadata.gender == "female" and audio.content_type == "audio/mpeg"]
        male_audio_mp3 = [audio for audio in wani_vocab.pronunciation_audios if audio.metadata.gender == "male" and audio.content_type == "audio/mpeg"]

        female_audios = [cls.download_file(value.url, f"Wani_{wani_vocab.id}_{value.metadata.pronunciation}_female.mp3") for value in female_audio_mp3]
        vocab.audio.second.set_multiple(female_audios[::-1])

        male_audios = [cls.download_file(value.url, f"Wani_{wani_vocab.id}_{value.metadata.pronunciation}_male.mp3") for value in male_audio_mp3]
        value1 = male_audios[::-1]
        vocab.audio.first.set_multiple(value1)

    @classmethod
    def fetch_missing_vocab_audio(cls) -> None:
        vocab_missing_audio: list[VocabNote] = [vocab for vocab in app.col().vocab.all_wani() if
                                                vocab.audio.second.raw_walue() == ""]
        for vocab in vocab_missing_audio:
            cls.fetch_audio_from_wanikani(vocab)
