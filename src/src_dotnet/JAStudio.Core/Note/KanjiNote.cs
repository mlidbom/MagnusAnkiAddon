using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using JAStudio.Core.LanguageServices;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.SysUtils;

namespace JAStudio.Core.Note;

public class KanjiNote : JPNote
{
   static readonly Regex PrimaryReadingPattern = new(@"<primary>(.*?)</primary>", RegexOptions.Compiled);

   public KanjiNote(NoteServices services, NoteData? data = null) : base(services, data?.Id as KanjiId ?? KanjiId.New(), data) {}

   public override HashSet<JPNote> GetDirectDependencies() => GetRadicalsNotes().Cast<JPNote>().ToHashSet();

   public override void UpdateInCache()
   {
      Services.Collection.Kanji.Cache.JpNoteUpdated(this);
   }

   public override string GetQuestion() => GetField(NoteFieldsConstants.Kanji.Question);

   public void SetQuestion(string value) => SetField(NoteFieldsConstants.Kanji.Question, value);

   public override string GetAnswer()
   {
      var userAnswer = UserAnswer;
      return !string.IsNullOrEmpty(userAnswer) ? userAnswer : GetField(NoteFieldsConstants.Kanji.SourceAnswer);
   }

   public string AnswerText => StringExtensions.StripHtmlMarkup(GetAnswer());

   public string UserAnswer
   {
      get => GetField(NoteFieldsConstants.Kanji.UserAnswer);
      set => SetField(NoteFieldsConstants.Kanji.UserAnswer, value);
   }

   public override void UpdateGeneratedData()
   {
      base.UpdateGeneratedData();

      // Katakana sneaks in via yomitan etc
      ReadingOnHtml = KanaUtils.KatakanaToHiragana(ReadingOnHtml);

      void UpdatePrimaryAudios()
      {
         var vocabWeShouldPlay = PrimaryVocab
                                .SelectMany(question => Services.Collection.Vocab.WithQuestion(question))
                                .ToList();

         var audioString = vocabWeShouldPlay.Count > 0
                              ? string.Join("", vocabWeShouldPlay.Select(vo => vo.Audio.PrimaryAudio))
                              : string.Empty;

         SetPrimaryVocabAudio(audioString);
      }

      SetField(NoteFieldsConstants.Kanji.ActiveAnswer, GetAnswer());
      UpdatePrimaryAudios();
   }

   public List<string> ReadingsOn => StringExtensions.ExtractCommaSeparatedValues(
      StringExtensions.StripHtmlMarkup(ReadingOnHtml));

   public List<string> ReadingOnListHtml => StringExtensions.ExtractCommaSeparatedValues(ReadingOnHtml);

   public List<string> ReadingsKun => StringExtensions.ExtractCommaSeparatedValues(
      StringExtensions.StripHtmlMarkup(ReadingKunHtml));

   public List<string> ReadingKunListHtml => StringExtensions.ExtractCommaSeparatedValues(ReadingKunHtml);

   public List<string> ReadingNanListHtml => StringExtensions.ExtractCommaSeparatedValues(ReadingNanHtml);

   public List<string> ReadingsClean
   {
      get
      {
         var allReadings = new List<string>();
         allReadings.AddRange(ReadingOnListHtml);
         allReadings.AddRange(ReadingKunListHtml);
         allReadings.AddRange(ReadingNanListHtml);
         return allReadings.Select(StringExtensions.StripHtmlMarkup).ToList();
      }
   }

   public string ReadingOnHtml
   {
      get => GetField(NoteFieldsConstants.Kanji.ReadingOn);
      set => SetField(NoteFieldsConstants.Kanji.ReadingOn, value);
   }

   public List<string> PrimaryReadings
   {
      get
      {
         var readings = new List<string>();
         readings.AddRange(PrimaryReadingsOn);
         readings.AddRange(PrimaryReadingsKun);
         readings.AddRange(PrimaryReadingsNan);
         return readings;
      }
   }

   public List<string> PrimaryReadingsOn
   {
      get
      {
         var matches = PrimaryReadingPattern.Matches(ReadingOnHtml);
         return matches.Select(m => StringExtensions.StripHtmlMarkup(m.Groups[1].Value)).ToList();
      }
   }

   public List<string> PrimaryReadingsKun
   {
      get
      {
         var matches = PrimaryReadingPattern.Matches(ReadingKunHtml);
         return matches.Select(m => StringExtensions.StripHtmlMarkup(m.Groups[1].Value)).ToList();
      }
   }

   public List<string> PrimaryReadingsNan
   {
      get
      {
         var matches = PrimaryReadingPattern.Matches(ReadingNanHtml);
         return matches.Select(m => StringExtensions.StripHtmlMarkup(m.Groups[1].Value)).ToList();
      }
   }

   public string ReadingKunHtml
   {
      get => GetField(NoteFieldsConstants.Kanji.ReadingKun);
      set => SetField(NoteFieldsConstants.Kanji.ReadingKun, value);
   }

   public string ReadingNanHtml => GetField(NoteFieldsConstants.Kanji.ReadingNan);

   public void AddPrimaryOnReading(string reading)
   {
      ReadingOnHtml = StringExtensions.ReplaceWord(reading, $"<primary>{reading}</primary>", ReadingOnHtml);
   }

   public void RemovePrimaryOnReading(string reading)
   {
      ReadingOnHtml = ReadingOnHtml.Replace($"<primary>{reading}</primary>", reading);
   }

   public void AddPrimaryKunReading(string reading)
   {
      ReadingKunHtml = StringExtensions.ReplaceWord(reading, $"<primary>{reading}</primary>", ReadingKunHtml);
   }

   public void RemovePrimaryKunReading(string reading)
   {
      ReadingKunHtml = ReadingKunHtml.Replace($"<primary>{reading}</primary>", reading);
   }

   public List<string> Radicals
   {
      get
      {
         var radicalsField = GetField(NoteFieldsConstants.Kanji.Radicals);
         var question = GetQuestion();
         return StringExtensions.ExtractCommaSeparatedValues(radicalsField)
                                .Where(r => r != question)
                                .ToList();
      }
   }

   public void SetRadicals(string value)
   {
      SetField(NoteFieldsConstants.Kanji.Radicals, value);
   }

   public void PositionPrimaryVocab(string vocab, int newIndex = -1)
   {
      vocab = vocab.Trim();
      var primaryVocabList = PrimaryVocab;

      // Remove if already present
      if(primaryVocabList.Contains(vocab))
      {
         primaryVocabList.Remove(vocab);
      }

      // Add at specified index or end
      if(newIndex == -1)
      {
         primaryVocabList.Add(vocab);
      } else
      {
         primaryVocabList.Insert(newIndex, vocab);
      }

      PrimaryVocab = primaryVocabList;
   }

   public void RemovePrimaryVocab(string vocab)
   {
      var primaryVocabList = PrimaryVocab;
      primaryVocabList.RemoveAll(v => v == vocab);
      PrimaryVocab = primaryVocabList;
   }

   public List<string> UserSimilarMeaning => StringExtensions.ExtractCommaSeparatedValues(
      GetField(NoteFieldsConstants.Kanji.UserSimilarMeaning));

   public void AddUserSimilarMeaning(string newSynonymQuestion, bool isRecursiveCall = false)
   {
      var nearSynonymsQuestions = UserSimilarMeaning;
      if(!nearSynonymsQuestions.Contains(newSynonymQuestion))
      {
         nearSynonymsQuestions.Add(newSynonymQuestion);
      }

      SetField(NoteFieldsConstants.Kanji.UserSimilarMeaning, string.Join(", ", nearSynonymsQuestions));

      // Reciprocal relationship
      if(!isRecursiveCall)
      {
         var newSynonym = Services.Collection.Kanji.WithKanji(newSynonymQuestion);
         if(newSynonym != null)
         {
            newSynonym.AddUserSimilarMeaning(GetQuestion(), isRecursiveCall: true);
         }
      }
   }

   public List<string> RelatedConfusedWith => StringExtensions.ExtractCommaSeparatedValues(
      GetField(NoteFieldsConstants.Kanji.RelatedConfusedWith));

   public void AddRelatedConfusedWith(string newConfusedWith)
   {
      var confusedWith = RelatedConfusedWith;
      if(!confusedWith.Contains(newConfusedWith))
      {
         confusedWith.Add(newConfusedWith);
      }

      SetField(NoteFieldsConstants.Kanji.RelatedConfusedWith, string.Join(", ", confusedWith));
   }

   public List<string> PrimaryVocabsOrDefaults
   {
      get
      {
         var primaryVocab = PrimaryVocab;
         return primaryVocab.Count > 0 ? primaryVocab : GenerateDefaultPrimaryVocab();
      }
   }

   public List<string> PrimaryVocab
   {
      get => StringExtensions.ExtractCommaSeparatedValues(GetField(NoteFieldsConstants.Kanji.PrimaryVocab));
      set => SetField(NoteFieldsConstants.Kanji.PrimaryVocab, string.Join(", ", value));
   }

   public List<string> GenerateDefaultPrimaryVocab()
   {
      var result = new List<string>();

      // Sort by descending count of studying sentences, then by ascending question length
      var studyingReadingVocabInDescendingStudyingSentencesOrder = GetVocabNotes()
                                                                  .Where(v => v.IsStudying(CardTypes.Reading))
                                                                  .OrderByDescending(v => v.Sentences.Studying().Count)
                                                                  .ThenBy(v => v.GetQuestion().Length)
                                                                  .ToList();

      var primaryReadings = PrimaryReadings.Distinct().ToList();

      foreach(var primaryReading in primaryReadings)
      {
         foreach(var vocab in studyingReadingVocabInDescendingStudyingSentencesOrder)
         {
            var readings = vocab.Readings.Get();
            if(readings.Count > 0 && ReadingInVocabReading(primaryReading, readings[0], vocab.GetQuestion()))
            {
               result.Add(vocab.GetQuestion());
               break;
            }
         }
      }

      return result;
   }

   static readonly Regex AnyWordPattern = new(@"\b[-\w]+\b", RegexOptions.Compiled);
   static readonly Regex ParenthesizedWordPattern = new(@"\([-\w]+\)", RegexOptions.Compiled);

   public string PrimaryMeaning
   {
      get
      {
         var radicalMeaningMatch = AnyWordPattern.Match(AnswerText.Replace("{", "").Replace("}", ""));
         return radicalMeaningMatch.Success ? radicalMeaningMatch.Groups[0].Value : "";
      }
   }

   public string PrimaryRadicalMeaning
   {
      get
      {
         string GetDedicatedRadicalPrimaryMeaning()
         {
            var radicalMeaningMatch = ParenthesizedWordPattern.Match(AnswerText);
            return radicalMeaningMatch.Success
                      ? radicalMeaningMatch.Groups[0].Value.Replace("(", "").Replace(")", "")
                      : "";
         }

         var result = GetDedicatedRadicalPrimaryMeaning();
         return !string.IsNullOrEmpty(result) ? result : PrimaryMeaning;
      }
   }

   public List<KanjiNote> GetRadicalsNotes()
   {
      return Radicals
            .Select(radical => Services.Collection.Kanji.WithKanji(radical))
            .Where(k => k != null)
            .Cast<KanjiNote>()
            .ToList();
   }

   public List<string> TagVocabReadings(VocabNote vocab)
   {
      string PrimaryReading(string read) => $"<span class=\"kanjiReadingPrimary\">{read}</span>";
      string SecondaryReading(string read) => $"<span class=\"kanjiReadingSecondary\">{read}</span>";

      var primaryReadings = PrimaryReadings;
      var secondaryReadings = ReadingsClean
                             .Where(reading => !primaryReadings.Contains(reading) && !string.IsNullOrEmpty(reading))
                             .ToList();

      var result = new List<string>();
      var vocabForm = vocab.GetQuestion();

      foreach(var vocabReading in vocab.GetReadings())
      {
         var found = false;

         foreach(var kanjiReading in primaryReadings)
         {
            if(ReadingInVocabReading(kanjiReading, vocabReading, vocabForm))
            {
               result.Add(vocabReading.Replace(kanjiReading, PrimaryReading(kanjiReading)));
               found = true;
               break;
            }
         }

         if(!found)
         {
            foreach(var kanjiReading in secondaryReadings)
            {
               if(ReadingInVocabReading(kanjiReading, vocabReading, vocabForm))
               {
                  result.Add(vocabReading.Replace(kanjiReading, SecondaryReading(kanjiReading)));
                  found = true;
                  break;
               }
            }

            if(!found)
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
      var coveringReadings = ReadingsClean
                            .Where(r => kanjiReading != r && r.Contains(kanjiReading))
                            .ToList();

      // If any covering reading matches, this reading shouldn't match
      if(coveringReadings.Any(coveringReading => ReadingInVocabReading(coveringReading, vocabReading, vocabForm)))
      {
         return false;
      }

      if(vocabForm.StartsWith(GetQuestion()))
      {
         return vocabReading.StartsWith(kanjiReading);
      }

      if(vocabForm.EndsWith(GetQuestion()))
      {
         return vocabReading.EndsWith(kanjiReading);
      }

      return vocabReading.Length >= 2
                ? vocabReading.Substring(1, vocabReading.Length - 2).Contains(kanjiReading)
                : kanjiReading == "";
   }

   public string ActiveMnemonic
   {
      get
      {
         if(!string.IsNullOrEmpty(UserMnemonic))
         {
            return UserMnemonic;
         }

         if(Services.Config.PreferDefaultMnemonicsToSourceMnemonics.Value)
         {
            return $"# {Services.KanjiNoteMnemonicMaker.CreateDefaultMnemonic(this)}";
         }

         return SourceMeaningMnemonic;
      }
   }

   public string UserMnemonic
   {
      get => GetField(NoteFieldsConstants.Kanji.UserMnemonic);
      set => SetField(NoteFieldsConstants.Kanji.UserMnemonic, value);
   }

   public string SourceMeaningMnemonic => GetField(NoteFieldsConstants.Kanji.SourceMeaningMnemonic);

   void SetPrimaryVocabAudio(string value)
   {
      SetField(NoteFieldsConstants.Kanji.Audio, value);
   }

   public List<VocabNote> GetVocabNotes() => Services.Collection.Vocab.WithKanjiInAnyForm(this);

   public List<VocabNote> GetVocabNotesSorted() =>
      VocabNoteSorting.SortVocabListByStudyingStatus(
         GetVocabNotes(),
         PrimaryVocabsOrDefaults,
         preferredKanji: GetQuestion());

   public void BootstrapMnemonicFromRadicals()
   {
      UserMnemonic = Services.KanjiNoteMnemonicMaker.CreateDefaultMnemonic(this);
   }

   public void PopulateRadicalsFromMnemonicTags()
   {
      List<string> DetectRadicalsFromMnemonic()
      {
         var radicalNames = Regex.Matches(UserMnemonic, @"<rad>(.*?)</rad>")
                                 .Select(m => m.Groups[1].Value)
                                 .ToList();

         bool KanjiAnswerContainsRadicalNameAsASeparateWord(string radicalName, KanjiNote kanji) => Regex.IsMatch(kanji.GetAnswer(), @"\b" + Regex.Escape(radicalName) + @"\b");

         bool KanjiAnswerContainsAnyRadicalNameAsASeparateWord(KanjiNote kanji)
         {
            return radicalNames.Any(name => KanjiAnswerContainsRadicalNameAsASeparateWord(name, kanji));
         }

         return Services.Collection.Kanji.All()
                        .Where(KanjiAnswerContainsAnyRadicalNameAsASeparateWord)
                        .Select(kanji => kanji.GetQuestion())
                        .ToList();
      }

      var radicals = Radicals;
      foreach(var radical in DetectRadicalsFromMnemonic())
      {
         if(!radicals.Contains(radical))
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
      note.UserAnswer = answer;
      note.ReadingOnHtml = onReadings;
      note.ReadingKunHtml = kunReading;
      services.Collection.Kanji.Add(note);
      return note;
   }
}
