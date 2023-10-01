import spacy
from unidic2ud import unidic2ud

from parsing.universal_dependencies.universal_dependencies_parse_result import UniversalDependenciesParseResult
from sysutils.lazy import Lazy

class UDParser:
    def __init__(self, name: str):
        self.name = name
    def parse(self, text: str) -> UniversalDependenciesParseResult:
        pass

class UD2UDParser(UDParser):
    def __init__(self, name: str):
        super().__init__(name)
        self._lazy_parser = Lazy(lambda: unidic2ud.load(name if name != "built-in" else None))

    def parse(self, text: str) -> UniversalDependenciesParseResult:
        return UniversalDependenciesParseResult(self._lazy_parser.instance()(text))

class GinzaParser(UDParser):
    def __init__(self) -> None:
        super().__init__("ja_ginza")
        self._lazy_parser = Lazy(lambda: spacy.load("ja_ginza"))

    def parse(self, text: str) -> UniversalDependenciesParseResult:
        text = text.replace(" ", "").replace("　", "")
        return UniversalDependenciesParseResult(self._lazy_parser.instance()(text))


ginza = GinzaParser() # Yes. 15 Differences to gendai. 8 Better, 6 worse, one unclear.
gendai = UD2UDParser("gendai")  # Yes. 15 Differences to ginza. 6 Better, 8 worse, one unclear.
spoken = UD2UDParser("spoken")  # ??. Zero differences compared to gendai so far...

qkana = UD2UDParser("qkana")  # Maybe. 2 difference with gendai. One clearly better and used in tests(But would likely be caught by dictionary compounding that we want anyway.).
kindai = UD2UDParser("kindai")  # Maybe. 8 Differences with gendai. One clearly better and used in tests(But would likely be caught by dictionary compounding that we want anyway.).
default = UD2UDParser("built-in")  # Maybe. 14 differences with gendai. One clearly better and used in tests(But would likely be caught by dictionary compounding that we want anyway.).
kinsei = UD2UDParser("kinsei")  # Maybe. 6 differences with gendai. One clearly better and used in tests(But would likely be caught by dictionary compounding that we want anyway.). 1 arguably better

# novel = UD2UDParser("novel") # NO. 2 difference with gendai. Both worse. Not worth the odds to try for the user.
# kyogen = UD2UDParser("kyogen") # NO. 18 differences with gendai. Consistently strange. Did often pick up kanji 無い but that was the only upside.
# wakan = UD2UDParser("wakan") #NO. 27 differences with gendai. Consistently strange.
# wabun = UD2UDParser("wabun") #NO. 27 differences with gendai. Consistently strange.
# manyo = UD2UDParser("manyo") #NO. 25 differences with gendai. Consistently strange.



best:UDParser = ginza

all_parsers:list[UDParser] = [gendai,
                              spoken,
                              qkana,
                              kindai,
                              default,
                              kinsei,
                              ginza,
                              # novel, kyogen, wakan, wabun, manyo
                              ]
