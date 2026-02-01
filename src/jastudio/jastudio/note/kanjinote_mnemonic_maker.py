from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils import kana_utils
from sysutils.ex_str import newline

from jastudio.ankiutils import app

if TYPE_CHECKING:
    from jastudio.note.kanjinote import KanjiNote

def create_default_mnemonic(kanji_note:KanjiNote) -> str:
    readings_mappings = app.config().readings_mappings_dict

    def create_readings_tag(kana_reading: str) -> str:
        reading = kana_utils.romanize(kana_reading)
        reading_length = len(reading)

        if reading in readings_mappings:
            read = readings_mappings[reading]
            return read if read.count("<read>") <= 1 else f"""<compound-reading>{read}</compound-reading>"""

        def try_combine_framentary_matches_into_one_reading() -> str:
            segments_with_mapped_readings_by_start_index: list[list[str]] = []
            for current_postion in range(reading_length):
                all_substrings_permutations_starting_at_current_position = [reading[current_postion:sub_string_length] for sub_string_length in range(current_postion + 1, reading_length + 1)]
                segments_with_mapped_readings_by_start_index.append([candidate for candidate in all_substrings_permutations_starting_at_current_position if candidate in readings_mappings])

            def remove_dead_end_paths() -> None:
                def reached_end_of_reading() -> bool: return path_index + len(match) == reading_length
                def is_dead_end_path() -> bool: return not segments_with_mapped_readings_by_start_index[path_index + len(match)]
                matches_removed = True
                while matches_removed:
                    matches_removed = False
                    for path_index in range(reading_length):
                        for match in segments_with_mapped_readings_by_start_index[path_index]:
                            if not reached_end_of_reading() and is_dead_end_path():
                                matches_removed = True
                                segments_with_mapped_readings_by_start_index[path_index].remove(match)

            def find_shortest_path_prefer_long_starting_segments() -> list[str]:
                shortest_paths_to_position: dict[int, list[str]] = {0: []}  # Start with an empty path at position 0

                def current_index_is_reachable() -> bool: return current_position in shortest_paths_to_position

                def current_segment_is_shortest_path_to_position_after_segment() -> bool:
                    return (position_after_segment not in shortest_paths_to_position or
                            len(shortest_paths_to_position[current_position]) < len(shortest_paths_to_position[position_after_segment]))

                def sort_candidates_longest_first_so_that_the_longest_starting_candidate_will_be_preferred() -> None:
                    for start_position in range(reading_length):
                        segments_with_mapped_readings_by_start_index[start_position].sort(key=lambda candidate: -len(candidate))

                sort_candidates_longest_first_so_that_the_longest_starting_candidate_will_be_preferred()

                current_position:int = 0
                for current_position in range(reading_length):
                    if not current_index_is_reachable(): continue

                    for current_segment in segments_with_mapped_readings_by_start_index[current_position]:
                        position_after_segment:int = current_position + len(current_segment)
                        if current_segment_is_shortest_path_to_position_after_segment():
                            shortest_paths_to_position[position_after_segment] = shortest_paths_to_position[current_position] + [current_segment]

                return shortest_paths_to_position.get(reading_length, [])

            remove_dead_end_paths()
            shortest_path = find_shortest_path_prefer_long_starting_segments()

            if not shortest_path: return ""
            combined_reading = "-".join([readings_mappings[fragment] for fragment in shortest_path])
            return f"""<compound-reading>{combined_reading}</compound-reading>"""


        combined = try_combine_framentary_matches_into_one_reading()
        if combined: return combined

        return f"<read>{reading.capitalize()}</read>"

    radical_names = [rad.get_primary_radical_meaning() for rad in kanji_note.get_radicals_notes()]
    mnemonic = f"""
{" ".join([f"<rad>{name}</rad>" for name in radical_names])}
 <kan>{kanji_note.get_primary_meaning()}</kan>
 {" ".join([create_readings_tag(reading) for reading in kanji_note.get_primary_readings()])}
 ...
""".replace(newline, "")
    return mnemonic.strip()