from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from note.note_constants import NoteFields, Tags
from note.notefields.auto_save_wrappers.set_wrapper import FieldSetWrapper
from note.notefields.json_object_field import JsonObjectField
from note.notefields.require_forbid_flag_field import RequireForbidFlagField
from note.notefields.tag_flag_field import TagFlagField
from note.vocabulary.serialization.matching_rules_serializer import VocabNoteMatchingRulesSerializer
from note.vocabulary.vocabnote_matching_rules_is_inflecting_word import IsInflectingWord
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
    def __init__(self, surface_is_not: set[str], prefix_is_not: set[str], suffix_is_not: set[str], required_prefix: set[str], yield_to_surface: set[str]) -> None:
        self.prefix_is_not = prefix_is_not
        self.suffix_is_not = suffix_is_not
        self.surface_is_not = surface_is_not
        self.yield_to_surface = yield_to_surface
        self.required_prefix = required_prefix

class VocabNoteMatchingRules(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._data: JsonObjectField[VocabNoteMatchingRulesData] = JsonObjectField(vocab, NoteFields.Vocab.matching_rules, VocabNoteMatchingRulesData.serializer)
        self.surface_is_not: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().surface_is_not)
        self.yield_to_surface: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().yield_to_surface)
        self.prefix_is_not: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().prefix_is_not)
        self.suffix_is_not: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().suffix_is_not)
        self.required_prefix: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().required_prefix)

    def save(self) -> None:
        self._data.save()

    def overwrite_with(self, other: VocabNoteMatchingRules) -> None:
        self.surface_is_not.overwrite_with(other.surface_is_not)
        self.yield_to_surface.overwrite_with(other.yield_to_surface)
        self.prefix_is_not.overwrite_with(other.prefix_is_not)
        self.suffix_is_not.overwrite_with(other.suffix_is_not)
        self.required_prefix.overwrite_with(other.required_prefix)

    def __repr__(self) -> str: return (SkipFalsyValuesDebugReprBuilder()
                                       .prop("surface_is_not", self.surface_is_not.get())
                                       .prop("prefix_is_not", self.prefix_is_not.get())
                                       .prop("suffix_is_not", self.suffix_is_not.get())
                                       .prop("required_prefix", self.required_prefix.get()).repr)

class VocabMatchingRulesConfigurationFlags(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.e_stem: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.e_stem, Tags.Vocab.Matching.Forbids.e_stem)
        self.a_stem: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.a_stem, Tags.Vocab.Matching.Forbids.a_stem)
        self.past_tense_stem: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.past_tense_stem, Tags.Vocab.Matching.Forbids.past_tense_stem)
        self.t_form_stem: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.t_form_stem, Tags.Vocab.Matching.Forbids.t_form_stem)
        self.single_token: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.single_token, Tags.Vocab.Matching.Requires.compound)
        self.sentence_end: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.sentence_end, Tags.Vocab.Matching.Forbids.sentence_end)
        self.yield_last_token: RequireForbidFlagField = YieldLastTokenToOverlappingCompound(vocab)

class VocabNoteMatchingConfiguration(WeakRefable, Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.vocab: WeakRef[VocabNote] = vocab
        self.weakref = WeakRef(self)
        self._rules: Lazy[VocabNoteMatchingRules] = Lazy(lambda: VocabNoteMatchingRules(vocab))
        self.requires_exact_match: TagFlagField = TagFlagField(vocab, Tags.Vocab.Matching.Requires.exact_match)

        self.flags = VocabMatchingRulesConfigurationFlags(vocab)

        self.is_inflecting_word: IsInflectingWord = IsInflectingWord(vocab)
        self.is_poison_word: TagFlagField = TagFlagField(vocab, Tags.Vocab.Matching.is_poison_word)
        self.match_with_preceding_vowel: TagFlagField = TagFlagField(vocab, Tags.Vocab.Matching.Todo.with_preceding_vowel)
        self.question_overrides_form: QuestionOverridesForm = QuestionOverridesForm(vocab)
        self.is_strictly_suffix: IsStrictlySuffix = IsStrictlySuffix(vocab)

    @property
    def configurable_rules(self) -> VocabNoteMatchingRules: return self._rules.instance()

    @property
    def e_stem(self) -> RequireForbidFlagField: return self.flags.e_stem
    @property
    def a_stem(self) -> RequireForbidFlagField: return self.flags.a_stem
    @property
    def past_tense_stem(self) -> RequireForbidFlagField: return self.flags.past_tense_stem
    @property
    def t_form_stem(self) -> RequireForbidFlagField: return self.flags.t_form_stem
    @property
    def single_token(self) -> RequireForbidFlagField: return self.flags.single_token
    @property
    def sentence_end(self) -> RequireForbidFlagField: return self.flags.sentence_end
    @property
    def yield_last_token(self) -> RequireForbidFlagField: return self.flags.yield_last_token

    def save(self) -> None: self.configurable_rules.save()

    def __repr__(self) -> str: return (SkipFalsyValuesDebugReprBuilder()
                                       .flag("requires_exact_match", self.requires_exact_match.is_set())
                                       .flag("requires_single_token", self.single_token.is_required)
                                       .flag("requires_compound", self.single_token.is_forbidden)
                                       .flag("requires_a_stem", self.a_stem.is_required)
                                       .flag("forbids_a_stem", self.a_stem.is_forbidden)
                                       .flag("requires_e_stem", self.e_stem.is_required)
                                       .flag("forbids_e_stem", self.e_stem.is_forbidden)
                                       .flag("requires_past_tense_stem", self.past_tense_stem.is_required)
                                       .flag("forbids_past_tense_stem", self.past_tense_stem.is_forbidden)
                                       .flag("requires_t_form_stem", self.t_form_stem.is_required)
                                       .flag("forbids_t_form_stem", self.t_form_stem.is_forbidden)
                                       .flag("requires_sentence_end", self.sentence_end.is_required)
                                       .flag("is_inflecting_word", self.is_inflecting_word.is_set())
                                       .flag("is_poison_word", self.is_poison_word.is_set())
                                       .flag("yield_last_token_to_overlapping_compound", self.yield_last_token.is_required)
                                       .flag("forbid_auto_yielding_last_token", self.yield_last_token.is_forbidden)
                                       .flag("match_with_preceding_vowel", self.match_with_preceding_vowel.is_set())
                                       .flag("question_overrides_form", self.question_overrides_form.is_set())
                                       .flag("is_strictly_suffix", self.is_strictly_suffix.is_set())
                                       .include(self.configurable_rules).repr)
