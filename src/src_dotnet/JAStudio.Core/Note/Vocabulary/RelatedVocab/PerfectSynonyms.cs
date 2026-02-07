using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.NoteFields.AutoSaveWrappers;

namespace JAStudio.Core.Note.Vocabulary.RelatedVocab;

public class PerfectSynonyms
{
    private readonly VocabNote _vocab;
    private readonly FieldSetWrapper<string> _value;

    public PerfectSynonyms(VocabNote vocab, FieldSetWrapper<string> data)
    {
        _vocab = vocab;
        _value = data;
        vocab.User.Answer.OnChange(PushAnswerToOtherSynonyms);
    }

    public List<VocabNote> Notes()
    {
        return _vocab.Services.Collection.Vocab.WithAnyDisambiguationNameIn(_value.Get()).ToList();
    }

    public void PushAnswerToOtherSynonyms()
    {
        foreach (var synonym in Notes())
        {
            synonym.User.Answer.Set(_vocab.GetAnswer());
        }
    }

    public HashSet<string> Get() => _value.Get();

    private void RemoveInternal(string synonym)
    {
        _value.Discard(synonym);
        _vocab.RelatedNotes.Synonyms.Add(synonym);
    }

    private void AddInternal(string synonym)
    {
        if (synonym == _vocab.GetQuestion()) return;
        _value.Add(synonym);
        _vocab.RelatedNotes.Synonyms.Add(synonym);
    }

    private HashSet<VocabNote> ResolveWholeWeb()
    {
        var found = new HashSet<VocabNote>();

        void RecurseInto(VocabNote syn)
        {
            found.Add(syn);
            foreach (var related in syn.RelatedNotes.PerfectSynonyms.Notes())
            {
                if (!found.Contains(related))
                {
                    RecurseInto(related);
                }
            }
        }

        RecurseInto(_vocab);
        foreach (var synonym in Notes())
        {
            RecurseInto(synonym);
        }
        return found;
    }

    private void EnsureAllPerfectSynonymsAreConnected()
    {
        var wholeWeb = ResolveWholeWeb();
        var allQuestions = wholeWeb.Select(syn => syn.GetQuestion()).ToHashSet();

        foreach (var synonym in wholeWeb)
        {
            foreach (var question in allQuestions)
            {
                synonym.RelatedNotes.PerfectSynonyms.AddInternal(question);
            }
        }
    }

    public void AddOverwritingTheAnswerOfTheAddedSynonym(string addedQuestion)
    {
        if (addedQuestion == _vocab.GetQuestion()) return;
        AddInternal(addedQuestion);
        EnsureAllPerfectSynonymsAreConnected();
        PushAnswerToOtherSynonyms();
    }

    public void Remove(string synonymToRemove)
    {
        foreach (var toRemove in _vocab.Services.Collection.Vocab.WithQuestion(synonymToRemove))
        {
            toRemove.RelatedNotes.PerfectSynonyms._value.Clear();
        }
        foreach (var syn in ResolveWholeWeb())
        {
            syn.RelatedNotes.PerfectSynonyms.RemoveInternal(synonymToRemove);
        }
    }

    public override string ToString()
    {
        return _value.ToString();
    }
}
