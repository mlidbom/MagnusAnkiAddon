from typing import Generator
import pytest
from ankiutils import search_utils
from fixtures.full_test_collection_factory import inject_full_anki_collection_for_testing
from ankiutils import app
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import kana_utils, listutils
from sysutils.stringutils import StringUtils

shtml = StringUtils.strip_html_markup

@pytest.fixture(scope="function", autouse=True)
def setup() -> Generator[None, None, None]:
    with (inject_full_anki_collection_for_testing()):
        yield

_sentences = ["今じゃ町は夜でも明るいしもう会うこともないかもな",
              "食べてもいいけど",
              "いるのにキス",
              "聞かなかったことにしてあげる",
              "ごめん　自分から誘っといて ちゃんと調べておけばよかった",
              "探しているんですか",
              "ダメダメ私を助けて",
              "いつまでも来ないと知らないからね",
              "ついに素晴らしい女性に逢えた。",
              "なかったかな",
              "離れていくよ",
              "夢を見た",
              "言われるまで気づかなかった",
              "行きたい所全部行こう",
              "当てられても",
              "逃げたり",
              "するためでした",
              "ように言ったのも",
              "一度聞いたことがある",
              "友達だから余計に気になっちゃうんだよ",
              "自分のことを知ってもらえてない人に",
              "良かったら",
              "よかったじゃん",
              "言えばよかった",
              "ううん藤宮さんは日記を捨てるような人じゃない",
              "としたら",
              "あいつが話の中に出てくるのが"]

#missing: 逢

su = search_utils
@pytest.mark.skip("Only used to generate test data, so no reason to run this slow code all the time.")
def test_create_sample_data() -> None:
    sentence_notes: list[SentenceNote] = []
    for sentence_text in _sentences:
        matching = app.col().sentences.search(f"{su.note_sentence} {su.question}:*{sentence_text}*")
        with_active_answer = [m for m in matching if m.get_active_answer()]
        sentence_notes += with_active_answer
        for sentence in with_active_answer:
            print(f"""SentenceSpec("{shtml(sentence.get_active_question())}", "{shtml(sentence.get_active_answer())}"),"""),

    needed_vocab_parsed_words = listutils.flatten([s.parse_words_from_expression() for s in sentence_notes])
    need_vocab_strings = set([f.word for f in needed_vocab_parsed_words])
    vocab_notes = listutils.flatten([app.col().vocab.search(su.single_vocab_by_form_exact(word)) for word in need_vocab_strings])

    non_duplicate_vocab_notes:list[VocabNote] = []
    added_words:set[str] = set()
    for candidate in vocab_notes:
        if candidate.get_question() not in added_words:
            added_words.add(candidate.get_question())
            non_duplicate_vocab_notes.append(candidate)

    for vocab in non_duplicate_vocab_notes:
        print(f"""VocabSpec("{vocab.get_question()}", "{vocab.get_active_answer()}", {vocab.get_readings()}),""")

    word_forms = "".join(listutils.flatten([list(n.get_forms()) for n in vocab_notes]))
    sentences_combined = "".join(_sentences)
    big_fat_string = word_forms + sentences_combined
    only_kanji = "".join(char for char in list(big_fat_string) if kana_utils.is_kanji(char))
    search_string = su.kanji_in_string(only_kanji)
    kanji_notes = app.col().kanji.search(search_string)
    for kanji_note in kanji_notes:
        print(f"""KanjiSpec("{shtml(kanji_note.get_question())}", "{shtml(kanji_note.get_active_answer())}", "{shtml(kanji_note.get_reading_kun())}", "{shtml(kanji_note.get_reading_on())}"),"""),
