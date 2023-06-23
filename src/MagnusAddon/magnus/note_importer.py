from aqt.utils import showInfo

from .wani_collection import WaniCollection
from .wanikani_note import *

waniClient = WanikaniClient.get_instance()


def import_missing_radicals() -> None:
    showInfo("")


def import_missing_kanji() -> None:
    showInfo("message")


def import_missing_vocab() -> None:
    all_vocabulary: list[WaniVocabNote] = WaniCollection.fetch_all_vocab_notes()
    local_vocabulary_dictionary = {vocab.get_vocab(): vocab for vocab in all_vocabulary}
    all_wani_vocabulary = waniClient.list_vocabulary()
    imported = 0
    for wani_vocab in all_wani_vocabulary:
        if wani_vocab.characters not in local_vocabulary_dictionary:
            print("Importing: {}".format(wani_vocab.slug))
            WaniVocabNote.create_from_wani_vocabulary(wani_vocab)
            imported = imported + 1

    showInfo("Imported {} vocabulary notes".format(imported))

def fetch_missing_audio() -> None:
    all_vocabulary: list[WaniVocabNote] = WaniCollection.fetch_all_vocab_notes()
    local_vocabulary_dictionary = {vocab.get_vocab(): vocab for vocab in all_vocabulary}
    all_wani_vocabulary = waniClient.list_vocabulary()
    imported = 0
    for wani_vocab in all_wani_vocabulary:
        if wani_vocab.characters not in local_vocabulary_dictionary:
            print("Importing: {}".format(wani_vocab.slug))
            WaniVocabNote.create_from_wani_vocabulary(wani_vocab)
            imported = imported + 1

    showInfo("Imported {} vocabulary notes".format(imported))

