using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Tests.Fixtures;
using Xunit;

namespace JAStudio.Core.Tests.LanguageServices.TextAnalysis;

/// <summary>
/// Tests ported from test_text_analysis_with_per_test_data.py
/// Note: This test uses per-test fixture scope (function scope in Python).
/// Each test creates and disposes its own collection.
/// </summary>
public class TextAnalysisWithPerTestDataTests : CollectionUsingTest
{
   public TextAnalysisWithPerTestDataTests() : base(DataNeeded.Vocabulary) {}

   [Theory]
   [InlineData("金<wbr>貸せって", "金", "貸す", "え", "って")]
   public void InvisibleSpaceBreakup(string sentence, params string[] expectedOutput)
   {
      var sentenceNote = SentenceNote.CreateTestNote(sentence, "");
      var rootWords = sentenceNote.ParsingResult.Get().ParsedWords
                                  .Select(w => w.ParsedForm)
                                  .ToList();
      Assert.Equal(expectedOutput.ToList(), rootWords);
   }
}
