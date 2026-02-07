using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary;

public class YieldLastTokenToOverlappingCompound : RequireForbidFlagField
{
    private readonly VocabNote _vocab;
    private readonly VocabNotePartsOfSpeech _pos;

    public YieldLastTokenToOverlappingCompound(VocabNote vocab)
        : base(vocab, 0, 0, 
            Tags.Vocab.Matching.YieldLastTokenToOverlappingCompound, 
            Tags.Vocab.Matching.Forbids.AutoYielding)
    {
        _vocab = vocab;
        _pos = vocab.PartsOfSpeech;
    }

    private bool DecideIfRequired()
    {
        return base.IsRequired
            || (!IsForbidden
                && (
                    // na adjectives
                    _pos.IsCompleteNaAdjective()
                    // suru verb compounds
                    || (_vocab.Services.Settings.AutomaticallyYieldLastTokenInSuruVerbCompoundsToOverlappingCompound()
                        && _pos.IsSuruVerbIncluded()
                        && !_pos.IsNiSuruGaSuruKuSuruCompound())
                    // passive verb compounds
                    || (_vocab.Services.Settings.AutomaticallyYieldLastTokenInPassiveVerbCompoundsToOverlappingCompound()
                        && _pos.IsPassiveVerbCompound())
                    // causative verb compounds
                    || (_vocab.Services.Settings.AutomaticallyYieldLastTokenInCausativeVerbCompoundsToOverlappingCompound()
                        && _pos.IsCausativeVerbCompound())
                ));
    }

    public override bool IsRequired => DecideIfRequired();

    public override string ToString()
    {
        var parts = new System.Collections.Generic.List<string>();
        if (IsRequired) parts.Add("required");
        if (IsForbidden) parts.Add("forbidden");
        return string.Join(" ", parts);
    }
}
