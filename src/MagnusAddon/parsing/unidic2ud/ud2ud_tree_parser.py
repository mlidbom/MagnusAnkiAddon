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
    if depth == Depth.morphemes_4:
        return [[token] for token in result_tokens]

    compounds: list[list[UDPipeEntry]] = []
    remaining_tokens = result_tokens.copy()
    while remaining_tokens:
        compound_start = remaining_tokens[0]
        compound_head: UDPipeEntry = _head(compound_start)
        token_index = 1

        token_index += _consume_children_of(compound_start, remaining_tokens[token_index:])

        if depth == Depth.surface_0:
            token_index += _consume_until(compound_head, remaining_tokens[token_index:])

        if len(remaining_tokens) > token_index:
            if (depth == Depth.surface_0
                    or depth == Depth.depth_1
                    or depth == Depth.depth_2 and compound_head.id == compound_start.id + 1):
                current_token = remaining_tokens[token_index]
                if current_token.id == compound_head.id:
                    token_index += 1
                    token_index += _consume_children_of(compound_head, remaining_tokens[token_index:])

        consumed_tokens = remaining_tokens[:token_index]
        remaining_tokens = remaining_tokens[token_index:]
        compounds.append(consumed_tokens)
    return compounds

class Depth:
    surface_0 = 0
    depth_1 = 1
    depth_2 = 2
    depth_3 = 3
    morphemes_4 = 4

def _head(token:UDPipeEntry) -> UDPipeEntry:
    return token.head # noqa

def parse(parser:UD2UDParser, text: str) -> UD2UDParseResult:
    return parse_internal(parser.parse(text))

def parse_internal(result_tokens) -> UD2UDParseResult:
    result_tokens = result_tokens[1:]  # The first is some empty thingy we don't want.
    depth = 0
    compounds: list[list[UDPipeEntry]] = _tree_parse_algorithm_1(result_tokens, depth)
    while len(compounds) == 1 and depth < Depth.depth_2: # making the whole text into a compound is not usually desired, but above depth 2 we loose words, so don't go that deep.
        depth += 1
        compounds = _tree_parse_algorithm_1(result_tokens, depth)

    return UD2UDParseResult(*[UD2UDTreeNode.create(compound, depth) for compound in compounds])

def parse_recursive(parent_node_tokens, depth:int) -> list[UD2UDTreeNode]:
    compounds = _tree_parse_algorithm_1(parent_node_tokens, depth)
    #todo using depth > 1 here instead often avoids nesting compound levels (e.g. さんは, 私を, 女性に, OBS:自分から is counter example...) that may not be desired by the user. Maybe expose as option?
    while len(compounds) < 2 and depth <= Depth.morphemes_4: # if len == 1 the result is identical to the parent, go down in granularity and try again
        depth += 1
        compounds = _tree_parse_algorithm_1(parent_node_tokens, depth)

    return [UD2UDTreeNode.create(phrase, depth) for phrase in compounds]