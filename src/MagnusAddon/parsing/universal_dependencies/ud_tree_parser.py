from parsing.universal_dependencies.ud_tree_node import UDTreeNode
from parsing.universal_dependencies.ud_tree_parse_result import UDTreeParseResult
from parsing.universal_dependencies.core.ud_parser import UDParser
from parsing.universal_dependencies.core.ud_token import UDToken
from sysutils import ex_list, ex_predicate

class _Depth:
    surface_0 = 0
    depth_1 = 1
    depth_2 = 2
    depth_3 = 3
    morphemes_4 = 4

def parse(parser: UDParser, text: str) -> UDTreeParseResult:
    tokens = parser.parse(text).tokens
    depth = 0
    compounds = _build_compounds(tokens, depth)
    while len(compounds) == 1 and depth < _Depth.depth_2:  # making the whole text into a compound is not usually desired, but above depth 2 we loose words, so don't go that deep.
        depth += 1
        compounds = _build_compounds(tokens, depth)
    return UDTreeParseResult(*[_create_node(compound, depth) for compound in compounds])

def _build_compounds(tokens: list[UDToken], depth: int) -> list[list[UDToken]]:
    if depth == _Depth.morphemes_4: return [[token] for token in tokens]

    created_compounds: list[list[UDToken]] = []
    unconsumed_tokens = tokens.copy()
    while unconsumed_tokens:
        compound_start = unconsumed_tokens.pop(0)
        compound_tokens = [compound_start]
        compound_head = compound_start.head
        created_compounds.append(compound_tokens) #python += mutates lists in place so this is safe
        compound_head_directly_follows_compound_start = compound_head.id == compound_start.id + 1

        compound_tokens += ex_list.consume_while(compound_start.is_parent_of, unconsumed_tokens)

        if depth == _Depth.surface_0:
            compound_tokens += ex_list.consume_until_before(ex_predicate.eq_(compound_head), unconsumed_tokens)

        if unconsumed_tokens:
            if (depth == _Depth.surface_0
                    or depth == _Depth.depth_1
                    or depth == _Depth.depth_2 and compound_head_directly_follows_compound_start):
                current_token = unconsumed_tokens[0]
                if current_token == compound_head:
                    compound_tokens.append(unconsumed_tokens.pop(0))
                    compound_tokens += ex_list.consume_while(compound_head.is_parent_of, unconsumed_tokens)

    return created_compounds

def _create_node(tokens: list[UDToken], depth: int) -> 'UDTreeNode':
    children = _build_child_compounds(tokens, depth + 1) if len(tokens) > 1 else []
    surface = "".join(tok.form for tok in tokens)
    base = "".join(tok.form for tok in tokens[:-1]) + tokens[-1].lemma
    return UDTreeNode(surface, base, children, tokens)

def _build_child_compounds(parent_node_tokens: list[UDToken], depth: int) -> list[UDTreeNode]:
    compounds = _build_compounds(parent_node_tokens, depth)
    while len(compounds) == 1 and depth <= _Depth.morphemes_4:  # if len == 1 the result is identical to the parent, go down in granularity and try again
        depth += 1
        compounds = _build_compounds(parent_node_tokens, depth)

    return [_create_node(phrase, depth) for phrase in compounds]
