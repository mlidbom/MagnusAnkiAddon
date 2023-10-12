from __future__ import annotations

unknown = "unknown"
very_low = "very_low"
low = "low"
medium = "medium"
high = "high"
very_high = "very_high"

hard_coded_base_priorities: dict[str, str] = dict()
hard_coded_surface_priorities: dict[str, str] = dict()

lowest_priority_surfaces: set[str] = set()
# for particle in "しもよかとたてでをなのにだがは": hard_coded_base_priorities[particle] = priorities.very_low
# for word in "する|です|私|なる|この|あの|その|いる|ある".split("|"): hard_coded_base_priorities[word] = priorities.low
