from parsing.universal_dependencies.ginza.ginza_parser import GinzaParser
from parsing.universal_dependencies.core.ud_parser import UDParser
from parsing.universal_dependencies.unidic2ud.unidic2ud_parser import UD2UDParser

ginza = GinzaParser() # Yes. 15 Differences to gendai. 8 Better, 6 worse, one unclear.
best = ginza
gendai = UD2UDParser("gendai")  # Yes. 15 Differences to ginza. 6 Better, 8 worse, one unclear.
spoken = UD2UDParser("spoken")  # ??. Zero differences compared to gendai so far...

qkana = UD2UDParser("qkana")  # Maybe. 2 difference with gendai. One clearly better and used in tests(Not any more. Ginza, the current winner handled this case fine.).
kindai = UD2UDParser("kindai")  # Maybe. 8 Differences with gendai. One clearly better and used in tests(Not any more. Ginza, the current winner handled this case fine.).
default = UD2UDParser("built-in")  # Maybe. 14 differences with gendai. One clearly better and used in tests(Not any more. Ginza, the current winner handled this case fine.).
kinsei = UD2UDParser("kinsei")  # Maybe. 6 differences with gendai. One clearly better and used in tests(Not any more. Ginza, the current winner handled this case fine.). 1 arguably better

# novel = UD2UDParser("novel") # NO. 2 difference with gendai. Both worse. Not worth the odds to try for the user.
# kyogen = UD2UDParser("kyogen") # NO. 18 differences with gendai. Consistently strange. Did often pick up kanji 無い but that was the only upside.
# wakan = UD2UDParser("wakan") #NO. 27 differences with gendai. Consistently strange.
# wabun = UD2UDParser("wabun") #NO. 27 differences with gendai. Consistently strange.
# manyo = UD2UDParser("manyo") #NO. 25 differences with gendai. Consistently strange.


all_parsers:list[UDParser] = [ginza,
                              gendai,
                              spoken,
                              qkana,
                              kindai,
                              default,
                              kinsei,
                              # novel, kyogen, wakan, wabun, manyo
                              ]
