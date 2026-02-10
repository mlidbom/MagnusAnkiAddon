using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Collection;

public class KanjiCache : NoteCache<KanjiNote, KanjiSnapshot>
{
   private readonly Dictionary<string, HashSet<KanjiNote>> _byRadical = new();
   public readonly Dictionary<string, HashSet<KanjiNote>> ByReading = new();

   public KanjiCache(NoteServices noteServices) : base(typeof(KanjiNote), (services, data) => new KanjiNote(services, data), noteServices)
   {
   }

   protected override void ClearDerivedIndexes()
   {
      _byRadical.Clear();
      ByReading.Clear();
   }

   protected override NoteId CreateTypedId(Guid value) => new KanjiId(value);

   protected override KanjiSnapshot CreateSnapshot(KanjiNote note)
   {
      return new KanjiSnapshot(note);
   }

   protected override void InheritorRemoveFromCache(KanjiNote note, KanjiSnapshot snapshot)
   {
      foreach (var form in snapshot.Radicals)
      {
         if (_byRadical.TryGetValue(form, out var set))
         {
            set.Remove(note);
         }
      }
      foreach (var reading in snapshot.Readings)
      {
         if (ByReading.TryGetValue(reading, out var set))
         {
            set.Remove(note);
         }
      }
   }

   protected override void InheritorAddToCache(KanjiNote note, KanjiSnapshot snapshot)
   {
      foreach (var form in snapshot.Radicals)
      {
         if (!_byRadical.ContainsKey(form))
         {
            _byRadical[form] = new HashSet<KanjiNote>();
         }
         _byRadical[form].Add(note);
      }
      foreach (var reading in snapshot.Readings)
      {
         if (!ByReading.ContainsKey(reading))
         {
            ByReading[reading] = new HashSet<KanjiNote>();
         }
         ByReading[reading].Add(note);
      }
   }

   public List<KanjiNote> WithRadical(string radical)
   {
      return _byRadical.TryGetValue(radical, out var notes) ? notes.ToList() : new List<KanjiNote>();
   }
}
