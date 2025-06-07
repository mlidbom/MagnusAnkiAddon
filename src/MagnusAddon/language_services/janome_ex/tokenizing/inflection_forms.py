from __future__ import annotations

all_dict: dict[str, InflectionForm] = {}

class InflectionForm:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

def _add_form(name: str, description: str) -> InflectionForm:
    form = InflectionForm(name, description)
    all_dict[name] = form
    return form

class InflectionForms:
    special_noun_connection = _add_form("体言接続特殊", "Special noun connection - Connects to nouns in special cases")

    all_string: set[str] = {
        "体言接続特殊",  # Special noun connection - Connects to nouns in special cases
        "連用ゴザイ接続",  # Continuative gozai connection - Links to polite auxiliary "gozai" (polite form)
        "命令ｅ",  # Imperative e-form - Command form ending in "e"
        "未然特殊",  # Special irrealis - Special form of the negative stem
        "仮定形",  # Hypothetical form - Used in conditional expressions
        "基本形",  # Basic form - Dictionary/plain form
        "命令ｙｏ",  # Imperative yo-form - Command form ending in "yo"
        "未然ウ接続",  # Irrealis u-connection - Connects to volitional auxiliary "u"
        "基本形-促音便",  # Basic form with gemination - Dictionary form with consonant doubling
        "体言接続特殊２",  # Special noun connection 2 - Another variant of noun connection
        "命令ｒｏ",  # Imperative ro-form - Command form ending in "ro"
        "体言接続",  # Noun connection - Form that connects to nouns
        "命令ｉ",  # Imperative i-form - Command form ending in "i"
        "連用ニ接続",  # Continuative ni-connection - Connects to the particle "ni"
        "ガル接続",  # Garu connection - Connects to suffix "garu" (showing signs of)
        "連用タ接続",  # Continuative ta-connection - Connects to past tense marker "ta"
        "仮定縮約１",  # Hypothetical contraction 1 - Contracted conditional form
        "連用デ接続",  # Continuative de-connection - Connects to the te-form variant "de"
        "未然ヌ接続",  # Irrealis nu-connection - Connects to classical negative "nu"
        "未然レル接続",  # Irrealis reru-connection - Connects to passive/potential "reru"
        "文語基本形",  # Classical basic form - Dictionary form in classical Japanese
        "音便基本形",  # Euphonic basic form - Dictionary form with sound changes
        "連用テ接続",  # Continuative te-connection - Connects to te-form
        "連用形",  # Continuative form - Used for connecting verbs/adjectives
        "未然形",  # Irrealis form - Used for negatives and some auxiliaries
        "仮定縮約２"  # Hypothetical contraction 2 - Another contracted conditional form
    }
