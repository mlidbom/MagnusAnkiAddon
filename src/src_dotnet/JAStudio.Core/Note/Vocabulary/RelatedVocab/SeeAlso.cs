using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

public class SeeAlso
{
   readonly VocabNote _vocab;
   readonly RelatedVocabData _data;
   readonly NoteGuard _guard;

   public SeeAlso(VocabNote vocab, RelatedVocabData data, NoteGuard guard)
   {
      _vocab = vocab;
      _data = data;
      _guard = guard;
   }

   public HashSet<string> Strings() => _data.SeeAlso;

   public List<VocabNote> Notes() => _vocab.Services.Collection.Vocab.WithAnyFormInPreferDisambiguationNameOrExactMatch(Strings().ToList());

   public void Add(string toAdd) => _guard.Update(() =>
   {
      Strings().Add(toAdd);

      foreach(var addedNote in _vocab.Services.Collection.Vocab.WithQuestion(toAdd))
      {
         if(!addedNote.RelatedNotes.SeeAlso.Strings().Contains(_vocab.GetQuestion()))
         {
            addedNote.RelatedNotes.SeeAlso.Add(_vocab.GetQuestion());
         }
      }
   });

   public void Remove(string toRemove) => _guard.Update(() =>
   {
      Strings().Remove(toRemove);

      foreach(var removedNote in _vocab.Services.Collection.Vocab.WithQuestion(toRemove))
      {
         if(removedNote.RelatedNotes.SeeAlso.Strings().Contains(_vocab.GetQuestion()))
         {
            removedNote.RelatedNotes.SeeAlso.Remove(_vocab.GetQuestion());
         }
      }
   });

   public override string ToString() => string.Join(", ", Strings());
}
