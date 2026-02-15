using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteConjugator
{
   readonly VocabNote _vocab;

   public VocabNoteConjugator(VocabNote vocab) => _vocab = vocab;

   VocabNote Vocab => _vocab;

   List<string> GetStemsForForm(string form)
   {
      return Conjugator.GetWordStems(form, _vocab.PartsOfSpeech.IsIchidan(), _vocab.PartsOfSpeech.IsGodan())
                       .Where(stem => stem != form)
                       .ToList();
   }

   public List<string> GetStemsForPrimaryForm() =>
      GetStemsForForm(Vocab.GetQuestion())
        .Distinct()
        .ToList();

   public List<string> GetStemsForAllForms() =>
      Vocab.Forms.AllSet()
           .SelectMany(GetStemsForForm)
           .Distinct()
           .ToList();
}
