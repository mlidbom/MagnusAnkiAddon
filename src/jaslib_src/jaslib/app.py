# from __future__ import annotations
#
# import os
# from pathlib import Path
# from typing import TYPE_CHECKING
#
# from typed_linq_collections.collections.q_set import QSet
#
# from jaslib.testutils import ex_pytest
#
# is_testing = ex_pytest.is_testing
#
# if TYPE_CHECKING:
#     from collections.abc import Callable
#
#     from jaslib.configuration.configuration_value import JapaneseConfig
#     from jaslib.note.backend_note_creator import IBackendNoteCreator
#     from jaslib.note.collection.jp_collection import JPCollection
#
# _collection: JPCollection | None = None
# _backend_note_creator: IBackendNoteCreator | None = None
#
# init_hooks: QSet[Callable[[], None]] = QSet()
#
# def add_init_hook(hook: Callable[[], None]) -> None:
#     init_hooks.add(hook)  # todo migration
#
# def config() -> JapaneseConfig:
#     from jaslib.configuration import configuration_value
#     return configuration_value.config()
#
# def col() -> JPCollection:
#     global _collection
#     if _collection is None:
#         if _backend_note_creator is None: raise Exception("Backend note creator not initialized")
#         from jaslib.note.collection.jp_collection import JPCollection
#         _collection = JPCollection(_backend_note_creator)
#     return _collection
#
# def reset(backend_note_creator: IBackendNoteCreator) -> None:
#     from jaslib.note.collection.jp_collection import JPCollection
#     global _collection
#     global _backend_note_creator
#     if _collection is not None:
#         _collection = None
#     if is_testing:
#         _collection = JPCollection(backend_note_creator)
#     _backend_note_creator = backend_note_creator
#
# user_files_dir = str(Path(os.path.abspath(__file__)).parent.parent.parent / "user_files")
