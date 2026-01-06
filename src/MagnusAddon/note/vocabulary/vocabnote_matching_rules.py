from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from note.note_constants import NoteFields
from note.notefields.auto_save_wrappers.set_wrapper import FieldSetWrapper
from note.notefields.json_object_field import MutableSerializedObjectField
from note.notefields.require_forbid_flag_field import RequireForbidFlagField
from note.notefields.tag_flag_field import TagFlagField
from note.tags import Tags
from note.vocabulary.serialization.matching_rules_serializer import VocabNoteMatchingRulesSerializer
from note.vocabulary.vocabnote_matching_rules_is_inflecting_word import IsInflectingWord
from note.vocabulary.vocabnote_matching_rules_yield_last_token_to_next_compound import YieldLastTokenToOverlappingCompound
from sysutils.debug_repr_builder import SkipFalsyValuesDebugReprBuilder
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote
    from typed_linq_collections.collections.q_set import QSet

class VocabNoteMatchingRulesData(Slots):
    serializer: Lazy[VocabNoteMatchingRulesSerializer] = Lazy(VocabNoteMatchingRulesSerializer)

    def __init__(self, surface_is_not: QSet[str], prefix_is_not: QSet[str], suffix_is_not: QSet[str], required_prefix: QSet[str], yield_to_surface: QSet[str]) -> None:
        self.prefix_is_not: QSet[str] = prefix_is_not
        self.suffix_is_not: QSet[str] = suffix_is_not
        self.surface_is_not: QSet[str] = surface_is_not
        self.yield_to_surface: QSet[str] = yield_to_surface
        self.required_prefix: QSet[str] = required_prefix

class VocabNoteMatchingRules(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._data: MutableSerializedObjectField[VocabNoteMatchingRulesData] = MutableSerializedObjectField(vocab, NoteFields.Vocab.matching_rules, VocabNoteMatchingRulesData.serializer())
        self.surface_is_not: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().surface_is_not)  # pyright: ignore[reportUnknownMemberType]
        self.yield_to_surface: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().yield_to_surface)  # pyright: ignore[reportUnknownMemberType]
        self.prefix_is_not: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().prefix_is_not)  # pyright: ignore[reportUnknownMemberType]
        self.suffix_is_not: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().suffix_is_not)  # pyright: ignore[reportUnknownMemberType]
        self.required_prefix: FieldSetWrapper[str] = FieldSetWrapper.for_json_object_field(self._data, self._data.get().required_prefix)  # pyright: ignore[reportUnknownMemberType]

    def overwrite_with(self, other: VocabNoteMatchingRules) -> None:
        self.surface_is_not.overwrite_with(other.surface_is_not)
        self.yield_to_surface.overwrite_with(other.yield_to_surface)
        self.prefix_is_not.overwrite_with(other.prefix_is_not)
        self.suffix_is_not.overwrite_with(other.suffix_is_not)
        self.required_prefix.overwrite_with(other.required_prefix)

    @override
    def __repr__(self) -> str: return (SkipFalsyValuesDebugReprBuilder()
                                       .prop("surface_is_not", self.surface_is_not.get())
                                       .prop("prefix_is_not", self.prefix_is_not.get())
                                       .prop("suffix_is_not", self.suffix_is_not.get())
                                       .prop("required_prefix", self.required_prefix.get()).repr)

# todo performance: memory: high-priority: combine into a single bitfield in memory
class VocabMatchingRulesConfigurationRequiresForbidsFlags(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.e_stem: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.e_stem, Tags.Vocab.Matching.Forbids.e_stem)
        self.a_stem: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.a_stem, Tags.Vocab.Matching.Forbids.a_stem)
        self.masu_stem: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.masu_stem, Tags.Vocab.Matching.Forbids.masu_stem)
        self.preceding_adverb: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.preceding_adverb, Tags.Vocab.Matching.Forbids.preceding_adverb)
        self.past_tense_stem: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.past_tense_stem, Tags.Vocab.Matching.Forbids.past_tense_stem)
        self.dictionary_form_stem: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.dictionary_form_stem, Tags.Vocab.Matching.Forbids.dictionary_form_stem)
        self.dictionary_form_prefix: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.dictionary_form_prefix, Tags.Vocab.Matching.Forbids.dictionary_form_prefix)
        self.te_form_stem: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.te_form_stem, Tags.Vocab.Matching.Forbids.te_form_stem)
        self.ichidan_imperative: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.ichidan_imperative, Tags.Vocab.Matching.Forbids.ichidan_imperative)
        self.godan_potential: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.godan_potential, Tags.Vocab.Matching.Forbids.godan_potential)
        self.godan_imperative: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.godan_imperative, Tags.Vocab.Matching.Forbids.godan_imperative)
        self.godan_imperative_prefix: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.godan_imperative_prefix, Tags.Vocab.Matching.Forbids.godan_imperative_prefix)
        self.single_token: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.single_token, Tags.Vocab.Matching.Requires.compound)
        self.sentence_end: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.sentence_end, Tags.Vocab.Matching.Forbids.sentence_end)
        self.sentence_start: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.sentence_start, Tags.Vocab.Matching.Forbids.sentence_start)
        self.exact_match: RequireForbidFlagField = RequireForbidFlagField(vocab, Tags.Vocab.Matching.Requires.exact_match, Tags.Vocab.Matching.Forbids.exact_match)
        self.yield_last_token: RequireForbidFlagField = YieldLastTokenToOverlappingCompound(vocab)

# todo performance: memory: high-priority: combine into a single bitfield in memory
class VocabMatchingRulesConfigurationBoolFlags(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab
        self.is_inflecting_word: IsInflectingWord = IsInflectingWord(vocab)

    @property
    def is_poison_word(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Matching.is_poison_word)
    @property
    def match_with_preceding_vowel(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Matching.Todo.with_preceding_vowel)
    @property
    def question_overrides_form(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.question_overrides_form)
    @property
    def is_compositionally_transparent_compound(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.is_compositionally_transparent_compound)

    @override
    def __repr__(self) -> str: return f"""{self.is_inflecting_word}, {self.is_poison_word}, {self.match_with_preceding_vowel}, {self.question_overrides_form}"""

class VocabNoteMatchingConfiguration(WeakRefable, Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self.vocab: WeakRef[VocabNote] = vocab
        self.weakref: WeakRef[VocabNoteMatchingConfiguration] = WeakRef(self)
        self._rules: Lazy[VocabNoteMatchingRules] = Lazy(lambda: VocabNoteMatchingRules(vocab))  # todo performance: memory: do we need to make this lazy? does it help?

        self.requires_forbids: VocabMatchingRulesConfigurationRequiresForbidsFlags = VocabMatchingRulesConfigurationRequiresForbidsFlags(vocab)
        self.bool_flags: VocabMatchingRulesConfigurationBoolFlags = VocabMatchingRulesConfigurationBoolFlags(vocab)

    @property
    def configurable_rules(self) -> VocabNoteMatchingRules: return self._rules()

    @override
    def __repr__(self) -> str: return (SkipFalsyValuesDebugReprBuilder()
                                       .flag("requires_exact_match", self.requires_forbids.exact_match.is_required)
                                       .flag("forbids_exact_match", self.requires_forbids.exact_match.is_forbidden)
                                       .flag("requires_single_token", self.requires_forbids.single_token.is_required)
                                       .flag("requires_compound", self.requires_forbids.single_token.is_forbidden)
                                       .flag("requires_a_stem", self.requires_forbids.a_stem.is_required)
                                       .flag("forbids_a_stem", self.requires_forbids.a_stem.is_forbidden)
                                       .flag("requires_e_stem", self.requires_forbids.e_stem.is_required)
                                       .flag("forbids_e_stem", self.requires_forbids.e_stem.is_forbidden)
                                       .flag("requires_masu_stem", self.requires_forbids.masu_stem.is_required)
                                       .flag("forbids_masu_stem", self.requires_forbids.masu_stem.is_forbidden)
                                       .flag("requires_preceding_adverb", self.requires_forbids.preceding_adverb.is_required)
                                       .flag("forbids_preceding_adverb", self.requires_forbids.preceding_adverb.is_forbidden)
                                       .flag("requires_past_tense_stem", self.requires_forbids.past_tense_stem.is_required)
                                       .flag("forbids_past_tense_stem", self.requires_forbids.past_tense_stem.is_forbidden)
                                       .flag("requires_dictionary_form_stem", self.requires_forbids.dictionary_form_stem.is_required)
                                       .flag("forbids_dictionary_form_stem", self.requires_forbids.dictionary_form_stem.is_forbidden)
                                       .flag("requires_dictionary_form_prefix", self.requires_forbids.dictionary_form_prefix.is_required)
                                       .flag("forbids_dictionary_form_prefix", self.requires_forbids.dictionary_form_prefix.is_forbidden)
                                       .flag("requires_godan_potential", self.requires_forbids.godan_potential.is_required)
                                       .flag("forbids_godan_potential", self.requires_forbids.godan_potential.is_forbidden)
                                       .flag("requires_ichidan_imperative", self.requires_forbids.ichidan_imperative.is_required)
                                       .flag("forbids_ichidan_imperative", self.requires_forbids.ichidan_imperative.is_forbidden)
                                       .flag("requires_godan_imperative", self.requires_forbids.godan_imperative.is_required)
                                       .flag("forbids_godan_imperative", self.requires_forbids.godan_imperative.is_forbidden)
                                       .flag("requires_godan_imperative_prefix", self.requires_forbids.godan_imperative_prefix.is_required)
                                       .flag("forbids_godan_imperative_prefix", self.requires_forbids.godan_imperative_prefix.is_forbidden)
                                       .flag("requires_t_form_stem", self.requires_forbids.te_form_stem.is_required)
                                       .flag("forbids_t_form_stem", self.requires_forbids.te_form_stem.is_forbidden)
                                       .flag("requires_sentence_end", self.requires_forbids.sentence_end.is_required)
                                       .flag("forbids_sentence_end", self.requires_forbids.sentence_end.is_forbidden)
                                       .flag("requires_sentence_start", self.requires_forbids.sentence_start.is_required)
                                       .flag("forbids_sentence_start", self.requires_forbids.sentence_start.is_forbidden)
                                       .flag("is_inflecting_word", self.bool_flags.is_inflecting_word.is_set())
                                       .flag("is_poison_word", self.bool_flags.is_poison_word.is_set())
                                       .flag("yield_last_token_to_overlapping_compound", self.requires_forbids.yield_last_token.is_required)
                                       .flag("forbid_auto_yielding_last_token", self.requires_forbids.yield_last_token.is_forbidden)
                                       .flag("match_with_preceding_vowel", self.bool_flags.match_with_preceding_vowel.is_set())
                                       .flag("question_overrides_form", self.bool_flags.question_overrides_form.is_set())
                                       .flag("is_compositionally_transparent_compound", self.bool_flags.is_compositionally_transparent_compound.is_set())
                                       .include(self.configurable_rules).repr)
