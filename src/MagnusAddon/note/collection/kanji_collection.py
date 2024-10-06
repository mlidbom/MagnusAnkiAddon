from __future__ import annotations

from typing import List, Optional, Union, TYPE_CHECKING

from note.radicalnote import RadicalNote

if TYPE_CHECKING:
    from note.collection.jp_collection import JPCollection

from anki.collection import Collection
from anki.notes import Note, NoteId
from note.collection.backend_facade import BackEndFacade
from note.collection.kanji_dependency import KanjiDependency
from note.collection.note_cache import CachedNote, NoteCache
from note.kanjinote import KanjiNote
from note.note_constants import NoteTypes
from sysutils import ex_list, ex_sequence

class _KanjiSnapshot(CachedNote):
    def __init__(self, note: KanjiNote):
        super().__init__(note)

class _KanjiCache(NoteCache[KanjiNote, _KanjiSnapshot]):
    def __init__(self, all_kanji: list[KanjiNote]):
        super().__init__(all_kanji, KanjiNote)

    def _create_snapshot(self, note: KanjiNote) -> _KanjiSnapshot: return _KanjiSnapshot(note)

class KanjiCollection:
    def __init__(self, collection: Collection, jp_collection: JPCollection):
        def kanji_constructor(note: Note) -> KanjiNote: return KanjiNote(note)
        self.jp_collection = jp_collection
        self.collection = BackEndFacade[KanjiNote](collection, kanji_constructor, NoteTypes.Kanji)
        self._cache = _KanjiCache(list(self.collection.all()))

    def search(self, query: str) -> list[KanjiNote]:
        return list(self.collection.search(query))

    def all(self) -> list[KanjiNote]: return self._cache.all()

    def with_id(self, note_id:NoteId) -> KanjiNote:
        return self._cache.with_id(note_id)

    def all_wani(self) -> list[KanjiNote]:
        return [kanji for kanji in self.all() if kanji.is_wani_note()]

    def with_any_kanji_in(self, kanji_list: list[str]) -> List[KanjiNote]:
        return ex_sequence.flatten([self._cache.with_question(kanji) for kanji in kanji_list])

    def with_kanji(self, kanji: str) -> Optional[KanjiNote]:
        found = self._cache.with_question(kanji)
        return found[0] if found else None

    def with_question(self, kanji: str) -> KanjiNote:
        return ex_list.single(self._cache.with_question(kanji))

    def display_dependencies_of(self, kanji_note: KanjiNote) -> list[KanjiDependency]:
        return [KanjiDependency.from_radical(rad) if isinstance(rad, RadicalNote)
                else KanjiDependency.from_kanji(rad)
                for rad in self.dependencies_of(kanji_note)]

    def dependencies_of(self, kanji_note: KanjiNote) -> list[Union[RadicalNote, KanjiNote]]:
        dependency_notes: list[Union[RadicalNote, KanjiNote]] = list()

        dependency_characters = kanji_note.get_radicals()
        for character in dependency_characters:
            radical_dependency = self.jp_collection.radicals.with_any_question_in([character])
            if radical_dependency:
                if not radical_dependency[0].is_replaced_by_kanji():
                    dependency_notes.append(radical_dependency[0])
                    continue

            kanji_dependency = [k for k in self.jp_collection.kanji.with_any_kanji_in([character]) if k.get_id() != kanji_note.get_id()]
            if kanji_dependency:
                dependency_notes.append(kanji_dependency[0])

        dependency_radicals_by_name_with_no_question_character = [rad for rad in self.jp_collection.radicals.with_any_answer_in(kanji_note.get_radical_dependencies_names()) if not rad.get_question()]
        dependency_notes += dependency_radicals_by_name_with_no_question_character
        ex_sequence.remove_duplicates_while_retaining_order(dependency_notes)

        return dependency_notes
