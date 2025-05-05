from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_location import TokenTextLocation


def forward_list(node_: TokenTextLocation, length: int) -> list[TokenTextLocation]:
    result:list[TokenTextLocation] = []
    index = 0
    node:Optional[TokenTextLocation] = node_
    while node is not None and index <= length:
        result.append(node)
        node = node.next
        index += 1
    return result
