import win32clipboard


def get_text() -> str:
    try:
        win32clipboard.OpenClipboard()
        try:
            clipboard_content = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            return clipboard_content
        finally:
            win32clipboard.CloseClipboard()
    except: # noqa
        pass  # Occasionally this code randomly fails. Let's not have that result in a crash of the addon OK?

    return ""

def set_text(text) -> None:
    try:
        win32clipboard.OpenClipboard()
        try:
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
            win32clipboard.CloseClipboard()
        finally:
            win32clipboard.CloseClipboard()
    except: # noqa
        pass  # Occasionally this code randomly fails. Let's not have that result in a crash of the addon OK?
