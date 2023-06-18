import aqt.editor
from aqt import gui_hooks


from .wanikani_note import *
from .wanikani_api_client_test import WanikaniClient

waniClient = WanikaniClient()

def get_wani_vocab(vocab_note: WaniVocabNote):
    remote_vocab = waniClient.get_vocab(vocab_note.get_vocab())
    remote_meaning = remote_vocab.meaning_mnemonic
    # vocab_note.set_meaning_exp(remote_meaning)

def setup_buttons(buttons, the_editor: aqt.editor.Editor):
    btn = the_editor.addButton("", "Update from wanikani",
                               lambda local_editor: get_wani_vocab(WaniVocabNote(local_editor.note)))
    buttons.append(btn)


gui_hooks.editor_did_init_buttons.append(setup_buttons)
