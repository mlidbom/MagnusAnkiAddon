using JAStudio.Core.Note.NoteFields;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.SysUtils;
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
        return StringExtensions.StripHtmlMarkup(GetAnswer());
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
        return StringExtensions.ExtractCommaSeparatedValues(
            StringExtensions.StripHtmlMarkup(GetReadingOnHtml()));
    }

    public List<string> GetReadingOnListHtml()
    {
        return StringExtensions.ExtractCommaSeparatedValues(GetReadingOnHtml());
    }

    public List<string> GetReadingsKun()
    {
        return StringExtensions.ExtractCommaSeparatedValues(
            StringExtensions.StripHtmlMarkup(GetReadingKunHtml()));
    }

    public List<string> GetReadingKunListHtml()
    {
        return StringExtensions.ExtractCommaSeparatedValues(GetReadingKunHtml());
    }

    public List<string> GetReadingNanListHtml()
    {
        return StringExtensions.ExtractCommaSeparatedValues(GetReadingNanHtml());
    }

    public List<string> GetReadingsClean()
    {
        var allReadings = new List<string>();
        allReadings.AddRange(GetReadingOnListHtml());
        allReadings.AddRange(GetReadingKunListHtml());
        allReadings.AddRange(GetReadingNanListHtml());
        return allReadings.Select(StringExtensions.StripHtmlMarkup).ToList();
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

    public void SetRadicals(string value)
    {
        SetField(NoteFieldsConstants.Kanji.Radicals, value);
    }

    public List<string> GetPrimaryVocabsOrDefaults()
    {
        var primaryVocab = GetPrimaryVocab();
        return primaryVocab.Count > 0 ? primaryVocab : GenerateDefaultPrimaryVocab();
    }

    public List<string> GetPrimaryVocab()
    {
        return StringExtensions.ExtractCommaSeparatedValues(GetField(NoteFieldsConstants.Kanji.PrimaryVocab));
    }

    public void SetPrimaryVocab(List<string> value)
    {
        SetField(NoteFieldsConstants.Kanji.PrimaryVocab, string.Join(", ", value));
    }

    public List<string> GenerateDefaultPrimaryVocab()
    {
        throw new NotImplementedException();
    }

    private static readonly Regex AnyWordPattern = new(@"\b[-\w]+\b", RegexOptions.Compiled);
    private static readonly Regex ParenthesizedWordPattern = new(@"\([-\w]+\)", RegexOptions.Compiled);

    public string GetPrimaryMeaning()
    {
        var radicalMeaningMatch = AnyWordPattern.Match(GetAnswerText().Replace("{", "").Replace("}", ""));
        return radicalMeaningMatch.Success ? radicalMeaningMatch.Groups[0].Value : "";
    }

    public string GetPrimaryRadicalMeaning()
    {
        string GetDedicatedRadicalPrimaryMeaning()
        {
            var radicalMeaningMatch = ParenthesizedWordPattern.Match(GetAnswerText());
            return radicalMeaningMatch.Success
                ? radicalMeaningMatch.Groups[0].Value.Replace("(", "").Replace(")", "")
                : "";
        }

        var result = GetDedicatedRadicalPrimaryMeaning();
        return !string.IsNullOrEmpty(result) ? result : GetPrimaryMeaning();
    }

    public List<KanjiNote> GetRadicalsNotes()
    {
        return GetRadicals()
            .Select(radical => App.Col().Kanji.WithKanji(radical))
            .Where(k => k != null)
            .Cast<KanjiNote>()
            .ToList();
    }

    public List<string> TagVocabReadings(VocabNote vocab)
    {
        string PrimaryReading(string read) => $"<span class=\"kanjiReadingPrimary\">{read}</span>";
        string SecondaryReading(string read) => $"<span class=\"kanjiReadingSecondary\">{read}</span>";

        var primaryReadings = GetPrimaryReadings();
        var secondaryReadings = GetReadingsClean()
            .Where(reading => !primaryReadings.Contains(reading) && !string.IsNullOrEmpty(reading))
            .ToList();

        var result = new List<string>();
        var vocabForm = vocab.GetQuestion();

        foreach (var vocabReading in vocab.GetReadings())
        {
            var found = false;

            foreach (var kanjiReading in primaryReadings)
            {
                if (ReadingInVocabReading(kanjiReading, vocabReading, vocabForm))
                {
                    result.Add(vocabReading.Replace(kanjiReading, PrimaryReading(kanjiReading)));
                    found = true;
                    break;
                }
            }

            if (!found)
            {
                foreach (var kanjiReading in secondaryReadings)
                {
                    if (ReadingInVocabReading(kanjiReading, vocabReading, vocabForm))
                    {
                        result.Add(vocabReading.Replace(kanjiReading, SecondaryReading(kanjiReading)));
                        found = true;
                        break;
                    }
                }

                if (!found)
                {
                    result.Add(vocabReading);
                }
            }
        }

        return result;
    }

    public bool ReadingInVocabReading(string kanjiReading, string vocabReading, string vocabForm)
    {
        vocabForm = ExStr.StripHtmlAndBracketMarkupAndNoiseCharacters(vocabForm);

        // Check for covering readings (readings that contain this reading as a substring)
        var coveringReadings = GetReadingsClean()
            .Where(r => kanjiReading != r && r.Contains(kanjiReading))
            .ToList();

        // If any covering reading matches, this reading shouldn't match
        if (coveringReadings.Any(coveringReading => ReadingInVocabReading(coveringReading, vocabReading, vocabForm)))
        {
            return false;
        }

        if (vocabForm.StartsWith(GetQuestion()))
        {
            return vocabReading.StartsWith(kanjiReading);
        }
        if (vocabForm.EndsWith(GetQuestion()))
        {
            return vocabReading.EndsWith(kanjiReading);
        }

        return vocabReading.Length >= 2 
            ? vocabReading.Substring(1, vocabReading.Length - 2).Contains(kanjiReading)
            : kanjiReading == "";
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

    public List<VocabNote> GetVocabNotesSorted()
    {
        return VocabNoteSorting.SortVocabListByStudyingStatus(
            GetVocabNotes(), 
            GetPrimaryVocabsOrDefaults(), 
            preferredKanji: GetQuestion());
    }

    public void BootstrapMnemonicFromRadicals()
    {
        SetUserMnemonic(KanjiNoteMnemonicMaker.CreateDefaultMnemonic(this));
    }

    public void PopulateRadicalsFromMnemonicTags()
    {
        List<string> DetectRadicalsFromMnemonic()
        {
            var radicalNames = System.Text.RegularExpressions.Regex.Matches(GetUserMnemonic(), @"<rad>(.*?)</rad>")
                .Cast<System.Text.RegularExpressions.Match>()
                .Select(m => m.Groups[1].Value)
                .ToList();

            bool KanjiAnswerContainsRadicalNameAsASeparateWord(string radicalName, KanjiNote kanji)
            {
                return System.Text.RegularExpressions.Regex.IsMatch(kanji.GetAnswer(), @"\b" + System.Text.RegularExpressions.Regex.Escape(radicalName) + @"\b");
            }

            bool KanjiAnswerContainsAnyRadicalNameAsASeparateWord(KanjiNote kanji)
            {
                return radicalNames.Any(name => KanjiAnswerContainsRadicalNameAsASeparateWord(name, kanji));
            }

            return App.Col().Kanji.All()
                .Where(KanjiAnswerContainsAnyRadicalNameAsASeparateWord)
                .Select(kanji => kanji.GetQuestion())
                .ToList();
        }

        var radicals = GetRadicals();
        foreach (var radical in DetectRadicalsFromMnemonic())
        {
            if (!radicals.Contains(radical))
            {
                radicals.Add(radical);
            }
        }

        SetRadicals(string.Join(", ", radicals));
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
