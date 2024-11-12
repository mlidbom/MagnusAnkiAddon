from typing import Generator

import pytest

from fixtures.collection_factory import inject_empty_anki_collection_with_note_types
from language_services.janome_ex.tokenizing.jn_tokenizer import JNTokenizer
from language_services.janome_ex.word_extraction import word_extractor
from language_services.janome_ex.word_extraction.word_extractor import WordExclusion
from note.vocabnote import VocabNote

_tokenizer: JNTokenizer

@pytest.fixture(scope='module', autouse=True)
def setup() -> None:
    global _tokenizer
    _tokenizer = JNTokenizer()

@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_empty_anki_collection_with_note_types():
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
     ['声', '出す', '出し', 'た', 'たら', '駄目', 'だ', 'だから', 'から', 'ね']),
    ("彼の日本語のレベルは私と同じ位だ。",
     ['彼', '彼の', 'の', '日本語', 'レベル', 'は', '私', 'と', '同じ', '同じ位', '位', 'だ']),
    ("それなのに 周りは化け物が出ることで有名だと聞き",
     ['それなのに', '周り', 'は', '化け物', 'が', '出る', 'こと', 'で', '有名', 'だ', 'と', '聞く', '聞き']),
    ("清めの一波", ['清める', '清め', 'の', '一波']),
    ("さっさと傷を清めてこい", ['さっさと', '傷', 'を', '清める', '清め', 'て', 'くる', 'こい'])
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
def test_custom_vocab_words(sentence: str, custom_words:list[str], expected_output: list[str]) -> None:
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

def insert_custom_words(custom_words:list[str]) -> None:
    from ankiutils import app
    for custom_word in custom_words:
        VocabNote.create(custom_word, "", [""])
    app.col().flush_cache_updates()


@pytest.mark.parametrize('sentence, custom_words, excluded, expected_output', [
    ("厳密に言えば　俺一人が友達だけど",[],
     [],
     ["厳密に言えば", "俺", "一人", "が", "友達", "だけど"]),
    ("厳密に言えば　俺一人が友達だけど",[],
     [WordExclusion("厳密に言えば"), WordExclusion("言え"), WordExclusion('だけど')],
     ['厳密', 'に', '言う', 'ば', '俺', '一人', 'が', '友達', 'だ', 'けど']),
    ("厳密に言えば　俺一人が友達だけどだけど",[],
     [],
     ['厳密に言えば', '俺', '一人', 'が', '友達', 'だけど', 'だけど']),
    ("厳密に言えばだけど俺一人が友達だけど", [],
     [WordExclusion("だけど", 4)],
     ['厳密に言えば', '俺', '一人', 'が', '友達', 'だけど']),
    ("幼すぎて よく覚えていないけど", [],
     [],
     ['幼い', '幼', 'すぎる', 'すぎ', 'て', 'よく', '覚える', '覚え', 'て', 'いる', 'い', 'ない', 'けど']),
    ("私は毎日ジョギングをすることを習慣にしています。",
     ["してい", "ている", "にする"],
     [WordExclusion("にして", 9), WordExclusion("にし", 9), WordExclusion("して", 10), WordExclusion("し", 10), WordExclusion("してい", 10), WordExclusion("い", 12), WordExclusion("にする")],
     ['私', 'は', '毎日', 'ジョギング', 'を', 'する', 'こと', 'を', '習慣', 'に', 'する', 'ている', 'ます']),
    ("私は毎日ジョギングをすることを習慣にしています。",
     ["してい", "ている", "にする"],
     [WordExclusion("にして", 9), WordExclusion("にし", 9), WordExclusion("して", 10), WordExclusion("し", 10), WordExclusion("してい", 10)],
     ['私', 'は', '毎日', 'ジョギング', 'を', 'する', 'こと', 'を', '習慣', 'にする', 'ている', 'ます'])
])
def test_hierarchical_extraction(sentence: str, custom_words:list[str], excluded:list[WordExclusion], expected_output: list[str]) -> None:
    insert_custom_words(custom_words)
    hierarchical = word_extractor.extract_words_hierarchical(sentence, excluded)
    root_words = [w.word.word for w in hierarchical]
    assert root_words == expected_output
