# from __future__ import annotations
#
# from typing import TYPE_CHECKING
#
# if TYPE_CHECKING:
#     from collections.abc import Callable
#     from concurrent.futures import Future
#
#     from jaslib.note.kanjinote import KanjiNote
#     from jaslib.ui.web.pre_rendering_content_renderer import PreRenderingContentRenderer
#
#
# def create_renderer(schedule_task: Callable[[Callable[[], str]], Future[str]]) -> PreRenderingContentRenderer[KanjiNote]:
#     """Factory method for KanjiNote renderer with all tag mappings."""
#     from jaslib.ui.web.kanji import dependencies_renderer, kanji_list_renderer, mnemonic_renderer, readings_renderer, vocab_list_renderer
#     from jaslib.ui.web.pre_rendering_content_renderer import PreRenderingContentRenderer
#
#     return PreRenderingContentRenderer({
#         "##DEPENDENCIES_LIST##": dependencies_renderer.render_dependencies_list,
#         "##MNEMONIC##": mnemonic_renderer.render_mnemonic,
#         "##KANJI_READINGS##": readings_renderer.render_katakana_onyomi,
#         "##VOCAB_LIST##": vocab_list_renderer.generate_vocab_html_list,
#         "##KANJI_LIST##": kanji_list_renderer.kanji_kanji_list,
#     }, schedule_task)
