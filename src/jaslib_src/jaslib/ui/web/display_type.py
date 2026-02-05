from __future__ import annotations


class DisplayType:
    """Display type constants and checks. Portable to C#."""
    REVIEW_QUESTION: str = "reviewQuestion"
    REVIEW_ANSWER: str = "reviewAnswer"
    _ANSWER_TYPES: set[str] = {"reviewAnswer", "previewAnswer", "clayoutAnswer"}

    @staticmethod
    def is_displaying_answer(display_type: str) -> bool:
        return display_type in DisplayType._ANSWER_TYPES

    @staticmethod
    def is_displaying_review_question(display_type: str) -> bool:
        return display_type == DisplayType.REVIEW_QUESTION

    @staticmethod
    def is_displaying_review_answer(display_type: str) -> bool:
        return display_type == DisplayType.REVIEW_ANSWER
