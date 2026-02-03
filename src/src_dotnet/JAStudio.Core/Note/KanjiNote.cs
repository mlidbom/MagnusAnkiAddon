using JAStudio.Core.Note.NoteFields;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace JAStudio.Core.Note;

public class KanjiNote : JPNote
{
    private static readonly Regex PrimaryReadingPattern = new(@"<primary>(.*?)</primary>", RegexOptions.Compiled);

    public KanjiNote(JPNoteData? data = null) : base(data)
    {
    }

    public override HashSet<JPNote> GetDirectDependencies()
    {
        return GetRadicalsNotes().Cast<JPNote>().ToHashSet();
    }

    public override void UpdateInCache()
    {
        App.Col().Kanji.Cache.JpNoteUpdated(this);
    }

    public override string GetQuestion()
    {
        return GetField(NoteFieldsConstants.Kanji.Question);
    }

    public void SetQuestion(string value)
    {
        SetField(NoteFieldsConstants.Kanji.Question, value);
    }

    public override string GetAnswer()
    {
        var userAnswer = GetUserAnswer();
        return !string.IsNullOrEmpty(userAnswer) ? userAnswer : GetField(NoteFieldsConstants.Kanji.SourceAnswer);
    }

    public string GetAnswerText()
    {
        // TODO: Implement StripHtmlMarkup when needed
        return GetAnswer();
    }

    public string GetUserAnswer()
    {
        return GetField(NoteFieldsConstants.Kanji.UserAnswer);
    }

    public void SetUserAnswer(string value)
    {
        SetField(NoteFieldsConstants.Kanji.UserAnswer, value);
    }

    public override void UpdateGeneratedData()
    {
        base.UpdateGeneratedData();

        // TODO: Implement katakana_to_hiragana when needed
        SetReadingOn(GetReadingOnHtml());

        void UpdatePrimaryAudios()
        {
            // TODO: Implement when vocab system is complete
            SetPrimaryVocabAudio(string.Empty);
        }

        SetField(NoteFieldsConstants.Kanji.ActiveAnswer, GetAnswer());
        UpdatePrimaryAudios();
    }

    public List<string> GetReadingsOn()
    {
        // TODO: Implement StripHtmlMarkup and ExtractCommaSeparatedValues
        return new List<string>();
    }

    public List<string> GetReadingOnListHtml()
    {
        // TODO: Implement ExtractCommaSeparatedValues
        return new List<string>();
    }

    public List<string> GetReadingsKun()
    {
        // TODO: Implement StripHtmlMarkup and ExtractCommaSeparatedValues
        return new List<string>();
    }

    public List<string> GetReadingKunListHtml()
    {
        // TODO: Implement ExtractCommaSeparatedValues
        return new List<string>();
    }

    public List<string> GetReadingNanListHtml()
    {
        // TODO: Implement ExtractCommaSeparatedValues
        return new List<string>();
    }

    public List<string> GetReadingsClean()
    {
        var allReadings = new List<string>();
        allReadings.AddRange(GetReadingOnListHtml());
        allReadings.AddRange(GetReadingKunListHtml());
        allReadings.AddRange(GetReadingNanListHtml());
        // TODO: Implement StripHtmlMarkup on each reading
        return allReadings;
    }

    public string GetReadingOnHtml()
    {
        return GetField(NoteFieldsConstants.Kanji.ReadingOn);
    }

    public void SetReadingOn(string value)
    {
        SetField(NoteFieldsConstants.Kanji.ReadingOn, value);
    }

    public List<string> GetPrimaryReadings()
    {
        var readings = new List<string>();
        readings.AddRange(GetPrimaryReadingsOn());
        readings.AddRange(GetPrimaryReadingsKun());
        readings.AddRange(GetPrimaryReadingsNan());
        return readings;
    }

    public List<string> GetPrimaryReadingsOn()
    {
        var matches = PrimaryReadingPattern.Matches(GetReadingOnHtml());
        // TODO: Implement StripHtmlMarkup
        return matches.Select(m => m.Groups[1].Value).ToList();
    }

    public List<string> GetPrimaryReadingsKun()
    {
        var matches = PrimaryReadingPattern.Matches(GetReadingKunHtml());
        // TODO: Implement StripHtmlMarkup
        return matches.Select(m => m.Groups[1].Value).ToList();
    }

    public List<string> GetPrimaryReadingsNan()
    {
        var matches = PrimaryReadingPattern.Matches(GetReadingNanHtml());
        // TODO: Implement StripHtmlMarkup
        return matches.Select(m => m.Groups[1].Value).ToList();
    }

    public string GetReadingKunHtml()
    {
        return GetField(NoteFieldsConstants.Kanji.ReadingKun);
    }

    public void SetReadingKun(string value)
    {
        SetField(NoteFieldsConstants.Kanji.ReadingKun, value);
    }

    public string GetReadingNanHtml()
    {
        return GetField(NoteFieldsConstants.Kanji.ReadingNan);
    }

    public void AddPrimaryOnReading(string reading)
    {
        // TODO: Implement ReplaceWord when needed
        SetReadingOn(GetReadingOnHtml().Replace(reading, $"<primary>{reading}</primary>"));
    }

    public void RemovePrimaryOnReading(string reading)
    {
        SetReadingOn(GetReadingOnHtml().Replace($"<primary>{reading}</primary>", reading));
    }

    public void AddPrimaryKunReading(string reading)
    {
        // TODO: Implement ReplaceWord when needed
        SetReadingKun(GetReadingKunHtml().Replace(reading, $"<primary>{reading}</primary>"));
    }

    public void RemovePrimaryKunReading(string reading)
    {
        SetReadingKun(GetReadingKunHtml().Replace($"<primary>{reading}</primary>", reading));
    }

    public List<string> GetRadicals()
    {
        // TODO: Implement ExtractCommaSeparatedValues
        var radicalsField = GetField(NoteFieldsConstants.Kanji.Radicals);
        var question = GetQuestion();
        return radicalsField.Split(',')
            .Select(r => r.Trim())
            .Where(r => !string.IsNullOrEmpty(r) && r != question)
            .ToList();
    }

    private void SetRadicals(string value)
    {
        SetField(NoteFieldsConstants.Kanji.Radicals, value);
    }

    public List<KanjiNote> GetRadicalsNotes()
    {
        return GetRadicals()
            .Select(radical => App.Col().Kanji.WithKanji(radical))
            .Where(k => k != null)
            .Cast<KanjiNote>()
            .ToList();
    }

    public string GetActiveMnemonic()
    {
        var userMnemonic = GetUserMnemonic();
        if (!string.IsNullOrEmpty(userMnemonic))
        {
            return userMnemonic;
        }

        // TODO: Implement config and mnemonic maker
        // if (App.Config().PreferDefaultMnemonicsToSourceMnemonics)
        // {
        //     return $"# {KanjiNoteMnemonicMaker.CreateDefaultMnemonic(this)}";
        // }

        return GetSourceMeaningMnemonic();
    }

    public string GetUserMnemonic()
    {
        return GetField(NoteFieldsConstants.Kanji.UserMnemonic);
    }

    public void SetUserMnemonic(string value)
    {
        SetField(NoteFieldsConstants.Kanji.UserMnemonic, value);
    }

    public string GetSourceMeaningMnemonic()
    {
        return GetField(NoteFieldsConstants.Kanji.SourceMeaningMnemonic);
    }

    private void SetPrimaryVocabAudio(string value)
    {
        SetField(NoteFieldsConstants.Kanji.Audio, value);
    }

    // Placeholder methods for vocab-related functionality
    public List<VocabNote> GetVocabNotes()
    {
        // TODO: Implement when VocabCollection is complete
        return new List<VocabNote>();
    }

    public static KanjiNote Create(string question, string answer, string onReadings, string kunReading)
    {
        var note = new KanjiNote();
        note.SetQuestion(question);
        note.SetUserAnswer(answer);
        note.SetReadingOn(onReadings);
        note.SetReadingKun(kunReading);
        App.Col().Kanji.Add(note);
        return note;
    }
}
