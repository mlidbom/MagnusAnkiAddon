from language_services.universal_dependencies.shared.tokenizing.ud_tokenizer import UDTokenizer
from language_services.universal_dependencies.unidic2ud.unidic2ud_tokenizer import UD2UDTokenizer

#gendai is the current leader, mostly because 1. It has few dependencies 2. It comes with a bunch of other tokenizers
gendai: UDTokenizer = UD2UDTokenizer("gendai")  # Yes. 15 Differences to ginza. 6 Better, 8 worse, one unclear.

spoken: UDTokenizer = UD2UDTokenizer("spoken")  # ??. Zero differences compared to gendai so far...
qkana: UDTokenizer = UD2UDTokenizer("qkana")  # Maybe. 2 difference with gendai. One clearly better and used in tests(Not any more. Ginza, the current winner handled this case fine.).
kindai: UDTokenizer = UD2UDTokenizer("kindai")  # Maybe. 8 Differences with gendai. One clearly better and used in tests(Not any more. Ginza, the current winner handled this case fine.).
built_in: UDTokenizer = UD2UDTokenizer("built-in")  # Maybe. 14 differences with gendai. One clearly better and used in tests(Not any more. Ginza, the current winner handled this case fine.).
kinsei: UDTokenizer = UD2UDTokenizer("kinsei")  # Maybe. 6 differences with gendai. One clearly better and used in tests(Not any more. Ginza, the current winner handled this case fine.). 1 arguably better

# novel = UD2UDParser("novel") # NO. 2 difference with gendai. Both worse. Not worth the odds to try for the user.
# kyogen = UD2UDParser("kyogen") # NO. 18 differences with gendai. Consistently strange. Did often pick up kanji 無い but that was the only upside.
# wakan = UD2UDParser("wakan") #NO. 27 differences with gendai. Consistently strange.
# wabun = UD2UDParser("wabun") #NO. 27 differences with gendai. Consistently strange.
# manyo = UD2UDParser("manyo") #NO. 25 differences with gendai. Consistently strange.


representative_tokenizers: list[UDTokenizer] = [gendai]

# noinspection PyUnusedName
all_tokenizers: list[UDTokenizer] = [
    gendai,
    spoken,
    built_in,
    qkana,
    kindai,
    kinsei,
    # novel, kyogen, wakan, wabun, manyo
]
