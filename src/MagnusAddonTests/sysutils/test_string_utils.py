import pytest

from sysutils.utils import StringUtils

@pytest.mark.parametrize('inp, output', [
    ("<div>something</div>", "something"),
    ("<div>something〜</div>", "something〜"),
    ("[aoeu]something〜[aeu]", "something〜")
])
def test_strip_(inp: str, output: str) -> None:
    assert output == StringUtils.strip_markup(inp)

@pytest.mark.parametrize('inp, output', [
    ("<div>something</div>", "something"),
    ("<div>something〜</div>", "something"),
    ("[aoeu]something〜[aeu]", "something")
])
def test_strip_markup(inp: str, output: str) -> None:
    assert output == StringUtils.strip_markup_and_noise_characters(inp)