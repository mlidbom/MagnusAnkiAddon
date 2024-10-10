import threading
from contextlib import contextmanager
from typing import Generator
from ankiutils import app
from ankiutils.ui_utils_interface import IUIUtils
from fixtures.stubs.ui_utils_stub import UIUtilsStub
from sysutils import progress_display_runner
from sysutils.progress_display_runner import Closable
from sysutils.typed import checked_cast

_thread_local = threading.local()


def get_thread_local_ui_utils() -> IUIUtils:
    return checked_cast(UIUtilsStub, _thread_local.ui_utils)


@contextmanager
def stub_ui_utils() -> Generator[None, None, None]:
    _thread_local.ui_utils = UIUtilsStub()
    app.ui_utils = get_thread_local_ui_utils
    yield

@contextmanager
def stub_progress_runner() -> Generator[None, None, None]:

    def _open_spinning_progress_dialog(message: str) -> Closable:
        print("#####################HELLLOOOOOO######################")
        return Closable(lambda: None)

    progress_display_runner.open_spinning_progress_dialog = _open_spinning_progress_dialog

    yield
