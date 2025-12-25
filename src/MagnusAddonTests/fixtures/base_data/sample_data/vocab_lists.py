from __future__ import annotations

from fixtures.base_data.sample_data.vocab_spec import VocabSpec
from note.note_constants import Tags

v = Tags.Vocab
vm = Tags.Vocab.Matching

test_special_vocab: list[VocabSpec] = [
    # <non-standard-token-splitting-to-enable-more-pedagogical-breakdowns-for-conjugations>
    # godan potential
    VocabSpec("える", "to-be-able-to", ["える"],
              forms=["える", "ける", "せる", "てる", "ねる", "へる", "める", "れる", "げる", "ぜる", "でる", "べる", "ぺる"],
              tags=[vm.is_inflecting_word, vm.Requires.godan_potential, Tags.Vocab.question_overrides_form]),
    VocabSpec("えない", "unable-able-to", ["えない"], compounds=["える", "ない"], tags=[vm.is_inflecting_word]),
    # /godan potential
    VocabSpec("え", "_!/do! (godan imperative)", ["え"], forms=["え", "け", "せ", "ね", "へ", "め", "れ", "げ", "ぜ", "で", "べ", "ぺ"], tags=[vm.is_inflecting_word, vm.Requires.godan_imperative, Tags.Vocab.question_overrides_form]),

    # needs exclusion
    VocabSpec("させる", "get-_/is-_", ["させる"], forms=["せる"], tags=[vm.is_inflecting_word, vm.Forbids.godan_potential]),
    VocabSpec("頑張れ", "do-your-best!", tags=[vm.Forbids.godan_potential]),
    VocabSpec("あれても", forms=["れても"], compounds=["あれる", "ても"], tags=[vm.yield_last_token_to_overlapping_compound, vm.Requires.a_stem, vm.Forbids.godan_potential, Tags.Vocab.question_overrides_form]),
    # /needs exclusion
    # </non-standard-token-splitting-to-enable-more-pedagogical-breakdowns-for-conjugations>

    # <te-stem-required>
    VocabSpec("て", "{continuing-action}", ["て"], tags=[vm.is_inflecting_word, vm.Requires.te_form_stem]),
    VocabSpec("てる", "{continuing-{activity | state}} / {progressive | perfect}", ["てる"], tags=[vm.is_inflecting_word, vm.Requires.te_form_stem]),
    VocabSpec("ている", "is-_-ing", readings=["ている"], tags=[vm.is_inflecting_word, vm.Requires.te_form_stem]),
    VocabSpec("てた", "{was}-{_-ing|_ed}", ["てた"], tags=[vm.is_inflecting_word, vm.Requires.te_form_stem]),
    VocabSpec("てたら", "{was}-{_-ing|_ed}", ["てたら"], tags=[vm.is_inflecting_word, vm.Requires.te_form_stem]),

    VocabSpec("んで", "and/て", forms=["で"], prefix_in={"ん"}, tags=[vm.Requires.te_form_stem, Tags.Vocab.question_overrides_form]),
    VocabSpec("んどる", forms=["どる"], prefix_in={"ん"}, tags=[Tags.Vocab.question_overrides_form, vm.Requires.te_form_stem]),
    VocabSpec("んでる", forms=["でる"], prefix_in={"ん"}, tags=[Tags.Vocab.question_overrides_form, vm.Requires.te_form_stem]),
    # </te-stem-required>
    # <te-stem-forbidden>
    VocabSpec("で", tags=[vm.Forbids.te_form_stem]),
    VocabSpec("でいる", tags=[vm.Forbids.te_form_stem]),
    VocabSpec("んで", "thing-is", tags=[vm.Forbids.te_form_stem]),
    # </te-stem-forbidden>
    VocabSpec("１人で", compounds=["で", "１人"], tags=[vm.yield_last_token_to_overlapping_compound]),
    VocabSpec("ないで", compounds=["ない", "で"], tags=[vm.yield_last_token_to_overlapping_compound]),

    # <past-tense-required>
    VocabSpec("た", "{past-tense} | (please)do", ["た"], surface_not={"たら"}, tags=[vm.is_inflecting_word, vm.Requires.past_tense_stem]),
    VocabSpec("んだ", "did/was", forms=["だ"], tags=[vm.Requires.past_tense_stem, vm.is_inflecting_word, Tags.Vocab.question_overrides_form]),
    # <past-tense-required>
    # <past-tense-forbidden>
    VocabSpec("んだ", "thing-is", tags=[vm.Requires.exact_match, vm.yield_last_token_to_overlapping_compound, vm.Forbids.past_tense_stem]),
    VocabSpec("たって", tags=[vm.Forbids.past_tense_stem]),
    VocabSpec("だ", surface_not={"なら", "な"}, tags=[vm.is_inflecting_word, vm.Forbids.past_tense_stem]),
    # </past-tense-forbidden>

    VocabSpec("たら", "conj{if/when} prt{as-for | why-not..  | I-said!/I-tell-you!}", ["たら"], tags=[vm.is_inflecting_word]),
    VocabSpec("ちゃう", "to do: accidentally/unfortunately | completely", ["ちゃう"], tags=[vm.is_inflecting_word]),
    VocabSpec("ても良い", "{concession/compromise} | {permission}", ["てもいい"], tags=[vm.is_inflecting_word]),
    VocabSpec("すぎる", "too-much", ["すぎる"], tags=[vm.is_inflecting_word]),
    VocabSpec("いらっしゃいます", "to: come/be/do", ["いらっしゃいます"]),
    VocabSpec("を頼む", "I-entrust-to-you", ["を頼む"], tags=[vm.Requires.exact_match]),
    VocabSpec("作れる", "to-be-able: to-make", ["つくれる"], compounds=["作る", "える"]),
    VocabSpec("たい", "want to", ["たい"], tags=[vm.is_inflecting_word]),
    VocabSpec("解放する", "to{} release", ["かいほうする"]),


    # require a stems
    VocabSpec("あれる", "get-_/is-_", ["あれる"], forms=["れる"], tags=[vm.Requires.a_stem, v.question_overrides_form, vm.is_inflecting_word]),
    VocabSpec("あせる", "get-_/is-_", ["あせる"], forms=["せる"], tags=[vm.Requires.a_stem, v.question_overrides_form, vm.is_inflecting_word]),

    VocabSpec("する", "to: do", yield_to_surface={"しろ"}),
    VocabSpec("しろ", "do!", ["しろ"]),
    VocabSpec("らっしゃる", yield_to_surface={"らっしゃい"}),
    VocabSpec("らっしゃい"),

    VocabSpec("ぬ", "not", ["ぬ"], surface_not={"ず"}),

    VocabSpec("だの", "and-the-like", ["だの"], prefix_not={"ん"}),

    VocabSpec("こ", "familiarizing-suffix", ["こ"], forms=["っこ"], tags=[vm.Forbids.sentence_start]),

    VocabSpec("ない", "not", forms=["ない"], tags=[vm.is_inflecting_word]),
    VocabSpec("無い", "not", forms=["ない"], tags=[vm.is_inflecting_word]),
    VocabSpec("うまい", yield_to_surface={"うまく"}),
    VocabSpec("うまく"),
    VocabSpec("笑える", tos="ichidan verb"),

    VocabSpec("にする", "to: turn-into"),
    VocabSpec("のか", tags=[vm.Requires.sentence_end]),
    VocabSpec("ないと", tags=[vm.yield_last_token_to_overlapping_compound]),
    VocabSpec("して", tags=[vm.yield_last_token_to_overlapping_compound]),
    VocabSpec("ても"),
    VocabSpec("と思う"),
    VocabSpec("たの", tags=[vm.is_poison_word]),

    VocabSpec("たかな", tags=[vm.is_poison_word]),
    VocabSpec("たか", tags=[vm.is_poison_word]),
    VocabSpec("なんて", tags=[vm.yield_last_token_to_overlapping_compound]),
    VocabSpec("何て", tags=[vm.yield_last_token_to_overlapping_compound]),
    VocabSpec("というか", forms=["[と言うか]", "っていうか", "ていうか", "て言うか"]),
    VocabSpec("ていうか", forms=["と言うか", "というか", "っていうか", "[て言うか]"]),
    VocabSpec("鰻", forms=["[うな]"], prefix_not={"ろ", "よ"}),
    VocabSpec("書き"),
    VocabSpec("なさい", tags=[vm.is_inflecting_word]),
    VocabSpec("風の強い", tags=[vm.Requires.exact_match]),
    VocabSpec("たね", tags=[vm.Requires.single_token]),
    VocabSpec("たらしい", tags=[vm.Requires.single_token]),
    VocabSpec("に決まる", forms=["に決る", "に決まる", "に極る"]),
    VocabSpec("に決まってる", forms=["に決っている", "に決まっている", "に極っている", "に決ってる", "に決まってる", "に極ってる"]),
    VocabSpec("された", surface_not={"されたら"}),

    VocabSpec("んです", tags=[vm.Requires.exact_match, vm.yield_last_token_to_overlapping_compound]),

    VocabSpec("たん", forms=["たの"], tags=[vm.Requires.single_token]),
    VocabSpec("たの", forms=["たん"], tags=[vm.yield_last_token_to_overlapping_compound]),
    VocabSpec("たんだ", tags=[vm.yield_last_token_to_overlapping_compound]),
    VocabSpec("んだろう", tags=[vm.is_poison_word]),
    VocabSpec("しちゃう"),
    VocabSpec("ものを", tags=[vm.Requires.sentence_end]),
    VocabSpec("いいものを", forms=["よいものを", "良いものを", "かったものを"], tags=[vm.Requires.sentence_end]),
    VocabSpec("に行く", compounds=["に", "行く"], tags=[vm.yield_last_token_to_overlapping_compound]),
    VocabSpec("行った", compounds=["行く", "た"], tags=[vm.yield_last_token_to_overlapping_compound]),

    VocabSpec("うと", compounds=["う", "と"], tags=[vm.yield_last_token_to_overlapping_compound]),
    VocabSpec("と思って", compounds=["と思う", "て"], tags=[vm.yield_last_token_to_overlapping_compound]),
    VocabSpec("ませ", forms=["まし"], suffix_not={"ん"}),
    VocabSpec("ところが", tags=[vm.Requires.sentence_start]),

    VocabSpec("成る", "to: become | result-in | turn-into", ["なる"], prefix_not={"く"}),
    VocabSpec("なる", "to: become | result-in | turn-into", ["なる"], prefix_not={"く"}),
    VocabSpec("くなる", "to: become", ["くなる"], forms=["なる"], prefix_in={"く"}, tags=[Tags.Vocab.question_overrides_form]),
    VocabSpec("言える", "to-be: able-to-say", compounds=["言う","える"]),
    VocabSpec("出会える", "to: be-{able/fortunate-enough}-to-{meet/come-across}"),
    VocabSpec("ていける", "can-go-on"),

    VocabSpec("ても知らない", forms=["ても知らん"], compounds=["ても", "知る", "ん"], tags=[vm.Requires.te_form_stem])
]