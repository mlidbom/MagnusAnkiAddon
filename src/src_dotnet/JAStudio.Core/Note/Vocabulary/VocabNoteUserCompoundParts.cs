using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices.JanomeEx;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.Sentences;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteUserCompoundParts
{
    private readonly VocabNote _vocab;
    private readonly MutableCommaSeparatedStringsListField _field;

    public VocabNoteUserCompoundParts(VocabNote vocab)
    {
        _vocab = vocab;
        _field = new MutableCommaSeparatedStringsListField(vocab, NoteFieldsConstants.Vocab.UserCompounds);
    }

    private VocabNote Vocab => _vocab;
    private JPCollection Collection => Vocab.Collection;

    public List<string> Primary()
    {
        return _field.Get()
            .Where(part => !part.StartsWith("["))
            .ToList();
    }

    public List<string> All()
    {
        return _field.Get()
            .Select(StripBrackets)
            .ToList();
    }

    /// Returns all compound parts with brackets preserved (e.g. "[word]" stays as-is).
    public List<string> AllRaw() => _field.Get();

    public void Set(List<string> value)
    {
        _field.Set(value);
    }

    public HashSet<VocabNote> AllNotes()
    {
        return All()
            .SelectMany(part => Vocab.Services.Collection.Vocab.WithQuestion(part))
            .ToHashSet();
    }

    public List<VocabNote> PrimaryPartsNotes()
    {
        return Primary()
            .SelectMany(part => Vocab.Services.Collection.Vocab.WithFormPreferDisambiguationNameOrExactMatch(part))
            .ToList();
    }

    public void AutoGenerate()
    {
        var exclusions = Vocab.Forms.AllSet()
            .Select(form => WordExclusion.Global(form))
            .ToList();
        var config = SentenceConfiguration.FromIncorrectMatches(exclusions);
        var analysisServices = new AnalysisServices(Vocab.Services.Collection.Vocab, Vocab.Services.DictLookup, Vocab.Services.Settings);
        var analysis = new TextAnalysis(analysisServices, Vocab.GetQuestion(), config);
        var compoundParts = analysis.DisplayWordVariants
            .Where(a => !Vocab.Forms.AllSet().Contains(a.Form))
            .Select(a => a.Form)
            .ToList();

        if (compoundParts.Count <= 1)  // time to brute force it
        {
            var word = Vocab.GetQuestion();
            var allSubstrings = new List<string>();
            for (int i = 0; i < word.Length; i++)
            {
                for (int j = i + 1; j <= word.Length; j++)
                {
                    var substring = word.Substring(i, j - i);
                    if (substring != word)
                    {
                        allSubstrings.Add(substring);
                    }
                }
            }

            var allWordSubstrings = allSubstrings
                .Where(w => Vocab.Services.DictLookup.IsDictionaryOrCollectionWord(w))
                .ToList();

            compoundParts = allWordSubstrings
                .Where(segment => !allWordSubstrings.Any(parent => parent.Contains(segment) && parent != segment))
                .ToList();
        }

        var segmentsMissingVocab = compoundParts
            .Where(segment => !Collection.Vocab.IsWord(segment))
            .ToList();

        foreach (var missing in segmentsMissingVocab)
        {
            Vocab.Services.VocabNoteFactory.CreateWithDictionary(missing);
        }

        Set(compoundParts);
    }

    private static string StripBrackets(string part)
    {
        return part.Replace("[", string.Empty).Replace("]", string.Empty);
    }

    public override string ToString()
    {
        return _field.ToString() ?? string.Empty;
    }
}
