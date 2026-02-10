using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements;

namespace JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests;

public sealed class ForbidsIsShadowed : MatchRequirement
{
    private readonly MatchInspector _inspector;

    public ForbidsIsShadowed(MatchInspector inspector)
    {
        _inspector = inspector;
    }

    public override bool IsFulfilled => !_inspector.Match.IsShadowed;

    public override string FailureReason
    {
        get
        {
            var shadowedBy = _inspector.Match.Word.ShadowedBy;
            return shadowedBy != "" ? $"forbids::shadowed_by:{shadowedBy}" : "";
        }
    }
}
