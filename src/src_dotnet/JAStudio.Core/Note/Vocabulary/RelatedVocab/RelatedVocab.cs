using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.NoteFields.AutoSaveWrappers;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

public class RelatedVocab
{
   readonly VocabNote _vocab;
   readonly MutableSerializedObjectField<RelatedVocabData> _data;
   readonly Lazy<HashSet<NoteId>> _inCompoundIds;

    public RelatedVocab(VocabNote vocab, Func<string, string> getField, Action<string, string> setField)
    {
        _vocab = vocab;

        _data = new MutableSerializedObjectField<RelatedVocabData>(
            new MutableStringField(NoteFieldsConstants.Vocab.RelatedVocab, getField, setField),
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

        _inCompoundIds = new Lazy<HashSet<NoteId>>(() =>
            InCompounds().Select(voc => voc.GetId()).ToHashSet());
    }

    public ErgativeTwin ErgativeTwin { get; }
    public Synonyms Synonyms { get; }
    public PerfectSynonyms PerfectSynonyms { get; }
    public Antonyms Antonyms { get; }
    public SeeAlso SeeAlso { get; }
    public FieldWrapper<string, RelatedVocabData> DerivedFrom { get; }
    public FieldSetWrapper<string> ConfusedWith { get; }

    public string RawJson
    {
        get => _data.RawValue;
        set => _data.RawValue = value;
    }

    public HashSet<NoteId> InCompoundIds => _inCompoundIds.Value;

    public List<VocabNote> InCompounds() => _vocab.Services.Collection.Vocab.WithCompoundPart(_vocab.Question.DisambiguationName);

    public HashSet<VocabNote> HomophonesNotes()
    {
        return _vocab.GetReadings()
            .SelectMany(reading => _vocab.Services.Collection.Vocab.WithReading(reading))
            .Where(homophone => homophone != _vocab)
            .ToHashSet();
    }

    public HashSet<VocabNote> StemsNotes()
    {
        return _vocab.Conjugator.GetStemsForPrimaryForm()
            .SelectMany(stem => _vocab.Services.Collection.Vocab.WithQuestion(stem))
            .ToHashSet();
    }

    HashSet<KanjiNote> MainFormKanjiNotes => _vocab.Services.Collection.Kanji.WithAnyKanjiIn(_vocab.Kanji.ExtractMainFormKanji()).ToHashSet();

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
