using System;
using JAStudio.PythonInterop;
using JAStudio.PythonInterop.Janome;
using JAStudio.PythonInterop.Utilities;
using Xunit;

namespace JAStudio.Core.Tests;

public class JanomeTokenizerTests
{
    private readonly JanomeTokenizer _tokenizer;

    public JanomeTokenizerTests()
    {
        PythonEnvironment.EnsureInitialized();
        _tokenizer = new JanomeTokenizer();
    }

    [Fact]
    public void Should_Tokenize_Simple_Japanese_Text()
    {
        // Arrange
        var text = "昨日";

        // Act
        var tokens = _tokenizer.Tokenize(text);

        // Assert
        Assert.NotEmpty(tokens);
        Assert.Equal("昨日", tokens[0].Surface);
        Console.WriteLine($"Tokenized '昨日' into {tokens.Count} token(s)");
        Console.WriteLine($"Base form: {tokens[0].BaseForm}");
        Console.WriteLine($"Reading: {tokens[0].Reading}");
    }

    [Fact]
    public void Should_Tokenize_Sentence()
    {
        // Arrange
        var sentence = "すべての事実に一致する以上　それが正しい事は間違いない";

        // Act

        for (var i = 0;i < 100; i++) //It seems 100 tokenized sentences only take a fraction of a second, so the interop overhead is acceptable
        {
            var result = _tokenizer.Tokenize(sentence);

            // Assert
            Assert.True(result.Count > 0, "There should be tokens");
        }
    }

    [Fact]
    public void Should_Handle_Multiple_Tokenizations()
    {
        // Test that we can tokenize multiple times (GIL handling)
        var texts = new[] { "食べる", "見る", "行く", "すべての事実に一致する以上　それが正しい事は間違いない" };

        foreach (var text in texts)
        {
            var tokens = _tokenizer.Tokenize(text);
            Assert.NotEmpty(tokens);
            Console.WriteLine($"{text} -> {tokens.Count} tokens. First:{tokens[0].BaseForm}");
        }
    }
}