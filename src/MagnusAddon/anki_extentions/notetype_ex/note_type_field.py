from typing import Any


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
