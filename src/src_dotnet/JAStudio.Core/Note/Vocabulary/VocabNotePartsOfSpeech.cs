using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNotePartsOfSpeech
{
   const string FieldName = NoteFieldsConstants.Vocab.PartsOfSpeech;
   readonly VocabNote _vocab;
   readonly Func<string, string> _getField;
   readonly Action<string, string> _setField;

    public VocabNotePartsOfSpeech(VocabNote vocab, Func<string, string> getField, Action<string, string> setField)
    {
        _vocab = vocab;
        _getField = getField;
        _setField = setField;
        // Initialize with current value
        SetRawStringValue(RawStringValue());
    }

    VocabNote Vocab => _vocab;

    public string RawStringValue() => _getField(FieldName);

    public void SetRawStringValue(string value)
    {
        _setField(FieldName, POSSetManager.InternAndHarmonize(value));
    }

    public void Set(IEnumerable<string> value)
    {
        SetRawStringValue(string.Join(",", value));
    }

    public HashSet<string> Get() => POSSetManager.Get(RawStringValue()).ToHashSet();

    public bool IsIchidan() => Get().Contains(POS.IchidanVerb);
    public bool IsGodan() => Get().Contains(POS.GodanVerb);
    public bool IsTransitive() => Get().Contains(POS.Transitive);
    public bool IsIntransitive() => Get().Contains(POS.Intransitive);
    public bool IsInflectingWordType() => IsGodan() || IsIchidan();

    public bool IsSuruVerbIncluded()
    {
        var question = Vocab.Question.WithoutNoiseCharacters;
        return question.Length > 2 && question.EndsWith("する");
    }

    static readonly HashSet<string> GaSuruNiSuruEndings = ["がする", "にする", "くする"];

    public bool IsNiSuruGaSuruKuSuruCompound()
    {
        var question = Vocab.Question.WithoutNoiseCharacters;
        if (question.Length <= 3)
            return false;

        var ending = question.Substring(question.Length - 3);
        return GaSuruNiSuruEndings.Contains(ending);
    }

    public bool IsUk() => Vocab.Tags.Contains(Tags.UsuallyKanaOnly);

    public void SetAutomaticallyFromDictionary()
    {
        var lookup = Vocab.Services.DictLookup.LookupVocabWordOrName(Vocab);
        if (lookup.FoundWords())
        {
            var value = string.Join(", ", lookup.PartsOfSpeech());
            SetRawStringValue(value);
        }
        else if (IsSuruVerbIncluded())
        {
            var question = Vocab.Question.WithoutNoiseCharacters;
            question = question.Substring(0, question.Length - 2);
            var readings = Vocab.GetReadings().Select(r => r.Substring(0, r.Length - 2)).ToList();
            lookup = Vocab.Services.DictLookup.LookupWordOrNameWithMatchingReading(question, readings);
            var pos = lookup.PartsOfSpeech().Intersect([POS.Transitive, POS.Intransitive]).ToList();
            var value = POS.SuruVerb + ", " + string.Join(", ", pos);
            SetRawStringValue(value);
        }
    }

    public bool IsPassiveVerbCompound()
    {
        var compounds = Vocab.CompoundParts.Primary();
        if (compounds.Count == 0) return false;
        return AnalysisConstants.PassiveVerbEndings.Contains(compounds[compounds.Count - 1]);
    }

    public bool IsCausativeVerbCompound()
    {
        var compounds = Vocab.CompoundParts.Primary();
        if (compounds.Count == 0) return false;
        return AnalysisConstants.CausativeVerbEndings.Contains(compounds[compounds.Count - 1]);
    }

    public bool IsCompleteNaAdjective() => Vocab.Question.Raw.EndsWith("な") && Get().Contains(POS.NaAdjective);

    public override string ToString() => RawStringValue();
}
