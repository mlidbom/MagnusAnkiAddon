# # noinspection PyUnusedClass, PyUnusedName
# from __future__ import annotations
#
# from typing import override
#
# from autoslot import Slots
# from typed_linq_collections.collections.q_set import QSet  # pyright: ignore[reportMissingTypeStubs]
#
# all_dict: dict[str, InflectionForm] = {}
#
# class InflectionForm(Slots):
#     def __init__(self, name: str, description: str) -> None:
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
#         if isinstance(other, InflectionForm):
#             return self.name == other.name
#         return False
#
#     @override
#     def __hash__(self) -> int: return hash(self.name)
#
# def _add_form(name: str, description: str) -> InflectionForm:
#     form = InflectionForm(name, description)
#     all_dict[name] = form
#     return form
#
# # noinspection PyUnusedClass,PyUnusedName
# class InflectionForms(Slots):
#     unknowm: InflectionForm = _add_form("*", "Unknown")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Basic(Slots):
#         dictionary_form: InflectionForm = _add_form("基本形", "Dictionary form")
#         gemination: InflectionForm = _add_form("基本形-促音便", "Dictionary form with consonant doubling")
#         euphonic: InflectionForm = _add_form("音便基本形", "Dictionary form with sound changes")
#         classical: InflectionForm = _add_form("文語基本形", "Dictionary form in classical Japanese")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Continuative(Slots):
#         renyoukei_masu_stem: InflectionForm = _add_form("連用形", "Continuative/masu-stem verbs/adjective")
#         te_connection: InflectionForm = _add_form("連用テ接続", "Continuative te-connection")
#         ta_connection: InflectionForm = _add_form("連用タ接続", "Continuative ta-connection")
#         de_connection: InflectionForm = _add_form("連用デ接続", "Continuative de-connection")
#         ni_connection: InflectionForm = _add_form("連用ニ接続", "Continuative ni-connection")
#         gozai_connection: InflectionForm = _add_form("連用ゴザイ接続", "Continuative gozai connection")
#
#         te_connection_forms: set[InflectionForm] = {te_connection, de_connection}
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Misc(Slots):
#         garu_connection: InflectionForm = _add_form("ガル接続", "Garu connection")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Irrealis(Slots):
#         general_irrealis_mizenkei: InflectionForm = _add_form("未然形", "Irrealis/a-stem : negatives/auxiliaries")
#         special_irrealis: InflectionForm = _add_form("未然特殊", "Irrealis - Special")
#         u_connection: InflectionForm = _add_form("未然ウ接続", 'Irrealis u-connection - volitional "u"')
#         nu_connection: InflectionForm = _add_form("未然ヌ接続", 'Irrealis nu-connection - negative "nu"')
#         reru_connection: InflectionForm = _add_form("未然レル接続", 'Irrealis reru-connection - passive/potential "reru"')
#         all_forms: set[InflectionForm] = {general_irrealis_mizenkei, special_irrealis, u_connection, nu_connection, reru_connection}
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class Hypothetical(Slots):
#         general_hypothetical_kateikei: InflectionForm = _add_form("仮定形", "Hypothetical/potential/e-stem verbs+adjectives.")
#         contraction1: InflectionForm = _add_form("仮定縮約１", "Hypothetical contraction version 1")
#         contraction2: InflectionForm = _add_form("仮定縮約２", "Hypothetical contraction version 2")
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class ImperativeMeireikei(Slots):
#         e: InflectionForm = _add_form("命令ｅ", "Imperative/command/meireikei -  e")
#         ro: InflectionForm = _add_form("命令ｒｏ", "Imperative/command/meireikei - ro")
#         yo: InflectionForm = _add_form("命令ｙｏ", "Imperative/command/meireikei - yo")
#         i: InflectionForm = _add_form("命令ｉ", "Imperative/command/meireikei - i")
#         godan_forms: QSet[InflectionForm] = QSet([e, i])
#         ichidan_forms: QSet[InflectionForm] = QSet([ro, yo])
#
#     # noinspection PyUnusedClass,PyUnusedName
#     class NounConnection(Slots):
#         general_noun_connection: InflectionForm = _add_form("体言接続", "Noun connection")
#         special_1: InflectionForm = _add_form("体言接続特殊", "Special noun connection")
#         special_2: InflectionForm = _add_form("体言接続特殊２", "Special noun connection 2")
