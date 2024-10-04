from ankiutils import app
from language_services.janome_ex.tokenizing import janome_ex
from note.note_constants import Mine
from note.sentencenote import SentenceNote
from sysutils import ex_str

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


def tmp_generate_context_sentences() -> None:
    class ContextSentence:
        def __init__(self, vocab:str, japanese: str, english: str, audio: str) -> None:
            self.vocab = vocab
            self.question = japanese
            self.answer = english
            self.audio = audio

    all_vocab = app.col().vocab.all()

    context_sentences = [ContextSentence(voc.get_question(), voc.get_context_jp(), voc.get_context_en(), voc.get_context_jp_audio()) for voc in all_vocab if voc.get_context_jp().strip()]
    context_sentences += [ContextSentence(voc.get_question(), voc.get_context_jp_2(), voc.get_context_en_2(), voc.get_context_jp_2_audio()) for voc in all_vocab if voc.get_context_jp_2().strip()]
    context_sentences += [ContextSentence(voc.get_question(), voc.get_context_jp_3(), voc.get_context_en_3(), voc.get_context_jp_3_audio()) for voc in all_vocab if voc.get_context_jp_3().strip()]

    #let's not add duplicate sentences
    context_sentences = [sent for sent in context_sentences if not app.col().sentences.with_question(sent.question)]

    #For now for testing, only create sentences for context sentences that have audio so that we don't clog up the collection with useless sentences
    context_sentences = [sent for sent in context_sentences if sent.audio]

    for sentence in context_sentences:
        created = SentenceNote.add_sentence(sentence.question, sentence.answer, sentence.audio)
        created.position_extra_vocab(sentence.vocab)
        created.set_tag(Mine.Tags.TTSAudio)



