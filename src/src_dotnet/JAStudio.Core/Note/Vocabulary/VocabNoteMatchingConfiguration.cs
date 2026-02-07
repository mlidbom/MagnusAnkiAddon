namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteMatchingConfiguration
{
    private readonly VocabNote _vocab;
    private VocabNoteMatchingRules? _rules;
    private int? _customRequirementsWeight;

    public VocabMatchingRulesConfigurationRequiresForbidsFlags RequiresForbids { get; }
    public VocabMatchingRulesConfigurationBoolFlags BoolFlags { get; }

    public VocabNoteMatchingConfiguration(VocabNote vocab)
    {
        _vocab = vocab;
        RequiresForbids = new VocabMatchingRulesConfigurationRequiresForbidsFlags(vocab);
        BoolFlags = new VocabMatchingRulesConfigurationBoolFlags(vocab);
    }

    public VocabNoteMatchingRules ConfigurableRules
    {
        get
        {
            _rules ??= new VocabNoteMatchingRules(_vocab);
            return _rules;
        }
    }

    public int CustomRequirementsWeight
    {
        get
        {
            if (_customRequirementsWeight == null)
            {
                _customRequirementsWeight = RequiresForbids.MatchWeight + ConfigurableRules.MatchWeight;
            }
            return _customRequirementsWeight.Value;
        }
    }
}
