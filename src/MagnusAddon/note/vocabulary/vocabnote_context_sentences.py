from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote


def can_generate_sentences_from_context_sentences(self:VocabNote, require_audio: bool) -> bool:
    from ankiutils import app

    def can_create_sentence(question: str, audio: str) -> bool:
        return question != "" and (audio or not require_audio) and not app.col().sentences.with_question(question)

    return ((can_create_sentence(question=self.get_context_jp(), audio=self.get_context_jp_audio()) or
             can_create_sentence(question=self.get_context_jp_2(), audio=self.get_context_jp_2_audio())) or
            can_create_sentence(question=self.get_context_jp_3(), audio=self.get_context_jp_3_audio()))

def generate_sentences_from_context_sentences(self:VocabNote, require_audio: bool) -> None:
    from ankiutils import app
    from note.sentencenote import SentenceNote

    def create_sentence_if_not_present(question: str, answer: str, audio: str) -> None:
        if question and (audio or not require_audio) and not app.col().sentences.with_question(question):
            SentenceNote.add_sentence(question=question, answer=answer, audio=audio, highlighted_vocab={self.get_question()})

    create_sentence_if_not_present(question=self.get_context_jp(), answer=self.get_context_en(), audio=self.get_context_jp_audio())
    create_sentence_if_not_present(question=self.get_context_jp_2(), answer=self.get_context_en_2(), audio=self.get_context_jp_2_audio())
    create_sentence_if_not_present(question=self.get_context_jp_3(), answer=self.get_context_en_3(), audio=self.get_context_jp_3_audio())