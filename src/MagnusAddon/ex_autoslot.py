from __future__ import annotations

from manually_copied_in_libraries.autoslot import SlotsPlusDict

# todo prorably add some code here to only use PlusDict when profiling and save us that overhead when not profiling, like ProfilableAutoSlots = SlotsPlusDict if os.environ.get('LINE_PROFILE') else Slots
class ProfilableAutoSlots(SlotsPlusDict):
    pass