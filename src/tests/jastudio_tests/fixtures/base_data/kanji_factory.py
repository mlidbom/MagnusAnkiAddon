from __future__ import annotations

from jaslib.note.note_constants import NoteFields, NoteTypes
from jastudio.anki_extentions.notetype_ex.note_type_ex import NoteTypeEx
from jastudio.anki_extentions.notetype_ex.note_type_field import NoteFieldEx
from jastudio.anki_extentions.notetype_ex.note_type_template import NoteTemplateEx


def create_kanji() -> NoteTypeEx:
    return NoteTypeEx(NoteTypes.Kanji,
                      [
                          NoteFieldEx(NoteFields.Kanji.question),
                          NoteFieldEx(NoteFields.Kanji.active_answer),
                          NoteFieldEx(NoteFields.Kanji.source_answer),
                          NoteFieldEx(NoteFields.Kanji.user_answer),
                          NoteFieldEx(NoteFields.Kanji.Reading_On),
                          NoteFieldEx(NoteFields.Kanji.Reading_Kun),
                          NoteFieldEx(NoteFields.Kanji.Reading_Nan),
                          NoteFieldEx(NoteFields.Kanji.Radicals),
                          NoteFieldEx(NoteFields.Kanji.Source_Meaning_Mnemonic),
                          NoteFieldEx(NoteFields.Kanji.Meaning_Info),
                          NoteFieldEx(NoteFields.Kanji.Reading_Mnemonic),
                          NoteFieldEx(NoteFields.Kanji.Reading_Info),
                          NoteFieldEx(NoteFields.Kanji.PrimaryVocab),
                          NoteFieldEx(NoteFields.Kanji.Audio__),
                          NoteFieldEx(NoteFields.Kanji.user_mnemonic)
                      ],
                      [NoteTemplateEx("reading")])
