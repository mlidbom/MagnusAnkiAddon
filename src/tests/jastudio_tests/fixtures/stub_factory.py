from __future__ import annotations

import threading
from contextlib import contextmanager
from typing import TYPE_CHECKING

from jaspythonutils.sysutils.typed import checked_cast
from jastudio.ankiutils import app
from jastudio_tests.fixtures.stubs.ui_utils_stub import UIUtilsStub

if TYPE_CHECKING:
    from collections.abc import Iterator

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
    with (_stub_ui_utils_real()):
        yield
