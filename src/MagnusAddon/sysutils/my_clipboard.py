import win32clipboard  # type: ignore

from sysutils.typed import checked_cast


def get_text() -> str:
    try:
        win32clipboard.OpenClipboard()
        try:
            clipboard_content = win32clipboard.GetClipboardData()
            return checked_cast(str, clipboard_content)
        finally:
            win32clipboard.CloseClipboard()
    except: # noqa
        pass  # Occasionally this code randomly fails. Let's not have that result in a crash of the addon OK?

    return ""

def set_text(text:str) -> None:
    try:
        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
        finally:
            win32clipboard.CloseClipboard()
    except: # noqa
        pass  # Occasionally this code randomly fails. Let's not have that result in a crash of the addon OK?
