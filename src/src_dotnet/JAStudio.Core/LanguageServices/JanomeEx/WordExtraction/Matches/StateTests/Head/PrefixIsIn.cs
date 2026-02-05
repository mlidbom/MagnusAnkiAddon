using System.Linq;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

public static class ForbidsPrefixIsIn
{
    public static FailedMatchRequirement? ApplyTo(VocabMatchInspector inspector)
    {
        var prefixes = inspector.Match.Rules.PrefixIsNot;
        if (prefixes.Any() && prefixes.Any(prefix => inspector.Prefix.EndsWith(prefix)))
        {
            return FailedMatchRequirement.Forbids($"prefix_in:{string.Join(",", prefixes)}");
        }

        return null;
    }
}

public static class RequiresPrefixIsIn
{
    public static FailedMatchRequirement? ApplyTo(VocabMatchInspector inspector)
    {
        var prefixes = inspector.Match.Rules.RequiredPrefix;
        if (prefixes.Any() && !prefixes.Any(prefix => inspector.Prefix.EndsWith(prefix)))
        {
            return FailedMatchRequirement.Required($"prefix_in:{string.Join(",", prefixes)}");
        }

        return null;
    }
}
