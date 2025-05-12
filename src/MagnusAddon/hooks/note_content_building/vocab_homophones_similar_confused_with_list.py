from __future__ import annotations

import note.vocabulary.vocabnote_sorting
from ankiutils import app
from aqt import gui_hooks
from hooks.note_content_building.content_renderer import PrerenderingAnswerContentRenderer
from note.vocabulary.vocabnote import VocabNote
from sysutils import ex_sequence
from sysutils.ex_str import newline


def _create_classes(_vocab: VocabNote) -> str:
    tags = list(_vocab.meta_data.priority_spec().tags)
    tags.sort()
    classes = " ".join([f"""common_ness_{prio}""" for prio in tags])
    classes += f""" {_vocab.meta_data.priority_spec().priority_string}"""
    classes += " " + " ".join(_vocab.get_meta_tags())
    return classes

def lookup_vocabs_prefer_exact_match(part:str) -> list[VocabNote]:
    matches: list[VocabNote] = app.col().vocab.with_form(part)
    exact_match = [voc for voc in matches if voc.get_question_without_noise_characters() == part]
    return exact_match if exact_match else matches

def lookup_vocabs_list_prefer_exact_match(vocabs:list[str]) -> list[VocabNote]:
    return ex_sequence.flatten([lookup_vocabs_prefer_exact_match(part) for part in vocabs])


def render_vocab_list(vocab_list: list[VocabNote], title:str, css_class:str, reading:bool = True) -> str:
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


def generate_homophones_html_list(vocab_note: VocabNote) -> str:
    forms = ex_sequence.flatten([app.col().vocab.with_question(reading) for reading in vocab_note.forms.unexcluded_set()])
    forms = [form for form in forms if form.get_id() != vocab_note.get_id()]
    forms = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(forms)

    forms_set = set(forms) | {vocab_note}

    homophones = ex_sequence.flatten([app.col().vocab.with_reading(reading) for reading in vocab_note.readings.get()])
    homophones = [homophone for homophone in homophones if homophone not in forms_set]
    homophones = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(homophones)

    return render_vocab_list(homophones, "homophones", css_class="homophones") if homophones else ""

def generate_similar_meaning_html_list(_vocab_note: VocabNote) -> str:
    similar = lookup_vocabs_list_prefer_exact_match(list(_vocab_note.related_notes.similar_meanings()))
    similar = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(similar)

    return render_vocab_list(similar, "similar", css_class="similar") if similar else ""

def generate_confused_with_html_list(_vocab_note: VocabNote) -> str:
    confused_with = lookup_vocabs_list_prefer_exact_match(list(_vocab_note.related_notes.confused_with.get()))
    confused_with = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(confused_with)

    return render_vocab_list(confused_with, "confused with", css_class="confused_with") if confused_with else ""

def generate_ergative_twin_html(_vocab_note: VocabNote) -> str:
    ergative_twin = lookup_vocabs_prefer_exact_match(_vocab_note.related_notes.ergative_twin())
    return render_vocab_list(ergative_twin, "ergative twin", css_class="ergative_twin") if ergative_twin else ""

def generate_derived_from(_vocab_note: VocabNote) -> str:
    derived_from = lookup_vocabs_prefer_exact_match(_vocab_note.related_notes.derived_from.get())
    return render_vocab_list(derived_from, "derived from", css_class="derived_from") if derived_from else ""

def generate_compounds(_vocab_note: VocabNote) -> str:
    compound_parts = lookup_vocabs_list_prefer_exact_match(_vocab_note.compound_parts.get())
    return render_vocab_list(compound_parts, "compound parts", css_class="compound_parts") if compound_parts else ""

def generate_in_compounds_list(_vocab_note: VocabNote) -> str:
    compound_parts = app.col().vocab.with_compound_part(_vocab_note.get_question_without_noise_characters())
    return render_vocab_list(compound_parts, "part of compound", css_class="in_compound_words") if compound_parts else ""

def generate_derived_list(_vocab_note: VocabNote) -> str:
    derived_vocabs = app.col().vocab.derived_from(_vocab_note.get_question())
    return render_vocab_list(derived_vocabs, "derived vocabulaty", css_class="derived_vocabulary") if derived_vocabs else ""

def generate_stem_vocabs(_vocab_note: VocabNote) -> str:
    stem_vocabs = ex_sequence.flatten([app.col().vocab.with_question(stem) for stem in (_vocab_note.conjugator.get_stems_for_primary_form())])
    return render_vocab_list(stem_vocabs, "conjugation forms", css_class="stem_vocabulary") if stem_vocabs else ""

def generate_stem_of_vocabs(_vocab_note: VocabNote) -> str:
    stem_of = app.col().vocab.with_stem(_vocab_note.get_question())
    return render_vocab_list(stem_of, "dictionary form", css_class="is_stem_of") if stem_of else ""

def generate_forms_list(vocab_note: VocabNote) -> str:
    forms = ex_sequence.flatten([app.col().vocab.with_question(form) for form in vocab_note.forms.unexcluded_set()])
    forms = [form for form in forms if form.get_id() != vocab_note.get_id()]
    forms = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(forms)

    return render_vocab_list([vocab_note] + forms, "forms", css_class="forms") if forms else ""

def generate_meta_tags(vocab_note:VocabNote) -> str:
    return vocab_note.meta_data.meta_tags_html(True)

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(VocabNote, {
        "##FORMS_LIST##": generate_forms_list,
        "##VOCAB_COMPOUNDS##": generate_compounds,
        "##IN_COMPOUNDS##": generate_in_compounds_list,
        "##DERIVED_VOCABULARY##": generate_derived_list,
        "##ERGATIVE_TWIN##": generate_ergative_twin_html,
        "##DERIVED_FROM##": generate_derived_from,
        "##HOMOPHONES_LIST##": generate_homophones_html_list,
        "##SIMILAR_MEANING_LIST##": generate_similar_meaning_html_list,
        "##CONFUSED_WITH_LIST##": generate_confused_with_html_list,
        "##VOCAB_META_TAGS_HTML##": generate_meta_tags,
        "##VOCAB_CLASSES##": _create_classes,
        "##STEM_VOCABULARY##": generate_stem_vocabs,
        "##IS_STEM_OF##": generate_stem_of_vocabs
    }).render)
