using JAStudio.Core.Note.ReactiveProperties;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteMatchingConfiguration
{
    private readonly VocabNote _vocab;
    private VocabNoteMatchingRules? _rules;
    private int? _customRequirementsWeight;

    public StringProperty MatchingRulesField { get; }
    public VocabMatchingRulesConfigurationRequiresForbidsFlags RequiresForbids { get; }
    public VocabMatchingRulesConfigurationBoolFlags BoolFlags { get; }

    public VocabNoteMatchingConfiguration(VocabNote vocab, StringProperty matchingRulesField)
    {
        _vocab = vocab;
        MatchingRulesField = matchingRulesField;
        RequiresForbids = new VocabMatchingRulesConfigurationRequiresForbidsFlags(vocab);
        BoolFlags = new VocabMatchingRulesConfigurationBoolFlags(vocab);
    }

    public VocabNoteMatchingRules ConfigurableRules
    {
        get
        {
            _rules ??= new VocabNoteMatchingRules(_vocab, MatchingRulesField);
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
