import pytest
from sysutils import ex_str


@pytest.mark.parametrize('inp, output', [
    ("<div>something</div>", "something"),
    ("<div>something〜</div>", "something〜"),
    ("[bah]something〜[aeu]", "something〜")
])
def test_strip_(inp: str, output: str) -> None:
    assert output == ex_str.strip_html_and_bracket_markup(inp)

@pytest.mark.parametrize('inp, output', [
    ("<div>something</div>", "something"),
    ("<div>something〜</div>", "something"),
    ("[bah]something〜[aeu]", "something")
])
def test_strip_markup(inp: str, output: str) -> None:
    assert output == ex_str.strip_html_and_bracket_markup_and_noise_characters(inp)

@pytest.mark.parametrize('inp, replacement, output', [
    ("""<div style="text-align: left;" class="yomitan-glossary"><ol><li>to quell (uprising, rebellion, etc.) to punish (another nation, etc.) by force of arms</li><li>sound</li><li>voice</li><li>tone</li></ol></div>""",
     "/",
     "///to quell (uprising, rebellion, etc.) to punish (another nation, etc.) by force of arms//sound//voice//tone///")
])
def test_replace_markup(inp: str, replacement: str, output: str) -> None:
    assert output == ex_str.replace_html_and_bracket_markup_with(inp, replacement)
