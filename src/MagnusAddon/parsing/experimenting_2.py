from janome.tokenizer import Tokenizer
from jamdict import Jamdict
from typing import List

def identify_potential_words(sentence: str) -> List[str]:
    tokenizer = Tokenizer()
    jmd = Jamdict()

    tokens = list(tokenizer.tokenize(sentence))
    potential_words: List[str] = []
    skip_next = False

    for i in range(len(tokens)):
        # If we are supposed to skip this token because it was part of a compound word
        if skip_next:
            skip_next = False
            continue

        word = tokens[i].base_form

        # Try to form a compound word
        if i < len(tokens) - 1:
            compound_word = word + tokens[i + 1].base_form
            if jmd.lookup(compound_word):
                potential_words.append(compound_word)
                potential_words.append(word)
                potential_words.append(tokens[i + 1].base_form)
                skip_next = True
                continue

        if not skip_next and jmd.lookup(word):
            potential_words.append(word)

    return list(dict.fromkeys(potential_words))  # Remove duplicates and maintain order

sentence1 = "ハート形のクッキーが美味しいです。"
print(identify_potential_words(sentence1))
