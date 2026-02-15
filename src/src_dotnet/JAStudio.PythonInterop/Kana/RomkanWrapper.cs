using JAStudio.PythonInterop.Utilities;
using Python.Runtime;

namespace JAStudio.PythonInterop.Kana;

/// <summary>
/// Wrapper for romkan Python library for converting between romaji and kana.
/// </summary>
public class RomkanWrapper
{
   readonly dynamic _romkanModule;

   public RomkanWrapper()
   {
      using(PythonEnvironment.LockGil())
      {
         _romkanModule = Py.Import("romkan");
      }
   }

   /// <summary>
   /// Converts romaji to hiragana.
   /// </summary>
   public string ToHiragana(string romaji) => PythonEnvironment.Use(() =>
   {
      if(string.IsNullOrEmpty(romaji))
         return string.Empty;

      return (string)_romkanModule.to_hiragana(romaji);
   });

   /// <summary>
   /// Converts romaji to katakana.
   /// </summary>
   public string ToKatakana(string romaji) => PythonEnvironment.Use(() =>
   {
      if(string.IsNullOrEmpty(romaji))
         return string.Empty;

      return (string)_romkanModule.to_katakana(romaji);
   });
}
