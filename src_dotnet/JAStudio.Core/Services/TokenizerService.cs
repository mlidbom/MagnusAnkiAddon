namespace JAStudio.Core.Services;

using System.Collections.Generic;
using System.Linq;
using Domain;
using Ports;

public class TokenizerService(IJapaneseNlpProvider nlpProvider)
{
    private readonly IJapaneseNlpProvider _nlpProvider = nlpProvider;

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