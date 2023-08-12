import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hooks import wani_menu_manager, hooks_suppress_audio_on_typing, right_click_menu
from _addon_copies import refresh_media_references # noqa

wani_menu_manager.setup()
hooks_suppress_audio_on_typing.setup()
right_click_menu.init()
