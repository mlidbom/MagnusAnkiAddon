using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.SysUtils;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using JAStudio.Core.LanguageServices;

namespace JAStudio.Core.Note;

public class KanjiNote : JPNote
{
    private static readonly Regex PrimaryReadingPattern = new(@"<primary>(.*?)</primary>", RegexOptions.Compiled);

    public KanjiNote(NoteServices services, NoteData? data = null) : base(services, data)
    {
    }

    public override HashSet<JPNote> GetDirectDependencies()
    {
        return GetRadicalsNotes().Cast<JPNote>().ToHashSet();
    }

    public override void UpdateInCache()
    {
        Services.Collection.Kanji.Cache.JpNoteUpdated(this);
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

        // Katakana sneaks in via yomitan etc
        SetReadingOn(KanaUtils.KatakanaToHiragana(GetReadingOnHtml()));

        void UpdatePrimaryAudios()
        {
            var vocabWeShouldPlay = GetPrimaryVocab()
                .SelectMany(question => Services.Collection.Vocab.WithQuestion(question))
                .ToList();
            
            var audioString = vocabWeShouldPlay.Count > 0
                ? string.Join("", vocabWeShouldPlay.Select(vo => vo.Audio.GetPrimaryAudio()))
                : string.Empty;
            
            SetPrimaryVocabAudio(audioString);
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
        return matches.Select(m => StringExtensions.StripHtmlMarkup(m.Groups[1].Value)).ToList();
    }

    public List<string> GetPrimaryReadingsKun()
    {
        var matches = PrimaryReadingPattern.Matches(GetReadingKunHtml());
        return matches.Select(m => StringExtensions.StripHtmlMarkup(m.Groups[1].Value)).ToList();
    }

    public List<string> GetPrimaryReadingsNan()
    {
        var matches = PrimaryReadingPattern.Matches(GetReadingNanHtml());
        return matches.Select(m => StringExtensions.StripHtmlMarkup(m.Groups[1].Value)).ToList();
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
        SetReadingOn(StringExtensions.ReplaceWord(reading, $"<primary>{reading}</primary>", GetReadingOnHtml()));
    }

    public void RemovePrimaryOnReading(string reading)
    {
        SetReadingOn(GetReadingOnHtml().Replace($"<primary>{reading}</primary>", reading));
    }

    public void AddPrimaryKunReading(string reading)
    {
        SetReadingKun(StringExtensions.ReplaceWord(reading, $"<primary>{reading}</primary>", GetReadingKunHtml()));
    }

    public void RemovePrimaryKunReading(string reading)
    {
        SetReadingKun(GetReadingKunHtml().Replace($"<primary>{reading}</primary>", reading));
    }

    public List<string> GetRadicals()
    {
        var radicalsField = GetField(NoteFieldsConstants.Kanji.Radicals);
        var question = GetQuestion();
        return StringExtensions.ExtractCommaSeparatedValues(radicalsField)
            .Where(r => r != question)
            .ToList();
    }

    public void SetRadicals(string value)
    {
        SetField(NoteFieldsConstants.Kanji.Radicals, value);
    }

    public void PositionPrimaryVocab(string vocab, int newIndex = -1)
    {
        vocab = vocab.Trim();
        var primaryVocabList = GetPrimaryVocab();
        
        // Remove if already present
        if (primaryVocabList.Contains(vocab))
        {
            primaryVocabList.Remove(vocab);
        }

        // Add at specified index or end
        if (newIndex == -1)
        {
            primaryVocabList.Add(vocab);
        }
        else
        {
            primaryVocabList.Insert(newIndex, vocab);
        }

        SetPrimaryVocab(primaryVocabList);
    }

    public void RemovePrimaryVocab(string vocab)
    {
        var primaryVocabList = GetPrimaryVocab();
        primaryVocabList.RemoveAll(v => v == vocab);
        SetPrimaryVocab(primaryVocabList);
    }

    public List<string> GetUserSimilarMeaning()
    {
        return StringExtensions.ExtractCommaSeparatedValues(
            GetField(NoteFieldsConstants.Kanji.UserSimilarMeaning));
    }

    public void AddUserSimilarMeaning(string newSynonymQuestion, bool isRecursiveCall = false)
    {
        var nearSynonymsQuestions = GetUserSimilarMeaning();
        if (!nearSynonymsQuestions.Contains(newSynonymQuestion))
        {
            nearSynonymsQuestions.Add(newSynonymQuestion);
        }

        SetField(NoteFieldsConstants.Kanji.UserSimilarMeaning, string.Join(", ", nearSynonymsQuestions));

        // Reciprocal relationship
        if (!isRecursiveCall)
        {
            var newSynonym = Services.Collection.Kanji.WithKanji(newSynonymQuestion);
            if (newSynonym != null)
            {
                newSynonym.AddUserSimilarMeaning(GetQuestion(), isRecursiveCall: true);
            }
        }
    }

    public List<string> GetRelatedConfusedWith()
    {
        return StringExtensions.ExtractCommaSeparatedValues(
            GetField(NoteFieldsConstants.Kanji.RelatedConfusedWith));
    }

    public void AddRelatedConfusedWith(string newConfusedWith)
    {
        var confusedWith = GetRelatedConfusedWith();
        if (!confusedWith.Contains(newConfusedWith))
        {
            confusedWith.Add(newConfusedWith);
        }
        SetField(NoteFieldsConstants.Kanji.RelatedConfusedWith, string.Join(", ", confusedWith));
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
        // When no explicit primary vocab is set, derive defaults from vocab notes
        // that contain this kanji. Prioritize studying vocab, then take by form.
        var vocabNotes = GetVocabNotes();
        
        // Prefer studying vocab first, then all others
        var studying = vocabNotes.Where(v => v.IsStudying()).ToList();
        var notStudying = vocabNotes.Where(v => !v.IsStudying()).ToList();
        
        var ordered = studying.Concat(notStudying);
        
        return ordered
            .Select(v => v.GetQuestion())
            .Where(q => !string.IsNullOrEmpty(q))
            .Distinct()
            .Take(5)
            .ToList();
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
            .Select(radical => Services.Collection.Kanji.WithKanji(radical))
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

        if (Services.Config.PreferDefaultMnemonicsToSourceMnemonics.GetValue())
        {
            return $"# {Services.KanjiNoteMnemonicMaker.CreateDefaultMnemonic(this)}";
        }

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

    public List<VocabNote> GetVocabNotes()
    {
        return Services.Collection.Vocab.WithKanjiInAnyForm(this);
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
        SetUserMnemonic(Services.KanjiNoteMnemonicMaker.CreateDefaultMnemonic(this));
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

            return Services.Collection.Kanji.All()
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

    public static KanjiNote Create(NoteServices services, string question, string answer, string onReadings, string kunReading)
    {
        var note = new KanjiNote(services);
        note.SetQuestion(question);
        note.SetUserAnswer(answer);
        note.SetReadingOn(onReadings);
        note.SetReadingKun(kunReading);
        services.Collection.Kanji.Add(note);
        return note;
    }
}
