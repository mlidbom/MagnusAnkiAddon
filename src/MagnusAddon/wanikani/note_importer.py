from aqt.utils import showInfo

from note.wanikanjinote import WaniKanjiNote
from note.waniradicalnote import WaniRadicalNote
from note.wanivocabnote import WaniVocabNote
from wanikani.wani_collection import WaniCollection
from wanikani.wanikani_api_client import WanikaniClient

waniClient = WanikaniClient.get_instance()


def import_missing_radicals() -> None:
    all_radicals: list[WaniRadicalNote] = WaniCollection.fetch_all_radical_notes()
    local_radicals_dictionary = {radical.get_subject_id(): radical for radical in all_radicals}
    all_wani_radicals = waniClient.list_radicals()
    imported = 0
    for wani_radical in all_wani_radicals:
        if wani_radical.id not in local_radicals_dictionary:
            print("Importing: {}".format(wani_radical.slug))
            WaniRadicalNote.create_from_wani_radical(wani_radical)
            imported = imported + 1

    showInfo("Imported {} radical notes".format(imported))


def import_missing_kanji() -> None:
    all_kanji: list[WaniKanjiNote] = WaniCollection.fetch_all_wani_kanji_notes()
    local_kanji_dictionary = {kanji.get_subject_id(): kanji for kanji in all_kanji}
    all_wani_kanji = waniClient.list_kanji()
    imported = 0
    for wani_kanji in all_wani_kanji:
        if wani_kanji.id not in local_kanji_dictionary:
            print("Importing: {}".format(wani_kanji.slug))
            WaniKanjiNote.create_from_wani_kanji(wani_kanji)
            imported = imported + 1

    showInfo("Imported {} kanji notes".format(imported))


def import_missing_vocab() -> None:
    all_vocabulary: list[WaniVocabNote] = WaniCollection.fetch_all_wani_vocab_notes()
    local_vocabulary_dictionary = {vocab.get_vocab(): vocab for vocab in all_vocabulary}
    all_wani_vocabulary = waniClient.list_vocabulary()
    imported = 0
    for wani_vocab in all_wani_vocabulary:
        if wani_vocab.characters not in local_vocabulary_dictionary:
            print("Importing: {}".format(wani_vocab.slug))
            WaniVocabNote.create_from_wani_vocabulary(wani_vocab)
            imported = imported + 1

    showInfo("Imported {} vocabulary notes".format(imported))

