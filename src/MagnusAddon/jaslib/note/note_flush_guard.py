from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING

from jaslib import mylog
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jaslib.configuration.settings import Settings
from jaslib.sysutils import ex_assert

if TYPE_CHECKING:
    from collections.abc import Iterator

    from jaslib.note.jpnote import JPNote
    from jaslib.sysutils.weak_ref import WeakRef

class NoteRecursiveFlushGuard(Slots):
    def __init__(self, note: WeakRef[JPNote]) -> None:
        self._note: WeakRef[JPNote] = note
        self._depth:int = 0

    @contextmanager
    def pause_flushing(self) -> Iterator[None]:
        ex_assert.equal(self._depth, 0, "We don't support nested flushing since the complexities have not been figured out yet")
        self._depth += 1
        try: yield
        finally:
            self._depth -= 1

    def _should_flush(self) -> bool: return self._depth == 0

    @property
    def is_flushing(self) -> bool: return self._depth > 0

    def flush(self) -> None:
        if self._should_flush():
            with self.pause_flushing():
                if Settings.log_when_flushing_notes():
                    mylog.info(f"Flushing {self._note().__class__.__name__}: {self._note().get_question()}")
                self._note()._update_in_cache()  # pyright: ignore [reportPrivateUsage]
                #raise NotImplementedError()
                #self._note().backend_note.col.update_note(self._note().backend_note)
