from __future__ import annotations

from aqt import gui_hooks
from note.note_constants import Tags
from note.vocabulary.vocabnote import VocabNote
from sysutils.ex_str import newline
from ui.web.vocab.vocab_sentences_vocab_sentence_view_model import VocabSentenceViewModel
from ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


def generate_sentences_list_html(_vocab_note: VocabNote) -> str:
    studying_sentences = set(_vocab_note.sentences.studying())

    def sort_sentences(_sentences: list[VocabSentenceViewModel]) -> list[VocabSentenceViewModel]:

        def prefer_highlighted(_sentence: VocabSentenceViewModel) -> int: return 0 if _sentence.is_highlighted() else 1
        def prefer_studying_read(_sentence: VocabSentenceViewModel) -> int: return 0 if _sentence.sentence.is_studying_read() else 1
        def prefer_studying_listening(_sentence: VocabSentenceViewModel) -> int: return 0 if _sentence.sentence.is_studying_listening() else 1
        def prefer_primary_form(_sentence: VocabSentenceViewModel) -> int: return 0 if _sentence.contains_primary_form() else 1
        def dislike_tts_sentences(_sentence: VocabSentenceViewModel) -> int: return 1 if _sentence.sentence.has_tag(Tags.TTSAudio) else 0
        def prefer_short_questions(_sentence: VocabSentenceViewModel) -> int: return len(_sentence.sentence.get_question())
        def prefer_lower_priority_tag_values(_sentence: VocabSentenceViewModel) -> int: return _sentence.sentence.priority_tag_value()
        def dislike_no_translation(_sentence: VocabSentenceViewModel) -> int: return 1 if not _sentence.sentence.get_answer() else 0

        def prefer_displayed(_sentence: VocabSentenceViewModel) -> int: return 0 if _sentence.vocab_is_displayed else 1

        return sorted(_sentences,
                      key=lambda x: (prefer_highlighted(x),
                                     prefer_studying_read(x),
                                     prefer_studying_listening(x),
                                     prefer_displayed(x),
                                     dislike_no_translation(x),
                                     prefer_lower_priority_tag_values(x),
                                     dislike_tts_sentences(x),
                                     prefer_primary_form(x),
                                     prefer_short_questions(x)))

    sentences = sort_sentences([VocabSentenceViewModel(_vocab_note, sentence_note) for sentence_note in _vocab_note.sentences.all()])
    primary_form_matches = len([x for x in sentences if x.contains_primary_form()])
    sentences = sentences[:30]

    return f'''
             <div id="highlightedSentencesSection" class="page_section {"" if studying_sentences else "no_studying_sentences"}">
                <div class="page_section_title" title="primary form hits: {primary_form_matches}">sentences: primary form hits: {primary_form_matches}, <span class="studing_sentence_count">studying: {len(studying_sentences)}</span></div>
                <div id="highlightedSentencesList">
                    <div>
                        {newline.join([f"""
                        <div class="highlightedSentenceDiv {_sentence.sentence_classes()}">
                            <audio src="{_sentence.sentence.audio.first_audiofile_path()}"></audio><a class="play-button"></a>
                            <div class="highlightedSentence">
                                <div class="sentenceQuestion"><span class="clipboard">{_sentence.format_sentence()}</span> <span class="deck_indicator">{_sentence.sentence.get_source_tag()}</div>
                                <div class="sentenceAnswer"> {_sentence.sentence.get_answer()}</span></div>
                            </div>
                        </div>
                        """ for _sentence in sentences])}
                    </div>
                </div>
            </div>
            ''' if sentences else ""

def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(VocabNote, {"##HIGHLIGHTED_SENTENCES##": generate_sentences_list_html}).render)
