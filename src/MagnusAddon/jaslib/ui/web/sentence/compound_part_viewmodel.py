from __future__ import annotations

from typing import TYPE_CHECKING

from ankiutils import app
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from configuration.settings import Settings
from typed_linq_collections.collections.q_set import QSet

if TYPE_CHECKING:
    from jaslib.note.jpnote import NoteId
    from jaslib.note.sentences.sentence_configuration import SentenceConfiguration
    from jaslib.note.vocabulary.vocabnote import VocabNote
    from jaslib.ui.web.sentence.match_viewmodel import MatchViewModel

class CompoundPartViewModel(Slots):
    def __init__(self, vocab_note: VocabNote, depth: int, config: SentenceConfiguration) -> None:
        self.vocab_note: VocabNote = vocab_note
        self.depth: int = depth
        self.question: str = vocab_note.get_question()
        self.answer: str = vocab_note.get_answer()
        self.readings: str = ", ".join(vocab_note.readings.get())
        self.audio_path: str = vocab_note.audio.get_primary_audio_path()
        self.meta_tags_html: str = vocab_note.meta_data.meta_tags_html(no_sentense_statistics=True)
        self.display_readings: bool = self.question != self.readings
        self.is_highlighted: bool = self.question in config.highlighted_words

        self.meta_tags_string: str = " ".join(vocab_note.get_meta_tags())
        self.meta_tags_string += f""" depth_{depth}"""
        self.meta_tags_string += " highlighted" if self.is_highlighted else ""

    @classmethod
    def get_compound_parts_recursive(cls, match_viewmodel: MatchViewModel, vocab_note: VocabNote, config: SentenceConfiguration, depth: int = 0, visited: QSet[NoteId] | None = None) -> list[CompoundPartViewModel]:
        if not Settings.hide_all_compounds():
            if not Settings.show_compound_parts_in_sentence_breakdown(): return []
            if visited is None: visited = QSet()
            if vocab_note.get_id() in visited: return []

            visited.add(vocab_note.get_id())

            result: list[CompoundPartViewModel] = []

            for part in vocab_note.compound_parts.primary_parts_notes():  # ex_sequence.flatten([app.col().vocab.with_form_prefer_exact_match(part) for part in vocab_note.compound_parts.primary()])
                wrapper = CompoundPartViewModel(part, depth, config)
                result.append(wrapper)
                nested_parts = cls.get_compound_parts_recursive(match_viewmodel, part, config, depth + 1, visited)
                result.extend(nested_parts)

            return result
        match = match_viewmodel.match
        if match.inspector.is_ichidan_covering_godan_potential:
            godan_base = match.word.start_location.token.base_form
            godan_potential_part_base = match.word.end_location.token.base_form
            godan = app.col().vocab.with_form_prefer_disambiguation_name_or_exact_match(godan_base)
            godan_potential = app.col().vocab.with_form_prefer_disambiguation_name_or_exact_match(godan_potential_part_base)
            if godan and godan_potential:
                return [(CompoundPartViewModel(godan[0], depth, config)),
                        (CompoundPartViewModel(godan_potential[0], depth, config))]
            return []
        # we may still have parts if janome tokenizes a word we consider a compound as a single token
        return (vocab_note.compound_parts.primary_parts_notes()
                .select(lambda _part: CompoundPartViewModel(_part, depth, config)).to_list())
