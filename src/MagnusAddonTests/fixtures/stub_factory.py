import threading
from contextlib import contextmanager
from typing import Callable, Generator, List, TypeVar
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
def _stub_ui_utils_real() -> Generator[None, None, None]:
    _thread_local.ui_utils = UIUtilsStub()
    app.ui_utils = get_thread_local_ui_utils
    yield

@contextmanager
def stub_ui_dependencies() -> Generator[None, None, None]:
    with (_stub_ui_utils_real(), _stub_progress_runner()):
        yield

@contextmanager
def _stub_progress_runner() -> Generator[None, None, None]:
    # noinspection PyUnusedLocal
    def _open_spinning_progress_dialog(message: str) -> Closable:
        return Closable(lambda: None)

    t = TypeVar('t')

    # noinspection PyUnusedLocal
    def _process_with_progress(items: List[t], process_item: Callable[[t], None], message: str, allow_cancel: bool = True, delay_display: bool = False, pause_cache_updates: bool = True) -> None:
        for item in items:
            process_item(item)

    progress_display_runner.open_spinning_progress_dialog = _open_spinning_progress_dialog
    progress_display_runner.process_with_progress = _process_with_progress

    yield
