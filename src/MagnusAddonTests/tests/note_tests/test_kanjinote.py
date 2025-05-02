from typing import Generator
import pytest

from fixtures import collection_factory
from fixtures.stub_factory import stub_ui_dependencies
from sysutils.typed import non_optional
from ankiutils import app

# noinspection PyUnusedFunction
@pytest.fixture(scope="function", autouse=True)
def setup() -> Generator[None, None, None]:
    with (stub_ui_dependencies(), collection_factory.inject_anki_collection_with_select_data(kanji=True)):
        app.config().readings_mappings.set_value(_readings_mappings)
        yield

def test_inside_radical_population() -> None:
    inside = non_optional(app.col().kanji.with_kanji("内"))
    inside.set_user_mnemonic("<rad>head</rad> <rad>person</rad>")

    inside.populate_radicals_from_mnemonic_tags()
    assert inside.get_radicals() == ['冂', '人']

@pytest.mark.parametrize("kanji, radicals, mnemonic", [
    ("内", ["冂, 人"], "<rad>head</rad> <rad>person</rad> <kan>inside</kan>"),
    ("病", ["疒","丙"], "<rad>sick</rad> <rad>dynamite</rad> <kan>illness</kan> <read>ya</read>nkey <read>ya</read>nkey-<read>mi</read>ce <read>BO</read>")
])
def test_bootstrap_mnemonic(kanji:str, radicals:list[str], mnemonic:str) -> None:
    kanji_note = non_optional(app.col().kanji.with_kanji(kanji))
    kanji_note._set_radicals(",".join(radicals))

    kanji_note.bootstrap_mnemonic_from_radicals()

    print(kanji_note.get_user_mnemonic())
    print(mnemonic)
    assert kanji_note.get_user_mnemonic() == mnemonic


def test_get_primary_meaning() -> None:
    one = non_optional(app.col().kanji.with_kanji("一"))
    assert one.get_primary_radical_meaning() == "ground"

    hon = non_optional(app.col().kanji.with_kanji("本"))
    assert hon.get_primary_radical_meaning() == "true"


_readings_mappings= """

aba:ABBA
an:an:chovie
ba:bu:tt
baku:backu:p
ban:bun
bei:bay
bin:bin
bo:bo:t
bou:bow
bu:bu:tt
byou:BO
chi:chi:mp
chiku:chick
cho:cho:p
dai:die
dama:Dama:scus
dan:done
den:den
e:E:lle
en:En:t
fu:foo:t
fuda:fooder
fuku:fuck
gai:guy
gan:gun
gi:gui:llotine
giwa:give-a
ha:hu:t
hada:had-a
haka:hacker
haku:hack
han:Hun
hei:hay
hi:hi:t
hoo:haw
hou:haw
i:ea:gle
in:inn
ita:Ita:ly
ji:Je:sus
jin:gin
jou:jaw 
jutsu:nin<read>jutsu</read>
juu:je:wel
ka:cu:t
kai:kay:ak
kan:can
kara:Cara
kata:kata
katsu:cats
kawa:Kawa:saki
kei:ca:ke
ki:key
kimo:kimo:no
ko:KO
kou:caw
kura:curra:nt
kutsu:cuts
kyou:Kyou:to
ma:mu:t
machi:match
mai:mi:ce
maji:magi:c
maku:muck
man:man
matsu:mats
metsu:met-Sue
miso:miso
mo:mo:p
moku:mock
mou:more
moude:moude
mugi:muggy
muku:muck
na:nu:t
nan:nun
nani:nun-y
nano:nano
nega:nega:tion
odoro:odor
oo:awe
oto:auto
otsu:oats
ou:awe
pan:pun:t
raku:lucky
ran:run
ro:ro:t
ru:roo:k
ryuu:dragon
sai:cy:borg
saida:aid-a
san:sun
satsu:satsu:ma
se:se:x
sei:sa:bre
setsu:sets
sha:sha:man
shaku:shack
shi:shi:t
shiki:sheik-y
shitsu:Shih-Tzu
shoku:shock
shou:shou:gun
shuu:shoe
soku:sock
sou:saw
su:soo:t
suki:ski
suu:sue
tai:tie
tan:tan
tazu:taze-u
tei:ta:pe
ten:ten:t
to:to:t
ton:ton:s
too:toe
tou:toe
tsu:tsu:ndere
tsubu:<read>tsu</read>ndere-<read>bu</read>ll
tsuu:two
u:U:ber
waka:walker
wan:one
wata:water
ya:ya:nkey
yo:ya:cht
you:yo:ghurt
yuu:you:th
zo:zo:mbie
zou:zou:mbie
"""