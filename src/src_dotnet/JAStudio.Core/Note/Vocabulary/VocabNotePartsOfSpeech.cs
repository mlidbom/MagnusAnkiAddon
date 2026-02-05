using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices.JamdictEx;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNotePartsOfSpeech
{
    private const string FieldName = "parts_of_speech"; // NoteFields.Vocab.parts_of_speech
    private readonly VocabNote _vocab;

    public VocabNotePartsOfSpeech(VocabNote vocab)
    {
        _vocab = vocab;
        // Initialize with current value
        SetRawStringValue(RawStringValue());
    }

    private VocabNote Vocab => _vocab;

    public string RawStringValue()
    {
        return Vocab.GetField(FieldName);
    }

    public void SetRawStringValue(string value)
    {
        Vocab.SetField(FieldName, POSSetManager.InternAndHarmonize(value));
    }

    public void Set(IEnumerable<string> value)
    {
        SetRawStringValue(string.Join(",", value));
    }

    public HashSet<string> Get()
    {
        return POSSetManager.Get(RawStringValue()).ToHashSet();
    }

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

    private static readonly HashSet<string> GaSuruNiSuruEndings = new() { "がする", "にする", "くする" };
    
    public bool IsNiSuruGaSuruKuSuruCompound()
    {
        var question = Vocab.Question.WithoutNoiseCharacters;
        if (question.Length <= 3)
            return false;
        
        var ending = question.Substring(question.Length - 3);
        return GaSuruNiSuruEndings.Contains(ending);
    }

    public bool IsUk()
    {
        return Vocab.Tags.Contains(Tags.Vocab.UsuallyKanaOnly);
    }

    public void SetAutomaticallyFromDictionary()
    {
        var lookup = DictLookup.LookupVocabWordOrName(Vocab);
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
            lookup = DictLookup.LookupWordOrNameWithMatchingReading(question, readings);
            var pos = lookup.PartsOfSpeech().Intersect(new[] { POS.Transitive, POS.Intransitive }).ToList();
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

    public bool IsCompleteNaAdjective()
    {
        return Vocab.Question.Raw.EndsWith("な") && Get().Contains(POS.NaAdjective);
    }

    public override string ToString() => RawStringValue();
}
