using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Storage.Converters;

namespace JAStudio.Core.Note.Collection;

public class KanjiCache : NoteCache<KanjiNote, KanjiSnapshot>
{
   readonly Dictionary<string, HashSet<KanjiNote>> _byRadical = new();
   readonly Dictionary<string, HashSet<KanjiNote>> _byReading = new();

   public KanjiCache(NoteServices noteServices) : base(typeof(KanjiNote), (services, data) => new KanjiNote(services, KanjiData.FromAnkiNoteData(data)), noteServices) {}

   protected override KanjiNote CreateNoteByMergingAnkiData(NoteServices services, KanjiNote existing, NoteData ankiData)
   {
      var mergedData = KanjiNoteConverter.ToCorpusData(existing).MergeAnkiData(ankiData);
      return new KanjiNote(services, mergedData);
   }

   protected override void ClearDerivedIndexes()
   {
      _byRadical.Clear();
      _byReading.Clear();
   }

   protected override NoteId CreateTypedId(Guid value) => new KanjiId(value);

   protected override KanjiSnapshot CreateSnapshot(KanjiNote note) => new(note);

   protected override void InheritorRemoveFromCache(KanjiNote note, KanjiSnapshot snapshot)
   {
      foreach(var form in snapshot.Radicals)
      {
         if(_byRadical.TryGetValue(form, out var set))
         {
            set.Remove(note);
         }
      }

      foreach(var reading in snapshot.Readings)
      {
         if(_byReading.TryGetValue(reading, out var set))
         {
            set.Remove(note);
         }
      }
   }

   protected override void InheritorAddToCache(KanjiNote note, KanjiSnapshot snapshot)
   {
      foreach(var form in snapshot.Radicals)
      {
         if(!_byRadical.ContainsKey(form))
         {
            _byRadical[form] = new HashSet<KanjiNote>();
         }

         _byRadical[form].Add(note);
      }

      foreach(var reading in snapshot.Readings)
      {
         if(!_byReading.ContainsKey(reading))
         {
            _byReading[reading] = new HashSet<KanjiNote>();
         }

         _byReading[reading].Add(note);
      }
   }

   public List<KanjiNote> WithRadical(string radical)
   {
      return _monitor.Read(() => _byRadical.TryGetValue(radical, out var notes) ? notes.ToList() : new List<KanjiNote>());
   }

   public HashSet<KanjiNote> WithReading(string reading)
   {
      return _monitor.Read(() => _byReading.TryGetValue(reading, out var notes) ? notes.ToHashSet() : new HashSet<KanjiNote>());
   }
}
