using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.NoteFields.AutoSaveWrappers;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

public class RelatedVocab
{
   readonly VocabNote _vocab;
   readonly RelatedVocabData _data;
   readonly NoteGuard _guard;
   readonly Lazy<HashSet<NoteId>> _inCompoundIds;

   public RelatedVocab(VocabNote vocab, VocabRelatedSubData? subData, NoteGuard guard)
   {
      _vocab = vocab;
      _guard = guard;

      _data = subData != null
                 ? new RelatedVocabData(
                    subData.ErgativeTwin,
                    new ValueWrapper<string>(subData.DerivedFrom),
                    subData.PerfectSynonyms.ToHashSet(),
                    subData.Synonyms.ToHashSet(),
                    subData.Antonyms.ToHashSet(),
                    subData.ConfusedWith.ToHashSet(),
                    subData.SeeAlso.ToHashSet())
                 : new RelatedVocabData(
                    string.Empty,
                    new ValueWrapper<string>(string.Empty),
                    [],
                    [],
                    [],
                    [],
                    []);

      ErgativeTwin = new ErgativeTwin(vocab, _data, guard);
      Synonyms = new Synonyms(vocab, _data, guard);
      PerfectSynonyms = new PerfectSynonyms(vocab, _data, guard);
      Antonyms = new Antonyms(vocab, _data, guard);
      SeeAlso = new SeeAlso(vocab, _data, guard);
      DerivedFrom = new DerivedFromField(_data, guard);
      ConfusedWith = new ConfusedWithField(_data, guard);

      _inCompoundIds = new Lazy<HashSet<NoteId>>(() => InCompounds().Select(voc => voc.GetId()).ToHashSet());
   }

   public ErgativeTwin ErgativeTwin { get; }
   public Synonyms Synonyms { get; }
   public PerfectSynonyms PerfectSynonyms { get; }
   public Antonyms Antonyms { get; }
   public SeeAlso SeeAlso { get; }
   public DerivedFromField DerivedFrom { get; }
   public ConfusedWithField ConfusedWith { get; }

   public string RawJson
   {
      get => RelatedVocabData.Serializer().Serialize(_data);
      set
      {
         var deserialized = RelatedVocabData.Serializer().Deserialize(value);
         _guard.Update(() =>
         {
            _data.ErgativeTwin = deserialized.ErgativeTwin;
            _data.DerivedFrom = deserialized.DerivedFrom;
            _data.PerfectSynonyms = deserialized.PerfectSynonyms;
            _data.Synonyms = deserialized.Synonyms;
            _data.Antonyms = deserialized.Antonyms;
            _data.ConfusedWith = deserialized.ConfusedWith;
            _data.SeeAlso = deserialized.SeeAlso;
         });
      }
   }

   public HashSet<NoteId> InCompoundIds => _inCompoundIds.Value;

   public List<VocabNote> InCompounds() => _vocab.Services.Collection.Vocab.WithCompoundPart(_vocab.Question.DisambiguationName);

   public HashSet<VocabNote> HomophonesNotes()
   {
      return _vocab.GetReadings()
                   .SelectMany(reading => _vocab.Services.Collection.Vocab.WithReading(reading))
                   .Where(homophone => !Equals(homophone, _vocab))
                   .ToHashSet();
   }

   public HashSet<VocabNote> StemsNotes()
   {
      return _vocab.Conjugator.GetStemsForPrimaryForm()
                   .SelectMany(stem => _vocab.Services.Collection.Vocab.WithQuestion(stem))
                   .ToHashSet();
   }
}

public class DerivedFromField
{
   readonly RelatedVocabData _data;
   readonly NoteGuard _guard;

   public DerivedFromField(RelatedVocabData data, NoteGuard guard)
   {
      _data = data;
      _guard = guard;
   }

   public string Get() => _data.DerivedFrom.Get();

   public void Set(string value)
   {
      _guard.Update(() => _data.DerivedFrom.Set(value));
   }

   public override string ToString() => Get();
}

public class ConfusedWithField
{
   readonly RelatedVocabData _data;
   readonly NoteGuard _guard;

   public ConfusedWithField(RelatedVocabData data, NoteGuard guard)
   {
      _data = data;
      _guard = guard;
   }

   public HashSet<string> Get() => _data.ConfusedWith;

   public void Add(string value) => _guard.Update(() => _data.ConfusedWith.Add(value));

   public void Remove(string value) => _guard.Update(() => _data.ConfusedWith.Remove(value));

   public override string ToString() => string.Join(", ", _data.ConfusedWith);
}
