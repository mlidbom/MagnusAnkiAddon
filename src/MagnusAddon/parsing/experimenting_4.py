# from janome.tokenizer import Tokenizer
# from jamdict import Jamdict
#
#
# def is_valid_word(word: str, jmd: Jamdict) -> bool:
#     result = jmd.lookup(word)
#     return len(result.entries) > 0
#
# def identify_words(sentence: str) -> list[str]:
#     jamdict = Jamdict()
#     tokens = [token.surface for token in Tokenizer().tokenize(sentence)]
#     potential_words = []
#
#     for token_index in range(len(tokens)):
#         word_combination = tokens[token_index]
#         if is_valid_word(word_combination, jamdict) and word_combination not in potential_words:
#             potential_words.append(word_combination)
#         for lookahead_index in range(token_index + 1, len(tokens)):
#             word_combination += tokens[lookahead_index]
#             if is_valid_word(word_combination, jamdict) and word_combination not in potential_words:
#                 potential_words.append(word_combination)
#             else:
#                 break  # If the current combination is not a valid word, break out of the inner loop
#
#     return potential_words
