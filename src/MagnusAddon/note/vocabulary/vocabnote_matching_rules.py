from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.note_constants import Mine, NoteFields
from note.notefields.auto_save_wrappers.set_wrapper import FieldSetWrapper
from note.notefields.json_object_field import JsonObjectField
from note.notefields.tag_flag_field import TagFlagField
from note.vocabulary.serialization.matching_rules_serializer import VocabNoteMatchingRulesSerializer
from sysutils.lazy import Lazy

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNoteMatchingRulesData(Slots):
    serializer = VocabNoteMatchingRulesSerializer()
    def __init__(self, surface_is_not: set[str], base_is_not: set[str], prefix_is_not:set[str], required_prefix:set[str]) -> None:
        self.prefix_is_not = prefix_is_not
        self.surface_is_not = surface_is_not
        self.base_is_not = base_is_not
        self.required_prefix = required_prefix

class VocabNoteMatchingRules:
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:

        self._data: JsonObjectField[VocabNoteMatchingRulesData] = JsonObjectField(vocab, NoteFields.Vocab.matching_rules, VocabNoteMatchingRulesData.serializer)
        self.surface_is_not: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data.weakref, self._data.get().surface_is_not)
        self.base_is_not: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data.weakref, self._data.get().base_is_not)
        self.prefix_is_not: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data.weakref, self._data.get().prefix_is_not)
        self.required_prefix: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data.weakref, self._data.get().required_prefix)

class VocabNoteMatching(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._data: WeakRef[VocabNote] = vocab
        self._rules: Lazy[VocabNoteMatchingRules] = Lazy(lambda: VocabNoteMatchingRules(vocab))
        self.requires_exact_match: TagFlagField = TagFlagField(vocab, Mine.Tags.requires_exact_match)
        self.question_overrides_form: TagFlagField = TagFlagField(vocab, Mine.Tags.question_overrides_form)
        self.requires_a_stem: TagFlagField = TagFlagField(vocab, Mine.Tags.requires_a_stem)
        self.requires_e_stem: TagFlagField = TagFlagField(vocab, Mine.Tags.requires_e_stem)
        self.match_with_preceding_character: TagFlagField = TagFlagField(vocab, Mine.Tags.match_with_preceding_character)
        self.match_with_preceding_vowel: TagFlagField = TagFlagField(vocab, Mine.Tags.match_with_preceding_vowel)

    @property
    def rules(self) -> VocabNoteMatchingRules:
        return self._rules.instance()
