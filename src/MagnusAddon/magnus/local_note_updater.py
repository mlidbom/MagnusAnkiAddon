from typing import *

from aqt.utils import tooltip

from .utils import StringUtils
from .wani_collection import WaniCollection
from .wanikani_note import *
import time

def update_all():
    def sort_vocab_list(vocabs: List[WaniVocabNote]) -> list[WaniVocabNote]:
        vocabs.sort(key=lambda vocab: (vocab.get_level(), vocab.get_lesson_position()))
        return vocabs

    all_vocabulary: list[WaniVocabNote] = WaniCollection.fetch_all_vocab_notes()
    all_kanji: list[WaniKanjiNote] = WaniCollection.fetch_all_kanji_notes()
    all_vocabulary = sort_vocab_list(all_vocabulary)# we want a specific order in the kanji entries etc

    _update_kanji(all_vocabulary, all_kanji)
    _update_vocab(all_vocabulary, all_kanji)

def _update_vocab(all_vocabulary: list[WaniVocabNote], all_kanji: list[WaniKanjiNote]) -> None:
    def update_kanji_names(all_vocabulary, all_kanji):
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

    update_kanji_names(all_vocabulary, all_kanji)
    tooltip("done")

def _update_kanji(all_vocabulary: list[WaniVocabNote], all_kanji: list[WaniKanjiNote]):
    def generate_vocab_html_list(vocabs: List[WaniVocabNote]):
        return f'''
                <div class="kanjiVocabList">
                    <div>
                    
                    {StringUtils.Newline().join([f"""
                    <div class="entry">
                        <span class="kanji clipboard">{vocab.get_vocab()}</span>
                        (<span class="reading clipboard">{vocab.get_reading()}</span>)
                        <span class="meaning"> {StringUtils.strip_markup(vocab.get_vocab_meaning())}</span>
                    </div>
                    """ for vocab in vocabs])}
                    
                    </div>
                </div>
                '''

    kanji_dict: Dict[str, WaniKanjiNote]   = {kanji.get_kanji(): kanji for kanji in all_kanji}
    kanji_vocab_dict: Dict[str, List[WaniVocabNote]] = {kanji.get_kanji(): [] for kanji in all_kanji}

    for voc in all_vocabulary:
        for char in voc.get_vocab():
            if char in kanji_vocab_dict:
                kanji_vocab_dict[char].append(voc)

    for kanji, vocabs in kanji_vocab_dict.items():

        html = generate_vocab_html_list(vocabs)
        kanji_dict[kanji].set_vocabs(html)

    kanji_with_vocab = [kanji for kanji in all_kanji if kanji.get_PrimaryVocab()]
    for kanji in kanji_with_vocab:
        kanji_vocab = kanji_vocab_dict[kanji.get_kanji()]
        primary_vocabs: List[str] = [StringUtils.strip_markup(vocab).strip() for vocab in kanji.get_PrimaryVocab().split(",")]
        if len(primary_vocabs) > 0:
            found_vocab: list[WaniVocabNote] = list[WaniVocabNote]()
            vocab_to_vocab: dict[str, WaniVocabNote] = {vo.get_vocab(): vo for vo in kanji_vocab}
            reading_to_vocab: dict[str, WaniVocabNote] = dict[str, WaniVocabNote]()

            for vocab in kanji_vocab:
                for reading in vocab.get_reading_list():
                    reading_to_vocab[reading] = vocab

            for vocab in primary_vocabs:
                if vocab in vocab_to_vocab:
                    found_vocab.append(vocab_to_vocab[vocab])
                elif vocab in reading_to_vocab:
                    found_vocab.append(reading_to_vocab[vocab])

            if len(found_vocab) > 0:
                audios = "".join([vo.get_audios() for vo in found_vocab])
                kanji.set_PrimaryVocabAudio(audios)

    tooltip("done")

