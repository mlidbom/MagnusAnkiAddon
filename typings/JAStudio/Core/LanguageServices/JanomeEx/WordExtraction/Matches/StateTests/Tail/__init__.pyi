import abc
from JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements import CustomForbidsNoCache, VocabMatchInspector
from JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head import FailedMatchRequirement

class ForbidsHasDisplayedOverlappingFollowingCompound(CustomForbidsNoCache):
    @property
    def Description(self) -> str: ...
    @property
    def FailureReason(self) -> str: ...
    @property
    def IsFulfilled(self) -> bool: ...
    @property
    def IsInState(self) -> bool: ...
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> ForbidsHasDisplayedOverlappingFollowingCompound: ...


class ForbidsSuffixIsIn(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbidsIsSentenceEnd(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...

