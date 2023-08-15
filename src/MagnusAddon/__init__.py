import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import _lib # noqa
import hooks
from _addon_copies import refresh_media_references # noqa

hooks.editor_buttons.init()
hooks.tools_menu.init()
hooks.suppress_audio_on_typing.init()
hooks.copy_card_sort_field_to_clipboard.init()
hooks.suppress_audio_on_typing.init()
hooks.right_click_menu.init()
hooks.show_previewer.init()
