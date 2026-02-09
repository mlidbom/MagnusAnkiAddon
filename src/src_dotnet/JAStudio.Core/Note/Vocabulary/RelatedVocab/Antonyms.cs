using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.ReactiveProperties;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

public class Antonyms
{
    private readonly VocabNote _vocab;
    private readonly SerializedObjectProperty<RelatedVocabData> _data;

    public Antonyms(VocabNote vocab, SerializedObjectProperty<RelatedVocabData> data)
    {
        _vocab = vocab;
        _data = data;
    }

    public HashSet<string> Strings() => _data.Get().Antonyms;

    public List<VocabNote> Notes()
    {
        return _vocab.Services.Collection.Vocab.WithAnyFormInPreferDisambiguationNameOrExactMatch(Strings().ToList());
    }

    public void Add(string antonym)
    {
        Strings().Add(antonym);

        foreach (var similar in _vocab.Services.Collection.Vocab.WithQuestion(antonym))
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

        foreach (var similar in _vocab.Services.Collection.Vocab.WithQuestion(toRemove))
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
