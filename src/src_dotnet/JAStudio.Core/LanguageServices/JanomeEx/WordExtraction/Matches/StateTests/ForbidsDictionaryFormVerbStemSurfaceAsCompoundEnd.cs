using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests;

public static class ForbidsDictionaryVerbFormStemAsCompoundEnd
{
    private static readonly FailedMatchRequirement Failed = FailedMatchRequirement.Forbids("dictionary_form_verb_stem_as_compound_end");

    public static FailedMatchRequirement? ApplyTo(MatchInspector inspector)
    {
        if (inspector.Variant.IsSurface && 
            inspector.Word.BaseVariant != null && 
            inspector.Word.EndLocation.Token.IsDictionaryVerbFormStem)
        {
            return Failed;
        }
        return null;
    }
}
