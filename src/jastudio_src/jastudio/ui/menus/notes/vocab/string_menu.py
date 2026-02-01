from __future__ import annotations

from typing import TYPE_CHECKING

from jastudio.ankiutils import app
from jastudio.sysutils.typed import non_optional
from jastudio.ui.menus.menu_utils import shortcutfinger
from jastudio.ui.menus.menu_utils.ex_qmenu import add_ui_action
from jastudio.ui.menus.notes.vocab.common import build_create_prefix_postfix_note_menu

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QMenu

    from jastudio.note.vocabulary.vocabnote import VocabNote

def build_string_menu(string_menu: QMenu, vocab: VocabNote, menu_string: str) -> None:
    def build_sentences_menu(sentence_menu: QMenu) -> None:
        def remove_highlight_from_sentences() -> None:
            for sent in sentences: sent.configuration.remove_highlighted_word(vocab.question.disambiguation_name)

        def mark_as_incorrect_match_in_sentences() -> None:
            for sent in sentences: sent.configuration.incorrect_matches.add_global(vocab.question.disambiguation_name)

        has_sentences = len(sentences) > 0

        add_ui_action(sentence_menu, shortcutfinger.home1("Add Highlight"),
                      lambda: sentences[0].configuration.add_highlighted_word(vocab.question.disambiguation_name),
                      has_sentences and vocab.question.disambiguation_name not in sentences[0].configuration.highlighted_words())
        add_ui_action(sentence_menu, shortcutfinger.home2("Remove highlight"),
                      lambda: remove_highlight_from_sentences(),
                      has_sentences and vocab.question.disambiguation_name in sentences[0].configuration.highlighted_words())
        add_ui_action(sentence_menu, shortcutfinger.home3("Remove-sentence: Mark as incorrect match in sentence"),
                      lambda: mark_as_incorrect_match_in_sentences(),
                      has_sentences)

    def build_add_menu(vocab_add_menu: QMenu) -> None:
        add_ui_action(vocab_add_menu, shortcutfinger.home1("Synonym"), lambda: vocab.related_notes.synonyms.add(menu_string), menu_string not in vocab.related_notes.synonyms.strings())
        add_ui_action(vocab_add_menu, shortcutfinger.home2("Synonyms transitively one level"), lambda: vocab.related_notes.synonyms.add_transitively_one_level(menu_string))
        add_ui_action(vocab_add_menu, shortcutfinger.home3("Confused with"), lambda: vocab.related_notes.confused_with.add(menu_string), menu_string not in vocab.related_notes.confused_with.get())
        add_ui_action(vocab_add_menu, shortcutfinger.home4("Antonym"), lambda: vocab.related_notes.antonyms.add(menu_string), menu_string not in vocab.related_notes.antonyms.strings())
        add_ui_action(vocab_add_menu, shortcutfinger.home5("Form"), lambda: vocab.forms.add(menu_string), menu_string not in vocab.forms.all_set())
        add_ui_action(vocab_add_menu, shortcutfinger.up1("See also"), lambda: vocab.related_notes.see_also.add(menu_string), menu_string not in vocab.related_notes.see_also.strings())
        add_ui_action(vocab_add_menu, shortcutfinger.down1("Perfect synonym, automatically syncronize answers"), lambda: vocab.related_notes.perfect_synonyms.add_overwriting_the_answer_of_the_added_synonym(menu_string), menu_string not in vocab.related_notes.perfect_synonyms.get())

    def build_remove_menu(vocab_remove_menu: QMenu) -> None:

        add_ui_action(vocab_remove_menu, shortcutfinger.home1("Synonym"), lambda: vocab.related_notes.synonyms.remove(menu_string), menu_string in vocab.related_notes.synonyms.strings())
        add_ui_action(vocab_remove_menu, shortcutfinger.home2("Confused with"), lambda: vocab.related_notes.confused_with.remove(menu_string), menu_string in vocab.related_notes.confused_with.get())
        add_ui_action(vocab_remove_menu, shortcutfinger.home3("Antonym"), lambda: vocab.related_notes.antonyms.remove(menu_string), menu_string in vocab.related_notes.antonyms.strings())
        add_ui_action(vocab_remove_menu, shortcutfinger.home4("Ergative twin"), lambda: vocab.related_notes.ergative_twin.remove(), menu_string == vocab.related_notes.ergative_twin.get())
        add_ui_action(vocab_remove_menu, shortcutfinger.home5("Form"), lambda: vocab.forms.remove(menu_string), menu_string in vocab.forms.all_set())
        add_ui_action(vocab_remove_menu, shortcutfinger.up1("See also"), lambda: vocab.related_notes.see_also.remove(menu_string), menu_string in vocab.related_notes.see_also.strings())
        add_ui_action(vocab_remove_menu, shortcutfinger.down1("Perfect synonym"), lambda: vocab.related_notes.perfect_synonyms.remove(menu_string), menu_string in vocab.related_notes.perfect_synonyms.get())
        add_ui_action(vocab_remove_menu, shortcutfinger.down2("Derived from"), lambda: vocab.related_notes.derived_from.set(""), menu_string == vocab.related_notes.derived_from.get())

    def build_set_menu(note_set_menu: QMenu) -> None:
        add_ui_action(note_set_menu, shortcutfinger.home1("Ergative twin"), lambda: vocab.related_notes.ergative_twin.set(menu_string))
        add_ui_action(note_set_menu, shortcutfinger.home2("Derived from"), lambda: vocab.related_notes.derived_from.set(menu_string))

    sentences = app.col().sentences.with_question(menu_string)

    build_add_menu(non_optional(string_menu.addMenu(shortcutfinger.home1("Add"))))
    build_set_menu(non_optional(string_menu.addMenu(shortcutfinger.home2("Set"))))
    build_remove_menu(non_optional(string_menu.addMenu(shortcutfinger.home3("Remove"))))
    build_sentences_menu(non_optional(string_menu.addMenu(shortcutfinger.home4("Sentence"))))
    build_create_prefix_postfix_note_menu(non_optional(string_menu.addMenu(shortcutfinger.up1(f"Create combined {menu_string}"))), vocab, menu_string)
