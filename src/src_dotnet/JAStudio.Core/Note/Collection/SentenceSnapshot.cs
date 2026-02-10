using System.Linq;

namespace JAStudio.Core.Note.Collection;

public class SentenceSnapshot : CachedNote
{
   public string[] Words { get; }
   public NoteId[] DetectedVocab { get; }
   public string[] UserHighlightedVocab { get; }
   public string[] MarkedIncorrectVocab { get; }

   public SentenceSnapshot(SentenceNote note) : base(note)
   {
      Words = note.GetWords().ToArray();
      DetectedVocab = note.ParsingResult.Get().MatchedVocabIds.ToArray();
      UserHighlightedVocab = note.Configuration.HighlightedWords.ToArray();
      MarkedIncorrectVocab = note.Configuration.IncorrectMatches.Words().ToArray();
   }
}
