using System.Collections.Generic;
using JAStudio.Core.Note;
using JAStudio.Core.Note.Vocabulary;

namespace JAStudio.Core.Tests.Fixtures.BaseData.SampleData;

public static class VocabLists
{
    private static readonly Tag V_QuestionOverridesForm = Tags.Vocab.QuestionOverridesForm;
    private static readonly Tag V_IsCompositionallyTransparentCompound = Tags.Vocab.IsCompositionallyTransparentCompound;
    
    private static readonly Tag VM_YieldLastToken = Tags.Vocab.Matching.YieldLastTokenToOverlappingCompound;
    private static readonly Tag VM_IsPoisonWord = Tags.Vocab.Matching.IsPoisonWord;
    private static readonly Tag VM_IsInflectingWord = Tags.Vocab.Matching.IsInflectingWord;

    private static readonly Tag VMR_DictionaryFormStem = Tags.Vocab.Matching.Requires.DictionaryFormStem;
    private static readonly Tag VMR_DictionaryFormPrefix = Tags.Vocab.Matching.Requires.DictionaryFormPrefix;
    private static readonly Tag VMR_GodanPotential = Tags.Vocab.Matching.Requires.GodanPotential;
    private static readonly Tag VMR_GodanImperative = Tags.Vocab.Matching.Requires.GodanImperative;
    private static readonly Tag VMR_IchidanImperative = Tags.Vocab.Matching.Requires.IchidanImperative;
    private static readonly Tag VMR_Irrealis = Tags.Vocab.Matching.Requires.Irrealis;
    private static readonly Tag VMR_Godan = Tags.Vocab.Matching.Requires.Godan;
    private static readonly Tag VMR_Ichidan = Tags.Vocab.Matching.Requires.Ichidan;
    private static readonly Tag VMR_TeFormStem = Tags.Vocab.Matching.Requires.TeFormStem;
    private static readonly Tag VMR_TeFormPrefix = Tags.Vocab.Matching.Requires.TeFormPrefix;
    private static readonly Tag VMR_PastTenseStem = Tags.Vocab.Matching.Requires.PastTenseStem;
    private static readonly Tag VMR_Surface = Tags.Vocab.Matching.Requires.Surface;
    private static readonly Tag VMR_SingleToken = Tags.Vocab.Matching.Requires.SingleToken;
    private static readonly Tag VMR_SentenceEnd = Tags.Vocab.Matching.Requires.SentenceEnd;
    private static readonly Tag VMR_SentenceStart = Tags.Vocab.Matching.Requires.SentenceStart;
    private static readonly Tag VMR_MasuStem = Tags.Vocab.Matching.Requires.MasuStem;

    private static readonly Tag VMF_DictionaryFormStem = Tags.Vocab.Matching.Forbids.DictionaryFormStem;
    private static readonly Tag VMF_GodanPotential = Tags.Vocab.Matching.Forbids.GodanPotential;
    private static readonly Tag VMF_GodanImperative = Tags.Vocab.Matching.Forbids.GodanImperative;
    private static readonly Tag VMF_IchidanImperative = Tags.Vocab.Matching.Forbids.IchidanImperative;
    private static readonly Tag VMF_TeFormStem = Tags.Vocab.Matching.Forbids.TeFormStem;
    private static readonly Tag VMF_TeFormPrefix = Tags.Vocab.Matching.Forbids.TeFormPrefix;
    private static readonly Tag VMF_PastTenseStem = Tags.Vocab.Matching.Forbids.PastTenseStem;
    private static readonly Tag VMF_SentenceStart = Tags.Vocab.Matching.Forbids.SentenceStart;
    private static readonly Tag VMF_SentenceEnd = Tags.Vocab.Matching.Forbids.SentenceEnd;
    private static readonly Tag VMF_Irrealis = Tags.Vocab.Matching.Forbids.Irrealis;
    private static readonly Tag VMF_PrecedingAdverb = Tags.Vocab.Matching.Forbids.PrecedingAdverb;

    public static readonly List<VocabSpec> TestSpecialVocab =
    [
        // <non-standard-token-splitting-to-enable-more-pedagogical-breakdowns-for-conjugations>
        new("う", "dictionary form verb inflection", forms: ["る"], tags: [VMR_DictionaryFormStem]),
        // godan potential
        new("える", "to-be-able-to", ["える"],
            forms: ["える", "ける", "せる", "てる", "ねる", "へる", "める", "れる", "げる", "ぜる", "でる", "べる", "ぺる"],
            tags: [VM_IsInflectingWord, VMR_GodanPotential, V_QuestionOverridesForm]),
        new("えない", "unable-able-to", ["えない"], compounds: ["える", "ない"], tags: [VM_IsInflectingWord]),
        // /godan potential
        new("え", "_!/do! (godan imperative)", ["え"], forms: ["え", "け", "せ", "ね", "へ", "め", "れ", "げ", "ぜ", "で", "べ", "ぺ"], tags: [VM_IsInflectingWord, VMR_GodanImperative, V_QuestionOverridesForm]),

        new("ろ", "_!/do! (ichidan imperative)", ["ろ"], tags: [VM_IsInflectingWord, VMR_IchidanImperative]),
        new("よ", "_!/do! (ichidan imperative)", ["よ"], tags: [VM_IsInflectingWord, VMR_IchidanImperative]),
        new("い", "_!/do! (godan-special imperative)", ["い"], tags: [VM_IsInflectingWord, VMR_GodanImperative]),

        // needs exclusion
        new("う", "volational inflection", tags: [VMF_DictionaryFormStem]),
        new("うん", tags: [VMF_DictionaryFormStem]),
        new("よ", "emphasis", ["よ"], tags: [VMF_IchidanImperative]),
        new("せよ", tags: [VMF_GodanImperative]),
        new("させる", "get-_/is-_", ["させる"], forms: ["せる"], tags: [VM_IsInflectingWord, VMF_GodanPotential]),
        new("頑張れ", "do-your-best!", tags: [VMF_GodanPotential]),
        new("あれても", forms: ["れても"], compounds: ["あれる", "ても"], tags: [VM_YieldLastToken, VMR_Irrealis, VMR_Godan, VMF_GodanPotential, V_QuestionOverridesForm]),
        new("くえ", "longtooth-grouper", tags: [VMF_GodanImperative]),
        // /needs exclusion

        // related
        new("なさる", tags: [VM_IsInflectingWord]),
        new("なさい", tags: [VM_IsInflectingWord]),
        // /related

        // compounds
        new("落ち着ける", compounds: ["落ち着く", "える"]),
        // /compounds

        // untangle offending actual dictionary entry
        new("楽しめる", compounds: ["楽しむ", "える"], tags: [VM_IsPoisonWord]),  // janome detects it as an ichidan so this sets it straight without showing the word, since it's a poison word...
        // /untangle offending actual dictionary entry

        // </non-standard-token-splitting-to-enable-more-pedagogical-breakdowns-for-conjugations>

        // infinite recursion with recursive shadowed and yielding implementetion for sentence: 服を引き出しの中に入れてください
        new("の中に", compounds: ["の中", "に"], tags: [VM_YieldLastToken]),
        new("の中", compounds: ["の", "中"]),
        new("中に", compounds: ["中", "に"]),
        new("に入る", compounds: ["に", "入る"]),
        new("入れる"),
        // infinite recursion with recursive shadowed and yielding implementetion

        // <te-stem-required>
        new("て", "{continuing-action}", ["て"], tags: [VM_IsInflectingWord, VMR_TeFormStem]),
        new("てる", tags: [VM_IsInflectingWord, VMR_TeFormStem]),
        new("とる:progressive", tags: [VM_IsInflectingWord, VMR_TeFormStem]),
        new("てん", tags: [VM_IsInflectingWord, VMR_TeFormStem]),
        new("とん", tags: [VM_IsInflectingWord, VMR_TeFormStem]),
        new("ている", "is-_-ing", readings: ["ている"], tags: [VM_IsInflectingWord, VMR_TeFormStem]),
        new("てた", "{was}-{_-ing|_ed}", ["てた"], tags: [VM_IsInflectingWord, VMR_TeFormStem]),
        new("てたら", "{was}-{_-ing|_ed}", ["てたら"], tags: [VM_IsInflectingWord, VMR_TeFormStem]),

        new("んで", "and/て", forms: ["で"], prefixIn: ["ん"], tags: [VMR_TeFormStem, V_QuestionOverridesForm]),
        new("んどる", forms: ["どる"], prefixIn: ["ん"], tags: [V_QuestionOverridesForm, VMR_TeFormStem]),
        new("んでる", forms: ["でる"], prefixIn: ["ん"], tags: [V_QuestionOverridesForm, VMR_TeFormStem]),
        // </te-stem-required>
        // <te-stem-forbidden>
        new("で", tags: [VMF_TeFormStem]),
        new("でいる", tags: [VMF_TeFormStem]),
        new("んで", "thing-is", tags: [VMF_TeFormStem]),
        new("とんだ", tags: [VMF_TeFormStem]),
        // </te-stem-forbidden>
        new("１人で", compounds: ["で", "１人"], tags: [VM_YieldLastToken]),
        new("ないで", compounds: ["ない", "で"], tags: [VM_YieldLastToken]),

        // <past-tense-required>
        new("た", "{past-tense} | (please)do", ["た"], surfaceNot: ["たら"], tags: [VM_IsInflectingWord, VMR_PastTenseStem]),
        new("んだ:past", "did/was", forms: ["だ"], tags: [VMR_PastTenseStem, VM_IsInflectingWord, V_QuestionOverridesForm]),
        // <past-tense-required>
        // <past-tense-forbidden>
        new("んだ:のだ", "thing-is", tags: [VMR_Surface, VM_YieldLastToken, VMF_PastTenseStem]),
        new("たって", tags: [VMF_PastTenseStem]),
        new("だ", surfaceNot: ["なら", "な"], tags: [VM_IsInflectingWord, VMF_PastTenseStem]),
        // </past-tense-forbidden>

        new("たら", "conj{if/when} prt{as-for | why-not..  | I-said!/I-tell-you!}", ["たら"], tags: [VM_IsInflectingWord]),
        new("ちゃう", "to do: accidentally/unfortunately | completely", ["ちゃう"], tags: [VM_IsInflectingWord]),
        new("ても良い", "{concession/compromise} | {permission}", ["てもいい"], tags: [VM_IsInflectingWord]),
        new("すぎる", "too-much", ["すぎる"], tags: [VM_IsInflectingWord]),
        new("いらっしゃいます", "to: come/be/do", ["いらっしゃいます"]),
        new("を頼む", "I-entrust-to-you", ["を頼む"], tags: [VMR_Surface]),
        new("作れる", "to-be-able: to-make", ["つくれる"], compounds: ["作る", "える"]),
        new("たい", "want to", ["たい"], tags: [VM_IsInflectingWord]),
        new("解放する", "to{} release", ["かいほうする"]),

        // require a stems
        new("あれる", "get-_/is-_", ["あれる"], forms: ["れる"], tags: [VMR_Irrealis, VMR_Godan, V_QuestionOverridesForm, VM_IsInflectingWord]),
        new("あせる", "get-_/is-_", ["あせる"], forms: ["せる"], tags: [VMR_Irrealis, VMR_Godan, V_QuestionOverridesForm, VM_IsInflectingWord]),

        new("する", "to: do", yieldToSurface: ["しろ"]),
        new("しろ", "do!", ["しろ"]),
        new("らっしゃる", yieldToSurface: ["らっしゃい"]),
        new("らっしゃい"),

        new("ぬ", "not", ["ぬ"], surfaceNot: ["ず"]),

        new("だの", "and-the-like", ["だの"], prefixNot: ["ん"]),

        new("こ", "familiarizing-suffix", ["こ"], forms: ["っこ"], tags: [VMF_SentenceStart]),

        new("ない", "not", forms: ["ない"], tags: [VM_IsInflectingWord]),
        new("無い", "not", forms: ["ない"], tags: [VM_IsInflectingWord]),
        new("うまい", yieldToSurface: ["うまく"]),
        new("うまく"),
        new("笑える", tos: [POS.IchidanVerb]),

        new("にする", "to: turn-into"),
        new("のか", tags: [VMR_SentenceEnd]),
        new("ないと", tags: [VM_YieldLastToken]),
        new("して", tags: [VM_YieldLastToken]),
        new("ても"),
        new("と思う"),
        new("たの", tags: [VM_IsPoisonWord]),

        new("たかな", tags: [VM_IsPoisonWord]),
        new("たか", tags: [VM_IsPoisonWord]),
        new("なんて", tags: [VM_YieldLastToken]),
        new("何て", tags: [VM_YieldLastToken]),
        new("というか", forms: ["[と言うか]", "っていうか", "ていうか", "て言うか"]),
        new("ていうか", forms: ["と言うか", "というか", "っていうか", "[て言うか]"]),
        new("鰻", forms: ["[うな]"], prefixNot: ["ろ", "よ"]),
        new("書き"),
        new("風の強い", tags: [VMR_Surface]),
        new("たね", tags: [VMR_SingleToken]),
        new("たらしい", tags: [VMR_SingleToken]),
        new("に決まる", forms: ["に決る", "に決まる", "に極る"]),
        new("に決まってる", forms: ["に決っている", "に決まっている", "に極っている", "に決ってる", "に決まってる", "に極ってる"]),
        new("された", surfaceNot: ["されたら"]),

        new("んです", tags: [VMR_Surface, VM_YieldLastToken]),

        new("たん", forms: ["たの"], tags: [VMR_SingleToken]),
        new("たの", forms: ["たん"], tags: [VM_YieldLastToken]),
        new("たんだ", tags: [VM_YieldLastToken]),
        new("んだろう", tags: [VM_IsPoisonWord]),
        new("しちゃう"),
        new("ものを", tags: [VMR_SentenceEnd]),
        new("いいものを", forms: ["よいものを", "良いものを", "かったものを"], tags: [VMR_SentenceEnd]),
        new("に行く", compounds: ["に", "行く"], tags: [VM_YieldLastToken]),
        new("行った", compounds: ["行く", "た"], tags: [VM_YieldLastToken]),

        new("うと", compounds: ["う", "と"], tags: [VM_YieldLastToken, VMF_DictionaryFormStem]),
        new("と思って", compounds: ["と思う", "て"], tags: [VM_YieldLastToken]),
        new("ませ", forms: ["まし"], suffixNot: ["ん"]),
        new("ところが", tags: [VMR_SentenceStart]),

        new("成る", "to: become | result-in | turn-into", ["なる"], prefixNot: ["く"]),
        new("なる", "to: become | result-in | turn-into", ["なる"], prefixNot: ["く"]),
        new("くなる", "to: become", ["くなる"], forms: ["なる"], prefixIn: ["く"], tags: [V_QuestionOverridesForm]),
        new("言える", "to-be: able-to-say", compounds: ["言う", "える"]),
        new("出会える", "to: be-{able/fortunate-enough}-to-{meet/come-across}"),
        new("ていける", "can-go-on"),

        new("ても知らない", forms: ["ても知らん"], compounds: ["ても", "知る", "ん"], tags: [VMR_TeFormStem]),

        new("とおり"),
        new("られる", tags: [VM_IsInflectingWord]),
        new("返せる", tos: [POS.IchidanVerb]),  // exposes a bug in godan imperative detection
        new("外出中", tags: [V_IsCompositionallyTransparentCompound]),
        new("買い替える", tags: [V_IsCompositionallyTransparentCompound]),

        new("きれない", forms: ["[切れない]"], tags: [VMR_MasuStem]),

        new("考えすぎ", tags: [VMF_PrecedingAdverb]),
        new("考えすぎる", tags: [VMF_PrecedingAdverb]),

        new("な", forms: ["な"]),
        new("な:dict", tags: [VMR_DictionaryFormPrefix]),
        new("な:masu", tags: [VMR_MasuStem]),
        new("な:s.end", tags: [VMR_SentenceEnd, VMF_SentenceStart]),
        new("な:s.start", tags: [VMR_SentenceStart]),
        new("すんな", forms: ["[すな]"], tags: [VMF_DictionaryFormStem]),

        new("がある", tags: [VM_YieldLastToken]),
        new("うの", forms: ["うの", "くの", "ぐの", "すの", "つの", "ぬの", "ぶの", "むの", "るの"], tags: [VMR_DictionaryFormStem, V_QuestionOverridesForm]),

        new("寝れる", tags: [VM_IsPoisonWord]),
        new("れる:ichidan", tags: [VMR_Ichidan, VMR_Irrealis]),
        new("れない", tags: [VMR_Ichidan, VMR_Irrealis]),
        new("っ放し", forms: ["っはなし", "っぱなし"], tags: [VM_IsInflectingWord]),

        new("なぜかというと"),
        new("おうと", forms: ["うと"]),

        new("に会う", forms: ["にあう"]),

        new("よい", yieldToSurface: ["よく"]),
        new("よく", suffixNot: ["て"]),

        new("ないし", tags: [VMF_Irrealis, VMF_SentenceEnd, VMF_PrecedingAdverb]),

        new("いただける:able-to", tags: [VMR_TeFormPrefix]),
        new("いただける:acceptable", tags: [VMF_TeFormPrefix]),
        new("てない", tags: [VMR_TeFormStem]),
        new("てしまいます", tags: [VMR_TeFormStem]),

        new("う以上", tags: [VMR_DictionaryFormStem]),
    ];
}
