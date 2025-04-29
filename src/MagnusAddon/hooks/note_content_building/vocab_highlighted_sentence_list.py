from aqt import gui_hooks
from ankiutils import app
from hooks.note_content_building.content_renderer import PrerenderingAnswerContentRenderer
from note.note_constants import Mine
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import ex_sequence, ex_str, kana_utils
from sysutils.ex_str import newline

def generate_highlighted_sentences_html_list(_vocab_note: VocabNote) -> str:
    forms = [_vocab_note.get_question()] + list(_vocab_note.get_forms_without_noise_characters())
    forms = ex_sequence.remove_duplicates_while_retaining_order(forms)
    primary_form = _vocab_note.get_question_without_noise_characters()
    primary_form_forms = _vocab_note.get_text_matching_forms_for_primary_form()
    secondary_forms = [form for form in forms if form != primary_form]
    secondary_forms_forms = ex_str.sort_by_length_descending([form for form in _vocab_note.get_text_matching_forms_for_all_form() if form not in primary_form_forms])

    secondary_forms_containing_primary_form_forms = [form for form in secondary_forms_forms if any(pform for pform in primary_form_forms if pform in form)]

    derived_compounds = _vocab_note.in_compounds()
    derived_compounds_forms = ex_str.sort_by_length_descending(ex_sequence.flatten([der.get_text_matching_forms_for_all_form() for der in derived_compounds]))

    secondary_forms_vocab_notes = ex_sequence.flatten([app.col().vocab.with_question(v) for v in secondary_forms])
    secondary_forms_with_their_own_vocab_forms = ex_sequence.flatten([f.get_text_matching_forms_for_all_form() for f in secondary_forms_vocab_notes])

    secondary_forms_with_their_own_vocab_forms = ex_str.sort_by_length_descending(secondary_forms_with_their_own_vocab_forms)

    primary_form_forms = _vocab_note.get_text_matching_forms_for_primary_form()

    def contains_primary_form(_sentence: SentenceNote) -> bool:
        clean_sentence = ex_str.strip_html_and_bracket_markup(_sentence.get_question())


        return (not any(covering_secondary_form for covering_secondary_form in secondary_forms_containing_primary_form_forms if covering_secondary_form in clean_sentence)
                and any(base_form for base_form in primary_form_forms if base_form in clean_sentence))

    def contains_secondary_form_with_its_own_vocabulary_note(_sentence: SentenceNote) -> bool:
        clean_sentence = ex_str.strip_html_and_bracket_markup(_sentence.get_question())
        return any(base_form for base_form in secondary_forms_with_their_own_vocab_forms if base_form in clean_sentence)

    def format_sentence(html_sentence: str) -> str:
        clean_sentence = ex_str.strip_html_and_bracket_markup(html_sentence)

        for form in derived_compounds_forms:
            if form in clean_sentence:
                return clean_sentence.replace(form, f"""<span class="vocabInContext derivedCompoundForm">{form}</span>""")

        for form in secondary_forms_containing_primary_form_forms:
            if form in clean_sentence:
                return clean_sentence.replace(form, f"""<span class="vocabInContext secondaryForm">{form}</span>""")

        for form in primary_form_forms:
            if form in clean_sentence:
                return clean_sentence.replace(form, f"""<span class="vocabInContext primaryForm">{form}</span>""")

        for form in secondary_forms_forms:
            if form in clean_sentence:
                return clean_sentence.replace(form, f"""<span class="vocabInContext secondaryForm">{form}</span>""")

        return clean_sentence

    sorted_sentences: set[str] = set()
    highlighted_sentences = set(_vocab_note.get_user_highlighted_sentences())
    studying_sentences = set(_vocab_note.get_sentences_studying())

    def sort_sentences(_sentences:list[SentenceNote]) -> list[SentenceNote]:
        is_low_reliability_matching = kana_utils.is_only_kana(primary_form) and len(primary_form) <= 2

        #todo: downprioritize matches for forms with their own vocabnote. Also for such forms, exclude those forms from the matches shown in the vocab metadata
        def prefer_highlighted_for_low_reliability_matches(_sentence: SentenceNote) -> int: return 0 if is_low_reliability_matching and _sentence in highlighted_sentences else 1
        def prefer_highlighted(_sentence:SentenceNote) -> int: return 0 if _sentence in highlighted_sentences else 1
        def prefer_studying_read(_sentence:SentenceNote) -> int: return 0 if _sentence.is_studying_read() else 1
        def prefer_studying_listening(_sentence: SentenceNote) -> int: return 0 if _sentence.is_studying_listening() else 1
        def dislike_secondary_form_with_vocab(_sentence: SentenceNote) -> int: return 1 if not contains_primary_form(_sentence) and contains_secondary_form_with_its_own_vocabulary_note(_sentence) else 0
        def prefer_primary_form(_sentence:SentenceNote) -> int: return 0 if contains_primary_form(_sentence) else 1
        def dislike_tts_sentences(_sentence:SentenceNote) -> int: return 1 if _sentence.has_tag(Mine.Tags.TTSAudio) else 0
        def prefer_short_questions(_sentence:SentenceNote) -> int: return len(_sentence.get_question())
        def prefer_lower_priority_tag_values(_sentence: SentenceNote) -> int: return _sentence.priority_tag_value()
        def dislike_no_translation(_sentence: SentenceNote) -> int: return 1 if not _sentence.get_answer().strip() else 0

        def prefer_non_duplicates(_sentence:SentenceNote) -> int:
            if _sentence.get_question() in sorted_sentences: return 1
            sorted_sentences.add(_sentence.get_question())
            return 0

        def dislike_sentences_containing_secondary_form(_sentence:SentenceNote) -> int:
            clean_sentence = ex_str.strip_html_and_bracket_markup(_sentence.get_question())
            return 1 if any(base_forms for base_forms in secondary_forms_forms if any(base_form for base_form in base_forms if base_form in clean_sentence)) else 0

        def dislike_contains_derived_compound(_sentence: SentenceNote) -> int:
            clean_sentence = ex_str.strip_html_and_bracket_markup(_sentence.get_question())
            return 1 if any(stem for stem in derived_compounds_forms if stem in clean_sentence) else 0

        return sorted(_sentences, key=lambda x: (dislike_secondary_form_with_vocab(x),
                                                 prefer_studying_read(x),
                                                 prefer_studying_listening(x),
                                                 prefer_highlighted_for_low_reliability_matches(x),
                                                 dislike_no_translation(x),
                                                 prefer_lower_priority_tag_values(x),
                                                 dislike_tts_sentences(x),
                                                 prefer_primary_form(x),
                                                 prefer_highlighted(x),
                                                 prefer_non_duplicates(x),
                                                 dislike_contains_derived_compound(x),
                                                 dislike_sentences_containing_secondary_form(x),
                                                 prefer_short_questions(x)))

    def sentence_classes(sentence: SentenceNote) -> str:
        classes = ""
        if sentence in highlighted_sentences: classes += "highlighted "
        classes += " ".join(sentence.get_meta_tags())
        return classes


    sentences = sort_sentences(_vocab_note.get_sentences())
    primary_form_matches = len([x for x in sentences if contains_primary_form(x)])
    sentences = sentences[:30]

    return f'''
             <div id="highlightedSentencesSection" class="page_section {"" if studying_sentences else "no_studying_sentences"}">
                <div class="page_section_title" title="primary form hits: {primary_form_matches}">sentences: primary form hits: {primary_form_matches}, <span class="studing_sentence_count">studying: {len(studying_sentences)}</span></div>
                <div id="highlightedSentencesList">
                    <div>
                        {newline.join([f"""
                        <div class="highlightedSentenceDiv {sentence_classes(_sentence)}">
                            <audio src="{_sentence.get_audio_path()}"></audio><a class="play-button"></a>
                            <div class="highlightedSentence">                            
                                <div class="sentenceQuestion"><span class="clipboard">{format_sentence(_sentence.get_question())}</span> <span class="deck_indicator">{_sentence.get_source_tag()}</div>
                                <div class="sentenceAnswer"> {_sentence.get_answer()}</span></div>
                            </div>
                        </div>
                        """ for _sentence in sentences])}
                    </div>
                </div>
            </div>
            ''' if sentences else ""


def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(VocabNote, {"##HIGHLIGHTED_SENTENCES##": generate_highlighted_sentences_html_list}).render)
