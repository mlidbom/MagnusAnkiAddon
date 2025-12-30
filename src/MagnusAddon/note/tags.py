from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots
from sysutils.bit_flags_set import BitFlagsSet
from sysutils.memory_usage import string_auto_interner
from typed_linq_collections.collections.q_dict import QDict
from typed_linq_collections.q_iterable import QIterable, query

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from typed_linq_collections.collections.q_list import QList

class Tag(Slots):
    _used_ids: set[int] = set()
    _by_id: QDict[int, Tag] = QDict()
    _by_name: QDict[str, Tag] = QDict()

    _secret: str = "lahoeubaoehbl2304985 iimjj08dm0"

    def __init__(self, name: str, secret_don_call_this_method: str) -> None:
        if secret_don_call_this_method != self._secret:
            raise ValueError("This is a private constructor, don't call it from outside the class")

        id = len(Tag._used_ids)

        self.name: str = name
        self.id: int = id
        self.bit: int = 1 << id

        Tag._used_ids.add(id)
        Tag._by_id[id] = self
        Tag._by_name[name] = self

    @staticmethod
    def _add_tag(name: str) -> Tag: return Tag(name, Tag._secret)

    @staticmethod
    def from_name(name: str) -> Tag:
        return Tag._by_name.get_or_add(name, Tag._add_tag)

    @staticmethod
    def from_id(id: int) -> Tag:
        return Tag._by_id[id]

    @staticmethod
    def all() -> QIterable[Tag]: return Tag._by_id.qvalues()

class TagSet(Slots):
    """Stores a set of Tags as a compact bitfield."""
    _flags: BitFlagsSet
    
    def __init__(self, initial_tags: Iterable[Tag] | None = None) -> None:
        self._flags = BitFlagsSet()
        if initial_tags is not None:
            for tag in initial_tags:
                self.set_tag(tag)

    def has_tag(self, tag: Tag) -> bool:
        return self._flags.has(tag.id)

    def set_tag(self, tag: Tag) -> None:
        self._flags.set_flag(tag.id)

    def unset_tag(self, tag: Tag) -> None:
        self._flags.unset_flag(tag.id)

    def has_name(self, tag_name: str) -> bool:
        return self.has_tag(Tag.from_name(tag_name))

    def set_name(self, tag_name: str) -> None:
        self.set_tag(Tag.from_name(tag_name))

    def unset_name(self, tag_name: str) -> None:
        self.unset_tag(Tag.from_name(tag_name))

    def __contains__(self, tag: Tag) -> bool:  # Support 'tag in tagset' syntax.
        return self.has_tag(tag)

    def __iter__(self) -> Iterator[Tag]:
        for bit_pos in self._flags.all_flags():
            yield Tag.from_id(bit_pos)

    @staticmethod
    def from_string_list(tags: QList[str]) -> TagSet:
        return TagSet(tags.select(Tag.from_name))

    _interned_string_lists: QDict[int, list[str]] = QDict()
    def to_interned_string_list(self) -> list[str]:
        bitfield = self._flags.bitfield
        if bitfield not in self._interned_string_lists:
            sorted_name_list = query(self).select(lambda it: it.name).order_by(lambda it: it).to_list()
            self._interned_string_lists[bitfield] = string_auto_interner.auto_intern_qlist(sorted_name_list)

        return self._interned_string_lists[bitfield]

f_root = "-::"
f_sentence: str = f"{f_root}sentence::"
f_kanji: str = f"{f_root}kanji::"
f_sentence_uses: str = f"{f_sentence}uses::"
f_vocab: str = f"{f_root}vocab::"
f_vocab_matching: str = f"{f_vocab}matching::"
f_vocab_matching_requires: str = f"{f_vocab_matching}requires::"
f_vocab_matching_forbids: str = f"{f_vocab_matching}forbids::"
f_vocab_matching_todo: str = f"{f_vocab_matching}todo::"
f_vocab_matching_uses: str = f"{f_vocab_matching}uses::"
f_source = "source::"

class Tags(Slots):
    class Sentence(Slots):
        class Uses(Slots):
            incorrect_matches: Tag = Tag.from_name(f"{f_sentence_uses}incorrect-matches")
            hidden_matches: Tag = Tag.from_name(f"{f_sentence_uses}hidden-matches")

    class Kanji(Slots):
        is_radical: Tag = Tag.from_name(f"{f_kanji}is-radical")
        is_radical_purely: Tag = Tag.from_name(f"{f_kanji}is-radical-purely")
        is_radical_silent: Tag = Tag.from_name(f"{f_kanji}is-radical-silent")
        in_vocab_main_form: Tag = Tag.from_name(f"{f_kanji}in-vocab-main-form")
        in_any_vocab_form: Tag = Tag.from_name(f"{f_kanji}in-any-vocab-form")

        with_single_kanji_vocab: Tag = Tag.from_name(f"{f_kanji}single-kanji-vocab")
        with_single_kanji_vocab_with_different_reading: Tag = Tag.from_name(f"{f_kanji}single-kanji-vocab-with-different-reading")
        with_studying_single_kanji_vocab_with_different_reading: Tag = Tag.from_name(f"{f_kanji}studying-single-kanji-vocab-with-different-reading")
        with_no_primary_on_readings: Tag = Tag.from_name(f"{f_kanji}no-primary-on-readings")
        with_no_primary_readings: Tag = Tag.from_name(f"{f_kanji}no-primary-readings")
        with_studying_vocab: Tag = Tag.from_name(f"{f_kanji}studying-vocab")
        with_vocab_with_primary_on_reading: Tag = Tag.from_name(f"{f_kanji}has-vocab-with-primary-on-reading")
        with_studying_vocab_with_primary_on_reading: Tag = Tag.from_name(f"{f_kanji}studying-vocab-with-primary-on-reading")

        has_studying_vocab_with_no_matching_primary_reading: Tag = Tag.from_name(f"{f_kanji}has-studying-vocab-with-no-matching-primary-reading")
        has_studying_vocab_for_each_primary_reading: Tag = Tag.from_name(f"{f_kanji}has-studying-vocab-for-each-primary-reading")
        has_primary_reading_with_no_studying_vocab: Tag = Tag.from_name(f"{f_kanji}has-primary-reading-with-no-studying-vocab")
        has_non_primary_on_reading_vocab: Tag = Tag.from_name(f"{f_kanji}has-non-primary-on-reading-vocab")
        has_non_primary_on_reading_vocab_with_only_known_kanji: Tag = Tag.from_name(f"{f_kanji}has-non-primary-on-reading-vocab-with-only-known-kanji")

    class Vocab(Slots):
        root: str = f_vocab  # Keep as string for startswith() checks
        has_no_studying_sentences: Tag = Tag.from_name(f"{f_vocab}has-no-studying-sentences")
        question_overrides_form: Tag = Tag.from_name(f"{f_vocab}question-overrides-form")

        class Matching(Slots):
            yield_last_token_to_overlapping_compound: Tag = Tag.from_name(f"{f_vocab_matching}yield-last-token-to-upcoming-compound")
            is_poison_word: Tag = Tag.from_name(f"{f_vocab_matching}is-poison-word")
            is_inflecting_word: Tag = Tag.from_name(f"{f_vocab_matching}is-inflecting-word")

            class Requires(Slots):
                a_stem: Tag = Tag.from_name(f"{f_vocab_matching_requires}a-stem")
                e_stem: Tag = Tag.from_name(f"{f_vocab_matching_requires}e-stem")
                past_tense_stem: Tag = Tag.from_name(f"{f_vocab_matching_requires}past-tense-stem")
                ichidan_imperative: Tag = Tag.from_name(f"{f_vocab_matching_requires}ichidan_imperative")
                godan_potential: Tag = Tag.from_name(f"{f_vocab_matching_requires}godan_potential")
                godan_imperative: Tag = Tag.from_name(f"{f_vocab_matching_requires}godan_imperative")
                godan_imperative_prefix: Tag = Tag.from_name(f"{f_vocab_matching_forbids}godan_imperative_prefix")
                te_form_stem: Tag = Tag.from_name(f"{f_vocab_matching_requires}te-form-stem")
                sentence_end: Tag = Tag.from_name(f"{f_vocab_matching_requires}sentence-end")
                sentence_start: Tag = Tag.from_name(f"{f_vocab_matching_requires}sentence-start")
                exact_match: Tag = Tag.from_name(f"{f_vocab_matching_requires}exact-match")
                single_token: Tag = Tag.from_name(f"{f_vocab_matching_requires}single-token")
                compound: Tag = Tag.from_name(f"{f_vocab_matching_requires}compound")

            class Forbids(Slots):
                a_stem: Tag = Tag.from_name(f"{f_vocab_matching_forbids}a-stem")
                e_stem: Tag = Tag.from_name(f"{f_vocab_matching_forbids}e-stem")
                past_tense_stem: Tag = Tag.from_name(f"{f_vocab_matching_forbids}past-tense-stem")
                ichidan_imperative: Tag = Tag.from_name(f"{f_vocab_matching_forbids}ichidan_imperative")
                godan_potential: Tag = Tag.from_name(f"{f_vocab_matching_forbids}godan_potential")
                godan_imperative: Tag = Tag.from_name(f"{f_vocab_matching_forbids}godan_imperative")
                godan_imperative_prefix: Tag = Tag.from_name(f"{f_vocab_matching_forbids}godan_imperative_prefix")
                te_form_stem: Tag = Tag.from_name(f"{f_vocab_matching_forbids}te-form-stem")
                sentence_end: Tag = Tag.from_name(f"{f_vocab_matching_forbids}sentence-end")
                sentence_start: Tag = Tag.from_name(f"{f_vocab_matching_forbids}sentence-start")
                exact_match: Tag = Tag.from_name(f"{f_vocab_matching_forbids}exact-match")
                auto_yielding: Tag = Tag.from_name(f"{f_vocab_matching_forbids}auto_yielding")

            class Todo(Slots):
                with_preceding_vowel: Tag = Tag.from_name(f"{f_vocab_matching_todo}match-with-preceding-vowel")

            class Uses(Slots):
                prefix_is_not: Tag = Tag.from_name(f"{f_vocab_matching_uses}prefix-is-not")
                suffix_is_not: Tag = Tag.from_name(f"{f_vocab_matching_uses}suffix-is-not")
                required_prefix: Tag = Tag.from_name(f"{f_vocab_matching_uses}required-prefix")
                surface_is_not: Tag = Tag.from_name(f"{f_vocab_matching_uses}surface-is-not")

    priority_folder: str = f"{f_root}priority::"  # Keep as string for startswith() checks

    class Source(Slots):
        folder: str = f_source  # Keep as string for startswith() checks
        immersion_kit: Tag = Tag.from_name(f"{f_source}immersion_kit")
        jamdict: Tag = Tag.from_name(f"{f_source}jamdict")

    DisableKanaOnly: Tag = Tag.from_name("_disable_uk")
    UsuallyKanaOnly: Tag = Tag.from_name("_uk")
    TTSAudio: Tag = Tag.from_name("_tts_audio")
