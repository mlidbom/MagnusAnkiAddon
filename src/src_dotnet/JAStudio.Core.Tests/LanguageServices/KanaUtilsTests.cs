using JAStudio.Core.LanguageServices;
using JAStudio.PythonInterop.Utilities;
using Xunit;

namespace JAStudio.Core.Tests.LanguageServices;

public class KanaUtilsTests
{
    public KanaUtilsTests()
    {
        PythonEnvironment.EnsureInitialized();
    }

    // Ported from test_kana_utils.py
    [Theory]
    [InlineData("かな", "kana", "かな", "カナ")]
    [InlineData("かく", "kaku", "かく", "カク")]
    [InlineData("かく はく", "kaku haku", "かく はく", "カク ハク")]
    [InlineData("ジャッツ", "jattsu", "じゃっつ", "ジャッツ")]
    [InlineData("じゃっつ", "jattsu", "じゃっつ", "ジャッツ")]
    [InlineData("ジャッ", "ja", "じゃ", "ジャ")]
    [InlineData("じゃっ", "ja", "じゃ", "ジャ")]
    [InlineData("キャク", "kyaku", "きゃく", "キャク")]
    [InlineData("チャ", "cha", "ちゃ", "チャ")]
    public void RomajiKanaRoundtripping(string kana, string expectedRomaji, string expectedHiragana, string expectedKatakana)
    {
        var romaji = KanaUtils.Romanize(kana);
        Assert.Equal(expectedRomaji, romaji);
        Assert.Equal(expectedHiragana, KanaUtils.RomajiToHiragana(romaji));
        Assert.Equal(expectedKatakana, KanaUtils.RomajiToKatakana(romaji));
    }

    [Fact]
    public void Should_Convert_Hiragana_To_Katakana()
    {
        // Arrange
        var hiragana = "ひらがな";

        // Act
        var katakana = KanaUtils.HiraganaToKatakana(hiragana);

        // Assert
        Assert.Equal("ヒラガナ", katakana);
    }

    [Fact]
    public void Should_Convert_Katakana_To_Hiragana()
    {
        // Arrange
        var katakana = "カタカナ";

        // Act
        var hiragana = KanaUtils.KatakanaToHiragana(katakana);

        // Assert
        Assert.Equal("かたかな", hiragana);
    }

    [Fact]
    public void Should_Romanize_Japanese_Text()
    {
        // Arrange
        var japanese = "こんにちは";

        // Act
        var romaji = KanaUtils.Romanize(japanese);

        // Assert - pykakasi uses "ha" for は in this context
        Assert.Equal("konnichiha", romaji);
    }

    [Fact]
    public void Should_Handle_Trailing_Small_Tsu()
    {
        // Arrange
        var japanese = "ちょっ";

        // Act
        var romaji = KanaUtils.Romanize(japanese);

        // Assert - small tsu at end should be removed before romanization
        Assert.Equal("cho", romaji);
    }

    [Fact]
    public void Should_Convert_Romaji_To_Hiragana()
    {
        // Arrange
        var romaji = "konnichiwa";

        // Act
        var hiragana = KanaUtils.RomajiToHiragana(romaji);

        // Assert - romkan doesn't double 'n' before certain consonants
        Assert.Equal("こんいちわ", hiragana);
    }

    [Fact]
    public void Should_Convert_Romaji_To_Katakana()
    {
        // Arrange
        var romaji = "konnichiwa";

        // Act
        var katakana = KanaUtils.RomajiToKatakana(romaji);

        // Assert - romkan doesn't double 'n' before certain consonants
        Assert.Equal("コンイチワ", katakana);
    }

    [Fact]
    public void Should_Detect_Hiragana()
    {
        Assert.True(KanaUtils.CharacterIsHiragana('あ'));
        Assert.False(KanaUtils.CharacterIsHiragana('ア'));
        Assert.False(KanaUtils.CharacterIsHiragana('漢'));
    }

    [Fact]
    public void Should_Detect_Katakana()
    {
        Assert.True(KanaUtils.CharacterIsKatakana('ア'));
        Assert.False(KanaUtils.CharacterIsKatakana('あ'));
        Assert.False(KanaUtils.CharacterIsKatakana('漢'));
    }

    [Fact]
    public void Should_Detect_Kana()
    {
        Assert.True(KanaUtils.CharacterIsKana('あ'));
        Assert.True(KanaUtils.CharacterIsKana('ア'));
        Assert.False(KanaUtils.CharacterIsKana('漢'));
    }

    [Fact]
    public void Should_Detect_Kanji()
    {
        Assert.True(KanaUtils.CharacterIsKanji('漢'));
        Assert.False(KanaUtils.CharacterIsKanji('あ'));
        Assert.False(KanaUtils.CharacterIsKanji('ア'));
    }

    [Fact]
    public void Should_Check_IsOnlyKana()
    {
        Assert.True(KanaUtils.IsOnlyKana("あいうえお"));
        Assert.True(KanaUtils.IsOnlyKana("アイウエオ"));
        Assert.True(KanaUtils.IsOnlyKana("あいうアイウ"));
        Assert.False(KanaUtils.IsOnlyKana("あい漢字"));
    }

    [Fact]
    public void Should_Extract_Kanji()
    {
        // Arrange
        var text = "今日は良い天気です";

        // Act
        var kanji = KanaUtils.ExtractKanji(text);

        // Assert
        Assert.Equal(new[] { "今", "日", "良", "天", "気" }, kanji);
    }

    [Fact]
    public void Should_Convert_Anything_To_Hiragana_From_Kana()
    {
        // Arrange
        var katakana = "カタカナ";

        // Act
        var hiragana = KanaUtils.AnythingToHiragana(katakana);

        // Assert
        Assert.Equal("かたかな", hiragana);
    }

    [Fact]
    public void Should_Convert_Anything_To_Hiragana_From_Romaji()
    {
        // Arrange
        var romaji = "konnichiwa";

        // Act
        var hiragana = KanaUtils.AnythingToHiragana(romaji);

        // Assert - romkan doesn't double 'n' before certain consonants
        Assert.Equal("こんいちわ", hiragana);
    }
}
