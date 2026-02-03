using JAStudio.Core.Note;
using JAStudio.Core.Note.Sentences;
using JAStudio.Core.TestUtils;
using Xunit;

namespace JAStudio.Core.Tests.Note;

public class SentenceNoteTests
{
    public SentenceNoteTests()
    {
        TestApp.Initialize();
    }

    [Fact]
    public void SentenceNote_CreateTestNote_SetsQuestionAndAnswer()
    {
        // Arrange & Act
        var sentence = SentenceNote.CreateTestNote("これは本です。", "This is a book.");

        // Assert
        Assert.NotNull(sentence);
        Assert.Equal("これは本です。", sentence.GetQuestion());
        Assert.Equal("This is a book.", sentence.GetAnswer());
        Assert.NotEqual(0, sentence.GetId());
    }

    [Fact]
    public void SentenceNote_GetAnswer_StripsHtml()
    {
        // Arrange
        var sentence = new SentenceNote();
        sentence.SetField(NoteFieldsConstants.Sentence.SourceAnswer, "<b>This</b> is a <i>book</i>.");

        // Act
        var answer = sentence.GetAnswer();

        // Assert
        Assert.DoesNotContain("<b>", answer);
        Assert.DoesNotContain("</b>", answer);
        Assert.Equal("This is a book.", answer);
    }

    [Fact]
    public void SentenceNote_Configuration_DefaultsToEmpty()
    {
        // Arrange
        var sentence = new SentenceNote();

        // Act & Assert
        Assert.NotNull(sentence.Configuration);
        Assert.Empty(sentence.Configuration.HighlightedWords);
        Assert.True(sentence.Configuration.IncorrectMatches.IsEmpty());
        Assert.True(sentence.Configuration.HiddenMatches.IsEmpty());
    }
}
