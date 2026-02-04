using System.Collections.Generic;
using JAStudio.Core.Note;

namespace JAStudio.Core.UI.Web.Sentence;

public class SentenceViewModel
{
    public SentenceNote Sentence { get; }
    public TextAnalysisViewModel Analysis { get; }
    public List<MatchViewModel> DisplayedMatches { get; }

    public SentenceViewModel(SentenceNote sentence)
    {
        Sentence = sentence;
        Analysis = new TextAnalysisViewModel(sentence.CreateAnalysis(forUI: true));
        DisplayedMatches = Analysis.DisplayedMatches;
    }
}
