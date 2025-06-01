from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from aqt.utils import showInfo
from note.kanjinote import KanjiNote
from note.note_constants import Tags
from note.sentences.sentencenote import SentenceNote
from note.vocabulary.vocabnote import VocabNote
from sysutils import progress_display_runner
from wanikani.wanikani_api_client import WanikaniClient

if TYPE_CHECKING:
    from wanikani_api.models import Vocabulary

waniClient = WanikaniClient.get_instance()

def import_missing_kanji() -> None:
    all_kanji: list[KanjiNote] = app.col().kanji.all_wani()
    local_kanji_dictionary = {kanji.get_question(): kanji for kanji in all_kanji}
    all_wani_kanji = waniClient.list_kanji()
    imported = 0
    for wani_kanji in all_wani_kanji:
        if wani_kanji.characters not in local_kanji_dictionary:
            print(f"Importing: {wani_kanji.slug}")
            KanjiNote.create_from_wani_kanji(wani_kanji)
            imported += 1

    showInfo(f"Imported {imported} kanji notes")

def import_missing_vocab() -> None:
    all_wani_vocabulary = waniClient.list_vocabulary()
    imported = 0
    for wani_vocab in all_wani_vocabulary:
        question = str(wani_vocab.characters)
        if not app.col().vocab.with_question(question):
            print(f"""Importing: {wani_vocab.slug}""")
            VocabNote.factory.create_from_wani_vocabulary(wani_vocab)
            imported += 1

    showInfo(f"""Imported {imported} vocabulary notes""")

def import_missing_context_sentences() -> None:
    progress = progress_display_runner.open_spinning_progress_dialog("Fetching wanikani vocabulary. Please be patient this will complete in a minute or two.")
    sentence_collection = app.col().sentences
    all_wani_vocabulary = waniClient.list_vocabulary()
    imported_sentences: list[SentenceNote] = []
    present: list[SentenceNote] = []
    progress.close()

    def handle_vocab(wani_vocab: Vocabulary) -> None:
        for sentence in wani_vocab.context_sentences:
            vocab = str(wani_vocab.characters)
            question = str(sentence.japanese).strip()
            answer = str(sentence.english).strip()

            existing_sentences = sentence_collection.with_question(question)

            if not existing_sentences:
                print(f"""Importing {vocab} :: {question} || {answer}""")
                imported_sentences.append(SentenceNote.add_sentence(question=question, answer=answer, highlighted_vocab={vocab}, tags={Tags.wani_sentence_current}))
            else:
                for existing in existing_sentences:
                    existing.set_tag(Tags.wani_sentence_current)
                    if vocab not in existing.configuration.highlighted_words():
                        existing.configuration.add_highlighted_word(vocab)
                    present.append(existing)

    progress_display_runner.process_with_progress(all_wani_vocabulary, handle_vocab, "Processing found Wanikani vacabulary")

    old_sentences = [sent for sent in app.col().sentences.all() if sent.has_tag(Tags.Wani) and not sent.has_tag(Tags.wani_sentence_current)]
    for old_sentence in old_sentences:
        old_sentence.remove_tag(Tags.wani_sentence_current)
        old_sentence.set_tag(Tags.wani_sentence_removed_on_wani)

    progress_display_runner.show_dismissable_message(window_title="Import completed", message=f"""
    Imported: {len(imported_sentences)} sentences.
    Already present: {len(present)} sentences.
    Marked as removed: {len(old_sentences)} sentences.""")
