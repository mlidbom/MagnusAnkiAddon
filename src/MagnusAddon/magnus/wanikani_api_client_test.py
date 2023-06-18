from typing import List, Optional

from wanikani_api.client import Client, models


class WanikaniClient:
    def __init__(self):
        self.isInitialized = False

    def _init(self):
        if self.isInitialized is False:
            self.v2_api_key = "ebeda84c-2f6a-423e-bfc7-3068796ed50a"
            client = Client(self.v2_api_key)

            self._radical_list: List[models.Radical] = list(client.subjects(types="radical", fetch_all=True))
            self._kanji_list: List[models.Kanji] = list(client.subjects(types="kanji", fetch_all=True))
            self._vocab_list: List[models.Vocabulary] = list(client.subjects(types="vocabulary", fetch_all=True))

            self._radical_dictionary = {radical.characters: radical for radical in self._radical_list}
            self._kanji_dictionary = {kanji.characters: kanji for kanji in self._kanji_list}
            self._vocab_dictionary = {vocab.characters: vocab for vocab in self._vocab_list}
            self.isInitialized = True
            return self

    def list_radicals(self) -> List[models.Radical]:
        self._init()
        return self._radical_list

    def list_kanji(self) -> List[models.Kanji]:
        self._init()
        return self._kanji_list

    def list_vocabulary(self) -> List[models.Vocabulary]:
        self._init()
        return self._vocab_list

    def get_radical(self, radical_name: str) -> models.Radical:
        self._init()
        return self._radical_dictionary[radical_name]

    def get_kanji(self, kanji_name: str) -> models.Kanji:
        self._init()
        return self._kanji_dictionary[kanji_name]

    def get_vocab(self, vocab_name: str) -> models.Vocabulary:
        self._init()
        return self._vocab_dictionary[vocab_name]
