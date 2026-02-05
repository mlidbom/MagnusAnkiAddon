using System.Linq;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests;

public static class ForbidsSurfaceIsIn
{
    public static FailedMatchRequirement? ApplyTo(VocabMatchInspector inspector)
    {
        var surfaces = inspector.Match.Rules.SurfaceIsNot;
        if (surfaces.Contains(inspector.Word.SurfaceVariant.Form))
        {
            return FailedMatchRequirement.Forbids($"surface_in:{string.Join(",", surfaces)}");
        }

        return null;
    }
}
