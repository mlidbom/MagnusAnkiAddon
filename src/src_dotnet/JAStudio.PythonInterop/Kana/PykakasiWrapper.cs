using System.Collections.Generic;
using JAStudio.PythonInterop.Utilities;
using Python.Runtime;

namespace JAStudio.PythonInterop.Kana;

/// <summary>
/// Wrapper for pykakasi Python library for romanization of Japanese text.
/// </summary>
public class PykakasiWrapper
{
   readonly dynamic _kakasi;

   public PykakasiWrapper()
   {
      using(PythonEnvironment.LockGil())
      {
         dynamic pykakasiModule = Py.Import("pykakasi");
         _kakasi = pykakasiModule.kakasi();
      }
   }

   /// <summary>
   /// Romanizes Japanese text (hiragana, katakana, kanji) to romaji.
   /// </summary>
   public string Romanize(string text) => PythonEnvironment.Use(() =>
   {
      if(string.IsNullOrEmpty(text))
         return string.Empty;

      // Handle trailing small tsu
      var processedText = text;
      if(text.EndsWith("っ") || text.EndsWith("ッ"))
      {
         processedText = text[..^1];
      }

      var result = _kakasi.convert(processedText);
      var parts = new List<string>();

      foreach(dynamic item in Dyn.Enumerate(result))
      {
         parts.Add((string)item["hepburn"]);
      }

      return string.Join("", parts);
   });
}
