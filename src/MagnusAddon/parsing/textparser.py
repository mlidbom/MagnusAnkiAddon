from janome.tokenizer import Tokenizer, Token
from jamdict import Jamdict
from parsing.janomeutils import ParsedWord

_jamdict = Jamdict(memory_mode=True)
_tokenizer: Tokenizer = Tokenizer()


def is_valid_word(word: str) -> bool:
    result = _jamdict.lookup(word)
    return len(result.entries) > 0

def identify_words(sentence: str) -> list[ParsedWord]:
    tokens: list[Token] = [token for token in _tokenizer.tokenize(sentence)]
    potential_words = list[ParsedWord]()

    for token_index in range(len(tokens)):
        word_combination:str = tokens[token_index].node.surface
        if is_valid_word(word_combination) and word_combination not in potential_words:
            potential_words.append(ParsedWord(word_combination, ""))
        for lookahead_index in range(token_index + 1, len(tokens)):
            word_combination += tokens[lookahead_index].node.surface
            if is_valid_word(word_combination) and word_combination not in potential_words:
                potential_words.append(ParsedWord(word_combination, ""))
            else:
                break

    return potential_words

def identify_words2(sentence: str) -> list[ParsedWord]:
    tokens: list[Token] = [token for token in _tokenizer.tokenize(sentence) if not token.part_of_speech.startswith("記号")]
    potential_words = list[str]()

    for token_index in range(len(tokens)):
        token = tokens[token_index]

        if not is_valid_word(token.base_form): raise Exception("WTF?")
        if token.base_form not in potential_words: potential_words.append(token.base_form)

        if not is_valid_word(token.surface): continue
        if token.surface not in potential_words: potential_words.append(token.surface)

        word_combination: str = token.surface
        for lookahead_index in range(token_index + 1, len(tokens)):
            surface_combination = word_combination + tokens[lookahead_index].surface
            if is_valid_word(surface_combination):
                if surface_combination not in potential_words:
                    potential_words.append(surface_combination)
                    word_combination = surface_combination
            else:
                base_form_combination = word_combination + tokens[lookahead_index].base_form
                if is_valid_word(base_form_combination):
                    if base_form_combination not in potential_words:
                        potential_words.append(base_form_combination)
                break

    return [ParsedWord(word, "") for word in potential_words]

def identify_first_word(sentence: str) -> str:

    tokens: list[Token] = [token for token in _tokenizer.tokenize(sentence) if not token.part_of_speech.startswith("記号")]
    word_combination = ""
    for token_index in range(len(tokens)):
        word_combination: str = tokens[token_index].base_form

        for lookahead_index in range(token_index + 1, len(tokens)):
            next_combination = word_combination + tokens[token_index + 1].base_form
            if not is_valid_word(next_combination):
                return word_combination
            word_combination = next_combination

        return word_combination


    return word_combination



