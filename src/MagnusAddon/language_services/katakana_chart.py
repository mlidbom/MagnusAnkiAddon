from __future__ import annotations

from autoslot import Slots  # type: ignore[reportMissingTypeStubs]


# noinspection PyUnusedName,PyUnusedClass
class KatakanaChart(Slots):
    k_index: int = 1
    s_index: int = 2
    t_index: int = 3
    n_index: int = 4
    h_index: int = 5
    m_index: int = 6
    y_index: int = 7
    r_index: int = 8
    w_index: int = 9

    a_row_1: list[str] = ["ア", "カ", "サ", "タ", "ナ", "ハ", "マ", "ヤ", "ラ", "ワ"]
    a_row_2: list[str] = ["　", "ガ", "ザ", "ダ", "　", "バ", "　", "　", "　", "　"]
    a_row_3: list[str] = ["　", "　", "　", "　", "　", "パ", "　", "　", "　", "　"]

    i_row_1: list[str] = ["イ", "キ", "シ", "チ", "ニ", "ヒ", "ミ", "　", "リ", "　"]
    i_row_2: list[str] = ["　", "ギ", "ジ", "ヂ", "　", "ビ", "　", "　", "　", "　"]
    i_row_3: list[str] = ["　", "　", "　", "　", "　", "ピ", "　", "　", "　", "　"]

    u_row_1: list[str] = ["ウ", "ク", "ス", "ツ", "ヌ", "フ", "ム", "ユ", "ル", "　"]
    u_row_2: list[str] = ["　", "グ", "ズ", "ヅ", "　", "ブ", "　", "　", "　", "　"]
    u_row_3: list[str] = ["　", "　", "　", "　", "　", "プ", "　", "　", "　", "　"]

    e_row_1: list[str] = ["エ", "ケ", "セ", "テ", "ネ", "ヘ", "メ", "　", "レ", "　"]
    e_row_2: list[str] = ["　", "ゲ", "ゼ", "デ", "　", "ベ", "　", "　", "　", "　"]
    e_row_3: list[str] = ["　", "　", "　", "　", "　", "ペ", "　", "　", "　", "　"]

    o_row_1: list[str] = ["オ", "コ", "ソ", "ト", "ノ", "ホ", "モ", "ヨ", "ロ", "ヲ"]
    o_row_2: list[str] = ["　", "ゴ", "ゾ", "ド", "　", "ボ", "　", "　", "　", "　"]
    o_row_3: list[str] = ["　", "　", "　", "　", "　", "ポ", "　", "　", "　", "　"]
