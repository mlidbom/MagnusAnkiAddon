from __future__ import annotations

from typing import TYPE_CHECKING
from sysutils import kana_utils
from sysutils.ex_str import newline

if TYPE_CHECKING:
    from note.kanjinote import KanjiNote

def create_default_mnemonic(kanji_note:KanjiNote) -> str:
    from ankiutils import app
    readings_mappings = app.config().readings_mappings_dict

    def create_readings_tag(kana_reading: str) -> str:
        romaji_reading = kana_utils.romanize(kana_reading)

        if romaji_reading in readings_mappings:
            read = readings_mappings[romaji_reading]
            return read if read.count("<read>") <= 1 else f"""<compound-reading>{read}</compound-reading>"""

        def try_combine_framentary_matches_into_one_reading() -> str:
            matches_by_sub_string_start_index: list[list[str]] = list()
            for sub_string_start_index in range(0, len(romaji_reading)):
                candidates = [romaji_reading[sub_string_start_index:sub_string_length] for sub_string_length in range(sub_string_start_index + 1, len(romaji_reading) + 1)]
                matches_by_sub_string_start_index.append([cand for cand in candidates if cand in readings_mappings])

            def remove_dead_end_paths() -> None:
                matches_removed = True
                while matches_removed:
                    matches_removed = False
                    for path_index in range(0, len(romaji_reading)):
                        for match in matches_by_sub_string_start_index[path_index]:
                            if not path_index + len(match) == len(romaji_reading): #this match brings us to the end of the reading
                                if not matches_by_sub_string_start_index[path_index + len(match)]: #There's nowhere to go after the end of this fragment
                                    matches_removed = True
                                    matches_by_sub_string_start_index[path_index].remove(match)

            def find_long_path() -> list[str]:
                next_fragment_index = 0
                path: list[str] = []
                while next_fragment_index < len(romaji_reading):
                    candidates_ = matches_by_sub_string_start_index[next_fragment_index]
                    if not candidates_:
                        return []

                    fragment = sorted(candidates_, key=lambda x: len(x), reverse=True)[0]
                    path.append(fragment)
                    next_fragment_index += len(fragment)
                return path

            remove_dead_end_paths()
            long_path = find_long_path()

            if not long_path: return ""
            combined_reading = "-".join([readings_mappings[fragment] for fragment in long_path])
            return f"""<compound-reading>{combined_reading}</compound-reading>"""


        combined = try_combine_framentary_matches_into_one_reading()
        if combined: return combined

        return f"<read>{romaji_reading.capitalize()}</read>"

    radical_names = [rad.get_primary_radical_meaning() for rad in kanji_note.get_radicals_notes()]
    mnemonic = f"""
{" ".join([f"<rad>{name}</rad>" for name in radical_names])} 
<kan>{kanji_note.get_primary_meaning()}</kan> 
{" ".join([create_readings_tag(reading) for reading in kanji_note.get_primary_readings()])}
""".replace(newline, "")
    return mnemonic.strip()
