using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests;

public static class ForbidsDictionaryInflectionSurfaceWithBase
{
    private static readonly FailedMatchRequirement Failed = FailedMatchRequirement.Forbids("dictionary_form_verb_inflection");

    public static FailedMatchRequirement? ApplyTo(MatchInspector inspector)
    {
        if (inspector.Variant.IsSurface && 
            !inspector.Word.IsCompound && 
            inspector.Word.BaseVariant != null && 
            inspector.Word.EndLocation.Token.IsDictionaryVerbInflection)
        {
            return Failed;
        }
        return null;
    }
}
