using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;

namespace JAStudio.Core.UI.Web.Sentence;

public class TextAnalysisViewModel
{
    public TextAnalysis Analysis { get; }
    public List<CandidateWordVariantViewModel> CandidateWords { get; }
    public List<MatchViewModel> DisplayedMatches { get; }

    public TextAnalysisViewModel(TextAnalysis textAnalysis)
    {
        Analysis = textAnalysis;
        CandidateWords = textAnalysis.IndexingWordVariants
            .Select(v => new CandidateWordVariantViewModel(v))
            .ToList();
        
        var matches = CandidateWords.SelectMany(variantVm => variantVm.Matches).ToList();
        DisplayedMatches = matches.Where(match => match.IsDisplayed).ToList();
    }
}
