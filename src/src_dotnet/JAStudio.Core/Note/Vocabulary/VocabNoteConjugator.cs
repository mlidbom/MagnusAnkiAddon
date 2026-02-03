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
        // TODO: Implement when conjugator service is ported
        // return conjugator.get_word_stems(form, is_ichidan_verb=vocab.parts_of_speech.is_ichidan(), is_godan=vocab.parts_of_speech.is_godan())
        //     .where(stem => stem != form)
        //     .to_list();
        
        return new List<string>();
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
