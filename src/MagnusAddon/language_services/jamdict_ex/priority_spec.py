_maximum_tags = set([f"nf{num:02}" for num in range(1,9)])
_high_tags = set([f"nf{num}" for num in range(10,20)])
_common_tags = {"news1", "spec1"}
_semi_common_tags = {"news2", "ichi1", "spec2"}

class PrioritySpec:
    def __init__(self, tags: set[str]):
        self.tags = tags

        if self.tags & _maximum_tags:
            self.priority_string = "priority_maximum"
            self.priority = int(list(self.tags & _maximum_tags)[0][-1]) #the actual number from the nf tag
        elif self.tags & _high_tags:
            self.priority_string = "priority_high"
            self.priority = int(list(self.tags & _high_tags)[0][-2:]) #the actual number from the nf tag
        elif self.tags & _common_tags:
            self.priority_string = "priority_medium"
            self.priority = 30
        elif len(self.tags) > 0:
            self.priority_string = "priority_low"
            self.priority = 40
        else:
            self.priority_string = "priority_very_low"
            self.priority = 50
