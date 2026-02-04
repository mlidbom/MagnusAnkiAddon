using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.NoteFields.AutoSaveWrappers;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

public class RelatedVocab
{
    private readonly VocabNote _vocab;
    private readonly SerializedObjectField<RelatedVocabData> _data;
    private readonly Lazy<HashSet<int>> _inCompoundIds;

    public RelatedVocab(VocabNote vocab)
    {
        _vocab = vocab;

        _data = new SerializedObjectField<RelatedVocabData>(
            vocab,
            NoteFieldsConstants.Vocab.RelatedVocab,
            RelatedVocabData.Serializer());

        ErgativeTwin = new ErgativeTwin(vocab, _data);
        Synonyms = new Synonyms(vocab, _data);
        PerfectSynonyms = new PerfectSynonyms(
            vocab,
            FieldSetWrapper<string>.ForJsonObjectField(_data, _data.Get().PerfectSynonyms));
        Antonyms = new Antonyms(vocab, _data);
        SeeAlso = new SeeAlso(vocab, _data);
        DerivedFrom = new FieldWrapper<string, RelatedVocabData>(_data, _data.Get().DerivedFrom);
        ConfusedWith = FieldSetWrapper<string>.ForJsonObjectField(_data, _data.Get().ConfusedWith);

        _inCompoundIds = new Lazy<HashSet<int>>(() =>
            InCompounds().Select(voc => voc.GetId()).ToHashSet());
    }

    public ErgativeTwin ErgativeTwin { get; }
    public Synonyms Synonyms { get; }
    public PerfectSynonyms PerfectSynonyms { get; }
    public Antonyms Antonyms { get; }
    public SeeAlso SeeAlso { get; }
    public FieldWrapper<string, RelatedVocabData> DerivedFrom { get; }
    public FieldSetWrapper<string> ConfusedWith { get; }

    public HashSet<int> InCompoundIds => _inCompoundIds.Value;

    public List<VocabNote> InCompounds()
    {
        return App.Col().Vocab.WithCompoundPart(_vocab.Question.DisambiguationName);
    }

    public HashSet<VocabNote> HomophonesNotes()
    {
        return _vocab.GetReadings()
            .SelectMany(reading => App.Col().Vocab.WithReading(reading))
            .Where(homophone => homophone != _vocab)
            .ToHashSet();
    }

    public HashSet<VocabNote> StemsNotes()
    {
        return _vocab.Conjugator.GetStemsForPrimaryForm()
            .SelectMany(stem => App.Col().Vocab.WithQuestion(stem))
            .ToHashSet();
    }

    private HashSet<KanjiNote> MainFormKanjiNotes
    {
        get
        {
            return App.Col().Kanji.WithAnyKanjiIn(_vocab.Kanji.ExtractMainFormKanji()).ToHashSet();
        }
    }

    public HashSet<JPNote> GetDirectDependencies()
    {
        var dependencies = new HashSet<JPNote>();
        
        foreach (var kanji in MainFormKanjiNotes)
        {
            dependencies.Add(kanji);
        }
        
        foreach (var compoundPart in _vocab.CompoundParts.AllNotes())
        {
            dependencies.Add(compoundPart);
        }
        
        return dependencies;
    }
}
