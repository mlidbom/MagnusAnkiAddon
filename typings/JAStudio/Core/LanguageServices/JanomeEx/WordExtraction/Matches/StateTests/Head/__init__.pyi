import abc
from JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements import MatchRequirement, MatchInspector, VocabMatchInspector
from System import Func_2
from JAStudio.Core.Note.NoteFields import RequireForbidFlagField

class FailedMatchRequirement(MatchRequirement):
    @property
    def FailureReason(self) -> str: ...
    @property
    def IsFulfilled(self) -> bool: ...
    @property
    def Reason(self) -> str: ...
    @staticmethod
    def Forbids(message: str) -> FailedMatchRequirement: ...
    @staticmethod
    def Required(message: str) -> FailedMatchRequirement: ...


class Forbids:
    def __init__(self, name: str, isInState: Func_2[MatchInspector, bool]) -> None: ...
    def ApplyTo(self, inspector: MatchInspector) -> FailedMatchRequirement: ...


class ForbidsPrefixIsIn(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbids:
    def __init__(self, name: str, getRequirement: Func_2[VocabMatchInspector, RequireForbidFlagField], isInState: Func_2[VocabMatchInspector, bool]) -> None: ...
    def ApplyTo(self, inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbidsDictionaryFormPrefix(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbidsDictionaryFormStem(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbidsHasGodanImperativePrefix(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbidsHasPastTenseStem(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbidsHasTeFormStem(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbidsIsSentenceStart(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbidsMasuStem(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbidsPrecedingAdverb(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresPrefixIsIn(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...

