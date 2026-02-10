using Xunit;

namespace JAStudio.Core.Tests.Note;

/// <summary>
/// Tests ported from test_sentencenote.py
/// </summary>
public class SentenceNotePortedTests : TestStartingWithEmptyCollection
{
   [Fact]
   public void SplitToken()
   {
      var sentence = "だったら普通に金貸せって言えよ";

      var sentenceNote = CreateSentence(sentence);
      sentenceNote.Question.SplitTokenWithWordBreakTag("金貸");

      Assert.Equal($"だったら普通に金{StringExtensions.InvisibleSpace}貸せって言えよ", sentenceNote.Question.WithInvisibleSpace());
   }
}
