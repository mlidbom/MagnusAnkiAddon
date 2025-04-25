from typing import Generator
import pytest

from fixtures import collection_factory
from fixtures.stub_factory import stub_ui_dependencies
from sysutils.typed import non_optional
from ankiutils import app

@pytest.fixture(scope="function", autouse=True)
def setup() -> Generator[None, None, None]:
    with (stub_ui_dependencies(), collection_factory.inject_anki_collection_with_select_data(kanji=True)):
        yield

def test_inside_radical_population() -> None:
    inside = non_optional(app.col().kanji.with_kanji("内"))
    inside.set_user_mnemonic("<rad>head</rad> <rad>person</rad>")

    inside.populate_radicals_from_mnemonic_tags()
    assert inside.get_radicals() == ['冂', '人']

def test_bootstrap_mnemonic() -> None:
    inside = non_optional(app.col().kanji.with_kanji("内"))
    inside._set_radicals("冂, 人")

    inside.bootstrap_mnemonic_from_radicals()
    assert inside.get_user_mnemonic() == "<rad>head</rad> <rad>person</rad> <kan>inside</kan>"


def test_get_primary_meaning() -> None:
    one = non_optional(app.col().kanji.with_kanji("一"))
    assert one.get_primary_radical_meaning() == "ground"

    hon = non_optional(app.col().kanji.with_kanji("本"))
    assert hon.get_primary_radical_meaning() == "true"
