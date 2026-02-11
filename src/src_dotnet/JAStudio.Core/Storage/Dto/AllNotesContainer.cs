using System.Collections.Generic;

namespace JAStudio.Core.Storage.Dto;

/// <summary>Container for serializing/deserializing all notes in a single file.</summary>
internal class AllNotesContainer
{
   public List<KanjiNoteDto> Kanji { get; set; } = [];
   public List<VocabNoteDto> Vocab { get; set; } = [];
   public List<SentenceNoteDto> Sentences { get; set; } = [];
}
