from anki_extentions.notetype_ex.note_type_ex import NoteTypeEx
from anki_extentions.notetype_ex.note_type_field import NoteFieldEx
from anki_extentions.notetype_ex.note_type_template import NoteTemplateEx
from note.note_constants import NoteFields, NoteTypes


def create_radical() -> NoteTypeEx:
    return NoteTypeEx(NoteTypes.Radical,
                      [NoteFieldEx(NoteFields.Radical.question),
                       NoteFieldEx(NoteFields.Radical.answer),
                       NoteFieldEx(NoteFields.Radical.source_mnemonic),
                       NoteFieldEx(NoteFields.Radical.Radical_Icon),
                       NoteFieldEx(NoteFields.Radical.sort_id),
                       NoteFieldEx(NoteFields.Radical.amalgamation_subject_ids)],
                      [NoteTemplateEx("reading")])