using System;
using System.Collections.Generic;

namespace JAStudio.Core.Tests.Fixtures.BaseData.SampleData;

public class KanjiSpec : IEquatable<KanjiSpec>
{
    public KanjiSpec(string question, string answer, string kunReadings, string onReadings)
    {
        Question = question;
        Answer = answer;
        KunReading = kunReadings;
        OnReadings = onReadings;
    }

    public string Question { get; }
    public string Answer { get; }
    public string KunReading { get; }
    public string OnReadings { get; }

    public override string ToString() => $"""KanjiSpec("{Question}", "{Answer}", "{KunReading}", "{OnReadings}")""";

    public override bool Equals(object? obj) => Equals(obj as KanjiSpec);

    public bool Equals(KanjiSpec? other) =>
        other is not null
        && other.Question == Question
        && other.Answer == Answer
        && other.KunReading == KunReading
        && other.OnReadings == OnReadings;

    public override int GetHashCode() => Question.GetHashCode();

    public static readonly List<KanjiSpec> TestKanjiList =
    [
        new("病", "illness", "<primary>ビョウ</primary>", "<primary>や</primary>, <primary>やまい</primary>"),
        new("品", "goods | elegance", "<primary>しな</primary>", "<primary>ひん</primary>"),
        new("塚", "a-{mound/aoeu}", "<primary>つか</primary>", "ちょう"),
        new("疒", "sick", "", ""),
        new("丙", "dynamite", "", ""),
        new("一", "one/(ground)", "ひと", "いち, いつ"),
        new("冂", "(head)", "", ""),
        new("人", "person", "ひと, と", "にん, じん"),
        new("女", "female", "おんな, め", "じょ, にょ, にょう"),
        new("本", "true/main | book", "もと", "ほん"),
        new("夕", "evening", "ゆう", "せき"),
        new("出", "exit|take-out", "で, だ", "しゅつ"),
        new("中", "inside/center", "なか", "ちゅう"),
        new("日", "day | sun", "ひ, か, び", "にち, じつ"),
        new("水", "water", "みず", "すい"),
        new("友", "friend", "とも", "ゆう"),
        new("内", "inside/within", "<primary>うち</primary>", "ない"),
        new("生", "life", "い, なま, う, は, き", "せい, しょう"),
        new("今", "now", "いま", "こん"),
        new("分", "part/portion|understand/know", "わ", "ぶん, ふん, ぶ"),
        new("気", "spirit/mind | atmosphere/mood", "", "き, け"),
        new("先", "previous/last | tip/edge/ahead", "さき, ま", "せん"),
        new("見", "See", "み", "けん"),
        new("町", "town/block/street", "まち", "ちょう"),
        new("角", "corner", "かど, つの", "かく"),
        new("体", "body|object|substance", "からだ", "たい"),
        new("色", "color", "いろ", "しき, しょく"),
        new("来", "come(ing)", "く, き", "らい"),
        new("当", "hit | correct/appropriate", "あ", "とう"),
        new("行", "going|carry-out", "い, おこな, ゆ", "こう, ぎょう"),
        new("会", "Meet, Meeting", "あ", "かい"),
        new("米", "rice/america", "こめ", "べい, まい"),
        new("言", "say | word", "い, こと", "げん, ごん"),
        new("自", "self(-)", "みずか", "じ, し"),
        new("別", "separate/fork", "わか", "べつ"),
        new("特", "Special", "", "とく"),
        new("合", "suit/fit | join", "あ, あい", "ごう, がっ"),
        new("様", "Formal Name Title, Formal Name Ender, Manner", "さま", "よう"),
        new("然", "sort-of-thing/nature", "しか, さ", "ぜん, ねん"),
        new("問", "question | problem", "と, とん", "もん"),
        new("題", "Topic", "", "だい"),
        new("折", "Fold, Bend, Break", "お, おり", "せつ"),
        new("性", "gender | nature | sex", "", "せい, しょう"),
        new("松", "Pine, Pine Tree", "まつ", "しょう"),
        new("秋", "Autumn, Fall", "あき", "しゅう"),
        new("晴", "clear-up", "は", "せい"),
        new("泣", "cry", "な", "きゅう"),
        new("丈", "height | sturdy/stout", "たけ, だけ", "じょう"),
        new("計", "plan/calculate | measure", "はか", "けい"),
        new("昼", "noon", "ひる", "ちゅう"),
        new("昨", "previous/yesterday", "", "さく"),
        new("存", "Exist, Suppose", "", "そん, ぞん"),
        new("守", "protect", "まも, もり", "す, しゅ"),
        new("取", "take", "と", "しゅ"),
        new("書", "write|writing", "か", "しょ"),
        new("是", "Absolutely", "", "ぜ"),
        new("識", "Discerning, Discriminating, Know", "", "しき"),
        new("敗", "failure/defeat", "やぶ", "はい"),
        new("無", "un-/non- | nothing", "な", "む, ぶ"),
        new("達", "reach|attain|{k:pluralizing-suffix}", "たち", "たつ"),
        new("報", "information/report | {k:reward|retaliate}", "むく", "ほう"),
        new("善", "Morally Good, Good", "", "ぜん"),
        new("夢", "dream", "ゆめ", "む"),
        new("在", "Exist", "", "ざい"),
        new("余", "surplus/excess", "あま", "よ"),
        new("素", "Element", "もと", "そ, す"),
        new("寝", "lie-down/sleep", "ね", "しん"),
        new("応", "respond | accept", "こた", "おう"),
        new("宮", "(shinto)shrine | palace", "みや", "きゅう"),
        new("観", "View", "み", "かん"),
        new("藤", "Wisteria", "ふじ", "とう, どう"),
        new("護", "Defend", "", "ご"),
        new("視", "Look At", "み", "し"),
        new("居", "reside/exist(animate)", "い", "きょ"),
        new("掛", "put-on/apply/consume", "か", "かい, けい"),
        new("捜", "search", "さが", "そう"),
        new("往", "Journey, Depart", "", "おう"),
        new("誘", "Invite", "さそ", "ゆう"),
        new("処", "Deal With", "ところ", "しょ"),
        new("恐", "fear", "おそ, こわ", "きょう"),
        new("怖", "scary", "こわ", "ふ"),
        new("遊", "play", "あそ", "ゆう"),
        new("離", "separation", "はな", "り"),
        new("幾", "How Many, How Much", "いく", "き"),
        new("探", "search-for", "さが, さぐ", "たん"),
        new("祖", "Ancestor", "", "そ"),
        new("捨", "throw-away", "す", "しゃ"),
        new("欲", "want", "ほ", "よく"),
        new("傷", "wound/injure", "きず, いた", "しょう"),
        new("刻", "Carve", "きざ", "こく"),
        new("奴", "{や:guy} | {ど:slave}", "やつ", "ど"),
        new("考", "Think, Consider", "かんが", "こう"),
        new("何", "what", "なに, なん", "か"),
        new("全", "all/entire", "すべ, まった", "ぜん"),
        new("明", "bright", "あ, あか, あき", "めい, みょう"),
        new("食", "eat | food", "た, く", "しょく"),
        new("前", "in-front-of(space)|before(time)", "まえ", "ぜん"),
        new("有", "possess | exists | happen/occur", "あ", "ゆう, う"),
        new("私", "private | I", "わたし", "し"),
        new("知", "Know", "し", "ち"),
        new("夜", "Night, Evening", "よ, よる", "や"),
        new("海", "sea", "うみ", "かい"),
        new("羊", "sheep", "ひつじ", "よう"),
        new("付", "attach", "つ", "ふ"),
        new("失", "loss | error/fault", "うしな", "しつ"),
        new("時", "time/hour", "とき", "じ"),
        new("記", "write | account", "しる", "き"),
        new("答", "answer/response | solution", "こた", "とう"),
        new("楽", "comfort/ease", "たの", "らく, がく"),
        new("助", "help/assist", "たす, すけ", "じょ"),
        new("所", "place", "ところ", "しょ"),
        new("身", "some(body)", "み", "しん"),
        new("話", "tale/talk", "はな, はなし", "わ"),
        new("事", "incorporeal-thing(matter|event|action|situation)", "こと, つか", "じ"),
        new("度", "degree | time(s)", "たび", "ど, たく"),
        new("要", "Need", "い, かなめ", "よう"),
        new("部", "department | club", "へ", "ぶ"),
        new("終", "end/finish", "おわ, お", "しゅう"),
        new("落", "Fall", "お", "らく"),
        new("頭", "Head", "あたま, かしら", "ず, とう"),
        new("聞", "hear | ask | listen", "き", "ぶん, もん"),
        new("調", "Investigate, Tone", "しら", "ちょう"),
        new("親", "parent|intimacy", "おや, した", "しん"),
        new("成", "(grow-to)become", "な", "せい"),
        new("命", "fate | life", "いのち", "めい, みょう"),
        new("良", "good/pleasing", "よ, い", "りょう"),
        new("好", "like", "す, この", "こう"),
        new("吉", "Good Luck", "よし", "きつ, きち"),
        new("俺", "I, Me", "おれ", ""),
        new("如", "Likeness", "ごと", "じょ"),
        new("遂", "accomplish", "と, つい", "すい"),
        new("勘", "Intuition", "", "かん"),
        new("佳", "Excellent, Skilled", "", "か"),
        new("癒", "Healing, Cure", "い, いや", "ゆ"),
        new("梓", "Japanese Birch, Birch", "あずさ", "し"),
        new("逝", "Die", "い, ゆ", "せい"),
        new("彼", "he | they/that/the", "かれ, かの", "ひ"),
        new("己", "Oneself, Self", "おのれ", "こ, き"),
        new("為", "do|benefit", "ため, な, す", "い"),
        new("戻", "Return", "もど", "れい"),
        new("宜", "best-regards|good", "よろ", "ぎ"),
        new("逃", "Escape", "に, のが, の", "とう"),
        new("懸", "Suspend", "か", "けん"),
        new("緒", "Together", "お", "しょ, ちょ"),
        new("免", "Excuse", "まぬか", "めん"),
        new("御", "honorable", "お, おん, み", "ご, ぎょ"),
        new("貰", "get/obtain", "もら.う", "せい, しゃ"),
        new("逢", "meetingtrystdate", "あ.う, むか.える", "ほう")
    ];
}
