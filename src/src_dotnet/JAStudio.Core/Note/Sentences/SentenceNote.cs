using JAStudio.Core.LanguageServices.JanomeEx;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.Sentences;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.LanguageServices;
using JAStudio.Core.Note.Sentences.Serialization;

namespace JAStudio.Core.Note;

public class SentenceNote : JPNote
{
    public CachingSentenceConfigurationField Configuration { get; private set; }
    public MutableSerializedObjectField<ParsingResult> ParsingResult { get; }

    public SentenceNote(NoteServices services, NoteData? data = null) : base(services, data)
    {
        Configuration = new CachingSentenceConfigurationField(this);
        ParsingResult = new MutableSerializedObjectField<ParsingResult>(
            this,
            SentenceNoteFields.ParsingResult,
            new ParsingResultSerializer());
    }

    public override void UpdateInCache()
    {
        Services.Collection.Sentences.Cache.JpNoteUpdated(this);
    }

    // Property accessors
    public MutableStringField Id => new(this, SentenceNoteFields.Id);
    public MutableStringField Reading => new(this, SentenceNoteFields.Reading);
    public SentenceUserFields User => new(this);
    public MutableStringField SourceQuestion => new(this, SentenceNoteFields.SourceQuestion);
    public MutableStringField ActiveQuestion => new(this, SentenceNoteFields.ActiveQuestion);
    public SentenceQuestionField Question => new(User.Question, SourceQuestion);
    public StripHtmlOnReadFallbackStringField Answer => new(User.Answer, SourceAnswer);
    private MutableStringField SourceAnswer => new(this, SentenceNoteFields.SourceAnswer);
    public MutableStringField ActiveAnswer => new(this, SentenceNoteFields.ActiveAnswer);
    public MutableStringField SourceComments => new(this, SentenceNoteFields.SourceComments);
    private MutableStringField Screenshot => new(this, SentenceNoteFields.Screenshot);
    public WritableAudioField Audio => new(this, SentenceNoteFields.Audio);

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
        return new TextAnalysis(AnalysisServices, Question.WithInvisibleSpace(), Configuration.Configuration, forUI);
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
            foreach (var match in parsingResult.ParsedWords.Where(p => p.IsDisplayed && p.VocabId != -1))
            {
                var vocab = Services.Collection.Vocab.WithIdOrNone(match.VocabId);
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
        
        SetField(SentenceNoteFields.ActiveAnswer, GetAnswer());
        SetField(SentenceNoteFields.ActiveQuestion, GetQuestion());
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

        var analysis = CreateAnalysis();
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
