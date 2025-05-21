from __future__ import annotations

import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import _lib_patched # noqa NOTE: this line sets up lib paths, lib imports before here do not work when running in anki
import _lib # noqa NOTE: this line sets up lib paths, lib imports before here do not work when running in anki

import ui # noqa
from ankiutils import app # noqa
if app.config().enable_automatic_garbage_collection.get_value():
    import gc
    gc.enable()

ui.timing_hacks.init()
ui.browser_right_click_menu.init()
ui.editor_buttons.init()
ui.tools_menu.init()
ui.menus.right_click_menu.init()

ui.note_content_building.ud_sentence_breakdown.init() #needs to be before vocab_and_sentence_kanji_list
ui.note_content_building.vocab_and_sentence_kanji_list.init()
ui.note_content_building.kanji_vocab_list.init()
ui.note_content_building.vocab_highlighted_sentence_list.init()

ui.copy_sort_field_to_clipboard.init()
ui.note_content_building.kanji_radical_and_kanji_dependencies_list.init()
ui.note_content_building.kanji_mnemonic.init()
ui.note_content_building.kanji_katakana_onyomi.init()
ui.note_content_building.vocab_related_vocabs.init()
ui.note_content_building.vocab_context_sentences.init()
ui.note_content_building.radical_and_kanji_kanji_kanji_list.init()
ui.clear_studying_cache_on_card_suspend_unsuspend.init()
ui.custom_auto_advance_timings.init()
ui.history_navigator.init()
ui.custom_shortcuts.init()
#hooks.auto_bury_multiple_failures.init()
