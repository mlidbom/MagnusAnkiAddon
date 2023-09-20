from ankiutils import search_utils
from note.sentencenote import SentenceNote
from note.wanivocabnote import WaniVocabNote
from parsing import textparser
from sysutils.utils import StringUtils, ListUtils
from wanikani.wani_collection import WaniCollection

_ignored_tokens: set[str] = set("しもよかとたてでをなのにだがは")
_ignored_vocab: set[str] = {"擦る"}


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

    tokens = textparser.identify_words(sentence.get_active_question())

    user_excluded = sentence.get_user_excluded_vocab()
    excluded = user_excluded | _ignored_vocab

    tokens = [token for token in tokens if token.word not in excluded]

    queries = [search_utils.vocab_lookup(parsed) for parsed in tokens]
    user_extras_queries = [search_utils.single_vocab_exact(word) for word in sentence.get_user_extra_vocab()]
    queries = user_extras_queries + queries
    notes = [WaniCollection.search_vocab_notes(word) for word in queries]

    vocabs_flattened: list[WaniVocabNote] = ListUtils.flatten_list(notes)
    vocabs_flattened = [word for word in vocabs_flattened if word.get_question() not in excluded]

    if len(vocabs_flattened) > 10:  # Having it in order is nice for shorter sentences, but painful for long ones
        low_priority = [vocab for vocab in vocabs_flattened if vocab.get_question() in _ignored_tokens]
        high_priority = [vocab for vocab in vocabs_flattened if vocab.get_question() not in _ignored_tokens]
        vocabs_flattened = high_priority + low_priority

    html = build_html(vocabs_flattened)
    sentence.set_break_down(html)