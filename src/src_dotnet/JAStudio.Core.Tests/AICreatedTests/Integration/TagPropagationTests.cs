using JAStudio.Core.Note;
using JAStudio.Core.TestUtils;
using Xunit;

namespace JAStudio.Core.Tests.AICreatedTests.Integration;

public class TagPropagationTests : TestStartingWithEmptyCollection, IAIGeneratedTestClass
{
    [Fact]
    public void SettingTag_StoresOnNote()
    {
        // Arrange
        var vocab = CreateVocab("食べる", "to eat", "たべる");

        // Act
        vocab.Tags.Set(Tags.TTSAudio);

        // Assert
        Assert.True(vocab.Tags.Contains(Tags.TTSAudio));
    }

    [Fact]
    public void UnsettingTag_RemovesFromNote()
    {
        // Arrange
        var vocab = CreateVocab("食べる", "to eat", "たべる");
        vocab.Tags.Set(Tags.TTSAudio);

        // Act
        vocab.Tags.Unset(Tags.TTSAudio);

        // Assert
        Assert.False(vocab.Tags.Contains(Tags.TTSAudio));
    }

    [Fact]
    public void MultipleTagsCanBeSetOnSameNote()
    {
        // Arrange
        var kanji = CreateKanji("食", "eat", "ショク", "た");

        // Act
        kanji.Tags.Set(Tags.TTSAudio);
        kanji.Tags.Set(Tags.Kanji.IsRadical);
        kanji.Tags.Set(Tags.Kanji.InVocabMainForm);

        // Assert
        Assert.True(kanji.Tags.Contains(Tags.TTSAudio));
        Assert.True(kanji.Tags.Contains(Tags.Kanji.IsRadical));
        Assert.True(kanji.Tags.Contains(Tags.Kanji.InVocabMainForm));
    }

    [Fact]
    public void TagsAreIndependentBetweenNotes()
    {
        // Arrange
        var vocab1 = CreateVocab("食べる", "to eat", "たべる");
        var vocab2 = CreateVocab("飲む", "to drink", "のむ");

        // Act
        vocab1.Tags.Set(Tags.TTSAudio);

        // Assert
        Assert.True(vocab1.Tags.Contains(Tags.TTSAudio));
        Assert.False(vocab2.Tags.Contains(Tags.TTSAudio));
    }

    [Fact]
    public void TogglingTag_WorksCorrectly()
    {
        // Arrange
        var sentence = CreateTestSentence("これは本です。", "This is a book.");

        // Act & Assert - Set tag
        sentence.Tags.Set(Tags.TTSAudio);
        Assert.True(sentence.Tags.Contains(Tags.TTSAudio));

        // Unset tag
        sentence.Tags.Unset(Tags.TTSAudio);
        Assert.False(sentence.Tags.Contains(Tags.TTSAudio));

        // Set again
        sentence.Tags.Set(Tags.TTSAudio);
        Assert.True(sentence.Tags.Contains(Tags.TTSAudio));
    }
}
