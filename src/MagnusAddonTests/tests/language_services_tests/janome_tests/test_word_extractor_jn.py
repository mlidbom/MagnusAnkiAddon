from typing import Generator

import pytest

from fixtures.collection_factory import inject_anki_collection_with_select_data
from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from language_services.janome_ex.word_extraction.text_analysis import TextAnalysis
from language_services.janome_ex.word_extraction.word_extractor import jn_extractor
from language_services.janome_ex.word_extraction.word_exclusion import WordExclusion
from note.vocabnote import VocabNote

_tokenizer: JNTokenizer

word_extractor = jn_extractor

# noinspection PyUnusedFunction
@pytest.fixture(scope='module', autouse=True)
def setup() -> None:
    global _tokenizer
    _tokenizer = JNTokenizer()

# noinspection PyUnusedFunction
@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_anki_collection_with_select_data(special_vocab=True):
        yield

@pytest.mark.parametrize('sentence, expected_output', [
    ("走る",
     ['走る']),
    ("走って",
     ['走る', 'て']),
    ("これをください。",
     ['これ', 'を', 'くださる', 'ください']),
    ("ハート形",
     ['ハート', 'ハート形', '形']),
    ("私が行きましょう。",
     ['私', 'が', '行く', '行き', 'ます', 'ましょ', 'ましょう', 'う']),
    ("１人でいる時間がこれほどまでに長く感じるとは",
     ['１', '１人', '１人で', '人', 'で', 'いる', '時間', 'が', 'これ', 'これほど', 'ほど', 'まで', 'までに', 'に', '長い', '長く', '感じる', 'と', 'とは', 'は']),
    ("どうやってここを知った。",
     ['どう', 'どうやって', 'やる', 'て', 'ここ', 'を', '知る', 'た']),
    ("声出したら駄目だからね",
     ['声', '出す', 'たら', '駄目', 'だ', 'だから', 'から', 'ね']
     ),
    ("彼の日本語のレベルは私と同じ位だ。",
     ['彼', '彼の', 'の', '日本語', 'レベル', 'は', '私', 'と', '同じ', '同じ位', '位', 'だ']),
    ("それなのに 周りは化け物が出ることで有名だと聞き",
     ['それなのに', '周り', 'は', '化け物', 'が', '出る', 'こと', 'で', '有名', 'だ', 'と', '聞く', '聞き']),
    ("清めの一波", ['清める', '清め', 'の', '一波']),
    ("さっさと傷を清めてこい",
     ['さっさと', '傷', 'を', '清める', 'て', 'くる', 'こい'])
])
def test_identify_words(sentence: str, expected_output: list[str]) -> None:
    result = [w.word for w in word_extractor.extract_words(sentence)]

    assert result == expected_output

@pytest.mark.parametrize('sentence, custom_words, expected_output', [
    ("彼の日本語のレベルは私と同じ位だ。",
     ["彼の日本語", "日本語のレベル"],
     ['彼', '彼の', '彼の日本語', 'の', '日本語', '日本語のレベル', 'レベル', 'は', '私', 'と', '同じ', '同じ位', '位', 'だ']
     )
])
def test_custom_vocab_words(sentence: str, custom_words: list[str], expected_output: list[str]) -> None:
    insert_custom_words(custom_words)
    result = [w.word for w in word_extractor.extract_words(sentence)]
    assert result == expected_output

def test_ignores_noise_characters() -> None:
    result = word_extractor.extract_words(". , : ; / | 。 、 ー")
    assert len(result) == 1
    assert result[0].word == "ー"

def test_something() -> None:
    result = word_extractor.extract_words("知ってる人があんまりいない高校に行って")
    print(result)

def insert_custom_words(custom_words: list[str]) -> None:
    from ankiutils import app
    for custom_word in custom_words:
        VocabNote.create(custom_word, "", [""])
    app.col().flush_cache_updates()

@pytest.mark.parametrize('run_text_analysis_test_version, sentence, custom_words, excluded, expected_output', [
    (True, "厳密に言えば　俺一人が友達だけど", [],
     [],
     ["厳密に言えば", "俺", "一人", "が", "友達", "だけど"]),
    (False, "厳密に言えば　俺一人が友達だけど", [],
     [WordExclusion("厳密に言えば"), WordExclusion("言え"), WordExclusion('だけど')],
     ['厳密', 'に', '言う', 'ば', '俺', '一人', 'が', '友達', 'だ', 'けど']),
    (True, "厳密に言えば　俺一人が友達だけどだけど", [],
     [],
     ['厳密に言えば', '俺', '一人', 'が', '友達', 'だけど', 'だけど']),
    (False, "厳密に言えばだけど俺一人が友達だけど", [],
     [WordExclusion("だけど", 6)],
     ['厳密に言えば', '俺', '一人', 'が', '友達', 'だけど']),
    (True, "幼すぎて よく覚えていないけど", [],
     [],
     ['幼い', 'すぎる', 'て', 'よく', '覚える', 'て', 'いる', 'ない', 'けど']
     ),
    (False, "私は毎日ジョギングをすることを習慣にしています。",
     ["してい", "ている", "にする"],
     [WordExclusion("にして", 17), WordExclusion("にし", 17), WordExclusion("して", 18), WordExclusion("し", 18), WordExclusion("してい", 18), WordExclusion("い", 12), WordExclusion("にする")],
     ['私', 'は', '毎日', 'ジョギング', 'を', 'する', 'こと', 'を', '習慣', 'に', 'する', 'ている', 'ます']),
    (False, "私は毎日ジョギングをすることを習慣にしています。",
     ["してい", "ている", "にする"],
     [WordExclusion("にして", 17), WordExclusion("にし", 17), WordExclusion("して", 18), WordExclusion("し", 18), WordExclusion("してい", 18)],
     ['私', 'は', '毎日', 'ジョギング', 'を', 'する', 'こと', 'を', '習慣', 'にする', 'ている', 'ます']),
    (True, "ばら撒かれるなんて死んでもいやだ",
     [],
     [],
     ['ばら撒く', 'れる', 'なんて', '死んでも', 'いや', 'だ']),
    (False, "ああもう　だったら普通に金貸せって言えよ",
     [],
     [],
     ['ああ', 'もう', 'だったら', '普通に', '金貸', 'せる', 'て', '言える', '言えよ']),
    (True, "お前も色々考えてるんだなぁ",
     [],
     [],
     ['お前', 'も', '色々', '考える', 'てる', 'んだ', 'なぁ']),
    (False, "この夏は　たくさん思い出を作れたなぁ",
     [],
     [],
     ['この', '夏', 'は', 'たくさん', '思い出', 'を', '作れる', 'た', 'なぁ']),
    (True, "教科書落ちちゃうから",
     [],
     [],
     ['教科書', '落ちる', 'ちゃう', 'から']),
    (True, "待ってました", [], [], ['待つ', 'て', 'ます', 'た']),
    (False, "怖くなくなったの", [], [], ['怖い', 'なくなる', 'た', 'の']),
    (False, "落ちてないかな", [], [], ['落ちる', 'てる', 'ないか', 'な']),
    (False, "分かってたら", [], [], ['分かる', 'てたら']),
    (False, "頑張れたというか", [], [], ['頑張れる', 'た', 'というか']),
    (False, "思い出せそうな気がする", [], [], ['思い出せる', 'そう', 'な', '気がする']),
    (False, "私が頼んだの", [], [], ['私', 'が', '頼む', '頼ん', 'だ', 'の']),
    (False, "いらっしゃいません", [], [WordExclusion('いらっしゃいませ')], ['いらっしゃいます', 'ん'])
])
def test_hierarchical_extraction(run_text_analysis_test_version:bool, sentence: str, custom_words: list[str], excluded: list[WordExclusion], expected_output: list[str]) -> None:
    print("")
    print("###### running test")
    insert_custom_words(custom_words)
    hierarchical = word_extractor.extract_words_hierarchical(sentence, excluded)
    root_words = [w.word.word for w in hierarchical]
    assert root_words == expected_output

    if run_text_analysis_test_version:
        analysis = TextAnalysis(sentence, excluded)
        root_words = [w.form for w in analysis.display_words]
        assert root_words == expected_output

def insert_custom_words_with_excluded_forms(custom_words: list[list[str]]) -> None:
    from ankiutils import app
    for custom_word in custom_words:
        note = VocabNote.create(custom_word[0], "", [""])
        note.set_forms(set(custom_word))
    app.col().flush_cache_updates()

@pytest.mark.parametrize('sentence, custom_words, expected_output', [
    ("後で下に下りてらっしゃいね",
     [["らっしゃい", "[[らっしゃる]]"]],
     ['後で', '下', '下に', 'に', '下りる', 'て', 'らっしゃい', 'ね']),
    ("無理して思い出す",
     [["する", "[[し]]"]],
     ['無理', 'する', 'して', 'て', '思い出す']),
    ("リセットしても",
     [["する", "[[し]]", "[[して]]"]],
     ['リセット', 'する', 'て', 'ても', 'も'],)
])
def test_custom_vocab_words_with_excluded_forms(sentence: str, custom_words: list[list[str]], expected_output: list[str]) -> None:
    insert_custom_words_with_excluded_forms(custom_words)
    result = [w.word for w in word_extractor.extract_words(sentence)]
    assert result == expected_output
