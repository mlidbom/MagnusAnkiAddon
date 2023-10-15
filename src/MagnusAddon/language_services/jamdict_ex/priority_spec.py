_maximum_tags = set([f"nf{num:02}" for num in range(0,10)])
_high_tags = set([f"nf{num}" for num in range(10,20)])
_common_tags = {"news1", "spec1"}
_semi_common_tags = {"news2", "ichi1", "spec2"}

class PrioritySpec:
    def __init__(self, tags: set[str]):
        self.tags = tags


    def priority(self) -> str:
        if self.tags & _maximum_tags:
            return "priority_maximum"
        elif self.tags & _high_tags:
            return "priority_high"
        elif self.tags & _common_tags:
            return "priority_medium"
        elif len(self.tags) > 0:
            return "priority_low"

        return "priority_very_low"
