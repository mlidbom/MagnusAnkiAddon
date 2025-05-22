from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.note_constants import NoteFields, Tags
from note.notefields.auto_save_wrappers.set_wrapper import FieldSetWrapper
from note.notefields.json_object_field import JsonObjectField
from note.notefields.tag_flag_field import TagFlagField
from note.vocabulary.serialization.matching_rules_serializer import VocabNoteMatchingRulesSerializer
from note.vocabulary.vocabnote_matching_rules_is_strictly_prefix import IsStrictlySuffix
from note.vocabulary.vocabnote_matching_rules_question_overrides_form import QuestionOverridesForm
from sysutils.lazy import Lazy

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from sysutils.weak_ref import WeakRef

class VocabNoteMatchingRulesData(Slots):
    serializer = VocabNoteMatchingRulesSerializer()
    def __init__(self, surface_is_not: set[str], prefer_over_base: set[str], prefix_is_not: set[str], required_prefix: set[str]) -> None:
        self.prefix_is_not = prefix_is_not
        self.surface_is_not = surface_is_not
        self.prefer_over_base = prefer_over_base
        self.required_prefix = required_prefix

class VocabNoteMatchingRules(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._data: JsonObjectField[VocabNoteMatchingRulesData] = JsonObjectField(vocab, NoteFields.Vocab.matching_rules, VocabNoteMatchingRulesData.serializer)
        self.surface_is_not: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().surface_is_not)
        self.prefer_over_base: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().prefer_over_base)
        self.prefix_is_not: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().prefix_is_not)
        self.required_prefix: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().required_prefix)

    def save(self) -> None:
        self._data.save()

class VocabNoteMatching(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._data: WeakRef[VocabNote] = vocab
        self._rules: Lazy[VocabNoteMatchingRules] = Lazy(lambda: VocabNoteMatchingRules(vocab))
        self.requires_exact_match: TagFlagField = TagFlagField(vocab, Tags.Vocab.Matching.requires_exact_match)
        self.question_overrides_form: QuestionOverridesForm = QuestionOverridesForm(vocab)
        self.requires_a_stem: TagFlagField = TagFlagField(vocab, Tags.Vocab.Matching.requires_a_stem)
        self.requires_e_stem: TagFlagField = TagFlagField(vocab, Tags.Vocab.Matching.requires_e_stem)
        self.match_with_preceding_vowel: TagFlagField = TagFlagField(vocab, Tags.Vocab.Matching.Todo.with_preceding_vowel)
        self.is_strictly_suffix: IsStrictlySuffix = IsStrictlySuffix(vocab)

    @property
    def rules(self) -> VocabNoteMatchingRules:
        return self._rules.instance()

    def save(self) -> None:
        self.rules.save()
