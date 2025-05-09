from anki_extentions.notetype_ex.note_type_ex import NoteTypeEx
from anki_extentions.notetype_ex.note_type_field import NoteFieldEx
from anki_extentions.notetype_ex.note_type_template import NoteTemplateEx
from note.note_constants import NoteTypes, SentenceNoteFields

def create_sentence() -> NoteTypeEx:
    return NoteTypeEx(NoteTypes.Sentence,
                      [
                          NoteFieldEx(SentenceNoteFields.active_question),
                          NoteFieldEx(SentenceNoteFields.source_question),
                          NoteFieldEx(SentenceNoteFields.user_question),
                          NoteFieldEx(SentenceNoteFields.active_answer),
                          NoteFieldEx(SentenceNoteFields.source_answer),
                          NoteFieldEx(SentenceNoteFields.user_answer),
                          NoteFieldEx(SentenceNoteFields.ParsedWords),
                          NoteFieldEx(SentenceNoteFields.user_excluded_vocab),
                          NoteFieldEx(SentenceNoteFields.user_extra_vocab),
                          NoteFieldEx(SentenceNoteFields.configuration)],
                      [NoteTemplateEx("reading")])
