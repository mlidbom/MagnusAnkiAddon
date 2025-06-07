# noinspection PyUnusedClass, PyUnusedName
from __future__ import annotations

all_dict: dict[str, InflectionType] = {}

class InflectionType:
    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

    def __repr__(self) -> str: return f"""{self.name} - {self.description}"""

    def __eq__(self, other: object) -> bool:
        if isinstance(other, InflectionType):
            return self.name == other.name
        return False

def _add_form(name: str, description: str) -> InflectionType:
    form = InflectionType(name, description)
    all_dict[name] = form
    return form

# noinspection PyUnusedClass
class InflectionTypes:
    # noinspection PyUnusedClass,PyUnusedName
    class Godan:
        sa_ending: InflectionType = _add_form("五段・サ行", "Godan verb with 'sa' ending - Changes 'sa' stem in conjugation")
        ra_ending: InflectionType = _add_form("五段・ラ行", "Godan verb with 'ra' ending - Changes 'ra' stem in conjugation")
        ma_ending: InflectionType = _add_form("五段・マ行", "Godan verb with 'ma' ending - Changes 'ma' stem in conjugation")
        ba_ending: InflectionType = _add_form("五段・バ行", "Godan verb with 'ba' ending - Changes 'ba' stem in conjugation")
        wa_ending_gemination: InflectionType = _add_form("五段・ワ行促音便", "Godan verb with 'wa' ending and 'っ' consonant assimilation - Special 'wa' conjugation pattern")
        ka_ending_gemination_yuku: InflectionType = _add_form("五段・カ行促音便ユク", "Godan verb 'yuku' (to go) with 'ka' ending and consonant assimilation - Special case verb")
        wa_ending_u_sound: InflectionType = _add_form("五段・ワ行ウ音便", "Godan verb with 'wa' ending and 'u' sound change - Special 'wa' conjugation pattern")
        na_ending: InflectionType = _add_form("五段・ナ行", "Godan verb with 'na' ending - Changes 'na' stem in conjugation")
        ka_ending_gemination: InflectionType = _add_form("五段・カ行促音便", "Godan verb with 'ka' ending and consonant assimilation - Special 'ka' conjugation pattern")
        ta_ending: InflectionType = _add_form("五段・タ行", "Godan verb with 'ta' ending - Changes 'ta' stem in conjugation")
        ga_ending: InflectionType = _add_form("五段・ガ行", "Godan verb with 'ga' ending - Changes 'ga' stem in conjugation")
        ra_ending_special: InflectionType = _add_form("五段・ラ行特殊", "Special godan verb with 'ra' ending - Irregular 'ra' conjugation pattern")
        ka_ending_i_sound: InflectionType = _add_form("五段・カ行イ音便", "Godan verb with 'ka' ending and 'i' sound change - Special 'ka' conjugation pattern")
        ra_ending_aru: InflectionType = _add_form("五段・ラ行アル", "Godan verb 'aru' (to exist) with 'ra' ending - Special case verb")

    # noinspection PyUnusedClass,PyUnusedName
    class Ichidan:
        regular: InflectionType = _add_form("一段", "Ichidan (one-step) verb - Regular -eru/-iru verb pattern")
        eru: InflectionType = _add_form("一段・得ル", "Ichidan verb 'eru' (to get/obtain) - Special case ichidan verb")
        kureru: InflectionType = _add_form("一段・クレル", "Ichidan verb 'kureru' (to give) - Special case ichidan verb")

    # noinspection PyUnusedClass,PyUnusedName
    class Adjective:
        i_ending: InflectionType = _add_form("形容詞・イ段", "I-adjective - Ends with 'i' and conjugates like 'takai' (high)")
        auo_ending: InflectionType = _add_form("形容詞・アウオ段", "Adjective with 'a', 'u', 'o' row - Special adjective conjugation pattern")
        ii: InflectionType = _add_form("形容詞・イイ", "Adjective 'ii' (good) - Special case adjective")

    # noinspection PyUnusedClass,PyUnusedName
    class Sahen:
        suru: InflectionType = _add_form("サ変・スル", "Suru verb - Irregular verb 'suru' (to do)")
        suru_compound: InflectionType = _add_form("サ変・−スル", "Suru compound verb - Noun + suru combination")
        zuru: InflectionType = _add_form("サ変・−ズル", "Zuru verb - Classical variation of suru")

    # noinspection PyUnusedClass,PyUnusedName
    class Kahen:
        kuru_kanji: InflectionType = _add_form("カ変・来ル", "Kuru verb - Irregular verb 'kuru' (to come) in kanji form")
        kuru_kana: InflectionType = _add_form("カ変・クル", "Kuru verb - Irregular verb 'kuru' (to come) in kana form")

    # noinspection PyUnusedClass,PyUnusedName
    class Bungo:
        nari: InflectionType = _add_form("文語・ナリ", "Classical 'nari' - Classical Japanese copula")
        ru: InflectionType = _add_form("文語・ル", "Classical 'ru' ending - Classical verb ending")
        ki: InflectionType = _add_form("文語・キ", "Classical 'ki' ending - Classical past tense marker")
        gotoshi: InflectionType = _add_form("文語・ゴトシ", "Classical 'gotoshi' - Classical expression meaning 'like/as if'")
        keri: InflectionType = _add_form("文語・ケリ", "Classical 'keri' - Classical perfect aspect marker")
        ri: InflectionType = _add_form("文語・リ", "Classical 'ri' - Classical verb ending")
        beshi: InflectionType = _add_form("文語・ベシ", "Classical 'beshi' - Classical expression of obligation/probability")

    # noinspection PyUnusedClass,PyUnusedName
    class Special:
        masu: InflectionType = _add_form("特殊・マス", "Special 'masu' form - Polite verb ending")
        ya: InflectionType = _add_form("特殊・ヤ", "Special 'ya' - Dialectal copula/question marker")
        ja: InflectionType = _add_form("特殊・ジャ", "Special 'ja' - Dialectal copula")
        ta: InflectionType = _add_form("特殊・タ", "Special 'ta' - Past tense marker")
        nai: InflectionType = _add_form("特殊・ナイ", "Special 'nai' - Negative form")
        nu: InflectionType = _add_form("特殊・ヌ", "Special 'nu' - Classical negative")
        da: InflectionType = _add_form("特殊・ダ", "Special 'da' - Copula (is/am/are)")
        tai: InflectionType = _add_form("特殊・タイ", "Special 'tai' - Desire form (-want to do)")
        desu: InflectionType = _add_form("特殊・デス", "Special 'desu' - Polite copula")

    # noinspection PyUnusedClass,PyUnusedName
    class Yodan:
        ha_ending: InflectionType = _add_form("四段・ハ行", "Classical yodan verb with 'ha' ending - Classical conjugation pattern")
        ba_ending: InflectionType = _add_form("四段・バ行", "Classical yodan verb with 'ba' ending - Classical conjugation pattern")

    # noinspection PyUnusedClass,PyUnusedName
    class Ruhen:
        ra_hen: InflectionType = _add_form("ラ変", "Classical ra-hen irregular verb - Classical irregular conjugation")

    # noinspection PyUnusedClass,PyUnusedName
    class Nidan:
        lower_da: InflectionType = _add_form("下二・ダ行", "Lower bigrade with 'da' ending - Classical conjugation pattern")
        lower_ta: InflectionType = _add_form("下二・タ行", "Lower bigrade with 'ta' ending - Classical conjugation pattern")

    # noinspection PyUnusedClass,PyUnusedName
    class Other:
        indeclinable: InflectionType = _add_form("不変化型", "Indeclinable type - Words that don't conjugate")
