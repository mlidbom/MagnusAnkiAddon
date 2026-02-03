using System;
using System.Collections.Generic;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteMatchingConfiguration
{
    private readonly Func<VocabNote> _vocab;

    public VocabNoteMatchingConfiguration(Func<VocabNote> vocab)
    {
        _vocab = vocab;
        // TODO: Implement matching rules when serialization and field wrappers are ported
        // - VocabNoteMatchingRules (surface_is_not, prefix_is_not, suffix_is_not, etc.)
        // - RequiresForbidsFlags (masu_stem, godan, ichidan, irrealis, etc.)
        // - BoolFlags (is_inflecting_word)
    }

    private VocabNote Vocab => _vocab();

    // TODO: Implement when matching rules are ported
    // public VocabNoteMatchingRules Rules { get; }
    // public VocabMatchingRulesConfigurationRequiresForbidsFlags RequiresForbids { get; }
    // public VocabMatchingRulesConfigurationBoolFlags BoolFlags { get; }

    public int MatchWeight
    {
        get
        {
            // TODO: Calculate from rules and flags
            return 0;
        }
    }
}
