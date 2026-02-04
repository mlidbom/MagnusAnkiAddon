using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;
using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.Sentences;
using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note.Sentences.Serialization;
using JAStudio.Core.SysUtils;

namespace JAStudio.Core.Note;

public class SentenceNote : JPNote
{
    public CachingSentenceConfigurationField Configuration { get; private set; }
    public MutableSerializedObjectField<ParsingResult> ParsingResult { get; }

    public SentenceNote(JPNoteData? data = null) : base(data)
    {
        Configuration = new CachingSentenceConfigurationField(this);
        ParsingResult = new MutableSerializedObjectField<ParsingResult>(
            this,
            NoteFieldsConstants.Sentence.ParsingResult,
            new ParsingResultSerializer());
    }

    public override void UpdateInCache()
    {
        App.Col().Sentences.Cache.JpNoteUpdated(this);
    }

    // Property accessors
    public MutableStringField Id => new(this, NoteFieldsConstants.Sentence.Id);
    public MutableStringField Reading => new(this, NoteFieldsConstants.Sentence.Reading);
    public SentenceUserFields User => new(this);
    public MutableStringField SourceQuestion => new(this, NoteFieldsConstants.Sentence.SourceQuestion);
    public MutableStringField ActiveQuestion => new(this, NoteFieldsConstants.Sentence.ActiveQuestion);
    public SentenceQuestionField Question => new(User.Question, SourceQuestion);
    public StripHtmlOnReadFallbackStringField Answer => new(User.Answer, SourceAnswer);
    private MutableStringField SourceAnswer => new(this, NoteFieldsConstants.Sentence.SourceAnswer);
    public MutableStringField ActiveAnswer => new(this, NoteFieldsConstants.Sentence.ActiveAnswer);
    public MutableStringField SourceComments => new(this, NoteFieldsConstants.Sentence.SourceComments);
    private MutableStringField Screenshot => new(this, NoteFieldsConstants.Sentence.Screenshot);
    public WritableAudioField Audio => new(this, NoteFieldsConstants.Sentence.Audio);

    public override string GetQuestion()
    {
        return Question.WithoutInvisibleSpace();
    }

    public override string GetAnswer()
    {
        return Answer.Get();
    }

    public TextAnalysis CreateAnalysis(bool forUI = false)
    {
        return new TextAnalysis(Question.WithInvisibleSpace(), Configuration.Configuration, forUI);
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
                var vocab = App.Col().Vocab.WithIdOrNone(match.VocabId);
                if (vocab != null)
                {
                    dependencies.Add(vocab);
                }
            }
        }

        // Add kanji
        var kanjiList = ExtractKanji();
        var kanjiNotes = App.Col().Kanji.WithAnyKanjiIn(kanjiList);
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
        
        SetField(NoteFieldsConstants.Sentence.ActiveAnswer, GetAnswer());
        SetField(NoteFieldsConstants.Sentence.ActiveQuestion, GetQuestion());
    }

    public void UpdateParsedWords(bool force = false)
    {
        var parsingResult = ParsingResult.Get();
        var questionText = GetQuestion();
        
        // TODO: Implement TextAnalysis.Version when ported
        if (!force && parsingResult != null && 
            parsingResult.Sentence == questionText &&
            parsingResult.ParserVersion == "1.0")  // Placeholder version
        {
            return;
        }

        // TODO: Implement CreateAnalysis when TextAnalysis is ported
        // var analysis = CreateAnalysis();
        // ParsingResult.Set(ParsingResult.FromAnalysis(analysis));
        throw new System.NotImplementedException("UpdateParsedWords requires TextAnalysis to be ported");
    }

    public List<string> ExtractKanji()
    {
        var clean = StringExtensions.StripHtmlMarkup(Question.WithoutInvisibleSpace());
        return clean.Where(KanaUtils.CharacterIsKanji)
            .Select(c => c.ToString())
            .ToList();
    }

    public static SentenceNote CreateTestNote(string question, string answer)
    {
        var note = new SentenceNote();
        note.SourceQuestion.Set(question);
        note.User.Answer.Set(answer);
        note.UpdateGeneratedData();
        App.Col().Sentences.Add(note);
        return note;
    }

    public static SentenceNote AddSentence(
        string question,
        string answer,
        string audio = "",
        string screenshot = "",
        HashSet<string>? highlightedVocab = null,
        HashSet<Tag>? tags = null)
    {
        var note = new SentenceNote();
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

        App.Col().Sentences.Add(note);
        return note;
    }

    public static SentenceNote Create(string question)
    {
        var note = new SentenceNote();
        note.SourceQuestion.Set(question);
        note.UpdateGeneratedData();
        App.Col().Sentences.Add(note);
        return note;
    }
}
