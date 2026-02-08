using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using JAStudio.Core.Configuration;
using JAStudio.Core.LanguageServices.JamdictEx;
using JAStudio.Core.LanguageServices.JanomeEx.Tokenizing.PreProcessingStage;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.Note.Vocabulary;
using JAStudio.Core.SysUtils;
using JAStudio.Core.TaskRunners;

namespace JAStudio.Core.Batches;

public class LocalNoteUpdater
{
   readonly TaskRunner _taskRunner;
   readonly VocabCollection _vocab;
   readonly KanjiCollection _kanji;
   readonly SentenceCollection _sentences;
   readonly JapaneseConfig _config;
   readonly DictLookup _dictLookup;
   readonly VocabNoteFactory _vocabNoteFactory;

   internal LocalNoteUpdater(TaskRunner taskRunner, VocabCollection vocab, KanjiCollection kanji, SentenceCollection sentences, JapaneseConfig config, DictLookup dictLookup, VocabNoteFactory vocabNoteFactory)
   {
      _taskRunner = taskRunner;
      _vocab = vocab;
      _kanji = kanji;
      _sentences = sentences;
      _config = config;
      _dictLookup = dictLookup;
      _vocabNoteFactory = vocabNoteFactory;
   }

    public void UpdateAll()
    {
        using (_taskRunner.Current("Updating everything but sentence reparsing"))
        {
            UpdateSentences();
            UpdateKanji();
            UpdateVocab();
            TagNoteMetadata();
        }
    }

    public void FullRebuild()
    {
        using (_taskRunner.Current("Full rebuild"))
        {
            ReparseAllSentences();
            UpdateAll();
        }
    }

    public void UpdateSentences()
    {
        void UpdateSentence(SentenceNote sentence)
        {
            sentence.UpdateGeneratedData();
        }

        using var scope = _taskRunner.Current("Updating sentences");
        scope.ProcessWithProgress(
            _sentences.All().ToList(),
            s => { UpdateSentence(s); return 0; },
            "Updating sentences");
    }

    public void UpdateKanji()
    {
        void UpdateKanji(KanjiNote kanji)
        {
            kanji.UpdateGeneratedData();
        }

        using var scope = _taskRunner.Current("Updating kanji");
        scope.ProcessWithProgress(
            _kanji.All().ToList(),
            k => { UpdateKanji(k); return 0; },
            "Updating kanji");
    }

    public void UpdateVocab()
    {
        void UpdateVocab(VocabNote vocab)
        {
            vocab.UpdateGeneratedData();
        }

        using var scope = _taskRunner.Current("Updating vocab");
        scope.ProcessWithProgress(
            _vocab.All().ToList(),
            v => { UpdateVocab(v); return 0; },
            "Updating vocab");
    }

    public void TagNoteMetadata()
    {
        using (_taskRunner.Current("Tagging notes"))
        {
            TagKanjiMetadata();
            TagVocabMetadata();
            TagSentenceMetadata();
        }
    }

    public void TagSentenceMetadata()
    {
        void TagSentence(SentenceNote sentence)
        {
            sentence.Tags.Toggle(Tags.Sentence.Uses.IncorrectMatches, sentence.Configuration.IncorrectMatches.Get().Any());
            sentence.Tags.Toggle(Tags.Sentence.Uses.HiddenMatches, sentence.Configuration.HiddenMatches.Get().Any());
        }

        using var scope = _taskRunner.Current("Tagging sentence notes");
        scope.ProcessWithProgress(
            _sentences.All().ToList(),
            s => { TagSentence(s); return 0; },
            "Tagging sentence notes");
    }

    public void TagVocabMetadata()
    {
        void TagNote(VocabNote vocab)
        {
            vocab.Tags.Toggle(Tags.Vocab.Matching.Uses.RequiredPrefix, vocab.MatchingConfiguration.ConfigurableRules.RequiredPrefix.Any());
            vocab.Tags.Toggle(Tags.Vocab.Matching.Uses.PrefixIsNot, vocab.MatchingConfiguration.ConfigurableRules.PrefixIsNot.Any());
            vocab.Tags.Toggle(Tags.Vocab.Matching.Uses.SuffixIsNot, vocab.MatchingConfiguration.ConfigurableRules.SuffixIsNot.Any());
            vocab.Tags.Toggle(Tags.Vocab.Matching.Uses.SurfaceIsNot, vocab.MatchingConfiguration.ConfigurableRules.SurfaceIsNot.Any());
            vocab.Tags.Toggle(Tags.Vocab.IsIchidanHidingGodanPotential, IchidanGodanPotentialOrImperativeHybridSplitter.IsIchidanHidingGodan(vocab));
        }

        using var scope = _taskRunner.Current("Tagging vocab");
        scope.ProcessWithProgress(
            _vocab.All().ToList(),
            v => { TagNote(v); return 0; },
            "Tag vocab notes");
    }

    public void TagKanjiMetadata()
    {
        var primaryReadingPattern = new Regex(@"<primary>(.*?)</primary>", RegexOptions.Compiled);
        var knownKanji = _kanji.All()
            .Where(kanji => kanji.IsStudying())
            .Select(kanji => kanji.GetQuestion())
            .ToHashSet();

        void TagKanji(KanjiNote kanji)
        {
            var vocabWithKanjiInMainForm = _vocab.WithKanjiInMainForm(kanji);
            var vocabWithKanjiInAnyForm = _vocab.WithKanjiInAnyForm(kanji);

            var isRadical = _kanji.WithRadical(kanji.GetQuestion()).Any();
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
            var vocabs = _vocab.WithKanjiInMainForm(kanji);
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

        using var scope = _taskRunner.Current("Tagging kanji");
        var allKanji = _kanji.All().ToList();
        scope.ProcessWithProgress(allKanji, k => { TagKanji(k); return 0; }, "Tagging kanji with studying metadata");
        scope.ProcessWithProgress(allKanji, k => { TagHasSingleKanjiVocabWithReadingDifferentFromKanjiPrimaryReading(k); return 0; }, "Tagging kanji with single kanji vocab");
    }

    public void ReparseAllSentences()
    {
        using (_taskRunner.Current("Reparse all sentences"))
        {
            ReparseSentences(_sentences.All().ToList());
        }
    }

    public bool ReadingInVocabReading(KanjiNote kanji, string kanjiReading, string vocabReading, string vocabForm)
    {
        vocabForm = ExStr.StripHtmlAndBracketMarkupAndNoiseCharacters(vocabForm);
        if (vocabForm.StartsWith(kanji.GetQuestion()))
        {
            return vocabReading.StartsWith(kanjiReading);
        }
        if (vocabForm.EndsWith(kanji.GetQuestion()))
        {
            return vocabReading.EndsWith(kanjiReading);
        }
        return vocabReading.Length >= 2 
            ? vocabReading.Substring(1, vocabReading.Length - 2).Contains(kanjiReading) 
            : kanjiReading == "";
    }

    public void ReparseSentences(List<SentenceNote> sentences, bool runGcDuringBatch = false)
    {
        void ReparseSentence(SentenceNote sentence)
        {
            sentence.UpdateParsedWords(force: true);
        }

        runGcDuringBatch = runGcDuringBatch && _config.EnableGarbageCollectionDuringBatches.GetValue();
        
        // Shuffle to get accurate time estimations
        var random = new Random();
        sentences = sentences.OrderBy(_ => random.Next()).ToList();

        using var scope = _taskRunner.Current("Reparse Sentences");
        scope.ProcessWithProgress(
            sentences,
            s => { ReparseSentence(s); return 0; },
            "Reparsing sentences.",
            runGc: runGcDuringBatch,
            minimumItemsToGc: 500);
    }

    public void ReparseSentencesForVocab(VocabNote vocab)
    {
        vocab.UpdateGeneratedData();
        using var scope = _taskRunner.Current("Reparsing sentences for vocab");
        
        var sentences = scope.RunOnBackgroundThreadWithSpinningProgressDialog(
            "Fetching sentences to reparse",
            () => _sentences.PotentiallyMatchingVocab(vocab).ToHashSet());
        
        sentences.UnionWith(vocab.Sentences.All());
        ReparseSentences(sentences.ToList(), runGcDuringBatch: true);
    }

    public void ReparseMatchingSentences(string questionSubstring)
    {
        var sentencesToUpdate = _sentences.SentencesWithSubstring(questionSubstring);
        ReparseSentences(sentencesToUpdate.ToList(), runGcDuringBatch: true);
    }

    public void CreateMissingVocabWithDictionaryEntries()
    {
        using var scope = _taskRunner.Current("Creating vocab notes for parsed words with no vocab notes");

        var dictionaryWordsWithNoVocab = scope.RunOnBackgroundThreadWithSpinningProgressDialog(
            "Fetching parsed words with no vocab notes from parsing results",
            () => _sentences.All()
                .SelectMany(sentence => sentence.ParsingResult.Get().ParsedWords
                    .Where(word => word.VocabId == ParsedMatch.MissingNoteId)
                    .Select(word => word.ParsedForm))
                .Distinct()
                .Select(form => _dictLookup.LookupWord(form))
                .Where(result => result.FoundWords())
                .OrderBy(result => result.PrioritySpec().Priority)
                .ToList());

        void CreateVocabIfNotAlreadyCreated(DictLookupResult result)
        {
            // We may well have created a vocab that provides this form already...
            if (!_vocab.WithForm(result.Word).Any())
            {
                _vocabNoteFactory.CreateWithDictionary(result.Word);
            }
        }

        scope.ProcessWithProgress(
            dictionaryWordsWithNoVocab,
            r => { CreateVocabIfNotAlreadyCreated(r); return 0; },
            "Creating vocab notes");
    }

    public void RegenerateJamdictVocabAnswers()
    {
        using var scope = _taskRunner.Current("Regenerating vocab source answers from jamdict");
        var vocabNotes = _vocab.All().ToList();
        scope.ProcessWithProgress(
            vocabNotes,
            vocab => { vocab.GenerateAndSetAnswer(); return 0; },
            "Regenerating vocab source answers from jamdict");
    }
}
