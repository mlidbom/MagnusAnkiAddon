from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from jaslib import app
from jaspythonutils.sysutils.typed import non_optional
from jastudio_tests.fixtures import collection_factory
from jastudio_tests.fixtures.stub_factory import stub_ui_dependencies

if TYPE_CHECKING:
    from collections.abc import Iterator


# noinspection PyUnusedFunction
@pytest.fixture(scope="function", autouse=True)
def setup() -> Iterator[None]:
    with (stub_ui_dependencies(), collection_factory.inject_collection_with_select_data(kanji=True)):
        app.config().set_readings_mappings_for_testing(_readings_mappings)
        yield

def test_inside_radical_population() -> None:
    inside = non_optional(app.col().kanji.with_kanji("内"))
    inside.set_user_mnemonic("<rad>head</rad> <rad>person</rad>")

    inside.populate_radicals_from_mnemonic_tags()
    assert inside.get_radicals() == ["冂", "人"]

@pytest.mark.parametrize("kanji, radicals, mnemonic", [
    ("内", ["冂, 人"], "<rad>head</rad> <rad>person</rad> <kan>inside</kan> <compound-reading><read>U</read>ber-<read>chi</read>mp</compound-reading> ..."),
    ("病", ["疒","丙"], "<rad>sick</rad> <rad>dynamite</rad> <kan>illness</kan> <read>yu</read>ck <compound-reading><read>yu</read>ck-<read>mi</read>ce</compound-reading> <read>BO</read> ..."),
    ("品", [], "<kan>goods</kan> <read>hin</read>t <compound-reading><read>shi</read>t-<read>nu</read>t</compound-reading> ..."),
    ("塚", [], "<kan>a-mound</kan> <read>Tsuka</read> ...")
])
def test_bootstrap_mnemonic(kanji:str, radicals:list[str], mnemonic:str) -> None:
    kanji_note = non_optional(app.col().kanji.with_kanji(kanji))
    kanji_note._set_radicals(",".join(radicals))  # pyright: ignore[reportPrivateUsage]

    kanji_note.bootstrap_mnemonic_from_radicals()

    assert kanji_note.get_user_mnemonic() == mnemonic


def test_get_primary_meaning() -> None:
    one = non_optional(app.col().kanji.with_kanji("一"))
    assert one.get_primary_radical_meaning() == "ground"

    hon = non_optional(app.col().kanji.with_kanji("本"))
    assert hon.get_primary_radical_meaning() == "true"


_readings_mappings = """

aba:ABBA
afu:afoo:t
ai:eye
akoga:a-couga:r
ame:Ame:rican
an:an:chovie
asa:as-a
ashi:ash
ate:ate
atsu:at-Sue
ba:bu:tt
baku:backu:p
ban:bun
bei:bay
betsu:bets
bi:bee
bin:bin
bo:bo:t
bou:bow
bu:bu:tt
byou:BO
chi:chi:mp
chika:chick-a
chiku:chick
cho:cho:p
chou:Chou
chuu:chew
da:DA
dai:die
dama:Dama:scus
dan:done
de:dea:d
den:den
do:do:g
doku:dock
dou:door
e:E:lle
ei:a:pe
en:En:t
fu:foo:t
fuda:fooder
fuku:fuck
fun:fun
futsu:foot's
ga:gu:t
gai:guy
gan:gun
gatsu:guts
getsu:gets
gi:GI
giwa:give-a
go:go:b
gou:go
gun:gun
guu:goo
gyou:gyo:za
ha:hu:t
habu:hub
hada:had-a
hai:hi:de
haka:hacker
haku:hack
han:Hun
hashi:hash
he:hea:lth
hei:hay
heki:heck
hen:hen
hi:hi:t
hiku:hicku:p
hin:hin:t
hiro:he-row
hisa:hiss-a
hitsu:hits
hoo:haw
hou:haw
i:ea:gle
iku:ick
in:inn
ino:inno:vation
ita:Ita:ly
itona:<read>i</read>n<read>tona</read>tion
ji:ji:g
jin:gin
jo:Jo
jou:jaw
ju:ju:g
jutsu:nin<read>jutsu</read>
juu:je:wel
ka:cu:t
kai:kay:ak
kaku:cack:le
kame:came
kan:can
kane:canne:lloni
kara:Cara
kare:curry
kasu:cuss
kata:kata
katsu:cuts
kawa:Kawa:saki
kayu:<read>ca</read>n-<read>you</read>
ke:ke:ttle
kei:ca:ke
ketsu:ketsu:p
ki:key
kichi:kitche:n
kimo:kimo:no
kin:kin
kitsu:kits
ko:KO
kokoroyo:Kokoroyo
koku:cock
koma:coma
kon:con
kona:con-a
koto:koto
kou:caw
kowa:cowa:rd
ku:coo:k
kuku:cuckoo
kura:curra:nt
kuru:curry
kuu:coo
kyou:Kyou:to
kyuu:cue
ma:mu:t
machi:match
mai:mi:ce
maji:magi:c
maku:muck
mamo:mamo:gram
man:man
maru:ma-rue
masu:muss
mata:mata:dor
matsu:mutts
mei:may
metsu:met-Sue
mi:mi:tt
miso:miso
mitsu:mitts
mo:mo:p
mochi:mochi
moku:mock
moo:maw
moto:moto:r
mou:maw
moude:moude
mugi:muggy
muku:muck
na:nu:t
nan:nun
nani:nun-y
nano:nano
ne:ne:t
nega:nega:tion
nichi:Nietzche
no:kno:t
noo:gnaw
nou:gnaw
nu:nu:de
nyuu:new
oda:awe-da:d
odo:odo:meter
odoro:odor
omo:c<read>ommo</read>n
on:on
ona:on-a
oo:awe
oto:auto
otsu:oats
ou:awe
pa:pa
pai:pie
pan:pun:t
pi:pi:t
po:po:t
ppa:pa
rai:rye
raku:lucky
ran:run
rei:ray
ri:ri:p
rin:rin:g
ro:ro:t
ru:rue
ryuu:dragon
sa:su:d
sai:cy:borg
saida:aid-a
saka:sucker
saki:sucky
saku:suck
san:sun
satsu:satsu:ma
se:se:x
sei:sa:bre
seki:sexy
sen:cen:taur
setsu:sets
sha:sha:ft
shaku:shack
shi:shi:t
shiki:sheik-y
shin:shin
shino:shino:bu
shita:shitter
shitsu:Shih-Tzu
sho:sho:t
shoku:shock
shou:shou:gun
shutsu:shuts
shuu:shoe
so:so:t
soda:sawdu:st
soku:sock
son:son
sou:saw
su:soo:t
sui:swee:t
suki:ski
suko:Sco:t
suku:suck
suu:sue
tai:tie
taku:tack
tame:tame
tan:tan
tazu:taze-u
tei:ta:pe
teki:techie
ten:ten:t
to:to:t
tobira:to-be-ra:ther
ton:ton:s
too:toe
tori:tory
totsu:tots
tou:toe
tsu:tsu:n
tsubu:<read>tsu</read>ndere-<read>bu</read>ll
tsuka:Tsuka
tsuu:two
u:U:ber
ura:ura:nium
wa:wa:d
waka:walker
wan:one
wari:warri:or
wata:water
ya:yu:ck
yaku:yak
yo:ya:cht
yoku:yolk
you:you:ghurt
yuru:you-rue
yuu:you:th
zai:xy:lophone
zan:Zan:sibar
zo:zo:mbie
zoku:zock
zou:zou:mbie
zu:Zeu:s
"""