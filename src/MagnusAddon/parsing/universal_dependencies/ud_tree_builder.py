from parsing.universal_dependencies.ud_tree_node import UDTextTreeNode
from parsing.universal_dependencies.ud_tree_parse_result import UDTextTree
from parsing.universal_dependencies.core.ud_parser import UDParser
from parsing.universal_dependencies.core.ud_token import UDToken
from sysutils import ex_list, ex_predicate

class _Depth:
    surface_0 = 0
    depth_1 = 1
    depth_2 = 2
    depth_3 = 3
    morphemes_4 = 4

def build_tree(parser: UDParser, text: str) -> UDTextTree:
    tokens = parser.parse(text).tokens
    depth = 0
    compounds = _build_compounds(tokens, depth)
    while len(compounds) == 1 and depth < _Depth.depth_2:  # making the whole text into a compound is not usually desired, but above depth 2 we loose words, so don't go that deep.
        depth += 1
        compounds = _build_compounds(tokens, depth)
    return UDTextTree(*[_create_node(compound, depth) for compound in compounds])

def _build_compounds(tokens: list[UDToken], depth: int) -> list[list[UDToken]]:
    if depth == _Depth.morphemes_4: return [[token] for token in tokens]

    created_compounds: list[list[UDToken]] = []
    unconsumed_tokens = tokens.copy()
    while unconsumed_tokens:
        compound = [unconsumed_tokens.pop(0)]
        compound += ex_list.consume_while(compound[0].is_parent_of, unconsumed_tokens)

        if depth == _Depth.surface_0:
            compound += ex_list.consume_until_before(ex_predicate.eq_(compound[0].head), unconsumed_tokens)

        if unconsumed_tokens:
            if (depth == _Depth.surface_0
                    or depth == _Depth.depth_1
                    or depth == _Depth.depth_2 and compound[0].head.id == compound[0].id + 1):
                if unconsumed_tokens[0] == compound[0].head:
                    compound.append(unconsumed_tokens.pop(0))
                    compound += ex_list.consume_while(compound[0].head.is_parent_of, unconsumed_tokens)
                    
        created_compounds.append(compound)

    return created_compounds

def _create_node(tokens: list[UDToken], depth: int) -> 'UDTextTreeNode':
    children = _build_child_compounds(tokens, depth + 1) if len(tokens) > 1 else []
    surface = "".join(tok.form for tok in tokens)
    base = "".join(tok.form for tok in tokens[:-1]) + tokens[-1].lemma
    return UDTextTreeNode(surface, base, children, tokens)

def _build_child_compounds(parent_node_tokens: list[UDToken], depth: int) -> list[UDTextTreeNode]:
    compounds = _build_compounds(parent_node_tokens, depth)
    while len(compounds) == 1 and depth <= _Depth.morphemes_4:  # if len == 1 the result is identical to the parent, go down in granularity and try again
        depth += 1
        compounds = _build_compounds(parent_node_tokens, depth)

    return [_create_node(phrase, depth) for phrase in compounds]