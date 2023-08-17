from janome.tokenizer import Tokenizer
from jamdict import Jamdict
from parsing.janomeutils import ParsedWord


def identify_words(sentence: str) -> list[ParsedWord]:
    jamdict = Jamdict()

    def is_valid_word(word: str) -> bool:
        result = jamdict.lookup(word, lookup_chars=False, lookup_ne=False)
        return len(result.entries) > 0


    tokens: list[str] = [token.surface for token in Tokenizer().tokenize(sentence)]
    potential_words = list[ParsedWord]()

    for token_index in range(len(tokens)):
        word_combination = tokens[token_index]
        if is_valid_word(word_combination) and word_combination not in potential_words:
            potential_words.append(ParsedWord(word_combination, ""))
        for lookahead_index in range(token_index + 1, len(tokens)):
            word_combination += tokens[lookahead_index]
            if is_valid_word(word_combination) and word_combination not in potential_words:
                potential_words.append(ParsedWord(word_combination, ""))
            else:
                break  # If the current combination is not a valid word, break out of the inner loop

    return potential_words
