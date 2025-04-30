from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from language_services.janome_ex.word_extraction.text_location import TextLocation


def forward_list(node_: TextLocation, length: int) -> list[T]:
    result:list[TextLocation] = [node_]
    index = 0
    node:Optional[TextLocation] = node_
    while node is not None and index < length:
        result.append(node)
        node = node.next
        index += 1
    return result
