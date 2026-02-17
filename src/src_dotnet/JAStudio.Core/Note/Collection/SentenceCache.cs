using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Storage.Converters;

namespace JAStudio.Core.Note.Collection;

class SentenceCache : NoteCache<SentenceNote, SentenceSnapshot>
{
   readonly Dictionary<string, HashSet<SentenceNote>> _byVocabForm = new();
   readonly Dictionary<string, HashSet<SentenceNote>> _byUserHighlightedVocab = new();
   readonly Dictionary<string, HashSet<SentenceNote>> _byUserMarkedInvalidVocab = new();
   readonly Dictionary<NoteId, HashSet<SentenceNote>> _byVocabId = new();

   public SentenceCache(NoteServices noteServices) : base((services, data) => new SentenceNote(services, SentenceData.FromAnkiNoteData(data)), noteServices) {}

   protected override SentenceNote CreateNoteByMergingAnkiData(NoteServices services, SentenceNote existing, NoteData ankiData)
   {
      var mergedData = SentenceNoteConverter.ToCorpusData(existing).MergeAnkiData(ankiData);
      return new SentenceNote(services, mergedData);
   }

   protected override void ClearDerivedIndexes()
   {
      _byVocabForm.Clear();
      _byUserHighlightedVocab.Clear();
      _byUserMarkedInvalidVocab.Clear();
      _byVocabId.Clear();
   }

   protected override NoteId CreateTypedId(Guid value) => new SentenceId(value);

   protected override SentenceSnapshot CreateSnapshot(SentenceNote note) => new(note);

   public List<SentenceNote> WithVocab(VocabNote vocab)
   {
      return _monitor.Read(() => _byVocabId.TryGetValue(vocab.GetId(), out var notes) ? notes.ToList() : []);
   }

   public List<SentenceNote> WithVocabForm(string form)
   {
      return _monitor.Read(() => _byVocabForm.TryGetValue(form, out var notes) ? notes.ToList() : []);
   }

   public List<SentenceNote> WithUserHighlightedVocab(string form)
   {
      return _monitor.Read(() => _byUserHighlightedVocab.TryGetValue(form, out var notes) ? notes.ToList() : []);
   }

   public List<SentenceNote> WithUserMarkedInvalidVocab(string form)
   {
      return _monitor.Read(() => _byUserMarkedInvalidVocab.TryGetValue(form, out var notes) ? notes.ToList() : []);
   }

   protected override void InheritorRemoveFromCache(SentenceNote note, SentenceSnapshot snapshot)
   {
      foreach(var vocabForm in snapshot.Words)
      {
         if(_byVocabForm.TryGetValue(vocabForm, out var set))
         {
            set.Remove(note);
         }
      }

      foreach(var vocabForm in snapshot.UserHighlightedVocab)
      {
         if(_byUserHighlightedVocab.TryGetValue(vocabForm, out var set))
         {
            set.Remove(note);
         }
      }

      foreach(var vocabForm in snapshot.MarkedIncorrectVocab)
      {
         if(_byUserMarkedInvalidVocab.TryGetValue(vocabForm, out var set))
         {
            set.Remove(note);
         }
      }

      foreach(var vocabId in snapshot.DetectedVocab)
      {
         if(_byVocabId.TryGetValue(vocabId, out var set))
         {
            set.Remove(note);
         }
      }
   }

   protected override void InheritorAddToCache(SentenceNote note, SentenceSnapshot snapshot)
   {
      foreach(var vocabForm in snapshot.Words)
      {
         if(!_byVocabForm.ContainsKey(vocabForm))
         {
            _byVocabForm[vocabForm] = [];
         }

         _byVocabForm[vocabForm].Add(note);
      }

      foreach(var vocabForm in snapshot.UserHighlightedVocab)
      {
         if(!_byUserHighlightedVocab.ContainsKey(vocabForm))
         {
            _byUserHighlightedVocab[vocabForm] = [];
         }

         _byUserHighlightedVocab[vocabForm].Add(note);
      }

      foreach(var vocabForm in snapshot.MarkedIncorrectVocab)
      {
         if(!_byUserMarkedInvalidVocab.ContainsKey(vocabForm))
         {
            _byUserMarkedInvalidVocab[vocabForm] = [];
         }

         _byUserMarkedInvalidVocab[vocabForm].Add(note);
      }

      foreach(var vocabId in snapshot.DetectedVocab)
      {
         if(!_byVocabId.ContainsKey(vocabId))
         {
            _byVocabId[vocabId] = [];
         }

         _byVocabId[vocabId].Add(note);
      }
   }
}
