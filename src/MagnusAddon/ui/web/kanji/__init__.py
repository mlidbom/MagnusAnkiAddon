from __future__ import annotations


def init() -> None:
    from . import dependencies, mnemonic, readings, vocab_list
    dependencies.init()
    mnemonic.init()
    readings.init()
    vocab_list.init()