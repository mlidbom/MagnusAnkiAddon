# noinspection PyUnusedClass, PyUnusedName
from __future__ import annotations

from typing import override

from ex_autoslot import ProfilableAutoSlots

all_dict: dict[str, InflectionForm] = {}

class InflectionForm(ProfilableAutoSlots):
    def __init__(self, name: str, description: str) -> None:
        self.name: str = name
        self.description: str = description

    @override
    def __repr__(self) -> str: return f"""{self.name} - {self.description}"""
    @override
    def __str__(self) -> str: return self.name

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, InflectionForm):
            return self.name == other.name
        return False

    @override
    def __hash__(self) -> int: return hash(self.name)

def _add_form(name: str, description: str) -> InflectionForm:
    form = InflectionForm(name, description)
    all_dict[name] = form
    return form

# noinspection PyUnusedClass,PyUnusedName
class InflectionForms(ProfilableAutoSlots):
    unknowm: InflectionForm = _add_form("*", "Unknown")

    # noinspection PyUnusedClass,PyUnusedName
    class Basic(ProfilableAutoSlots):
        dictionary_form: InflectionForm = _add_form("基本形", "Basic form - Dictionary/plain form")
        gemination: InflectionForm = _add_form("基本形-促音便", "Basic form with gemination - Dictionary form with consonant doubling")
        euphonic: InflectionForm = _add_form("音便基本形", "Euphonic basic form - Dictionary form with sound changes")
        classical: InflectionForm = _add_form("文語基本形", "Classical basic form - Dictionary form in classical Japanese")

    # noinspection PyUnusedClass,PyUnusedName
    class Continuative(ProfilableAutoSlots):
        renyoukei_masu_stem: InflectionForm = _add_form("連用形", "Continuative - masu-stem/i-stem [読み] - verbs/adjective")
        te_connection: InflectionForm = _add_form("連用テ接続", "Continuative te-connection - Connects to te-form")
        ta_connection: InflectionForm = _add_form("連用タ接続", 'Continuative ta-connection - Connects to past tense marker "ta"')
        de_connection: InflectionForm = _add_form("連用デ接続", 'Continuative de-connection - Connects to the te-form variant "de"')
        ni_connection: InflectionForm = _add_form("連用ニ接続", 'Continuative ni-connection - Connects to the particle "ni"')
        gozai_connection: InflectionForm = _add_form("連用ゴザイ接続", 'Continuative gozai connection - Links to polite auxiliary "gozai" (polite form)')

    # noinspection PyUnusedClass,PyUnusedName
    class Misc(ProfilableAutoSlots):
        garu_connection: InflectionForm = _add_form("ガル接続", 'Garu connection - Connects to suffix "garu" (showing signs of)')

    # noinspection PyUnusedClass,PyUnusedName
    class Irrealis(ProfilableAutoSlots):
        general_irrealis_mizenkei: InflectionForm = _add_form("未然形", "Irrealis - a-stem [読ま] - for negatives and some auxiliaries")
        special_irrealis: InflectionForm = _add_form("未然特殊", "Irrealis - Special - Special form of the negative stem")
        u_connection: InflectionForm = _add_form("未然ウ接続", 'Irrealis u-connection - Connects to volitional auxiliary "u"')
        nu_connection: InflectionForm = _add_form("未然ヌ接続", 'Irrealis nu-connection - Connects to classical negative "nu"')
        reru_connection: InflectionForm = _add_form("未然レル接続", 'Irrealis reru-connection - Connects to passive/potential "reru"')

    # noinspection PyUnusedClass,PyUnusedName
    class Hypothetical(ProfilableAutoSlots):
        general_hypothetical_kateikei: InflectionForm = _add_form("仮定形", "Hypothetical/potential - e-stem [読め] - of verbs and adjectives.")
        contraction1: InflectionForm = _add_form("仮定縮約１", "Hypothetical form of verbs and adjectives contraction version 1")
        contraction2: InflectionForm = _add_form("仮定縮約２", "Hypothetical form of verbs and adjectives contraction version 2")

    # noinspection PyUnusedClass,PyUnusedName
    class ImperativeMeireikei(ProfilableAutoSlots):
        e: InflectionForm = _add_form("命令ｅ", 'Imperative/command/meireikei -  e-stem[読め] - Command form ending in "e"')
        ro: InflectionForm = _add_form("命令ｒｏ", 'Imperative/command/meireikei - ro [食べろ] - Command form ending in "ro"')
        yo: InflectionForm = _add_form("命令ｙｏ", 'Imperative/command/meireikei - yo [食べよ] - Command form ending in "yo"')
        i: InflectionForm = _add_form("命令ｉ", 'Imperative/command/meireikei - i-form - Command form ending in "i"')

    # noinspection PyUnusedClass,PyUnusedName
    class NounConnection(ProfilableAutoSlots):
        general_noun_connection: InflectionForm = _add_form("体言接続", "Noun connection - Form that connects to nouns")
        special_1: InflectionForm = _add_form("体言接続特殊", "Special noun connection - Connects to nouns in special cases")
        special_2: InflectionForm = _add_form("体言接続特殊２", "Special noun connection 2 - Another variant of noun connection")
