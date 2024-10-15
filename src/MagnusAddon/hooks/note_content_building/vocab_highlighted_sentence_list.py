from anki.cards import Card
from aqt import gui_hooks
from ankiutils import ui_utils
from note.jpnote import JPNote
from note.note_constants import Mine
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import ex_sequence, ex_str, kana_utils
from sysutils.ex_str import newline

def generate_highlighted_sentences_html_list(_vocab_note: VocabNote) -> str:
    forms = [_vocab_note.get_question()] + list(_vocab_note.get_forms())
    forms = ex_sequence.remove_duplicates_while_retaining_order(forms)
    primary_form = _vocab_note.get_question_without_noise_characters()
    secondary_forms = [form for form in forms if form != primary_form]
    secondary_forms_conjugation_base_form = [kana_utils.get_conjugation_base(form) for form in secondary_forms]
    conjugation_base_form = kana_utils.get_conjugation_base(primary_form)

    def contains_primary_form(_sentence: SentenceNote) -> bool:
        clean_sentence = ex_str.strip_html_and_bracket_markup(_sentence.get_question())
        return conjugation_base_form in clean_sentence

    def format_sentence(html_sentence: str) -> str:
        clean_sentence = ex_str.strip_html_and_bracket_markup(html_sentence)

        def create_form_class(_form:str) -> str:
            return "primaryForm" if _form == primary_form else "secondaryForm"


        for form in forms:
            if form in clean_sentence:
                return clean_sentence.replace(form, f"""<span class="vocabInContext {create_form_class(form)}">{form}</span>""")
            else:
                _conjugation_base_form = kana_utils.get_conjugation_base(form)
                if _conjugation_base_form in clean_sentence:
                    return clean_sentence.replace(_conjugation_base_form, f"""<span class="vocabInContext {create_form_class(form)}">{_conjugation_base_form}</span>""")

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
            return 1 if any((_base_form in clean_sentence for _base_form in secondary_forms_conjugation_base_form)) else 0

        return sorted(_sentences, key=lambda x: (prefer_highlighted_for_low_reliability_matches(x),
                                                 prefer_studying_read(x),
                                                 prefer_studying_listening(x),
                                                 dislike_no_translation(x),
                                                 prefer_lower_priority_tag_values(x),
                                                 dislike_tts_sentences(x),
                                                 prefer_primary_form(x),
                                                 prefer_highlighted(x),
                                                 prefer_non_duplicates(x),
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

def render_highlighted_sentence_list(html: str, card: Card, _type_of_display: str) -> str:
    vocab_note = JPNote.note_from_card(card)

    if isinstance(vocab_note, VocabNote) and ui_utils.is_displaytype_displaying_answer(_type_of_display):
        highlighted_sentences_html = generate_highlighted_sentences_html_list(vocab_note)
        html = html.replace("##HIGHLIGHTED_SENTENCES##", highlighted_sentences_html)

    return html

def init() -> None:
    gui_hooks.card_will_show.append(render_highlighted_sentence_list)
