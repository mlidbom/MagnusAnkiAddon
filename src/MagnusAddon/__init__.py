import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from magnus import wani_queue_manager, wani_note_updater, note_importer, wani_menu_manager, hooks_suppress_audio_on_typing
from wanikani_api import client, constants, models
from . import collection_search,  context_search, refresh_media_references