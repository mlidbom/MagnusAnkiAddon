using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests;

public static class RequiresOrForbidsStartsWithIchidanImperativeStemOrInflection
{
    private static readonly FailedMatchRequirement RequiredFailure = FailedMatchRequirement.Required("ichidan_imperative");
    private static readonly FailedMatchRequirement ForbiddenFailure = FailedMatchRequirement.Forbids("ichidan_imperative");

    public static FailedMatchRequirement? ApplyTo(VocabMatchInspector inspector)
    {
        var requirement = inspector.Match.RequiresForbids.IchidanImperative;
        if (requirement.IsActive)
        {
            var isInState = inspector.Word.StartLocation.Token.IsIchidanImperativeStem || 
                           inspector.Word.StartLocation.Token.IsIchidanImperativeInflection;
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
}
