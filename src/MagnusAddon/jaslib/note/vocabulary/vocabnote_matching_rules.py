from __future__ import annotations

from typing import TYPE_CHECKING, override

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from jaslib.note.note_constants import NoteFields
from jaslib.note.notefields.auto_save_wrappers.set_wrapper import FieldSetWrapper
from jaslib.note.notefields.json_object_field import MutableSerializedObjectField
from jaslib.note.notefields.require_forbid_flag_field import RequireForbidFlagField
from jaslib.note.notefields.tag_flag_field import TagFlagField
from jaslib.note.tags import Tags
from jaslib.note.vocabulary.serialization.matching_rules_serializer import VocabNoteMatchingRulesSerializer
from jaslib.note.vocabulary.vocabnote_matching_rules_is_inflecting_word import IsInflectingWord
from jaslib.note.vocabulary.vocabnote_matching_rules_yield_last_token_to_next_compound import YieldLastTokenToOverlappingCompound
from sysutils.debug_repr_builder import SkipFalsyValuesDebugReprBuilder
from sysutils.lazy import Lazy
from sysutils.weak_ref import WeakRef, WeakRefable

if TYPE_CHECKING:
    from collections.abc import Iterable

    from jaslib.note.tag import Tag
    from jaslib.note.vocabulary.vocabnote import VocabNote
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
        self._all_sets: list[FieldSetWrapper[str]] = []
        self._data: MutableSerializedObjectField[VocabNoteMatchingRulesData] = MutableSerializedObjectField(vocab, NoteFields.Vocab.matching_rules, VocabNoteMatchingRulesData.serializer())
        self.surface_is_not: FieldSetWrapper[str] = self._add_set(self._data.get().surface_is_not)  # pyright: ignore[reportUnknownMemberType]
        self.yield_to_surface: FieldSetWrapper[str] = self._add_set(self._data.get().yield_to_surface)  # pyright: ignore[reportUnknownMemberType]
        self.prefix_is_not: FieldSetWrapper[str] = self._add_set(self._data.get().prefix_is_not)  # pyright: ignore[reportUnknownMemberType]
        self.suffix_is_not: FieldSetWrapper[str] = self._add_set(self._data.get().suffix_is_not)  # pyright: ignore[reportUnknownMemberType]
        self.required_prefix: FieldSetWrapper[str] = self._add_set(self._data.get().required_prefix)  # pyright: ignore[reportUnknownMemberType]

    def _add_set(self, value: QSet[str]) -> FieldSetWrapper[str]:
        wrapper: FieldSetWrapper[str] = FieldSetWrapper[str].for_json_object_field(self._data, value)
        self._all_sets.append(wrapper)
        return wrapper

    @property
    def match_weight(self) -> int:
        weight = 0
        if self.required_prefix.any():
            weight += 10
        for _ in (set_ for set_ in self._all_sets if set_):
            weight += 2
        return weight

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
        self._vocab: WeakRef[VocabNote] = vocab
        self._all_flags: list[RequireForbidFlagField] = []
        self.masu_stem: RequireForbidFlagField = self._add_flag(50, 1, Tags.Vocab.Matching.Requires.masu_stem, Tags.Vocab.Matching.Forbids.masu_stem)
        self.godan: RequireForbidFlagField = self._add_flag(50, 1, Tags.Vocab.Matching.Requires.godan, Tags.Vocab.Matching.Forbids.godan)
        self.ichidan: RequireForbidFlagField = self._add_flag(50, 1, Tags.Vocab.Matching.Requires.ichidan, Tags.Vocab.Matching.Forbids.ichidan)
        self.irrealis: RequireForbidFlagField = self._add_flag(50, 1, Tags.Vocab.Matching.Requires.irrealis, Tags.Vocab.Matching.Forbids.irrealis)
        self.preceding_adverb: RequireForbidFlagField = self._add_flag(30, 1, Tags.Vocab.Matching.Requires.preceding_adverb, Tags.Vocab.Matching.Forbids.preceding_adverb)
        self.past_tense_stem: RequireForbidFlagField = self._add_flag(30, 1, Tags.Vocab.Matching.Requires.past_tense_stem, Tags.Vocab.Matching.Forbids.past_tense_stem)
        self.dictionary_form_stem: RequireForbidFlagField = self._add_flag(30, 1, Tags.Vocab.Matching.Requires.dictionary_form_stem, Tags.Vocab.Matching.Forbids.dictionary_form_stem)
        self.dictionary_form_prefix: RequireForbidFlagField = self._add_flag(30, 1, Tags.Vocab.Matching.Requires.dictionary_form_prefix, Tags.Vocab.Matching.Forbids.dictionary_form_prefix)
        self.te_form_stem: RequireForbidFlagField = self._add_flag(20, 1, Tags.Vocab.Matching.Requires.te_form_stem, Tags.Vocab.Matching.Forbids.te_form_stem)
        self.te_form_prefix: RequireForbidFlagField = self._add_flag(20, 1, Tags.Vocab.Matching.Requires.te_form_prefix, Tags.Vocab.Matching.Forbids.te_form_prefix)
        self.ichidan_imperative: RequireForbidFlagField = self._add_flag(30, 1, Tags.Vocab.Matching.Requires.ichidan_imperative, Tags.Vocab.Matching.Forbids.ichidan_imperative)
        self.godan_potential: RequireForbidFlagField = self._add_flag(30, 1, Tags.Vocab.Matching.Requires.godan_potential, Tags.Vocab.Matching.Forbids.godan_potential)
        self.godan_imperative: RequireForbidFlagField = self._add_flag(30, 1, Tags.Vocab.Matching.Requires.godan_imperative, Tags.Vocab.Matching.Forbids.godan_imperative)
        self.godan_imperative_prefix: RequireForbidFlagField = self._add_flag(30, 1, Tags.Vocab.Matching.Requires.godan_imperative_prefix, Tags.Vocab.Matching.Forbids.godan_imperative_prefix)
        self.single_token: RequireForbidFlagField = self._add_flag(30, 1, Tags.Vocab.Matching.Requires.single_token, Tags.Vocab.Matching.Requires.compound)
        self.sentence_end: RequireForbidFlagField = self._add_flag(10, 1, Tags.Vocab.Matching.Requires.sentence_end, Tags.Vocab.Matching.Forbids.sentence_end)
        self.sentence_start: RequireForbidFlagField = self._add_flag(10, 1, Tags.Vocab.Matching.Requires.sentence_start, Tags.Vocab.Matching.Forbids.sentence_start)
        self.surface: RequireForbidFlagField = self._add_flag(10, 1, Tags.Vocab.Matching.Requires.surface, Tags.Vocab.Matching.Forbids.surface)
        self.yield_last_token: RequireForbidFlagField = YieldLastTokenToOverlappingCompound(vocab)
        self._all_flags.append(self.yield_last_token)
        self._match_weight: int | None = None

    def _add_flag(self, required_weight: int, forbidden_weight: int, required_tag: Tag, forbidden_tag: Tag) -> RequireForbidFlagField:
        flag_field = RequireForbidFlagField(self._vocab, required_weight, forbidden_weight, required_tag, forbidden_tag)
        self._all_flags.append(flag_field)
        return flag_field

    @property
    def all_flags(self) -> Iterable[RequireForbidFlagField]: return self._all_flags

    @property
    def match_weight(self) -> int: return sum(flag.match_weight for flag in self._all_flags)

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
        self._custom_requirements_weight: int | None = None

    @property
    def configurable_rules(self) -> VocabNoteMatchingRules: return self._rules()

    @property
    def custom_requirements_weight(self) -> int:
        if self._custom_requirements_weight is None:
            self._custom_requirements_weight = self.requires_forbids.match_weight + self._rules().match_weight
        return self._custom_requirements_weight

    @override
    def __repr__(self) -> str:
        builder = SkipFalsyValuesDebugReprBuilder()
        for flag in self.requires_forbids.all_flags:
            builder.prop(f"requires_{flag.name}", flag.is_required)
            builder.prop(f"forbids_{flag.name}", flag.is_forbidden)

        return (SkipFalsyValuesDebugReprBuilder()
                .flag("is_inflecting_word", self.bool_flags.is_inflecting_word.is_set())
                .flag("is_poison_word", self.bool_flags.is_poison_word.is_set())
                .flag("match_with_preceding_vowel", self.bool_flags.match_with_preceding_vowel.is_set())
                .flag("question_overrides_form", self.bool_flags.question_overrides_form.is_set())
                .flag("is_compositionally_transparent_compound", self.bool_flags.is_compositionally_transparent_compound.is_set())
                .include(self.configurable_rules).repr)
