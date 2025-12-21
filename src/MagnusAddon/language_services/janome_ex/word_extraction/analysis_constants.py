from __future__ import annotations

from sysutils import ex_str
from typed_linq_collections.collections.q_set import QSet

real_quote_characters: QSet[str] = QSet(("「", "」", '"'))
pseudo_quote_characters: QSet[str] = QSet(("と", "って"))
all_quote_characters: QSet[str] = real_quote_characters | pseudo_quote_characters

space_characters: QSet[str] = QSet((" ", "\t", ex_str.invisible_space))

question_marks: QSet[str] = QSet(("？", "?"))
periods: QSet[str] = QSet((".", "。", "｡"))
commas: QSet[str] = QSet((",", "、"))
tilde: QSet[str] = QSet(("～", "~"))


exclamations: QSet[str] = QSet(["!"]) #todo: isn't there a full size exclamation mark?

all_punctuation_characters: QSet[str] = all_quote_characters | question_marks | periods | commas | exclamations | tilde | QSet((":", ";", "/", "|"))


sentence_start_characters: QSet[str] = real_quote_characters | space_characters
sentence_end_characters: QSet[str] = all_quote_characters | space_characters | question_marks | periods
noise_characters = all_punctuation_characters | space_characters | pseudo_quote_characters | sentence_end_characters


passive_verb_endings: QSet[str] = QSet(("あれる", "られる", "される"))
causative_verb_endings: QSet[str] = QSet(("あせる", "させる", "あす", "さす"))