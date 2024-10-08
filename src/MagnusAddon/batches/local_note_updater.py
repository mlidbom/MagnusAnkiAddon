from ankiutils import app, query_builder
from language_services.janome_ex.tokenizing import janome_ex
from note.kanjinote import KanjiNote
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote

from sysutils import progress_display_runner

def update_all() -> None:
    update_sentences()
    update_kanji()
    update_vocab()
    #update_vocab_parsed_parts_of_speech()


#todo: I don't think this is reliable at the moment. Review it.
def update_vocab_parsed_parts_of_speech() -> None:
    for vocab in app.col().vocab.all():
        vocab.set_parsed_type_of_speech(janome_ex.get_word_parts_of_speech(vocab.get_question()))

def update_sentences() -> None:
    def update_sentence(sentence: SentenceNote) -> None:
        sentence.update_generated_data()

    progress_display_runner.process_with_progress(app.col().sentences.all(), update_sentence, "Updating sentences", allow_cancel=True)


def update_kanji() -> None:
    def _update_kanji(kanji: KanjiNote) -> None:
        kanji.update_generated_data()

    progress_display_runner.process_with_progress(app.col().kanji.all(), _update_kanji, "Updating kanji", allow_cancel=True)

def update_vocab() -> None:
    def _update_vocab(vocab: VocabNote) -> None:
        vocab.update_generated_data()

    progress_display_runner.process_with_progress(app.col().vocab.all(), _update_vocab, "Updating vocab", allow_cancel=True)


def generate_sentences_for_context_sentences_with_audio() -> None:
    def generate_sentences(vocab: VocabNote) -> None:
        vocab.generate_sentences_from_context_sentences(require_audio=True)

    progress_display_runner.process_with_progress(app.col().vocab.all(), generate_sentences, "Generating sentences", allow_cancel=True)

def convert_immersion_kit_sentences() -> None:
    immersion_kit_sences = app.anki_collection().find_notes(query_builder.immersion_kit_sentences())
    for note_id in immersion_kit_sences:
        immersion_kit_note = app.anki_collection().get_note(note_id)
        SentenceNote.import_immersion_kit_sentence(immersion_kit_note)
        app.anki_collection().remove_notes([note_id])