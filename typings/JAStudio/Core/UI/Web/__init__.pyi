import typing, abc
from System.Collections.Generic import Dictionary_2
from System import Func_2

class PreRenderingContentRenderer_GenericClasses(abc.ABCMeta):
    Generic_PreRenderingContentRenderer_GenericClasses_PreRenderingContentRenderer_1_TNote = typing.TypeVar('Generic_PreRenderingContentRenderer_GenericClasses_PreRenderingContentRenderer_1_TNote')
    def __getitem__(self, types : typing.Type[Generic_PreRenderingContentRenderer_GenericClasses_PreRenderingContentRenderer_1_TNote]) -> typing.Type[PreRenderingContentRenderer_1[Generic_PreRenderingContentRenderer_GenericClasses_PreRenderingContentRenderer_1_TNote]]: ...

PreRenderingContentRenderer : PreRenderingContentRenderer_GenericClasses

PreRenderingContentRenderer_1_TNote = typing.TypeVar('PreRenderingContentRenderer_1_TNote')
class PreRenderingContentRenderer_1(typing.Generic[PreRenderingContentRenderer_1_TNote]):
    def __init__(self, renderMethods: Dictionary_2[str, Func_2[PreRenderingContentRenderer_1_TNote, str]]) -> None: ...
    def Render(self, note: PreRenderingContentRenderer_1_TNote, html: str, typeOfDisplay: str) -> str: ...

