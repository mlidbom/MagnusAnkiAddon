using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

public class SeeAlso
{
    private readonly VocabNote _vocab;
    private readonly MutableSerializedObjectField<RelatedVocabData> _data;

    public SeeAlso(VocabNote vocab, MutableSerializedObjectField<RelatedVocabData> data)
    {
        _vocab = vocab;
        _data = data;
    }

    public HashSet<string> Strings() => _data.Get().SeeAlso;

    public List<VocabNote> Notes()
    {
        return App.Col().Vocab.WithAnyFormInPreferDisambiguationNameOrExactMatch(Strings().ToList());
    }

    public void Add(string toAdd)
    {
        Strings().Add(toAdd);

        foreach (var addedNote in App.Col().Vocab.WithQuestion(toAdd))
        {
            if (!addedNote.RelatedNotes.SeeAlso.Strings().Contains(_vocab.GetQuestion()))
            {
                addedNote.RelatedNotes.SeeAlso.Add(_vocab.GetQuestion());
            }
        }

        _data.Save();
    }

    public void Remove(string toRemove)
    {
        Strings().Remove(toRemove);

        foreach (var removedNote in App.Col().Vocab.WithQuestion(toRemove))
        {
            if (removedNote.RelatedNotes.SeeAlso.Strings().Contains(_vocab.GetQuestion()))
            {
                removedNote.RelatedNotes.SeeAlso.Remove(_vocab.GetQuestion());
            }
        }

        _data.Save();
    }

    public override string ToString()
    {
        return _data.ToString();
    }
}
