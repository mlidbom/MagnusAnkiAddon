import threading
from contextlib import contextmanager
from typing import Generator
from ankiutils import app
from ankiutils.ui_utils_interface import UIUtilsInterface
from fixtures.stubs.ui_utils_stub import UIUtilsStub
from sysutils.typed import checked_cast

_thread_local = threading.local()


def get_thread_local_ui_utils() -> UIUtilsInterface:
    return checked_cast(UIUtilsStub, _thread_local.ui_utils)


@contextmanager
def stub_ui_utils() -> Generator[None, None, None]:
    _thread_local.ui_utils = UIUtilsStub()
    app.ui_utils = get_thread_local_ui_utils
    yield
