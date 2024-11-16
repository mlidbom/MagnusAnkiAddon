from typing import Generator

import pytest

from fixtures.collection_factory import inject_empty_anki_collection_with_note_types
from language_services.janome_ex.word_extraction import ud_word_extractor
from note.vocabnote import VocabNote

# noinspection PyUnusedFunction
@pytest.fixture(scope="function", autouse=True)
def setup_object() -> Generator[None, None, None]:
    with inject_empty_anki_collection_with_note_types():
        yield

# noinspection PyUnusedName
pytestmark = pytest.mark.skip(f"""I thought the ud tools would do a better job than janome, but these tests don't seem to bear that thought out. 
Maybe it's time to stop trying do to magic, rip out all the attempts at magic and just use janome and have the user do the rest of the validation""")

@pytest.mark.parametrize('sentence, expected_output', [
    ("走る",
     ['走る']),
    ("走って",
     ['走る', '走っ', 'て']),
    ("これをください。",
     ['これ', 'を', 'くださる', 'ください']),
    ("ハート形",
     ['ハート', 'ハート形', '形']),
    ("私が行きましょう。",
     ['私', 'が', '行く', '行き', 'ます', 'ましょう']),
    ("１人でいる時間がこれほどまでに長く感じるとは",
     ['１', '１人', '１人で', '人', 'で', 'いる', '時間', 'が', 'これ', 'これほど', 'ほど', 'まで', 'までに', 'に', '長い', '長く', '感じる', 'と', 'とは', 'は']),
    ("どうやってここを知った。",
     ['どう', 'どうやって', 'やる', 'やっ', 'て', 'ここ', 'を', '知る', '知っ', 'た']),
    ("声出したら駄目だからね",
     ['声', '出す', '出し', 'た', 'たら', '駄目', 'だ', 'だから', 'から', 'ね']),
    ("彼の日本語のレベルは私と同じ位だ。",
     ['彼', '彼の', 'の', '日本語', 'レベル', 'は', '私', 'と', '同じ', '同じ位', '位', 'だ'])
])
def test_identify_words(sentence: str, expected_output: list[str]) -> None:
    result = ud_word_extractor.extract_words(sentence)
    assert result == expected_output

@pytest.mark.parametrize('sentence, custom_words, expected_output', [
    ("彼の日本語のレベルは私と同じ位だ。",
     ["彼の日本語", "日本語のレベル"],
     ['彼', '彼の', '彼の日本語', 'の', '日本語', '日本語のレベル', 'レベル', 'は', '私', 'と', '同じ', '同じ位', '位', 'だ']
     )
])
def test_custom_vocab_characters(sentence: str, custom_words:list[str], expected_output: list[str]) -> None:
    from ankiutils import app

    for custom_word in custom_words:
        VocabNote.create(custom_word, "", [""])

    app.col().flush_cache_updates()
    result = ud_word_extractor.extract_words(sentence)
    assert result == expected_output

def test_ignores_noise_characters() -> None:
    result = ud_word_extractor.extract_words(". , : ; / | 。 、 ー")
    assert result == ["ー"]

def test_something() -> None:
    result = ud_word_extractor.extract_words("知ってる人があんまりいない高校に行って")
    print(result)
