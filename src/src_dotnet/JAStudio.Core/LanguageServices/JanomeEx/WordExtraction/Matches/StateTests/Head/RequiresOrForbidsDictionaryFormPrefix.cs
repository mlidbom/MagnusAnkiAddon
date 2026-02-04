using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

public static class RequiresOrForbidsDictionaryFormPrefix
{
    private static readonly FailedMatchRequirement RequiredFailure = FailedMatchRequirement.Required("dictionary_form_prefix");
    private static readonly FailedMatchRequirement ForbiddenFailure = FailedMatchRequirement.Forbids("dictionary_form_prefix");

    public static FailedMatchRequirement? ApplyTo(VocabMatchInspector inspector)
    {
        var requirement = inspector.Match.RequiresForbids.DictionaryFormPrefix;
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
        if (inspector.PreviousLocation != null && inspector.PreviousLocation.Token.IsDictionaryVerbInflection)
        {
            return true;
        }

        return false;
    }
}
