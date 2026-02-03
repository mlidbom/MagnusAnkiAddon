using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

public class VocabRelatedNotes
{
    private readonly VocabNote _vocab;
    private HashSet<int>? _inCompoundIds;

    public VocabRelatedNotes(VocabNote vocab)
    {
        _vocab = vocab;
        // TODO: Initialize related vocab components when ported:
        // - ErgativeTwin
        // - Synonyms
        // - PerfectSynonyms
        // - Antonyms
        // - SeeAlso
        // - DerivedFrom
        // - ConfusedWith
    }

    private VocabNote Vocab => _vocab;

    public HashSet<int> InCompoundIds
    {
        get
        {
            if (_inCompoundIds == null)
            {
                _inCompoundIds = InCompounds()
                    .Select(voc => voc.GetId())
                    .ToHashSet();
            }
            return _inCompoundIds;
        }
    }

    public List<VocabNote> InCompounds()
    {
        return App.Col().Vocab.WithCompoundPart(Vocab.Question.DisambiguationName);
    }

    public HashSet<VocabNote> HomophonesNotes()
    {
        return Vocab.GetReadings()
            .SelectMany(reading => App.Col().Vocab.WithReading(reading))
            .Where(homophone => homophone != Vocab)
            .ToHashSet();
    }

    public HashSet<VocabNote> StemsNotes()
    {
        return Vocab.Conjugator.GetStemsForPrimaryForm()
            .SelectMany(stem => App.Col().Vocab.WithQuestion(stem))
            .ToHashSet();
    }

    private HashSet<KanjiNote> MainFormKanjiNotes()
    {
        return App.Col().Kanji.WithAnyKanjiIn(Vocab.Kanji.ExtractMainFormKanji()).ToHashSet();
    }

    public HashSet<JPNote> GetDirectDependencies()
    {
        var dependencies = new HashSet<JPNote>();
        
        foreach (var kanji in MainFormKanjiNotes())
        {
            dependencies.Add(kanji);
        }
        
        foreach (var compoundPart in Vocab.CompoundParts.AllNotes())
        {
            dependencies.Add(compoundPart);
        }
        
        return dependencies;
    }

    // TODO: Port these when their implementations are ready:
    // public string DerivedFrom { get; set; }
    // public HashSet<string> ConfusedWith { get; set; }
    // public ErgativeTwin ErgativeTwin { get; }
    // public Synonyms Synonyms { get; }
    // public PerfectSynonyms PerfectSynonyms { get; }
    // public Antonyms Antonyms { get; }
    // public SeeAlso SeeAlso { get; }
}
