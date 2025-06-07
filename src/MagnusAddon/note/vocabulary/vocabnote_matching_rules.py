from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.note_constants import NoteFields, Tags
from note.notefields.auto_save_wrappers.set_wrapper import FieldSetWrapper
from note.notefields.json_object_field import JsonObjectField
from note.notefields.require_forbid_flag_field import RequireForbidFlagField
from note.notefields.tag_flag_field import TagFlagField
from note.vocabulary.serialization.matching_rules_serializer import VocabNoteMatchingRulesSerializer
from note.vocabulary.vocabnote_matching_rules_is_strictly_prefix import IsStrictlySuffix
from note.vocabulary.vocabnote_matching_rules_question_overrides_form import QuestionOverridesForm
from note.vocabulary.vocabnote_matching_rules_yield_last_token_to_next_compound import YieldLastTokenToOverlappingCompound
from sysutils.debug_repr_builder import SkipFalsyValuesDebugReprBuilder
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

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

    def __repr__(self) -> str: return (SkipFalsyValuesDebugReprBuilder()
                                       .prop("surface_is_not", self.surface_is_not.get())
                                       .prop("prefer_over_base", self.prefer_over_base.get())
                                       .prop("prefix_is_not", self.prefix_is_not.get())
                                       .prop("required_prefix", self.required_prefix.get()).repr)

class VocabNoteMatching(WeakRefable, Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.vocab: WeakRef[VocabNote] = vocab
        self.weakref = WeakRef(self)
        self._rules: Lazy[VocabNoteMatchingRules] = Lazy(lambda: VocabNoteMatchingRules(vocab))
        self.requires_exact_match: TagFlagField = TagFlagField(vocab, Tags.Vocab.Matching.Requires.exact_match)

        self.e_stem: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.e_stem, Tags.Vocab.Matching.Forbids.e_stem)
        self.a_stem: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.a_stem, Tags.Vocab.Matching.Forbids.a_stem)
        self.single_token: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.single_token, Tags.Vocab.Matching.Requires.compound)
        self.sentence_end: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.sentence_end, Tags.Vocab.Matching.Forbids.sentence_end)
        self.yield_last_token: RequireForbidFlagField = YieldLastTokenToOverlappingCompound(vocab)

        self.is_inflecting_word: TagFlagField = TagFlagField(vocab, Tags.Vocab.Matching.is_inflecting_word)
        self.is_poison_word: TagFlagField = TagFlagField(vocab, Tags.Vocab.Matching.is_poison_word)
        self.match_with_preceding_vowel: TagFlagField = TagFlagField(vocab, Tags.Vocab.Matching.Todo.with_preceding_vowel)
        self.question_overrides_form: QuestionOverridesForm = QuestionOverridesForm(vocab)
        self.is_strictly_suffix: IsStrictlySuffix = IsStrictlySuffix(vocab)

    @property
    def rules(self) -> VocabNoteMatchingRules:
        return self._rules.instance()

    def save(self) -> None:
        self.rules.save()

    def __repr__(self) -> str: return (SkipFalsyValuesDebugReprBuilder()
                                       .flag("requires_exact_match", self.requires_exact_match.is_set())
                                       .flag("requires_single_token", self.single_token.is_required)
                                       .flag("requires_compound", self.single_token.is_forbidden)
                                       .flag("requires_a_stem", self.a_stem.is_required)
                                       .flag("forbids_a_stem", self.a_stem.is_forbidden)
                                       .flag("requires_e_stem", self.e_stem.is_required)
                                       .flag("forbids_e_stem", self.e_stem.is_forbidden)
                                       .flag("requires_sentence_end", self.sentence_end.is_required)
                                       .flag("is_inflecting_word", self.is_inflecting_word.is_set())
                                       .flag("is_poison_word", self.is_poison_word.is_set())
                                       .flag("yield_last_token_to_overlapping_compound", self.yield_last_token.is_required)
                                       .flag("forbid_auto_yielding_last_token", self.yield_last_token.is_required)
                                       .flag("match_with_preceding_vowel", self.match_with_preceding_vowel.is_set())
                                       .flag("question_overrides_form", self.question_overrides_form.is_set())
                                       .flag("is_strictly_suffix", self.is_strictly_suffix.is_set())
                                       .include(self.rules).repr)
