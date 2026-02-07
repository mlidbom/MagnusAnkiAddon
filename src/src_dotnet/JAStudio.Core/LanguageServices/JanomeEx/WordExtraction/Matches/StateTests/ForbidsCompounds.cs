using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests;

public static class ForbidsConfiguredToHideAllCompounds
{
    private static readonly FailedMatchRequirement Failed = FailedMatchRequirement.Forbids("configured_to_hide_all_compounds");

    public static FailedMatchRequirement? ApplyTo(MatchInspector inspector)
    {
        if (inspector.Settings.HideAllCompounds() &&
            inspector.Word.IsCompound &&
            inspector.Word.Analysis.ForUI &&
            inspector.CompoundLocationsAllHaveValidNonCompoundMatches &&
            !inspector.IsVerbDictionaryFormCompound &&
            !inspector.IsIchidanCoveringGodanPotential)
        {
            return Failed;
        }

        return null;
    }
}
