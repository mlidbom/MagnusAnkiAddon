import aqt.editor
from aqt import gui_hooks, mw
from aqt.utils import showInfo, qconnect
from aqt.qt import *

from .wanikani_note import *
from .wanikani_api_client_test import WanikaniClient
from .wani_collection import WaniCollection

waniClient = WanikaniClient()


def get_wani_vocab(vocab_note: WaniVocabNote):
    remote_vocab = waniClient.get_vocab(vocab_note.get_vocab())
    vocab_note.update_from_wani(remote_vocab)


def setup_buttons(buttons, the_editor: aqt.editor.Editor):
    btn = the_editor.addButton("", "Update from wanikani",
                               lambda local_editor: get_wani_vocab(WaniVocabNote(local_editor.note)))
    buttons.append(btn)


gui_hooks.editor_did_init_buttons.append(setup_buttons)


def update_radical() -> None:
    all_radicals: list[WaniRadicalNote] = WaniCollection.fetch_all_radical_notes()
    fetched = 0
    failed: str = ""
    for radical_note in all_radicals:
        try:
            wani_radical = waniClient.get_radical(radical_note.get_radical_name())
            radical_note.update_from_wani(wani_radical)
            fetched = fetched + 1
        except KeyError:
            failed = failed + "," + radical_note.get_radical_name()

    message = "Successfully matched {} radical notes.\n Failed:{}".format(fetched, failed)
    print(message)
    showInfo(message)

def update_kanji() -> None:
    all_kanji: list[WaniKanjiNote] = WaniCollection.fetch_all_kanji_notes()
    fetched = 0
    failed: str = ""
    for kanji_note in all_kanji:
        try:
            wani_kanji = waniClient.get_kanji(kanji_note.get_kanji())
            kanji_note.update_from_wani(wani_kanji)
            fetched = fetched + 1
        except KeyError:
            failed = failed + "," + kanji_note.get_kanji()

    message = "Successfully matched {} kanji notes.\n Failed:{}".format(fetched, failed)
    print(message)
    showInfo(message)

def update_vocab() -> None:
    all_vocabulary: list[WaniVocabNote] = WaniCollection.fetch_all_vocab_notes()
    updated = 0
    failed: str = ""
    for vocab_note in all_vocabulary:
        try:
            wani_vocab = waniClient.get_vocab(vocab_note.get_vocab())
            vocab_note.update_from_wani(wani_vocab)
            updated = updated + 1
        except KeyError:
            failed = failed + "," + vocab_note.get_vocab()

    message = "Successfully matched {} vocab notes.\n Failed:{}".format(updated, failed)
    print(message)
    showInfo(message)


action = QAction("Update Radicals", mw)
qconnect(action.triggered, update_radical)
mw.form.menuTools.addAction(action)

action = QAction("Update Kanji", mw)
qconnect(action.triggered, update_kanji)
mw.form.menuTools.addAction(action)

action = QAction("Update Vocabulary", mw)
qconnect(action.triggered, update_vocab)
mw.form.menuTools.addAction(action)
