using System.Collections.Generic;
using JAStudio.Core.Note.CorpusData;
using MemoryPack;

namespace JAStudio.Core.Storage.Dto;

/// <summary>Container for serializing/deserializing all notes as a single unit (JSON or binary snapshot).</summary>
[MemoryPackable] partial class AllNotesContainer
{
   public List<KanjiData> Kanji { get; set; } = [];
   public List<VocabData> Vocab { get; set; } = [];
   public List<SentenceData> Sentences { get; set; } = [];
}
