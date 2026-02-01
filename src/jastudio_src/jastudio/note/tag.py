from __future__ import annotations

from autoslot import Slots
from typed_linq_collections.collections.q_dict import QDict


class Tag(Slots):
    _used_ids: set[int] = set()
    _by_id: QDict[int, Tag] = QDict()
    _by_name: QDict[str, Tag] = QDict()

    _secret: str = "lahoeubaoehbl2304985 iimjj08dm0"

    def __init__(self, name: str, secret_don_call_this_method: str) -> None:
        if secret_don_call_this_method != self._secret:
            raise ValueError("This is a private constructor, don't call it from outside the class")

        id = len(Tag._used_ids)

        self.name: str = name
        self.id: int = id
        self.bit: int = 1 << id

        Tag._used_ids.add(id)
        Tag._by_id[id] = self
        Tag._by_name[name] = self

    @classmethod
    def _add_tag(cls, name: str) -> Tag: return Tag(name, Tag._secret)

    @classmethod
    def from_name(cls, name: str) -> Tag:
        return Tag._by_name.get_or_add(name, Tag._add_tag)

    @classmethod
    def from_id(cls, id: int) -> Tag:
        return Tag._by_id[id]
