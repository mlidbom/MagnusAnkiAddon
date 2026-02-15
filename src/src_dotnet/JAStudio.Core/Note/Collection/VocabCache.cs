using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Storage.Converters;

namespace JAStudio.Core.Note.Collection;

public class VocabCache : NoteCache<VocabNote, VocabSnapshot>
{
   private readonly Dictionary<string, HashSet<VocabNote>> _byDisambiguationName = new();
   private readonly Dictionary<string, HashSet<VocabNote>> _byForm = new();
   private readonly Dictionary<string, HashSet<VocabNote>> _byKanjiInMainForm = new();
   private readonly Dictionary<string, HashSet<VocabNote>> _byKanjiInAnyForm = new();
   private readonly Dictionary<string, HashSet<VocabNote>> _byCompoundPart = new();
   private readonly Dictionary<string, HashSet<VocabNote>> _byDerivedFrom = new();
   private readonly Dictionary<string, HashSet<VocabNote>> _byReading = new();
   private readonly Dictionary<string, HashSet<VocabNote>> _byStem = new();

   public VocabCache(NoteServices noteServices) : base(typeof(VocabNote), (services, data) => new VocabNote(services, VocabData.FromAnkiNoteData(data)), noteServices)
   {
   }

   protected override VocabNote CreateNoteByMergingAnkiData(NoteServices services, VocabNote existing, NoteData ankiData)
   {
      var mergedData = VocabNoteConverter.ToCorpusData(existing).MergeAnkiData(ankiData);
      return new VocabNote(services, mergedData);
   }

   protected override void ClearDerivedIndexes()
   {
      _byDisambiguationName.Clear();
      _byForm.Clear();
      _byKanjiInMainForm.Clear();
      _byKanjiInAnyForm.Clear();
      _byCompoundPart.Clear();
      _byDerivedFrom.Clear();
      _byReading.Clear();
      _byStem.Clear();
   }

   protected override NoteId CreateTypedId(Guid value) => new VocabId(value);

   public List<VocabNote> WithForm(string form)
   {
      return _monitor.Read(() => _byForm.TryGetValue(form, out var notes) ? notes.ToList() : new List<VocabNote>());
   }

   public List<VocabNote> WithDisambiguationName(string form)
   {
      return _monitor.Read(() => _byDisambiguationName.TryGetValue(form, out var notes) ? notes.ToList() : new List<VocabNote>());
   }

   public List<VocabNote> WithCompoundPart(string disambiguationName)
   {
      return _monitor.Read(() =>
      {
         var compoundParts = new HashSet<VocabNote>();

         void FetchParts(string partForm)
         {
            if (_byCompoundPart.TryGetValue(partForm, out var vocabList))
            {
               foreach (var vocab in vocabList)
               {
                  if (!compoundParts.Contains(vocab))
                  {
                     compoundParts.Add(vocab);
                     FetchParts(vocab.Question.DisambiguationName);
                  }
               }
            }
         }

         FetchParts(disambiguationName);

         return compoundParts.OrderBy(v => v.GetQuestion()).ToList();
      });
   }

   public List<VocabNote> DerivedFrom(string form)
   {
      return _monitor.Read(() => _byDerivedFrom.TryGetValue(form, out var notes) ? notes.ToList() : new List<VocabNote>());
   }

   public List<VocabNote> WithKanjiInMainForm(string kanji)
   {
      return _monitor.Read(() => _byKanjiInMainForm.TryGetValue(kanji, out var notes) ? notes.ToList() : new List<VocabNote>());
   }

   public List<VocabNote> WithKanjiInAnyForm(string kanji)
   {
      return _monitor.Read(() => _byKanjiInAnyForm.TryGetValue(kanji, out var notes) ? notes.ToList() : new List<VocabNote>());
   }

   public List<VocabNote> WithReading(string reading)
   {
      return _monitor.Read(() => _byReading.TryGetValue(reading, out var notes) ? notes.ToList() : new List<VocabNote>());
   }

   public List<VocabNote> WithStem(string stem)
   {
      return _monitor.Read(() => _byStem.TryGetValue(stem, out var notes) ? notes.ToList() : new List<VocabNote>());
   }

   protected override VocabSnapshot CreateSnapshot(VocabNote note)
   {
      return new VocabSnapshot(note);
   }

   protected override void InheritorRemoveFromCache(VocabNote note, VocabSnapshot snapshot)
   {
      foreach (var form in snapshot.Forms)
      {
         if (_byForm.TryGetValue(form, out var set)) set.Remove(note);
      }
      foreach (var part in snapshot.CompoundParts)
      {
         if (_byCompoundPart.TryGetValue(part, out var set)) set.Remove(note);
      }
      if (_byDerivedFrom.TryGetValue(snapshot.DerivedFrom, out var derivedSet))
      {
         derivedSet.Remove(note);
      }
      if (_byDisambiguationName.TryGetValue(snapshot.DisambiguationName, out var disambigSet))
      {
         disambigSet.Remove(note);
      }
      foreach (var kanji in snapshot.MainFormKanji)
      {
         if (_byKanjiInMainForm.TryGetValue(kanji, out var set)) set.Remove(note);
      }
      foreach (var kanji in snapshot.AllKanji)
      {
         if (_byKanjiInAnyForm.TryGetValue(kanji, out var set)) set.Remove(note);
      }
      foreach (var reading in snapshot.Readings)
      {
         if (_byReading.TryGetValue(reading, out var set)) set.Remove(note);
      }
      foreach (var stem in snapshot.Stems)
      {
         if (_byStem.TryGetValue(stem, out var set)) set.Remove(note);
      }
   }

   protected override void InheritorAddToCache(VocabNote note, VocabSnapshot snapshot)
   {
      foreach (var form in snapshot.Forms)
      {
         if (!_byForm.ContainsKey(form)) _byForm[form] = new HashSet<VocabNote>();
         _byForm[form].Add(note);
      }
      foreach (var compoundPart in snapshot.CompoundParts)
      {
         if (!_byCompoundPart.ContainsKey(compoundPart)) _byCompoundPart[compoundPart] = new HashSet<VocabNote>();
         _byCompoundPart[compoundPart].Add(note);
      }
      if (!_byDerivedFrom.ContainsKey(snapshot.DerivedFrom)) _byDerivedFrom[snapshot.DerivedFrom] = new HashSet<VocabNote>();
      _byDerivedFrom[snapshot.DerivedFrom].Add(note);
        
      if (!_byDisambiguationName.ContainsKey(snapshot.DisambiguationName)) _byDisambiguationName[snapshot.DisambiguationName] = new HashSet<VocabNote>();
      _byDisambiguationName[snapshot.DisambiguationName].Add(note);
        
      foreach (var kanji in snapshot.MainFormKanji)
      {
         if (!_byKanjiInMainForm.ContainsKey(kanji)) _byKanjiInMainForm[kanji] = new HashSet<VocabNote>();
         _byKanjiInMainForm[kanji].Add(note);
      }
      foreach (var kanji in snapshot.AllKanji)
      {
         if (!_byKanjiInAnyForm.ContainsKey(kanji)) _byKanjiInAnyForm[kanji] = new HashSet<VocabNote>();
         _byKanjiInAnyForm[kanji].Add(note);
      }
      foreach (var reading in snapshot.Readings)
      {
         if (!_byReading.ContainsKey(reading)) _byReading[reading] = new HashSet<VocabNote>();
         _byReading[reading].Add(note);
      }
      foreach (var stem in snapshot.Stems)
      {
         if (!_byStem.ContainsKey(stem)) _byStem[stem] = new HashSet<VocabNote>();
         _byStem[stem].Add(note);
      }
   }
}
