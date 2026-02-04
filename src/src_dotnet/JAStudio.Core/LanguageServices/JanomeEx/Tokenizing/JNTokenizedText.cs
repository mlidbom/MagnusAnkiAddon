using System;
using System.Collections.Generic;
using JAStudio.Core.LanguageServices.JanomeEx.Tokenizing.PreProcessingStage;

namespace JAStudio.Core.LanguageServices.JanomeEx.Tokenizing;

public class JNTokenizedText
{
    public string Text { get; }
    public List<JNToken> Tokens { get; }

    public JNTokenizedText(string text, List<JNToken> tokens)
    {
        Text = text;
        Tokens = tokens;
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
