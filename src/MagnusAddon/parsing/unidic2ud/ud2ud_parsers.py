from unidic2ud import unidic2ud, UniDic2UDEntry

from sysutils.lazy import Lazy


class UD2UDParser:
    def __init__(self, name: str):
        self.name = name
        self._lazy_parser = Lazy(lambda: unidic2ud.load(name if name != "built-in" else None))

    def parse(self, text: str) -> UniDic2UDEntry:
        return self._lazy_parser.instance()(text)


gendai = UD2UDParser("gendai") # The leader so far, quite accurate
spoken = UD2UDParser("spoken") # ??. Zero differences compared to gendai so far...

#alternatives?
kindai = UD2UDParser("kindai")  # Yes. 8 Differences. One clearly better and used in tests. 60+% of the times it differs from gendai, gendai is better.
default = UD2UDParser("built-in")  # Maybe. 14 differences. 80-90% worse, but different in ways that may sometimes be what one wants...
kinsei = UD2UDParser("kinsei") # Maybe. 6 differences. 1 better, 1 arguably better

novel = UD2UDParser("novel") # NO. 1 difference with gendai and it was worse. Not worth the odds to try for the user.
qkana = UD2UDParser("qkana") # NO. 1 difference with gendai and it was worse.



kyogen = UD2UDParser("kyogen") # NO. 18 differences. Consistently strange. Did often pick up kanji 無い but that was the only upside.
wakan = UD2UDParser("wakan") #NO. 27 differences. Consistently strange.
wabun = UD2UDParser("wabun") #NO. 27 differences. Consistently strange.
manyo = UD2UDParser("manyo") #NO. 25 differences. Consistently strange.

best = gendai