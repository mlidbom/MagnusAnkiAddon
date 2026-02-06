using System;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Tests.Fixtures;
using JAStudio.Core.Tests.Fixtures.BaseData.SampleData;
using Xunit;

namespace JAStudio.Core.Tests.Fixtures;

/// <summary>
/// Tests ported from test_collection_factory.py
/// </summary>
public class CollectionFactoryTests : CollectionUsingTest
{
   [Fact]
   public void KanjiAddedCorrectly()
   {
      var kanjiAll = App.Col().Kanji.All();
      var savedKanji = kanjiAll.Select(kanji =>
                                          new KanjiSpec(
                                             kanji.GetQuestion(),
                                             kanji.GetAnswer(),
                                             kanji.GetReadingKunHtml(),
                                             kanji.GetReadingOnHtml()
                                          )
      ).ToHashSet();

      Assert.Equal(KanjiSpec.TestKanjiList.ToHashSet(), savedKanji);
   }

   [Fact]
   public void VocabAddedCorrectly()
   {
      var expectedVocab = VocabLists.TestSpecialVocab.OrderBy(x => x.Question).ToList();
      var vocabAll = App.Col().Vocab.All();
      var savedVocab = vocabAll
                      .Select(vocab => new VocabSpec(vocab.GetQuestion(), vocab.GetAnswer(), vocab.Readings.Get()))
                      .OrderBy(x => x.Question)
                      .ToList();

      Assert.Equal(expectedVocab, savedVocab);
   }

   [Fact]
   public void SentencesAddedCorrectly()
   {
      var expectedSentences = SentenceSpec.TestSentenceList.OrderBy(x => x.Question).ToList();
      var sentencesAll = App.Col().Sentences.All()
                            .OrderBy(x => x.Question.WithoutInvisibleSpace())
                            .ToList();
      var savedSentences = sentencesAll
                          .Select(sentence => new SentenceSpec(
                                     sentence.Question.WithoutInvisibleSpace(),
                                     sentence.GetAnswer()
                                  ))
                          .ToList();

      Assert.Equal(expectedSentences, savedSentences);
   }
}
