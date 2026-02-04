using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

public static class RequiresOrForbidsPrecedingAdverb
{
    private static readonly FailedMatchRequirement RequiredReason = FailedMatchRequirement.Required("preceding-adverb");
    private static readonly FailedMatchRequirement ForbiddenReason = FailedMatchRequirement.Forbids("preceding-adverb");

    public static FailedMatchRequirement? ApplyTo(VocabMatchInspector inspector)
    {
        if (inspector.RequiresForbids.PrecedingAdverb.IsRequired && !inspector.HasPrecedingAdverb)
        {
            return RequiredReason;
        }
        if (inspector.RequiresForbids.PrecedingAdverb.IsForbidden && inspector.HasPrecedingAdverb)
        {
            return ForbiddenReason;
        }
        return null;
    }
}
