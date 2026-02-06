using System;
using System.Collections.Generic;
using JAStudio.Core.Note;
using JAStudio.Core.Tests.Fixtures;
using Xunit;

namespace JAStudio.Core.Tests.Note;

/// <summary>
/// Tests ported from test_kanjinote.py
/// </summary>
public class KanjiNotePortedTests : CollectionUsingTest
{
   public KanjiNotePortedTests() : base(DataNeeded.Kanji) {}

   [Fact]
   public void InsideRadicalPopulation()
   {
      var inside = App.Col().Kanji.WithKanji("内")!;
      inside.SetUserMnemonic("<rad>head</rad> <rad>person</rad>");

      inside.PopulateRadicalsFromMnemonicTags();

      Assert.Equal(new List<string> { "冂", "人" }, inside.GetRadicals());
   }

   [Theory]
   [InlineData("内", "冂, 人", "<rad>head</rad> <rad>person</rad> <kan>inside</kan> <compound-reading><read>U</read>ber-<read>chi</read>mp</compound-reading> ...")]
   [InlineData("病", "疒,丙", "<rad>sick</rad> <rad>dynamite</rad> <kan>illness</kan> <read>yu</read>ck <compound-reading><read>yu</read>ck-<read>mi</read>ce</compound-reading> <read>BO</read> ...")]
   [InlineData("品", "", "<kan>goods</kan> <read>hin</read>t <compound-reading><read>shi</read>t-<read>nu</read>t</compound-reading> ...")]
   [InlineData("塚", "", "<kan>a-mound</kan> <read>Tsuka</read> ...")]
   public void BootstrapMnemonic(string kanji, string radicals, string expectedMnemonic)
   {
      var kanjiNote = App.Col().Kanji.WithKanji(kanji)!;
      kanjiNote.SetRadicals(radicals);

      kanjiNote.BootstrapMnemonicFromRadicals();

      Assert.Equal(expectedMnemonic, kanjiNote.GetUserMnemonic());
   }

   [Fact]
   public void GetPrimaryMeaning()
   {
      var one = App.Col().Kanji.WithKanji("一")!;
      Assert.Equal("ground", one.GetPrimaryRadicalMeaning());

      var hon = App.Col().Kanji.WithKanji("本")!;
      Assert.Equal("true", hon.GetPrimaryRadicalMeaning());
   }
}
