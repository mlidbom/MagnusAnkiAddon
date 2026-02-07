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
            return _parent().All().Count(it => it.IsStudying(card));
        }

        if ((DateTime.Now - _lastUpdateTime).TotalSeconds > _cacheSeconds)
        {
            _lastUpdateTime = DateTime.Now;
            var sentences = _parent().WithOwnedForm();
            _studyingReading = GetStudyingSentenceCount(NoteFieldsConstants.VocabNoteType.Card.Reading);
            _studyingListening = GetStudyingSentenceCount(NoteFieldsConstants.VocabNoteType.Card.Listening);
            _total = sentences.Count;
            _cacheSeconds = HowLongToCacheFor();
        }
        return this;
    }
}

public class VocabNoteSentences
{
    private readonly VocabNote _vocab;
    private SentenceCounts? _counts;

    public VocabNoteSentences(VocabNote vocab)
    {
        _vocab = vocab;
    }

    private VocabNote Vocab => _vocab;

    public SentenceCounts Counts()
    {
        _counts ??= new SentenceCounts(() => this);
        return _counts;
    }

    public List<SentenceNote> Studying()
    {
        return All().Where(it => it.IsStudying()).ToList();
    }

    public List<SentenceNote> All()
    {
        return Vocab.Services.Collection.Sentences.WithVocab(Vocab);
    }

    public List<SentenceNote> InvalidIn()
    {
        return Vocab.Services.Collection.Sentences.WithVocabMarkedInvalid(Vocab);
    }

    public List<SentenceNote> WithOwnedForm()
    {
        return Vocab.Services.Collection.Sentences.WithVocabOwnedForm(Vocab);
    }

    public List<SentenceNote> WithPrimaryForm()
    {
        return Vocab.Services.Collection.Sentences.WithForm(Vocab.GetQuestion());
    }

    public List<SentenceNote> UserHighlighted()
    {
        return Vocab.Services.Collection.Sentences.WithUserHighlightedVocab(Vocab.GetQuestion());
    }
}
