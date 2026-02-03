using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabCloner
{
    private readonly Func<VocabNote> _noteRef;

    public VocabCloner(Func<VocabNote> noteRef)
    {
        _noteRef = noteRef;
    }

    private VocabNote Note => _noteRef();

    public VocabNote PrefixToDictionaryForm(string prefix, string speechType = POS.Expression)
    {
        return CreatePostfixPrefixVersion(prefix, speechType, isPrefix: true);
    }

    public VocabNote PrefixToChopped(string prefix, int chopCharacters)
    {
        return CreatePostfixPrefixVersion(prefix, POS.Expression, isPrefix: true, chopOffCharacters: chopCharacters);
    }

    public string PrefixToChoppedPreview(string formPrefix, int chopCharacters)
    {
        return formPrefix + Note.GetQuestion().Substring(chopCharacters);
    }

    public VocabNote CreateSuffixVersion(string suffix, string speechType = POS.Expression, bool setCompounds = true, int truncateCharacters = 0)
    {
        return CreatePostfixPrefixVersion(suffix, speechType, setCompounds: setCompounds, chopOffCharacters: truncateCharacters);
    }

    private VocabNote CreatePostfixPrefixVersion(string addendum, string speechType, bool isPrefix = false, bool setCompounds = true, int chopOffCharacters = 0)
    {
        string AppendPrependAddendum(string baseStr)
        {
            if (!isPrefix)
            {
                return chopOffCharacters == 0 
                    ? baseStr + addendum 
                    : baseStr.Substring(0, baseStr.Length - chopOffCharacters) + addendum;
            }
            return addendum + baseStr.Substring(chopOffCharacters);
        }

        var vocabNote = Note;
        var newQuestion = AppendPrependAddendum(Note.GetQuestion());
        var newReadings = vocabNote.GetReadings().Select(AppendPrependAddendum).ToList();
        
        var newVocab = CreateNewVocabWithSomeDataCopied(newQuestion, Note.GetAnswer(), newReadings);

        if (setCompounds)
        {
            var compounds = isPrefix
                ? new List<string> { addendum, Note.Question.DisambiguationName }
                : new List<string> { Note.Question.DisambiguationName, addendum };
            newVocab.CompoundParts.Set(compounds);
        }

        newVocab.PartsOfSpeech.SetRawStringValue(speechType);
        newVocab.Forms.SetList(Note.Forms.AllSet().Select(AppendPrependAddendum).ToList());
        
        return newVocab;
    }

    private VocabNote CreateNewVocabWithSomeDataCopied(string question, string answer, List<string> readings)
    {
        // TODO: Implement proper cloning when VocabNote.Create is fully implemented
        var newVocab = VocabNote.Create(question, answer, readings, new List<string>());
        // Copy other fields as needed
        return newVocab;
    }

    public VocabNote CreateNaAdjective()
    {
        return CreatePostfixPrefixVersion("な", "na-adjective");
    }

    public VocabNote CreateNoAdjective()
    {
        return CreatePostfixPrefixVersion("の", "expression, no-adjective");
    }

    public VocabNote CreateNiAdverb()
    {
        return CreatePostfixPrefixVersion("に", "adverb");
    }

    public VocabNote CreateToAdverb()
    {
        return CreatePostfixPrefixVersion("と", "to-adverb");
    }

    public VocabNote CreateTePrefixedWord()
    {
        return CreatePostfixPrefixVersion("て", "auxiliary", isPrefix: true);
    }

    public VocabNote CreateOPrefixedWord()
    {
        return CreatePostfixPrefixVersion("お", Note.PartsOfSpeech.RawStringValue(), isPrefix: true);
    }

    public VocabNote CreateNSuffixedWord()
    {
        return CreatePostfixPrefixVersion("ん", POS.Expression);
    }

    public VocabNote CreateKaSuffixedWord()
    {
        return CreatePostfixPrefixVersion("か", POS.Expression);
    }

    public VocabNote CreateSuruVerb(bool shimasu = false)
    {
        var suruVerb = CreatePostfixPrefixVersion(shimasu ? "します" : "する", POS.SuruVerb);

        var forms = suruVerb.Forms.AllSet()
            .Concat(suruVerb.Forms.AllSet().Select(form => form.Replace("する", "をする")))
            .ToList();
        suruVerb.Forms.SetList(forms);

        if (Note.PartsOfSpeech.IsTransitive())
        {
            var value = suruVerb.PartsOfSpeech.RawStringValue() + ", " + POS.Transitive;
            suruVerb.PartsOfSpeech.SetRawStringValue(value);
        }

        if (Note.PartsOfSpeech.IsIntransitive())
        {
            var value = suruVerb.PartsOfSpeech.RawStringValue() + ", " + POS.Intransitive;
            suruVerb.PartsOfSpeech.SetRawStringValue(value);
        }

        return suruVerb;
    }
}
