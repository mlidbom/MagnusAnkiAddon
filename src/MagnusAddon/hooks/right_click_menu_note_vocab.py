import pyperclip # type: ignore
from PyQt6.QtWidgets import QMenu

from ankiutils import app, query_builder
from hooks.right_click_menu_utils import add_lookup_action, add_single_vocab_lookup_action, add_ui_action, add_vocab_dependencies_lookup, create_vocab_note_action
from note.note_constants import NoteFields, NoteTypes
from note.sentencenote import SentenceNote
from note.vocabnote import VocabNote
from sysutils import ex_str
from sysutils.ex_str import newline
from sysutils.typed import non_optional
from hooks import shortcutfinger

def setup_note_menu(vocab: VocabNote, note_menu: QMenu, string_menus: list[tuple[QMenu, str]], selection:str, clipboard:str) -> None:
    def build_create_note_menu(note_create_menu: QMenu) -> None:
        def build_forms_menu(clone_to_form_menu: QMenu) -> None:
            forms_with_no_vocab = [form for form in vocab.get_forms() if not any(app.col().vocab.with_question(form))]
            for index, form in enumerate(forms_with_no_vocab):
                create_vocab_note_action(clone_to_form_menu, shortcutfinger.numpad(index, form), lambda _form=form: vocab.cloner.clone_to_form(_form))  # type: ignore

        def build_noun_menu(noun_menu: QMenu) -> None:
            create_vocab_note_action(noun_menu, shortcutfinger.home1("する-verb"), lambda: vocab.cloner.create_suru_verb())
            create_vocab_note_action(noun_menu, shortcutfinger.home2("します-verb"), lambda: vocab.cloner.create_shimasu_verb())
            create_vocab_note_action(noun_menu, shortcutfinger.home3("な-adjective"), lambda: vocab.cloner.create_na_adjective())
            create_vocab_note_action(noun_menu, shortcutfinger.home4("の-adjective"), lambda: vocab.cloner.create_no_adjective())
            create_vocab_note_action(noun_menu, shortcutfinger.up1("に-adverb"), lambda: vocab.cloner.create_ni_adverb())
            create_vocab_note_action(noun_menu, shortcutfinger.up2("と-adverb"), lambda: vocab.cloner.create_to_adverb())

        def build_verb_menu(verb_menu: QMenu) -> None:
            create_vocab_note_action(verb_menu, shortcutfinger.home1("ます-form"), lambda: vocab.cloner.create_masu_form())
            create_vocab_note_action(verb_menu, shortcutfinger.home2("て-form"), lambda: vocab.cloner.create_te_form())
            create_vocab_note_action(verb_menu, shortcutfinger.home3("た-form"), lambda: vocab.cloner.create_ta_form())
            create_vocab_note_action(verb_menu, shortcutfinger.home4("ない-form"), lambda: vocab.cloner.create_nai_form())

        def build_misc_menu(misc_menu:QMenu) -> None:
            create_vocab_note_action(misc_menu, shortcutfinger.home1("く-form-of-い-adjective"), lambda: vocab.cloner.create_ku_form())
            create_vocab_note_action(misc_menu, shortcutfinger.home2("て-prefixed"), lambda: vocab.cloner.create_te_prefixed_word())
            create_vocab_note_action(misc_menu, shortcutfinger.home3("お-prefixed"), lambda: vocab.cloner.create_o_prefixed_word())
            create_vocab_note_action(misc_menu, shortcutfinger.home4("ん-suffixed"), lambda: vocab.cloner.create_n_suffixed_word())
            create_vocab_note_action(misc_menu, shortcutfinger.home5("か-suffixed"), lambda: vocab.cloner.create_ka_suffixed_word())


        def build_create_prefix_postfix_note_menu(prefix_postfix_note_menu: QMenu, addendum:str) -> None:
            def create_suffix_note_menu(suffix_note_menu: QMenu) -> None:
                create_vocab_note_action(suffix_note_menu, shortcutfinger.home1(f"dictionary-form"), lambda: vocab.cloner.create_suffix_version(addendum))
                create_vocab_note_action(suffix_note_menu, shortcutfinger.home2(f"い-stem"), lambda: vocab.cloner.suffix_to_i_stem(addendum))
                create_vocab_note_action(suffix_note_menu, shortcutfinger.home3(f"て-stem"), lambda: vocab.cloner.suffix_to_te_stem(addendum))
                create_vocab_note_action(suffix_note_menu, shortcutfinger.home4(f"え-stem"), lambda: vocab.cloner.suffix_to_e_stem(addendum))
                create_vocab_note_action(suffix_note_menu, shortcutfinger.up1(f"あ-stem"), lambda: vocab.cloner.suffix_to_e_stem(addendum))

            create_vocab_note_action(prefix_postfix_note_menu, shortcutfinger.home1(f"prefix-{addendum}{vocab.get_question()}"), lambda: vocab.cloner.create_prefix_version(addendum))

            create_suffix_note_menu(non_optional(prefix_postfix_note_menu.addMenu(shortcutfinger.home2("Suffix-onto"))))


        build_forms_menu(non_optional(note_create_menu.addMenu(shortcutfinger.home1("Clone to form"))))
        build_noun_menu(non_optional(note_create_menu.addMenu(shortcutfinger.home2("Noun variations"))))
        build_verb_menu(non_optional(note_create_menu.addMenu(shortcutfinger.home3("Verb variations"))))
        build_misc_menu(non_optional(note_create_menu.addMenu(shortcutfinger.home4("Misc"))))
        if selection:
            build_create_prefix_postfix_note_menu(non_optional(note_create_menu.addMenu(shortcutfinger.up1("Selection"))), selection)

        if clipboard:
            build_create_prefix_postfix_note_menu(non_optional(note_create_menu.addMenu(shortcutfinger.up2("Clipboard"))), clipboard)


    def build_lookup_menu(note_lookup_menu: QMenu) -> None:
        add_lookup_action(note_lookup_menu, shortcutfinger.home1("Kanji"), f"note:{NoteTypes.Kanji} ( {' OR '.join([f'{NoteFields.Kanji.question}:{char}' for char in vocab.get_question()])} )")
        if vocab.get_related_ergative_twin():
            add_single_vocab_lookup_action(note_lookup_menu, shortcutfinger.home2("Ergative twin"), vocab.get_related_ergative_twin())

        add_lookup_action(note_lookup_menu, shortcutfinger.home3("Sentences I'm Studying"), query_builder.notes_lookup(vocab.get_sentences_studying()))
        add_lookup_action(note_lookup_menu, shortcutfinger.home4("Sentences"), query_builder.notes_lookup(vocab.get_sentences()))
        add_lookup_action(note_lookup_menu, shortcutfinger.up1("Sentences with primary form"), query_builder.notes_lookup(vocab.get_sentences_with_primary_form()))
        add_lookup_action(note_lookup_menu, shortcutfinger.up2("Sentences with this word highlighted"), query_builder.notes_lookup(vocab.get_user_highlighted_sentences()))

        add_lookup_action(note_lookup_menu, shortcutfinger.up3("Compounds"), query_builder.notes_lookup(vocab.in_compounds()))
        add_vocab_dependencies_lookup(note_lookup_menu, shortcutfinger.up3("Dependencies"), vocab)

        for reading in vocab.get_readings():
            add_lookup_action(note_lookup_menu, shortcutfinger.up4(f"Homonyms: {reading}"), query_builder.notes_lookup(app.col().vocab.with_reading(reading)))

    def build_note_menu() -> None:
        if not vocab.get_user_answer():
            add_ui_action(note_menu, shortcutfinger.up1("Accept meaning"), lambda: vocab.set_user_answer(format_vocab_meaning(vocab.get_answer())))

        add_ui_action(note_menu, shortcutfinger.up2("Generate answer"), lambda: vocab.generate_and_set_answer())
        if vocab.can_generate_sentences_from_context_sentences(require_audio=False):
            add_ui_action(note_menu, shortcutfinger.up3("Generate sentences"), lambda: vocab.generate_sentences_from_context_sentences(require_audio=False))

        from batches import local_note_updater
        add_ui_action(note_menu, shortcutfinger.up4("Reparse matching sentences"), lambda: local_note_updater.reparse_sentences_for_vocab(vocab))
        add_ui_action(note_menu, shortcutfinger.up5("Repopulate TOS"), lambda: vocab.auto_set_speech_type())

    def build_string_menus() -> None:
        for string_menu, menu_string in string_menus:
            def build_sentences_menu(sentence_menu: QMenu) -> None:
                def remove_highlight(_sentences: list[SentenceNote]) -> None:
                    for _sentence in _sentences:
                        _sentence.remove_extra_vocab(vocab.get_question())

                def exclude(_sentences: list[SentenceNote]) -> None:
                    for _sentence in _sentences:
                        _sentence.exclude_vocab(vocab.get_question())

                sentence = sentences[0]

                if vocab.get_question() not in sentence.get_user_highlighted_vocab():
                    add_ui_action(sentence_menu, shortcutfinger.home1("Add Highlight"), lambda _sentence=sentence: _sentence.position_extra_vocab(vocab.get_question()))  # type: ignore
                else:
                    # noinspection PyDefaultArgument
                    add_ui_action(sentence_menu, shortcutfinger.home2("Remove highlight"), lambda _sentences=sentences: remove_highlight(_sentences))  # type: ignore

                # noinspection PyDefaultArgument
                add_ui_action(sentence_menu, shortcutfinger.home3("Exclude this vocab"), lambda _sentences=sentences: exclude(_sentences))  # type: ignore

            def build_add_menu(vocab_add_menu: QMenu) -> None:
                add_ui_action(vocab_add_menu, shortcutfinger.home1("Similar meaning"), lambda _menu_string=menu_string: vocab.add_related_similar_meaning(_menu_string))  # type: ignore
                add_ui_action(vocab_add_menu, shortcutfinger.home2("Confused with"), lambda _menu_string=menu_string: vocab.add_related_confused_with(_menu_string))  # type: ignore

            def build_set_menu(note_set_menu: QMenu) -> None:
                add_ui_action(note_set_menu, shortcutfinger.home1("Derived from"), lambda _menu_string=menu_string: vocab.set_related_derived_from(_menu_string))  # type: ignore
                add_ui_action(note_set_menu, shortcutfinger.home2("Ergative twin"), lambda _menu_string=menu_string: vocab.set_related_ergative_twin(_menu_string))  # type: ignore

            sentences = app.col().sentences.with_question(menu_string)
            if sentences:
                build_sentences_menu(non_optional(string_menu.addMenu(shortcutfinger.home1("Sentence"))))

            build_add_menu(non_optional(string_menu.addMenu(shortcutfinger.home2("Add"))))
            build_set_menu(non_optional(string_menu.addMenu(shortcutfinger.home3("Set"))))

    def build_copy_menu(note_copy_menu: QMenu) -> None:
        note_copy_menu.addAction(shortcutfinger.home1("Question"), lambda: pyperclip.copy(vocab.get_question()))
        note_copy_menu.addAction(shortcutfinger.home2("Answer"), lambda: pyperclip.copy(vocab.get_answer()))
        note_copy_menu.addAction(shortcutfinger.home3("Definition (question:answer)"), lambda: pyperclip.copy(f"""{vocab.get_question()}: {vocab.get_answer()}"""))
        note_copy_menu.addAction(shortcutfinger.home4("Sentences: max 30"), lambda: pyperclip.copy(newline.join([sent.get_question() for sent in vocab.get_sentences()[0:30]])))




    build_lookup_menu(non_optional(note_menu.addMenu(shortcutfinger.home1("Open"))))
    build_create_note_menu(non_optional(note_menu.addMenu(shortcutfinger.home2("Create"))))
    build_copy_menu(non_optional(note_menu.addMenu(shortcutfinger.home3("Copy"))))
    build_note_menu()
    build_string_menus()

def format_vocab_meaning(meaning: str) -> str:
    return ex_str.strip_html_and_bracket_markup(meaning
                                                .replace(" SOURCE", "")
                                                .replace(", ", "/")
                                                .replace(" ", "-")
                                                .lower())
