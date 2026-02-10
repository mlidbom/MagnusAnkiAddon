import typing, abc
from System import IDisposable, Delegate, IFormattable, IEquatable_1, IFormatProvider
from Avalonia.Media.Imaging import Bitmap
from Avalonia import PixelPoint, Point, StyledProperty_1, DirectProperty_2, Rect, Size, Thickness, StyledElement, RelativePoint, AvaloniaObject, AvaloniaProperty, Visual, Vector
from Avalonia.Interactivity import RoutedEventArgs, RoutingStrategies, RoutedEvent, Interactive, RoutedEvent_1
from System.Collections.Generic import IEnumerable_1, List_1, IReadOnlyList_1
from Avalonia.Input.Raw import RawInputEventArgs
from Avalonia.Platform import IPlatformSettings
from Avalonia.Input.TextInput import TextInputMethodClientRequestedEventArgs
from Avalonia.Styling import ThemeVariant, Styles, ControlTheme
from Avalonia.Controls import Classes, IResourceDictionary
from Avalonia.Media import Geometry, IEffect, FlowDirection, IBrush, ITransform
from Avalonia.Input.GestureRecognizers import GestureRecognizerCollection
from Avalonia.Layout import HorizontalAlignment, VerticalAlignment
from Avalonia.Animation import Transitions
from Avalonia.Data import IndexerDescriptor, IBinding
from System.Windows.Input import ICommand

class Cursor(IDisposable):
    @typing.overload
    def __init__(self, cursor: Bitmap, hotSpot: PixelPoint) -> None: ...
    @typing.overload
    def __init__(self, cursorType: StandardCursorType) -> None: ...
    Default : Cursor
    def Dispose(self) -> None: ...
    @staticmethod
    def Parse(s: str) -> Cursor: ...
    def ToString(self) -> str: ...


class GotFocusEventArgs(RoutedEventArgs):
    def __init__(self) -> None: ...
    @property
    def Handled(self) -> bool: ...
    @Handled.setter
    def Handled(self, value: bool) -> bool: ...
    @property
    def KeyModifiers(self) -> KeyModifiers: ...
    @KeyModifiers.setter
    def KeyModifiers(self, value: KeyModifiers) -> KeyModifiers: ...
    @property
    def NavigationMethod(self) -> NavigationMethod: ...
    @NavigationMethod.setter
    def NavigationMethod(self, value: NavigationMethod) -> NavigationMethod: ...
    @property
    def Route(self) -> RoutingStrategies: ...
    @Route.setter
    def Route(self, value: RoutingStrategies) -> RoutingStrategies: ...
    @property
    def RoutedEvent(self) -> RoutedEvent: ...
    @RoutedEvent.setter
    def RoutedEvent(self, value: RoutedEvent) -> RoutedEvent: ...
    @property
    def Source(self) -> typing.Any: ...
    @Source.setter
    def Source(self, value: typing.Any) -> typing.Any: ...


class HoldingRoutedEventArgs(RoutedEventArgs):
    def __init__(self, holdingState: HoldingState, position: Point, pointerType: PointerType) -> None: ...
    @property
    def Handled(self) -> bool: ...
    @Handled.setter
    def Handled(self, value: bool) -> bool: ...
    @property
    def HoldingState(self) -> HoldingState: ...
    @property
    def PointerType(self) -> PointerType: ...
    @property
    def Position(self) -> Point: ...
    @property
    def Route(self) -> RoutingStrategies: ...
    @Route.setter
    def Route(self, value: RoutingStrategies) -> RoutingStrategies: ...
    @property
    def RoutedEvent(self) -> RoutedEvent: ...
    @RoutedEvent.setter
    def RoutedEvent(self, value: RoutedEvent) -> RoutedEvent: ...
    @property
    def Source(self) -> typing.Any: ...
    @Source.setter
    def Source(self, value: typing.Any) -> typing.Any: ...


class HoldingState(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Started : HoldingState # 0
    Completed : HoldingState # 1
    Cancelled : HoldingState # 2


class ICloseable(typing.Protocol):
    pass


class IDataObject(typing.Protocol):
    @abc.abstractmethod
    def Contains(self, dataFormat: str) -> bool: ...
    @abc.abstractmethod
    def Get(self, dataFormat: str) -> typing.Any: ...
    @abc.abstractmethod
    def GetDataFormats(self) -> IEnumerable_1[str]: ...


class IFocusManager(typing.Protocol):
    @abc.abstractmethod
    def ClearFocus(self) -> None: ...
    @abc.abstractmethod
    def GetFocusedElement(self) -> IInputElement: ...


class IFocusScope(typing.Protocol):
    pass


class IInputDevice(typing.Protocol):
    @abc.abstractmethod
    def ProcessRawEvent(self, ev: RawInputEventArgs) -> None: ...


class IInputElement(typing.Protocol):
    @property
    def Cursor(self) -> Cursor: ...
    @property
    def Focusable(self) -> bool: ...
    @property
    def IsEffectivelyEnabled(self) -> bool: ...
    @property
    def IsEffectivelyVisible(self) -> bool: ...
    @property
    def IsEnabled(self) -> bool: ...
    @property
    def IsFocused(self) -> bool: ...
    @property
    def IsHitTestVisible(self) -> bool: ...
    @property
    def IsKeyboardFocusWithin(self) -> bool: ...
    @property
    def IsPointerOver(self) -> bool: ...
    @property
    def KeyBindings(self) -> List_1[KeyBinding]: ...
    @abc.abstractmethod
    def AddHandler(self, routedEvent: RoutedEvent, handler: Delegate, routes: RoutingStrategies = ..., handledEventsToo: bool = ...) -> None: ...
    @abc.abstractmethod
    def Focus(self, method: NavigationMethod = ..., keyModifiers: KeyModifiers = ...) -> bool: ...
    @abc.abstractmethod
    def RaiseEvent(self, e: RoutedEventArgs) -> None: ...
    @abc.abstractmethod
    def RemoveHandler(self, routedEvent: RoutedEvent, handler: Delegate) -> None: ...


class IInputRoot(IInputElement, typing.Protocol):
    @property
    def FocusManager(self) -> IFocusManager: ...
    @property
    def KeyboardNavigationHandler(self) -> IKeyboardNavigationHandler: ...
    @property
    def PlatformSettings(self) -> IPlatformSettings: ...
    @property
    def PointerOverElement(self) -> IInputElement: ...
    @PointerOverElement.setter
    def PointerOverElement(self, value: IInputElement) -> IInputElement: ...
    @property
    def ShowAccessKeys(self) -> bool: ...
    @ShowAccessKeys.setter
    def ShowAccessKeys(self, value: bool) -> bool: ...


class IKeyboardNavigationHandler(typing.Protocol):
    @abc.abstractmethod
    def Move(self, element: IInputElement, direction: NavigationDirection, keyModifiers: KeyModifiers = ...) -> None: ...
    @abc.abstractmethod
    def SetOwner(self, owner: IInputRoot) -> None: ...


class InputElement(Interactive, IInputElement):
    def __init__(self) -> None: ...
    CursorProperty : StyledProperty_1[Cursor]
    DoubleTappedEvent : RoutedEvent_1[TappedEventArgs]
    FocusableProperty : StyledProperty_1[bool]
    GotFocusEvent : RoutedEvent_1[GotFocusEventArgs]
    HoldingEvent : RoutedEvent_1[HoldingRoutedEventArgs]
    IsEffectivelyEnabledProperty : DirectProperty_2[InputElement, bool]
    IsEnabledProperty : StyledProperty_1[bool]
    IsFocusedProperty : DirectProperty_2[InputElement, bool]
    IsHitTestVisibleProperty : StyledProperty_1[bool]
    IsKeyboardFocusWithinProperty : DirectProperty_2[InputElement, bool]
    IsPointerOverProperty : DirectProperty_2[InputElement, bool]
    IsTabStopProperty : StyledProperty_1[bool]
    KeyDownEvent : RoutedEvent_1[KeyEventArgs]
    KeyUpEvent : RoutedEvent_1[KeyEventArgs]
    LostFocusEvent : RoutedEvent_1[RoutedEventArgs]
    PointerCaptureLostEvent : RoutedEvent_1[PointerCaptureLostEventArgs]
    PointerEnteredEvent : RoutedEvent_1[PointerEventArgs]
    PointerExitedEvent : RoutedEvent_1[PointerEventArgs]
    PointerMovedEvent : RoutedEvent_1[PointerEventArgs]
    PointerPressedEvent : RoutedEvent_1[PointerPressedEventArgs]
    PointerReleasedEvent : RoutedEvent_1[PointerReleasedEventArgs]
    PointerWheelChangedEvent : RoutedEvent_1[PointerWheelEventArgs]
    TabIndexProperty : StyledProperty_1[int]
    TappedEvent : RoutedEvent_1[TappedEventArgs]
    TextInputEvent : RoutedEvent_1[TextInputEventArgs]
    TextInputMethodClientRequestedEvent : RoutedEvent_1[TextInputMethodClientRequestedEventArgs]
    @property
    def ActualThemeVariant(self) -> ThemeVariant: ...
    @property
    def Bounds(self) -> Rect: ...
    @Bounds.setter
    def Bounds(self, value: Rect) -> Rect: ...
    @property
    def Classes(self) -> Classes: ...
    @property
    def Clip(self) -> Geometry: ...
    @Clip.setter
    def Clip(self, value: Geometry) -> Geometry: ...
    @property
    def ClipToBounds(self) -> bool: ...
    @ClipToBounds.setter
    def ClipToBounds(self, value: bool) -> bool: ...
    @property
    def Cursor(self) -> Cursor: ...
    @Cursor.setter
    def Cursor(self, value: Cursor) -> Cursor: ...
    @property
    def DataContext(self) -> typing.Any: ...
    @DataContext.setter
    def DataContext(self, value: typing.Any) -> typing.Any: ...
    @property
    def DesiredSize(self) -> Size: ...
    @property
    def Effect(self) -> IEffect: ...
    @Effect.setter
    def Effect(self, value: IEffect) -> IEffect: ...
    @property
    def FlowDirection(self) -> FlowDirection: ...
    @FlowDirection.setter
    def FlowDirection(self, value: FlowDirection) -> FlowDirection: ...
    @property
    def Focusable(self) -> bool: ...
    @Focusable.setter
    def Focusable(self, value: bool) -> bool: ...
    @property
    def GestureRecognizers(self) -> GestureRecognizerCollection: ...
    @property
    def HasMirrorTransform(self) -> bool: ...
    @HasMirrorTransform.setter
    def HasMirrorTransform(self, value: bool) -> bool: ...
    @property
    def Height(self) -> float: ...
    @Height.setter
    def Height(self, value: float) -> float: ...
    @property
    def HorizontalAlignment(self) -> HorizontalAlignment: ...
    @HorizontalAlignment.setter
    def HorizontalAlignment(self, value: HorizontalAlignment) -> HorizontalAlignment: ...
    @property
    def IsArrangeValid(self) -> bool: ...
    @property
    def IsEffectivelyEnabled(self) -> bool: ...
    @IsEffectivelyEnabled.setter
    def IsEffectivelyEnabled(self, value: bool) -> bool: ...
    @property
    def IsEffectivelyVisible(self) -> bool: ...
    @property
    def IsEnabled(self) -> bool: ...
    @IsEnabled.setter
    def IsEnabled(self, value: bool) -> bool: ...
    @property
    def IsFocused(self) -> bool: ...
    @IsFocused.setter
    def IsFocused(self, value: bool) -> bool: ...
    @property
    def IsHitTestVisible(self) -> bool: ...
    @IsHitTestVisible.setter
    def IsHitTestVisible(self, value: bool) -> bool: ...
    @property
    def IsInitialized(self) -> bool: ...
    @property
    def IsKeyboardFocusWithin(self) -> bool: ...
    @IsKeyboardFocusWithin.setter
    def IsKeyboardFocusWithin(self, value: bool) -> bool: ...
    @property
    def IsMeasureValid(self) -> bool: ...
    @property
    def IsPointerOver(self) -> bool: ...
    @IsPointerOver.setter
    def IsPointerOver(self, value: bool) -> bool: ...
    @property
    def IsTabStop(self) -> bool: ...
    @IsTabStop.setter
    def IsTabStop(self, value: bool) -> bool: ...
    @property
    def IsVisible(self) -> bool: ...
    @IsVisible.setter
    def IsVisible(self, value: bool) -> bool: ...
    @property
    def KeyBindings(self) -> List_1[KeyBinding]: ...
    @property
    def Margin(self) -> Thickness: ...
    @Margin.setter
    def Margin(self, value: Thickness) -> Thickness: ...
    @property
    def MaxHeight(self) -> float: ...
    @MaxHeight.setter
    def MaxHeight(self, value: float) -> float: ...
    @property
    def MaxWidth(self) -> float: ...
    @MaxWidth.setter
    def MaxWidth(self, value: float) -> float: ...
    @property
    def MinHeight(self) -> float: ...
    @MinHeight.setter
    def MinHeight(self, value: float) -> float: ...
    @property
    def MinWidth(self) -> float: ...
    @MinWidth.setter
    def MinWidth(self, value: float) -> float: ...
    @property
    def Name(self) -> str: ...
    @Name.setter
    def Name(self, value: str) -> str: ...
    @property
    def Opacity(self) -> float: ...
    @Opacity.setter
    def Opacity(self, value: float) -> float: ...
    @property
    def OpacityMask(self) -> IBrush: ...
    @OpacityMask.setter
    def OpacityMask(self, value: IBrush) -> IBrush: ...
    @property
    def Parent(self) -> StyledElement: ...
    @property
    def RenderTransform(self) -> ITransform: ...
    @RenderTransform.setter
    def RenderTransform(self, value: ITransform) -> ITransform: ...
    @property
    def RenderTransformOrigin(self) -> RelativePoint: ...
    @RenderTransformOrigin.setter
    def RenderTransformOrigin(self, value: RelativePoint) -> RelativePoint: ...
    @property
    def Resources(self) -> IResourceDictionary: ...
    @Resources.setter
    def Resources(self, value: IResourceDictionary) -> IResourceDictionary: ...
    @property
    def StyleKey(self) -> typing.Type[typing.Any]: ...
    @property
    def Styles(self) -> Styles: ...
    @property
    def TabIndex(self) -> int: ...
    @TabIndex.setter
    def TabIndex(self, value: int) -> int: ...
    @property
    def TemplatedParent(self) -> AvaloniaObject: ...
    @TemplatedParent.setter
    def TemplatedParent(self, value: AvaloniaObject) -> AvaloniaObject: ...
    @property
    def Theme(self) -> ControlTheme: ...
    @Theme.setter
    def Theme(self, value: ControlTheme) -> ControlTheme: ...
    @property
    def Transitions(self) -> Transitions: ...
    @Transitions.setter
    def Transitions(self, value: Transitions) -> Transitions: ...
    @property
    def UseLayoutRounding(self) -> bool: ...
    @UseLayoutRounding.setter
    def UseLayoutRounding(self, value: bool) -> bool: ...
    @property
    def VerticalAlignment(self) -> VerticalAlignment: ...
    @VerticalAlignment.setter
    def VerticalAlignment(self, value: VerticalAlignment) -> VerticalAlignment: ...
    @property
    def Width(self) -> float: ...
    @Width.setter
    def Width(self, value: float) -> float: ...
    @property
    def ZIndex(self) -> int: ...
    @ZIndex.setter
    def ZIndex(self, value: int) -> int: ...
    def Focus(self, method: NavigationMethod = ..., keyModifiers: KeyModifiers = ...) -> bool: ...
    def __getitem__(self, property: AvaloniaProperty) -> typing.Any: ...
    def __setitem__(self, property: AvaloniaProperty, value: typing.Any) -> None: ...
    def __getitem__(self, binding: IndexerDescriptor) -> IBinding: ...
    def __setitem__(self, binding: IndexerDescriptor, value: IBinding) -> None: ...


class IPointer(typing.Protocol):
    @property
    def Captured(self) -> IInputElement: ...
    @property
    def Id(self) -> int: ...
    @property
    def IsPrimary(self) -> bool: ...
    @property
    def Type(self) -> PointerType: ...
    @abc.abstractmethod
    def Capture(self, control: IInputElement) -> None: ...


class Key(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : Key # 0
    Cancel : Key # 1
    Back : Key # 2
    Tab : Key # 3
    LineFeed : Key # 4
    Clear : Key # 5
    Return : Key # 6
    Enter : Key # 6
    Pause : Key # 7
    CapsLock : Key # 8
    Capital : Key # 8
    HangulMode : Key # 9
    KanaMode : Key # 9
    JunjaMode : Key # 10
    FinalMode : Key # 11
    KanjiMode : Key # 12
    HanjaMode : Key # 12
    Escape : Key # 13
    ImeConvert : Key # 14
    ImeNonConvert : Key # 15
    ImeAccept : Key # 16
    ImeModeChange : Key # 17
    Space : Key # 18
    PageUp : Key # 19
    Prior : Key # 19
    PageDown : Key # 20
    Next : Key # 20
    End : Key # 21
    Home : Key # 22
    Left : Key # 23
    Up : Key # 24
    Right : Key # 25
    Down : Key # 26
    Select : Key # 27
    Print : Key # 28
    Execute : Key # 29
    Snapshot : Key # 30
    PrintScreen : Key # 30
    Insert : Key # 31
    Delete : Key # 32
    Help : Key # 33
    D0 : Key # 34
    D1 : Key # 35
    D2 : Key # 36
    D3 : Key # 37
    D4 : Key # 38
    D5 : Key # 39
    D6 : Key # 40
    D7 : Key # 41
    D8 : Key # 42
    D9 : Key # 43
    A : Key # 44
    B : Key # 45
    C : Key # 46
    D : Key # 47
    E : Key # 48
    F : Key # 49
    G : Key # 50
    H : Key # 51
    I : Key # 52
    J : Key # 53
    K : Key # 54
    L : Key # 55
    M : Key # 56
    N : Key # 57
    O : Key # 58
    P : Key # 59
    Q : Key # 60
    R : Key # 61
    S : Key # 62
    T : Key # 63
    U : Key # 64
    V : Key # 65
    W : Key # 66
    X : Key # 67
    Y : Key # 68
    Z : Key # 69
    LWin : Key # 70
    RWin : Key # 71
    Apps : Key # 72
    Sleep : Key # 73
    NumPad0 : Key # 74
    NumPad1 : Key # 75
    NumPad2 : Key # 76
    NumPad3 : Key # 77
    NumPad4 : Key # 78
    NumPad5 : Key # 79
    NumPad6 : Key # 80
    NumPad7 : Key # 81
    NumPad8 : Key # 82
    NumPad9 : Key # 83
    Multiply : Key # 84
    Add : Key # 85
    Separator : Key # 86
    Subtract : Key # 87
    Decimal : Key # 88
    Divide : Key # 89
    F1 : Key # 90
    F2 : Key # 91
    F3 : Key # 92
    F4 : Key # 93
    F5 : Key # 94
    F6 : Key # 95
    F7 : Key # 96
    F8 : Key # 97
    F9 : Key # 98
    F10 : Key # 99
    F11 : Key # 100
    F12 : Key # 101
    F13 : Key # 102
    F14 : Key # 103
    F15 : Key # 104
    F16 : Key # 105
    F17 : Key # 106
    F18 : Key # 107
    F19 : Key # 108
    F20 : Key # 109
    F21 : Key # 110
    F22 : Key # 111
    F23 : Key # 112
    F24 : Key # 113
    NumLock : Key # 114
    Scroll : Key # 115
    LeftShift : Key # 116
    RightShift : Key # 117
    LeftCtrl : Key # 118
    RightCtrl : Key # 119
    LeftAlt : Key # 120
    RightAlt : Key # 121
    BrowserBack : Key # 122
    BrowserForward : Key # 123
    BrowserRefresh : Key # 124
    BrowserStop : Key # 125
    BrowserSearch : Key # 126
    BrowserFavorites : Key # 127
    BrowserHome : Key # 128
    VolumeMute : Key # 129
    VolumeDown : Key # 130
    VolumeUp : Key # 131
    MediaNextTrack : Key # 132
    MediaPreviousTrack : Key # 133
    MediaStop : Key # 134
    MediaPlayPause : Key # 135
    LaunchMail : Key # 136
    SelectMedia : Key # 137
    LaunchApplication1 : Key # 138
    LaunchApplication2 : Key # 139
    OemSemicolon : Key # 140
    Oem1 : Key # 140
    OemPlus : Key # 141
    OemComma : Key # 142
    OemMinus : Key # 143
    OemPeriod : Key # 144
    OemQuestion : Key # 145
    Oem2 : Key # 145
    OemTilde : Key # 146
    Oem3 : Key # 146
    AbntC1 : Key # 147
    AbntC2 : Key # 148
    OemOpenBrackets : Key # 149
    Oem4 : Key # 149
    OemPipe : Key # 150
    Oem5 : Key # 150
    OemCloseBrackets : Key # 151
    Oem6 : Key # 151
    OemQuotes : Key # 152
    Oem7 : Key # 152
    Oem8 : Key # 153
    OemBackslash : Key # 154
    Oem102 : Key # 154
    ImeProcessed : Key # 155
    System : Key # 156
    OemAttn : Key # 157
    DbeAlphanumeric : Key # 157
    OemFinish : Key # 158
    DbeKatakana : Key # 158
    DbeHiragana : Key # 159
    OemCopy : Key # 159
    DbeSbcsChar : Key # 160
    OemAuto : Key # 160
    DbeDbcsChar : Key # 161
    OemEnlw : Key # 161
    OemBackTab : Key # 162
    DbeRoman : Key # 162
    DbeNoRoman : Key # 163
    Attn : Key # 163
    CrSel : Key # 164
    DbeEnterWordRegisterMode : Key # 164
    ExSel : Key # 165
    DbeEnterImeConfigureMode : Key # 165
    EraseEof : Key # 166
    DbeFlushString : Key # 166
    Play : Key # 167
    DbeCodeInput : Key # 167
    DbeNoCodeInput : Key # 168
    Zoom : Key # 168
    NoName : Key # 169
    DbeDetermineString : Key # 169
    DbeEnterDialogConversionMode : Key # 170
    Pa1 : Key # 170
    OemClear : Key # 171
    DeadCharProcessed : Key # 172
    FnLeftArrow : Key # 10001
    FnRightArrow : Key # 10002
    FnUpArrow : Key # 10003
    FnDownArrow : Key # 10004
    MediaHome : Key # 100000
    MediaChannelList : Key # 100001
    MediaChannelRaise : Key # 100002
    MediaChannelLower : Key # 100003
    MediaRecord : Key # 100005
    MediaRed : Key # 100010
    MediaGreen : Key # 100011
    MediaYellow : Key # 100012
    MediaBlue : Key # 100013
    MediaMenu : Key # 100020
    MediaMore : Key # 100021
    MediaOption : Key # 100022
    MediaInfo : Key # 100023
    MediaSearch : Key # 100024
    MediaSubtitle : Key # 100025
    MediaTvGuide : Key # 100026
    MediaPreviousChannel : Key # 100027


class KeyBinding(AvaloniaObject):
    def __init__(self) -> None: ...
    CommandParameterProperty : StyledProperty_1[typing.Any]
    CommandProperty : StyledProperty_1[ICommand]
    GestureProperty : StyledProperty_1[KeyGesture]
    @property
    def Command(self) -> ICommand: ...
    @Command.setter
    def Command(self, value: ICommand) -> ICommand: ...
    @property
    def CommandParameter(self) -> typing.Any: ...
    @CommandParameter.setter
    def CommandParameter(self, value: typing.Any) -> typing.Any: ...
    @property
    def Gesture(self) -> KeyGesture: ...
    @Gesture.setter
    def Gesture(self, value: KeyGesture) -> KeyGesture: ...
    def TryHandle(self, args: KeyEventArgs) -> None: ...
    def __getitem__(self, property: AvaloniaProperty) -> typing.Any: ...
    def __setitem__(self, property: AvaloniaProperty, value: typing.Any) -> None: ...
    def __getitem__(self, binding: IndexerDescriptor) -> IBinding: ...
    def __setitem__(self, binding: IndexerDescriptor, value: IBinding) -> None: ...


class KeyDeviceType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Keyboard : KeyDeviceType # 0
    Gamepad : KeyDeviceType # 1
    Remote : KeyDeviceType # 2


class KeyEventArgs(RoutedEventArgs):
    def __init__(self) -> None: ...
    @property
    def Handled(self) -> bool: ...
    @Handled.setter
    def Handled(self, value: bool) -> bool: ...
    @property
    def Key(self) -> Key: ...
    @Key.setter
    def Key(self, value: Key) -> Key: ...
    @property
    def KeyDeviceType(self) -> KeyDeviceType: ...
    @KeyDeviceType.setter
    def KeyDeviceType(self, value: KeyDeviceType) -> KeyDeviceType: ...
    @property
    def KeyModifiers(self) -> KeyModifiers: ...
    @KeyModifiers.setter
    def KeyModifiers(self, value: KeyModifiers) -> KeyModifiers: ...
    @property
    def KeySymbol(self) -> str: ...
    @KeySymbol.setter
    def KeySymbol(self, value: str) -> str: ...
    @property
    def PhysicalKey(self) -> PhysicalKey: ...
    @PhysicalKey.setter
    def PhysicalKey(self, value: PhysicalKey) -> PhysicalKey: ...
    @property
    def Route(self) -> RoutingStrategies: ...
    @Route.setter
    def Route(self, value: RoutingStrategies) -> RoutingStrategies: ...
    @property
    def RoutedEvent(self) -> RoutedEvent: ...
    @RoutedEvent.setter
    def RoutedEvent(self, value: RoutedEvent) -> RoutedEvent: ...
    @property
    def Source(self) -> typing.Any: ...
    @Source.setter
    def Source(self, value: typing.Any) -> typing.Any: ...


class KeyGesture(IFormattable, IEquatable_1[KeyGesture]):
    def __init__(self, key: Key, modifiers: KeyModifiers = ...) -> None: ...
    @property
    def Key(self) -> Key: ...
    @property
    def KeyModifiers(self) -> KeyModifiers: ...
    def GetHashCode(self) -> int: ...
    def Matches(self, keyEvent: KeyEventArgs) -> bool: ...
    def __eq__(self, left: KeyGesture, right: KeyGesture) -> bool: ...
    def __ne__(self, left: KeyGesture, right: KeyGesture) -> bool: ...
    @staticmethod
    def Parse(gesture: str) -> KeyGesture: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        @typing.overload
        def __call__(self, other: KeyGesture) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...

    # Skipped ToString due to it being static, abstract and generic.

    ToString : ToString_MethodGroup
    class ToString_MethodGroup:
        @typing.overload
        def __call__(self) -> str:...
        @typing.overload
        def __call__(self, format: str, formatProvider: IFormatProvider) -> str:...



class KeyModifiers(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : KeyModifiers # 0
    Alt : KeyModifiers # 1
    Control : KeyModifiers # 2
    Shift : KeyModifiers # 4
    Meta : KeyModifiers # 8


class MouseButton(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : MouseButton # 0
    Left : MouseButton # 1
    Right : MouseButton # 2
    Middle : MouseButton # 3
    XButton1 : MouseButton # 4
    XButton2 : MouseButton # 5


class NavigationDirection(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Next : NavigationDirection # 0
    Previous : NavigationDirection # 1
    First : NavigationDirection # 2
    Last : NavigationDirection # 3
    Left : NavigationDirection # 4
    Right : NavigationDirection # 5
    Up : NavigationDirection # 6
    Down : NavigationDirection # 7
    PageUp : NavigationDirection # 8
    PageDown : NavigationDirection # 9


class NavigationMethod(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Unspecified : NavigationMethod # 0
    Tab : NavigationMethod # 1
    Directional : NavigationMethod # 2
    Pointer : NavigationMethod # 3


class PhysicalKey(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : PhysicalKey # 0
    Backquote : PhysicalKey # 1
    Backslash : PhysicalKey # 2
    BracketLeft : PhysicalKey # 3
    BracketRight : PhysicalKey # 4
    Comma : PhysicalKey # 5
    Digit0 : PhysicalKey # 6
    Digit1 : PhysicalKey # 7
    Digit2 : PhysicalKey # 8
    Digit3 : PhysicalKey # 9
    Digit4 : PhysicalKey # 10
    Digit5 : PhysicalKey # 11
    Digit6 : PhysicalKey # 12
    Digit7 : PhysicalKey # 13
    Digit8 : PhysicalKey # 14
    Digit9 : PhysicalKey # 15
    Equal : PhysicalKey # 16
    IntlBackslash : PhysicalKey # 17
    IntlRo : PhysicalKey # 18
    IntlYen : PhysicalKey # 19
    A : PhysicalKey # 20
    B : PhysicalKey # 21
    C : PhysicalKey # 22
    D : PhysicalKey # 23
    E : PhysicalKey # 24
    F : PhysicalKey # 25
    G : PhysicalKey # 26
    H : PhysicalKey # 27
    I : PhysicalKey # 28
    J : PhysicalKey # 29
    K : PhysicalKey # 30
    L : PhysicalKey # 31
    M : PhysicalKey # 32
    N : PhysicalKey # 33
    O : PhysicalKey # 34
    P : PhysicalKey # 35
    Q : PhysicalKey # 36
    R : PhysicalKey # 37
    S : PhysicalKey # 38
    T : PhysicalKey # 39
    U : PhysicalKey # 40
    V : PhysicalKey # 41
    W : PhysicalKey # 42
    X : PhysicalKey # 43
    Y : PhysicalKey # 44
    Z : PhysicalKey # 45
    Minus : PhysicalKey # 46
    Period : PhysicalKey # 47
    Quote : PhysicalKey # 48
    Semicolon : PhysicalKey # 49
    Slash : PhysicalKey # 50
    AltLeft : PhysicalKey # 51
    AltRight : PhysicalKey # 52
    Backspace : PhysicalKey # 53
    CapsLock : PhysicalKey # 54
    ContextMenu : PhysicalKey # 55
    ControlLeft : PhysicalKey # 56
    ControlRight : PhysicalKey # 57
    Enter : PhysicalKey # 58
    MetaLeft : PhysicalKey # 59
    MetaRight : PhysicalKey # 60
    ShiftLeft : PhysicalKey # 61
    ShiftRight : PhysicalKey # 62
    Space : PhysicalKey # 63
    Tab : PhysicalKey # 64
    Convert : PhysicalKey # 65
    KanaMode : PhysicalKey # 66
    Lang1 : PhysicalKey # 67
    Lang2 : PhysicalKey # 68
    Lang3 : PhysicalKey # 69
    Lang4 : PhysicalKey # 70
    Lang5 : PhysicalKey # 71
    NonConvert : PhysicalKey # 72
    Delete : PhysicalKey # 73
    End : PhysicalKey # 74
    Help : PhysicalKey # 75
    Home : PhysicalKey # 76
    Insert : PhysicalKey # 77
    PageDown : PhysicalKey # 78
    PageUp : PhysicalKey # 79
    ArrowDown : PhysicalKey # 80
    ArrowLeft : PhysicalKey # 81
    ArrowRight : PhysicalKey # 82
    ArrowUp : PhysicalKey # 83
    NumLock : PhysicalKey # 84
    NumPad0 : PhysicalKey # 85
    NumPad1 : PhysicalKey # 86
    NumPad2 : PhysicalKey # 87
    NumPad3 : PhysicalKey # 88
    NumPad4 : PhysicalKey # 89
    NumPad5 : PhysicalKey # 90
    NumPad6 : PhysicalKey # 91
    NumPad7 : PhysicalKey # 92
    NumPad8 : PhysicalKey # 93
    NumPad9 : PhysicalKey # 94
    NumPadAdd : PhysicalKey # 95
    NumPadClear : PhysicalKey # 96
    NumPadComma : PhysicalKey # 97
    NumPadDecimal : PhysicalKey # 98
    NumPadDivide : PhysicalKey # 99
    NumPadEnter : PhysicalKey # 100
    NumPadEqual : PhysicalKey # 101
    NumPadMultiply : PhysicalKey # 102
    NumPadParenLeft : PhysicalKey # 103
    NumPadParenRight : PhysicalKey # 104
    NumPadSubtract : PhysicalKey # 105
    Escape : PhysicalKey # 106
    F1 : PhysicalKey # 107
    F2 : PhysicalKey # 108
    F3 : PhysicalKey # 109
    F4 : PhysicalKey # 110
    F5 : PhysicalKey # 111
    F6 : PhysicalKey # 112
    F7 : PhysicalKey # 113
    F8 : PhysicalKey # 114
    F9 : PhysicalKey # 115
    F10 : PhysicalKey # 116
    F11 : PhysicalKey # 117
    F12 : PhysicalKey # 118
    F13 : PhysicalKey # 119
    F14 : PhysicalKey # 120
    F15 : PhysicalKey # 121
    F16 : PhysicalKey # 122
    F17 : PhysicalKey # 123
    F18 : PhysicalKey # 124
    F19 : PhysicalKey # 125
    F20 : PhysicalKey # 126
    F21 : PhysicalKey # 127
    F22 : PhysicalKey # 128
    F23 : PhysicalKey # 129
    F24 : PhysicalKey # 130
    PrintScreen : PhysicalKey # 131
    ScrollLock : PhysicalKey # 132
    Pause : PhysicalKey # 133
    BrowserBack : PhysicalKey # 134
    BrowserFavorites : PhysicalKey # 135
    BrowserForward : PhysicalKey # 136
    BrowserHome : PhysicalKey # 137
    BrowserRefresh : PhysicalKey # 138
    BrowserSearch : PhysicalKey # 139
    BrowserStop : PhysicalKey # 140
    Eject : PhysicalKey # 141
    LaunchApp1 : PhysicalKey # 142
    LaunchApp2 : PhysicalKey # 143
    LaunchMail : PhysicalKey # 144
    MediaPlayPause : PhysicalKey # 145
    MediaSelect : PhysicalKey # 146
    MediaStop : PhysicalKey # 147
    MediaTrackNext : PhysicalKey # 148
    MediaTrackPrevious : PhysicalKey # 149
    Power : PhysicalKey # 150
    Sleep : PhysicalKey # 151
    AudioVolumeDown : PhysicalKey # 152
    AudioVolumeMute : PhysicalKey # 153
    AudioVolumeUp : PhysicalKey # 154
    WakeUp : PhysicalKey # 155
    Again : PhysicalKey # 156
    Copy : PhysicalKey # 157
    Cut : PhysicalKey # 158
    Find : PhysicalKey # 159
    Open : PhysicalKey # 160
    Paste : PhysicalKey # 161
    Props : PhysicalKey # 162
    Select : PhysicalKey # 163
    Undo : PhysicalKey # 164


class PointerCaptureLostEventArgs(RoutedEventArgs):
    def __init__(self, source: typing.Any, pointer: IPointer) -> None: ...
    @property
    def Handled(self) -> bool: ...
    @Handled.setter
    def Handled(self, value: bool) -> bool: ...
    @property
    def Pointer(self) -> IPointer: ...
    @property
    def Route(self) -> RoutingStrategies: ...
    @Route.setter
    def Route(self, value: RoutingStrategies) -> RoutingStrategies: ...
    @property
    def RoutedEvent(self) -> RoutedEvent: ...
    @RoutedEvent.setter
    def RoutedEvent(self, value: RoutedEvent) -> RoutedEvent: ...
    @property
    def Source(self) -> typing.Any: ...
    @Source.setter
    def Source(self, value: typing.Any) -> typing.Any: ...


class PointerEventArgs(RoutedEventArgs):
    def __init__(self, routedEvent: RoutedEvent, source: typing.Any, pointer: IPointer, rootVisual: Visual, rootVisualPosition: Point, timestamp: int, properties: PointerPointProperties, modifiers: KeyModifiers) -> None: ...
    @property
    def Handled(self) -> bool: ...
    @Handled.setter
    def Handled(self, value: bool) -> bool: ...
    @property
    def KeyModifiers(self) -> KeyModifiers: ...
    @property
    def Pointer(self) -> IPointer: ...
    @property
    def Route(self) -> RoutingStrategies: ...
    @Route.setter
    def Route(self, value: RoutingStrategies) -> RoutingStrategies: ...
    @property
    def RoutedEvent(self) -> RoutedEvent: ...
    @RoutedEvent.setter
    def RoutedEvent(self, value: RoutedEvent) -> RoutedEvent: ...
    @property
    def Source(self) -> typing.Any: ...
    @Source.setter
    def Source(self, value: typing.Any) -> typing.Any: ...
    @property
    def Timestamp(self) -> int: ...
    def GetCurrentPoint(self, relativeTo: Visual) -> PointerPoint: ...
    def GetIntermediatePoints(self, relativeTo: Visual) -> IReadOnlyList_1[PointerPoint]: ...
    def GetPosition(self, relativeTo: Visual) -> Point: ...
    def PreventGestureRecognition(self) -> None: ...


class PointerPoint(IEquatable_1[PointerPoint]):
    def __init__(self, pointer: IPointer, position: Point, properties: PointerPointProperties) -> None: ...
    @property
    def Pointer(self) -> IPointer: ...
    @property
    def Position(self) -> Point: ...
    @property
    def Properties(self) -> PointerPointProperties: ...
    def GetHashCode(self) -> int: ...
    def __eq__(self, left: PointerPoint, right: PointerPoint) -> bool: ...
    def __ne__(self, left: PointerPoint, right: PointerPoint) -> bool: ...
    def ToString(self) -> str: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        @typing.overload
        def __call__(self, other: PointerPoint) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...



class PointerPointProperties(IEquatable_1[PointerPointProperties]):
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, modifiers: RawInputModifiers, kind: PointerUpdateKind) -> None: ...
    @typing.overload
    def __init__(self, modifiers: RawInputModifiers, kind: PointerUpdateKind, twist: float, pressure: float, xTilt: float, yTilt: float) -> None: ...
    @property
    def IsBarrelButtonPressed(self) -> bool: ...
    @property
    def IsEraser(self) -> bool: ...
    @property
    def IsInverted(self) -> bool: ...
    @property
    def IsLeftButtonPressed(self) -> bool: ...
    @property
    def IsMiddleButtonPressed(self) -> bool: ...
    @property
    def IsRightButtonPressed(self) -> bool: ...
    @property
    def IsXButton1Pressed(self) -> bool: ...
    @property
    def IsXButton2Pressed(self) -> bool: ...
    # Skipped property None since it is a reserved python word. Use reflection to access.
    @property
    def PointerUpdateKind(self) -> PointerUpdateKind: ...
    @property
    def Pressure(self) -> float: ...
    @property
    def Twist(self) -> float: ...
    @property
    def XTilt(self) -> float: ...
    @property
    def YTilt(self) -> float: ...
    def GetHashCode(self) -> int: ...
    def __eq__(self, left: PointerPointProperties, right: PointerPointProperties) -> bool: ...
    def __ne__(self, left: PointerPointProperties, right: PointerPointProperties) -> bool: ...
    def ToString(self) -> str: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        @typing.overload
        def __call__(self, other: PointerPointProperties) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...



class PointerPressedEventArgs(PointerEventArgs):
    def __init__(self, source: typing.Any, pointer: IPointer, rootVisual: Visual, rootVisualPosition: Point, timestamp: int, properties: PointerPointProperties, modifiers: KeyModifiers, clickCount: int = ...) -> None: ...
    @property
    def ClickCount(self) -> int: ...
    @property
    def Handled(self) -> bool: ...
    @Handled.setter
    def Handled(self, value: bool) -> bool: ...
    @property
    def KeyModifiers(self) -> KeyModifiers: ...
    @property
    def Pointer(self) -> IPointer: ...
    @property
    def Route(self) -> RoutingStrategies: ...
    @Route.setter
    def Route(self, value: RoutingStrategies) -> RoutingStrategies: ...
    @property
    def RoutedEvent(self) -> RoutedEvent: ...
    @RoutedEvent.setter
    def RoutedEvent(self, value: RoutedEvent) -> RoutedEvent: ...
    @property
    def Source(self) -> typing.Any: ...
    @Source.setter
    def Source(self, value: typing.Any) -> typing.Any: ...
    @property
    def Timestamp(self) -> int: ...


class PointerReleasedEventArgs(PointerEventArgs):
    def __init__(self, source: typing.Any, pointer: IPointer, rootVisual: Visual, rootVisualPosition: Point, timestamp: int, properties: PointerPointProperties, modifiers: KeyModifiers, initialPressMouseButton: MouseButton) -> None: ...
    @property
    def Handled(self) -> bool: ...
    @Handled.setter
    def Handled(self, value: bool) -> bool: ...
    @property
    def InitialPressMouseButton(self) -> MouseButton: ...
    @property
    def KeyModifiers(self) -> KeyModifiers: ...
    @property
    def Pointer(self) -> IPointer: ...
    @property
    def Route(self) -> RoutingStrategies: ...
    @Route.setter
    def Route(self, value: RoutingStrategies) -> RoutingStrategies: ...
    @property
    def RoutedEvent(self) -> RoutedEvent: ...
    @RoutedEvent.setter
    def RoutedEvent(self, value: RoutedEvent) -> RoutedEvent: ...
    @property
    def Source(self) -> typing.Any: ...
    @Source.setter
    def Source(self, value: typing.Any) -> typing.Any: ...
    @property
    def Timestamp(self) -> int: ...


class PointerType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Mouse : PointerType # 0
    Touch : PointerType # 1
    Pen : PointerType # 2


class PointerUpdateKind(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    LeftButtonPressed : PointerUpdateKind # 0
    MiddleButtonPressed : PointerUpdateKind # 1
    RightButtonPressed : PointerUpdateKind # 2
    XButton1Pressed : PointerUpdateKind # 3
    XButton2Pressed : PointerUpdateKind # 4
    LeftButtonReleased : PointerUpdateKind # 5
    MiddleButtonReleased : PointerUpdateKind # 6
    RightButtonReleased : PointerUpdateKind # 7
    XButton1Released : PointerUpdateKind # 8
    XButton2Released : PointerUpdateKind # 9
    Other : PointerUpdateKind # 10


class PointerWheelEventArgs(PointerEventArgs):
    def __init__(self, source: typing.Any, pointer: IPointer, rootVisual: Visual, rootVisualPosition: Point, timestamp: int, properties: PointerPointProperties, modifiers: KeyModifiers, delta: Vector) -> None: ...
    @property
    def Delta(self) -> Vector: ...
    @property
    def Handled(self) -> bool: ...
    @Handled.setter
    def Handled(self, value: bool) -> bool: ...
    @property
    def KeyModifiers(self) -> KeyModifiers: ...
    @property
    def Pointer(self) -> IPointer: ...
    @property
    def Route(self) -> RoutingStrategies: ...
    @Route.setter
    def Route(self, value: RoutingStrategies) -> RoutingStrategies: ...
    @property
    def RoutedEvent(self) -> RoutedEvent: ...
    @RoutedEvent.setter
    def RoutedEvent(self, value: RoutedEvent) -> RoutedEvent: ...
    @property
    def Source(self) -> typing.Any: ...
    @Source.setter
    def Source(self, value: typing.Any) -> typing.Any: ...
    @property
    def Timestamp(self) -> int: ...


class RawInputModifiers(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    None_ : RawInputModifiers # 0
    Alt : RawInputModifiers # 1
    Control : RawInputModifiers # 2
    Shift : RawInputModifiers # 4
    Meta : RawInputModifiers # 8
    KeyboardMask : RawInputModifiers # 15
    LeftMouseButton : RawInputModifiers # 16
    RightMouseButton : RawInputModifiers # 32
    MiddleMouseButton : RawInputModifiers # 64
    XButton1MouseButton : RawInputModifiers # 128
    XButton2MouseButton : RawInputModifiers # 256
    PenInverted : RawInputModifiers # 512
    PenEraser : RawInputModifiers # 1024
    PenBarrelButton : RawInputModifiers # 2048


class StandardCursorType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    Arrow : StandardCursorType # 0
    Ibeam : StandardCursorType # 1
    Wait : StandardCursorType # 2
    Cross : StandardCursorType # 3
    UpArrow : StandardCursorType # 4
    SizeWestEast : StandardCursorType # 5
    SizeNorthSouth : StandardCursorType # 6
    SizeAll : StandardCursorType # 7
    No : StandardCursorType # 8
    Hand : StandardCursorType # 9
    AppStarting : StandardCursorType # 10
    Help : StandardCursorType # 11
    TopSide : StandardCursorType # 12
    BottomSide : StandardCursorType # 13
    LeftSide : StandardCursorType # 14
    RightSide : StandardCursorType # 15
    TopLeftCorner : StandardCursorType # 16
    TopRightCorner : StandardCursorType # 17
    BottomLeftCorner : StandardCursorType # 18
    BottomRightCorner : StandardCursorType # 19
    DragMove : StandardCursorType # 20
    DragCopy : StandardCursorType # 21
    DragLink : StandardCursorType # 22
    None_ : StandardCursorType # 23


class TappedEventArgs(RoutedEventArgs):
    def __init__(self, routedEvent: RoutedEvent, lastPointerEventArgs: PointerEventArgs) -> None: ...
    @property
    def Handled(self) -> bool: ...
    @Handled.setter
    def Handled(self, value: bool) -> bool: ...
    @property
    def KeyModifiers(self) -> KeyModifiers: ...
    @property
    def Pointer(self) -> IPointer: ...
    @property
    def Route(self) -> RoutingStrategies: ...
    @Route.setter
    def Route(self, value: RoutingStrategies) -> RoutingStrategies: ...
    @property
    def RoutedEvent(self) -> RoutedEvent: ...
    @RoutedEvent.setter
    def RoutedEvent(self, value: RoutedEvent) -> RoutedEvent: ...
    @property
    def Source(self) -> typing.Any: ...
    @Source.setter
    def Source(self, value: typing.Any) -> typing.Any: ...
    @property
    def Timestamp(self) -> int: ...
    def GetPosition(self, relativeTo: Visual) -> Point: ...


class TextInputEventArgs(RoutedEventArgs):
    def __init__(self) -> None: ...
    @property
    def Handled(self) -> bool: ...
    @Handled.setter
    def Handled(self, value: bool) -> bool: ...
    @property
    def Route(self) -> RoutingStrategies: ...
    @Route.setter
    def Route(self, value: RoutingStrategies) -> RoutingStrategies: ...
    @property
    def RoutedEvent(self) -> RoutedEvent: ...
    @RoutedEvent.setter
    def RoutedEvent(self, value: RoutedEvent) -> RoutedEvent: ...
    @property
    def Source(self) -> typing.Any: ...
    @Source.setter
    def Source(self, value: typing.Any) -> typing.Any: ...
    @property
    def Text(self) -> str: ...
    @Text.setter
    def Text(self, value: str) -> str: ...

