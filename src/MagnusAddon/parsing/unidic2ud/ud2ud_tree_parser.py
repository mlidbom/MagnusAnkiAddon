from unidic2ud import UDPipeEntry

from parsing.unidic2ud.ud2ud_tree_node import UD2UDTreeNode
from parsing.unidic2ud.ud2ud_tree_parser_result import UD2UDParseResult
from parsing.unidic2ud.ud2ud_parsers import UD2UDParser


def _consume_children_of(entry:UDPipeEntry, tokens:list[UDPipeEntry]) -> int:
    index = 0
    for current_token in tokens:
        if _head(current_token).id != entry.id:
            break
        index += 1
    return index

def _consume_until(entry:UDPipeEntry, tokens:list[UDPipeEntry]) -> int:
    index = 0
    for current_token in tokens:
        if current_token.id == entry.id:
            break
        index += 1
    return index

def _tree_parse_algorithm_1(result_tokens:list[UDPipeEntry], depth:int) -> list[list[UDPipeEntry]]:
    if depth > 3:
        raise Exception("whut?")

    compounds: list[list[UDPipeEntry]] = []
    remaining_tokens = result_tokens.copy()
    while remaining_tokens:
        compound_start = remaining_tokens[0]
        compound_head: UDPipeEntry = _head(compound_start)
        token_index = 1

        token_index += _consume_children_of(compound_start, remaining_tokens[token_index:])

        if depth == 0:
            token_index += _consume_until(compound_head, remaining_tokens[token_index:])

        if len(remaining_tokens) > token_index:
            if (depth == 0
                    or depth == 1
                    or depth == 2 and compound_head.id == compound_start.id + 1):
                current_token = remaining_tokens[token_index]
                if current_token.id == compound_head.id:
                    token_index += 1
                    token_index += _consume_children_of(compound_head, remaining_tokens[token_index:])

        consumed_tokens = remaining_tokens[:token_index]
        remaining_tokens = remaining_tokens[token_index:]
        compounds.append(consumed_tokens)
    return compounds

class Depth: #??????
    surface = 0
    phrases = 1
    conjugations = 2
    words = 3
    morphemes = 4

def _head(token:UDPipeEntry) -> UDPipeEntry:
    return token.head # noqa

def parse(parser:UD2UDParser, text: str) -> UD2UDParseResult:
    return parse_internal(parser.parse(text))

def parse_internal(result_tokens) -> UD2UDParseResult:
    result_tokens = result_tokens[1:]  # The first is some empty thingy we don't want.
    depth = 0
    compounds = _tree_parse_algorithm_1(result_tokens, depth)
    while len(compounds) == 1 and depth < 2: # making the whole text into a compound is not usually desired, but above depth 2 we loose whole words, not just subphrases, so don't go that deep.
        depth += 1
        compounds = _tree_parse_algorithm_1(result_tokens, depth)

    return UD2UDParseResult(*[UD2UDTreeNode.create(compound, depth) for compound in compounds])

def parse_recursive(parent_node_tokens, depth:int) -> list[UD2UDTreeNode]:
    compounds = _tree_parse_algorithm_1(parent_node_tokens, depth)
    #todo using depth > 1 here instead often avoids nesting compound levels (e.g. さんは, 私を, 女性に, OBS:自分から is counter example...) that may not be desired by the user. Maybe expose as option?
    while len(compounds) < 2 and depth <= 2: # if len == 1 the result is identical to the parent, go down in granularity and try again
        depth += 1
        compounds = _tree_parse_algorithm_1(parent_node_tokens, depth)

    if len(compounds) == 1: # No compound children. Create children from the individual tokens
        return [UD2UDTreeNode.create([token], depth) for token in compounds[0]]

    return [UD2UDTreeNode.create(phrase, depth) for phrase in compounds]