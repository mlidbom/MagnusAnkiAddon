using System;
using System.Collections.Generic;
using JAStudio.Core.LanguageServices.JanomeEx.Tokenizing.PreProcessingStage;

namespace JAStudio.Core.LanguageServices.JanomeEx.Tokenizing;

public class JNTokenizedText
{
    public string Text { get; }
    public List<JNToken> Tokens { get; }
    public object RawTokens { get; } // Python-specific Janome tokens, kept as object for compatibility

    public JNTokenizedText(string text, List<JNToken> tokens, object? rawTokens = null)
    {
        Text = text;
        Tokens = tokens;
        RawTokens = rawTokens ?? new object(); // Placeholder - not used in C# but maintained for API compatibility
    }

    public List<IAnalysisToken> PreProcess()
    {
        try
        {
            return new PreProcessingStage.PreProcessingStage(App.Col().Vocab).PreProcess(Tokens);
        }
        catch (Exception)
        {
            MyLog.Error($"Failed to pre-process text: {Text}");
            throw;
        }
    }
}
