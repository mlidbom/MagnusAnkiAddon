from __future__ import annotations

from typing import TYPE_CHECKING

from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]

from jastudio.note.notefields.tag_flag_field import TagFlagField
from jastudio.note.tags import Tags

if TYPE_CHECKING:
    from jastudio.note.vocabulary.vocabnote import VocabNote
    from jastudio.sysutils.weak_ref import WeakRef

# todo performance: memory: high-priority: combine into a single bitfield in memory
class VocabNoteRegister(Slots):
    def __init__(self, vocab: WeakRef[VocabNote]) -> None:
        self._vocab: WeakRef[VocabNote] = vocab

    @property
    def polite(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Register.polite)
    @property
    def formal(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Register.formal)
    @property
    def informal(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Register.informal)
    @property
    def archaic(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Register.archaic)
    @property
    def sensitive(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Register.sensitive)
    @property
    def vulgar(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Register.vulgar)
    @property
    def humble(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Register.humble)
    @property
    def literary(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Register.literary)
    @property
    def honorific(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Register.honorific)
    @property
    def rough_masculine(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Register.rough_masculine)
    @property
    def soft_feminine(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Register.soft_feminine)
    @property
    def slang(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Register.slang)
    @property
    def derogatory(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Register.derogatory)
    @property
    def childish(self) -> TagFlagField: return TagFlagField(self._vocab, Tags.Vocab.Register.childish)
