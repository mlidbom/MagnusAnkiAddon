from __future__ import annotations

from ankiutils import app
from aqt import gui_hooks
from note.vocabulary.vocabnote import VocabNote
from sysutils.ex_str import newline
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


class CompoundPart:
    def __init__(self, vocab_note: VocabNote, depth: int = 0) -> None:
        self.vocab_note = vocab_note
        self.depth = depth

def _create_classes(_vocab: VocabNote, depth: int = 0) -> str:
    # noinspection DuplicatedCode
    tags = list(_vocab.meta_data.priority_spec().tags)
    tags.sort()
    classes = " ".join([f"""common_ness_{prio}""" for prio in tags])
    classes += f""" {_vocab.meta_data.priority_spec().priority_string}"""
    classes += " " + " ".join(_vocab.get_meta_tags())
    classes += f" compound_part_depth_{depth}"
    return classes

def render_vocab_list(vocab_list: list[CompoundPart], title: str, css_class: str, reading: bool = True) -> str:
    def render_readings(_vocab_wrapper: CompoundPart) -> str:
        _vocab_note = _vocab_wrapper.vocab_note
        readings = ", ".join(_vocab_note.readings.get())
        return f"""<span class="clipboard vocabReading">{readings}</span>""" if reading and readings != _vocab_note.get_question() else ""

    return f'''
             <div class="relatedVocabListDiv page_section {css_class}">
                <div class="page_section_title">{title}</div>
                <div class="vocabHomophonesList">
                    <div>
                        {newline.join([f"""
                        <div class="relatedVocab {_create_classes(_vocab_wrapper.vocab_note, _vocab_wrapper.depth)}">
                            <audio src="{_vocab_wrapper.vocab_note.audio.get_primary_audio_path()}"></audio><a class="play-button"></a>
                            <span class="question clipboard">{_vocab_wrapper.vocab_note.get_question()}</span>
                            {render_readings(_vocab_wrapper)}
                            {_vocab_wrapper.vocab_note.meta_data.meta_tags_html(display_extended_sentence_statistics=False)}
                            <span class="meaning"> {_vocab_wrapper.vocab_note.get_answer()}</span>
                        </div>
                        """ for _vocab_wrapper in vocab_list])}
                    </div>
                </div>
            </div>
            '''

def get_compound_parts_recursive(vocab_note: VocabNote, depth: int = 0, visited: set = None) -> list[CompoundPart]:
    if visited is None: visited = set()
    if vocab_note.get_id() in visited: return []

    visited.add(vocab_note.get_id())

    compound_parts = app.col().vocab.with_any_form_in_prefer_exact_match(vocab_note.compound_parts.get())

    result = []

    for part in compound_parts:
        wrapper = CompoundPart(part, depth)
        result.append(wrapper)
        nested_parts = get_compound_parts_recursive(part, depth + 1, visited)
        result.extend(nested_parts)

    return result

def generate_compounds(_vocab_note: VocabNote) -> str:
    compound_parts = get_compound_parts_recursive(_vocab_note)
    return render_vocab_list(compound_parts, "compound parts", css_class="compound_parts") if compound_parts else ""

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(VocabNote, {
        "##VOCAB_COMPOUNDS##": generate_compounds,
    }).render)