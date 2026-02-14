using System.Collections.Generic;
using MemoryPack;

namespace JAStudio.Core.Storage.Dto;

/// <summary>Container for serializing/deserializing all notes as a single unit (JSON or binary snapshot).</summary>
[MemoryPackable]
internal partial class AllNotesContainer
{
   public List<KanjiNoteDto> Kanji { get; set; } = [];
   public List<VocabNoteDto> Vocab { get; set; } = [];
   public List<SentenceNoteDto> Sentences { get; set; } = [];
}
