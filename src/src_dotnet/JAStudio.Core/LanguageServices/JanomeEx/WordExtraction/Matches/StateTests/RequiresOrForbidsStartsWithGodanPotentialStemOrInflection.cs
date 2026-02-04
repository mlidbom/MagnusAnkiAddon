using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests;

public static class RequiresOrForbidsStartsWithGodanPotentialStemOrInflection
{
    private static readonly FailedMatchRequirement RequiredFailure = FailedMatchRequirement.Required("godan_potential");
    private static readonly FailedMatchRequirement ForbiddenFailure = FailedMatchRequirement.Forbids("godan_potential");

    public static FailedMatchRequirement? ApplyTo(VocabMatchInspector inspector)
    {
        var requirement = inspector.Match.RequiresForbids.GodanPotential;
        if (requirement.IsActive)
        {
            var isInState = InternalIsInState(inspector);
            if (requirement.IsRequired && !isInState)
            {
                return RequiredFailure;
            }
            if (requirement.IsForbidden && isInState)
            {
                return ForbiddenFailure;
            }
        }
        return null;
    }

    private static bool InternalIsInState(VocabMatchInspector inspector)
    {
        if (inspector.Word.StartLocation.Token.IsGodanPotentialInflection || 
            inspector.Word.StartLocation.Token.IsGodanPotentialStem)
        {
            return true;
        }
        return false;
    }
}
