from __future__ import annotations

all_dict: dict[str, InflectionForm] = {}

class InflectionForm:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def __eq__(self, other: object) -> bool:
        if isinstance(other, InflectionForm):
            return self.name == other.name
        return False

def _add_form(name: str, description: str) -> InflectionForm:
    form = InflectionForm(name, description)
    all_dict[name] = form
    return form

class InflectionForms:
    special_noun_connection = _add_form("体言接続特殊", "Special noun connection - Connects to nouns in special cases")
    continuative_gozai_connection = _add_form("連用ゴザイ接続", 'Continuative gozai connection - Links to polite auxiliary "gozai" (polite form)')
    imperative_e = _add_form("命令ｅ", 'Imperative e-form - Command form ending in "e"')
    special_irrealis = _add_form("未然特殊", "Special irrealis - Special form of the negative stem")
    hypothetical_form = _add_form("仮定形", "Hypothetical form - Used in conditional expressions")
    basic_form = _add_form("基本形", "Basic form - Dictionary/plain form")
    imperative_yo = _add_form("命令ｙｏ", 'Imperative yo-form - Command form ending in "yo"')
    irrealis_u_connection = _add_form("未然ウ接続", 'Irrealis u-connection - Connects to volitional auxiliary "u"')
    basic_form_gemination = _add_form("基本形-促音便", "Basic form with gemination - Dictionary form with consonant doubling")
    special_noun_connection2 = _add_form("体言接続特殊２", "Special noun connection 2 - Another variant of noun connection")
    imperative_ro = _add_form("命令ｒｏ", 'Imperative ro-form - Command form ending in "ro"')
    noun_connection = _add_form("体言接続", "Noun connection - Form that connects to nouns")
    imperative_i = _add_form("命令ｉ", 'Imperative i-form - Command form ending in "i"')
    continuative_ni_connection = _add_form("連用ニ接続", 'Continuative ni-connection - Connects to the particle "ni"')
    garu_connection = _add_form("ガル接続", 'Garu connection - Connects to suffix "garu" (showing signs of)')
    continuative_ta_connection = _add_form("連用タ接続", 'Continuative ta-connection - Connects to past tense marker "ta"')
    hypothetical_contraction1 = _add_form("仮定縮約１", "Hypothetical contraction 1 - Contracted conditional form")
    continuative_de_connection = _add_form("連用デ接続", 'Continuative de-connection - Connects to the te-form variant "de"')
    irrealis_nu_connection = _add_form("未然ヌ接続", 'Irrealis nu-connection - Connects to classical negative "nu"')
    irrealis_reru_connection = _add_form("未然レル接続", 'Irrealis reru-connection - Connects to passive/potential "reru"')
    classical_basic_form = _add_form("文語基本形", "Classical basic form - Dictionary form in classical Japanese")
    euphonic_basic_form = _add_form("音便基本形", "Euphonic basic form - Dictionary form with sound changes")
    continuative_te_connection = _add_form("連用テ接続", "Continuative te-connection - Connects to te-form")
    continuative_form = _add_form("連用形", "Continuative form - Used for connecting verbs/adjectives")
    irrealis_form = _add_form("未然形", "Irrealis form - Used for negatives and some auxiliaries")
    hypothetical_contraction2 = _add_form("仮定縮約２", "Hypothetical contraction 2 - Another contracted conditional form")
