from __future__ import annotations

import threading
from contextlib import contextmanager
from typing import TYPE_CHECKING

from jastudio.ankiutils import app
from jastudio_tests.fixtures.stubs.ui_utils_stub import UIUtilsStub
from sysutils import progress_display_runner
from sysutils.typed import checked_cast

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator

    from jastudio.ankiutils.ui_utils_interface import IUIUtils

_thread_local = threading.local()

def get_thread_local_ui_utils() -> IUIUtils:
    return checked_cast(UIUtilsStub, _thread_local.ui_utils)  # pyright: ignore[reportAny]

@contextmanager
def _stub_ui_utils_real() -> Iterator[None]:
    _thread_local.ui_utils = UIUtilsStub()
    app.get_ui_utils = get_thread_local_ui_utils
    yield

@contextmanager
def stub_ui_dependencies() -> Iterator[None]:
    with (_stub_ui_utils_real(), _stub_progress_runner()):
        yield

@contextmanager
def _stub_progress_runner() -> Iterator[None]:
    # noinspection PyUnusedLocal
    def _process_with_progress[T](items: list[T], process_item: Callable[[T], None], _message: str, _allow_cancel: bool = True, _display_delay_seconds: float = 0.0, _pause_cache_updates: bool = True, _run_gc:bool = False) -> None:
        for item in items:
            process_item(item)

    progress_display_runner.process_with_progress = _process_with_progress

    yield
