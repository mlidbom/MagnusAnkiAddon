import typing
from Avalonia.Media import IImageBrushSource
from Avalonia.Platform import PixelFormat, AlphaFormat, ILockedFramebuffer
from Avalonia import PixelSize, Vector, Size, PixelRect
from System.IO import Stream

class Bitmap(IImageBrushSource):
    @typing.overload
    def __init__(self, fileName: str) -> None: ...
    @typing.overload
    def __init__(self, format: PixelFormat, alphaFormat: AlphaFormat, data: int, size: PixelSize, dpi: Vector, stride: int) -> None: ...
    @typing.overload
    def __init__(self, stream: Stream) -> None: ...
    @property
    def AlphaFormat(self) -> typing.Optional[AlphaFormat]: ...
    @property
    def Dpi(self) -> Vector: ...
    @property
    def Format(self) -> typing.Optional[PixelFormat]: ...
    @property
    def PixelSize(self) -> PixelSize: ...
    @property
    def Size(self) -> Size: ...
    def CreateScaledBitmap(self, destinationSize: PixelSize, interpolationMode: BitmapInterpolationMode = ...) -> Bitmap: ...
    @staticmethod
    def DecodeToHeight(stream: Stream, height: int, interpolationMode: BitmapInterpolationMode = ...) -> Bitmap: ...
    @staticmethod
    def DecodeToWidth(stream: Stream, width: int, interpolationMode: BitmapInterpolationMode = ...) -> Bitmap: ...
    def Dispose(self) -> None: ...
    # Skipped CopyPixels due to it being static, abstract and generic.

    CopyPixels : CopyPixels_MethodGroup
    class CopyPixels_MethodGroup:
        @typing.overload
        def __call__(self, buffer: ILockedFramebuffer, alphaFormat: AlphaFormat) -> None:...
        @typing.overload
        def __call__(self, sourceRect: PixelRect, buffer: int, bufferSize: int, stride: int) -> None:...

    # Skipped Save due to it being static, abstract and generic.

    Save : Save_MethodGroup
    class Save_MethodGroup:
        @typing.overload
        def __call__(self, fileName: str, quality: typing.Optional[int] = ...) -> None:...
        @typing.overload
        def __call__(self, stream: Stream, quality: typing.Optional[int] = ...) -> None:...



class BitmapBlendingMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unspecified : BitmapBlendingMode # 0
    SourceOver : BitmapBlendingMode # 1
    Source : BitmapBlendingMode # 2
    Destination : BitmapBlendingMode # 3
    DestinationOver : BitmapBlendingMode # 4
    SourceIn : BitmapBlendingMode # 5
    DestinationIn : BitmapBlendingMode # 6
    SourceOut : BitmapBlendingMode # 7
    DestinationOut : BitmapBlendingMode # 8
    SourceAtop : BitmapBlendingMode # 9
    DestinationAtop : BitmapBlendingMode # 10
    Xor : BitmapBlendingMode # 11
    Plus : BitmapBlendingMode # 12


class BitmapInterpolationMode(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unspecified : BitmapInterpolationMode # 0
    None_ : BitmapInterpolationMode # 1
    LowQuality : BitmapInterpolationMode # 2
    MediumQuality : BitmapInterpolationMode # 3
    HighQuality : BitmapInterpolationMode # 4

