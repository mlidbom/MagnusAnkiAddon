from typing import Any

from anki.models import NotetypeDict

from anki_extentions.notetype_ex.note_type_field import NoteFieldEx
from anki_extentions.notetype_ex.note_type_template import NoteTemplateEx


class NoteTypeEx:
    def __init__(self, name: str, fields: list[NoteFieldEx], templates: list[NoteTemplateEx]):
        self.name = name
        self.id = 0
        self.flds = fields
        self.tmpls = templates
        self.type = 0
        self.mod = 0
        self.usn = 0
        self.sortf = 0
        self.did = 0
        self.css = ''
        self.latexPre = ''
        self.latexPost = ''
        self.latexsvg = False
        self.req:list[Any] = []
        self.vers: list[Any] = []
        self.tags: list[Any] = []

        index = 0
        for field in self.flds:
            field.ord = index
            index += 1

        index = 0
        for template in self.tmpls:
            template.ord = index
            index += 1

    def to_dict(self) -> NotetypeDict:
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'mod': self.mod,
            'usn': self.usn,
            'sortf': self.sortf,
            'did': self.did,
            'tmpls': [t.to_dict() for t in self.tmpls],
            'flds': [f.to_dict() for f in self.flds],
            'css': self.css,
            'latexPre': self.latexPre,
            'latexPost': self.latexPost,
            'latexsvg': self.latexsvg,
            'req': self.req,
            'vers': self.vers,
            'tags': self.tags
        }
