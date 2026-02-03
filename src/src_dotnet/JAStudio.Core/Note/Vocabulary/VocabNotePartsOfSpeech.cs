using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNotePartsOfSpeech
{
    private const string FieldName = "parts_of_speech"; // NoteFields.Vocab.parts_of_speech
    private readonly Func<VocabNote> _vocab;

    public VocabNotePartsOfSpeech(Func<VocabNote> vocab)
    {
        _vocab = vocab;
        // Initialize with current value
        SetRawStringValue(RawStringValue());
    }

    private VocabNote Vocab => _vocab();

    public string RawStringValue()
    {
        return Vocab.GetField(FieldName);
    }

    public void SetRawStringValue(string value)
    {
        // TODO: Implement POSSetManager.InternAndHarmonize when ported
        Vocab.SetField(FieldName, value);
    }

    public void Set(IEnumerable<string> value)
    {
        SetRawStringValue(string.Join(",", value));
    }

    public HashSet<string> Get()
    {
        // TODO: Implement POSSetManager.Get when ported
        var raw = RawStringValue();
        if (string.IsNullOrWhiteSpace(raw))
            return new HashSet<string>();
        
        return raw.Split(',', StringSplitOptions.RemoveEmptyEntries)
            .Select(s => s.Trim())
            .ToHashSet();
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
        // TODO: Implement when Tags.UsuallyKanaOnly is ported
        return false;
    }

    public void SetAutomaticallyFromDictionary()
    {
        // TODO: Implement when DictLookup is ported
        // from jaslib.language_services.jamdict_ex.dict_lookup import DictLookup
        // lookup = DictLookup.lookup_vocab_word_or_name(self._vocab)
        // if lookup.found_words():
        //     value = ", ".join(lookup.parts_of_speech())
        //     self.set_raw_string_value(value)
    }

    public bool IsPassiveVerbCompound()
    {
        // TODO: Implement when compound_parts is ported
        return false;
    }
}
