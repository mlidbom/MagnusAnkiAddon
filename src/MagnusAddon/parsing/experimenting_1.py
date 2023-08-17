from typing import List
from janome.tokenizer import Tokenizer
from jamdict import Jamdict


def identify_potential_words(sentence: str) -> List[str]:
    tokenizer: Tokenizer = Tokenizer()
    jmd: Jamdict = Jamdict()
    tokens: List = list(tokenizer.tokenize(sentence))
    potential_words: List[str] = []

    # Single words
    for token in tokens:
        word: str = token.base_form  # or token.surface for the surface form
        if jmd.lookup(word).entries:  # Check if the word exists in JMdict
            potential_words.append(word)

    # Compound words (simple heuristic: consecutive kanji tokens)
    for i in range(len(tokens) - 1):
        if tokens[i].surface[-1].isalnum():  # if the last character of the current token is alphanumeric
            compound_word: str = tokens[i].surface + tokens[i + 1].surface
            if jmd.lookup(compound_word).entries:
                potential_words.append(compound_word)

    return potential_words  # Assuming you want duplicates retained for order, else wrap with set for uniqueness.


# Test
sentence1 = "ハート形のクッキーが美味しいです。"
print(identify_potential_words(sentence1))
