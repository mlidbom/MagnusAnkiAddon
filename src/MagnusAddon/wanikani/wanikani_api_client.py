from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wanikani_api.client import Client

if TYPE_CHECKING:
    from wanikani_api import models

class WanikaniClient:
    _instance = None

    @classmethod
    def get_instance(cls) -> WanikaniClient:
        if not cls._instance:
            cls._instance = WanikaniClient()
        return cls._instance

    def __init__(self) -> None:
        self._is_initialized = False
        v2_api_key = "ebeda84c-2f6a-423e-bfc7-3068796ed50a"
        self._client = Client(v2_api_key)

    # noinspection PyTypeChecker
    def _init(self) -> WanikaniClient:
        if self._is_initialized is False:
            from sysutils import progress_display_runner
            progress = progress_display_runner.open_spinning_progress_dialog("Fetching Wanikani data")
            try:
                client = self._client

                self._radical_list: list[models.Radical] = list(client.subjects(types="radical", fetch_all=True))
                self._kanji_list: list[models.Kanji] = list(client.subjects(types="kanji", fetch_all=True))
                self._vocab_list: list[models.Vocabulary] = list(client.subjects(types="vocabulary", fetch_all=True))

                self._radical_list = [radical for radical in self._radical_list if radical.hidden_at is None]
                self._kanji_list = [kanji for kanji in self._kanji_list if kanji.hidden_at is None]
                self._vocab_list = [vocab for vocab in self._vocab_list if vocab.hidden_at is None]

                self._radical_dictionary = {radical.slug: radical for radical in self._radical_list}
                self._kanji_dictionary = {kanji.characters: kanji for kanji in self._kanji_list}
                self._vocab_dictionary = {vocab.characters: vocab for vocab in self._vocab_list}

                self._radical_id_dictionary = {radical.id: radical for radical in self._radical_list}
                self._kanji_id_dictionary = {kanji.id: kanji for kanji in self._kanji_list}
                self._vocab_id_dictionary = {vocab.id: vocab for vocab in self._vocab_list}
            finally:
                # noinspection PyInconsistentReturns
                progress.close()


            self._is_initialized = True
        return self

    def list_radicals(self) -> list[models.Radical]:
        self._init()
        return self._radical_list

    def list_kanji(self) -> list[models.Kanji]:
        self._init()
        return self._kanji_list

    def list_vocabulary(self) -> list[models.Vocabulary]:
        self._init()
        return self._vocab_list

    _kana_vocab_list: list[models.Vocabulary] = list()
    _kana_vocab_dictionary: dict[Any, models.Vocabulary] = {}
    _kana_vocab_id_dictionary: dict[Any,models.Vocabulary] = {}
    # noinspection PyTypeChecker
    def list_kana_vocabulary(self) -> list[models.Vocabulary]:
        if not self._kana_vocab_list:
            from sysutils import progress_display_runner
            progress = progress_display_runner.open_spinning_progress_dialog("Fetching Wanikani data")
            try:
                client = self._client

                self._kana_vocab_list: list[models.Vocabulary] = list(client.subjects(types="kana_vocabulary", fetch_all=True))

                self._kana_vocab_list = [kana_vocab for kana_vocab in self._kana_vocab_list if kana_vocab.hidden_at is None]
                self._kana_vocab_dictionary = {vocab.characters: vocab for vocab in self._kana_vocab_list}
                self._kana_vocab_id_dictionary = {vocab.id: vocab for vocab in self._kana_vocab_list}
            finally:
                # noinspection PyInconsistentReturns
                progress.close()


        return self._kana_vocab_list

    def get_radical(self, radical_name: str) -> models.Radical:
        self._init()
        return self._radical_dictionary[radical_name.replace(" ", "-").lower()]

    def get_radical_by_id(self, radical_id: int) -> models.Radical:
        self._init()
        return self._radical_id_dictionary[radical_id]

    def get_kanji_by_name(self, kanji_name: str) -> models.Kanji:
        self._init()
        return self._kanji_dictionary[kanji_name]

    def get_kanji_by_id(self, kanji_id: int) -> models.Kanji:
        self._init()
        return self._kanji_id_dictionary[kanji_id]

    def get_vocab_by_id(self, vocab_id: int) -> models.Vocabulary:
        self._init()
        return self._vocab_id_dictionary[vocab_id]

    def get_vocab(self, vocab_name: str) -> models.Vocabulary:
        self._init()
        return self._vocab_dictionary[vocab_name]
