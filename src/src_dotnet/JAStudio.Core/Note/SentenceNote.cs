using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.Sentences;
using System.Collections.Generic;
using System.Linq;

namespace JAStudio.Core.Note;

public class SentenceNote : JPNote
{
    public SentenceConfiguration Configuration { get; private set; }
    public SerializedObjectField<ParsingResult> ParsingResult { get; }

    public SentenceNote(JPNoteData? data = null) : base(data)
    {
        Configuration = SentenceConfiguration.Empty();
        ParsingResult = new SerializedObjectField<ParsingResult>(
            this,
            NoteFieldsConstants.Sentence.ParsingResult,
            new ParsingResultSerializer());
    }

    public override void UpdateInCache()
    {
        App.Col().Sentences.Cache.JpNoteUpdated(this);
    }

    public override string GetQuestion()
    {
        var userQuestion = GetField(NoteFieldsConstants.Sentence.UserQuestion);
        var sourceQuestion = GetField(NoteFieldsConstants.Sentence.SourceQuestion);
        var question = !string.IsNullOrEmpty(userQuestion) ? userQuestion : sourceQuestion;
        return question.Replace(StringExtensions.InvisibleSpace, string.Empty);
    }

    public override string GetAnswer()
    {
        var userAnswer = GetField(NoteFieldsConstants.Sentence.UserAnswer);
        var sourceAnswer = GetField(NoteFieldsConstants.Sentence.SourceAnswer);
        var answer = !string.IsNullOrEmpty(userAnswer) ? userAnswer : sourceAnswer;
        return StringExtensions.StripHtmlMarkup(answer);
    }

    public List<string> GetWords()
    {
        var parsedWords = ParsingResult.Get().ParsedWordsStrings();
        var highlightedWords = Configuration.HighlightedWords;
        var incorrectWords = Configuration.IncorrectMatches.Words();

        var allWords = new HashSet<string>(parsedWords);
        allWords.UnionWith(highlightedWords);
        allWords.ExceptWith(incorrectWords);

        return allWords.ToList();
    }

    public override HashSet<JPNote> GetDirectDependencies()
    {
        var dependencies = new HashSet<JPNote>();

        // Add highlighted vocab
        foreach (var word in Configuration.HighlightedWords)
        {
            var vocabNotes = App.Col().Vocab.Cache.WithQuestion(word);
            foreach (var vocab in vocabNotes)
            {
                dependencies.Add(vocab);
            }
        }

        // Add displayed parsed words
        foreach (var match in ParsingResult.Get().ParsedWords.Where(p => p.IsDisplayed && p.VocabId != -1))
        {
            var vocab = App.Col().Vocab.WithIdOrNone(match.VocabId);
            if (vocab != null)
            {
                dependencies.Add(vocab);
            }
        }

        // Add kanji
        var kanji = ExtractKanji();
        foreach (var kanjiChar in kanji)
        {
            var kanjiNote = App.Col().Kanji.WithKanji(kanjiChar);
            if (kanjiNote != null)
            {
                dependencies.Add(kanjiNote);
            }
        }

        return dependencies;
    }

    public override void UpdateGeneratedData()
    {
        base.UpdateGeneratedData();
        
        // TODO: UpdateParsedWords when text analysis is available
        
        SetField(NoteFieldsConstants.Sentence.ActiveAnswer, GetAnswer());
        SetField(NoteFieldsConstants.Sentence.ActiveQuestion, GetQuestion());
    }

    public List<string> ExtractKanji()
    {
        var clean = StringExtensions.StripHtmlMarkup(GetQuestion());
        // TODO: Implement character_is_kanji when KanaUtils is ported
        return new List<string>();
    }

    public static SentenceNote CreateTestNote(string question, string answer)
    {
        var note = new SentenceNote();
        note.SetField(NoteFieldsConstants.Sentence.SourceQuestion, question);
        note.SetField(NoteFieldsConstants.Sentence.UserAnswer, answer);
        note.UpdateGeneratedData();
        App.Col().Sentences.Add(note);
        return note;
    }
}

// Placeholder serializer
public class ParsingResultSerializer : IObjectSerializer<ParsingResult>
{
    public string Serialize(ParsingResult instance)
    {
        // TODO: Implement JSON serialization
        return string.Empty;
    }

    public ParsingResult Deserialize(string serialized)
    {
        if (string.IsNullOrEmpty(serialized))
        {
            return ParsingResult.Empty();
        }
        // TODO: Implement JSON deserialization
        return ParsingResult.Empty();
    }
}
