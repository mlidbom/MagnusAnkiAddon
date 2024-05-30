import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import _lib_patched # noqa NOTE: this line sets up lib paths, lib imports before here do not work when running in anki
import _lib # noqa NOTE: this line sets up lib paths, lib imports before here do not work when running in anki

import hooks # noqa

from _addon_copies import refresh_media_references # noqa

hooks.timing_hacks.init()
hooks.browser_right_click_menu.init()
hooks.editor_buttons.init()
hooks.tools_menu.init()
hooks.show_dependencies_in_browser.init()
hooks.right_click_menu.init()
hooks.note_content_building.ud_sentence_breakdown.init() #needs to be before vocab_and_sentence_kanji_list
hooks.note_content_building.vocab_and_sentence_kanji_list.init()
hooks.note_content_building.kanji_vocab_list.init()
hooks.copy_sort_field_to_clipboard.init()
hooks.note_content_building.kanji_radical_and_kanji_dependencies_list.init()
hooks.note_content_building.kanji_katakana_onyomi.init()
hooks.note_content_building.vocab_compounds_and_kanji_names.init()
hooks.note_content_building.vocab_homophones_list.init()
