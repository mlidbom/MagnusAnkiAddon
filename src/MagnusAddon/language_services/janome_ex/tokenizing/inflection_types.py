####Inflection types ###########
from __future__ import annotations

all_dict: dict[str, InflectionType] = {}

class InflectionType:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def __eq__(self, other: object) -> bool:
        if isinstance(other, InflectionType):
            return self.name == other.name
        return False

def _add_form(name: str, description: str) -> InflectionType:
    form = InflectionType(name, description)
    all_dict[name] = form
    return form

class InflectionTypes:
    class Godan:
        sa_ending: InflectionType = _add_form("五段・サ行", "Godan verb with 'sa' ending - Changes 'sa' stem in conjugation")

godan: set[str] = {
    "五段・サ行",  # Godan verb with 'sa' ending - Changes 'sa' stem in conjugation
    "五段・ラ行",  # Godan verb with 'ra' ending - Changes 'ra' stem in conjugation
    "五段・マ行",  # Godan verb with 'ma' ending - Changes 'ma' stem in conjugation
    "五段・バ行",  # Godan verb with 'ba' ending - Changes 'ba' stem in conjugation
    "五段・ワ行促音便",  # Godan verb with 'wa' ending and 'っ' consonant assimilation - Special 'wa' conjugation pattern
    "五段・カ行促音便ユク",  # Godan verb 'yuku' (to go) with 'ka' ending and consonant assimilation - Special case verb
    "五段・ワ行ウ音便",  # Godan verb with 'wa' ending and 'u' sound change - Special 'wa' conjugation pattern
    "五段・ナ行",  # Godan verb with 'na' ending - Changes 'na' stem in conjugation
    "五段・カ行促音便",  # Godan verb with 'ka' ending and consonant assimilation - Special 'ka' conjugation pattern
    "五段・タ行",  # Godan verb with 'ta' ending - Changes 'ta' stem in conjugation
    "五段・ガ行",  # Godan verb with 'ga' ending - Changes 'ga' stem in conjugation
    "五段・ラ行特殊",  # Special godan verb with 'ra' ending - Irregular 'ra' conjugation pattern
    "五段・カ行イ音便",  # Godan verb with 'ka' ending and 'i' sound change - Special 'ka' conjugation pattern
    "五段・ラ行アル"  # Godan verb 'aru' (to exist) with 'ra' ending - Special case verb
}

ichidan: set[str] = {
    "一段",  # Ichidan (one-step) verb - Regular -eru/-iru verb pattern
    "一段・得ル",  # Ichidan verb 'eru' (to get/obtain) - Special case ichidan verb
    "一段・クレル",  # Ichidan verb 'kureru' (to give) - Special case ichidan verb
}

adjective: set[str] = {
    "形容詞・イ段",  # I-adjective - Ends with 'i' and conjugates like 'takai' (high)
    "形容詞・アウオ段",  # Adjective with 'a', 'u', 'o' row - Special adjective conjugation pattern
    "形容詞・イイ",  # Adjective 'ii' (good) - Special case adjective
}

sahen: set[str] = {
    "サ変・スル",  # Suru verb - Irregular verb 'suru' (to do)
    "サ変・−スル",  # Suru compound verb - Noun + suru combination
    "サ変・−ズル",  # Zuru verb - Classical variation of suru
}

kahen: set[str] = {
    "カ変・来ル",  # Kuru verb - Irregular verb 'kuru' (to come) in kanji form
    "カ変・クル",  # Kuru verb - Irregular verb 'kuru' (to come) in kana form
}

bungo: set[str] = {
    "文語・ナリ",  # Classical 'nari' - Classical Japanese copula
    "文語・ル",  # Classical 'ru' ending - Classical verb ending
    "文語・キ",  # Classical 'ki' ending - Classical past tense marker
    "文語・ゴトシ",  # Classical 'gotoshi' - Classical expression meaning 'like/as if'
    "文語・ケリ",  # Classical 'keri' - Classical perfect aspect marker
    "文語・リ",  # Classical 'ri' - Classical verb ending
    "文語・ベシ",  # Classical 'beshi' - Classical expression of obligation/probability
}

special_class: set[str] = {
    "特殊・マス",  # Special 'masu' form - Polite verb ending
    "特殊・ヤ",  # Special 'ya' - Dialectal copula/question marker
    "特殊・ジャ",  # Special 'ja' - Dialectal copula
    "特殊・タ",  # Special 'ta' - Past tense marker
    "特殊・ナイ",  # Special 'nai' - Negative form
    "特殊・ヌ",  # Special 'nu' - Classical negative
    "特殊・ダ",  # Special 'da' - Copula (is/am/are)
    "特殊・タイ",  # Special 'tai' - Desire form (-want to do)
    "特殊・デス",  # Special 'desu' - Polite copula
}

yodan: set[str] = {
    "四段・ハ行",  # Classical yodan verb with 'ha' ending - Classical conjugation pattern
    "四段・バ行",  # Classical yodan verb with 'ba' ending - Classical conjugation pattern
}

ruhen: set[str] = {
    "ラ変",  # Classical ra-hen irregular verb - Classical irregular conjugation
}

who_knows: set[str] = {
    "下二・ダ行",  # Lower bigrade with 'da' ending - Classical conjugation pattern
    "下二・タ行",  # Lower bigrade with 'ta' ending - Classical conjugation pattern
}

indeclinable: set[str] = {
    "不変化型",  # Indeclinable type - Words that don't conjugate
}
