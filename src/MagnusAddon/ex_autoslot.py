from __future__ import annotations

from autoslot import SlotsPlusDict  # noqa: F401  # pyright: ignore

# todo prorably add some code here to only use PlusDict when profiling and save us that overhead when not profiling, like ProfilableAutoSlots = SlotsPlusDict if os.environ.get('LINE_PROFILE') else Slots
ProfilableAutoSlots = SlotsPlusDict