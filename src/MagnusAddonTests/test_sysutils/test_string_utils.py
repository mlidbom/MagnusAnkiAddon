import pytest

from sysutils.stringutils import StringUtils

@pytest.mark.parametrize('inp, output', [
    ("<div>something</div>", "something"),
    ("<div>something〜</div>", "something〜"),
    ("[bah]something〜[aeu]", "something〜")
])
def test_strip_(inp: str, output: str) -> None:
    assert output == StringUtils.strip_html_and_bracket_markup(inp)

@pytest.mark.parametrize('inp, output', [
    ("<div>something</div>", "something"),
    ("<div>something〜</div>", "something"),
    ("[bah]something〜[aeu]", "something")
])
def test_strip_markup(inp: str, output: str) -> None:
    assert output == StringUtils.strip_html_and_bracket_markup_and_noise_characters(inp)