from typing import Any

class KanjiSpec:
    def __init__(self, question: str, answer: str, kun_readings: str, on_readings: str):
        self.question = question
        self.answer = answer
        self.kun_reading = kun_readings
        self.on_readings = on_readings

    def __repr__(self) -> str: return f"""KanjiSpec("{self.question}", "{self.answer}", "{self.kun_reading}", "{self.on_readings}")"""

    def __eq__(self, other:Any) -> bool:
        return (isinstance(other, KanjiSpec)
                and other.question == self.question
                and other.answer == self.answer
                and other.kun_reading == self.kun_reading
                and other.on_readings == self.on_readings)

    def __hash__(self) -> int:
        return hash(self.question)

#Generated by test_create_sample_data()
test_kanji_list = [
    KanjiSpec("一", "one", "ひと", "いち, いつ"),
    KanjiSpec("人", "person", "ひと, と", "にん, じん"),
    KanjiSpec("女", "female", "おんな, め", "じょ, にょ, にょう"),
    KanjiSpec("本", "main/true | book", "もと", "ほん"),
    KanjiSpec("夕", "evening", "ゆう", "せき"),
    KanjiSpec("出", "exit|take-out", "で, だ", "しゅつ"),
    KanjiSpec("中", "inside/center", "なか", "ちゅう"),
    KanjiSpec("々", "repeater", "のま", ""),
    KanjiSpec("日", "day | sun", "ひ, か, び", "にち, じつ"),
    KanjiSpec("水", "water", "みず", "すい"),
    KanjiSpec("友", "friend", "とも", "ゆう"),
    KanjiSpec("内", "inside/within", "うち", "ない"),
    KanjiSpec("生", "life", "い, なま, う, は, き", "せい, しょう"),
    KanjiSpec("今", "now", "いま", "こん"),
    KanjiSpec("分", "part/portion|understand/know", "わ", "ぶん, ふん, ぶ"),
    KanjiSpec("気", "spirit/mind | atmosphere/mood", "", "き, け"),
    KanjiSpec("先", "previous/last | tip/edge/ahead", "さき, ま", "せん"),
    KanjiSpec("見", "See", "み", "けん"),
    KanjiSpec("角", "corner", "かど, つの", "かく"),
    KanjiSpec("体", "body|object|substance", "からだ", "たい"),
    KanjiSpec("色", "color", "いろ", "しき, しょく"),
    KanjiSpec("来", "come(ing)", "く, き", "らい"),
    KanjiSpec("当", "hit | correct/appropriate", "あ", "とう"),
    KanjiSpec("行", "going|carry-out", "い, おこな, ゆ", "こう, ぎょう"),
    KanjiSpec("米", "rice/america", "こめ", "べい, まい"),
    KanjiSpec("言", "say | word", "い, こと", "げん, ごん"),
    KanjiSpec("自", "self(-)", "みずか", "じ, し"),
    KanjiSpec("別", "separate/fork", "わか", "べつ"),
    KanjiSpec("特", "Special", "", "とく"),
    KanjiSpec("合", "suit/fit | join", "あ, あい", "ごう, がっ"),
    KanjiSpec("様", "Formal Name Title, Formal Name Ender, Manner", "さま", "よう"),
    KanjiSpec("然", "sort-of-thing/nature", "しか, さ", "ぜん, ねん"),
    KanjiSpec("問", "question | problem", "と, とん", "もん"),
    KanjiSpec("題", "Topic", "", "だい"),
    KanjiSpec("折", "Fold, Bend, Break", "お, おり", "せつ"),
    KanjiSpec("性", "gender | nature | sex", "", "せい, しょう"),
    KanjiSpec("松", "Pine, Pine Tree", "まつ", "しょう"),
    KanjiSpec("秋", "Autumn, Fall", "あき", "しゅう"),
    KanjiSpec("晴", "clear-up", "は", "せい"),
    KanjiSpec("泣", "cry", "な", "きゅう"),
    KanjiSpec("丈", "height | sturdy/stout", "たけ, だけ", "じょう"),
    KanjiSpec("昼", "noon", "ひる", "ちゅう"),
    KanjiSpec("昨", "previous/yesterday", "", "さく"),
    KanjiSpec("存", "Exist, Suppose", "", "そん, ぞん"),
    KanjiSpec("守", "protect", "まも, もり", "す, しゅ"),
    KanjiSpec("取", "take", "と", "しゅ"),
    KanjiSpec("書", "write|writing", "か", "しょ"),
    KanjiSpec("是", "Absolutely", "", "ぜ"),
    KanjiSpec("識", "Discerning, Discriminating, Know", "", "しき"),
    KanjiSpec("敗", "failure/defeat", "やぶ", "はい"),
    KanjiSpec("無", "un-/non- | nothing", "な", "む, ぶ"),
    KanjiSpec("達", "reach|attain|{k:pluralizing-suffix}", "たち", "たつ"),
    KanjiSpec("報", "information/report | {k:reward|retaliate}", "むく", "ほう"),
    KanjiSpec("善", "Morally Good, Good", "", "ぜん"),
    KanjiSpec("夢", "dream", "ゆめ", "む"),
    KanjiSpec("在", "Exist", "", "ざい"),
    KanjiSpec("素", "Element", "もと", "そ, す"),
    KanjiSpec("寝", "lie-down/sleep", "ね", "しん"),
    KanjiSpec("応", "respond | accept", "こた", "おう"),
    KanjiSpec("観", "View", "み", "かん"),
    KanjiSpec("護", "Defend", "", "ご"),
    KanjiSpec("視", "Look At", "み", "し"),
    KanjiSpec("居", "reside/exist(animate)", "い", "きょ"),
    KanjiSpec("掛", "put-on/apply/consume", "か", "かい, けい"),
    KanjiSpec("捜", "search", "さが", "そう"),
    KanjiSpec("往", "Journey, Depart", "", "おう"),
    KanjiSpec("処", "Deal With", "ところ", "しょ"),
    KanjiSpec("恐", "fear", "おそ, こわ", "きょう"),
    KanjiSpec("怖", "scary", "こわ", "ふ"),
    KanjiSpec("遊", "play", "あそ", "ゆう"),
    KanjiSpec("幾", "How Many, How Much", "いく", "き"),
    KanjiSpec("探", "search-for", "さが, さぐ", "たん"),
    KanjiSpec("祖", "Ancestor", "", "そ"),
    KanjiSpec("欲", "want", "ほ", "よく"),
    KanjiSpec("傷", "wound/injure", "きず, いた", "しょう"),
    KanjiSpec("刻", "Carve", "きざ", "こく"),
    KanjiSpec("奴", "{や:guy} | {ど:slave}", "やつ", "ど"),
    KanjiSpec("考", "Think, Consider", "かんが", "こう"),
    KanjiSpec("何", "what", "なに, なん", "か"),
    KanjiSpec("食", "eat | food", "た, く", "しょく"),
    KanjiSpec("前", "in-front-of(space)|before(time)", "まえ", "ぜん"),
    KanjiSpec("有", "possess | exists | happen/occur", "あ", "ゆう, う"),
    KanjiSpec("私", "private | I", "わたし", "し"),
    KanjiSpec("知", "Know", "し", "ち"),
    KanjiSpec("夜", "Night, Evening", "よ, よる", "や"),
    KanjiSpec("海", "sea", "うみ", "かい"),
    KanjiSpec("羊", "sheep", "ひつじ", "よう"),
    KanjiSpec("付", "attach", "つ", "ふ"),
    KanjiSpec("失", "loss | error/fault", "うしな", "しつ"),
    KanjiSpec("時", "time/hour", "とき", "じ"),
    KanjiSpec("記", "write | account", "しる", "き"),
    KanjiSpec("答", "answer/response | solution", "こた", "とう"),
    KanjiSpec("楽", "comfort/ease", "たの", "らく, がく"),
    KanjiSpec("所", "place", "ところ", "しょ"),
    KanjiSpec("身", "some(body)", "み", "しん"),
    KanjiSpec("話", "tale/talk", "はな, はなし", "わ"),
    KanjiSpec("事", "incorporeal-thing(matter|event|action|situation)", "こと, つか", "じ"),
    KanjiSpec("度", "degree | time(s)", "たび", "ど, たく"),
    KanjiSpec("要", "Need", "い, かなめ", "よう"),
    KanjiSpec("終", "end/finish", "おわ, お", "しゅう"),
    KanjiSpec("落", "Fall", "お", "らく"),
    KanjiSpec("頭", "Head", "あたま, かしら", "ず, とう"),
    KanjiSpec("親", "parent|intimacy", "おや, した", "しん"),
    KanjiSpec("成", "(grow-to)become", "な", "せい"),
    KanjiSpec("命", "fate | life", "いのち", "めい, みょう"),
    KanjiSpec("良", "good/pleasing", "よ, い", "りょう"),
    KanjiSpec("好", "like", "す, この", "こう"),
    KanjiSpec("吉", "Good Luck", "よし", "きつ, きち"),
    KanjiSpec("俺", "I, Me", "おれ", ""),
    KanjiSpec("如", "Likeness", "ごと", "じょ"),
    KanjiSpec("遂", "accomplish", "と, つい", "すい"),
    KanjiSpec("勘", "Intuition", "", "かん"),
    KanjiSpec("佳", "Excellent, Skilled", "", "か"),
    KanjiSpec("癒", "Healing, Cure", "い, いや", "ゆ"),
    KanjiSpec("梓", "Japanese Birch, Birch", "あずさ", "し"),
    KanjiSpec("逝", "Die", "い, ゆ", "せい"),
    KanjiSpec("彼", "he | they/that/the", "かれ, かの", "ひ"),
    KanjiSpec("己", "Oneself, Self", "おのれ", "こ, き"),
    KanjiSpec("為", "do|benefit", "ため, な, す", "い"),
    KanjiSpec("戻", "Return", "もど", "れい"),
    KanjiSpec("宜", "best-regards|good", "よろ", "ぎ"),
    KanjiSpec("逃", "Escape", "に, のが, の", "とう"),
    KanjiSpec("懸", "Suspend", "か", "けん"),
    KanjiSpec("緒", "Together", "お", "しょ, ちょ"),
    KanjiSpec("免", "Excuse", "まぬか", "めん"),
    KanjiSpec("御", "honorable", "お, おん, み", "ご, ぎょ"),
    KanjiSpec("貰", "get/obtain", "もら.う", "セイ, シャ")
]