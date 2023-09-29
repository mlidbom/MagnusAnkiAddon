import os
from typing import List

import requests

from ankiutils.anki_shim import facade
from note.wanivocabnote import WaniVocabNote
from wanikani.jp_collection import JPCollection
from wanikani.wanikani_api_client import WanikaniClient


class FileDownloadError(Exception):
    pass


class WaniDownloader:
    @staticmethod
    def media_dir() -> str:
        return facade.col().media.dir()

    @classmethod
    def download_file(cls, url, filename) -> str:
        response = requests.get(url)

        if response.status_code == 200:
            file_path = os.path.join(cls.media_dir(), filename)
            with open(file_path, 'wb') as file:
                file.write(response.content)

            return filename
        else:
            raise FileDownloadError("{} -> {}".format(url, cls.media_dir()))

    @classmethod
    def fetch_audio_from_wanikani(cls, vocab: WaniVocabNote) -> None:
        wani_client: WanikaniClient = WanikaniClient.get_instance()
        wani_vocab = wani_client.get_vocab(vocab.get_question())
        female_audio_mp3 = [audio for audio in wani_vocab.pronunciation_audios if audio.metadata.gender == "female" and audio.content_type == "audio/mpeg"]
        male_audio_mp3 = [audio for audio in wani_vocab.pronunciation_audios if audio.metadata.gender == "male" and audio.content_type == "audio/mpeg"]

        female_audios = [cls.download_file(value.url, f"Wani_{wani_vocab.id}_{value.metadata.pronunciation}_female.mp3") for value in female_audio_mp3]
        vocab.set_audio_female(female_audios[::-1])

        male_audios = [cls.download_file(value.url, f"Wani_{wani_vocab.id}_{value.metadata.pronunciation}_male.mp3") for value in male_audio_mp3]
        vocab.set_audio_male(male_audios[::-1])

    @classmethod
    def fetch_missing_vocab_audio(cls) -> None:
        vocab_missing_audio: List[WaniVocabNote] = [vocab for vocab in JPCollection.fetch_all_wani_vocab_notes() if
                                                    vocab.get_audio_female() == ""]
        for vocab in vocab_missing_audio:
            cls.fetch_audio_from_wanikani(vocab)
