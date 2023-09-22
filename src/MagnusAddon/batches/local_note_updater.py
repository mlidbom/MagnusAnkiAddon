from typing import *

from note.sentencenote import SentenceNote
from note_content_building import sentence_content_builder
from parsing.jamdict_extensions.dict_lookup import DictLookup
from sysutils import kana_utils
from parsing import janomeutils
from sysutils.utils import StringUtils
from sysutils.ui_utils import UIUtils
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
        _set_vocab_uk_and_forms_from_dictionary(all_vocabulary)
        _update_vocab_parsed_parts_of_speech(all_vocabulary)

    UIUtils.run_ui_action(update_all_inner)

def set_vocab_uk_and_forms_from_dictionary() -> None:
    def inner() -> None:
        all_vocabulary: list[WaniVocabNote] = WaniCollection.fetch_all_vocab_notes()
        _set_vocab_uk_and_forms_from_dictionary(all_vocabulary)

    UIUtils.run_ui_action(inner)

def _set_vocab_uk_and_forms_from_dictionary(all_vocabulary: list[WaniVocabNote]) -> None:
    for vocab in all_vocabulary:
        lookup = DictLookup.try_lookup_vocab_word_or_name(vocab)
        if lookup.is_uk() and not vocab.has_tag(Mine.Tags.DisableKanaOnly):
            vocab.set_tag(Mine.Tags.UsuallyKanaOnly)

        if not vocab.get_forms():
            if lookup.found_words():
                vocab.set_forms(lookup.valid_forms(vocab.is_uk()))
            else:
                vocab.set_forms(set(vocab.get_readings()))


def _update_vocab_parsed_parts_of_speech(all_vocabulary: list[WaniVocabNote]) -> None:
    for vocab in all_vocabulary:
        vocab.set_parsed_type_of_speech(janomeutils.get_word_parts_of_speech(vocab.get_question()))

def update_sentences() -> None:
    UIUtils.run_ui_action(lambda: _update_sentences(WaniCollection.list_sentence_notes()))

def update_sentence_breakdown() -> None:
    UIUtils.run_ui_action(lambda: _update_sentence_breakdown(WaniCollection.list_sentence_notes()))

def update_kanji(_kanji_note: WaniKanjiNote) -> None:
    UIUtils.run_ui_action(lambda: _update_kanji(WaniCollection.fetch_all_vocab_notes(), WaniCollection.fetch_all_kanji_notes()))

def update_vocab() -> None:
    UIUtils.run_ui_action(lambda: _update_vocab(WaniCollection.fetch_all_vocab_notes(), WaniCollection.fetch_all_kanji_notes()))


def _update_sentences(sentences: list[SentenceNote]) -> None:
    for sentence in sentences: sentence.update_generated_data()

def _update_sentence_breakdown(sentences: list[SentenceNote]) -> None:
    first_few = sentences[:100]
    for sentence in first_few: sentence_content_builder.build_breakdown_html(sentence)

def _update_vocab(all_vocabulary: list[WaniVocabNote], all_kanji: list[WaniKanjiNote]) -> None:
    def update_generated_data() -> None:
        for vocab in all_vocabulary:
            vocab.update_generated_data()

    def update_kanji_names() -> None:
        def prepare_kanji_meaning(kanji: WaniKanjiNote) -> str:
            meaning = kanji.get_active_answer()
            meaning = StringUtils.strip_html_and_bracket_markup(meaning)
            meaning = meaning.strip().replace(",", "/").replace(" ", "")
            return meaning

        kanji_dict = {kanji.get_question(): prepare_kanji_meaning(kanji) for kanji in all_kanji}
        for vocab_note in all_vocabulary:
            kanji_list = StringUtils.extract_characters(vocab_note.get_question())
            kanji_list = [item for item in kanji_list if item in kanji_dict]
            kanji_meanings = [kanji_dict[kanji] for kanji in kanji_list]
            kanji_names_string = " # ".join(kanji_meanings)
            vocab_note.set_kanji_name(kanji_names_string)

    def format_context_sentences() -> None:
        for vocab in all_vocabulary:
            def format_sentence(html_sentence: str):
                clean_sentence = StringUtils.strip_html_and_bracket_markup(html_sentence)
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

    def fill_empty_reading_for_uk_vocab() -> None:
        for vocab in all_vocabulary:
            q = vocab.get_question().strip()
            readings = ",".join(vocab.get_readings())

            if q == readings:
                vocab.set_tag(Mine.Tags.UsuallyKanaOnly)

            if not readings:
                if kana_utils.is_only_kana(q):
                    vocab.set_readings([q])
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
                    homonyms = [voc.get_question() for voc in vocabs if voc is not vocab]
                    vocab.set_related_homophones(homonyms if read else [])

    update_generated_data()
    update_kanji_names()
    format_context_sentences()
    fill_empty_reading_for_uk_vocab()
    populate_homophones()


def _update_kanji(all_vocabulary: list[WaniVocabNote], all_kanji: list[WaniKanjiNote]):
    def generate_vocab_html_list(note: WaniKanjiNote, vocabs: List[WaniVocabNote]):
        def sort_vocab_list() -> None:
            def prefer_primary_vocab_in_order(local_vocab: WaniVocabNote):
                for index, primary in enumerate(primary_voc):
                    if local_vocab.get_question() == primary or local_vocab.get_readings()[0] == primary:
                        return index

                return 100

            def prefer_non_compound(local_vocab: WaniVocabNote) -> str:
                return "A" if kana_utils.is_only_kana(local_vocab.get_question()[1:]) else "B"

            def prefer_starts_with_vocab(local_vocab: WaniVocabNote) -> str:
                return "A" if local_vocab.get_question()[0] == note.get_question() else "B"

            vocabs.sort(key=lambda local_vocab: (prefer_primary_vocab_in_order(local_vocab),
                                                 prefer_non_compound(local_vocab),
                                                 prefer_starts_with_vocab(local_vocab),
                                                 voc.get_question()))

        primary_voc = note.get_primary_vocab()
        sort_vocab_list()

        return f'''
                <div class="kanjiVocabList">
                    <div>
                    
                    {StringUtils.newline().join([f"""
                    <div class="kanjiVocabEntry">
                        <span class="kanji clipboard">{inner_vocab.get_question()}</span>
                        (<span class="clipboard vocabReading">{note.tag_readings_in_string(", ".join(inner_vocab.get_readings()), lambda read: f'<span class="kanjiReading">{read}</span>')}</span>)
                        <span class="meaning"> {StringUtils.strip_html_markup(inner_vocab.get_active_answer())}</span>
                    </div>
                    """ for inner_vocab in vocabs])}
                    
                    </div>
                </div>
                '''

    def update_generated_data() -> None:
        for kanji in all_kanji:
            kanji.update_generated_data()

    update_generated_data()

    kanji_dict: Dict[str, WaniKanjiNote] = {kanji.get_question(): kanji for kanji in all_kanji}
    kanji_vocab_dict: Dict[str, List[WaniVocabNote]] = {kanji.get_question(): [] for kanji in all_kanji}

    for voc in all_vocabulary:
        for char in voc.get_question():
            if char in kanji_vocab_dict:
                kanji_vocab_dict[char].append(voc)

    for kanji, vocabulary_entries in kanji_vocab_dict.items():
        kanji_note = kanji_dict[kanji]
        html = generate_vocab_html_list(kanji_note, vocabulary_entries)
        kanji_note.set_vocabs(html)
        kanji_note.set_vocabs_raw([vo.get_question() for vo in vocabulary_entries])

    kanji_with_vocab = [kanji for kanji in all_kanji if kanji.get_primary_vocab()]
    for kanji in kanji_with_vocab:
        kanji_vocab = kanji_vocab_dict[kanji.get_question()]
        primary_vocabs: List[str] = kanji.get_primary_vocab()
        if len(primary_vocabs) > 0:
            found_vocab: list[WaniVocabNote] = list[WaniVocabNote]()
            vocab_to_vocab: dict[str, WaniVocabNote] = {vo.get_question(): vo for vo in kanji_vocab}
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
