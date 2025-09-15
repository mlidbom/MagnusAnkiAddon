from __future__ import annotations

from anki_extentions.notetype_ex.note_type_ex import NoteTypeEx
from anki_extentions.notetype_ex.note_type_field import NoteFieldEx
from anki_extentions.notetype_ex.note_type_template import NoteTemplateEx
from note.note_constants import NoteFields, NoteTypes


def create_vocab() -> NoteTypeEx:
    return NoteTypeEx(NoteTypes.Vocab,
                      [NoteFieldEx(NoteFields.Vocab.question),
                       NoteFieldEx(NoteFields.Vocab.active_answer),
                       NoteFieldEx(NoteFields.Vocab.source_answer),
                       NoteFieldEx(NoteFields.Vocab.user_answer),
                       NoteFieldEx(NoteFields.Vocab.Reading),
                       NoteFieldEx(NoteFields.Vocab.parts_of_speech),
                       NoteFieldEx(NoteFields.Vocab.source_mnemonic),
                       NoteFieldEx(NoteFields.Vocab.Audio_b),
                       NoteFieldEx(NoteFields.Vocab.Audio_g),
                       NoteFieldEx(NoteFields.Vocab.Audio_TTS),
                       NoteFieldEx(NoteFields.Vocab.Forms),
                       NoteFieldEx(NoteFields.Vocab.source_reading_mnemonic),
                       NoteFieldEx(NoteFields.Vocab.Homophones),
                       NoteFieldEx(NoteFields.Vocab.ParsedTypeOfSpeech),
                       NoteFieldEx(NoteFields.Vocab.user_mnemonic),
                       NoteFieldEx(NoteFields.Vocab.sentence_count),
                       NoteFieldEx(NoteFields.Vocab.user_compounds),
                       NoteFieldEx(NoteFields.Vocab.matching_rules),
                       NoteFieldEx(NoteFields.Vocab.related_vocab)
                       ],
                      [NoteTemplateEx("reading")])
