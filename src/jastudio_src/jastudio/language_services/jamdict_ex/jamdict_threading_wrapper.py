from __future__ import annotations

import queue
import threading
from concurrent.futures import Future
from typing import TYPE_CHECKING, Any

from autoslot import Slots
from jamdict import Jamdict  # pyright: ignore [reportMissingTypeStubs]
from typed_linq_collections.collections.q_list import QList

from jastudio.ankiutils import app
from jastudio.sysutils.lazy import Lazy
from jastudio.sysutils.typed import non_optional, str_
from jastudio.sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from collections.abc import Callable

    from jamdict.util import LookupResult  # pyright: ignore [reportMissingTypeStubs]

class Request[T](Slots):
    def __init__(self, func: Callable[[Jamdict], T], future: Future[T]) -> None:
        self.func: Callable[[Jamdict], T] = func
        self.future: Future[T] = future

class JamdictThreadingWrapper(WeakRefable,Slots):
    def __init__(self) -> None:
        self._queue: queue.Queue[Request[Any]] = queue.Queue()  # pyright: ignore[reportExplicitAny]
        self._thread: threading.Thread = threading.Thread(target=self._worker, daemon=True)
        self._running: bool = True
        self._thread.start()
        weak_self = WeakRef(self)
        self.jamdict: Lazy[Jamdict] = Lazy(lambda: weak_self().create_jamdict()) # todo: earlier attempts to save memory by resetting the jamdict instance periodically were flawed since the lazy did not use a weak reference, creatinga circular referenene that kept the instance in memory.

    @classmethod
    def create_jamdict(cls) -> Jamdict:
        return Jamdict(memory_mode=True) \
            if (app.config().load_jamdict_db_into_memory.get_value()
                and not app.is_testing) \
            else Jamdict(reuse_ctx=True)

    def _worker(self) -> None:
        while self._running:
            request = self._queue.get()
            try:
                result = request.func(self.jamdict())  # pyright: ignore[reportAny]
                request.future.set_result(result)
            except Exception as e:
                request.future.set_exception(e)

    def lookup(self, word: str, include_names: bool) -> LookupResult:
        future: Future[LookupResult] = Future()

        def do_actual_lookup(jamdict: Jamdict) -> LookupResult:
            return jamdict.lookup(word, lookup_chars=False, lookup_ne=include_names)  # pyright: ignore[reportUnknownMemberType]

        self._queue.put(Request(do_actual_lookup, future))
        return future.result()

    def run_string_query(self, sql_query: str) -> QList[str]:
        def perform_query(jamdict: Jamdict) -> QList[str]:
            result: QList[str] = QList()
            for batch in non_optional(non_optional(jamdict.jmdict).ctx().conn).execute(sql_query):  # pyright: ignore[reportAny]
                for row in batch:  # pyright: ignore[reportAny]
                    result.append(str_(row))  # noqa: PERF401  # pyright: ignore[reportAny]

            return result

        future: Future[QList[str]] = Future()

        self._queue.put(Request(perform_query, future))
        return future.result()
