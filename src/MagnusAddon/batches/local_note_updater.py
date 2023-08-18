from typing import *

from parsing.textparser import DictLookup
from sysutils import kana_utils
from parsing import janomeutils
from sysutils.utils import StringUtils, UIUtils
from note.wanikanjinote import WaniKanjiNote
from note.wanivocabnote import WaniVocabNote
from wanikani.wani_collection import WaniCollection
from wanikani.wani_constants import Mine


def update_all() -> None:
    def update_all_inner() -> None:
        all_vocabulary: list[WaniVocabNote] = WaniCollection.fetch_all_vocab_notes()
        all_kanji: list[WaniKanjiNote] = WaniCollection.fetch_all_kanji_notes()
        all_sentences = WaniCollection.list_sentence_notes()

        _update_sentences(all_sentences)
        _update_kanji(all_vocabulary, all_kanji)
        _update_vocab(all_vocabulary, all_kanji)
        _update_vocab_parsed_parts_of_speech(all_vocabulary)

    UIUtils.run_ui_action(update_all_inner)

def update_vocab_pos_information() -> None:
    def inner() -> None:
        all_vocabulary: list[WaniVocabNote] = WaniCollection.fetch_all_vocab_notes()
        for vocab in all_vocabulary:
            try:
                lookup = DictLookup.lookup_vocab_word_or_name(vocab)
            except KeyError:
                pass

    UIUtils.run_ui_action(inner)


def _update_vocab_parsed_parts_of_speech(all_vocabulary: list[WaniVocabNote]) -> None:
    for vocab in all_vocabulary:
        vocab.set_parsed_type_of_speech(janomeutils.get_word_parts_of_speech(vocab.get_vocab()))

def update_sentences() -> None:
    UIUtils.run_ui_action(lambda: _update_sentences(WaniCollection.list_sentence_notes()))

def update_kanji(_kanji_note: WaniKanjiNote) -> None:
    UIUtils.run_ui_action(lambda: _update_kanji(WaniCollection.fetch_all_vocab_notes(), WaniCollection.fetch_all_kanji_notes()))

def update_vocab() -> None:
    UIUtils.run_ui_action(lambda: _update_vocab(WaniCollection.fetch_all_vocab_notes(), WaniCollection.fetch_all_kanji_notes()))

def _sort_vocab_list(vocabs: List[WaniVocabNote]) -> list[WaniVocabNote]:
    vocabs.sort(key=lambda vocab: (vocab.get_level(), vocab.get_lesson_position()))
    return vocabs

def _update_sentences(sentences) -> None:
    for sentence in sentences: sentence.update_parsed_words()

def _update_vocab(all_vocabulary: list[WaniVocabNote], all_kanji: list[WaniKanjiNote]) -> None:
    def update_kanji_names() -> None:
        def prepare_kanji_meaning(kanji: WaniKanjiNote) -> str:
            meaning = kanji.get_kanji_meaning()
            meaning = StringUtils.strip_markup(meaning)
            meaning = meaning.strip().replace(",", "/").replace(" ", "")
            return meaning

        kanji_dict = {kanji.get_kanji(): prepare_kanji_meaning(kanji) for kanji in all_kanji}
        for vocab_note in all_vocabulary:
            kanji_list = StringUtils.extract_characters(vocab_note.get_vocab())
            kanji_list = [item for item in kanji_list if item in kanji_dict]
            kanji_meanings = [kanji_dict[kanji] for kanji in kanji_list]
            kanji_names_string = " # ".join(kanji_meanings)
            vocab_note.set_kanji_name(kanji_names_string)

    def format_context_sentences() -> None:
        for vocab in all_vocabulary:
            def format_sentence(html_sentence: str):
                clean_sentence = StringUtils.strip_markup(html_sentence)
                word = vocab.get_vocab()
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

    def fill_empty_reading_for_uk_vocab() -> None:
        for vocab in all_vocabulary:
            expression = vocab.get_vocab().strip()
            readings = ",".join(vocab.get_readings())

            if expression == readings:
                vocab.set_tag(Mine.Tags.UsuallyKanaOnly)

            if not readings:
                if kana_utils.is_only_kana(expression):
                    vocab.set_readings([expression])
                    vocab.set_tag(Mine.Tags.UsuallyKanaOnly)


    def populate_homophones() -> None:
        reading_dict = dict[str, list[WaniVocabNote]]()
        for vocab in all_vocabulary:
            for reading in vocab.get_readings():
                if reading not in reading_dict: reading_dict[reading] = list[WaniVocabNote]()
                reading_dict[reading].append(vocab)

        for read, vocabs in reading_dict.items():
            if len(vocabs) > 1:
                for vocab in vocabs:
                    homonyms = [voc.get_vocab() for voc in vocabs if voc is not vocab]
                    vocab.set_related_homophones(homonyms)


    update_kanji_names()
    format_context_sentences()
    fill_empty_reading_for_uk_vocab()
    populate_homophones()


def _update_kanji(all_vocabulary: list[WaniVocabNote], all_kanji: list[WaniKanjiNote]):
    def generate_vocab_html_list(note: WaniKanjiNote, vocabs: List[WaniVocabNote]):

        return f'''
                <div class="kanjiVocabList">
                    <div>
                    
                    {StringUtils.newline().join([f"""
                    <div class="kanjiVocabEntry">
                        <span class="kanji clipboard">{vocab.get_vocab()}</span>
                        (<span class="clipboard vocabReading">{note.tag_readings_in_string(", ".join(vocab.get_readings()), lambda read: f'<span class="kanjiReading">{read}</span>')}</span>)
                        <span class="meaning"> {StringUtils.strip_markup(vocab.get_vocab_meaning())}</span>
                    </div>
                    """ for vocab in vocabs])}
                    
                    </div>
                </div>
                '''
    all_vocabulary = _sort_vocab_list(all_vocabulary)  # we want a specific order in the kanji entries etc
    kanji_dict: Dict[str, WaniKanjiNote] = {kanji.get_kanji(): kanji for kanji in all_kanji}
    kanji_vocab_dict: Dict[str, List[WaniVocabNote]] = {kanji.get_kanji(): [] for kanji in all_kanji}

    for voc in all_vocabulary:
        for char in voc.get_vocab():
            if char in kanji_vocab_dict:
                kanji_vocab_dict[char].append(voc)

    for kanji, vocabulary_entries in kanji_vocab_dict.items():
        kanji_note = kanji_dict[kanji]
        html = generate_vocab_html_list(kanji_note, vocabulary_entries)
        kanji_note.set_vocabs(html)
        kanji_note.set_vocabs_raw([vo.get_vocab() for vo in vocabulary_entries])

    kanji_with_vocab = [kanji for kanji in all_kanji if kanji.get_primary_vocab()]
    for kanji in kanji_with_vocab:
        kanji_vocab = kanji_vocab_dict[kanji.get_kanji()]
        primary_vocabs: List[str] = [StringUtils.strip_markup(vocab).strip() for vocab in kanji.get_primary_vocab().split(",")]
        if len(primary_vocabs) > 0:
            found_vocab: list[WaniVocabNote] = list[WaniVocabNote]()
            vocab_to_vocab: dict[str, WaniVocabNote] = {vo.get_vocab(): vo for vo in kanji_vocab}
            reading_to_vocab: dict[str, WaniVocabNote] = dict[str, WaniVocabNote]()

            for vocab in kanji_vocab:
                for reading in vocab.get_readings():
                    reading_to_vocab[reading] = vocab

            for vocab in primary_vocabs:
                if vocab in vocab_to_vocab:
                    found_vocab.append(vocab_to_vocab[vocab])
                elif vocab in reading_to_vocab:
                    found_vocab.append(reading_to_vocab[vocab])

            if len(found_vocab) > 0:
                audios = "".join([vo.get_audios() for vo in found_vocab])
                kanji.set_primary_vocab_audio(audios)
