from _lib.wanikani_api import models
from anki.notes import Note

from wanikani.Note.WaniNote import WaniNote
from wanikani.wani_constants import Wani


class WaniKanaVocabNote(WaniNote):
    def __init__(self, note: Note):
        super().__init__(note)

    def get_vocab(self): return super().get_field(Wani.KanaVocabFields.Vocab)
    def set_vocab(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Vocab, value)

    def get_vocab_meaning(self):
        meaning = self.get_override_meaning()
        if meaning != "": return meaning
        return super().get_field(Wani.KanaVocabFields.Vocab_Meaning)

    def set_vocab_meaning(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Vocab_Meaning, value)

    def get_override_meaning(self) -> str: return super().get_field(Wani.KanaVocabFields.Override_meaning)
    def set_override_meaning(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Override_meaning, value)

    def get_related_homophones(self) -> str: return super().get_field(Wani.KanaVocabFields.Related_homophones)
    def set_related_homophones(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Related_homophones, value)

    def get_related_similar_meaning(self) -> str: return super().get_field(Wani.KanaVocabFields.Related_similar_meaning)
    def set_related_similar_meaning(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Related_similar_meaning, value)

    def get_related_derived_from(self) -> str: return super().get_field(Wani.KanaVocabFields.Related_derived_from)
    def set_related_derived_from(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Related_derived_from, value)

    def get_related_ergative_twin(self) -> str: return super().get_field(Wani.KanaVocabFields.Related_ergative_twin)
    def set_related_ergative_twin(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Related_ergative_twin, value)

    def get_related_similar_vocab(self) -> str: return super().get_field(Wani.KanaVocabFields.Related_similarVocab)
    def set_related_similar_vocab(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Related_similarVocab, value)

    def get_speech_type(self) -> str: return super().get_field(Wani.KanaVocabFields.Speech_Type)
    def set_speech_type(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Speech_Type, value)

    def get_context_jp(self): return super().get_field(Wani.KanaVocabFields.Context_jp)
    def set_context_jp(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Context_jp, value)

    def get_context_en(self): return super().get_field(Wani.KanaVocabFields.Context_en)
    def set_context_en(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Context_en, value)

    def get_context_jp_2(self): return super().get_field(Wani.KanaVocabFields.Context_jp_2)
    def set_context_jp_2(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Context_jp_2, value)

    def get_context_en_2(self): return super().get_field(Wani.KanaVocabFields.Context_en_2)
    def set_context_en_2(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Context_en_2, value)

    def get_context_jp_3(self): return super().get_field(Wani.KanaVocabFields.Context_jp_3)
    def set_context_jp_3(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Context_jp_3, value)

    def get_context_en_3(self): return super().get_field(Wani.KanaVocabFields.Context_en_3)
    def set_context_en_3(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Context_en_3, value)

    def get_meaning_mnemonic(self): return super().get_field(Wani.KanaVocabFields.Meaning_Exp)
    def set_meaning_mnemonic(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Meaning_Exp, value)

    def get_audio_male(self): return super().get_field(Wani.KanaVocabFields.Audio_b)
    def set_audio_male(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Audio_b,
                                                                     "[sound:{}]".format(value))

    def get_audio_female(self): return super().get_field(Wani.KanaVocabFields.Audio_g)
    def set_audio_female(self, value: str) -> None: super().set_field(Wani.KanaVocabFields.Audio_g,
                                                                       "[sound:{}]".format(value))

    def get_audios(self): return f"{self.get_audio_male()}{self.get_audio_female()}"

    def update_from_wani(self, wani_vocab: models.Vocabulary):
        super().update_from_wani(wani_vocab)

        self.set_meaning_mnemonic(wani_vocab.meaning_mnemonic)

        meanings = ', '.join(str(meaning.meaning) for meaning in wani_vocab.meanings)
        self.set_vocab_meaning(meanings)

        self.set_speech_type(", ".join(wani_vocab.parts_of_speech))
