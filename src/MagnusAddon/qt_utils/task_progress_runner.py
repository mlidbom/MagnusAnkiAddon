from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots
from qt_utils.invisible_task_progress_runner import InvisibleTaskRunner
from qt_utils.qt_task_progress_runner import QtTaskProgressRunner
from sysutils.typed import non_optional

if TYPE_CHECKING:
    from collections.abc import Iterator

    from qt_utils.i_task_progress_runner import ITaskRunner

class TaskRunner(Slots):
    @classmethod
    def create(cls, window_title: str, label_text: str, visible: bool | None = None, allow_cancel: bool = True) -> ITaskRunner:
        if visible is None: visible = not app.is_testing
        if not visible:
            return InvisibleTaskRunner(window_title, label_text)
        return QtTaskProgressRunner(window_title, label_text, allow_cancel)

    _depth: int = 0
    _current: ITaskRunner | None = None

    @classmethod
    @contextmanager
    def current(cls, window_title: str, label_text: str | None = None, force_hide: bool = False, inhibit_gc: bool = False, force_gc: bool = False, allow_cancel: bool = True) -> Iterator[ITaskRunner]:
        cls._depth += 1
        if cls._depth == 1:
            visible = (not app.is_testing) and not force_hide
            cls._current = cls.create(window_title, label_text or window_title, visible, allow_cancel)
            if not inhibit_gc:
                cls._current.run_gc()
        else:
            non_optional(cls._current).set_label_text(label_text or window_title)

        runner = non_optional(cls._current)

        try: yield non_optional(cls._current)
        finally:
            cls._depth -= 1
            if cls._depth == 0:
                if not inhibit_gc:
                    runner.run_gc()
                runner.close()
                cls._current = None
            elif force_gc:
                runner.run_gc()

