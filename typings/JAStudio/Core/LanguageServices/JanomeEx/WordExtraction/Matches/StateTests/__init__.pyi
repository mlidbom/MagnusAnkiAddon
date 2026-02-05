import abc
from JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.StateTests.Head import FailedMatchRequirement
from JAStudio.Core.LanguageServices.JanomeEx.WordExtraction.Matches.Requirements import VocabMatchInspector, MatchInspector, MatchRequirement

class ForbidsAnotherMatchIsHigherPriority(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class ForbidsCompositionallyTransparentCompound(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class ForbidsConfiguredToHideAllCompounds(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: MatchInspector) -> FailedMatchRequirement: ...


class ForbidsDictionaryInflectionSurfaceWithBase(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: MatchInspector) -> FailedMatchRequirement: ...


class ForbidsDictionaryVerbFormStemAsCompoundEnd(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: MatchInspector) -> FailedMatchRequirement: ...


class ForbidsIsConfiguredHidden(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: MatchInspector) -> FailedMatchRequirement: ...


class ForbidsIsConfiguredIncorrect(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: MatchInspector) -> FailedMatchRequirement: ...


class ForbidsIsGodanImperativeInflectionWithBase(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: MatchInspector) -> FailedMatchRequirement: ...


class ForbidsIsGodanPotentialInflectionWithBase(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: MatchInspector) -> FailedMatchRequirement: ...


class ForbidsIsPoisonWord(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class ForbidsIsShadowed(MatchRequirement):
    def __init__(self, inspector: MatchInspector) -> None: ...
    @property
    def FailureReason(self) -> str: ...
    @property
    def IsFulfilled(self) -> bool: ...


class ForbidsSurfaceIfBaseIsValidAndContextIndicatesAVerb(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: MatchInspector) -> FailedMatchRequirement: ...


class ForbidsSurfaceIsIn(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class ForbidsYieldsToValidSurfaceSurface(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbidsIsSingleToken(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbidsStartsWithGodanImperativeStemOrInflection(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbidsStartsWithGodanPotentialStemOrInflection(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbidsStartsWithIchidanImperativeStemOrInflection(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...


class RequiresOrForbidsSurface(abc.ABC):
    @staticmethod
    def ApplyTo(inspector: VocabMatchInspector) -> FailedMatchRequirement: ...

