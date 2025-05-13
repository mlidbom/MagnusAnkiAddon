from __future__ import annotations

import threading
from contextlib import contextmanager
from typing import TYPE_CHECKING, Any, Callable, TypeVar

from ankiutils import app
from fixtures.stubs.ui_utils_stub import UIUtilsStub
from language_services.jamdict_ex import dict_lookup
from sysutils import progress_display_runner
from sysutils.lazy import Lazy
from sysutils.progress_display_runner import Closable
from sysutils.typed import checked_cast

if TYPE_CHECKING:
    from collections.abc import Generator

    from ankiutils.ui_utils_interface import IUIUtils

_thread_local = threading.local()


def get_thread_local_ui_utils() -> IUIUtils:
    return checked_cast(UIUtilsStub, _thread_local.ui_utils)


@contextmanager
def _stub_ui_utils_real() -> Generator[None, None, None]:
    _thread_local.ui_utils = UIUtilsStub()
    app.get_ui_utils = get_thread_local_ui_utils
    yield

@contextmanager
def _stub_dict_optimizations() -> Generator[None, None, None]:
    dict_lookup.is_unit_testing_mode = True
    yield

@contextmanager
def _stub_config_dict() -> Generator[None, None, None]:
    _config_dict:dict[str,Any] = dict()

    from configuration import configuration_value

    def _write_config_dict() -> None: pass

    configuration_value._config_dict = Lazy(lambda: _config_dict)
    configuration_value._write_config_dict = _write_config_dict

    yield

@contextmanager
def stub_ui_dependencies() -> Generator[None, None, None]:
    with (_stub_ui_utils_real(), _stub_progress_runner(), _stub_config_dict(), _stub_dict_optimizations()):
        yield

T = TypeVar('T')
@contextmanager
def _stub_progress_runner() -> Generator[None, None, None]:
    # noinspection PyUnusedLocal
    def _open_spinning_progress_dialog(message: str) -> Closable:
        return Closable(lambda: None)

    # noinspection PyUnusedLocal
    def _process_with_progress(items: list[T], process_item: Callable[[T], None], message:str, allow_cancel: bool = True, display_delay_seconds: float = 0.0, pause_cache_updates: bool = True) -> None:
        for item in items:
            process_item(item)

    progress_display_runner.open_spinning_progress_dialog = _open_spinning_progress_dialog
    progress_display_runner.process_with_progress = _process_with_progress

    yield
