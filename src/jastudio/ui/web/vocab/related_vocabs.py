from __future__ import annotations

import note.vocabulary.vocabnote_sorting
from jastudio.ankiutils import app
from aqt import gui_hooks
from language_services import conjugator
from note.vocabulary.vocabnote import VocabNote
from sysutils.ex_str import newline
from typed_linq_collections.q_iterable import query
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


def _create_classes(_vocab: VocabNote) -> str:
    return " ".join(_vocab.get_meta_tags())

def render_vocab_list(vocab_list: list[VocabNote], title: str, css_class: str, reading: bool = True, no_sentense_statistics: bool = True) -> str:
    def render_readings(_vocab_note: VocabNote) -> str:
        readings = ", ".join(_vocab_note.readings.get())
        return f"""<span class="clipboard vocabReading">{readings}</span>""" if reading and readings != _vocab_note.get_question() else ""

    if len(vocab_list) == 0: return ""

    return f'''
             <div class="relatedVocabListDiv page_section {css_class}">
                <div class="page_section_title">{title}</div>
                <div class="vocabHomophonesList">
                    <div>
                        {newline.join([f"""
                        <div class="relatedVocab {_create_classes(_vocab_note)}">
                            <audio src="{_vocab_note.audio.get_primary_audio_path()}"></audio><a class="play-button"></a>
                            <span class="question clipboard">{_vocab_note.question.disambiguation_name}</span>
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
    homophone_notes = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(vocab_note.related_notes.homophones_notes())
    if len(homophone_notes) > 0:
        homophone_notes = [vocab_note] + homophone_notes
    return render_vocab_list(homophone_notes, "homophones", css_class="homophones")

def generate_synonyms_meaning_html_list(_vocab_note: VocabNote) -> str:
    synonym_notes = _vocab_note.related_notes.synonyms.notes()
    perfect_synonyms = set(_vocab_note.related_notes.perfect_synonyms.notes())
    synonym_notes = query(synonym_notes).where(lambda synonym: synonym not in perfect_synonyms).to_list()
    synonym_notes = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(synonym_notes)

    return render_vocab_list(synonym_notes, "synonyms", css_class="similar")

def generate_perfect_synonyms_meaning_html_list(_vocab_note: VocabNote) -> str:
    perfect_synonym_notes = _vocab_note.related_notes.perfect_synonyms.notes()
    perfect_synonym_notes = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(perfect_synonym_notes)

    return render_vocab_list(perfect_synonym_notes, "perfect synonyms, answer automatically synced", css_class="similar")

def generate_antonyms_meaning_html_list(_vocab_note: VocabNote) -> str:
    antonym_notes = _vocab_note.related_notes.antonyms.notes()
    antonym_notes = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(antonym_notes)

    return render_vocab_list(antonym_notes, "antonyms", css_class="similar")

def generate_see_also_html_list(_vocab_note: VocabNote) -> str:
    see_also = _vocab_note.related_notes.see_also.notes()
    see_also = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(see_also)

    return render_vocab_list(see_also, "see also", css_class="similar")

def generate_confused_with_html_list(_vocab_note: VocabNote) -> str:
    vocabs = list(_vocab_note.related_notes.confused_with.get())
    confused_with = app.col().vocab.with_any_form_in_prefer_disambiguation_name_or_exact_match(vocabs)
    confused_with = note.vocabulary.vocabnote_sorting.sort_vocab_list_by_studying_status(confused_with)

    return render_vocab_list(confused_with, "confused with", css_class="confused_with")

def generate_ergative_twin_html(_vocab_note: VocabNote) -> str:
    ergative_twin = app.col().vocab.with_form_prefer_disambiguation_name_or_exact_match(_vocab_note.related_notes.ergative_twin.get())
    return render_vocab_list(ergative_twin, "ergative twin", css_class="ergative_twin")

def generate_derived_from(_vocab_note: VocabNote) -> str:
    part = _vocab_note.related_notes.derived_from.get()
    derived_from = app.col().vocab.with_form_prefer_disambiguation_name_or_exact_match(part)
    return render_vocab_list(derived_from, "derived from", css_class="derived_from")

def generate_in_compounds_list(_vocab_note: VocabNote) -> str:
    forms = conjugator.get_vocab_stems(_vocab_note) + [_vocab_note.question.raw]
    def prefer_compounds_starting_with_this_vocab(_vocab: VocabNote) -> int:
        question = _vocab.question.raw
        return 0 if any(form for form in forms if question.startswith(form)) else 1

    in_compounds = (query(_vocab_note.related_notes.in_compounds())
                    .order_by(lambda it: it.get_question())
                    .order_by(prefer_compounds_starting_with_this_vocab)
                    .take(30).to_list())
    return render_vocab_list(in_compounds, "part of compound", css_class="in_compound_words")

def generate_stem_in_compounds_list(_vocab_note: VocabNote) -> str:
    if _vocab_note.question.stems().masu_stem() is None: return ""
    masu_stem_in_compounds = app.col().vocab.with_compound_part(_vocab_note.question.stems().masu_stem() or "")[:30]
    return render_vocab_list(masu_stem_in_compounds, "masu stem is part of compound", css_class="in_compound_words")

def generate_derived_list(_vocab_note: VocabNote) -> str:
    derived_vocabs = app.col().vocab.derived_from(_vocab_note.get_question())
    return render_vocab_list(derived_vocabs, "derived vocabulaty", css_class="derived_vocabulary")

def generate_stem_vocabs(_vocab_note: VocabNote) -> str:
    return render_vocab_list(_vocab_note.related_notes.stems_notes().to_list(), "conjugation forms", css_class="stem_vocabulary")

def generate_stem_of_vocabs(_vocab_note: VocabNote) -> str:
    return render_vocab_list(app.col().vocab.with_stem(_vocab_note.get_question()), "dictionary form", css_class="is_stem_of")

def generate_forms_list(vocab_note: VocabNote) -> str:
    forms = vocab_note.forms.all_list_notes_by_sentence_count()
    return render_vocab_list(forms, "forms", css_class="forms", no_sentense_statistics=False) if len(forms) > 1 else ""

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
            "##PERFECT_SYNONYMS_LIST##": generate_perfect_synonyms_meaning_html_list,
            "##SYNONYMS_LIST##": generate_synonyms_meaning_html_list,
            "##SEE_ALSO_LIST##": generate_see_also_html_list,
            "##ANTONYMS_LIST##": generate_antonyms_meaning_html_list,
            "##CONFUSED_WITH_LIST##": generate_confused_with_html_list,
            "##VOCAB_META_TAGS_HTML##": generate_meta_tags,
            "##VOCAB_CLASSES##": _create_classes,
            "##STEM_VOCABULARY##": generate_stem_vocabs,
            "##IS_STEM_OF##": generate_stem_of_vocabs
    }).render)
