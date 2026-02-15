using JAStudio.Core.Note.CorpusData;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteMatchingConfiguration
{
    private readonly VocabNote _vocab;
    private int? _customRequirementsWeight;

    public VocabNoteMatchingRules ConfigurableRules { get; }
    public VocabMatchingRulesConfigurationRequiresForbidsFlags RequiresForbids { get; private set; }
    public VocabMatchingRulesConfigurationBoolFlags BoolFlags { get; private set; }

    public VocabNoteMatchingConfiguration(VocabNote vocab, VocabData? data, NoteGuard guard)
    {
        _vocab = vocab;
        ConfigurableRules = new VocabNoteMatchingRules(vocab, data?.MatchingRules, guard);
        RequiresForbids = new VocabMatchingRulesConfigurationRequiresForbidsFlags(vocab);
        BoolFlags = new VocabMatchingRulesConfigurationBoolFlags(vocab);
    }

    public void RefreshTagBasedFlags()
    {
        RequiresForbids = new VocabMatchingRulesConfigurationRequiresForbidsFlags(_vocab);
        BoolFlags = new VocabMatchingRulesConfigurationBoolFlags(_vocab);
        _customRequirementsWeight = null;
    }

    public int CustomRequirementsWeight
    {
        get
        {
            _customRequirementsWeight ??= RequiresForbids.MatchWeight + ConfigurableRules.MatchWeight;
            return _customRequirementsWeight.Value;
        }
    }
}
