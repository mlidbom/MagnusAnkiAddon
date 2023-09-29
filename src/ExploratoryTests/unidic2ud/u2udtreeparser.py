from unidic2ud import UDPipeEntry

from src.ExploratoryTests.unidic2ud.u2udtreenode import U2UdTreeNode


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

def tree_parse_algorithm_1(result_tokens:list[UDPipeEntry], depth:int) -> list[list[UDPipeEntry]]:
    compounds: list[list[UDPipeEntry]] = []
    remaining_tokens = result_tokens.copy()
    while remaining_tokens:
        compound_start = remaining_tokens[0]
        compound_head: UDPipeEntry = _head(compound_start)
        token_index = 1

        token_index += _consume_children_of(compound_start, remaining_tokens[token_index:])

        if depth >= 3:
            token_index += _consume_until(compound_head, remaining_tokens[token_index:])

        if len(remaining_tokens) > token_index:
            if (depth >= 3
                    or depth >= 2
                    or depth >= 1 and compound_head.id == compound_start.id + 1):
                current_token = remaining_tokens[token_index]
                if current_token.id == compound_head.id:
                    token_index += 1
                    token_index += _consume_children_of(compound_head, remaining_tokens[token_index:])

        consumed_tokens = remaining_tokens[:token_index]
        remaining_tokens = remaining_tokens[token_index:]
        compounds.append(consumed_tokens)
    return compounds


def _head(token:UDPipeEntry) -> UDPipeEntry:
    return token.head # noqa

def parse(result_tokens) -> list[U2UdTreeNode]:
    result_tokens = result_tokens[1:]  # The first is some empty thingy we don't want.
    depth = 3
    compounds = tree_parse_algorithm_1(result_tokens, depth)
    while len(compounds) == 1 and depth > 1:
        depth -= 1
        compounds = tree_parse_algorithm_1(result_tokens, depth)

    return [U2UdTreeNode.create(compound, depth) for compound in compounds]

def parse_recursive(result_tokens, depth:int) -> list[U2UdTreeNode]:
    compounds = tree_parse_algorithm_1(result_tokens, depth)
    while len(compounds) == 1 and depth > 1:
        depth -= 1
        compounds = tree_parse_algorithm_1(result_tokens, depth)

    if len(compounds) == 1:
        compounds = []

    return [U2UdTreeNode.create(phrase, depth) for phrase in compounds]