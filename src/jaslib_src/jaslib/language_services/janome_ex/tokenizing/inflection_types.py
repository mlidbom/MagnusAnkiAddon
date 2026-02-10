# # noinspection PyUnusedClass, PyUnusedName
# from __future__ import annotations
#
# from typing import override
#
# from autoslot import Slots
#
# all_dict: dict[str, InflectionType] = {}
#
# class InflectionType(Slots):
#     def __init__(self, name: str, description: str, base: str) -> None:
#         self.base: str = base
#         self.name: str = name
#         self.description: str = description
#
#     @override
#     def __repr__(self) -> str: return f"""{self.name} - {self.description}"""
#     @override
#     def __str__(self) -> str: return self.__repr__()
#
#     @override
#     def __eq__(self, other: object) -> bool:
#         if isinstance(other, InflectionType):
#             return self.name == other.name
#         return False
#
# def _add_form(name: str, description: str) -> InflectionType:
#     parts = name.split("・")
#     base = parts[0]
#     form = InflectionType(name, description, base)
#     all_dict[name] = form
#     return form
#
# # noinspection PyUnusedClass,PyUnusedName
# class InflectionTypes(Slots):
#     unknown: InflectionType = _add_form("*", "Unknown")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Godan(Slots):
#         base: str = "五段"
#         su: InflectionType = _add_form("五段・サ行", "Godan verb with 'su' ending")
#         mu: InflectionType = _add_form("五段・マ行", "Godan verb with 'mu' ending")
#         bu: InflectionType = _add_form("五段・バ行", "Godan verb with 'bu' ending")
#         gu_ending: InflectionType = _add_form("五段・ガ行", "Godan verb with 'gu' ending")
#         tsu: InflectionType = _add_form("五段・タ行", "Godan verb with 'tsu' ending")
#         nu: InflectionType = _add_form("五段・ナ行", "Godan verb with 'nu' ending")
#         ru: InflectionType = _add_form("五段・ラ行", "Godan verb with 'ru' ending")
#         ru_special: InflectionType = _add_form("五段・ラ行特殊", "Godan verb with 'ru' ending - Irregular conjugation")
#         ru_ending_aru: InflectionType = _add_form("五段・ラ行アル", "Godan verb 'aru'")
#
#         u_gemination: InflectionType = _add_form("五段・ワ行促音便", "Godan verb with 'u' ending and 'っ' consonant assimilation")
#         u_u_sound: InflectionType = _add_form("五段・ワ行ウ音便", "Godan verb with 'u' ending and 'u' sound change")
#
#         ku_gemination_yuku: InflectionType = _add_form("五段・カ行促音便ユク", "Godan verb 'yuku'")
#         ku_gemination: InflectionType = _add_form("五段・カ行促音便", "Godan verb with 'ku' ending and consonant assimilation")
#         ku_i_sound: InflectionType = _add_form("五段・カ行イ音便", "Godan verb with 'ku' ending and 'i' sound change")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Ichidan(Slots):
#         base: str = "一段"
#         regular: InflectionType = _add_form("一段", "Ichidan verb")
#         eru: InflectionType = _add_form("一段・得ル", "Ichidan verb 'eru'")
#         kureru: InflectionType = _add_form("一段・クレル", "Ichidan verb 'kureru'")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Adjective(Slots):
#         base: str = "形容詞"
#         i_ending: InflectionType = _add_form("形容詞・イ段", "I-adjective")
#         auo_ending: InflectionType = _add_form("形容詞・アウオ段", "Adjective with 'a', 'u', 'o' row")
#         ii: InflectionType = _add_form("形容詞・イイ", "Adjective 'いい'")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Sahen(Slots):
#         base: str = "サ変"
#         suru: InflectionType = _add_form("サ変・スル", "Suru verb")
#         suru_compound: InflectionType = _add_form("サ変・−スル", "Suru compound verb")
#         zuru: InflectionType = _add_form("サ変・−ズル", "Zuru verb - Classical variation of suru")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Kahen(Slots):
#         base: str = "カ変"
#         kuru_kanji: InflectionType = _add_form("カ変・来ル", "Kuru verb in kanji")
#         kuru_kana: InflectionType = _add_form("カ変・クル", "Kuru verb in kana")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Bungo(Slots):
#         base: str = "文語"
#         nari: InflectionType = _add_form("文語・ナリ", "Classical 'nari' - Classical Japanese copula")
#         ru: InflectionType = _add_form("文語・ル", "Classical 'ru' ending - Classical verb ending")
#         ki: InflectionType = _add_form("文語・キ", "Classical 'ki' ending - Classical past tense marker")
#         gotoshi: InflectionType = _add_form("文語・ゴトシ", "Classical 'gotoshi' - Classical expression meaning 'like/as if'")
#         keri: InflectionType = _add_form("文語・ケリ", "Classical 'keri' - Classical perfect aspect marker")
#         ri: InflectionType = _add_form("文語・リ", "Classical 'ri' - Classical verb ending")
#         beshi: InflectionType = _add_form("文語・ベシ", "Classical 'beshi' - Classical expression of obligation/probability")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Special(Slots):
#         base: str = "特殊"
#         masu: InflectionType = _add_form("特殊・マス", "Special 'masu'")
#         ya: InflectionType = _add_form("特殊・ヤ", "Special 'ya' - Dialectal copula/question marker")
#         ja: InflectionType = _add_form("特殊・ジャ", "Special 'ja' - Dialectal copula")
#         ta: InflectionType = _add_form("特殊・タ", "Special 'ta' - Past tense marker")
#         nai: InflectionType = _add_form("特殊・ナイ", "Special 'nai' - Negative form")
#         nu: InflectionType = _add_form("特殊・ヌ", "Special 'nu' - Classical negative")
#         da: InflectionType = _add_form("特殊・ダ", "Special 'da' - Copula (is/am/are)")
#         tai: InflectionType = _add_form("特殊・タイ", "Special 'tai' - Desire form (-want to do)")
#         desu: InflectionType = _add_form("特殊・デス", "Special 'desu' - Polite copula")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Yodan(Slots):
#         base: str = "四段"
#         ha_ending: InflectionType = _add_form("四段・ハ行", "Classical yodan verb with 'ha' ending")
#         ba_ending: InflectionType = _add_form("四段・バ行", "Classical yodan verb with 'ba' ending")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Ruhen(Slots):
#         base: str = "ラ変"
#         ra_hen: InflectionType = _add_form("ラ変", "Classical ra-hen irregular verb")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Nidan(Slots):
#         base: str = "下二"
#         lower_da: InflectionType = _add_form("下二・ダ行", "Lower bigrade with 'da' ending")
#         lower_ta: InflectionType = _add_form("下二・タ行", "Lower bigrade with 'ta' ending")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Other(Slots):
#         indeclinable: InflectionType = _add_form("不変化型", "Indeclinable type - Words that don't conjugate")
