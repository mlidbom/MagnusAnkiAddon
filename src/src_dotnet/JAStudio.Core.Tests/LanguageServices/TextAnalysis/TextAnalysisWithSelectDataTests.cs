using System;
using System.Collections.Generic;
using System.Linq;
using JAStudio.Core.Note;
using JAStudio.Core.Tests.Fixtures;
using Xunit;

namespace JAStudio.Core.Tests.LanguageServices.TextAnalysis;

/// <summary>
/// Tests ported from test_text_analysis_with_select_data.py
/// </summary>
public class TextAnalysisWithSelectDataTests : IDisposable
{
    private readonly IDisposable _collectionScope;

    public TextAnalysisWithSelectDataTests()
    {
        _collectionScope = CollectionFactory.InjectCollectionWithSelectData(specialVocab: true);
    }

    public void Dispose()
    {
        _collectionScope.Dispose();
    }

    // test_new_stuff - empty parametrize, no tests to port

    [Theory]
    [InlineData("走る", "う", "走る")]
    [InlineData("走って", "て", "走る")]
    [InlineData("これをください。", "い", "くださる", "ください", "これ", "を")]
    [InlineData("ハート形", "ハート", "ハート形", "形")]
    [InlineData("私が行きましょう。", "う", "が", "ましょ", "ましょう", "ます", "私", "行き", "行く")]
    [InlineData("１人でいる時間がこれほどまでに長く感じるとは", "１", "１人", "１人で", "いる", "が", "これ", "これほど", "で", "でいる", "と", "とは", "に", "は", "ほど", "まで", "までに", "る", "人", "時間", "感じる", "長い")]
    [InlineData("どうやってここを知った。", "ここ", "た", "て", "どう", "どうやって", "やる", "を", "知る")]
    [InlineData("彼の日本語のレベルは私と同じ位だ。", "と", "だ", "の", "は", "レベル", "位", "同じ", "同じ位", "彼", "彼の", "日本語", "私")]
    [InlineData("それなのに 周りは化け物が出ることで有名だと聞き", "こと", "それなのに", "だ", "と", "で", "は", "る", "出る", "化け物", "周り", "有名", "聞き", "聞く", "が")]
    [InlineData("清めの一波", "の", "清め", "清める")]
    [InlineData("さっさと傷を清めてこい", "い", "くる", "こい", "て", "てこ", "を", "傷", "清める")]
    [InlineData("すげえ", "すげ", "すげえ")]
    [InlineData("「コーヒーはいかがですか？」「いえ、結構です。お構いなく。」", "いえ", "いかが", "お構いなく", "か", "です", "ですか", "は", "コーヒー", "結構")]
    [InlineData("解放する", "る", "する", "解放", "解放する")]
    [InlineData("落書きしたろ", "た", "する", "落書き")]
    [InlineData("なのかな", "か", "かな", "な", "なの", "の", "のか")]
    [InlineData("前だったのか", "か", "た", "たの", "だ", "だった", "の", "のか", "前")]
    [InlineData("未練たらしい", "たらしい", "未練", "未練たらしい")]
    [InlineData("作るに決まってるだろ", "う", "だ", "だろ", "てる", "に", "に決まってる", "に決まる", "作る", "決まる")]
    [InlineData("良いものを食べる", "もの", "る", "を", "良い", "食べる")]
    [InlineData("のに", "のに")]
    [InlineData("もう逃がしません", "ません", "ます", "もう", "ん", "逃がす")]
    [InlineData("死んどる", "んどる", "死ぬ")]
    [InlineData("そうよ　あんたの言うとおりよ！", "う", "そう", "とおり", "の", "よ", "あんた", "言う", "言うとおり")]
    public void IdentifyWords(string sentence, params string[] expectedOutput)
    {
        var sentenceNote = SentenceNote.CreateTestNote(sentence, "");
        var words = sentenceNote.ParsingResult.Get().ParsedWords
            .Select(w => w.ParsedForm)
            .ToHashSet()
            .OrderBy(w => w)
            .ToList();
        var expected = expectedOutput.ToHashSet().OrderBy(w => w).ToList();
        Assert.Equal(expected, words);
    }

    [Theory]
    [InlineData("言わず", "言う", "ず")]
    [InlineData("声出したら駄目だからね", "声", "出す", "たら", "駄目", "だから", "だ", "から", "ね")]
    [InlineData("無理して思い出す", "無理", "して", "する", "て", "思い出す", "思い出す", "う")]
    [InlineData("私が頼んだの", "私", "が", "頼む", "んだ", "の")]
    public void ExcludedSurfaces(string sentence, params string[] expectedOutput)
    {
        var sentenceNote = SentenceNote.CreateTestNote(sentence, "");
        var words = sentenceNote.ParsingResult.Get().ParsedWords
            .Select(w => w.ParsedForm)
            .ToList();
        Assert.Equal(expectedOutput.ToList(), words);
    }

    [Theory]
    [InlineData("うわ こわっ", "うわ", "こい", "わっ")]
    public void StrictlySuffix(string sentence, params string[] expectedOutput)
    {
        var sentenceNote = SentenceNote.CreateTestNote(sentence, "");
        var words = sentenceNote.ParsingResult.Get().ParsedWords
            .Select(w => w.ParsedForm)
            .ToList();
        Assert.Equal(expectedOutput.ToList(), words);
    }

    [Theory]
    [InlineData("うるせえ", "うるせえ", "う", "せえ", "せる")]
    [InlineData("お金貸せって", "お金", "貸す", "え", "って")]
    public void RequiresAStem(string sentence, params string[] expectedOutput)
    {
        var sentenceNote = SentenceNote.CreateTestNote(sentence, "");
        var rootWords = sentenceNote.ParsingResult.Get().ParsedWords
            .Select(w => w.ParsedForm)
            .ToList();
        Assert.Equal(expectedOutput.ToList(), rootWords);
    }

    [Fact]
    public void IgnoresNoiseCharacters()
    {
        var sentence = ". , : ; / | 。 、ー ? !";
        var expected = new HashSet<string> { "ー" };

        var sentenceNote = SentenceNote.CreateTestNote(sentence, "");
        var words = sentenceNote.ParsingResult.Get().ParsedWords
            .Select(w => w.ParsedForm)
            .ToHashSet();
        Assert.Equal(expected, words);
    }

    [Fact]
    public void ThatVocabIsNotIndexedEvenIfFormIsHighlightedIfInvalidAndThereIsAnotherValidVocabWithTheForm()
    {
        var sentence = SentenceNote.CreateTestNote("勝つんだ", "");
        sentence.Configuration.AddHighlightedWord("んだ");
        sentence.UpdateParsedWords(force: true);
        var parsingResult = sentence.ParsingResult.Get();
        var words = parsingResult.ParsedWords
            .Select(w => w.ParsedForm)
            .Distinct()
            .ToList();
        Assert.Equal(new List<string> { "勝つ", "う", "んだ", "ん", "だ" }, words);
    }

    // test_no_memory_leak_weak_references_are_disposed - Skipped
    // This test is Python-specific (tests WeakRef disposal). C# uses normal references with GC.
}
