from typing import List, Optional

from wanikani_api.client import Client, models

v2_api_key = "ebeda84c-2f6a-423e-bfc7-3068796ed50a"
client = Client(v2_api_key)

_all_vocabulary: Optional[List[models.Vocabulary]] = None
_all_radicals: Optional[List[models.Radical]] = None
_all_kanji: Optional[List[models.Kanji]] = None


def fetch_radicals() -> List[models.Radical]:
    global _all_radicals
    if _all_radicals is None:
        _all_radicals = list(client.subjects(types="radical", fetch_all=True))
    return _all_radicals


def fetch_kanji() -> List[models.Kanji]:
    global _all_kanji
    if _all_kanji is None:
        _all_kanji = list(client.subjects(types="kanji", fetch_all=True))
    return _all_kanji


def fetch_vocabulary() -> List[models.Vocabulary]:
    global _all_vocabulary
    if _all_vocabulary is None:
        _all_vocabulary = list(client.subjects(types="vocabulary", fetch_all=True))
    return _all_vocabulary
