using System;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note.Vocabulary;

public class SentenceCounts
{
    private readonly Func<VocabNoteSentences> _parent;
    private int _studyingReading;
    private int _studyingListening;
    private int _total;
    private DateTime _lastUpdateTime;
    private int _cacheSeconds;

    public SentenceCounts(Func<VocabNoteSentences> parent)
    {
        _parent = parent;
        _studyingReading = 0;
        _studyingListening = 0;
        _total = 0;
        _lastUpdateTime = DateTime.MinValue;
        _cacheSeconds = 0;
    }

    public int Total => UpToDateSelf()._total;
    public int StudyingReading => UpToDateSelf()._studyingReading;
    public int StudyingListening => UpToDateSelf()._studyingListening;

    private SentenceCounts UpToDateSelf()
    {
        int HowLongToCacheFor()
        {
            if (_total < 10) return 60;
            if (_total < 100) return 600;
            return 6000;
        }

        int GetStudyingSentenceCount(string card = "")
        {
            // TODO: Implement when SentenceNote.IsStudying is ported
            return 0; // _parent().All().Count(it => it.IsStudying(card));
        }

        if ((DateTime.Now - _lastUpdateTime).TotalSeconds > _cacheSeconds)
        {
            _lastUpdateTime = DateTime.Now;
            var sentences = _parent().WithOwnedForm();
            _studyingReading = GetStudyingSentenceCount("Reading"); // TODO: Use NoteFields constant
            _studyingListening = GetStudyingSentenceCount("Listening"); // TODO: Use NoteFields constant
            _total = sentences.Count;
            _cacheSeconds = HowLongToCacheFor();
        }
        return this;
    }
}

public class VocabNoteSentences
{
    private readonly Func<VocabNote> _vocab;
    private SentenceCounts? _counts;

    public VocabNoteSentences(Func<VocabNote> vocab)
    {
        _vocab = vocab;
    }

    private VocabNote Vocab => _vocab();

    public SentenceCounts Counts()
    {
        _counts ??= new SentenceCounts(() => this);
        return _counts;
    }

    public List<SentenceNote> Studying()
    {
        // TODO: Implement when SentenceNote.IsStudying is ported
        return All(); // All().Where(it => it.IsStudying()).ToList();
    }

    public List<SentenceNote> All()
    {
        return App.Col().Sentences.WithVocab(Vocab);
    }

    public List<SentenceNote> InvalidIn()
    {
        // TODO: Implement when WithVocabMarkedInvalid is ported
        return new List<SentenceNote>();
    }

    public List<SentenceNote> WithOwnedForm()
    {
        // TODO: Implement when WithVocabOwnedForm is ported
        return new List<SentenceNote>();
    }

    public List<SentenceNote> WithPrimaryForm()
    {
        return App.Col().Sentences.WithForm(Vocab.GetQuestion());
    }

    public List<SentenceNote> UserHighlighted()
    {
        return App.Col().Sentences.WithUserHighlightedVocab(Vocab.GetQuestion());
    }
}
