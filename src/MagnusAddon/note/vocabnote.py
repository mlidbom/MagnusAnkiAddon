from __future__ import annotations

from ankiutils import anki_module_import_issues_fix_just_import_this_module_before_any_other_anki_modules # noqa
from wanikani_api import models
from anki.notes import Note

from language_services.jamdict_ex.priority_spec import PrioritySpec
from note.kanavocabnote import KanaVocabNote
from sysutils import kana_utils
from sysutils import ex_str
from note.note_constants import NoteFields, Mine, NoteTypes
from wanikani.wanikani_api_client import WanikaniClient

class VocabMetaTag:
    def __init__(self, name: str, display: str, tooltip: str):
        self.name = name
        self.display = display
        self.tooltip = tooltip


class VocabNote(KanaVocabNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def __repr__(self) -> str: return f"""{self.get_question()}"""

    def get_kanji(self) -> str: return self.get_field(NoteFields.Vocab.Kanji)
    def set_kanji(self, value: str) -> None: self.set_field(NoteFields.Vocab.Kanji, value)

    def get_forms(self) -> set[str]: return set(ex_str.extract_comma_separated_values(self._get_forms()))
    def set_forms(self, forms: set[str]) -> None: self._set_forms(", ".join([form.strip() for form in forms]))
    def _get_forms(self) -> str: return self.get_field(NoteFields.Vocab.Forms)
    def _set_forms(self, value: str) -> None: self.set_field(NoteFields.Vocab.Forms, value)
    def get_user_compounds(self) -> list[str]: return ex_str.extract_comma_separated_values(self.get_field(NoteFields.Vocab.user_compounds))

    def update_generated_data(self) -> None:
        from language_services.jamdict_ex.dict_lookup import DictLookup

        super().update_generated_data()

        question = self.get_question().strip()
        readings = ",".join(self.get_readings())

        if question == readings:
            self.set_tag(Mine.Tags.UsuallyKanaOnly)

        if not readings:
            if kana_utils.is_only_kana(question):
                self.set_readings([question])
                self.set_tag(Mine.Tags.UsuallyKanaOnly)

        lookup = DictLookup.try_lookup_vocab_word_or_name(self)
        if lookup.is_uk() and not self.has_tag(Mine.Tags.DisableKanaOnly):
            self.set_tag(Mine.Tags.UsuallyKanaOnly)

        if not self.get_forms():
            if lookup.found_words():
                self.set_forms(lookup.valid_forms(self.is_uk()))

            if self.get_question() not in self.get_forms():
                self.set_forms(self.get_forms() | {self.get_question()})

            if self.is_uk() and self.get_readings()[0] not in self.get_forms():
                self.set_forms(self.get_forms() | set(self.get_readings()))

    def extract_kanji(self) -> list[str]:
        clean = ex_str.strip_html_and_bracket_markup(self.get_question())
        return [char for char in clean if kana_utils.is_kanji(char)]

    def is_uk(self) -> bool: return self.has_tag(Mine.Tags.UsuallyKanaOnly)

    def get_display_question(self) -> str:
        return self.get_readings()[0] if self.is_uk() else self.get_question()

    def get_kanji_name(self) -> str: return self.get_field(NoteFields.Vocab.Kanji_Name)
    def set_kanji_name(self, value: str) -> None: self.set_field(NoteFields.Vocab.Kanji_Name, value)

    def get_reading_mnemonic(self) -> str: return self.get_field(NoteFields.Vocab.Reading_Exp)
    def set_reading_mnemonic(self, value: str) -> None: self.set_field(NoteFields.Vocab.Reading_Exp, value)

    def get_readings(self) -> list[str]: return [reading.strip() for reading in self._get_reading().split(",")]
    def set_readings(self, readings: list[str]) -> None: self._set_reading(", ".join([reading.strip() for reading in readings]))

    def _get_reading(self) -> str: return self.get_field(NoteFields.Vocab.Reading)
    def _set_reading(self, value: str) -> None: self.set_field(NoteFields.Vocab.Reading, value)

    def get_component_subject_ids(self) -> str: return self.get_field(NoteFields.Vocab.component_subject_ids)
    def set_component_subject_ids(self, value: str) -> None: self.set_field(NoteFields.Vocab.component_subject_ids, value)

    def priority_spec(self) -> PrioritySpec:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        lookup = DictLookup.try_lookup_vocab_word_or_name(self)
        return lookup.priority_spec() if lookup else PrioritySpec(set())


    def override_meaning_mnemonic(self) -> None:
        if not self.get_mnemonics_override():
            self.set_mnemonics_override("-")

    def restore_meaning_mnemonic(self) -> None:
        if self.get_mnemonics_override() == "-":
            self.set_mnemonics_override("")

    def get_mnemonics_override(self) -> str: return self.get_field(NoteFields.Vocab.Mnemonic__)
    def set_mnemonics_override(self, value: str) -> None: self.set_field(NoteFields.Vocab.Mnemonic__, value)

    def get_parsed_type_of_speech(self) -> str: return self.get_field(NoteFields.Vocab.ParsedTypeOfSpeech)
    def set_parsed_type_of_speech(self, value: str) -> None: self.set_field(NoteFields.Vocab.ParsedTypeOfSpeech, value)

    def get_dual_audios(self) -> str:
        if self.get_audio_male() and self.get_audio_female():
            return f"{self.get_audio_male()}{self.get_audio_female()}"
        elif self.get_audio_male():
            return f"{self.get_audio_male()}{self.get_audio_male()}"
        elif self.get_audio_female():
            return f"{self.get_audio_female()}{self.get_audio_female()}"
        else:
            return ""

    def get_meta_tags(self) -> str:
        tags = set(self.get_tags())
        meta: list[VocabMetaTag] = []
        tos = [t.lower().strip() for t in self.get_speech_type().split(",")]

        #writing
        if "_uk" in tags: meta.append(VocabMetaTag("uk", "uk", "usually kana only"))

        #verbs
        if "ichidan verb" in tos: meta.append(VocabMetaTag("ichidan", "1", "ichidan verb"))
        if "godan verb" in tos: meta.append(VocabMetaTag("godan", "5", "godan verb"))
        if "suru verb" in tos or "verbal noun" in tos: meta.append(VocabMetaTag("suru-verb", "s", "suru verb"))
        if "kuru verb" in tos: meta.append(VocabMetaTag("kuru-verb", "k-v", "kuru verb"))
        if "auxiliary verb" in tos: meta.append(VocabMetaTag("auxiliary-verb", "aux-v", "auxiliary verb"))

        if "intransitive verb" in tos: meta.append(VocabMetaTag("intransitive", "t", "intransitive verb"))
        if "transitive verb" in tos: meta.append(VocabMetaTag("transitive", "i", "transitive verb"))

        if "adverb" in tos: meta.append(VocabMetaTag("adverb", "a", "adverb"))

        #nouns
        if "proper noun" in tos: meta.append(VocabMetaTag("proper-noun", "pn", "proper noun"))
        if "pronoun" in tos: meta.append(VocabMetaTag("pronoun", "pr", "pronoun"))
        elif "noun" in tos: meta.append(VocabMetaTag("noun", "n", "noun"))
        if "adverbial noun" in tos: meta.append(VocabMetaTag("adverbial-noun", "adv-n", "adverbial noun"))
        if "independent noun" in tos: meta.append(VocabMetaTag("independent-noun", "i-n", "independent noun"))

        #adjectives
        if "い adjective" in tos or "i-adjective" in tos: meta.append(VocabMetaTag("i-adjective", "い", "い adjective"))
        if "の adjective" in tos: meta.append(VocabMetaTag("no-adjective", "の", "の adjective"))
        if "な adjective" in tos or "na adjective" in tos: meta.append(VocabMetaTag("na-adjective", "な", "な adjective"))
        if "auxiliary adjective" in tos: meta.append(VocabMetaTag("auxiliary-adjective", "aa", "auxiliary adjective"))


        #???
        if "in compounds" in tos: meta.append(VocabMetaTag("in-compounds", "i-c", "in compounds"))
        if "n-adv" in tos: meta.append(VocabMetaTag("n-adv", "n-adv", "n-adv"))


        #misc
        if "counter" in tos: meta.append(VocabMetaTag("counter", "ctr", "counter"))
        if "numeral" in tos: meta.append(VocabMetaTag("numeral", "num", "numeral"))
        if "auxiliary" in tos: meta.append(VocabMetaTag("auxiliary", "aux", "auxiliary"))
        if "interjection" in tos: meta.append(VocabMetaTag("interjection", "int", "interjection"))
        if "conjunction" in tos: meta.append(VocabMetaTag("conjunction", "conj", "conjunction"))
        if "particle" in tos: meta.append(VocabMetaTag("particle", "part", "particle"))
        if "prefix" in tos: meta.append(VocabMetaTag("prefix", "p", "prefix"))
        if "suff" in tos: meta.append(VocabMetaTag("suffix", "s", "suffix"))
        if "expression" in tos: meta.append(VocabMetaTag("expression", "x", "expression"))

        return """<ol class="vocab_tag_list">""" +  "".join([f"""<li class="vocab_tag {tag.name}" title="{tag.tooltip}">{tag.display}</li>""" for tag in meta]) + "</ol>"

    def update_from_wani(self, wani_vocab: models.Vocabulary) -> None:
        super().update_from_wani(wani_vocab)

        self.set_reading_mnemonic(wani_vocab.reading_mnemonic)

        readings = [reading.reading for reading in wani_vocab.readings]
        self._set_reading(", ".join(readings))

        component_subject_ids = [str(subject_id) for subject_id in wani_vocab.component_subject_ids]
        self.set_component_subject_ids(", ".join(component_subject_ids))

        client = WanikaniClient.get_instance()
        kanji_subjects = [client.get_kanji_by_id(kanji_id) for kanji_id in wani_vocab.component_subject_ids]
        kanji_characters = [subject.characters for subject in kanji_subjects]
        self.set_kanji(", ".join(kanji_characters))

        kanji_names = [subject.meanings[0].meaning for subject in kanji_subjects]
        self.set_kanji_name(", ".join(kanji_names))

    @staticmethod
    def create_from_wani_vocabulary(wani_vocab: models.Vocabulary) -> None:
        from ankiutils import app
        note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Vocab))
        note.add_tag("__imported")
        note.add_tag(Mine.Tags.Wani)
        kanji_note = VocabNote(note)
        app.anki_collection().addNote(note)
        kanji_note._set_question(wani_vocab.characters)
        kanji_note.update_from_wani(wani_vocab)

        # Do not move to update method or we will wipe out local changes made to the context sentences.
        if len(wani_vocab.context_sentences) > 0:
            kanji_note.set_context_en(wani_vocab.context_sentences[0].english)
            kanji_note.set_context_jp(wani_vocab.context_sentences[0].japanese)

        if len(wani_vocab.context_sentences) > 1:
            kanji_note.set_context_en_2(wani_vocab.context_sentences[1].english)
            kanji_note.set_context_jp_2(wani_vocab.context_sentences[1].japanese)

        if len(wani_vocab.context_sentences) > 2:
            kanji_note.set_context_en_3(wani_vocab.context_sentences[2].english)
            kanji_note.set_context_jp_3(wani_vocab.context_sentences[2].japanese)

    def generate_and_set_answer(self) -> None:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        dict_lookup = DictLookup.try_lookup_vocab_word_or_name(self)
        if dict_lookup.found_words():
            generated = dict_lookup.entries[0].generate_answer()
            self.set_user_answer(generated)

    @classmethod
    def create(cls, question:str, answer:str, readings:list[str]) -> VocabNote:
        from ankiutils import app
        backend_note = Note(app.anki_collection(), app.anki_collection().models.by_name(NoteTypes.Vocab))
        note = VocabNote(backend_note)
        note._set_question(question)
        note.set_user_answer(answer)
        note.set_readings(readings)
        note.update_generated_data()
        app.anki_collection().addNote(backend_note)
        return note
