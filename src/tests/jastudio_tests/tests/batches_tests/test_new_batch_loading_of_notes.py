# from __future__ import annotations
#
# from typing import TYPE_CHECKING
#
# import pytest
# from jastudio.ankiutils import app
# from jastudio_tests.fixtures.collection_factory import inject_collection_with_all_sample_data
# from jastudio_tests.fixtures.stub_factory import stub_ui_dependencies
# from note.collection.jp_collection import JPCollection
# from qt_utils.task_runner_progress_dialog import TaskRunner
#
# if TYPE_CHECKING:
#     from collections.abc import Iterator, Sequence
#
#     from note.jpnote import JPNote
#
# # noinspection PyUnusedFunction
# @pytest.fixture(scope="function")
# def setup() -> Iterator[None]:
#     with (stub_ui_dependencies(), inject_collection_with_all_sample_data()):
#         yield
#
# @pytest.mark.usefixtures("setup")
# def test_batch_loading_all_notes() -> None:
#     def assert_all_notes_equal(old_jp_list: Sequence[JPNote], new_jp_list: Sequence[JPNote]) -> None:
#         assert len(old_jp_list) == len(new_jp_list)
#         assert len(old_jp_list) > 10
#         old_list = [jp.backend_note for jp in old_jp_list]
#         new_list = [jp.backend_note for jp in new_jp_list]
#         all_old_dict = {note.id: note for note in old_list}
#
#         for new in new_list:
#             old = all_old_dict[new.id]
#             assert old.id == new.id
#             assert old.guid == new.guid
#             assert old.mid == new.mid
#             assert old.mod == new.mod
#             assert old.usn == new.usn
#             assert old.tags == new.tags
#             assert old.fields == new.fields
#             assert old._fmap == new._fmap # pyright: ignore[reportPrivateUsage]
#
#             assert old.flags == new.flags
#             assert old.data == new.data
#
#             assert old.values() == new.values()
#
#     new_collection = JPCollection(app.anki_collection())
#
#     task_runner = TaskRunner.invisible()
#
#     assert_all_notes_equal(new_collection.kanji.all(), new_collection.kanji.all_old(task_runner))
#     assert_all_notes_equal(new_collection.sentences.all(), new_collection.sentences.all_old(task_runner))
#     assert_all_notes_equal(new_collection.vocab.all(), new_collection.vocab.all_old(task_runner))
#
#     new_collection.destruct_sync()
