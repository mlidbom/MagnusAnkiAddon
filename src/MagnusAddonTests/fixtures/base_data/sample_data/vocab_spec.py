from __future__ import annotations

from typing import TYPE_CHECKING, override

from ex_autoslot import ProfilableAutoSlots

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote


class VocabSpec(ProfilableAutoSlots):
    # noinspection PyDefaultArgument
    def __init__(self, question: str,
                 answer: str | None = None,
                 readings: list[str] | None = None,
                 forms: list[str] | None = None,
                 tags: list[str] | None = None,
                 compounds: list[str] | None = None,
                 surface_not: set[str] | None = None,
                 yield_to_surface: set[str] | None = None,
                 prefix_not: set[str] | None = None,
                 suffix_not: set[str] | None = None,
                 tos: str | None = None,
                 prefix_in: set[str] | None = None) -> None:
        self.question: str = question
        self.answer: str = answer or question
        self.readings: list[str] = readings or [self.question]
        self.extra_forms: set[str] = set(forms if forms else [])
        self.tags: set[str] = set(tags if tags else [])
        self.compounds: list[str] = compounds if compounds else []
        self.surface_is_not: set[str] = surface_not if surface_not else set()
        self.yield_to_surface: set[str] = yield_to_surface if yield_to_surface else set()
        self.prefix_is_not: set[str] = prefix_not if prefix_not else set()
        self.suffix_is_not: set[str] = suffix_not if suffix_not else set()
        self.tos: str = tos if tos else ""
        self.required_prefix: set[str] = prefix_in if prefix_in else set()

    @override
    def __repr__(self) -> str:
        return f"""VocabSpec("{self.question}", "{self.answer}", {self.readings})"""

    @override
    def __hash__(self) -> int:
        return hash(self.question)

    @override
    def __eq__(self, other: object) -> bool:
        return (isinstance(other, VocabSpec)
                and other.question == self.question
                and other.answer == self.answer
                and other.readings == self.readings)

    def _initialize_note(self, vocab_note: VocabNote) -> None:
        vocab_note.compound_parts.set(self.compounds)

        if self.extra_forms:
            vocab_note.forms.set_set(vocab_note.forms.all_set() | self.extra_forms)

        for tag in self.tags:
            vocab_note.set_tag(tag)

        for excluded_surface in self.surface_is_not:
            vocab_note.matching_configuration.configurable_rules.surface_is_not.add(excluded_surface)

        for yield_to_surface in self.yield_to_surface:
            vocab_note.matching_configuration.configurable_rules.yield_to_surface.add(yield_to_surface)

        for forbidden_prefix in self.prefix_is_not:
            vocab_note.matching_configuration.configurable_rules.prefix_is_not.add(forbidden_prefix)

        for forbidden_suffix in self.suffix_is_not:
            vocab_note.matching_configuration.configurable_rules.suffix_is_not.add(forbidden_suffix)

        for required_prefix in self.required_prefix:
            vocab_note.matching_configuration.configurable_rules.required_prefix.add(required_prefix)

        if self.tos:
            vocab_note.parts_of_speech.set_raw_string_value(self.tos)

    def create_vocab_note(self) -> None:
        from note.vocabulary.vocabnote import VocabNote
        VocabNote.factory.create(self.question, self.answer, self.readings, self._initialize_note)
