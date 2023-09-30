import pytest

from sysutils import my_clipboard


@pytest.mark.skip("Messing up the clipboard content constantly is no fun")
def test_clipboard_read_write() -> None:
    text = "something"
    my_clipboard.set_text(text)

    assert my_clipboard.get_text() == text