from __future__ import annotations

from aqt import gui_hooks
from jaslib.note.vocabulary.vocabnote import VocabNote
from jaslib.ui.web.vocab import related_vocabs_renderer

from jastudio.ui.web.web_utils.content_renderer import PrerenderingAnswerContentRenderer


def init() -> None:
    gui_hooks.card_will_show.append(PrerenderingAnswerContentRenderer(VocabNote, {
            "##FORMS_LIST##": related_vocabs_renderer.generate_forms_list,
            "##IN_COMPOUNDS##": related_vocabs_renderer.generate_in_compounds_list,
            "##STEM_IN_COMPOUNDS##": related_vocabs_renderer.generate_stem_in_compounds_list,
            "##DERIVED_VOCABULARY##": related_vocabs_renderer.generate_derived_list,
            "##ERGATIVE_TWIN##": related_vocabs_renderer.generate_ergative_twin_html,
            "##DERIVED_FROM##": related_vocabs_renderer.generate_derived_from,
            "##HOMOPHONES_LIST##": related_vocabs_renderer.generate_homophones_html_list,
            "##PERFECT_SYNONYMS_LIST##": related_vocabs_renderer.generate_perfect_synonyms_meaning_html_list,
            "##SYNONYMS_LIST##": related_vocabs_renderer.generate_synonyms_meaning_html_list,
            "##SEE_ALSO_LIST##": related_vocabs_renderer.generate_see_also_html_list,
            "##ANTONYMS_LIST##": related_vocabs_renderer.generate_antonyms_meaning_html_list,
            "##CONFUSED_WITH_LIST##": related_vocabs_renderer.generate_confused_with_html_list,
            "##VOCAB_META_TAGS_HTML##": related_vocabs_renderer.generate_meta_tags,
            "##VOCAB_CLASSES##": related_vocabs_renderer.create_classes,
            "##STEM_VOCABULARY##": related_vocabs_renderer.generate_stem_vocabs,
            "##IS_STEM_OF##": related_vocabs_renderer.generate_stem_of_vocabs
    }).render)
