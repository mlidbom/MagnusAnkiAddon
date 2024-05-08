from ankiutils import app
from note.sentencenote import SentenceNote
from sysutils import ex_str, kana_utils
from language_services.janome_ex.tokenizing import janome_ex
from note.kanjinote import KanjiNote
from note.vocabnote import VocabNote



def update_all() -> None:
    all_vocabulary: list[VocabNote] = app.col().vocab.all()
    all_kanji: list[KanjiNote] = app.col().kanji.all()
    all_sentences = app.col().sentences.all()

    _update_sentences(all_sentences)
    _update_kanji(all_kanji)
    _update_vocab(all_vocabulary, all_kanji)
    _update_vocab_parsed_parts_of_speech(all_vocabulary)


def _update_vocab_parsed_parts_of_speech(all_vocabulary: list[VocabNote]) -> None:
    for vocab in all_vocabulary:
        vocab.set_parsed_type_of_speech(janome_ex.get_word_parts_of_speech(vocab.get_question()))

def update_sentences() -> None:
    _update_sentences(app.col().sentences.all())

def update_kanji() -> None:
    _update_kanji(app.col().kanji.all())

def update_vocab() -> None:
    _update_vocab(app.col().vocab.all(), app.col().kanji.all())

def _update_sentences(sentences: list[SentenceNote]) -> None:
    for sentence in sentences: sentence.update_generated_data()

def _update_vocab(all_vocabulary: list[VocabNote], all_kanji: list[KanjiNote]) -> None:
    def update_generated_data() -> None:
        for vocab in all_vocabulary:
            vocab.update_generated_data()

    def update_kanji_names() -> None: # todo move to a rendering step
        def prepare_kanji_meaning(kanji: KanjiNote) -> str:
            meaning = kanji.get_answer()
            meaning = ex_str.strip_html_and_bracket_markup(meaning)
            meaning = meaning.strip().replace(",", "/").replace(" ", "")
            return meaning

        kanji_dict = {kanji.get_question(): prepare_kanji_meaning(kanji) for kanji in all_kanji}
        for vocab_note in all_vocabulary:
            kanji_list = ex_str.extract_characters(vocab_note.get_question())
            kanji_list = [item for item in kanji_list if item in kanji_dict]
            kanji_meanings = [kanji_dict[kanji] for kanji in kanji_list]
            kanji_names_string = " # ".join(kanji_meanings)
            vocab_note.set_kanji_name(kanji_names_string)

    def format_context_sentences() -> None: # todo move to a rendering step
        for vocab in all_vocabulary:
            def format_sentence(html_sentence: str) -> str:
                clean_sentence = ex_str.strip_html_and_bracket_markup(html_sentence)
                word = vocab.get_question()
                if word in clean_sentence:
                    return clean_sentence.replace(word, f"""<span class="vocabInContext">{word}</span>""")
                else:
                    word = kana_utils.get_conjugation_base(word)
                    return clean_sentence.replace(word, f"""<span class="vocabInContext">{word}</span>""")

            for get_context_japanese, set_contex_japanese in [(vocab.get_context_jp, vocab.set_context_jp), (vocab.get_context_jp_2, vocab.set_context_jp_2),
                                                              (vocab.get_context_jp_3, vocab.set_context_jp_3)]:
                sentence = get_context_japanese()
                if sentence:
                    formatted = format_sentence(sentence)
                    set_contex_japanese(formatted)


    def populate_homophones() -> None: # todo move to a rendering step
        reading_dict = dict[str, list[VocabNote]]()
        for vocab in all_vocabulary:
            for reading in vocab.get_readings():
                if reading not in reading_dict: reading_dict[reading] = list[VocabNote]()
                reading_dict[reading].append(vocab)

        for read, vocabs in reading_dict.items():
            if len(vocabs) > 1:
                for vocab in vocabs:
                    homonyms = [voc.get_question() for voc in vocabs if voc is not vocab]
                    vocab.set_related_homophones(homonyms if read else [])

    update_generated_data()
    update_kanji_names()
    format_context_sentences()
    populate_homophones()


def _update_kanji(all_kanji: list[KanjiNote]) -> None:
    def update_generated_data() -> None:
        for kanji in all_kanji:
            kanji.update_generated_data()

    update_generated_data()

