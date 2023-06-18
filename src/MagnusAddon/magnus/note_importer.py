import aqt.editor
from aqt import gui_hooks, mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *

from .wanikani_note import *
from .wanikani_api_client import WanikaniClient
from .wani_collection import WaniCollection

waniClient = WanikaniClient()


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


action = QAction("Import Missing Radicals", mw)
qconnect(action.triggered, import_missing_radicals)
mw.form.menuTools.addAction(action)

action = QAction("Import Missing Kanji", mw)
qconnect(action.triggered, import_missing_kanji)
mw.form.menuTools.addAction(action)

action = QAction("Import Missing Vocabulary", mw)
qconnect(action.triggered, import_missing_vocab)
mw.form.menuTools.addAction(action)
