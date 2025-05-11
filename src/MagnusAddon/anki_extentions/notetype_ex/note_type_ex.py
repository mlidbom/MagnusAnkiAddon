from __future__ import annotations

from typing import Any, cast

from anki.models import NotetypeDict, NotetypeId
from anki_extentions.notetype_ex.note_type_field import NoteFieldEx
from anki_extentions.notetype_ex.note_type_template import NoteTemplateEx
from sysutils import typed


class NoteTypeEx:
    def __init__(self, name: str, fields: list[NoteFieldEx], templates: list[NoteTemplateEx]):
        self.name = name
        self.id:NotetypeId = NotetypeId(0)
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

        for index, field in enumerate(self.flds):
            field.ord = index

        for index, template in enumerate(self.tmpls):
            template.ord = index

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

    def assert_schema_matches(self, other: NoteTypeEx) -> None:
        assert len(self.flds) == len(other.flds)
        for index in range(len(self.flds)):
            assert self.flds[index].ord == other.flds[index].ord
            assert self.flds[index].name == other.flds[index].name

    @classmethod
    def from_dict(cls, note_type_dict: NotetypeDict) -> NoteTypeEx:
        created = NoteTypeEx(note_type_dict['name'],[], [])
        created.flds = [NoteFieldEx.from_dict(d) for d in note_type_dict['flds']]
        created.tmpls = [NoteTemplateEx.from_dict(t) for t in note_type_dict['tmpls']]

        created.id = cast(NotetypeId, typed.int_(note_type_dict['id']))
        created.type = typed.int_(note_type_dict['type'])
        created.mod = typed.int_(note_type_dict['mod'])
        created.usn = typed.int_(note_type_dict['usn'])
        created.sortf = typed.int_(note_type_dict['sortf'])
        #todo: wth is this None? created.did = typed.int_(note_type_dict['did'])
        created.css = typed.str_(note_type_dict['css'])
        created.latexPre = typed.str_(note_type_dict['latexPre'])
        created.latexPost = typed.str_(note_type_dict['latexPost'])
        created.latexsvg = typed.bool_(note_type_dict['latexsvg'])
        created.req = note_type_dict['req']
        #todo: wth is this missing? created.vers = note_type_dict['vers']
        #todo: wth is this missing? created.tags = note_type_dict['tags']

        return created

