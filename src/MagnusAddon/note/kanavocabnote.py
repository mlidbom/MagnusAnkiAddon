from wanikani_api import models
from anki.notes import Note

from note.waninote import WaniNote
from sysutils import ex_str
from note.note_constants import NoteFields


class KanaVocabNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_question_without_noise_characters(self) -> str: return self.get_question().replace("〜","")
    def get_question(self) -> str: return self.get_field(NoteFields.Vocab.question).strip()
    def _set_question(self, value: str) -> None: self.set_field(NoteFields.Vocab.question, value)

    def get_answer(self) -> str:
        return self.get_user_answer() or self.get_field(NoteFields.Vocab.source_answer)

    def _set_source_answer(self, value: str) -> None: self.set_field(NoteFields.Vocab.source_answer, value)

    def update_generated_data(self) -> None:
        self.set_field(NoteFields.Vocab.active_answer, self.get_answer())

    def get_user_answer(self) -> str: return self.get_field(NoteFields.Vocab.user_answer)
    def set_user_answer(self, value: str) -> None: self.set_field(NoteFields.Vocab.user_answer, value)

    def get_related_homophones(self) -> list[str]: return self.get_field(NoteFields.Vocab.Related_homophones).split(", ")
    def set_related_homophones(self, value: list[str]) -> None:
        html = f'''<ul class="homophone">
{ex_str.newline.join([f'   <li class="clipboard">{val}</li>' for val in value])}
</ul>'''
        self.set_field(NoteFields.Vocab.Related_homophones, html if value else "")

    def get_related_similar_meaning(self) -> str: return self.get_field(NoteFields.Vocab.Related_similar_meaning)
    def set_related_similar_meaning(self, value: str) -> None: self.set_field(NoteFields.Vocab.Related_similar_meaning, value)

    def get_related_derived_from(self) -> str: return self.get_field(NoteFields.Vocab.Related_derived_from)
    def set_related_derived_from(self, value: str) -> None: self.set_field(NoteFields.Vocab.Related_derived_from, value)

    def get_related_ergative_twin(self) -> str: return self.get_field(NoteFields.Vocab.Related_ergative_twin)
    def set_related_ergative_twin(self, value: str) -> None: self.set_field(NoteFields.Vocab.Related_ergative_twin, value)

    def get_related_confused_with(self) -> str: return self.get_field(NoteFields.Vocab.Related_confused_with)
    def set_related_confused_with(self, value: str) -> None: self.set_field(NoteFields.Vocab.Related_confused_with, value)

    def get_speech_type(self) -> str: return self.get_field(NoteFields.Vocab.Speech_Type)
    def set_speech_type(self, value: str) -> None: self.set_field(NoteFields.Vocab.Speech_Type, value)

    def get_context_jp(self) -> str: return self.get_field(NoteFields.Vocab.Context_jp)
    def set_context_jp(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_jp, value)

    def get_context_en(self) -> str: return self.get_field(NoteFields.Vocab.Context_en)
    def set_context_en(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_en, value)

    def get_context_jp_2(self) -> str: return self.get_field(NoteFields.Vocab.Context_jp_2)
    def set_context_jp_2(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_jp_2, value)

    def get_context_en_2(self) -> str: return self.get_field(NoteFields.Vocab.Context_en_2)
    def set_context_en_2(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_en_2, value)

    def get_context_jp_3(self) -> str: return self.get_field(NoteFields.Vocab.Context_jp_3)
    def set_context_jp_3(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_jp_3, value)

    def get_context_en_3(self) -> str: return self.get_field(NoteFields.Vocab.Context_en_3)
    def set_context_en_3(self, value: str) -> None: self.set_field(NoteFields.Vocab.Context_en_3, value)

    def get_meaning_mnemonic(self) -> str: return self.get_field(NoteFields.Vocab.Meaning_Exp)
    def set_meaning_mnemonic(self, value: str) -> None: self.set_field(NoteFields.Vocab.Meaning_Exp, value)

    def get_audio_male(self) -> str: return self.get_field(NoteFields.Vocab.Audio_b)
    def set_audio_male(self, value: list[str]) -> None: self.set_field(NoteFields.Vocab.Audio_b, ''.join([f'[sound:{item}]' for item in value]))

    def get_audio_female(self) -> str: return self.get_field(NoteFields.Vocab.Audio_g)
    def set_audio_female(self, value: list[str]) -> None: self.set_field(NoteFields.Vocab.Audio_g, ''.join([f'[sound:{item}]' for item in value]))

    def get_audios(self) -> str: return f"{self.get_audio_male()}{self.get_audio_female()}"

    def update_from_wani(self, wani_vocab: models.Vocabulary) -> None:
        super().update_from_wani(wani_vocab)

        self.set_meaning_mnemonic(wani_vocab.meaning_mnemonic)

        meanings = ', '.join(str(meaning.meaning) for meaning in wani_vocab.meanings)
        self._set_source_answer(meanings)

        self.set_speech_type(", ".join(wani_vocab.parts_of_speech))
