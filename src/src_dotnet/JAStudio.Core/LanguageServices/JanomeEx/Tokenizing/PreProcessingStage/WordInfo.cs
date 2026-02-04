using System.Linq;
using JAStudio.Core.LanguageServices.JamdictEx;
using JAStudio.Core.Note.Collection;

namespace JAStudio.Core.LanguageServices.JanomeEx.Tokenizing.PreProcessingStage;

public static class WordInfo
{
    public static WordInfoEntry? Lookup(string word)
    {
        var vocabEntries = App.Col().Vocab.WithForm(word);
        if (vocabEntries.Any())
        {
            // Try to find exact question match first
            foreach (var vocab in vocabEntries)
            {
                if (vocab.GetQuestion() == word)
                {
                    return new VocabWordInfoEntry(word, vocab);
                }
            }
            return new VocabWordInfoEntry(word, vocabEntries.First());
        }

        var dictLookupResult = DictLookup.LookupWord(word);
        if (dictLookupResult.FoundWords())
        {
            return new DictWordInfoEntry(word, dictLookupResult);
        }

        return null;
    }

    public static WordInfoEntry? LookupGodan(string word)
    {
        var wordInfo = Lookup(word);
        return wordInfo != null && wordInfo.IsGodan ? wordInfo : null;
    }

    public static WordInfoEntry? LookupIchidan(string word)
    {
        var wordInfo = Lookup(word);
        return wordInfo != null && wordInfo.IsIchidan ? wordInfo : null;
    }

    public static bool IsGodan(string word) => LookupGodan(word) != null;

    public static bool IsIchidan(string word) => LookupIchidan(word) != null;
}
