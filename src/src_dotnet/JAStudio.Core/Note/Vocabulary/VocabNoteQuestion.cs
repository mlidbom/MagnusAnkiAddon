using JAStudio.Core.LanguageServices;
using JAStudio.Core.Note.ReactiveProperties;
using System.Collections.Generic;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabStems
{
    private readonly VocabNote _vocab;

    public VocabStems(VocabNote vocab)
    {
        _vocab = vocab;
    }

    public string? MasuStem()
    {
        var masuStem = Conjugator.GetIStemVocab(_vocab);
        return masuStem != _vocab.Question.Raw ? masuStem : null;
    }
}

public class VocabNoteQuestion
{
    public const string DisambiguationMarker = ":";
    public const string InvalidQuestionMessage = "INVALID QUESTION FORMAT. If you need to specify disambiguation, use question:disambiguation if not do NOT use : characters. More than one is invalid";

    private readonly VocabNote _vocab;
    private readonly StringProperty _field;
    public string Raw { get; private set; }
    public string DisambiguationName { get; private set; }

    public VocabNoteQuestion(VocabNote vocab, StringProperty field)
    {
        _vocab = vocab;
        _field = field;
        Raw = string.Empty;
        DisambiguationName = string.Empty;
        InitValueRaw();
    }

    private void InitValueRaw()
    {
        var value = _field.Value;
        
        if (value.Contains(DisambiguationMarker))
        {
            DisambiguationName = value;
            var parts = DisambiguationName.Split(DisambiguationMarker);
            
            if (parts.Length != 2)
            {
                Raw = InvalidQuestionMessage;
            }
            else
            {
                Raw = parts[0];
            }
        }
        else
        {
            Raw = value;
            DisambiguationName = value;
        }

        if (string.IsNullOrEmpty(Raw))
        {
            Raw = "[EMPTY]";
        }
    }

    public bool IsValid => Raw != InvalidQuestionMessage;
    public bool IsDisambiguated => DisambiguationName.Contains(DisambiguationMarker);

    public string WithoutNoiseCharacters => Raw.Replace(Mine.VocabPrefixSuffixMarker, "");

    public VocabStems Stems() => new VocabStems(_vocab);

    public void Set(string value)
    {
        _field.Set(value);
        InitValueRaw();
        
        if (!_vocab.Forms.AllSet().Contains(Raw))
        {
            var updatedForms = new HashSet<string>(_vocab.Forms.AllSet()) { Raw };
            _vocab.Forms.SetSet(updatedForms);
        }
    }

    public override string ToString() => Raw;
}

