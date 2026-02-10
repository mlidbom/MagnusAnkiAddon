using JAStudio.Core.Configuration;
using JAStudio.Core.LanguageServices.JamdictEx;
using JAStudio.Core.Note.Collection;

namespace JAStudio.Core.LanguageServices.JanomeEx;

/// <summary>
/// Bundles the services needed by the text analysis pipeline (tokenizing, word extraction, match evaluation).
/// Threaded through TextAnalysis → TextLocation → CandidateWord → CandidateWordVariant → Match state tests.
/// </summary>
public class AnalysisServices
{
   public VocabCollection Vocab { get; }
   public DictLookup DictLookup { get; }
   public Settings Settings { get; }

   public AnalysisServices(VocabCollection vocab, DictLookup dictLookup, Settings settings)
   {
      Vocab = vocab;
      DictLookup = dictLookup;
      Settings = settings;
   }
}
