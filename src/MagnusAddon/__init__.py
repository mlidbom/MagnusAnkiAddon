import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import _lib # noqa
import hooks
from _addon_copies import refresh_media_references # noqa

hooks.timing_hacks.init()
hooks.update_note_on_edit.init()
hooks.browser_right_click_menu.init()
hooks.editor_buttons.init()
hooks.tools_menu.init()
hooks.show_dependencies_in_browser.init()
hooks.right_click_menu.init()
hooks.note_content_building.sentence_breakdown.init()#needs to be before vocab_and_sentence_kanji_list
hooks.note_content_building.vocab_and_sentence_kanji_list.init()
#hooks.show_previewer.init()
