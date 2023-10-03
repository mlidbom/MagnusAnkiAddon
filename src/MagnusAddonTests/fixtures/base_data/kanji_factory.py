from anki_extentions.notetype_ex.note_type_ex import NoteTypeEx
from anki_extentions.notetype_ex.note_type_field import NoteFieldEx
from anki_extentions.notetype_ex.note_type_template import NoteTemplateEx
from note.note_constants import NoteTypes, NoteFields

def create_kanji() -> NoteTypeEx:
    return NoteTypeEx(NoteTypes.Kanji,
                      [
                          NoteFieldEx(NoteFields.Kanji.active_answer),
                          NoteFieldEx(NoteFields.Kanji.source_answer),
                          NoteFieldEx(NoteFields.Kanji.user_answer),
                          NoteFieldEx(NoteFields.Kanji.Reading_On),
                          NoteFieldEx(NoteFields.Kanji.Reading_Kun),
                          NoteFieldEx(NoteFields.Kanji.Radicals),
                          NoteFieldEx(NoteFields.Kanji.Radicals_Icons),
                          NoteFieldEx(NoteFields.Kanji.Radicals_Names),
                          NoteFieldEx(NoteFields.Kanji.Radicals_Icons_Names),
                          NoteFieldEx(NoteFields.Kanji.Meaning_Mnemonic),
                          NoteFieldEx(NoteFields.Kanji.Meaning_Info),
                          NoteFieldEx(NoteFields.Kanji.Reading_Mnemonic),
                          NoteFieldEx(NoteFields.Kanji.Reading_Info),
                          NoteFieldEx(NoteFields.Kanji.PrimaryVocab),
                          NoteFieldEx(NoteFields.Kanji.Audio__),
                          NoteFieldEx(NoteFields.Kanji.Mnemonic__),
                          NoteFieldEx(NoteFields.Kanji.amalgamation_subject_ids),
                          NoteFieldEx(NoteFields.Kanji.component_subject_ids),
                          NoteFieldEx(NoteFields.Kanji.Vocabs),
                          NoteFieldEx(NoteFields.Kanji.VocabsRaw)],
                      [NoteTemplateEx("reading")])