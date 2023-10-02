from typing import Any


class NoteTemplateEx:
    def __init__(self, name: str):
        self.name = name
        self.ord = 0
        self.qfmt = "{{Tags}}"
        self.afmt = "{{Tags}}"
        self.bqfmt = ""
        self.bafmt = ""
        self.did = 0
        self.bfont = "Arial"
        self.bsize = 30

    def to_dict(self) -> dict[str, Any]:
        return {'name': self.name,
                'ord': self.ord,
                'qfmt': self.qfmt,
                'afmt': self.afmt,
                'bqfmt': self.bqfmt,
                'bafmt': self.bafmt,
                'did': self.did,
                'bfont': self.bfont,
                'bsize': self.bsize}
