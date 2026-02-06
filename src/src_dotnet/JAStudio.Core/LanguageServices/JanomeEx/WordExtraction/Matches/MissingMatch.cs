using System.Collections.Generic;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches;

public sealed class MissingMatch : Match
{
    public MissingMatch(CandidateWordVariant wordVariant) : base(wordVariant)
    {
    }

    public override string Answer => "---";
    public override string MatchForm => "[MISSING]"; // Change this so the tests can distinguish that this is a missing match
    public override bool IsValid => false;
    public override List<string> Readings => [];
    public override List<string> FailureReasons =>
       [..base.FailureReasons, "no_dictionary_or_vocabulary_match_found"];
}
