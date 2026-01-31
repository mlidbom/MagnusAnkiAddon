namespace JAStudio.Core.Services;

using System.Collections.Generic;
using System.Linq;
using Domain;
using Ports;

/// <summary>
/// Example service showing how to use the NLP provider
/// This will eventually become your TextAnalysisService
/// </summary>
public class TokenizerService
{
    private readonly IJapaneseNlpProvider _nlpProvider;

    public TokenizerService(IJapaneseNlpProvider nlpProvider)
    {
        _nlpProvider = nlpProvider;
    }

    /// <summary>
    /// Tokenize and return basic statistics
    /// </summary>
    public TokenizationResult Analyze(string text)
    {
        var tokens = _nlpProvider.Tokenize(text);

        return new TokenizationResult(
            Text: text,
            Tokens: tokens,
            TokenCount: tokens.Count,
            UniqueBaseForms: tokens.Select(t => t.BaseForm).Distinct().Count()
        );
    }

    /// <summary>
    /// Example: Find all verbs in the text
    /// </summary>
    public List<Token> ExtractVerbs(string text)
    {
        var tokens = _nlpProvider.Tokenize(text);
        return tokens
            .Where(t => t.PartOfSpeech.StartsWith("動詞"))
            .ToList();
    }
}

public record TokenizationResult(
    string Text,
    List<Token> Tokens,
    int TokenCount,
    int UniqueBaseForms
);
