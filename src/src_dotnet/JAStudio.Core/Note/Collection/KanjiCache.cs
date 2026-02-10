using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Collection;

public class KanjiCache : NoteCache<KanjiNote, KanjiSnapshot>
{
   private readonly Dictionary<string, List<KanjiNote>> _byRadical = new();
   public readonly Dictionary<string, List<KanjiNote>> ByReading = new();

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

   private static void RemoveFirstNoteWithId(List<KanjiNote> noteList, NoteId id)
   {
      for (var i = 0; i < noteList.Count; i++)
      {
         if (noteList[i].GetId() == id)
         {
            noteList.RemoveAt(i);
            return;
         }
      }
      throw new Exception($"Could not find note with id {id} in list");
   }

   protected override void InheritorRemoveFromCache(KanjiNote note, KanjiSnapshot snapshot)
   {
      var id = snapshot.Id;
      foreach (var form in snapshot.Radicals)
      {
         if (_byRadical.TryGetValue(form, out var list))
         {
            RemoveFirstNoteWithId(list, id);
         }
      }
      foreach (var reading in snapshot.Readings)
      {
         if (ByReading.TryGetValue(reading, out var list))
         {
            RemoveFirstNoteWithId(list, id);
         }
      }
   }

   protected override void InheritorAddToCache(KanjiNote note, KanjiSnapshot snapshot)
   {
      foreach (var form in snapshot.Radicals)
      {
         if (!_byRadical.ContainsKey(form))
         {
            _byRadical[form] = new List<KanjiNote>();
         }
         _byRadical[form].Add(note);
      }
      foreach (var reading in snapshot.Readings)
      {
         if (!ByReading.ContainsKey(reading))
         {
            ByReading[reading] = new List<KanjiNote>();
         }
         ByReading[reading].Add(note);
      }
   }

   public List<KanjiNote> WithRadical(string radical)
   {
      return _byRadical.TryGetValue(radical, out var notes) ? notes.ToList() : new List<KanjiNote>();
   }
}
