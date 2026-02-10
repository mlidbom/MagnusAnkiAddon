# from __future__ import annotations
#
# from typing import TYPE_CHECKING
#
# if TYPE_CHECKING:
#     from collections.abc import Callable
#     from concurrent.futures import Future
#
#     from jaslib.note.sentences.sentencenote import SentenceNote
#     from jaslib.ui.web.pre_rendering_content_renderer import PreRenderingContentRenderer
#
#
# def create_renderer(schedule_task: Callable[[Callable[[], str]], Future[str]]) -> PreRenderingContentRenderer[SentenceNote]:
#     """Factory method for SentenceNote renderer with all tag mappings."""
#     from jaslib.ui.web.pre_rendering_content_renderer import PreRenderingContentRenderer
#     from jaslib.ui.web.sentence import sentence_renderer, ud_sentence_breakdown_renderer
#
#     return PreRenderingContentRenderer({
#         "##USER_QUESTION##": sentence_renderer.render_user_question,
#         "##SOURCE_QUESTION##": sentence_renderer.render_source_question,
#         "##SENTENCE_ANALYSIS##": ud_sentence_breakdown_renderer.render_sentence_analysis,
#     }, schedule_task)
