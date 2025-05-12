from __future__ import annotations

from typing import TYPE_CHECKING

from language_services.jamdict_ex.priority_spec import PrioritySpec
from note.note_constants import Mine, NoteFields
from note.notefields.integer_field import IntegerField
from note.vocabulary import vocabnote_meta_tag

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

class VocabNoteMetaDataFlags:
    def __init__(self, vocab: VocabNote) -> None:
        self._vocab: VocabNote = vocab

    def question_overrides_form(self) -> bool:
        return self._vocab.has_tag(Mine.Tags.question_overrides_form)

    def requires_exact_match(self) -> bool:
        return self._vocab.has_tag(Mine.Tags.requires_exact_match)

class VocabNoteMetaData:
    def __init__(self, vocab: VocabNote) -> None:
        self._vocab: VocabNote = vocab
        self.flags: VocabNoteMetaDataFlags = VocabNoteMetaDataFlags(vocab)
        self.sentence_count: IntegerField = IntegerField(vocab, NoteFields.Vocab.sentence_count)

    def meta_tags_html(self: VocabNote, display_extended_sentence_statistics: bool = True) -> str:
        return vocabnote_meta_tag.get_meta_tags_html(self, display_extended_sentence_statistics)

    def priority_spec(self) -> PrioritySpec:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        lookup = DictLookup.try_lookup_vocab_word_or_name(self._vocab)
        return lookup.priority_spec() if lookup else PrioritySpec(set())
