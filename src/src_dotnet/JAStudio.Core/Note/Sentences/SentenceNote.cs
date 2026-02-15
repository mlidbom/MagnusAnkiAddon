using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices;
using JAStudio.Core.LanguageServices.JanomeEx;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;
using JAStudio.Core.Note.CorpusData;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.Storage.Converters;

namespace JAStudio.Core.Note.Sentences;

public class SentenceNote : JPNote
{
    public CachingSentenceConfigurationField Configuration { get; private set; }

    public SentenceUserFields User { get; }

    public WritableStringValue ExternalId { get; }
    public WritableStringValue Reading { get; }
    public WritableStringValue SourceQuestion { get; }
    public WritableStringValue ActiveQuestion { get; }
    public WritableStringValue SourceAnswer { get; }
    public WritableStringValue ActiveAnswer { get; }
    public WritableStringValue SourceComments { get; }
    public WritableStringValue JanomeTokens { get; }
    public WritableImageValue Screenshot { get; }
    public WritableAudioValue Audio { get; }

    ParsingResult _parsingResult;

    public SentenceQuestionField Question => new(User.Question, SourceQuestion);
    public StripHtmlOnReadFallbackStringField Answer => new(User.Answer, SourceAnswer);

    public SentenceNote(NoteServices services, SentenceData? data = null) : base(services, data != null ? new SentenceId(data.Id) : SentenceId.New(), data?.Tags)
    {
        ExternalId = new WritableStringValue(data?.ExternalId ?? string.Empty, Guard);
        Reading = new WritableStringValue(data?.Reading ?? string.Empty, Guard);
        SourceQuestion = new WritableStringValue(data?.SourceQuestion ?? string.Empty, Guard);
        ActiveQuestion = new WritableStringValue(data?.ActiveQuestion ?? string.Empty, Guard);
        SourceAnswer = new WritableStringValue(data?.SourceAnswer ?? string.Empty, Guard);
        ActiveAnswer = new WritableStringValue(data?.ActiveAnswer ?? string.Empty, Guard);
        SourceComments = new WritableStringValue(data?.SourceComments ?? string.Empty, Guard);
        JanomeTokens = new WritableStringValue(data?.JanomeTokens ?? string.Empty, Guard);
        Screenshot = new WritableImageValue(data?.Screenshot ?? string.Empty, Guard);
        Audio = new WritableAudioValue(data?.Audio ?? string.Empty, Guard);

        User = new SentenceUserFields(data, Guard);
        Configuration = new CachingSentenceConfigurationField(this, data?.Configuration, Guard);
        _parsingResult = SentenceData.CreateParsingResult(data?.ParsingResult);
    }

    public override void UpdateInCache()
    {
        Services.Collection.Sentences.Cache.JpNoteUpdated(this);
    }

    public override CorpusDataBase ToCorpusData() => SentenceNoteConverter.ToCorpusData(this);

    public override List<MediaReference> GetMediaReferences()
    {
        var refs = Audio.GetMediaReferences();
        refs.AddRange(Screenshot.GetMediaReferences());
        return refs;
    }

    public override string GetQuestion()
    {
        return Question.WithoutInvisibleSpace();
    }

    public override string GetAnswer()
    {
        return Answer.Get();
    }

    public AnalysisServices AnalysisServices => new(Services.Collection.Vocab, Services.DictLookup, Services.Settings);

    public TextAnalysis CreateAnalysis(bool forUI = false)
    {
        var cachedTokens = JanomeTokens.HasValue() ? JanomeTokens.Value : null;
        return new TextAnalysis(AnalysisServices, Question.WithInvisibleSpace(), Configuration.Configuration, forUI, cachedTokens);
    }

    public ParsingResult GetParsingResult() => _parsingResult;

    public void SetParsingResult(ParsingResult value) => Guard.Update(() => _parsingResult = value);

    public List<string> GetWords()
    {
        var parsedWords = GetParsingResult().ParsedWordsStrings();
        var highlightedWords = Configuration.HighlightedWords;
        var incorrectWords = Configuration.IncorrectMatches.Words();

        var allWords = new HashSet<string>(parsedWords);
        allWords.UnionWith(highlightedWords);
        allWords.ExceptWith(incorrectWords);

        return allWords.Distinct().ToList();
    }

    public override HashSet<JPNote> GetDirectDependencies()
    {
        var dependencies = new HashSet<JPNote>();

        // Add highlighted vocab
        var highlightedVocab = Configuration.HighlightedVocab();
        foreach (var vocab in highlightedVocab)
        {
            dependencies.Add(vocab);
        }

        var parsingResult = GetParsingResult();
        if (parsingResult != null)
        {
            foreach (var match in parsingResult.ParsedWords.Where(p => p.IsDisplayed && p.VocabId != null))
            {
                var vocab = Services.Collection.Vocab.WithIdOrNone(match.VocabId!);
                if (vocab != null)
                {
                    dependencies.Add(vocab);
                }
            }
        }

        // Add kanji
        var kanjiList = ExtractKanji();
        var kanjiNotes = Services.Collection.Kanji.WithAnyKanjiIn(kanjiList);
        foreach (var kanjiNote in kanjiNotes)
        {
            dependencies.Add(kanjiNote);
        }

        return dependencies;
    }

    public override void UpdateGeneratedData()
    {
        base.UpdateGeneratedData();

        UpdateParsedWords();

        ActiveAnswer.Set(GetAnswer());
        ActiveQuestion.Set(GetQuestion());
    }

    public void UpdateParsedWords(bool force = false)
    {
        var parsingResult = GetParsingResult();
        var questionText = Question.WithoutInvisibleSpace();

        if (!force && parsingResult != null &&
            parsingResult.Sentence == questionText &&
            parsingResult.ParserVersion == TextAnalysis.Version)
        {
            return;
        }

        // Invalidate cached janome tokens if the sentence text has changed
        if (parsingResult == null || parsingResult.Sentence != questionText)
        {
            JanomeTokens.Empty();
        }

        var analysis = CreateAnalysis();
        JanomeTokens.Set(analysis.SerializedJanomeTokens);
        SetParsingResult(Sentences.ParsingResult.FromAnalysis(analysis));
    }

    public List<string> ExtractKanji()
    {
        var clean = StringExtensions.StripHtmlMarkup(Question.WithoutInvisibleSpace());
        return clean.Where(KanaUtils.CharacterIsKanji)
            .Select(c => c.ToString())
            .ToList();
    }

    public static SentenceNote CreateTestNote(NoteServices services, string question, string answer)
    {
        var note = new SentenceNote(services);
        note.SourceQuestion.Set(question);
        note.User.Answer.Set(answer);
        note.UpdateGeneratedData();
        services.Collection.Sentences.Add(note);
        return note;
    }

    public static SentenceNote AddSentence(
        NoteServices services,
        string question,
        string answer,
        string audio = "",
        string screenshot = "",
        HashSet<string>? highlightedVocab = null,
        HashSet<Tag>? tags = null)
    {
        var note = new SentenceNote(services);
        note.SourceQuestion.Set(question);
        note.SourceAnswer.Set(answer);
        note.Screenshot.SetRawValue(screenshot);
        note.UpdateGeneratedData();

        if(string.IsNullOrWhiteSpace(audio))
        {
            note.Tags.Set(Note.Tags.TTSAudio);
        }
        else
        {
            note.Audio.SetRawValue(audio.Trim());
        }

        if(highlightedVocab != null)
        {
            foreach(var vocab in highlightedVocab)
            {
                note.Configuration.AddHighlightedWord(vocab);
            }
        }

        if(tags != null)
        {
            foreach(var tag in tags)
            {
                note.Tags.Set(tag);
            }
        }

        services.Collection.Sentences.Add(note);
        return note;
    }

    public static SentenceNote Create(NoteServices services, string question)
    {
        var note = new SentenceNote(services);
        note.SourceQuestion.Set(question);
        note.UpdateGeneratedData();
        services.Collection.Sentences.Add(note);
        return note;
    }
}
