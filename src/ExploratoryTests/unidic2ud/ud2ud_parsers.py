from unidic2ud import unidic2ud, UniDic2UDEntry

from sysutils.lazy import Lazy


class UD2UDParser:
    def __init__(self, name: str ):
        self.name = name
        self._lazy_parser = Lazy(lambda: unidic2ud.load(name if name != "built-in" else None))

    def parse(self, text: str) -> UniDic2UDEntry:
        return self._lazy_parser.instance()(text)


gendai = UD2UDParser("gendai")  # the leader so far
best = gendai

kindai = UD2UDParser("kindai")  # seems slightly less accurate than gendai.
default = UD2UDParser("built-in")  # As alternative? When differing from kindai, usually seems worse but significantly different. Polarity negative feature. Good for something?
spoken = UD2UDParser("spoken") # todo Recheck
kinsei_edo = UD2UDParser("kinsei\\50c_kinsei-edo") # todo Recheck
kinsei_kindai_bungo = UD2UDParser("kinsei\\60a_kindai-bungo") # todo Recheck
novel = UD2UDParser("novel") # todo Recheck
qkana = UD2UDParser("qkana") # todo Recheck
kyogen = UD2UDParser("kyogen") # todo Recheck
wakan = UD2UDParser("wakan") #No. wakan gives wack results
wabun = UD2UDParser("wabun") #No. oddness abounds
manyo = UD2UDParser("manyo") #No. seems to usually give some truly strange results