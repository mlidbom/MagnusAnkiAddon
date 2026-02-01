from __future__ import annotations

from jastudio.sysutils import ex_str

real_quote_characters: set[str] = {"「", "」", '"'}
pseudo_quote_characters: set[str] = {"と", "って"}
all_quote_characters: set[str] = real_quote_characters | pseudo_quote_characters

space_characters: set[str] = {" ", "\t", ex_str.invisible_space}

question_marks: set[str] = {"？", "?"}
periods: set[str] = {".", "。", "｡"}
commas: set[str] = {",", "、"}
tilde: set[str] = {"～", "~"}


exclamations: set[str] = {"!"} #todo: isn't there a full size exclamation mark?

all_punctuation_characters: set[str] = all_quote_characters | question_marks | periods | commas | exclamations | tilde | {":", ";", "/", "|"}


sentence_start_characters: set[str] = real_quote_characters | space_characters | question_marks | periods
sentence_end_characters: set[str] = all_quote_characters | space_characters | question_marks | periods
noise_characters = all_punctuation_characters | space_characters | pseudo_quote_characters | sentence_end_characters


passive_verb_endings: set[str] = {"あれる", "られる", "される"}
causative_verb_endings: set[str] = {"あせる", "させる", "あす", "さす"}