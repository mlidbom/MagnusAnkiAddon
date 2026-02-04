using System.Linq;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Tail;

public sealed class ForbidsHasDisplayedOverlappingFollowingCompound : CustomForbidsNoCache
{
    private ForbidsHasDisplayedOverlappingFollowingCompound(VocabMatchInspector inspector) : base(inspector)
    {
    }

    public static ForbidsHasDisplayedOverlappingFollowingCompound? ApplyTo(VocabMatchInspector inspector)
    {
        return inspector.RequiresForbids.YieldLastToken.IsRequired && !inspector.Match.IsHighlighted
            ? new ForbidsHasDisplayedOverlappingFollowingCompound(inspector)
            : null;
    }

    public override string Description => "has_displayed_following_overlapping_compound";

    protected override bool InternalIsInState()
    {
        // todo: this is a problematic reference to display_words. That collection is initialized using this class,
        // so this class will return different results depending on whether it is used after or before display_words is first initialized. Ouch

        var endLocation = Inspector.EndLocation;
        var tailLocation = endLocation;
        // The dictionary verb inflection is a special case that is shown as a separate token after the word in which it is part, so it does not by itself cover/shadow anything
        // thus, we skip such tokens as possible locations for following compounds to overlap, since that words starting with that token are shown after this compound anyway, and are not hidden by this compound.
        // this logic is mirrored in is_shadowed logic
        if (endLocation.Token.IsDictionaryVerbInflection)
        {
            if (endLocation.Previous == null)
            {
                return false;
            }
            tailLocation = endLocation.Previous;
        }

        while (tailLocation != Inspector.Word.StartLocation)
        {
            foreach (var displayWord in tailLocation.DisplayWords)
            {
                if (displayWord.EndLocation.TokenIndex > endLocation.TokenIndex)
                {
                    return true;
                }
            }

            tailLocation = tailLocation.Previous!;
        }

        return false;
    }
}
