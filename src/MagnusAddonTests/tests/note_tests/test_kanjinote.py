from typing import Generator
import pytest

from fixtures import collection_factory
from fixtures.stub_factory import stub_ui_dependencies
from sysutils.typed import non_optional
from ankiutils import app

@pytest.fixture(scope="function", autouse=True)
def setup() -> Generator[None, None, None]:
    with (stub_ui_dependencies(), collection_factory.inject_anki_collection_with_generated_sample_data()):
        yield

def test_inside_radical_population() -> None:
    inside = non_optional(app.col().kanji.with_kanji("内"))
    inside.set_user_mnemonic("<rad>head</rad> <rad>person</rad>")

    inside.populate_radicals_from_mnemonic_tags()
    assert inside.get_radicals() == ['冂', '人']
