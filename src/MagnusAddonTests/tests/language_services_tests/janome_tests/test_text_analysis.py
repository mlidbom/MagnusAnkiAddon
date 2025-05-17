from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from ankiutils import app
from fixtures.collection_factory import inject_anki_collection_with_select_data, inject_empty_anki_collection_with_note_types
from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.sentences.sentence_configuration import SentenceConfiguration
from note.vocabulary.vocabnote import VocabNote

if TYPE_CHECKING:
    from collections.abc import Generator

# noinspection PyUnusedFunction
@pytest.fixture(scope="function")
def setup_collection_with_select_data() -> Generator[None, None, None]:
    with inject_anki_collection_with_select_data(special_vocab=True):
        yield

@pytest.fixture(scope="function")
def setup_empty_collection() -> Generator[None, None, None]:
    with inject_empty_anki_collection_with_note_types():
        yield

@pytest.mark.parametrize("sentence, expected_output", [
    ("走る",
     ["走る"]),
    ("走って",
     ["走る", "て"]),
    ("これをください。",
     ["これ", "を", "くださる", "ください"]),
    ("ハート形",
     ["ハート形", "ハート", "形"]),
    ("私が行きましょう。",
     ["私", "が", "行く", "行き", "ましょう", "ます", "ましょ", "う"]),
    ("１人でいる時間がこれほどまでに長く感じるとは",
     ["１人で", "１人", "１", "人", "で", "いる", "時間", "が", "これほど", "これ", "ほど", "までに", "まで", "に", "長い", "長く", "感じる", "とは", "と", "は"]
     ),
    ("どうやってここを知った。",
     ["どうやって", "どう", "やる", "て", "ここ", "を", "知る", "た"]),
    ("彼の日本語のレベルは私と同じ位だ。",
     ["彼の", "彼", "の", "日本語", "の", "レベル", "は", "私", "と", "同じ位", "同じ", "位", "だ"]),
    ("それなのに 周りは化け物が出ることで有名だと聞き",
     ["それなのに", "周り", "は", "化け物", "が", "出る", "こと", "で", "有名", "だ", "と", "聞く", "聞き"]),
    ("清めの一波", ["清める", "清め", "の", "一波"]),
    ("さっさと傷を清めてこい",
     ["さっさと", "傷", "を", "清める", "て", "くる", "こい"]),
    ("すげえ", ["すげえ", "すげる", "すげ", "え"]),
    ("「コーヒーはいかがですか？」「いえ、結構です。お構いなく。」", ["コーヒー", "は", "いかが", "ですか", "です", "か", "いえる", "いえ", "結構", "です", "お構いなく"]),
    ("解放する", ["解放する", "解放", "する"])
])
def test_identify_words(setup_collection_with_select_data: object, sentence: str, expected_output: list[str]) -> None:
    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    root_words = [w.form for w in analysis.all_words]
    assert root_words == expected_output

@pytest.mark.parametrize("sentence, expected_output", [
    ("言わず", ["言う", "言わ", "ず"]),
    ("しろ", ["しろ"]),
    ("声出したら駄目だからね", ["声", "出す", "たら", "駄目", "だから", "だ", "から", "ね"]),
    ("後で下に下りてらっしゃいね", ["後で", "下に", "下", "に", "下りる", "て", "らっしゃい", "ね"]),
    ("無理して思い出す", ["無理", "して", "する", "て", "思い出す"])
])
def test_excluded_surfaces(setup_collection_with_select_data: object, sentence: str, expected_output: list[str]) -> None:
    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    root_words = [w.form for w in analysis.all_words]
    assert root_words == expected_output

@pytest.mark.parametrize("sentence, custom_words, expected_output", [
    ("彼の日本語のレベルは私と同じ位だ。",
     ["彼の日本語", "日本語のレベル"],
     ["彼", "彼の", "彼の日本語", "の", "日本語", "日本語のレベル", "レベル", "は", "私", "と", "同じ", "同じ位", "位", "だ"]
     )
])
def test_custom_vocab_words(setup_collection_with_select_data: object, sentence: str, custom_words: list[str], expected_output: list[str]) -> None:
    insert_custom_words(custom_words)

    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    root_words = {w.form for w in analysis.all_words}
    assert root_words == set(expected_output)

def test_ignores_noise_characters(setup_collection_with_select_data: object) -> None:
    sentence = ". , : ; / | 。 、ー ? !"
    expected = {"ー"}

    analysis = TextAnalysis(sentence, SentenceConfiguration.empty())
    words = {w.form for w in analysis.all_words}
    assert words == expected

def insert_custom_words(custom_words: list[str]) -> None:
    for custom_word in custom_words:
        VocabNote.factory.create(custom_word, "", [""])
    app.col().flush_cache_updates()

@pytest.mark.parametrize("sentence, custom_words, excluded, expected_output, expected_display_output", [
    ("厳密に言えば　俺一人が友達だけど", [],
     [],
     ["厳密に言えば", "俺", "一人", "が", "友達", "だけど"], []),
    ("厳密に言えば　俺一人が友達だけど", [],
     [WordExclusion.global_("厳密に言えば"), WordExclusion.global_("言え"), WordExclusion.global_("だけど")],
     ["厳密", "に", "言う", "ば", "俺", "一人", "が", "友達", "だ", "けど"], []),
    ("厳密に言えば　俺一人が友達だけどだけど", [],
     [],
     ["厳密に言えば", "俺", "一人", "が", "友達", "だけど", "だけど"], []),
    ("厳密に言えばだけど俺一人が友達だけど", [],
     [WordExclusion.at_index("だけど", 6)],
     ["厳密に言えば", "俺", "一人", "が", "友達", "だけど"], []),
    ("幼すぎて よく覚えていないけど", [],
     [],
     ["幼い", "すぎる", "て", "よく", "覚える", "て", "いる", "ない", "けど"], []),
    ("私は毎日ジョギングをすることを習慣にしています。",
     ["してい", "ている", "にする"],
     [WordExclusion.at_index("にして", 17), WordExclusion.at_index("にし", 17), WordExclusion.at_index("して", 18), WordExclusion.at_index("し", 18), WordExclusion.at_index("してい", 18), WordExclusion.at_index("い", 12), WordExclusion.global_("にする")],
     ["私", "は", "毎日", "ジョギング", "を", "する", "こと", "を", "習慣", "に", "する", "ている", "ます"], []),
    ("私は毎日ジョギングをすることを習慣にしています。",
     ["してい", "ている", "にする"],
     [WordExclusion.at_index("にして", 17), WordExclusion.at_index("にし", 17), WordExclusion.at_index("して", 18), WordExclusion.at_index("し", 18), WordExclusion.at_index("してい", 18)],
     ["私", "は", "毎日", "ジョギング", "を", "する", "こと", "を", "習慣", "にする", "ている", "ます"], []),
    ("ばら撒かれるなんて死んでもいやだ",
     [],
     [],
     ["ばら撒く", "あれる", "なんて", "死んでも", "いや", "だ"], ["ばら撒く", "あれる", "なんて", "死んでも", "いや", "だ"]),
    ("ああもう　だったら普通に金貸せって言えよ",
     [],
     [],
     ["ああ", "もう", "だったら", "普通に", "金貸", "せる", "て", "言える", "言えよ"], []),
    ("お前も色々考えてるんだなぁ",
     [],
     [],
     ["お前", "も", "色々", "考える", "てる", "んだ", "なぁ"], []),
    ("教科書落ちちゃうから",
     [],
     [],
     ["教科書", "落ちる", "ちゃう", "から"], []),
    ("待ってました", [], [], ["待つ", "て", "ます", "た"], []),
    ("怖くなくなったの", [], [], ["怖い", "なくなる", "た", "の"], []),
    ("落ちてないかな", [], [], ["落ちる", "てる", "ないか", "な"], []),
    ("分かってたら", [], [], ["分かる", "てたら"], []),
    ("頑張れたというか", [], [WordExclusion.global_("頑張れ")], ["頑張る", "える", "た", "というか"], []),
    ("思い出せそうな気がする", [], [], ["思い出す", "える", "そうだ", "気がする"], []),
    ("私が頼んだの", [], [], ["私", "が", "頼む", "頼ん", "だ", "の"], []),
    ("いらっしゃいません", [], [WordExclusion.global_("いらっしゃいませ")], ["いらっしゃいます", "ん"], []),
    ("代筆を頼みたいんだが", [], [], ["代筆", "を", "頼む", "頼み", "たい", "んだ", "が"], []),
    ("飛ばされる", [], [], ["飛ばす", "あれる"], ["飛ばす", "あれる"]),
    ("食べれる", [], [], ["食べる", "えれる"], ["食べる", "えれる"]),
    ("破られたか", [], [], ["破る", "あれる", "たか"], ["破る", "あれる", "たか"]),
    ("大家族だもの", [], [], ["大家族", "だもの"], []),
    ("奪うんだもの", [], [], ["奪う", "んだ", "もの"], [])
])
def test_hierarchical_extraction(setup_collection_with_select_data: object, sentence: str, custom_words: list[str], excluded: list[WordExclusion], expected_output: list[str], expected_display_output: list[str]) -> None:
    _run_assertions(sentence, custom_words, excluded, expected_output, expected_display_output)

@pytest.mark.parametrize("sentence, custom_words, excluded, expected_output, expected_display_output", [
    ("会える", [], [], ["会える"], []),
    ("会える", [], [WordExclusion.global_("会える")], ["会う", "える"], []),
    ("会えて", [], [WordExclusion.global_("会える")], ["会う", "える", "て"], []),
    ("作れる", [], [], ["作れる"], []),
    ("作れる", [], [WordExclusion.global_("作れる")], ["作る", "える"], []),
    ("作れて", [], [], ["作れる", "て"], []),
    ("作れて", [], [WordExclusion.global_("作れる")], ["作る", "える", "て"], []),
    ("今日会えた", [], [], ["今日", "会える", "た"], []),
    ("今日会えた", [], [WordExclusion.global_("会える")], ["今日", "会う", "える", "た"], []),
    ("今日会えないかな", [], [], ["今日", "会える", "ないか", "な"], []),
    ("今日会えないかな", [], [WordExclusion.global_("会える")], ["今日", "会う", "えない", "かな"], []),
    ("この夏は　たくさん思い出を作れたなぁ", [], [], ["この", "夏", "は", "たくさん", "思い出", "を", "作れる", "た", "なぁ"], []),
])
def test_potential_verb_splitting_with_vocab(setup_collection_with_select_data: object, sentence: str, custom_words: list[str], excluded: list[WordExclusion], expected_output: list[str], expected_display_output: list[str]) -> None:
    _run_assertions(sentence, custom_words, excluded, expected_output, expected_display_output)

@pytest.mark.parametrize("sentence, custom_words, excluded, expected_output, expected_display_output", [
    ("会える", [], [], ["会う", "える"], []),
    ("会える", [], [WordExclusion.global_("会える")], ["会う", "える"], []),
    ("会えて", [], [WordExclusion.global_("会える")], ["会う", "える", "て"], []),
    ("作れる", [], [], ["作る", "える"], []),
    ("作れる", [], [WordExclusion.global_("作れる")], ["作る", "える"], []),
    ("作れて", [], [], ["作る", "える", "て"], []),
    ("作れて", [], [WordExclusion.global_("作れる")], ["作る", "える", "て"], []),
    ("今日会えた", [], [], ["今日", "会う", "える", "た"], []),
    ("今日会えた", [], [WordExclusion.global_("会える")], ["今日", "会う", "える", "た"], []),
    ("今日会えないかな", [], [], ["今日", "会う", "える", "ないか", "な"], []),
    ("今日会えないかな", [], [WordExclusion.global_("会える")], ["今日", "会う", "える", "ないか", "な"], []),
    ("この夏は　たくさん思い出を作れたなぁ", [], [], ["この", "夏", "は", "たくさん", "思い出", "を", "作る", "える", "た", "なぁ"], []),
    ("買えよ　私", [], [], ["買える", "買えよ", "私"], []),
    ("覚ませない", [], [], ["覚ます", "える", "ない"], [])
])
def test_potential_verb_splitting_without_vocab(setup_empty_collection: object, sentence: str, custom_words: list[str], excluded: list[WordExclusion], expected_output: list[str], expected_display_output: list[str]) -> None:
    _run_assertions(sentence, custom_words, excluded, expected_output, expected_display_output)

def _run_assertions(sentence: str, custom_words: list[str], excluded: list[WordExclusion], expected_output: list[str], expected_display_output: list[str]) -> None:
    insert_custom_words(custom_words)
    analysis = TextAnalysis(sentence, SentenceConfiguration.from_incorrect_matches(excluded))
    root_words = [w.form for w in analysis.display_words]
    assert root_words == expected_output
    display_words_forms = [dw.parsed_form for dw in analysis.display_forms]
    if expected_display_output:
        assert display_words_forms == expected_display_output
    else:
        assert display_words_forms == expected_output