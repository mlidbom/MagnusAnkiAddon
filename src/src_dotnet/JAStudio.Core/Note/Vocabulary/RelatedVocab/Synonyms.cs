using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

public class Synonyms
{
   readonly VocabNote _vocab;
   readonly RelatedVocabData _data;
   readonly NoteGuard _guard;

   public Synonyms(VocabNote vocab, RelatedVocabData data, NoteGuard guard)
   {
      _vocab = vocab;
      _data = data;
      _guard = guard;
   }

   public HashSet<string> Strings() => _data.Synonyms;

   void Save() => _guard.Update(() => Strings().Remove(_vocab.GetQuestion()));

   public List<VocabNote> Notes() => _vocab.Services.Collection.Vocab.WithAnyFormInPreferDisambiguationNameOrExactMatch(Strings().ToList());

   public void Add(string synonym)
   {
      if(synonym == _vocab.GetQuestion()) return;
      Strings().Add(synonym);

      foreach(var similar in _vocab.Services.Collection.Vocab.WithQuestion(synonym).ToList())
      {
         if(!similar.RelatedNotes.Synonyms.Strings().Contains(_vocab.GetQuestion()))
         {
            similar.RelatedNotes.Synonyms.Add(_vocab.GetQuestion());
         }
      }

      Save();
   }

   public void AddTransitivelyOneLevel(string synonym)
   {
      var newSynonymNotes = _vocab.Services.Collection.Vocab.WithAnyFormInPreferDisambiguationNameOrExactMatch([synonym]);

      foreach(var synonymNote in newSynonymNotes)
      {
         foreach(var mySynonym in Strings())
         {
            synonymNote.RelatedNotes.Synonyms.Add(mySynonym);
         }
      }

      var synonymsOfNewSynonymStrings = newSynonymNotes
                                       .SelectMany<VocabNote, string>(newSynonymNote => newSynonymNote.RelatedNotes.Synonyms.Strings())
                                       .Concat(newSynonymNotes.Select(newSynonymNote => newSynonymNote.GetQuestion()))
                                       .ToHashSet();

      foreach(var newSynonym in synonymsOfNewSynonymStrings)
      {
         Add(newSynonym);
      }
   }

   public void Remove(string toRemove)
   {
      Strings().Remove(toRemove);

      foreach(var similar in _vocab.Services.Collection.Vocab.WithQuestion(toRemove))
      {
         if(similar.RelatedNotes.Synonyms.Strings().Contains(_vocab.GetQuestion()))
         {
            similar.RelatedNotes.Synonyms.Remove(_vocab.GetQuestion());
         }
      }

      Save();
   }
}
