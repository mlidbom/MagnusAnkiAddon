from typing import *

from aqt.utils import tooltip

from .utils import StringUtils
from .wani_collection import WaniCollection
from .wanikani_note import *

def update_vocab_kani_names() -> None:
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

    all_vocabulary: list[WaniVocabNote] = WaniCollection.fetch_all_vocab_notes()
    all_kanji: list[WaniKanjiNote] = WaniCollection.fetch_all_kanji_notes()

    update_kanji_names(all_vocabulary, all_kanji)
    tooltip("done")

def update_kanji_vocab_List():
    def generate_vocab_html_list(vocabs: List[WaniVocabNote]):
        newline = "\n"
        vocab_html = f'''
                <div class="vocabList">
                    <div>
                    
                    {newline.join([f"""
                    <div class="vocabEntry">
                        <span class="clipboard">{vocab.get_vocab()}</span>
                        (<span class="vocabReading">{vocab.get_reading()}</span>)
                        <span class="vocabListMeaning"> {StringUtils.strip_markup(vocab.get_vocab_meaning())}</span>
                    </div>
                    """ for vocab in vocabs])}
                    
                    </div>
                </div>
                '''
        return vocab_html

    def sort_vocab_list(vocabs: List[WaniVocabNote]) -> list[WaniVocabNote]:
        vocabs.sort(key=lambda vocab: (vocab.get_level(), vocab.get_lesson_position()))
        return vocabs

    all_vocabulary: list[WaniVocabNote] = WaniCollection.fetch_all_vocab_notes()
    all_vocabulary = sort_vocab_list(all_vocabulary)# we want a specific order in the kanji entries
    kanji_list = WaniCollection.fetch_all_kanji_notes()
    kanji_dict: Dict[str, WaniKanjiNote]   = {kanji.get_kanji(): kanji for kanji in kanji_list}
    kanji_vocab_dict: Dict[str, List[WaniVocabNote]] = {kanji.get_kanji(): [] for kanji in kanji_list}

    for voc in all_vocabulary:
        for char in voc.get_vocab():
            if char in kanji_vocab_dict:
                kanji_vocab_dict[char].append(voc)

    for kanji, vocabs in kanji_vocab_dict.items():

        html = generate_vocab_html_list(vocabs)
        kanji_dict[kanji].set_vocabs(html)

    tooltip("done")
