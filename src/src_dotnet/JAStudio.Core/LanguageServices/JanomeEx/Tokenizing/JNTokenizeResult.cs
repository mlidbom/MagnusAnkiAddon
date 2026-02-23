namespace JAStudio.Core.LanguageServices.JanomeEx.Tokenizing;

public class JNTokenizeResult(JNTokenizedText tokenizedText, string serializedTokens)
{
   public JNTokenizedText TokenizedText { get; } = tokenizedText;
   public string SerializedTokens { get; } = serializedTokens;
}
