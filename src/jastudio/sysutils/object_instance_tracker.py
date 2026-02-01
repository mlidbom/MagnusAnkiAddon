from __future__ import annotations

import sys

from jastudio.ankiutils import app
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from sysutils.ex_str import newline
from typed_linq_collections.collections.q_dict import QDict

current_instance_count: QDict[str, int] = QDict()

class Snapshot(Slots):
    def __init__(self, current_state: dict[str, int], previous_state: dict[str, int]) -> None:
        self.previous: dict[str, int] = previous_state
        self.current_counts: dict[str, int] = current_state

    def single_line_diff_report(self) -> str:
        diffs: dict[str, int] = {}
        for type_name, count in self.current_counts.items():
            change = count - self.previous.get(type_name, 0)
            if change != 0:
                diffs[type_name] = change
        return f"""{newline.join([f"{type_name.split('.')[-1]}:{diff}" for type_name, diff in diffs.items()])}""" if diffs else "No changes"

snapshots: list[Snapshot] = []

def take_snapshot() -> Snapshot:
    diff = create_transient_snapshot_against_last_snapshot()
    snapshots.append(diff)
    return diff

def create_transient_snapshot_against_last_snapshot() -> Snapshot:
    current_state = current_instance_count.copy()
    previous_state = snapshots[-1].current_counts if len(snapshots) > 0 else {}
    return Snapshot(current_state, previous_state)

def create_transient_snapshot_against_first_snapshot() -> Snapshot:
    current_state = current_instance_count.copy()
    previous_state = snapshots[0].current_counts if len(snapshots) > 0 else {}
    return Snapshot(current_state, previous_state)

def current_snapshot() -> Snapshot:
    if len(snapshots) == 0:
        take_snapshot()
    return snapshots[-1]

# NOTE: THIS IS NOT RELIABLE, IT WILL SOMETIMES, IN UNKNOWN CIRCUMSTANCES REPORT ZERO INSTANCES OF A CLASS, AND STILL A MAJOR MEMORY LEAK WILL BE RESOLVED WHENE A CIRCULAR REFERENCE WITHIN THAT CLASS IS FIXED
class ObjectInstanceTracker(Slots):
    _track_instances_in_memory: bool = app.config().track_instances_in_memory.get_value()
    def __init__(self, cls_type: type[object]) -> None:
        self.type_name: str = self._get_fully_qualified_name(cls_type)
        current_instance_count[self.type_name] = current_instance_count.get(self.type_name, 0) + 1

    def __del__(self) -> None:
        current_instance_count[self.type_name] -= 1

    @classmethod
    def _get_fully_qualified_name(cls, cls_type: type[object]) -> str:
        if cls_type.__module__ != "__builtin__":
            return sys.intern(cls_type.__module__ + "." + cls_type.__qualname__)
        return sys.intern(cls_type.__qualname__)

    # noinspection PyUnusedFunction
    @classmethod
    def configured_tracker_for(cls, obj: object) -> object | None: return ObjectInstanceTracker(obj.__class__) if ObjectInstanceTracker._track_instances_in_memory else None

    @classmethod
    def tracker_for(cls, obj: object) -> ObjectInstanceTracker: return ObjectInstanceTracker(obj.__class__)

def print_instance_counts() -> None:
    print("################### Instance counts ###################")

    counts = (current_instance_count.qitems()
              .order_by(lambda kv: kv.key)
              .order_by_descending(lambda kv: kv.value)
              .to_list())
    for type_name, count in counts:
        print(f"{count} {type_name}")

def single_line_report() -> str:
    return f"""{', '.join([f"{type_name.split('.')[-1]}:{count}" for type_name, count in current_instance_count.items()])}"""
