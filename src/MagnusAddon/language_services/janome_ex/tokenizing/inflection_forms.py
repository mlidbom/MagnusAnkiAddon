# noinspection PyUnusedClass, PyUnusedName
from __future__ import annotations

all_dict: dict[str, InflectionForm] = {}

class InflectionForm:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def __repr__(self) -> str: return f"""{self.name} - {self.description}"""

    def __eq__(self, other: object) -> bool:
        if isinstance(other, InflectionForm):
            return self.name == other.name
        return False

def _add_form(name: str, description: str) -> InflectionForm:
    form = InflectionForm(name, description)
    all_dict[name] = form
    return form

# noinspection PyUnusedClass
class InflectionForms:
    # noinspection PyUnusedClass,PyUnusedName
    class Basic:
        general_basic = _add_form("基本形", "Basic form - Dictionary/plain form")
        gemination = _add_form("基本形-促音便", "Basic form with gemination - Dictionary form with consonant doubling")
        euphonic = _add_form("音便基本形", "Euphonic basic form - Dictionary form with sound changes")
        classical = _add_form("文語基本形", "Classical basic form - Dictionary form in classical Japanese")

    # noinspection PyUnusedClass,PyUnusedName
    class Continuative:
        general_continuative = _add_form("連用形", "Continuative form - Used for connecting verbs/adjectives")
        te_connection = _add_form("連用テ接続", "Continuative te-connection - Connects to te-form")
        ta_connection = _add_form("連用タ接続", 'Continuative ta-connection - Connects to past tense marker "ta"')
        de_connection = _add_form("連用デ接続", 'Continuative de-connection - Connects to the te-form variant "de"')
        ni_connection = _add_form("連用ニ接続", 'Continuative ni-connection - Connects to the particle "ni"')
        gozai_connection = _add_form("連用ゴザイ接続", 'Continuative gozai connection - Links to polite auxiliary "gozai" (polite form)')

    # noinspection PyUnusedClass,PyUnusedName
    class Misc:
        garu_connection = _add_form("ガル接続", 'Garu connection - Connects to suffix "garu" (showing signs of)')

    # noinspection PyUnusedClass,PyUnusedName
    class Irrealis:
        general_irrealis = _add_form("未然形", "Irrealis form - Used for negatives and some auxiliaries")
        special_irrealis = _add_form("未然特殊", "Special irrealis - Special form of the negative stem")
        u_connection = _add_form("未然ウ接続", 'Irrealis u-connection - Connects to volitional auxiliary "u"')
        nu_connection = _add_form("未然ヌ接続", 'Irrealis nu-connection - Connects to classical negative "nu"')
        reru_connection = _add_form("未然レル接続", 'Irrealis reru-connection - Connects to passive/potential "reru"')

    # noinspection PyUnusedClass,PyUnusedName
    class Hypothetical:
        general_hypothetical = _add_form("仮定形", "Hypothetical form - Used in conditional expressions")
        contraction1 = _add_form("仮定縮約１", "Hypothetical contraction 1 - Contracted conditional form")
        contraction2 = _add_form("仮定縮約２", "Hypothetical contraction 2 - Another contracted conditional form")

    # noinspection PyUnusedClass,PyUnusedName
    class Imperative:
        e = _add_form("命令ｅ", 'Imperative e-form - Command form ending in "e"')
        ro = _add_form("命令ｒｏ", 'Imperative ro-form - Command form ending in "ro"')
        yo = _add_form("命令ｙｏ", 'Imperative yo-form - Command form ending in "yo"')
        i = _add_form("命令ｉ", 'Imperative i-form - Command form ending in "i"')

    # noinspection PyUnusedClass,PyUnusedName
    class NounConnection:
        general_noun_connection = _add_form("体言接続", "Noun connection - Form that connects to nouns")
        special_1 = _add_form("体言接続特殊", "Special noun connection - Connects to nouns in special cases")
        special_2 = _add_form("体言接続特殊２", "Special noun connection 2 - Another variant of noun connection")
