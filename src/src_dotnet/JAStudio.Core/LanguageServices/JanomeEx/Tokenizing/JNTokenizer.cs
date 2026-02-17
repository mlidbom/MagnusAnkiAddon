using System.Collections.Generic;
using Compze.Utilities.SystemCE.ThreadingCE.ResourceAccess;
using JAStudio.PythonInterop.Utilities;
using Python.Runtime;

namespace JAStudio.Core.LanguageServices.JanomeEx.Tokenizing;

public sealed class JNTokenizer
{
   readonly IMonitorCE _monitor = IMonitorCE.WithDefaultTimeout();

   static readonly HashSet<string> CharactersThatMayConfuseJanomeSoWeReplaceThemWithOrdinaryFullWidthSpaces =
      ["!", "！", "|", "（", "）"];

   /// <summary>The invisible space character (U+200B) used as field separator in the serialized token string from Python.</summary>
   const string FieldSeparator = StringExtensions.InvisibleSpace;

   const string WrapperPythonCode =
      $"""
      from janome.tokenizer import Tokenizer

      _FIELD_SEPARATOR = "{FieldSeparator}"
      _tokenizer = Tokenizer()

      def _sanitize(value):
          if value is None:
              return ""
          return str(value).replace("\n", " ").replace("\r", " ")

      def tokenize_to_string(text):
          lines = []
          for token in _tokenizer.tokenize(text):
              fields = _FIELD_SEPARATOR.join([
                  _sanitize(token.part_of_speech),
                  _sanitize(token.base_form),
                  _sanitize(token.surface),
                  _sanitize(token.infl_type),
                  _sanitize(token.infl_form),
                  _sanitize(token.reading),
                  _sanitize(token.phonetic),
                  _sanitize(token.node_type),
              ])
              lines.append(fields)
          return "\n".join(lines)
      """;

   readonly PythonObjectWrapper _wrapper;

   public JNTokenizer()
   {
      _wrapper = PythonEnvironment.Use(() =>
      {
         var module = PyModule.FromString("janome_tokenizer_wrapper", WrapperPythonCode);
         return new PythonObjectWrapper(module);
      });
   }

   public JNTokenizeResult Tokenize(string text, string? cachedSerializedTokens = null)
   {
      // Apparently janome does not fully understand that invisible spaces are word separators,
      // so we replace them with ordinary spaces since they are not anything that should need to be parsed
      var sanitizedText = text.Replace(StringExtensions.InvisibleSpace, JNToken.SplitterTokenText);

      foreach(var character in CharactersThatMayConfuseJanomeSoWeReplaceThemWithOrdinaryFullWidthSpaces)
      {
         sanitizedText = sanitizedText.Replace(character, " ");
      }

      // Use cached serialized tokens if available, otherwise call Python (the expensive part)
      var serialized = cachedSerializedTokens ?? _monitor.Read(() => _wrapper.Use(module => (string)module.tokenize_to_string(sanitizedText)));

      var jnTokens = ParseSerializedTokens(serialized);

      // Link tokens with previous/next pointers
      for(var i = 0; i < jnTokens.Count; i++)
      {
         if(i > 0)
         {
            jnTokens[i].Previous = jnTokens[i - 1];
         }

         if(i < jnTokens.Count - 1)
         {
            jnTokens[i].Next = jnTokens[i + 1];
         }
      }

      return new JNTokenizeResult(new JNTokenizedText(text, jnTokens), serialized);
   }

   static List<JNToken> ParseSerializedTokens(string serialized)
   {
      if(string.IsNullOrEmpty(serialized))
         return [];

      var lines = serialized.Split('\n');
      var result = new List<JNToken>(lines.Length);

      foreach(var line in lines)
      {
         if(line.Length == 0) continue;

         var fields = line.Split(FieldSeparator);
         // Fields: 0=part_of_speech, 1=base_form, 2=surface, 3=infl_type, 4=infl_form, 5=reading, 6=phonetic, 7=node_type
         var partsOfSpeech = JNPartsOfSpeech.Fetch(fields[0]);

         result.Add(new JNToken(
                       partsOfSpeech,
                       baseForm: fields[1],
                       surface: fields[2],
                       inflectionType: fields[3],
                       inflectedForm: fields[4],
                       reading: fields[5],
                       phonetic: fields[6],
                       nodeType: fields[7]
                    ));
      }

      return result;
   }
}
