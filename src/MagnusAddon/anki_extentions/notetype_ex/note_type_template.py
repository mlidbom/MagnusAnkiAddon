from __future__ import annotations

from typing import Any

from autoslot import Slots
from sysutils import typed


class NoteTemplateEx(Slots):
    def __init__(self, name: str) -> None:
        self.name: str = name
        self.ord: int = 0
        self.qfmt: str = "{{Tags}}"
        self.afmt: str = "{{Tags}}"
        self.bqfmt: str = ""
        self.bafmt: str = ""
        self.did: int = 0
        self.bfont: str = "Arial"
        self.bsize: int = 30

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name,
                "ord": self.ord,
                "qfmt": self.qfmt,
                "afmt": self.afmt,
                "bqfmt": self.bqfmt,
                "bafmt": self.bafmt,
                "did": self.did,
                "bfont": self.bfont,
                "bsize": self.bsize}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> NoteTemplateEx:
        instance = NoteTemplateEx(d["name"])

        instance.ord = typed.int_(d["ord"])
        instance.qfmt = typed.str_(d["qfmt"])
        instance.afmt = typed.str_(d["afmt"])
        instance.bqfmt = typed.str_(d["bqfmt"])
        instance.bafmt = typed.str_(d["bafmt"])
        # missing for som reason# instance.did = typed.int_(d['did'])
        instance.bfont = typed.str_(d["bfont"])
        instance.bsize = typed.int_(d["bsize"])
        return instance
