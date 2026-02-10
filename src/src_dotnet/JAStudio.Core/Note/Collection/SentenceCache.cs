using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Collection;

public class SentenceCache : NoteCache<SentenceNote, SentenceSnapshot>
{
   private readonly Dictionary<string, HashSet<SentenceNote>> _byVocabForm = new();
   private readonly Dictionary<string, List<SentenceNote>> _byUserHighlightedVocab = new();
   private readonly Dictionary<string, List<SentenceNote>> _byUserMarkedInvalidVocab = new();
   private readonly Dictionary<NoteId, HashSet<SentenceNote>> _byVocabId = new();

   public SentenceCache(NoteServices noteServices) : base(typeof(SentenceNote), (services, data) => new SentenceNote(services, data), noteServices)
   {
   }

   protected override void ClearDerivedIndexes()
   {
      _byVocabForm.Clear();
      _byUserHighlightedVocab.Clear();
      _byUserMarkedInvalidVocab.Clear();
      _byVocabId.Clear();
   }

   protected override NoteId CreateTypedId(Guid value) => new SentenceId(value);

   protected override SentenceSnapshot CreateSnapshot(SentenceNote note)
   {
      return new SentenceSnapshot(note);
   }

   public List<SentenceNote> WithVocab(VocabNote vocab)
   {
      return _byVocabId.TryGetValue(vocab.GetId(), out var notes) ? notes.ToList() : new List<SentenceNote>();
   }

   public List<SentenceNote> WithVocabForm(string form)
   {
      return _byVocabForm.TryGetValue(form, out var notes) ? notes.ToList() : new List<SentenceNote>();
   }

   public List<SentenceNote> WithUserHighlightedVocab(string form)
   {
      return _byUserHighlightedVocab.TryGetValue(form, out var notes) ? notes : new List<SentenceNote>();
   }

   public List<SentenceNote> WithUserMarkedInvalidVocab(string form)
   {
      return _byUserMarkedInvalidVocab.TryGetValue(form, out var notes) ? notes : new List<SentenceNote>();
   }

   private static void RemoveFirstNoteWithId(List<SentenceNote> noteList, NoteId id)
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

   protected override void InheritorRemoveFromCache(SentenceNote note, SentenceSnapshot snapshot)
   {
      var id = snapshot.Id;

      foreach (var vocabForm in snapshot.Words)
      {
         if (_byVocabForm.TryGetValue(vocabForm, out var set))
         {
            set.Remove(note);
         }
      }
      foreach (var vocabForm in snapshot.UserHighlightedVocab)
      {
         if (_byUserHighlightedVocab.TryGetValue(vocabForm, out var list))
         {
            RemoveFirstNoteWithId(list, id);
         }
      }
      foreach (var vocabForm in snapshot.MarkedIncorrectVocab)
      {
         if (_byUserMarkedInvalidVocab.TryGetValue(vocabForm, out var list))
         {
            RemoveFirstNoteWithId(list, id);
         }
      }
      foreach (var vocabId in snapshot.DetectedVocab)
      {
         if (_byVocabId.TryGetValue(vocabId, out var set))
         {
            set.Remove(note);
         }
      }
   }

   protected override void InheritorAddToCache(SentenceNote note, SentenceSnapshot snapshot)
   {
      foreach (var vocabForm in snapshot.Words)
      {
         if (!_byVocabForm.ContainsKey(vocabForm))
         {
            _byVocabForm[vocabForm] = new HashSet<SentenceNote>();
         }
         _byVocabForm[vocabForm].Add(note);
      }
      foreach (var vocabForm in snapshot.UserHighlightedVocab)
      {
         if (!_byUserHighlightedVocab.ContainsKey(vocabForm))
         {
            _byUserHighlightedVocab[vocabForm] = new List<SentenceNote>();
         }
         _byUserHighlightedVocab[vocabForm].Add(note);
      }
      foreach (var vocabForm in snapshot.MarkedIncorrectVocab)
      {
         if (!_byUserMarkedInvalidVocab.ContainsKey(vocabForm))
         {
            _byUserMarkedInvalidVocab[vocabForm] = new List<SentenceNote>();
         }
         _byUserMarkedInvalidVocab[vocabForm].Add(note);
      }
      foreach (var vocabId in snapshot.DetectedVocab)
      {
         if (!_byVocabId.ContainsKey(vocabId))
         {
            _byVocabId[vocabId] = new HashSet<SentenceNote>();
         }
         _byVocabId[vocabId].Add(note);
      }
   }
}
