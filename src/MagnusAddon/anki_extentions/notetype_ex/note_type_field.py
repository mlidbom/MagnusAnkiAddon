from __future__ import annotations

from typing import Any

from sysutils import typed


class NoteFieldEx:
    def __init__(self, name: str):
        self.name = name
        self.ord = 0
        self.sticky = False
        self.rtl = False
        self.font = 'Arial'
        self.size = 20
        self.description = ""
        self.plainText = False
        self.collapsed = False
        self.excludeFromSearch = False
        self.media: list[Any] = []

    def to_dict(self) -> dict[str, Any]:
        return {
            'name': self.name,
            'ord': self.ord,
            'sticky': self.sticky,
            'rtl': self.rtl,
            'font': self.font,
            'size': self.size,
            'description': self.description,
            'plainText': self.plainText,
            'collapsed': self.collapsed,
            'excludeFromSearch': self.excludeFromSearch,
            'media': self.media}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> NoteFieldEx:
        instance = NoteFieldEx(d['name'])

        instance.ord = typed.int_(d['ord'])
        instance.sticky = typed.bool_(d['sticky'])
        instance.rtl = typed.bool_(d['rtl'])
        instance.font = typed.str_(d['font'])
        instance.size = typed.int_(d['size'])
        instance.description = typed.str_(d['description'])
        instance.plainText = typed.bool_(d['plainText'])
        instance.collapsed = typed.bool_(d['collapsed'])
        instance.excludeFromSearch = typed.bool_(d['excludeFromSearch'])
        #todo: wth is this missing? instance.media = d['media']

        return instance

