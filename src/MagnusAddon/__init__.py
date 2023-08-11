import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from hooks import  wani_menu_manager, hooks_suppress_audio_on_typing, collection_search
from _addon_copies import refresh_media_references

wani_menu_manager.setup()
hooks_suppress_audio_on_typing.setup()
collection_search.init()
