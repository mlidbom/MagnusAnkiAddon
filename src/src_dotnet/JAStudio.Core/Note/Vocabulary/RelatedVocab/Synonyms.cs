using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.NoteFields;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

public class Synonyms
{
    private readonly VocabNote _vocab;
    private readonly MutableSerializedObjectField<RelatedVocabData> _data;

    public Synonyms(VocabNote vocab, MutableSerializedObjectField<RelatedVocabData> data)
    {
        _vocab = vocab;
        _data = data;
    }

    public HashSet<string> Strings() => _data.Get().Synonyms;

    private void Save()
    {
        Strings().Remove(_vocab.GetQuestion()); // todo: this is cleanup after a bug. Remove soon
        _data.Save();
    }

    public List<VocabNote> Notes()
    {
        return App.Col().Vocab.WithAnyFormInPreferDisambiguationNameOrExactMatch(Strings().ToList());
    }

    public void Add(string synonym)
    {
        if (synonym == _vocab.GetQuestion()) return;
        Strings().Add(synonym);

        foreach (var similar in App.Col().Vocab.WithQuestion(synonym).ToList())
        {
            if (!similar.RelatedNotes.Synonyms.Strings().Contains(_vocab.GetQuestion()))
            {
                similar.RelatedNotes.Synonyms.Add(_vocab.GetQuestion());
            }
        }

        Save();
    }

    public void AddTransitivelyOneLevel(string synonym)
    {
        var newSynonymNotes = App.Col().Vocab.WithAnyFormInPreferDisambiguationNameOrExactMatch(new List<string> { synonym });

        foreach (var synonymNote in newSynonymNotes)
        {
            foreach (var mySynonym in Strings())
            {
                synonymNote.RelatedNotes.Synonyms.Add(mySynonym);
            }
        }

        var synonymsOfNewSynonymStrings = newSynonymNotes
            .SelectMany<VocabNote, string>(newSynonymNote => newSynonymNote.RelatedNotes.Synonyms.Strings())
            .Concat(newSynonymNotes.Select(newSynonymNote => newSynonymNote.GetQuestion()))
            .ToHashSet();

        foreach (var newSynonym in synonymsOfNewSynonymStrings)
        {
            Add(newSynonym);
        }
    }

    public void Remove(string toRemove)
    {
        Strings().Remove(toRemove);

        foreach (var similar in App.Col().Vocab.WithQuestion(toRemove))
        {
            if (similar.RelatedNotes.Synonyms.Strings().Contains(_vocab.GetQuestion()))
            {
                similar.RelatedNotes.Synonyms.Remove(_vocab.GetQuestion());
            }
        }

        Save();
    }
}
