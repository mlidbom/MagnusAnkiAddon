using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using JAStudio.Core.LanguageServices.JanomeEx.Tokenizing.PreProcessingStage;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.TaskRunners;

namespace JAStudio.Core.Batches;

public static class LocalNoteUpdater
{
    public static void UpdateAll()
    {
        using (TaskRunner.Current("Updating everything but sentence reparsing"))
        {
            UpdateSentences();
            UpdateKanji();
            UpdateVocab();
            TagNoteMetadata();
        }
    }

    public static void FullRebuild()
    {
        using (TaskRunner.Current("Full rebuild"))
        {
            ReparseAllSentences();
            UpdateAll();
        }
    }

    public static void UpdateSentences()
    {
        void UpdateSentence(SentenceNote sentence)
        {
            sentence.UpdateGeneratedData();
        }

        using var scope = TaskRunner.Current("Updating sentences");
        var runner = TaskRunner.GetCurrent()!;
        runner.ProcessWithProgress(
            App.Col().Sentences.All().ToList(),
            s => { UpdateSentence(s); return 0; },
            "Updating sentences");
    }

    public static void UpdateKanji()
    {
        void UpdateKanji(KanjiNote kanji)
        {
            kanji.UpdateGeneratedData();
        }

        using var scope = TaskRunner.Current("Updating kanji");
        var runner = TaskRunner.GetCurrent()!;
        runner.ProcessWithProgress(
            App.Col().Kanji.All().ToList(),
            k => { UpdateKanji(k); return 0; },
            "Updating kanji");
    }

    public static void UpdateVocab()
    {
        void UpdateVocab(VocabNote vocab)
        {
            vocab.UpdateGeneratedData();
        }

        using var scope = TaskRunner.Current("Updating vocab");
        var runner = TaskRunner.GetCurrent()!;
        runner.ProcessWithProgress(
            App.Col().Vocab.All().ToList(),
            v => { UpdateVocab(v); return 0; },
            "Updating vocab");
    }

    public static void TagNoteMetadata()
    {
        using (TaskRunner.Current("Tagging notes"))
        {
            TagKanjiMetadata();
            TagVocabMetadata();
            TagSentenceMetadata();
        }
    }

    public static void TagSentenceMetadata()
    {
        void TagSentence(SentenceNote sentence)
        {
            sentence.Tags.Toggle(Tags.Sentence.Uses.IncorrectMatches, sentence.Configuration.IncorrectMatches.Get().Any());
            sentence.Tags.Toggle(Tags.Sentence.Uses.HiddenMatches, sentence.Configuration.HiddenMatches.Get().Any());
        }

        using var scope = TaskRunner.Current("Tagging sentence notes");
        var runner = TaskRunner.GetCurrent()!;
        runner.ProcessWithProgress(
            App.Col().Sentences.All().ToList(),
            s => { TagSentence(s); return 0; },
            "Tagging sentence notes");
    }

    public static void TagVocabMetadata()
    {
        void TagNote(VocabNote vocab)
        {
            vocab.Tags.Toggle(Tags.Vocab.Matching.Uses.RequiredPrefix, vocab.MatchingConfiguration.ConfigurableRules.RequiredPrefix.Any());
            vocab.Tags.Toggle(Tags.Vocab.Matching.Uses.PrefixIsNot, vocab.MatchingConfiguration.ConfigurableRules.PrefixIsNot.Any());
            vocab.Tags.Toggle(Tags.Vocab.Matching.Uses.SuffixIsNot, vocab.MatchingConfiguration.ConfigurableRules.SuffixIsNot.Any());
            vocab.Tags.Toggle(Tags.Vocab.Matching.Uses.SurfaceIsNot, vocab.MatchingConfiguration.ConfigurableRules.SurfaceIsNot.Any());
            vocab.Tags.Toggle(Tags.Vocab.IsIchidanHidingGodanPotential, IchidanGodanPotentialOrImperativeHybridSplitter.IsIchidanHidingGodan(vocab));
        }

        using var scope = TaskRunner.Current("Tagging vocab");
        var runner = TaskRunner.GetCurrent()!;
        runner.ProcessWithProgress(
            App.Col().Vocab.All().ToList(),
            v => { TagNote(v); return 0; },
            "Tag vocab notes");
    }

    public static void TagKanjiMetadata()
    {
        var primaryReadingPattern = new Regex(@"<primary>(.*?)</primary>", RegexOptions.Compiled);
        var knownKanji = App.Col().Kanji.All()
            .Where(kanji => kanji.IsStudying())
            .Select(kanji => kanji.GetQuestion())
            .ToHashSet();

        void TagKanji(KanjiNote kanji)
        {
            var vocabWithKanjiInMainForm = App.Col().Vocab.WithKanjiInMainForm(kanji);
            var vocabWithKanjiInAnyForm = App.Col().Vocab.WithKanjiInAnyForm(kanji);

            var isRadical = App.Col().Kanji.WithRadical(kanji.GetQuestion()).Any();
            kanji.Tags.Toggle(Tags.Kanji.InVocabMainForm, vocabWithKanjiInMainForm.Any());
            kanji.Tags.Toggle(Tags.Kanji.InAnyVocabForm, vocabWithKanjiInAnyForm.Any());

            var studyingReadingVocab = vocabWithKanjiInMainForm
                .Where(voc => voc.IsStudying(CardTypes.Reading))
                .ToList();
            kanji.Tags.Toggle(Tags.Kanji.WithStudyingVocab, studyingReadingVocab.Any());

            var readingsHtml = $"{kanji.GetReadingOnHtml()} {kanji.GetReadingKunHtml()} {kanji.GetReadingNanHtml()}";
            var primaryReadings = primaryReadingPattern.Matches(readingsHtml)
                .Select(m => m.Groups[1].Value)
                .ToList();
            kanji.Tags.Toggle(Tags.Kanji.WithNoPrimaryReadings, !primaryReadings.Any());

            var primaryOnReadings = primaryReadingPattern.Matches(kanji.GetReadingOnHtml())
                .Select(m => m.Groups[1].Value)
                .ToList();
            var nonPrimaryOnReadings = kanji.GetReadingsOn()
                .Where(reading => !primaryReadings.Contains(reading))
                .ToList();

            kanji.Tags.Toggle(Tags.Kanji.WithNoPrimaryOnReadings, !primaryOnReadings.Any());

            bool ReadingIsInVocabReadings(string kanjiReading, VocabNote voc)
            {
                return voc.GetReadings().Any(vocabReading =>
                    ReadingInVocabReading(kanji, kanjiReading, vocabReading, voc.GetQuestion()));
            }

            bool HasVocabWithReading(string kanjiReading)
            {
                return vocabWithKanjiInMainForm.Any(voc =>
                    voc.GetReadings().Any(vocabReading =>
                        ReadingInVocabReading(kanji, kanjiReading, vocabReading, voc.GetQuestion())));
            }

            bool VocabHasOnlyKnownKanji(VocabNote voc)
            {
                return !voc.Kanji.ExtractAllKanji().Any(kan => !knownKanji.Contains(kan));
            }

            bool HasVocabWithReadingAndNoUnknownKanji(string kanjiReading)
            {
                return vocabWithKanjiInMainForm.Any(voc =>
                    ReadingIsInVocabReadings(kanjiReading, voc) && VocabHasOnlyKnownKanji(voc));
            }

            kanji.Tags.Toggle(Tags.Kanji.WithVocabWithPrimaryOnReading,
                primaryOnReadings.Any() && HasVocabWithReading(primaryOnReadings[0]));

            bool HasStudyingVocabWithReading(string kanjiReading)
            {
                return studyingReadingVocab.Any(voc =>
                    voc.GetReadings().Any(vocabReading =>
                        ReadingInVocabReading(kanji, kanjiReading, vocabReading, voc.GetQuestion())));
            }

            kanji.Tags.Toggle(Tags.Kanji.WithStudyingVocabWithPrimaryOnReading,
                primaryOnReadings.Any() && HasStudyingVocabWithReading(primaryOnReadings[0]));
            kanji.Tags.Toggle(Tags.Kanji.HasStudyingVocabForEachPrimaryReading,
                primaryReadings.Any() && !primaryReadings.Any(reading => !HasStudyingVocabWithReading(reading)));
            kanji.Tags.Toggle(Tags.Kanji.HasPrimaryReadingWithNoStudyingVocab,
                primaryReadings.Any() && studyingReadingVocab.Any() &&
                primaryReadings.Any(reading => !HasStudyingVocabWithReading(reading)));
            kanji.Tags.Toggle(Tags.Kanji.HasNonPrimaryOnReadingVocab,
                nonPrimaryOnReadings.Any(reading => HasVocabWithReading(reading)));
            kanji.Tags.Toggle(Tags.Kanji.HasNonPrimaryOnReadingVocabWithOnlyKnownKanji,
                nonPrimaryOnReadings.Any(reading => HasVocabWithReadingAndNoUnknownKanji(reading)));

            var allReadings = kanji.GetReadingsClean();

            bool VocabMatchesPrimaryReading(VocabNote vocab)
            {
                return primaryReadings.Any(pr =>
                    vocab.GetReadings().Any(vr => vr.Contains(pr)));
            }

            bool VocabMatchesReading(VocabNote vocab)
            {
                return allReadings.Any(r =>
                    vocab.GetReadings().Any(vr => vr.Contains(r)));
            }

            kanji.Tags.Toggle(Tags.Kanji.HasStudyingVocabWithNoMatchingPrimaryReading,
                studyingReadingVocab.Any(vocab =>
                    !VocabMatchesPrimaryReading(vocab) && VocabMatchesReading(vocab)));

            kanji.Tags.Toggle(Tags.Kanji.IsRadical, isRadical);
            kanji.Tags.Toggle(Tags.Kanji.IsRadicalPurely, isRadical && !vocabWithKanjiInAnyForm.Any());
            kanji.Tags.Toggle(Tags.Kanji.IsRadicalSilent, isRadical && !primaryReadings.Any());
        }

        void TagHasSingleKanjiVocabWithReadingDifferentFromKanjiPrimaryReading(KanjiNote kanji)
        {
            var vocabs = App.Col().Vocab.WithKanjiInMainForm(kanji);
            var singleKanjiVocab = vocabs.Where(v => v.GetQuestion() == kanji.GetQuestion()).ToList();
            kanji.Tags.Toggle(Tags.Kanji.WithSingleKanjiVocab, singleKanjiVocab.Any());

            if (singleKanjiVocab.Any())
            {
                var readingsHtml = $"{kanji.GetReadingOnHtml()} {kanji.GetReadingKunHtml()} {kanji.GetReadingNanHtml()}";
                var primaryReadings = primaryReadingPattern.Matches(readingsHtml)
                    .Select(m => m.Groups[1].Value)
                    .ToList();

                kanji.Tags.Unset(Tags.Kanji.WithSingleKanjiVocabWithDifferentReading);
                kanji.Tags.Unset(Tags.Kanji.WithStudyingSingleKanjiVocabWithDifferentReading);

                foreach (var vocab in singleKanjiVocab)
                {
                    foreach (var reading in vocab.GetReadings())
                    {
                        if (!primaryReadings.Contains(reading))
                        {
                            kanji.Tags.Set(Tags.Kanji.WithSingleKanjiVocabWithDifferentReading);
                        }
                    }
                }
            }
        }

        using var scope = TaskRunner.Current("Tagging kanji");
        var runner = TaskRunner.GetCurrent()!;
        var allKanji = App.Col().Kanji.All().ToList();
        runner.ProcessWithProgress(allKanji, k => { TagKanji(k); return 0; }, "Tagging kanji with studying metadata");
        runner.ProcessWithProgress(allKanji, k => { TagHasSingleKanjiVocabWithReadingDifferentFromKanjiPrimaryReading(k); return 0; }, "Tagging kanji with single kanji vocab");
    }

    public static void ReparseAllSentences()
    {
        using (TaskRunner.Current("Reparse all sentences"))
        {
            ReparseSentences(App.Col().Sentences.All().ToList());
        }
    }

    public static bool ReadingInVocabReading(KanjiNote kanji, string kanjiReading, string vocabReading, string vocabForm)
    {
        vocabForm = StripHtmlAndBracketMarkupAndNoiseCharacters(vocabForm);
        if (vocabForm.StartsWith(kanji.GetQuestion()))
        {
            return vocabReading.StartsWith(kanjiReading);
        }
        if (vocabForm.EndsWith(kanji.GetQuestion()))
        {
            return vocabReading.EndsWith(kanjiReading);
        }
        return vocabReading.Length > 2 && vocabReading.Substring(1, vocabReading.Length - 2).Contains(kanjiReading);
    }

    private static string StripHtmlAndBracketMarkupAndNoiseCharacters(string input)
    {
        // Remove HTML tags
        var result = Regex.Replace(input, @"<[^>]*>", string.Empty);
        // Remove bracket markup
        result = Regex.Replace(result, @"\[[^\]]*\]", string.Empty);
        result = Regex.Replace(result, @"\([^)]*\)", string.Empty);
        // Remove noise characters (special characters that don't affect meaning)
        result = result.Replace("・", "").Replace("～", "").Replace("〜", "");
        return result;
    }

    public static void ReparseSentences(List<SentenceNote> sentences, bool runGcDuringBatch = false)
    {
        void ReparseSentence(SentenceNote sentence)
        {
            sentence.UpdateParsedWords(force: true);
        }

        runGcDuringBatch = runGcDuringBatch && App.Config().EnableGarbageCollectionDuringBatches.GetValue();
        
        // Shuffle to get accurate time estimations
        var random = new Random();
        sentences = sentences.OrderBy(_ => random.Next()).ToList();

        using var scope = TaskRunner.Current("Reparse Sentences", inhibitGc: runGcDuringBatch);
        var runner = TaskRunner.GetCurrent()!;
        runner.ProcessWithProgress(
            sentences,
            s => { ReparseSentence(s); return 0; },
            "Reparsing sentences.",
            runGc: runGcDuringBatch,
            minimumItemsToGc: 500);
    }

    public static void ReparseSentencesForVocab(VocabNote vocab)
    {
        vocab.UpdateGeneratedData();
        using var scope = TaskRunner.Current("Reparsing sentences for vocab");
        var runner = TaskRunner.GetCurrent()!;
        
        var sentences = runner.RunOnBackgroundThreadWithSpinningProgressDialog(
            "Fetching sentences to reparse",
            () => App.Col().Sentences.PotentiallyMatchingVocab(vocab).ToHashSet());
        
        sentences.UnionWith(vocab.Sentences.All());
        ReparseSentences(sentences.ToList(), runGcDuringBatch: true);
    }

    public static void ReparseMatchingSentences(string questionSubstring)
    {
        var sentencesToUpdate = App.Col().Sentences.SentencesWithSubstring(questionSubstring);
        ReparseSentences(sentencesToUpdate.ToList(), runGcDuringBatch: true);
    }

    public static void CreateMissingVocabWithDictionaryEntries()
    {
        throw new NotImplementedException("DictLookup not yet ported");
    }

    public static void RegenerateJamdictVocabAnswers()
    {
        using var scope = TaskRunner.Current("Regenerating vocab source answers from jamdict");
        var runner = TaskRunner.GetCurrent()!;
        var vocabNotes = App.Col().Vocab.All().ToList();
        runner.ProcessWithProgress(
            vocabNotes,
            vocab => { vocab.GenerateAndSetAnswer(); return 0; },
            "Regenerating vocab source answers from jamdict");
    }
}
