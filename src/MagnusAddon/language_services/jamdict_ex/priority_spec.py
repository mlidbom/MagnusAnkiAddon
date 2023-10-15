_maximum_tags = set([f"nf{num:02}" for num in range(0,10)])
_high_tags = set([f"nf{num}" for num in range(10,20)])
_common_tags = {"news1", "spec1"}
_semi_common_tags = {"news2", "ichi1", "spec2"}

class PrioritySpec:
    def __init__(self, tags: set[str]):
        self.tags = tags

        if self.tags & _maximum_tags:
            self.priority_string = "priority_maximum"
            self.priority = 0
        elif self.tags & _high_tags:
            self.priority_string = "priority_high"
            self.priority = 1
        elif self.tags & _common_tags:
            self.priority_string = "priority_medium"
            self.priority = 2
        elif len(self.tags) > 0:
            self.priority_string = "priority_low"
            self.priority = 3
        else:
            self.priority_string = "priority_very_low"
            self.priority = 4
