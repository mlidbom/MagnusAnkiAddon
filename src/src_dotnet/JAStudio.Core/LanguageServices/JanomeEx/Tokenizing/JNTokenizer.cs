using System.Collections.Generic;
using System.Linq;
using JAStudio.PythonInterop.Utilities;
using Python.Runtime;

namespace JAStudio.Core.LanguageServices.JanomeEx.Tokenizing;

public sealed class JNTokenizer
{
   static readonly HashSet<string> CharactersThatMayConfuseJanomeSoWeReplaceThemWithOrdinaryFullWidthSpaces =
       ["!", "！", "|", "（", "）"];

   readonly dynamic _tokenizer;

    public JNTokenizer()
    {
        using (PythonEnvironment.LockGil())
        {
            dynamic janome = Py.Import("janome.tokenizer");
            _tokenizer = janome.Tokenizer();
        }
    }

    public JNTokenizedText Tokenize(string text)
    {
        return PythonEnvironment.Use(() =>
        {
            // Apparently janome does not fully understand that invisible spaces are word separators,
            // so we replace them with ordinary spaces since they are not anything that should need to be parsed
            var sanitizedText = text.Replace(StringExtensions.InvisibleSpace, JNToken.SplitterTokenText);

            foreach (var character in CharactersThatMayConfuseJanomeSoWeReplaceThemWithOrdinaryFullWidthSpaces)
            {
                sanitizedText = sanitizedText.Replace(character, " ");
            }

            // It seems that janome is sometimes confused and changes its parsing if there is no whitespace after the text, so let's add one
            var tokens = new List<dynamic>();
            foreach (var token in Dyn.Enumerate(_tokenizer.tokenize(sanitizedText)))
            {
                tokens.Add(token);
            }

            // Create JNToken objects - extract all data from Python immediately
            var jnTokens = tokens.Select(token =>
            {
                var partsOfSpeech = JNPartsOfSpeech.Fetch((string)token.part_of_speech);

                return new JNToken(
                    partsOfSpeech,
                    baseForm: (string)token.base_form ?? string.Empty,
                    surface: (string)token.surface ?? string.Empty,
                    inflectionType: (string)token.infl_type ?? "*",
                    inflectedForm: (string)token.infl_form ?? "*",
                    reading: (string)token.reading ?? string.Empty,
                    phonetic: (string)token.phonetic ?? string.Empty,
                    nodeType: (string)token.node_type ?? string.Empty
                );
            }).ToList();

            // Link tokens with previous/next pointers
            for (var i = 0; i < jnTokens.Count; i++)
            {
                if (i > 0)
                {
                    jnTokens[i].Previous = jnTokens[i - 1];
                }
                if (i < jnTokens.Count - 1)
                {
                    jnTokens[i].Next = jnTokens[i + 1];
                }
            }

            return new JNTokenizedText(text, jnTokens);
        });
    }
}
