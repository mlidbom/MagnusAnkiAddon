using JAStudio.Core.LanguageServices.JanomeEx;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;
using JAStudio.Core.Note.ReactiveProperties;
using JAStudio.Core.Note.Sentences;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices;
using JAStudio.Core.Note.Sentences.Serialization;

namespace JAStudio.Core.Note;

public class SentenceNote : JPNote
{
    readonly PropertyBag _properties = new();

    // Stored fields
    public CachingSentenceConfigurationField Configuration { get; private set; }
    public SerializedObjectProperty<ParsingResult> ParsingResult { get; }

    // String properties (registered in PropertyBag, backed by Anki field dictionary)
    public StringProperty Id { get; }
    public StringProperty Reading { get; }
    public StringProperty SourceQuestion { get; }
    public StringProperty ActiveQuestion { get; }
    public StringProperty SourceComments { get; }
    public StringProperty JanomeTokens { get; }
    public StringProperty Screenshot { get; }

    // User fields
    public SentenceUserProperties User { get; }

    // Composite properties
    public SentenceQuestionProperty Question { get; }
    public FallbackHtmlStrippedProperty Answer { get; }
    public AudioProperty Audio { get; }

    // Private string properties
    StringProperty SourceAnswer { get; }
    StringProperty ActiveAnswerField { get; }

    public SentenceNote(NoteServices services, NoteData? data = null) : base(services, data?.Id != null ? new SentenceId(data.Id.Value) : SentenceId.New(), data)
    {
        // Register all string fields in the PropertyBag
        Id = _properties.String(SentenceNoteFields.Id);
        Reading = _properties.String(SentenceNoteFields.Reading);
        SourceQuestion = _properties.String(SentenceNoteFields.SourceQuestion);
        ActiveQuestion = _properties.String(SentenceNoteFields.ActiveQuestion);
        SourceAnswer = _properties.String(SentenceNoteFields.SourceAnswer);
        ActiveAnswerField = _properties.String(SentenceNoteFields.ActiveAnswer);
        SourceComments = _properties.String(SentenceNoteFields.SourceComments);
        JanomeTokens = _properties.String(SentenceNoteFields.JanomeTokens);
        Screenshot = _properties.String(SentenceNoteFields.Screenshot);

        var userComments = _properties.String(SentenceNoteFields.UserComments);
        var userAnswer = _properties.String(SentenceNoteFields.UserAnswer);
        var userQuestion = _properties.String(SentenceNoteFields.UserQuestion);
        User = new SentenceUserProperties(userComments, userAnswer, userQuestion);

        var audioField = _properties.String(SentenceNoteFields.Audio);
        Audio = new AudioProperty(audioField);

        var parsingResultField = _properties.String(SentenceNoteFields.ParsingResult);

        // Load all registered properties from the Anki field dictionary
        _properties.LoadFromDictionary(data?.Fields);

        // Initialize complex sub-objects after loading
        var configField = _properties.String(SentenceNoteFields.Configuration);
        configField.SetSilently(data?.Fields != null && data.Fields.TryGetValue(SentenceNoteFields.Configuration, out var configValue) ? configValue : "");
        Configuration = new CachingSentenceConfigurationField(this, configField);

        ParsingResult = new SerializedObjectProperty<ParsingResult>(parsingResultField, new ParsingResultSerializer());

        // Composite read-only properties
        Question = new SentenceQuestionProperty(userQuestion, SourceQuestion);
        Answer = new FallbackHtmlStrippedProperty(userAnswer, SourceAnswer);

        // Wire up PropertyBag changes to JPNote's Flush mechanism
        _properties.AnyChanged.Subscribe(() => Flush());
    }

    public override NoteData GetData() => new(GetId(), _properties.ToDictionary(), Tags.ToInternedStringList());

    public override void UpdateInCache()
    {
        Services.Collection.Sentences.Cache.JpNoteUpdated(this);
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

    public List<string> GetWords()
    {
        var parsedWords = ParsingResult.Get().ParsedWordsStrings();
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

        // Add displayed parsed words
        var parsingResult = ParsingResult.Get();
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

        ActiveAnswerField.Set(GetAnswer());
        ActiveQuestion.Set(GetQuestion());
    }

    public void UpdateParsedWords(bool force = false)
    {
        var parsingResult = ParsingResult.Get();
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
        ParsingResult.Set(Sentences.ParsingResult.FromAnalysis(analysis));
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
        note.Screenshot.Set(screenshot);
        note.UpdateGeneratedData();

        if (string.IsNullOrWhiteSpace(audio))
        {
            note.Tags.Set(Note.Tags.TTSAudio);
        }
        else
        {
            note.Audio.SetRawValue(audio.Trim());
        }

        if (highlightedVocab != null)
        {
            foreach (var vocab in highlightedVocab)
            {
                note.Configuration.AddHighlightedWord(vocab);
            }
        }

        if (tags != null)
        {
            foreach (var tag in tags)
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
