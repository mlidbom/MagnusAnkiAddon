import sys
import os

import hooks.tools_menu

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hooks import hooks_suppress_audio_on_typing, right_click_menu, copy_card_sort_field_to_clipboard
from _addon_copies import refresh_media_references # noqa

hooks.tools_menu.setup()

copy_card_sort_field_to_clipboard.setup()
hooks_suppress_audio_on_typing.setup()
right_click_menu.init()
