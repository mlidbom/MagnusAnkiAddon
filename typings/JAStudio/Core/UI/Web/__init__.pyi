import typing, abc
from System import Func_5, Func_2
from System.Collections.Generic import Dictionary_2

class AppendingPrerenderer_GenericClasses(abc.ABCMeta):
    Generic_AppendingPrerenderer_GenericClasses_AppendingPrerenderer_1_TNote = typing.TypeVar('Generic_AppendingPrerenderer_GenericClasses_AppendingPrerenderer_1_TNote')
    def __getitem__(self, types : typing.Type[Generic_AppendingPrerenderer_GenericClasses_AppendingPrerenderer_1_TNote]) -> typing.Type[AppendingPrerenderer_1[Generic_AppendingPrerenderer_GenericClasses_AppendingPrerenderer_1_TNote]]: ...

AppendingPrerenderer : AppendingPrerenderer_GenericClasses

AppendingPrerenderer_1_TNote = typing.TypeVar('AppendingPrerenderer_1_TNote')
class AppendingPrerenderer_1(typing.Generic[AppendingPrerenderer_1_TNote]):
    def __init__(self, renderIframe: Func_5[AppendingPrerenderer_1_TNote, str, str, str, str]) -> None: ...
    def Render(self, note: AppendingPrerenderer_1_TNote, html: str, typeOfDisplay: str, cardTemplateName: str) -> str: ...


class CardServerUrl(abc.ABC):
    @classmethod
    @property
    def BaseUrl(cls) -> str: ...
    @classmethod
    @BaseUrl.setter
    def BaseUrl(cls, value: str) -> str: ...


class PreRenderingContentRenderer_GenericClasses(abc.ABCMeta):
    Generic_PreRenderingContentRenderer_GenericClasses_PreRenderingContentRenderer_1_TNote = typing.TypeVar('Generic_PreRenderingContentRenderer_GenericClasses_PreRenderingContentRenderer_1_TNote')
    def __getitem__(self, types : typing.Type[Generic_PreRenderingContentRenderer_GenericClasses_PreRenderingContentRenderer_1_TNote]) -> typing.Type[PreRenderingContentRenderer_1[Generic_PreRenderingContentRenderer_GenericClasses_PreRenderingContentRenderer_1_TNote]]: ...

PreRenderingContentRenderer : PreRenderingContentRenderer_GenericClasses

PreRenderingContentRenderer_1_TNote = typing.TypeVar('PreRenderingContentRenderer_1_TNote')
class PreRenderingContentRenderer_1(typing.Generic[PreRenderingContentRenderer_1_TNote]):
    def __init__(self, renderMethods: Dictionary_2[str, Func_2[PreRenderingContentRenderer_1_TNote, str]]) -> None: ...
    def Render(self, note: PreRenderingContentRenderer_1_TNote, html: str, typeOfDisplay: str, cardTemplateName: str) -> str: ...

