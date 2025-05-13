from __future__ import annotations

import gc
from typing import Any

from sysutils import ex_gc
from sysutils.timeutil import StopWatch

instance_counts: dict[str, int] = {}

class ObjectInstanceTracker:

    def __init__(self, cls_type: type[Any]) -> None:
        self.type_name = self._get_fully_qualified_name(cls_type)
        instance_counts[self.type_name] = instance_counts.get(self.type_name, 0) + 1

    def count(self) -> int:
        return instance_counts[self.type_name]

    def run_gc_and_assert_single_instance(self) -> None:
        with StopWatch.log_execution_time():
            #gc.collect()
            ex_gc.collect_on_on_ui_thread()
            if not instance_counts[self.type_name] == 1: raise Exception(f"Expected single instance of {self.type_name}, found {instance_counts[self.type_name]}")

    def __del__(self) -> None:
        instance_counts[self.type_name] -= 1

    @staticmethod
    def _get_fully_qualified_name(cls_type: type[Any]) -> str:
        if cls_type.__module__ is not None and cls_type.__module__ != "__builtin__":
            return cls_type.__module__ + "." + cls_type.__qualname__
        return cls_type.__qualname__

def print_instance_counts() -> None:
    print("################### Instance counts ###################")
    for type_name, count in instance_counts.items():
        print(f"{type_name}: {count}")
