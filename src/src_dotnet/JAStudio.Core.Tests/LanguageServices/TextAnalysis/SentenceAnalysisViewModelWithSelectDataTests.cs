using System;
using System.Collections.Generic;
using JAStudio.Core.LanguageServices.JanomeEx.WordExtraction;
using JAStudio.Core.Note;
using JAStudio.Core.Tests.Fixtures;
using Xunit;
using static JAStudio.Core.Tests.LanguageServices.TextAnalysis.SentenceAnalysisViewModelCommon;

namespace JAStudio.Core.Tests.LanguageServices.TextAnalysis;

/// <summary>
/// Tests ported from test_sentence_analysis_viewmodel_with_select_data.py
/// </summary>
public class SentenceAnalysisViewModelWithSelectDataTests : IDisposable
{
    private readonly IDisposable _collectionScope;

    public SentenceAnalysisViewModelWithSelectDataTests()
    {
        _collectionScope = CollectionFactory.InjectCollectionWithSelectData(specialVocab: true);
    }

    public void Dispose()
    {
        _collectionScope.Dispose();
    }

    // test_new_stuff - empty parametrize, no tests to port

    [Theory]
    [MemberData(nameof(RequireForbidTePrefixOrStemData))]
    public void RequireForbidTePrefixOrStem(string sentence, List<string> expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput);
    }

    public static IEnumerable<object[]> RequireForbidTePrefixOrStemData()
    {
        yield return new object[] { "座っているのはいただけない", new List<string> { "座る", "ている", "の", "は", "いただける:acceptable", "ない" } };
        yield return new object[] { "お金を貸していただけないでしょうか", new List<string> { "お金", "を", "貸す", "て", "いただける:able-to", "ない", "でしょうか" } };
        yield return new object[] { "お腹空かしてない", new List<string> { "お腹", "空かす", "てない" } };
        yield return new object[] { "さっき殴ったから拗ねてんのか", new List<string> { "さっき", "殴る", "た", "から", "拗ねる", "てん", "のか" } };
        yield return new object[] { "言っとる", new List<string> { "言う", "とる:progressive" } };
        yield return new object[] { "何言っとんだ", new List<string> { "何", "言う", "とん", "んだ:past" } };
        yield return new object[] { "長居してしまいまして", new List<string> { "長居", "する", "てしまいます", "て" } };
        yield return new object[] { "天気がよくて", new List<string> { "天気", "が", "よい", "て" } };
        yield return new object[] { "馴染めないでいる", new List<string> { "馴染む", "える", "ない", "でいる" } };
    }

    [Theory]
    [MemberData(nameof(RequiresEStemData))]
    public void RequiresEStem(string sentence, List<string> expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput);
    }

    public static IEnumerable<object[]> RequiresEStemData()
    {
        yield return new object[] { "寝れない", new List<string> { "寝る", "れない" } };
        yield return new object[] { "食べれる", new List<string> { "食べる", "れる:ichidan", "る:う" } };
    }

    [Theory]
    [MemberData(nameof(WbrWordSeparationData))]
    public void WbrWordSeparation(string sentence, List<string> expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput);
    }

    public static IEnumerable<object[]> WbrWordSeparationData()
    {
        yield return new object[] { "おっせぇ<wbr>な　あいつら", new List<string> { "おる", "せ", "ぇ:[MISSING]:emergency", "な:s.end", "あいつら" } };
        yield return new object[] { "何て言うか<wbr>さ", new List<string> { "何", "て言うか:ていうか", "さ" } };
        yield return new object[] { "だったら普通に金<wbr>貸せって言えよ", new List<string> { "だったら", "普通に", "金", "貸す", "え", "って言う", "え", "よ" } };
    }

    [Theory]
    [MemberData(nameof(RequireForbidDictionaryFormPrefixAndStemData))]
    public void RequireForbidDictionaryFormPrefixAndStem(string sentence, List<string> expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput);
    }

    public static IEnumerable<object[]> RequireForbidDictionaryFormPrefixAndStemData()
    {
        yield return new object[] { "食べるな", new List<string> { "食べる", "る:う", "な:dict" } };
        yield return new object[] { "食べな", new List<string> { "食べる", "な:masu" } };
        yield return new object[] { "そうだな", new List<string> { "そうだ", "な:s.end" } };
        yield return new object[] { "頭突き以外でな", new List<string> { "頭突き", "以外", "で", "な:s.end" } };
        yield return new object[] { "胸あるよ", new List<string> { "胸", "ある", "う", "よ" } };
        yield return new object[] { "和むし", new List<string> { "和む", "う", "し" } };
        yield return new object[] { "デカいな", new List<string> { "デカい", "な:masu" } };
    }

    [Theory]
    [MemberData(nameof(DictionaryFormSplittingData))]
    public void DictionaryFormSplitting(string sentence, List<string> expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput);
    }

    public static IEnumerable<object[]> DictionaryFormSplittingData()
    {
        yield return new object[] { "なる", new List<string> { "なる", "う" } };
        yield return new object[] { "する", new List<string> { "する", "る:う" } };
        yield return new object[] { "くる", new List<string> { "くる", "う" } };
        yield return new object[] { "食べる", new List<string> { "食べる", "る:う" } };
        yield return new object[] { "はしゃいでる", new List<string> { "はしゃぐ", "でる" } };
        yield return new object[] { "音がするの", new List<string> { "音がする", "うの" } };
        yield return new object[] { "大声出すな", new List<string> { "大声出す", "う", "な:dict" } };
        yield return new object[] { "があるの", new List<string> { "がある", "うの" } };
        yield return new object[] { "にある", new List<string> { "に", "ある", "う" } };
        yield return new object[] { "なぜかというと", new List<string> { "なぜかというと" } };
        yield return new object[] { "止めるかな", new List<string> { "止める", "る:う", "かな" } };
    }

    [Theory]
    [MemberData(nameof(ForbidAdverbStemData))]
    public void ForbidAdverbStem(string sentence, List<string> expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput);
    }

    public static IEnumerable<object[]> ForbidAdverbStemData()
    {
        yield return new object[] { "考えすぎ", new List<string> { "考えすぎ" } };
        yield return new object[] { "難しく考えすぎ", new List<string> { "難しい", "考える", "すぎ" } };
    }

    [Theory]
    [MemberData(nameof(RequiresMasuStemData))]
    public void RequiresMasuStem(string sentence, List<string> expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput);
    }

    public static IEnumerable<object[]> RequiresMasuStemData()
    {
        yield return new object[] { "平日に切れないよう", new List<string> { "平日", "に", "切れる", "ない", "よう" } };
        yield return new object[] { "償いきれない", new List<string> { "償い", "きれない" } };
    }

    [Theory]
    [MemberData(nameof(HideAllCompoundsData))]
    public void HideAllCompounds(string sentence, List<string> expectedOutput)
    {
        try
        {
            App.Config().HideAllCompounds.SetValue(true);
            AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput);
        }
        finally
        {
            App.Config().HideAllCompounds.SetValue(false);
        }
    }

    public static IEnumerable<object[]> HideAllCompoundsData()
    {
        yield return new object[] { "教えにしたがって", new List<string> { "教え", "に", "したがって" } };
    }

    [Theory]
    [MemberData(nameof(HideTransparentCompoundsData))]
    public void HideTransparentCompounds(string sentence, List<string> expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput);
    }

    public static IEnumerable<object[]> HideTransparentCompoundsData()
    {
        yield return new object[] { "外出中", new List<string> { "外出", "中" } };
        yield return new object[] { "買い替えています", new List<string> { "買い替える", "ている", "ます" } };
    }

    [Theory]
    [MemberData(nameof(GodanPotentialAndImperativeData))]
    public void GodanPotentialAndImperative(string sentence, List<string> expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput);
    }

    public static IEnumerable<object[]> GodanPotentialAndImperativeData()
    {
        yield return new object[] { "お金貸せって", new List<string> { "お金", "貸す", "え", "って" } };
        yield return new object[] { "お前に会えて", new List<string> { "お前", "に会う", "える", "て" } };
        yield return new object[] { "逆に大丈夫に思えてくる", new List<string> { "逆に", "大丈夫", "に", "思える", "て", "くる", "る:う" } };
        yield return new object[] { "黙れ", new List<string> { "黙る", "え" } };
        yield return new object[] { "楽しめてる", new List<string> { "楽しむ", "える", "てる" } };
        yield return new object[] { "会えたりしない", new List<string> { "会う", "える", "たり", "する", "ない" } };
        yield return new object[] { "くれよ", new List<string> { "くれる", "え", "よ" } };
        yield return new object[] { "放せよ　俺は…", new List<string> { "放す", "え", "よ", "俺", "は" } };
        yield return new object[] { "出ていけ", new List<string> { "出ていく", "え" } };
        yield return new object[] { "進めない", new List<string> { "進める", "ない" } };
        yield return new object[] { "さっさと傷を清めてこい", new List<string> { "さっさと:[MISSING]:emergency", "傷", "を", "清める", "てこ", "い" } };
        yield return new object[] { "清めの一波", new List<string> { "清め", "の", "一波:[MISSING]:emergency" } };
        yield return new object[] { "ここは清められ", new List<string> { "ここ", "は", "清める", "られる" } };
        yield return new object[] { "その物陰に隠れろ", new List<string> { "その", "物陰", "に", "隠れる", "ろ" } };
        yield return new object[] { "聞けよ", new List<string> { "聞え", "よ" } };
        yield return new object[] { "返せったら", new List<string> { "返す", "え", "ったら" } };
        yield return new object[] { "返せ俺の", new List<string> { "返す", "え", "俺", "の" } };
        yield return new object[] { "返せ盗人", new List<string> { "返す", "え", "盗人" } };
        yield return new object[] { "カバンに入れっぱなし", new List<string> { "カバン", "に", "入れる", "っぱなし:っ放し" } };
        yield return new object[] { "綺麗 母様に見せよう", new List<string> { "綺麗", "母様", "に", "見せる", "う" } };
    }

    [Theory]
    [MemberData(nameof(IchidanImperativeData))]
    public void IchidanImperative(string sentence, List<string> expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput);
    }

    public static IEnumerable<object[]> IchidanImperativeData()
    {
        yield return new object[] { "食べろ", new List<string> { "食べる", "ろ" } };
        yield return new object[] { "食べよ", new List<string> { "食べる", "よ" } };
        yield return new object[] { "見つけよ", new List<string> { "見つける", "よ" } };
        yield return new object[] { "捕まえよ", new List<string> { "捕まえる", "よ" } };
        yield return new object[] { "離れよ", new List<string> { "離れる", "よ" } };
        yield return new object[] { "落ち着け！", new List<string> { "落ち着く", "え" } };
        yield return new object[] { "食べよう", new List<string> { "食べる", "う" } };
    }

    [Theory]
    [MemberData(nameof(IImperativeFormsData))]
    public void IImperativeForms(string sentence, List<string> expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput);
    }

    public static IEnumerable<object[]> IImperativeFormsData()
    {
        yield return new object[] { "書きなさい", new List<string> { "書く", "なさい" } };
    }

    // test_bugs_todo_fixme - empty parametrize, no tests to port

    [Theory]
    [MemberData(nameof(MiscStuffData))]
    public void MiscStuff(string sentence, List<string> expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput);
    }

    public static IEnumerable<object[]> MiscStuffData()
    {
        yield return new object[] { "厳密に言えば　俺一人が友達だけど", new List<string> { "厳密に言えば", "俺", "一人", "が", "友達", "だけど" } };
        yield return new object[] { "厳密に言えば　俺一人が友達だけどだけど", new List<string> { "厳密に言えば", "俺", "一人", "が", "友達", "だけど", "だけど" } };
        yield return new object[] { "幼すぎて よく覚えていないけど", new List<string> { "幼い", "すぎる", "て", "よく", "覚える", "ている", "ない", "けど" } };
        yield return new object[] { "ばら撒かれるなんて死んでもいやだ", new List<string> { "ばら撒く", "あれる", "る:う", "なんて", "死んでも", "いや", "だ" } };
        yield return new object[] { "お前も色々考えてるんだなぁ", new List<string> { "お前", "も", "色々", "考える", "てる", "んだ:のだ", "なぁ" } };
        yield return new object[] { "教科書落ちちゃうから", new List<string> { "教科書", "落ちる", "ちゃう", "う", "から" } };
        yield return new object[] { "待ってました", new List<string> { "待つ", "て", "ます", "た" } };
        yield return new object[] { "落ちてないかな", new List<string> { "落ちる", "てない", "かな" } };
        yield return new object[] { "分かってたら", new List<string> { "分かる", "てたら" } };
        yield return new object[] { "思い出せそうな気がする", new List<string> { "思い出す", "える", "そうだ", "気がする", "る:う" } };
        yield return new object[] { "代筆を頼みたいんだが", new List<string> { "代筆", "を", "頼む", "たい", "ん", "だが" } };
        yield return new object[] { "飛ばされる", new List<string> { "飛ばす", "あれる", "る:う" } };
        yield return new object[] { "破られたか", new List<string> { "破る", "あれる", "た", "か" } };
        yield return new object[] { "大家族だもの", new List<string> { "大家族", "だもの" } };
        yield return new object[] { "奪うんだもの", new List<string> { "奪う", "う", "ん", "だもの" } };
        yield return new object[] { "やり過ぎた", new List<string> { "やり過ぎる", "た" } };
        yield return new object[] { "ない", new List<string> { "ない" } };
        yield return new object[] { "俺に謝られても", new List<string> { "俺", "に", "謝る", "あれても" } };
        yield return new object[] { "いいのかよ", new List<string> { "いい", "のか", "よ" } };
        yield return new object[] { "立ってるのかと思った", new List<string> { "立つ", "てる", "のか", "と思う", "た" } };
        yield return new object[] { "ないと思う", new List<string> { "ない", "と思う", "う" } };
        yield return new object[] { "しても", new List<string> { "する", "ても" } };
        yield return new object[] { "見えなくなったって そんな", new List<string> { "見える", "なくなる", "たって:emergency", "そんな" } };
        yield return new object[] { "焼けたかな", new List<string> { "焼ける", "た", "かな" } };
        yield return new object[] { "また来ような", new List<string> { "また", "来る", "う", "な:s.end" } };
        yield return new object[] { "何なんだろうな", new List<string> { "何だ", "ん", "だろう", "な:s.end" } };
        yield return new object[] { "存在したね", new List<string> { "存在", "する", "た", "ね" } };
        yield return new object[] { "作るに決まってるだろ", new List<string> { "作る", "う", "に決まってる", "だろ" } };
        yield return new object[] { "知らないんでしょう", new List<string> { "知らない", "ん", "でしょう" } };
        yield return new object[] { "横取りされたらたまらん", new List<string> { "横取り", "される", "たら", "たまらん" } };
        yield return new object[] { "ガチだったんでしょ", new List<string> { "ガチ", "だった", "ん", "でしょ" } };
        yield return new object[] { "どうしちゃったんだろうな", new List<string> { "どう", "しちゃう", "たん:たの", "だろう", "な:s.end" } };
        yield return new object[] { "良いものを食べる", new List<string> { "良い", "もの", "を", "食べる", "る:う" } };
        yield return new object[] { "いいものを食べる", new List<string> { "いい", "もの", "を", "食べる", "る:う" } };
        yield return new object[] { "うまく笑えずに", new List<string> { "うまく", "笑える", "ずに" } };
        yield return new object[] { "慣れているんでね", new List<string> { "慣れる", "ている", "んで", "ね" } };
        yield return new object[] { "私が頼んだの", new List<string> { "私", "が", "頼む", "んだ:past", "の" } };
        yield return new object[] { "月光が差し込んでるんだ", new List<string> { "月光", "が", "差し込む", "んでる", "んだ:のだ" } };
        yield return new object[] { "悪かったって", new List<string> { "悪い", "た", "って" } };
        yield return new object[] { "落としたって何を", new List<string> { "落とす", "た", "って", "何", "を" } };
        yield return new object[] { "行ったって話", new List<string> { "行く", "たって:emergency", "話" } };
        yield return new object[] { "会いに行ったんだ", new List<string> { "会う", "に行く", "たんだ" } };
        yield return new object[] { "聞こうと思ってた", new List<string> { "聞く", "う", "と思う", "てた" } };
        yield return new object[] { "沈んで", new List<string> { "沈む", "んで" } };
        yield return new object[] { "死んどる", new List<string> { "死ぬ", "んどる" } };
        yield return new object[] { "ちょっと強引なところがあるから", new List<string> { "ちょっと", "強引", "な", "ところ", "がある", "う", "から" } };
        yield return new object[] { "また寒くなるな", new List<string> { "また", "寒い", "くなる", "う", "な:dict" } };
        yield return new object[] { "空を飛べる機械", new List<string> { "空を飛ぶ", "える", "る:う", "機械" } };
        yield return new object[] { "出会える", new List<string> { "出会える", "る:う" } };
        yield return new object[] { "頑張れた", new List<string> { "頑張る", "える", "た" } };
        yield return new object[] { "頑張れ", new List<string> { "頑張れ" } };
        yield return new object[] { "私たちなら嘘をつかずに付き合っていけるかもしれないね", new List<string> { "私たち", "なら", "嘘をつく", "ずに", "付き合う", "ていける", "る:う", "かもしれない", "ね" } };
        yield return new object[] { "どやされても知らんぞ", new List<string> { "どやす", "あれる", "ても知らん:ても知らない", "ぞ" } };
        yield return new object[] { "服を引き出しの中に入れてください", new List<string> { "服", "を", "引き出し", "の中", "に入る", "える", "て", "ください" } };
        yield return new object[] { "他人を気遣い", new List<string> { "他人", "を", "気遣う" } };
        yield return new object[] { "まだ割れんのか", new List<string> { "まだ", "割れる", "のか" } };
        yield return new object[] { "思えないしな", new List<string> { "思える", "ない", "しな" } };
    }

    [Theory]
    [MemberData(nameof(YieldToSurfaceData))]
    public void YieldToSurface(string sentence, List<string> expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, new List<WordExclusion>(), expectedOutput);
    }

    public static IEnumerable<object[]> YieldToSurfaceData()
    {
        yield return new object[] { "しろ", new List<string> { "しろ" } };
        yield return new object[] { "後で下に下りてらっしゃいね", new List<string> { "後で", "下に", "下りる", "て", "らっしゃい", "ね" } };
    }

    [Theory]
    [MemberData(nameof(ExclusionsData))]
    public void Exclusions(string sentence, List<WordExclusion> excluded, List<string> expectedOutput)
    {
        AssertDisplayWordsEqualAndThatAnalysisInternalStateIsValid(sentence, excluded, expectedOutput);
    }

    public static IEnumerable<object[]> ExclusionsData()
    {
        yield return new object[]
        {
            "厳密に言えば　俺一人が友達だけど",
            new List<WordExclusion> { WordExclusion.Global("厳密に言えば"), WordExclusion.Global("言え"), WordExclusion.Global("だけど") },
            new List<string> { "厳密", "に", "言う", "ば", "俺", "一人", "が", "友達", "だ", "けど" }
        };
        yield return new object[]
        {
            "厳密に言えばだけど俺一人が友達だけど",
            new List<WordExclusion> { WordExclusion.AtIndex("だけど", 6) },
            new List<string> { "厳密に言えば", "俺", "一人", "が", "友達", "だけど" }
        };
        yield return new object[]
        {
            "私は毎日ジョギングをすることを習慣にしています。",
            new List<WordExclusion>
            {
                WordExclusion.AtIndex("にして", 17),
                WordExclusion.AtIndex("にし", 17),
                WordExclusion.AtIndex("して", 18),
                WordExclusion.AtIndex("し", 18),
                WordExclusion.AtIndex("してい", 18),
                WordExclusion.AtIndex("い", 12),
                WordExclusion.Global("にする")
            },
            new List<string> { "私", "は", "毎日", "ジョギング", "を", "する", "る:う", "こと", "を", "習慣", "に", "する", "ている", "ます" }
        };
        yield return new object[]
        {
            "私は毎日ジョギングをすることを習慣にしています。",
            new List<WordExclusion>
            {
                WordExclusion.AtIndex("にして", 17),
                WordExclusion.AtIndex("にし", 17),
                WordExclusion.AtIndex("して", 18),
                WordExclusion.AtIndex("し", 18),
                WordExclusion.AtIndex("してい", 18)
            },
            new List<string> { "私", "は", "毎日", "ジョギング", "を", "する", "る:う", "こと", "を", "習慣", "にする", "ている", "ます" }
        };
        yield return new object[]
        {
            "頑張れたというか",
            new List<WordExclusion> { WordExclusion.Global("頑張る"), WordExclusion.Global("頑張れ") },
            new List<string> { "える", "た", "というか" }
        };
        yield return new object[]
        {
            "いらっしゃいません",
            new List<WordExclusion> { WordExclusion.Global("いらっしゃいませ") },
            new List<string> { "いらっしゃいます", "ん" }
        };
        yield return new object[]
        {
            "風の強さに驚きました",
            new List<WordExclusion> { WordExclusion.Global("風の強い") },
            new List<string> { "風", "の", "強さ", "に", "驚き", "ます", "た" }
        };
    }

    [Theory]
    [MemberData(nameof(AllWordsEqualData))]
    public void AllWordsEqual(string sentence, List<string> expectedOutput)
    {
        AssertAllWordsEqual(sentence, expectedOutput);
    }

    public static IEnumerable<object[]> AllWordsEqualData()
    {
        yield return new object[]
        {
            "風の強さに驚きました",
            new List<string> { "風の強い", "風", "の", "強さ", "強", "強い", "さ", "に", "驚き", "驚く", "まし:ませ", "まし", "ます", "た" }
        };
    }
}
