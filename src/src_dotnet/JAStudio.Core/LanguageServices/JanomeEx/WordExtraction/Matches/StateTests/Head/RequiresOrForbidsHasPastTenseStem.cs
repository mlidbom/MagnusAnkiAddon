using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

public static class RequiresOrForbidsHasPastTenseStem
{
    private static readonly FailedMatchRequirement RequiredFailure = FailedMatchRequirement.Required("past_tense_stem");
    private static readonly FailedMatchRequirement ForbiddenFailure = FailedMatchRequirement.Forbids("past_tense_stem");

    public static FailedMatchRequirement? ApplyTo(VocabMatchInspector inspector)
    {
        var requirement = inspector.Match.RequiresForbids.PastTenseStem;
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
        if (inspector.PreviousLocation == null)
        {
            return false;
        }

        if (inspector.PreviousLocation.Token.IsPastTenseStem)
        {
            return true;
        }

        if (inspector.Word.StartLocation.Token.IsPastTenseMarker)
        {
            return true;
        }

        return false;
    }
}
