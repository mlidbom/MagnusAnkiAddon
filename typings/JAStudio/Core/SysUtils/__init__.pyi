import abc

class ExStr(abc.ABC):
    @staticmethod
    def StripHtmlAndBracketMarkupAndNoiseCharacters(input: str) -> str: ...

