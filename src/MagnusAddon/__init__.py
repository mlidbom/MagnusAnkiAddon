import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import hooks
from _addon_copies import refresh_media_references # noqa

hooks.editor_buttons.setup()
hooks.tools_menu.setup()
hooks.suppress_audio_on_typing.setup()
hooks.copy_card_sort_field_to_clipboard.setup()
hooks.suppress_audio_on_typing.setup()
hooks.right_click_menu.init()
hooks.show_previewer.init()
