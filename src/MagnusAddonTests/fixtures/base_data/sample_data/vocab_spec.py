from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from note.note_constants import Mine

if TYPE_CHECKING:
    from note.vocabulary.vocabnote import VocabNote

class VocabSpec:
    # noinspection PyDefaultArgument
    def __init__(self, question: str,
                 answer: str,
                 readings: list[str],
                 extra_forms: Optional[list[str]] = None,
                 tags: Optional[list[str]] = None,
                 compounds: Optional[list[str]] = None) -> None:
        self.question = question
        self.answer = answer
        self.readings = readings
        self.extra_forms = set(extra_forms if extra_forms else [])
        self.tags = set(tags if tags else [])
        self.compounds = compounds if compounds else []

    def __repr__(self) -> str: return f"""VocabSpec("{self.question}", "{self.answer}", {self.readings})"""

    def __hash__(self) -> int: return hash(self.question)

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, VocabSpec)
                and other.question == self.question
                and other.answer == self.answer
                and other.readings == self.readings)

    def create_vocab_note(self) -> VocabNote:
        from note.vocabulary.vocabnote import VocabNote
        vocab_note = VocabNote.factory.create(self.question, self.answer, self.readings)
        vocab_note.set_user_compounds(self.compounds)

        if self.extra_forms:
            vocab_note.forms.set_set(vocab_note.forms.unexcluded_set() | self.extra_forms)

        for tag in self.tags:
            vocab_note.set_tag(tag)

        return vocab_note

test_special_vocab = [
    VocabSpec("てる", "{continuing-{activity | state}} / {progressive | perfect}", ['てる'], tags=[Mine.Tags.inflecting_word]),
    VocabSpec("た", "{past-tense} | (please)do", ['た'], tags=[Mine.Tags.inflecting_word]),
    VocabSpec("て", "{continuing-action}", ['て'], tags=[Mine.Tags.inflecting_word]),
    VocabSpec("てた", "{was}-{_-ing|_ed}", ['てた'], tags=[Mine.Tags.inflecting_word]),
    VocabSpec("てたら", "{was}-{_-ing|_ed}", ['てたら'], tags=[Mine.Tags.inflecting_word]),
    VocabSpec("たら", "conj{if/when} prt{as-for | why-not..  | I-said!/I-tell-you!}", ['たら'], extra_forms=["[[た]]"], tags=[Mine.Tags.inflecting_word]),
    VocabSpec("ちゃう", "to do: accidentally/unfortunately | completely", ['ちゃう'], tags=[Mine.Tags.inflecting_word]),
    VocabSpec("無い", "{negation} | nonexistent | unowned | impossible/won't-happen", ['ない'], tags=[Mine.Tags.inflecting_word]),
    VocabSpec("ても良い", "{concession/compromise} | {permission}", ['てもいい'], tags=[Mine.Tags.inflecting_word]),
    VocabSpec("たの", "{indicates-{emotion/admiration/emphasis}}", ['たの'], extra_forms=["[[たの]]"]),
    VocabSpec("すぎる", "too-much", ['すぎる'], tags=[Mine.Tags.inflecting_word]),
    VocabSpec("だったら", "if-so", ['だったら'], extra_forms=["[[だった]]"]),
    VocabSpec("に", "{location/direction/target/reason/purpose} {adv}", ['に'], extra_forms=["[[だ]]"]),
    VocabSpec("で", "{act-ctx{time|place|cause|means}}　| {て-form:+<ja>む/ぬ</ja>-verbs+<ja>だ</ja>} | ksb:よ", ['で'], extra_forms=["[[だ]]"]),
    VocabSpec("な", "{attributive-copula} | な-particle ...", ['な'], extra_forms=["[[だ]]"]),
    VocabSpec("だの", "and-the-like", ['だの'], extra_forms=["[[んだの]]"]),
    VocabSpec("いらっしゃいませ", "welcome!", ['いらっしゃいませ'], extra_forms=["[[いらっしゃいます]]"]),
    VocabSpec("いらっしゃいます", "to: come/be/do", ['いらっしゃいます']),
    VocabSpec("を頼む", "I-entrust-to-you", ["を頼む"], tags=[Mine.Tags.requires_exact_match]),
    VocabSpec("あれる", "get-_/is-_", ["あれる"], extra_forms=["れる"], tags=[Mine.Tags.requires_a_stem, Mine.Tags.question_overrides_form, Mine.Tags.inflecting_word]),
    VocabSpec("えれる", "is-able-to-_", ["えれる"], extra_forms=["れる"], tags=[Mine.Tags.requires_e_stem, Mine.Tags.question_overrides_form, Mine.Tags.inflecting_word]),
    VocabSpec("会える", "to-be-able: to-meet", ["あえる"], compounds=["会う", "える"]),
    VocabSpec("作れる", "to-be-able: to-make", ["つくれる"], compounds=["作る", "える"]),
    VocabSpec("える", "to-be-able-to", ["える"], extra_forms=["[[れる]]"], tags=[Mine.Tags.inflecting_word]),
    VocabSpec("えない", "unable-able-to", ["えない"], compounds=["える", "ない"], tags=[Mine.Tags.inflecting_word]),
    VocabSpec("だもの", "is-the-thing", ["だもの"], extra_forms=["[[んだもの]]"])
]

test_ordinary_vocab_list = [
    VocabSpec("為", "sake/purpose/objective | good/advantage", ['ため']),
    VocabSpec("俺", "I/me", ['おれ']),
    VocabSpec("ように言う", "to: tell-(someone)-to", ['ようにいう']),
    VocabSpec("様に", "in-order-to | {hoping/wishing}-that", ['ように']),
    VocabSpec("なら", "if-so/that-being-the-case | if/in-case | as-for/on-the-topic-of", ['なら']),
    VocabSpec("折角", "With Trouble, Valuable, Rare", ['せっかく']),
    VocabSpec("取る", "to{}: take(lit.fig.)", ['とる']),
    VocabSpec("いい", "good/pleasant | enough | beneficial | OK/no-problem", ['いい']),
    VocabSpec("食べる", "to{}: eat", ['たべる']),
    VocabSpec("一緒に", "together/at-the-same-time", ['いっしょに']),
    VocabSpec("話しかける", "to: address/accost/talk-to | begin-to-talk/start-a-conversation", ['はなしかける']),
    VocabSpec("楽", "comfort/ease/relief | easy/without-hardship", ['らく']),
    VocabSpec("本当", "truth/reality | proper/right |  genuine/authentic", ['ほんとう']),
    VocabSpec("を", "{marks: direct-object | subject(caus:expr)}", ['を']),
    VocabSpec("夢を見る", "to: dream", ['ゆめをみる']),
    VocabSpec("考える", "to{}: think-over | bear-in-mind | hold-a-view", ['かんがえる']),
    VocabSpec("失敗", "Failure, Mistake", ['しっぱい']),
    VocabSpec("良かったら", "if-you-like", ['よかったら']),
    VocabSpec("られる", "aux: {passive} |{potential} | {spontaneous-occurence} | {honorific}", ['られる']),
    VocabSpec("夢", "dream", ['ゆめ']),
    VocabSpec("答え", "answer/response | solution", ['こたえ']),
    VocabSpec("話す", "to{}: talk/speak | tell/explain", ['はなす']),
    VocabSpec("特別", "Special", ['とくべつ']),
    VocabSpec("女性", "Female, Woman, Lady", ['じょせい']),
    VocabSpec("御免", "sorry/i-beg-your-pardon", ['ごめん']),
    VocabSpec("ご免", "I'm sorry/my-apologies | excuse-me | may I come in", ['ごめん']),
    VocabSpec("し", "is-one-reason", ['し']),
    VocabSpec("米", "rice", ['こめ']),
    VocabSpec("当てる", "to{}: hit | expose | apply/put-on | call-on(in-class)", ['あてる']),
    VocabSpec("守る", "to{}: protect/guard{} | keep{promise} | abideby{rules}", ['まもる']),
    VocabSpec("それなのに", "and-yet/but-even-so/despite-this", ['それなのに']),
    VocabSpec("そう", "aux{seems/looks}like | adv{in-that-way} | int{right!|really?}", ['そう']),
    VocabSpec("頭", "Head", ['あたま']),
    VocabSpec("ちゃんと", "diligently/seriously | perfectly/properly | sufficiently/satisfactorily", ['ちゃんと']),
    VocabSpec("泣く", "To Cry", ['なく']),
    VocabSpec("や", "{non-exhaustive-list-item} | {the-minute-thate} | ksb:だ", ['や']),
    VocabSpec("よね", "isn't-that-right? | right!?", ['よね']),
    VocabSpec("に", "{location/direction/target/reason/purpose} {adv}", ['に']),
    VocabSpec("じゃん", "isn't-it?/don't-you-think?/surely? | ta-da!/voilà!", ['じゃん']),
    VocabSpec("何だ", "well-now/how-about-that | what-the-heck/damn", ['なんだ']),
    VocabSpec("まあ", "t!{well.. | tolerably/passably} int{now-now | oh my!}", ['まあ']),
    VocabSpec("欲しい", "Wanted, Desired, Want", ['ほしい']),
    VocabSpec("気になる", "to: {worry/be-anxious}-about | be{interested/curious}-about", ['きになる']),
    VocabSpec("私", "I/me", ['わたし', 'わたくし']),
    VocabSpec("気", "spirit/mind | disposition | intent | mood | care...", ['き']),
    VocabSpec("あいつ", "he/she/that-guy[derog/fam] | that/that-one/that-thing", ['あいつ']),
    VocabSpec("日記", "diary/journal", ['にっき']),
    VocabSpec("出る", "to: go-out/exit/leave ....", ['でる']),
    VocabSpec("たり", "doing-such-things-as ...", ['たり']),
    VocabSpec("なあ", "int{hey/listen} | s.end{I-tell-you!/you-know | right?/isn't-it?}", ['なあ']),
    VocabSpec("としたら", "if-it-happens-that / if-we-assume", ['としたら']),
    VocabSpec("だろう", "seems/I-think/I-guess | right?/don't-you-agree?", ['だろう']),
    VocabSpec("だろ", "seems/I-think/I-guess | right?/don't-you-agree?", ['だろ']),
    VocabSpec("する", "{verbalizes-noun} #to: do | make-into | serve-as | wear", ['する']),
    VocabSpec("友達", "friend/companion", ['ともだち']),
    VocabSpec("様", "appearing/looking | way to | form/style", ['よう']),
    VocabSpec("考え", "Thought, A Thought", ['かんがえ']),
    VocabSpec("恐ろしい", "Scary, Fearful", ['おそろしい']),
    VocabSpec("だ", "cop{be/is} aux{past-tense | please/do}", ['だ']),
    VocabSpec("傷つける", "to{}: wound/injure", ['きずつける']),
    VocabSpec("ね", "end{right?|see?|please?} int{hey/say} ", ['ね']),
    VocabSpec("ねぇ", "nonexistent/not-being | not | <ja>ね:</ja> right/isn't-it ...", ['ねぇ']),
    VocabSpec("遊び", "Play, Playing, Games", ['あそび']),
    VocabSpec("ても", "even-if/even-though | wow ", ['ても']),
    VocabSpec("って", "{quotes(speech|thoughts|implications)} | {topic-marker}", ['って']),
    VocabSpec("か", "{question} | {alternative} | {adverb | adjective} ...", ['か']),
    VocabSpec("じゃない", "[ではない] {is/am/are}not | isn't-it?/right?", ['じゃない']),
    VocabSpec("は", "{topic} | {contrast} | {emphasis}", ['は']),
    VocabSpec("でも", "conj{but/however} prt{even(if) | or-something | {either/neither}-or}", ['でも']),
    VocabSpec("あの", "pn{that/those/the} | int{say/well/um/er}", ['あの']),
    VocabSpec("存在", " existence/being/presence", ['そんざい']),
    VocabSpec("体", "body", ['からだ']),
    VocabSpec("身体", "The Body, Health, Body", ['しんたい', 'からだ']),
    VocabSpec("付き合う", "to{go-out|associate}-with | go-along-with | accompany", ['つきあう']),
    VocabSpec("ここ", "here / this place SOURCE", ['ここ']),
    VocabSpec("どう", "how/in-what-way/how-about", ['どう']),
    VocabSpec("事", "{nominalizer} | incorporeal-thing(subject|event|action|situation)", ['こと']),
    VocabSpec("親", "Parent", ['おや']),
    VocabSpec("素晴らしい", "wonderful/splendid/magnificent", ['すばらしい']),
    VocabSpec("お昼", "lunch | noon | daytime | {waking/getting}-up", ['おひる']),
    VocabSpec("んだ", "<ja>のだ</ja> the-{thing/expectation/reason/fact}-is | that's-right/uh-huh", ['んだ']),
    VocabSpec("ううん", "nuh-uh/no | um/er/well | oof!", ['ううん']),
    VocabSpec("出てくる", "to: come-out/appear/turn-up/emerge", ['でてくる']),
    VocabSpec("から", "from/since | because", ['から']),
    VocabSpec("として", "as(role) | apart-from | !even | vol&gt;{thinking-that/trying-to}...", ['として']),
    VocabSpec("成る", "to: become | result-in | turn-into", ['なる']),
    VocabSpec("が", "{subject} | passive:{object} | but/however/still", ['が']),
    VocabSpec("寝る", "to: lie(sleeping|down|flat|idle|fermenting) | have-sex", ['ねる']),
    VocabSpec("けど", "but/however/although", ['けど']),
    VocabSpec("かも", "may/might/perhaps", ['かも']),
    VocabSpec("お前", "you (oft:derog/angr/disdain)", ['おまえ']),
    VocabSpec("答える", "to: answer-question | provide-solution", ['こたえる']),
    VocabSpec("のです", "the-{thing/expectation/reason/fact/explanation}-is", ['のです']),
    VocabSpec("人", "person | people | human-species", ['ひと']),
    VocabSpec("色々", "various", ['いろいろ']),
    VocabSpec("来る", "to: come{space|time} aux{come{to-be/become}}", ['くる']),
    VocabSpec("貰う", "to: recieve-upon-request{item/favor}", ['もらう']),
    VocabSpec("書く", "to{}: write", ['かく']),
    VocabSpec("要る", "to: (be)need/want(ed)", ['いる']),
    VocabSpec("居る", "to: be(animate) | て{continuing-{action/state}}", ['いる']),
    VocabSpec("いる", "to: 居る:be(animate) | stay | {progressive | perfect} | 要る:need/want", ['いる']),
    VocabSpec("幾ら", "How Much", ['いくら']),
    VocabSpec("逃げる", "To Escape, To Flee, To Run Away", ['にげる']),
    VocabSpec("有る", "to: be/exist | have/own", ['ある']),
    VocabSpec("とする", "to: おう{try/be-about}to　る{decide}-to ...", ['とする']),
    VocabSpec("話", "conversation | topic | tale/story&nbsp;", ['はなし']),
    VocabSpec("ですか", "indicates-question", ['ですか']),
    VocabSpec("まで", "{until/to/as-far-as}{time|place|extent/degree} ", ['まで']),
    VocabSpec("だって", "conj{after-all/because | but} prt{even | too/as-well | I-hear/you-mean}", ['だって']),
    VocabSpec("ん", "<ja>の</ja>{nom |poss | explan } ...", ['ん']),
    VocabSpec("一緒", "together | at-the-same-time | same/identical", ['いっしょ']),
    VocabSpec("一度", "once/on-one-occation", ['いちど']),
    VocabSpec("たい", "want to", ['たい']),
    VocabSpec("と", "conj{if/when | exhaus-list-item} prt{with | quote | adverb}", ['と']),
    VocabSpec("たの", "{indicates-{emotion/admiration/emphasis}}", ['たの']),
    VocabSpec("今", "now", ['いま']),
    VocabSpec("言う", "to: say | name/call", ['いう']),
    VocabSpec("そんなに", "so-much/so/like-that", ['そんなに']),
    VocabSpec("〜時", "hour/o'clock", ['じ']),
    VocabSpec("時", "<ja>とき</ja>:time/hour | moment/occasion | chance/opportunity <ja>じ</ja>:o'clock", ['とき']),
    VocabSpec("一生懸命", "very-hard/with-utmost-effort/for-dear-life/desperately", ['いっしょうけんめい']),
    VocabSpec("それ", "that(near-listener) | then/that-time | int{there!/look! | go-on!/here-goes!}", ['それ']),
    VocabSpec("夕べ", "(last){night/evening}", ['ゆうべ']),
    VocabSpec("昨夜", "last night, last evening SOURCE", ['ゆうべ']),
    VocabSpec("遂に", "finally/at-last | !{in-the-end/after-all/never(happened)}", ['ついに']),
    VocabSpec("じゃ", "[では] then/well(then) ...", ['じゃ']),
    VocabSpec("良い", "good/excellent | sufficient | beneficial | OK/no-problem", ['よい', 'いい']),
    VocabSpec("やばい", "dangerous/risky | awful/terrible | terrific/amazing | crazy/insane", ['やばい']),
    VocabSpec("も", "prt: too/also | even/as-far-as | even-{if/though} | further/more", ['も']),
    VocabSpec("気付く", "to: realize/notice", ['きづく']),
    VocabSpec("気づく", "to: notice/realize | come-to-one's-senses", ['きづく']),
    VocabSpec("自分", "{subject's}self, {topics's}self", ['じぶん']),
    VocabSpec("中", "inside | among | center/middle", ['なか']),
    VocabSpec("内", "inside/within | one's-{home/family}", ['うち']),
    VocabSpec("問題", "test-question | problem/issue | doubt/question", ['もんだい']),
    VocabSpec("の", "{possesive/attributive} | {nominalizing} | {explanatory} | {subject(sub.phr)}", ['の']),
    VocabSpec("それが", "{subject}that/it | {well,actually/unfortunately}[hesitant-reply]", ['それが']),
    VocabSpec("どこ", "where | how(much/long/far)/to-what-extent", ['どこ']),
    VocabSpec("落とす", "to{}: drop | lower/reduce | loose  | clean-off", ['おとす']),
    VocabSpec("行く", "to: go(wide.lit.fig)", ['いく']),
    VocabSpec("其れ丈", "that-much/to-that-extent | only-that/that-alone", ['それだけ']),
    VocabSpec("う", "{speculation | will/invitation}", ['う']),
    VocabSpec("戻す", "To Return, To Return Something", ['もどす']),
    VocabSpec("よ", "prt: s.end{emphasis/!} | hey(!)/hold-on(!)", ['よ']),
    VocabSpec("先生", "Teacher, Sensei, Doctor", ['せんせい']),
    VocabSpec("のに", "and-yet/although", ['のに']),
    VocabSpec("まま", "(remaining/leaving)-{as-is/unchanged}", ['まま']),
    VocabSpec("見る", "to{}: see/look | examine | aux{try}", ['みる']),
    VocabSpec("観る", "To View, To Watch, To See", ['みる']),
    VocabSpec("みる", "to: aux: try/have-a-go-at | {see/find}-that", ['みる']),
    VocabSpec("知る", "To Know, To Learn, To Find Out", ['しる']),
    VocabSpec("です", "polite-copula{be/is}", ['です']),
    VocabSpec("ば", "if/when | if-you-only-X-then-Y", ['ば']),
    VocabSpec("捜す", "to{}: search-for {} | search{in/through} {}", ['さがす']),
    VocabSpec("探す", "to{}: search-for {} | search{in/through} {}", ['さがす']),
]

# Generated by test_create_sample_data()
test_vocab_list = test_special_vocab + test_ordinary_vocab_list
