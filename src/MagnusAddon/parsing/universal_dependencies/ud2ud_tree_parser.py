from parsing.universal_dependencies.ud2ud_tree_node import UD2UDTreeNode
from parsing.universal_dependencies.ud2ud_tree_parser_result import UD2UDParseResult
from parsing.universal_dependencies.ud2ud_parsers import UD2UDParser
from parsing.universal_dependencies.universal_dependencies_token import UDToken


def _consume_children_of(entry:UDToken, tokens:list[UDToken]) -> int:
    index = 0
    for current_token in tokens:
        if current_token.head.id != entry.id:
            break
        index += 1
    return index

def _consume_until(entry:UDToken, tokens:list[UDToken]) -> int:
    index = 0
    for current_token in tokens:
        if current_token.id == entry.id:
            break
        index += 1
    return index

def _build_compounds(tokens:list[UDToken], depth:int) -> list[list[UDToken]]:
    if depth == _Depth.morphemes_4:
        return [[token] for token in tokens]

    compounds: list[list[UDToken]] = []
    remaining_tokens = tokens.copy()
    while remaining_tokens:
        compound_start = remaining_tokens[0]
        compound_head = compound_start.head
        token_index = 1

        token_index += _consume_children_of(compound_start, remaining_tokens[token_index:])

        if depth == _Depth.surface_0:
            token_index += _consume_until(compound_head, remaining_tokens[token_index:])

        if len(remaining_tokens) > token_index:
            if (depth == _Depth.surface_0
                    or depth == _Depth.depth_1
                    or depth == _Depth.depth_2 and compound_head.id == compound_start.id + 1):
                current_token = remaining_tokens[token_index]
                if current_token.id == compound_head.id:
                    token_index += 1
                    token_index += _consume_children_of(compound_head, remaining_tokens[token_index:])

        consumed_tokens = remaining_tokens[:token_index]
        remaining_tokens = remaining_tokens[token_index:]
        compounds.append(consumed_tokens)
    return compounds

class _Depth:
    surface_0 = 0
    depth_1 = 1
    depth_2 = 2
    depth_3 = 3
    morphemes_4 = 4

def parse(parser:UD2UDParser, text: str) -> UD2UDParseResult:
    tokens = parser.parse(text).tokens[1:]  # The first token always empty.
    depth = 0
    compounds = _build_compounds(tokens, depth)
    while len(compounds) == 1 and depth < _Depth.depth_2:  # making the whole text into a compound is not usually desired, but above depth 2 we loose words, so don't go that deep.
        depth += 1
        compounds = _build_compounds(tokens, depth)
    return UD2UDParseResult(*[UD2UDTreeNode.create(compound, depth) for compound in compounds])


def _parse_recursive(parent_node_tokens, depth:int) -> list[UD2UDTreeNode]:
    compounds = _build_compounds(parent_node_tokens, depth)
    while len(compounds) < 2 and depth <= _Depth.morphemes_4: # if len == 1 the result is identical to the parent, go down in granularity and try again
        depth += 1
        compounds = _build_compounds(parent_node_tokens, depth)

    return [UD2UDTreeNode.create(phrase, depth) for phrase in compounds]