from ankiutils import search_utils
from note.sentencenote import SentenceNote
from note.wanivocabnote import WaniVocabNote
from parsing import textparser
from sysutils.utils import StringUtils, ListUtils
from wanikani import wani_collection
from wanikani.wani_collection import WaniCollection


def build_breakdown_html(sentence: SentenceNote) -> None:
    def build_html(vocab_list: list[WaniVocabNote]) -> str:
        return f'''
    <div class="sentenceVocabList">
        <div>
    
        {StringUtils.newline().join([f"""
        <div class="sentenceVocabEntry">
            <span class="vocabQuestion clipboard">{vocab.get_question()}</span>
            <span class="vocabAnswer">{vocab.get_active_answer()}</span>
        </div>
        """ for vocab in vocab_list])}
    
        </div>
    </div>
'''

    top_level_words = textparser.identify_words(sentence.get_active_question())
    top_level_queries = [search_utils.vocab_lookup(parsed) for parsed in top_level_words]
    top_level_word_notes = [WaniCollection.search_vocab_notes(word) for word in top_level_queries]
    top_level_word_notes_flattened = ListUtils.flatten_list(top_level_word_notes)
    html = build_html(top_level_word_notes_flattened)
    sentence.set_break_down(html)

