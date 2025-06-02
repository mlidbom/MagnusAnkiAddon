from __future__ import annotations

import note.vocabulary.vocabnote_sorting
from ankiutils import app
from aqt import gui_hooks
from note.vocabulary.vocabnote import VocabNote
from sysutils import ex_sequence
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

def render_vocab_list(vocab_list: list[VocabNote], title: str, css_class: str, reading: bool = True, no_sentense_statistics: bool = True) -> str:
    def render_readings(_vocab_note: VocabNote) -> str:
        readings = ", ".join(_vocab_note.readings.get())
        return f"""<span class="clipboard vocabReading">{readings}</span>""" if reading and readings != _vocab_note.get_question() else ""

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
                            {_vocab_note.meta_data.meta_tags_html(no_sentense_statistics=no_sentense_statistics)}
                            <span class="meaning"> {_vocab_note.get_answer()}</span>
                        </div>
                        """ for _vocab_note in vocab_list])}
                    </div>
                </div>
            </div>
            '''

def generate_homophones_html_list(vocab_note: VocabNote) -> str:
    forms = ex_sequence.flatten([app.col().vocab.with_question(reading) for reading in vocab_note.forms.all_set()])
    forms = [form for form in forms if form.get_id() != vocab_note.get_id()]
    forms = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(forms)

    forms_set = set(forms) | {vocab_note}

    homophones = ex_sequence.flatten([app.col().vocab.with_reading(reading) for reading in vocab_note.readings.get()])
    homophones = [homophone for homophone in homophones if homophone not in forms_set]
    homophones = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(homophones)

    return render_vocab_list(homophones, "homophones", css_class="homophones") if homophones else ""

def generate_synonyms_meaning_html_list(_vocab_note: VocabNote) -> str:
    synonym_notes = _vocab_note.related_notes.synonyms.notes()
    synonym_notes = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(synonym_notes)

    return render_vocab_list(synonym_notes, "synonyms", css_class="similar") if synonym_notes else ""

def generate_antonyms_meaning_html_list(_vocab_note: VocabNote) -> str:
    antonym_notes = _vocab_note.related_notes.antonyms.notes()
    antonym_notes = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(antonym_notes)

    return render_vocab_list(antonym_notes, "antonyms", css_class="similar") if antonym_notes else ""

def generate_see_also_html_list(_vocab_note: VocabNote) -> str:
    see_also = _vocab_note.related_notes.see_also.notes()
    see_also = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(see_also)

    return render_vocab_list(see_also, "see also", css_class="similar") if see_also else ""

def generate_confused_with_html_list(_vocab_note: VocabNote) -> str:
    vocabs = list(_vocab_note.related_notes.confused_with.get())
    confused_with = app.col().vocab.with_any_form_in_prefer_exact_match(vocabs)
    confused_with = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(confused_with)

    return render_vocab_list(confused_with, "confused with", css_class="confused_with") if confused_with else ""

def generate_ergative_twin_html(_vocab_note: VocabNote) -> str:
    ergative_twin = app.col().vocab.with_form_prefer_exact_match(_vocab_note.related_notes.ergative_twin.get())
    return render_vocab_list(ergative_twin, "ergative twin", css_class="ergative_twin") if ergative_twin else ""

def generate_derived_from(_vocab_note: VocabNote) -> str:
    part = _vocab_note.related_notes.derived_from.get()
    derived_from = app.col().vocab.with_form_prefer_exact_match(part)
    return render_vocab_list(derived_from, "derived from", css_class="derived_from") if derived_from else ""

def generate_in_compounds_list(_vocab_note: VocabNote) -> str:
    compound_parts = app.col().vocab.with_compound_part(_vocab_note.question.without_noise_characters())
    return render_vocab_list(compound_parts, "part of compound", css_class="in_compound_words") if compound_parts else ""

def generate_stem_in_compounds_list(_vocab_note: VocabNote) -> str:
    if _vocab_note.question.stems().masu_stem() is None: return ""
    compound_parts = app.col().vocab.with_compound_part(_vocab_note.question.stems().masu_stem() or "")
    return render_vocab_list(compound_parts, "masu stem is part of compound", css_class="in_compound_words") if compound_parts else ""

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
    forms = ex_sequence.flatten([app.col().vocab.with_question(form) for form in vocab_note.forms.all_set()])
    forms = [form for form in forms if form.get_id() != vocab_note.get_id()]
    forms = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(forms)

    return render_vocab_list([vocab_note] + forms, "forms", css_class="forms", no_sentense_statistics=False) if forms else ""

def generate_meta_tags(vocab_note: VocabNote) -> str:
    return vocab_note.meta_data.meta_tags_html(True)

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(VocabNote, {
        "##FORMS_LIST##": generate_forms_list,
        "##IN_COMPOUNDS##": generate_in_compounds_list,
        "##STEM_IN_COMPOUNDS##": generate_stem_in_compounds_list,
        "##DERIVED_VOCABULARY##": generate_derived_list,
        "##ERGATIVE_TWIN##": generate_ergative_twin_html,
        "##DERIVED_FROM##": generate_derived_from,
        "##HOMOPHONES_LIST##": generate_homophones_html_list,
        "##SYNONYMS_LIST##": generate_synonyms_meaning_html_list,
        "##SEE_ALSO_LIST##": generate_see_also_html_list,
        "##ANTONYMS_LIST##": generate_antonyms_meaning_html_list,
        "##CONFUSED_WITH_LIST##": generate_confused_with_html_list,
        "##VOCAB_META_TAGS_HTML##": generate_meta_tags,
        "##VOCAB_CLASSES##": _create_classes,
        "##STEM_VOCABULARY##": generate_stem_vocabs,
        "##IS_STEM_OF##": generate_stem_of_vocabs
    }).render)
