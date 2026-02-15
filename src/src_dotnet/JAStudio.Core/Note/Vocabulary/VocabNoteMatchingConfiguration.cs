using System;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteMatchingConfiguration
{
    private readonly VocabNote _vocab;
    private readonly Func<string, string> _getField;
    private readonly Action<string, string> _setField;
    private VocabNoteMatchingRules? _rules;
    private int? _customRequirementsWeight;

    public VocabMatchingRulesConfigurationRequiresForbidsFlags RequiresForbids { get; }
    public VocabMatchingRulesConfigurationBoolFlags BoolFlags { get; }

    public VocabNoteMatchingConfiguration(VocabNote vocab, Func<string, string> getField, Action<string, string> setField)
    {
        _vocab = vocab;
        _getField = getField;
        _setField = setField;
        RequiresForbids = new VocabMatchingRulesConfigurationRequiresForbidsFlags(vocab);
        BoolFlags = new VocabMatchingRulesConfigurationBoolFlags(vocab);
    }

    public VocabNoteMatchingRules ConfigurableRules
    {
        get
        {
            _rules ??= new VocabNoteMatchingRules(_vocab, _getField, _setField);
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
