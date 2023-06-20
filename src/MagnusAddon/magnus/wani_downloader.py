import os
from typing import List

import requests
from aqt import mw

from magnus import wanikani_api_client
from magnus.wani_collection import WaniCollection
from magnus.wanikani_api_client import WanikaniClient
from magnus.wanikani_note import *


class FileDownloadError(Exception):
    pass


class WaniDownloader:
    def media_dir() -> str:
        return mw.col.media.dir()

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
        wani_vocab = wani_client.get_vocab(vocab.get_vocab())
        female_audio_mp3 = [audio for audio in wani_vocab.pronunciation_audios if
                            audio.metadata.gender == "female" and audio.content_type == "audio/mpeg"]
        male_audio_mp3 = [audio for audio in wani_vocab.pronunciation_audios if
                            audio.metadata.gender == "male" and audio.content_type == "audio/mpeg"]

        if len(female_audio_mp3) > 0:
            vocab.set_audio_female(cls.download_file(female_audio_mp3[0].url, "Wani_{}_female.mp3".format(wani_vocab.id)))

        if len(male_audio_mp3) > 0:
            vocab.set_audio_male(cls.download_file(male_audio_mp3[0].url, "Wani_{}_male.mp3".format(wani_vocab.id)))

    @classmethod
    def fetch_missing_vocab_audio(cls):
        vocab_missing_audio: List[WaniVocabNote] = [vocab for vocab in WaniCollection.fetch_all_vocab_notes() if vocab.get_audio_female() == ""]
        for vocab in vocab_missing_audio:
            cls.fetch_audio_from_wanikani(vocab)


