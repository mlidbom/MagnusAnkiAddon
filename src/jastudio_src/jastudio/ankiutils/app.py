from __future__ import annotations  # noqa: I001

import os
from typing import TYPE_CHECKING

from jastudio import mylog
from jaspythonutils.sysutils.typed import checked_cast, non_optional
# noinspection PyUnusedImports, Annotator
import jastudio.mylog  # pyright: ignore [reportUnusedImport]  # noqa: F401
from jastudio.testutils import ex_pytest

# noinspection Annotator
from jastudio.dotnet import load_dotnet_runtime  # pyright: ignore [reportUnusedImport]  # noqa: F401

is_testing = ex_pytest.is_testing

if TYPE_CHECKING:
    from anki.collection import Collection
    from anki.dbproxy import DBProxy
    from anki.scheduler.v3 import Scheduler  # pyright: ignore[reportMissingTypeStubs]
    from aqt import AnkiQt  # type: ignore[attr-defined]  # pyright: ignore[reportPrivateImportUsage]
    from JAStudio.Core.Anki import AnkiLifecycleEvent
    from JAStudio.Core.Configuration import JapaneseConfig

    from jastudio.anki_extentions.config_manager_ex import ConfigManagerEx
    from jastudio.ankiutils.ui_utils_interface import IUIUtils
    from jastudio.note.collection.anki_collection_sync_runner import AnkiCollectionSyncRunner

_anki_collection: Collection | None = None
_sync_runner: AnkiCollectionSyncRunner | None = None
_initialized: bool = False

addon_name: str = "should_be_replaced_by_init"


def _notify_dotnet(event: AnkiLifecycleEvent) -> None:
    from jastudio.ui import dotnet_ui_root
    dotnet_ui_root.HandleAnkiLifecycleEvent(event)


def config() -> JapaneseConfig:
    from jastudio.ui import dotnet_ui_root
    return dotnet_ui_root.Services.ConfigurationStore.Config()


def is_initialized() -> bool:
    return _initialized


def _start_sync_bridges(col: Collection) -> None:
    """Create the sync runner and per-note-type bridges that forward real-time Anki edits to C#."""
    from JAStudio.Core.Note import NoteTypes, KanjiNote, SentenceNote, VocabNote
    from jastudio.note.collection.anki_collection_sync_runner import AnkiCollectionSyncRunner
    from jastudio.note.collection.anki_single_collection_syncer import AnkiSingleCollectionSyncer
    from jastudio.ui import dotnet_ui_root

    global _sync_runner
    _sync_runner = AnkiCollectionSyncRunner(col)
    collection = dotnet_ui_root.Services.App.Collection
    AnkiSingleCollectionSyncer(VocabNote, collection.Vocab.AnkiSyncHandler, _sync_runner, NoteTypes.Vocab)
    AnkiSingleCollectionSyncer(SentenceNote, collection.Sentences.AnkiSyncHandler, _sync_runner, NoteTypes.Sentence)
    AnkiSingleCollectionSyncer(KanjiNote, collection.Kanji.AnkiSyncHandler, _sync_runner, NoteTypes.Kanji)
    _sync_runner.start()


def _stop_sync_bridges() -> None:
    global _sync_runner
    if _sync_runner is not None:
        _sync_runner.destruct()
        _sync_runner = None


def flush_sync_updates() -> None:
    if _sync_runner is not None:
        _sync_runner.flush_updates()


def _profile_opened() -> None:
    mylog.info("profile_opened")
    from aqt import gui_hooks, mw
    from JAStudio.Core.Anki import AnkiLifecycleEvent

    global _anki_collection, _initialized

    _anki_collection = non_optional(mw.col)
    _start_sync_bridges(_anki_collection)
    _notify_dotnet(AnkiLifecycleEvent.ProfileOpened)
    _initialized = True

    gui_hooks.sync_will_start.append(_sync_will_start)
    gui_hooks.sync_did_finish.append(_sync_did_finish)
    gui_hooks.collection_did_load.append(_collection_did_load)  # pyright: ignore[reportUnknownMemberType]


def _profile_closing() -> None:
    mylog.info("profile_closing")
    from aqt import gui_hooks
    from JAStudio.Core.Anki import AnkiLifecycleEvent

    global _anki_collection, _initialized

    gui_hooks.sync_will_start.remove(_sync_will_start)
    gui_hooks.sync_did_finish.remove(_sync_did_finish)
    gui_hooks.collection_did_load.remove(_collection_did_load)  # pyright: ignore[reportUnknownMemberType]

    _stop_sync_bridges()
    _notify_dotnet(AnkiLifecycleEvent.ProfileClosing)
    _anki_collection = None
    _initialized = False


# noinspection Annotator
def _sync_will_start(_col: object | None = None) -> None:
    mylog.info("sync_will_start")
    from JAStudio.Core.Anki import AnkiLifecycleEvent
    _stop_sync_bridges()
    _notify_dotnet(AnkiLifecycleEvent.SyncStarting)


def _sync_did_finish() -> None:
    mylog.info("sync_did_finish")
    from aqt import mw
    from JAStudio.Core.Anki import AnkiLifecycleEvent

    global _anki_collection
    _anki_collection = non_optional(mw.col)
    _start_sync_bridges(_anki_collection)
    _notify_dotnet(AnkiLifecycleEvent.SyncCompleted)


# noinspection Annotator
def _collection_did_load(_col: object | None = None) -> None:
    mylog.info("collection_did_load")
    from aqt import mw
    from JAStudio.Core.Anki import AnkiLifecycleEvent

    global _anki_collection
    _stop_sync_bridges()
    _anki_collection = non_optional(mw.col)
    _start_sync_bridges(_anki_collection)
    _notify_dotnet(AnkiLifecycleEvent.CollectionLoaded)


def anki_config() -> ConfigManagerEx:
    from aqt import mw

    from jastudio.anki_extentions.config_manager_ex import ConfigManagerEx
    return ConfigManagerEx(non_optional(mw.col).conf)


def anki_collection() -> Collection:
    if _anki_collection is None: raise AssertionError("Anki collection not available")
    return _anki_collection


def anki_db() -> DBProxy: return non_optional(anki_collection().db)


def anki_scheduler() -> Scheduler:
    from anki.scheduler.v3 import Scheduler  # pyright: ignore[reportMissingTypeStubs]
    return checked_cast(Scheduler, anki_collection().sched)


def main_window() -> AnkiQt:
    from aqt import mw
    return non_optional(mw)


def get_ui_utils() -> IUIUtils:
    from jastudio.ankiutils.ui_utils import UIUtils
    return UIUtils(main_window())


def _setup_gui_hooks() -> None:
    from aqt import gui_hooks
    gui_hooks.profile_will_close.append(_profile_closing)
    gui_hooks.profile_did_open.append(_profile_opened)

user_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\\user_files")

_setup_gui_hooks()
