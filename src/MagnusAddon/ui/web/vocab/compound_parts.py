from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from note.vocabulary.vocabnote import VocabNote
from sysutils.ex_str import newline
from typed_linq_collections.collections.q_set import QSet
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer

if TYPE_CHECKING:
    from note.jpnote import NoteId


class CompoundPart(Slots):
    def __init__(self, vocab_note: VocabNote, depth: int = 0) -> None:
        self.vocab_note: VocabNote = vocab_note
        self.depth: int = depth

def _create_classes(_vocab: VocabNote, depth: int = 0) -> str:
    # noinspection DuplicatedCode
    classes = " ".join(_vocab.get_meta_tags())
    classes += f" compound_part_depth_{depth}"
    return classes

def render_vocab_list(vocab_list: list[CompoundPart], title: str, css_class: str, reading: bool = True) -> str:
    def render_readings(_vocab_wrapper: CompoundPart) -> str:
        _vocab_note = _vocab_wrapper.vocab_note
        readings = ", ".join(_vocab_note.readings.get())
        return f"""<span class="clipboard vocabReading">{readings}</span>""" if reading and readings != _vocab_note.question.raw else ""

    return f'''
             <div class="relatedVocabListDiv page_section {css_class}">
                <div class="page_section_title">{title}</div>
                <div class="vocabHomophonesList">
                    <div>
                        {newline.join([f"""
                        <div class="relatedVocab {_create_classes(_vocab_wrapper.vocab_note, _vocab_wrapper.depth)}">
                            <audio src="{_vocab_wrapper.vocab_note.audio.get_primary_audio_path()}"></audio><a class="play-button"></a>
                            <span class="question clipboard">{_vocab_wrapper.vocab_note.question.disambiguation_name}</span>
                            {render_readings(_vocab_wrapper)}
                            {_vocab_wrapper.vocab_note.meta_data.meta_tags_html(no_sentense_statistics=True)}
                            <span class="meaning"> {_vocab_wrapper.vocab_note.get_answer()}</span>
                        </div>
                        """ for _vocab_wrapper in vocab_list])}
                    </div>
                </div>
            </div>
            '''

def get_compound_parts_recursive(vocab_note: VocabNote, depth: int = 0, visited: QSet[NoteId] | None = None) -> list[CompoundPart]:
    if visited is None: visited = QSet()
    if vocab_note.get_id() in visited: return []

    visited.add(vocab_note.get_id())

    compound_parts = vocab_note.compound_parts.primary_parts_notes()  # ex_sequence.flatten([app.col().vocab.with_form_prefer_exact_match(part) for part in vocab_note.compound_parts.primary()])

    result: list[CompoundPart] = []

    for part in compound_parts:
        wrapper = CompoundPart(part, depth)
        result.append(wrapper)
        nested_parts = get_compound_parts_recursive(part, depth + 1, visited)
        result.extend(nested_parts)

    return result

# noinspection PyUnusedFunction
def generate_compounds(_vocab_note: VocabNote) -> str:
    compound_parts = get_compound_parts_recursive(_vocab_note)
    return render_vocab_list(compound_parts, "compound parts", css_class="compound_parts") if compound_parts else ""

def init() -> None:
    # noinspection PyStatementEffect
    PrerenderingAnswerContentRenderer(VocabNote, {  # noqa: B018
            "##VOCAB_COMPOUNDS##": generate_compounds,
    }).render
