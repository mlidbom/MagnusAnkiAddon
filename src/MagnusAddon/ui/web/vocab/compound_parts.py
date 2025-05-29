from __future__ import annotations

from ankiutils import app
from aqt import gui_hooks
from note.vocabulary.vocabnote import VocabNote
from sysutils.ex_str import newline
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


def _create_classes(_vocab: VocabNote) -> str:
    # noinspection DuplicatedCode
    tags = list(_vocab.meta_data.priority_spec().tags)
    tags.sort()
    classes = " ".join([f"""common_ness_{prio}""" for prio in tags])
    classes += f""" {_vocab.meta_data.priority_spec().priority_string}"""
    classes += " " + " ".join(_vocab.get_meta_tags())
    return classes

def render_vocab_list(vocab_list: list[VocabNote], title: str, css_class: str, reading: bool = True) -> str:
    def render_readings(_vocab_note: VocabNote) -> str:
        return f"""<span class="clipboard vocabReading">{", ".join(_vocab_note.readings.get())}</span>""" if reading else ""

    return f'''
             <div class="relatedVocabListDiv page_section {css_class}">
                <div class="page_section_title">{title}</div>
                <div class="vocabHomophonesList">
                    <div>
                        {newline.join([f"""
                        <div class="relatedVocab {_create_classes(_vocab_note)}">
                            <audio src="{_vocab_note.audio.get_primary_audio_path()}"></audio><a class="play-button"></a>
                            <span class="question clipboard">{_vocab_note.get_question()}</span>
                            {render_readings(_vocab_note)}
                            {_vocab_note.meta_data.meta_tags_html(True)}
                            <span class="meaning"> {_vocab_note.get_answer()}</span>
                        </div>
                        """ for _vocab_note in vocab_list])}
                    </div>
                </div>
            </div>
            '''

def generate_compounds(_vocab_note: VocabNote) -> str:
    vocabs = _vocab_note.compound_parts.get()
    compound_parts = app.col().vocab.with_any_form_in_prefer_exact_match(vocabs)
    return render_vocab_list(compound_parts, "compound parts", css_class="compound_parts") if compound_parts else ""


def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(VocabNote, {
        "##VOCAB_COMPOUNDS##": generate_compounds,
    }).render)
