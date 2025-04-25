from wanikani_api import models
from anki.notes import Note

from note.waninote import WaniNote
from note.note_constants import Mine, NoteFields
from sysutils import ex_str

class KanaVocabNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_question_without_noise_characters(self) -> str: return self.get_question().replace(Mine.VocabPrefixSuffixMarker, "")
    def get_question(self) -> str: return self.get_field(NoteFields.Vocab.question).strip()
    def _set_question(self, value: str) -> None: self.set_field(NoteFields.Vocab.question, value)

    def get_answer(self) -> str:
        return self.get_user_answer() or self.get_field(NoteFields.Vocab.source_answer)

    def _set_source_answer(self, value: str) -> None: self.set_field(NoteFields.Vocab.source_answer, value)

    def update_generated_data(self) -> None:
        super().update_generated_data()
        self.set_field(NoteFields.Vocab.active_answer, self.get_answer())

    def get_user_answer(self) -> str: return self.get_field(NoteFields.Vocab.user_answer)
    def set_user_answer(self, value: str) -> None: self.set_field(NoteFields.Vocab.user_answer, value)

    def get_related_similar_meaning(self) -> set[str]: return set(ex_str.extract_comma_separated_values(self.get_field(NoteFields.Vocab.Related_similar_meaning)))
    def add_related_similar_meaning(self, new_similar: str, _is_recursive_call:bool = False) -> None:
        similar_vocab_questions = self.get_related_similar_meaning()
        similar_vocab_questions.add(new_similar)

        self.set_field(NoteFields.Vocab.Related_similar_meaning, ", ".join(similar_vocab_questions))

        if not _is_recursive_call:
            from ankiutils import app
            for similar in app.col().vocab.with_question(new_similar):
                similar.add_related_similar_meaning(self.get_question(), _is_recursive_call=True)


    def get_related_derived_from(self) -> str: return self.get_field(NoteFields.Vocab.Related_derived_from)
    def set_related_derived_from(self, value: str) -> None: self.set_field(NoteFields.Vocab.Related_derived_from, value)


    def get_related_ergative_twin(self) -> str: return self.get_field(NoteFields.Vocab.Related_ergative_twin)
    def set_related_ergative_twin(self, value: str) -> None:
        self.set_field(NoteFields.Vocab.Related_ergative_twin, value)

        from ankiutils import app
        for twin in app.col().vocab.with_question(value):
            twin.set_field(NoteFields.Vocab.Related_ergative_twin, self.get_question())

    def get_related_confused_with(self) -> set[str]: return set(ex_str.extract_comma_separated_values(self.get_field(NoteFields.Vocab.Related_confused_with)))
    def add_related_confused_with(self, new_confused_with: str) -> None:
        confused_with = self.get_related_confused_with()
        confused_with.add(new_confused_with)
        self.set_field(NoteFields.Vocab.Related_confused_with, ", ".join(confused_with))

    def get_speech_type(self) -> str: return self.get_field(NoteFields.Vocab.Speech_Type)
    def set_speech_type(self, value: str) -> None: self.set_field(NoteFields.Vocab.Speech_Type, value)
    def get_speech_types(self) -> set[str]: return set(ex_str.extract_comma_separated_values(self.get_field(NoteFields.Vocab.Speech_Type)))

    _transitive_string_values = ["transitive", "transitive verb"]
    _intransitive_string_values = ["intransitive", "intransitive verb"]
    def is_transitive(self) -> bool: return any(val for val in self._transitive_string_values if val in self.get_speech_types())
    def is_intransitive(self) -> bool: return any(val for val in self._intransitive_string_values if val in self.get_speech_types())

    def get_context_jp(self) -> str: return ex_str.strip_html_markup(self.get_field(NoteFields.Vocab.Context_jp))
    def set_context_jp(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_jp, value)

    def get_context_jp_audio(self) -> str: return self.get_field(NoteFields.Vocab.Context_jp_audio)

    def get_context_en(self) -> str: return self.get_field(NoteFields.Vocab.Context_en)
    def set_context_en(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_en, value)

    def get_context_jp_2(self) -> str: return ex_str.strip_html_markup(self.get_field(NoteFields.Vocab.Context_jp_2))
    def set_context_jp_2(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_jp_2, value)

    def get_context_jp_2_audio(self) -> str: return self.get_field(NoteFields.Vocab.Context_jp_2_audio)

    def get_context_en_2(self) -> str: return self.get_field(NoteFields.Vocab.Context_en_2)
    def set_context_en_2(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_en_2, value)

    def get_context_jp_3(self) -> str: return ex_str.strip_html_markup(self.get_field(NoteFields.Vocab.Context_jp_3))
    def set_context_jp_3(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_jp_3, value)

    def get_context_jp_3_audio(self) -> str: return self.get_field(NoteFields.Vocab.Context_jp_3_audio)

    def get_context_en_3(self) -> str: return self.get_field(NoteFields.Vocab.Context_en_3)
    def set_context_en_3(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_en_3, value)

    def set_meaning_mnemonic(self, value: str) -> None: self.set_field(NoteFields.Vocab.source_mnemonic, value)

    def get_audio_male(self) -> str: return self.get_field(NoteFields.Vocab.Audio_b)
    def set_audio_male(self, value: list[str]) -> None: self.set_field(NoteFields.Vocab.Audio_b, ''.join([f'[sound:{item}]' for item in value]))

    def get_audio_female(self) -> str: return self.get_field(NoteFields.Vocab.Audio_g)
    def set_audio_female(self, value: list[str]) -> None: self.set_field(NoteFields.Vocab.Audio_g, ''.join([f'[sound:{item}]' for item in value]))

    def update_from_wani(self, wani_vocab: models.Vocabulary) -> None:
        super().update_from_wani(wani_vocab)

        self.set_meaning_mnemonic(wani_vocab.meaning_mnemonic)

        meanings = ', '.join(str(meaning.meaning) for meaning in wani_vocab.meanings)
        self._set_source_answer(meanings)

        self.set_speech_type(", ".join(wani_vocab.parts_of_speech))
