from ankiutils import app, query_builder
from language_services.janome_ex.tokenizing import janome_ex
from note.sentencenote import SentenceNote

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

    progress_display_runner.process_with_progress(app.col().sentences.all(), update_sentence, "Updating sentences", allow_cancel=True, delay_display=False)


def update_kanji() -> None:
    for kanji in app.col().kanji.all(): kanji.update_generated_data()

def update_vocab() -> None:
    for vocab in app.col().vocab.all(): vocab.update_generated_data()


def generate_sentences_for_context_sentences_with_audio() -> None:
    for vocab in app.col().vocab.all():
        vocab.generate_sentences_from_context_sentences(require_audio=True)

def convert_immersion_kit_sentences() -> None:
    immersion_kit_sences = app.anki_collection().find_notes(query_builder.immersion_kit_sentences())
    for note_id in immersion_kit_sences:
        immersion_kit_note = app.anki_collection().get_note(note_id)
        SentenceNote.import_immersion_kit_sentence(immersion_kit_note)
        app.anki_collection().remove_notes([note_id])