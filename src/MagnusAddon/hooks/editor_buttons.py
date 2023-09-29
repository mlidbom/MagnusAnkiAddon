from aqt import gui_hooks
from aqt.editor import Editor

from note.vocabnote import VocabNote
from wanikani import wani_note_updater
from wanikani.wani_downloader import WaniDownloader


def setup_editor_buttons(buttons, the_editor: Editor):
    buttons.append(the_editor.addButton("", "Unsuspend with dependencies",
                                            lambda local_editor: wani_queue_manager.unsuspend_with_dependencies(
                                                local_editor.note)))

    buttons.append(the_editor.addButton("", "prioritize with dependencies",
                                            lambda local_editor: wani_queue_manager.prioritize_with_dependencies(
                                                local_editor.note)))

    buttons.append(the_editor.addButton("", "answer again with zero interval with dependencies",
                                            lambda local_editor: wani_queue_manager.answer_again_with_zero_interval_for_new_note_cards_with_dependencies(
                                                local_editor.note)))

    buttons.append(the_editor.addButton("", "Update from wanikani",
                                        lambda local_editor: wani_note_updater.update_from_wanikani(
                                             local_editor.note)))

    buttons.append(the_editor.addButton("", "Fetch audio from wanikani",
                                        lambda local_editor: WaniDownloader.fetch_audio_from_wanikani(
                                            VocabNote(local_editor.note))))


def init() -> None:
    gui_hooks.editor_did_init_buttons.append(setup_editor_buttons)
