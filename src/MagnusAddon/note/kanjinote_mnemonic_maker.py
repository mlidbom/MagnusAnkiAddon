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
        reading = kana_utils.romanize(kana_reading)
        reading_length = len(reading)

        if reading in readings_mappings:
            read = readings_mappings[reading]
            return read if read.count("<read>") <= 1 else f"""<compound-reading>{read}</compound-reading>"""

        def try_combine_framentary_matches_into_one_reading() -> str:
            segments_by_start_index: list[list[str]] = list()
            for segment_start_index in range(reading_length):
                candidates = [reading[segment_start_index:sub_string_length] for sub_string_length in range(segment_start_index + 1, reading_length + 1)]
                segments_by_start_index.append([cand for cand in candidates if cand in readings_mappings])

            def remove_dead_end_paths() -> None:
                matches_removed = True
                while matches_removed:
                    matches_removed = False
                    for path_index in range(reading_length):
                        for match in segments_by_start_index[path_index]:
                            if not path_index + len(match) == reading_length: #this match brings us to the end of the reading
                                if not segments_by_start_index[path_index + len(match)]: #There's nowhere to go after the end of this fragment
                                    matches_removed = True
                                    segments_by_start_index[path_index].remove(match)

            def find_path_with_fewest_segments() -> list[str]:
                shortest_paths_to_position: dict[int, list[str]] = {0: []}  # Start with an empty path at position 0

                def current_index_is_reachable() -> bool: return index in shortest_paths_to_position

                def segment_is_shortest_path_to_position_after_segment() -> bool:
                    return (position_after_segment not in shortest_paths_to_position or
                            len(shortest_paths_to_position[index]) + 1 < len(shortest_paths_to_position[position_after_segment]))

                index:int = 0
                for index in range(reading_length):
                    if not current_index_is_reachable(): continue

                    segments_starting_at_current_index = segments_by_start_index[index]
                    for segment in segments_starting_at_current_index:
                        position_after_segment:int = index + len(segment)
                        if segment_is_shortest_path_to_position_after_segment():
                            shortest_paths_to_position[position_after_segment] = shortest_paths_to_position[index] + [segment]

                return shortest_paths_to_position.get(reading_length, []) # Return the shortest path to the end of the string, or empty list if no path exists

            remove_dead_end_paths()
            long_path = find_path_with_fewest_segments()

            if not long_path: return ""
            combined_reading = "-".join([readings_mappings[fragment] for fragment in long_path])
            return f"""<compound-reading>{combined_reading}</compound-reading>"""


        combined = try_combine_framentary_matches_into_one_reading()
        if combined: return combined

        return f"<read>{reading.capitalize()}</read>"

    radical_names = [rad.get_primary_radical_meaning() for rad in kanji_note.get_radicals_notes()]
    mnemonic = f"""
{" ".join([f"<rad>{name}</rad>" for name in radical_names])} 
<kan>{kanji_note.get_primary_meaning()}</kan> 
{" ".join([create_readings_tag(reading) for reading in kanji_note.get_primary_readings()])}
""".replace(newline, "")
    return mnemonic.strip()