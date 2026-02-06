using System.Collections.Generic;
using JAStudio.Core.LanguageServices;
using JAStudio.Core.TestUtils;
using Xunit;

namespace JAStudio.Core.Tests.LanguageServices;

public class ConjugationBaseTests : TestStartingWithEmptyCollection
{
    [Theory]
    // irregular verbs
    [InlineData("くる", new[] { "き", "こ", "くれ", "き" })]
    [InlineData("する", new[] { "し", "さ", "すれ", "し", "せ" })]
    [InlineData("いく", new[] { "いき", "いか", "いけ", "いっ", "いこ" })]
    [InlineData("行く", new[] { "行き", "行か", "行け", "行っ", "行こ" })]
    [InlineData("います", new[] { "いまし", "いませ" })]
    [InlineData("しようとする", new[] { "しようとし", "しようとさ", "しようとすれ", "しようとし", "しようとせ" })]
    [InlineData("おいてくる", new[] { "おいてき", "おいてこ", "おいてくれ", "おいてき" })]
    public void IrregularVerbs(string word, string[] conjugationBases)
    {
        RunTests(word, conjugationBases);
    }

    [Theory]
    [InlineData("食べる", new[] { "食べり", "食べら", "食べれ", "食べっ", "食べ", "食べろ", "食べな" }, false)]
    [InlineData("食べる", new[] { "食べ", "食べろ", "食べな" }, true)]
    public void Ichidan(string word, string[] conjugationBases, bool isIchidan)
    {
        RunTests(word, conjugationBases, isIchidan);
    }

    [Theory]
    // adjectives
    [InlineData("美味しい", new[] { "美味しく", "美味しけ", "美味しか" })]
    // irregular adjective
    [InlineData("いい", new[] { "よく", "よけ", "よか", "よかっ" })]
    public void Adjectives(string word, string[] conjugationBases)
    {
        RunTests(word, conjugationBases);
    }

    [Theory]
    // aru verbs
    [InlineData("なさる", new[] { "なさい", "なさら", "なされ", "なさっ" })]
    [InlineData("くださる", new[] { "ください", "くださら", "くだされ", "くださっ" })]
    [InlineData("いらっしゃる", new[] { "いらっしゃい", "いらっしゃら", "いらっしれば", "いらっしゃっ" })]
    [InlineData("おっしゃる", new[] { "おっしゃい", "おっしゃら", "おっしれば", "おっしゃっ" })]
    [InlineData("ござる", new[] { "ござい", "ござら", "ござれ", "ござっ" })]
    public void AruVerbs(string word, string[] conjugationBases)
    {
        RunTests(word, conjugationBases);
    }

    [Theory]
    // unknown godan verbs should add the ichidan endings
    [InlineData("走る", new[] { "走り", "走ら", "走れ", "走っ", "走", "走ろ", "走な" })]
    [InlineData("帰る", new[] { "帰り", "帰ら", "帰れ", "帰っ", "帰", "帰ろ", "帰な" })]
    // ordinary godan
    [InlineData("使う", new[] { "使い", "使わ", "使え", "使っ" })]
    [InlineData("書く", new[] { "書き", "書か", "書け", "書い" })]
    [InlineData("立つ", new[] { "立ち", "立た", "立て", "立っ" })]
    [InlineData("死ぬ", new[] { "死に", "死な", "死ね", "死ん" })]
    [InlineData("飛ぶ", new[] { "飛び", "飛ば", "飛べ", "飛ん" })]
    [InlineData("読む", new[] { "読み", "読ま", "読め", "読ん" })]
    public void UnknownGodan(string word, string[] conjugationBases)
    {
        RunTests(word, conjugationBases);
    }

    [Theory]
    // godan verbs
    [InlineData("走る", new[] { "走り", "走ら", "走れ", "走っ" })]
    [InlineData("帰る", new[] { "帰り", "帰ら", "帰れ", "帰っ" })]
    [InlineData("使う", new[] { "使い", "使わ", "使え", "使っ" })]
    [InlineData("書く", new[] { "書き", "書か", "書け", "書い" })]
    [InlineData("立つ", new[] { "立ち", "立た", "立て", "立っ" })]
    [InlineData("死ぬ", new[] { "死に", "死な", "死ね", "死ん" })]
    [InlineData("飛ぶ", new[] { "飛び", "飛ば", "飛べ", "飛ん" })]
    [InlineData("読む", new[] { "読み", "読ま", "読め", "読ん" })]
    public void KnownGodan(string word, string[] conjugationBases)
    {
        RunTests(word, conjugationBases, isIchidan: false, isGodan: true);
    }

    static void RunTests(string word, string[] conjugationBases, bool isIchidan = false, bool isGodan = false)
    {
        var result = Conjugator.GetWordStems(word, isIchidan, isGodan);
        Assert.Equal(conjugationBases, result);

        if (conjugationBases.Length > 1)
        {
            var iStem = Conjugator.GetIStem(word, isIchidan, isGodan);
            Assert.Equal(conjugationBases[0], iStem);
        }

        if (isIchidan)
        {
            return;
        }

        if (conjugationBases.Length > 2)
        {
            var aStem = Conjugator.GetAStem(word, isIchidan, isGodan);
            Assert.Equal(conjugationBases[1], aStem);
        }

        if (conjugationBases.Length > 3)
        {
            var eStem = Conjugator.GetEStem(word, isIchidan, isGodan);
            Assert.Equal(conjugationBases[2], eStem);
        }

        if (conjugationBases.Length > 4)
        {
            var teStem = Conjugator.GetTeStem(word, isIchidan, isGodan);
            Assert.Equal(conjugationBases[3], teStem);
        }
    }
}
