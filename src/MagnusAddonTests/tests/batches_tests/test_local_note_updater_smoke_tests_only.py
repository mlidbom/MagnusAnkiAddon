from typing import Any, Generator

import pytest

# from ankiutils import app
from fixtures.collection_factory import inject_anki_collection_with_all_sample_data
from fixtures.stub_factory import stub_ui_dependencies
# from language_services.janome_ex.word_extraction.candidate_word import CandidateWord
# from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
# from note.vocabnote import VocabNote

# noinspection PyUnusedFunction
@pytest.fixture(scope="function")
def setup() -> Generator[None, None, None]:
    with (stub_ui_dependencies(), inject_anki_collection_with_all_sample_data()):
        yield


def test_smoke_update_all(setup:Any) -> None:
    from batches import local_note_updater
    local_note_updater.update_all()


def test_memory_leak(setup:Any) -> None:
    pass
    # from batches import local_note_updater
    #
    # print()
    # print("starting")
    #
    # def output_function(o:Any) -> str:
    #     return str(type(o))
    #
    # print("aoeusnth")
    #
    # from pympler import muppy, summary, refbrowser, tracker
    # tr = tracker.SummaryTracker()  # type: ignore
    #
    # tr.print_diff()# type: ignore
    #
    # for sentence in  app.col().sentences.all():
    #     sentence.update_parsed_words(force=True)
    #
    # tr.print_diff()  # type: ignore

    # analysis = TextAnalysis(app.col().sentences.all()[0].get_question(), [])
    #
    # cb = refbrowser.ConsoleBrowser(analysis, maxdepth=2, str_func=output_function)  # type: ignore
    # cb.print_tree()  # type: ignore
    #
    # all_objects = muppy.get_objects()
    # instances = muppy.filter(all_objects, TextAnalysis)

    # if instances:
    #     root = instances[0]
    #
    #     cb = refbrowser.ConsoleBrowser(analysis, maxdepth=2, str_func=output_function)  # type: ignore
    #     cb.print_tree()  # type: ignore
    #
    #     # ib = refbrowser.InteractiveBrowser(root) # type: ignore
    #     # ib.main() # type: ignore
    #
    #     print("finished")
    #
    #     # sum1 = summary.summarize(all_objects) # type: ignore
    #     # summary.print_(sum1) # type: ignore
    # else:
    #     print("no instances")
