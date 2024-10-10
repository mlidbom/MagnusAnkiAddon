from anki_extentions.notetype_ex.note_type_ex import NoteTypeEx
from anki_extentions.notetype_ex.note_type_field import NoteFieldEx
from anki_extentions.notetype_ex.note_type_template import NoteTemplateEx
from note.note_constants import NoteTypes, NoteFields

def create_vocab() -> NoteTypeEx:
    return NoteTypeEx(NoteTypes.Vocab,
                      [NoteFieldEx(NoteFields.Vocab.question),
                       NoteFieldEx(NoteFields.Vocab.active_answer),
                       NoteFieldEx(NoteFields.Vocab.source_answer),
                       NoteFieldEx(NoteFields.Vocab.user_answer),
                       NoteFieldEx(NoteFields.Vocab.Reading),
                       NoteFieldEx(NoteFields.Vocab.Speech_Type),
                       NoteFieldEx(NoteFields.Vocab.Context_jp),
                       NoteFieldEx(NoteFields.Vocab.Context_en),
                       NoteFieldEx(NoteFields.Vocab.Context_jp_2),
                       NoteFieldEx(NoteFields.Vocab.Context_en_2),
                       NoteFieldEx(NoteFields.Vocab.Context_jp_3),
                       NoteFieldEx(NoteFields.Vocab.Context_en_3),
                       NoteFieldEx(NoteFields.Vocab.source_mnemonic),
                       NoteFieldEx(NoteFields.Vocab.Audio_b),
                       NoteFieldEx(NoteFields.Vocab.Audio_g),
                       NoteFieldEx(NoteFields.Vocab.sort_id),
                       NoteFieldEx(NoteFields.Vocab.Related_similar_meaning),
                       NoteFieldEx(NoteFields.Vocab.Related_derived_from),
                       NoteFieldEx(NoteFields.Vocab.Related_ergative_twin),
                       NoteFieldEx(NoteFields.Vocab.Related_confused_with),
                       NoteFieldEx(NoteFields.Vocab.Kanji),
                       NoteFieldEx(NoteFields.Vocab.Forms),
                       NoteFieldEx(NoteFields.Vocab.source_reading_mnemonic),
                       NoteFieldEx(NoteFields.Vocab.Homophones),
                       NoteFieldEx(NoteFields.Vocab.ParsedTypeOfSpeech),
                       NoteFieldEx(NoteFields.Vocab.Mnemonic__),
                       NoteFieldEx(NoteFields.Vocab.component_subject_ids),
                       NoteFieldEx(NoteFields.Vocab.sentence_count)],
                      [NoteTemplateEx("reading")])