using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

public class Antonyms
{
    private readonly VocabNote _vocab;
    private readonly MutableSerializedObjectField<RelatedVocabData> _data;

    public Antonyms(VocabNote vocab, MutableSerializedObjectField<RelatedVocabData> data)
    {
        _vocab = vocab;
        _data = data;
    }

    public HashSet<string> Strings() => _data.Get().Antonyms;

    public List<VocabNote> Notes()
    {
        return TemporaryServiceCollection.Instance.App.Col().Vocab.WithAnyFormInPreferDisambiguationNameOrExactMatch(Strings().ToList());
    }

    public void Add(string antonym)
    {
        Strings().Add(antonym);

        foreach (var similar in TemporaryServiceCollection.Instance.App.Col().Vocab.WithQuestion(antonym))
        {
            if (!similar.RelatedNotes.Antonyms.Strings().Contains(_vocab.GetQuestion()))
            {
                similar.RelatedNotes.Antonyms.Add(_vocab.GetQuestion());
            }
        }

        _data.Save();
    }

    public void Remove(string toRemove)
    {
        Strings().Remove(toRemove);

        foreach (var similar in TemporaryServiceCollection.Instance.App.Col().Vocab.WithQuestion(toRemove))
        {
            if (similar.RelatedNotes.Antonyms.Strings().Contains(_vocab.GetQuestion()))
            {
                similar.RelatedNotes.Antonyms.Remove(_vocab.GetQuestion());
            }
        }

        _data.Save();
    }

    public override string ToString()
    {
        return _data.ToString();
    }
}
