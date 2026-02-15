using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

public class Antonyms
{
   readonly VocabNote _vocab;
   readonly RelatedVocabData _data;
   readonly NoteGuard _guard;

   public Antonyms(VocabNote vocab, RelatedVocabData data, NoteGuard guard)
   {
      _vocab = vocab;
      _data = data;
      _guard = guard;
   }

   public HashSet<string> Strings() => _data.Antonyms;

   public List<VocabNote> Notes() => _vocab.Services.Collection.Vocab.WithAnyFormInPreferDisambiguationNameOrExactMatch(Strings().ToList());

   public void Add(string antonym) => _guard.Update(() =>
   {
      Strings().Add(antonym);

      foreach(var similar in _vocab.Services.Collection.Vocab.WithQuestion(antonym))
      {
         if(!similar.RelatedNotes.Antonyms.Strings().Contains(_vocab.GetQuestion()))
         {
            similar.RelatedNotes.Antonyms.Add(_vocab.GetQuestion());
         }
      }
   });

   public void Remove(string toRemove) => _guard.Update(() =>
   {
      Strings().Remove(toRemove);

      foreach(var similar in _vocab.Services.Collection.Vocab.WithQuestion(toRemove))
      {
         if(similar.RelatedNotes.Antonyms.Strings().Contains(_vocab.GetQuestion()))
         {
            similar.RelatedNotes.Antonyms.Remove(_vocab.GetQuestion());
         }
      }
   });

   public override string ToString() => string.Join(", ", Strings());
}
