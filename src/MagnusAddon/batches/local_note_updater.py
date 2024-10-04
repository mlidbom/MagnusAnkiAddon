from ankiutils import app
from language_services.janome_ex.tokenizing import janome_ex
from note.note_constants import Mine
from note.sentencenote import SentenceNote

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
    for sentence in app.col().sentences.all(): sentence.update_generated_data()

def update_kanji() -> None:
    for kanji in app.col().kanji.all(): kanji.update_generated_data()

def update_vocab() -> None:
    for vocab in app.col().vocab.all(): vocab.update_generated_data()


def generate_sentences_for_context_sentences_with_audio() -> None:
    for vocab in app.col().vocab.all():
        vocab.generate_sentences_from_context_sentences(require_audio=True)



