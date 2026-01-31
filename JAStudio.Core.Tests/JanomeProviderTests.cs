namespace JAStudio.Core.Tests;

using System;
using System.Linq;
using JAStudio.Core.Services;
using JAStudio.PythonInterop;
using Xunit;

/// <summary>
/// Tests for janome integration via Python.NET
/// These tests will initialize Python runtime and create janome instances
/// </summary>
public class JanomeProviderTests : IDisposable
{
    private readonly JanomeProvider _provider;
    private readonly TokenizerService _service;

    public JanomeProviderTests()
    {
        // Initialize Python environment once for all tests
        PythonEnvironment.Initialize();

        _provider = new JanomeProvider();
        _service = new TokenizerService(_provider);
    }

    [Fact]
    public void Should_Tokenize_Simple_Japanese_Text()
    {
        // Arrange
        var text = "昨日";

        // Act
        var tokens = _provider.Tokenize(text);

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
        var sentence = "昨日、友達と映画を見ました。";

        // Act
        var result = _service.Analyze(sentence);

        // Assert
        Assert.True(result.TokenCount > 0, "Should have tokenized the sentence");
        Console.WriteLine($"Sentence: {sentence}");
        Console.WriteLine($"Token count: {result.TokenCount}");
        Console.WriteLine($"Unique base forms: {result.UniqueBaseForms}");
        Console.WriteLine("\nTokens:");
        foreach (var token in result.Tokens)
        {
            Console.WriteLine($"  {token.Surface} ({token.BaseForm}) - {token.PartOfSpeech}");
        }
    }

    [Fact]
    public void Should_Extract_Verbs()
    {
        // Arrange
        var sentence = "昨日、友達と映画を見ました。";

        // Act
        var verbs = _service.ExtractVerbs(sentence);

        // Assert
        Assert.NotEmpty(verbs);
        Console.WriteLine($"Found {verbs.Count} verb(s):");
        foreach (var verb in verbs)
        {
            Console.WriteLine($"  {verb.Surface} (base: {verb.BaseForm})");
        }
    }

    [Fact]
    public void Should_Handle_Multiple_Tokenizations()
    {
        // Test that we can tokenize multiple times (GIL handling)
        var texts = new[] { "食べる", "見る", "行く" };

        foreach (var text in texts)
        {
            var tokens = _provider.Tokenize(text);
            Assert.NotEmpty(tokens);
            Console.WriteLine($"{text} -> {tokens[0].BaseForm}");
        }
    }

    [Fact]
    public void Should_Show_Initialization_Mode()
    {
        // This test shows how the provider was initialized
        var mode = _provider.GetInitializationMode();
        Console.WriteLine($"Provider initialization mode: {mode}");
        Assert.Contains("initialized", mode.ToLower());
    }

    public void Dispose()
    {
        // Python runtime stays alive across tests for performance
        // Will be shut down when test process exits
    }
}
