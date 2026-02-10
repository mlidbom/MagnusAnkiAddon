using JAStudio.Core.LanguageServices;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Vocabulary;

public class VocabNoteConjugator
{
    private readonly VocabNote _vocab;

    public VocabNoteConjugator(VocabNote vocab)
    {
        _vocab = vocab;
    }

    private VocabNote Vocab => _vocab;

    private List<string> GetStemsForForm(string form)
    {
        return Conjugator.GetWordStems(form, _vocab.PartsOfSpeech.IsIchidan(), _vocab.PartsOfSpeech.IsGodan())
            .Where(stem => stem != form)
            .ToList();
    }

    public List<string> GetStemsForPrimaryForm()
    {
        return GetStemsForForm(Vocab.GetQuestion())
            .Distinct()
            .ToList();
    }

    public List<string> GetStemsForAllForms()
    {
        return Vocab.Forms.AllSet()
            .SelectMany(GetStemsForForm)
            .Distinct()
            .ToList();
    }
}
