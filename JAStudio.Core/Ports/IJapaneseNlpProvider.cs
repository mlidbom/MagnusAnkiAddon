namespace JAStudio.Core.Ports;

using Domain;

/// <summary>
/// Interface for Japanese NLP operations
/// Implementations can come from Python (via Python.NET) or future C# alternatives
/// </summary>
public interface IJapaneseNlpProvider
{
    /// <summary>
    /// Tokenize Japanese text into morphemes
    /// </summary>
    List<Token> Tokenize(string text);
}
