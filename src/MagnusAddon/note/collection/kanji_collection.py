from __future__ import annotations

from typing import List, TYPE_CHECKING

from note.radicalnote import RadicalNote

if TYPE_CHECKING:
    from note.collection.jp_collection import JPCollection

from anki.collection import Collection
from anki.notes import Note
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

    def all_wani(self) -> list[KanjiNote]:
        return [kanji for kanji in self.all() if kanji.is_wani_note()]

    def with_any_kanji_in(self, kanji_list: list[str]) -> List[KanjiNote]:
        return ex_sequence.flatten([self._cache.with_question(kanji) for kanji in kanji_list])

    def dependencies_of(self, kanji_note: KanjiNote) -> list[KanjiDependency]:
        radical_dependencies_notes = self.jp_collection.radicals.with_any_question_in(kanji_note.get_radicals())
        radical_dependencies_notes += self.jp_collection.radicals.with_any_answer_in(kanji_note.get_radical_dependencies_names())
        radical_dependencies_notes = ex_sequence.remove_duplicates_while_retaining_order(radical_dependencies_notes)

        radicals_exchanged_for_kanji = ex_list.remove_items_where(RadicalNote.predicates().is_replaced_by_kanji, radical_dependencies_notes)
        kanji_dependencies_notes = self.jp_collection.kanji.with_any_kanji_in([radical.get_question() for radical in radicals_exchanged_for_kanji])

        radical_dependencies = [KanjiDependency.from_radical(rad) for rad in radical_dependencies_notes]
        kanji_dependencies = [KanjiDependency.from_kanji(rad) for rad in kanji_dependencies_notes]

        return radical_dependencies + kanji_dependencies
