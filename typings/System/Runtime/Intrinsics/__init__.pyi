import typing, clr, abc
from System.Numerics import Plane, Quaternion, Vector2, Vector3, Vector4, Vector_1
from System import UIntPtr, Array_1, Span_1, ReadOnlySpan_1, MidpointRounding, ValueTuple_2

class Vector128_GenericClasses(abc.ABCMeta):
    Generic_Vector128_GenericClasses_Vector128_1_T = typing.TypeVar('Generic_Vector128_GenericClasses_Vector128_1_T')
    def __getitem__(self, types : typing.Type[Generic_Vector128_GenericClasses_Vector128_1_T]) -> typing.Type[Vector128_1[Generic_Vector128_GenericClasses_Vector128_1_T]]: ...

class Vector128(Vector128_0, metaclass =Vector128_GenericClasses): ...

class Vector128_0(abc.ABC):
    @classmethod
    @property
    def IsHardwareAccelerated(cls) -> bool: ...
    @staticmethod
    def AsPlane(value: Vector128_1[float]) -> Plane: ...
    @staticmethod
    def AsQuaternion(value: Vector128_1[float]) -> Quaternion: ...
    @staticmethod
    def AsVector2(value: Vector128_1[float]) -> Vector2: ...
    @staticmethod
    def AsVector3(value: Vector128_1[float]) -> Vector3: ...
    @staticmethod
    def AsVector4(value: Vector128_1[float]) -> Vector4: ...
    @staticmethod
    def ConvertToInt32(vector: Vector128_1[float]) -> Vector128_1[int]: ...
    @staticmethod
    def ConvertToInt32Native(vector: Vector128_1[float]) -> Vector128_1[int]: ...
    @staticmethod
    def ConvertToInt64(vector: Vector128_1[float]) -> Vector128_1[int]: ...
    @staticmethod
    def ConvertToInt64Native(vector: Vector128_1[float]) -> Vector128_1[int]: ...
    @staticmethod
    def ConvertToUInt32(vector: Vector128_1[float]) -> Vector128_1[int]: ...
    @staticmethod
    def ConvertToUInt32Native(vector: Vector128_1[float]) -> Vector128_1[int]: ...
    @staticmethod
    def ConvertToUInt64(vector: Vector128_1[float]) -> Vector128_1[int]: ...
    @staticmethod
    def ConvertToUInt64Native(vector: Vector128_1[float]) -> Vector128_1[int]: ...
    # Skipped Abs due to it being static, abstract and generic.

    Abs : Abs_MethodGroup
    class Abs_MethodGroup:
        def __getitem__(self, t:typing.Type[Abs_1_T1]) -> Abs_1[Abs_1_T1]: ...

        Abs_1_T1 = typing.TypeVar('Abs_1_T1')
        class Abs_1(typing.Generic[Abs_1_T1]):
            Abs_1_T = Vector128_0.Abs_MethodGroup.Abs_1_T1
            def __call__(self, vector: Vector128_1[Abs_1_T]) -> Vector128_1[Abs_1_T]:...


    # Skipped Add due to it being static, abstract and generic.

    Add : Add_MethodGroup
    class Add_MethodGroup:
        def __getitem__(self, t:typing.Type[Add_1_T1]) -> Add_1[Add_1_T1]: ...

        Add_1_T1 = typing.TypeVar('Add_1_T1')
        class Add_1(typing.Generic[Add_1_T1]):
            Add_1_T = Vector128_0.Add_MethodGroup.Add_1_T1
            def __call__(self, left: Vector128_1[Add_1_T], right: Vector128_1[Add_1_T]) -> Vector128_1[Add_1_T]:...


    # Skipped AddSaturate due to it being static, abstract and generic.

    AddSaturate : AddSaturate_MethodGroup
    class AddSaturate_MethodGroup:
        def __getitem__(self, t:typing.Type[AddSaturate_1_T1]) -> AddSaturate_1[AddSaturate_1_T1]: ...

        AddSaturate_1_T1 = typing.TypeVar('AddSaturate_1_T1')
        class AddSaturate_1(typing.Generic[AddSaturate_1_T1]):
            AddSaturate_1_T = Vector128_0.AddSaturate_MethodGroup.AddSaturate_1_T1
            def __call__(self, left: Vector128_1[AddSaturate_1_T], right: Vector128_1[AddSaturate_1_T]) -> Vector128_1[AddSaturate_1_T]:...


    # Skipped All due to it being static, abstract and generic.

    All : All_MethodGroup
    class All_MethodGroup:
        def __getitem__(self, t:typing.Type[All_1_T1]) -> All_1[All_1_T1]: ...

        All_1_T1 = typing.TypeVar('All_1_T1')
        class All_1(typing.Generic[All_1_T1]):
            All_1_T = Vector128_0.All_MethodGroup.All_1_T1
            def __call__(self, vector: Vector128_1[All_1_T], value: All_1_T) -> bool:...


    # Skipped AllWhereAllBitsSet due to it being static, abstract and generic.

    AllWhereAllBitsSet : AllWhereAllBitsSet_MethodGroup
    class AllWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[AllWhereAllBitsSet_1_T1]) -> AllWhereAllBitsSet_1[AllWhereAllBitsSet_1_T1]: ...

        AllWhereAllBitsSet_1_T1 = typing.TypeVar('AllWhereAllBitsSet_1_T1')
        class AllWhereAllBitsSet_1(typing.Generic[AllWhereAllBitsSet_1_T1]):
            AllWhereAllBitsSet_1_T = Vector128_0.AllWhereAllBitsSet_MethodGroup.AllWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector128_1[AllWhereAllBitsSet_1_T]) -> bool:...


    # Skipped AndNot due to it being static, abstract and generic.

    AndNot : AndNot_MethodGroup
    class AndNot_MethodGroup:
        def __getitem__(self, t:typing.Type[AndNot_1_T1]) -> AndNot_1[AndNot_1_T1]: ...

        AndNot_1_T1 = typing.TypeVar('AndNot_1_T1')
        class AndNot_1(typing.Generic[AndNot_1_T1]):
            AndNot_1_T = Vector128_0.AndNot_MethodGroup.AndNot_1_T1
            def __call__(self, left: Vector128_1[AndNot_1_T], right: Vector128_1[AndNot_1_T]) -> Vector128_1[AndNot_1_T]:...


    # Skipped Any due to it being static, abstract and generic.

    Any : Any_MethodGroup
    class Any_MethodGroup:
        def __getitem__(self, t:typing.Type[Any_1_T1]) -> Any_1[Any_1_T1]: ...

        Any_1_T1 = typing.TypeVar('Any_1_T1')
        class Any_1(typing.Generic[Any_1_T1]):
            Any_1_T = Vector128_0.Any_MethodGroup.Any_1_T1
            def __call__(self, vector: Vector128_1[Any_1_T], value: Any_1_T) -> bool:...


    # Skipped AnyWhereAllBitsSet due to it being static, abstract and generic.

    AnyWhereAllBitsSet : AnyWhereAllBitsSet_MethodGroup
    class AnyWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[AnyWhereAllBitsSet_1_T1]) -> AnyWhereAllBitsSet_1[AnyWhereAllBitsSet_1_T1]: ...

        AnyWhereAllBitsSet_1_T1 = typing.TypeVar('AnyWhereAllBitsSet_1_T1')
        class AnyWhereAllBitsSet_1(typing.Generic[AnyWhereAllBitsSet_1_T1]):
            AnyWhereAllBitsSet_1_T = Vector128_0.AnyWhereAllBitsSet_MethodGroup.AnyWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector128_1[AnyWhereAllBitsSet_1_T]) -> bool:...


    # Skipped As due to it being static, abstract and generic.

    As : As_MethodGroup
    class As_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[As_2_T1], typing.Type[As_2_T2]]) -> As_2[As_2_T1, As_2_T2]: ...

        As_2_T1 = typing.TypeVar('As_2_T1')
        As_2_T2 = typing.TypeVar('As_2_T2')
        class As_2(typing.Generic[As_2_T1, As_2_T2]):
            As_2_TFrom = Vector128_0.As_MethodGroup.As_2_T1
            As_2_TTo = Vector128_0.As_MethodGroup.As_2_T2
            def __call__(self, vector: Vector128_1[As_2_TFrom]) -> Vector128_1[As_2_TTo]:...


    # Skipped AsByte due to it being static, abstract and generic.

    AsByte : AsByte_MethodGroup
    class AsByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsByte_1_T1]) -> AsByte_1[AsByte_1_T1]: ...

        AsByte_1_T1 = typing.TypeVar('AsByte_1_T1')
        class AsByte_1(typing.Generic[AsByte_1_T1]):
            AsByte_1_T = Vector128_0.AsByte_MethodGroup.AsByte_1_T1
            def __call__(self, vector: Vector128_1[AsByte_1_T]) -> Vector128_1[int]:...


    # Skipped AsDouble due to it being static, abstract and generic.

    AsDouble : AsDouble_MethodGroup
    class AsDouble_MethodGroup:
        def __getitem__(self, t:typing.Type[AsDouble_1_T1]) -> AsDouble_1[AsDouble_1_T1]: ...

        AsDouble_1_T1 = typing.TypeVar('AsDouble_1_T1')
        class AsDouble_1(typing.Generic[AsDouble_1_T1]):
            AsDouble_1_T = Vector128_0.AsDouble_MethodGroup.AsDouble_1_T1
            def __call__(self, vector: Vector128_1[AsDouble_1_T]) -> Vector128_1[float]:...


    # Skipped AsInt16 due to it being static, abstract and generic.

    AsInt16 : AsInt16_MethodGroup
    class AsInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt16_1_T1]) -> AsInt16_1[AsInt16_1_T1]: ...

        AsInt16_1_T1 = typing.TypeVar('AsInt16_1_T1')
        class AsInt16_1(typing.Generic[AsInt16_1_T1]):
            AsInt16_1_T = Vector128_0.AsInt16_MethodGroup.AsInt16_1_T1
            def __call__(self, vector: Vector128_1[AsInt16_1_T]) -> Vector128_1[int]:...


    # Skipped AsInt32 due to it being static, abstract and generic.

    AsInt32 : AsInt32_MethodGroup
    class AsInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt32_1_T1]) -> AsInt32_1[AsInt32_1_T1]: ...

        AsInt32_1_T1 = typing.TypeVar('AsInt32_1_T1')
        class AsInt32_1(typing.Generic[AsInt32_1_T1]):
            AsInt32_1_T = Vector128_0.AsInt32_MethodGroup.AsInt32_1_T1
            def __call__(self, vector: Vector128_1[AsInt32_1_T]) -> Vector128_1[int]:...


    # Skipped AsInt64 due to it being static, abstract and generic.

    AsInt64 : AsInt64_MethodGroup
    class AsInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt64_1_T1]) -> AsInt64_1[AsInt64_1_T1]: ...

        AsInt64_1_T1 = typing.TypeVar('AsInt64_1_T1')
        class AsInt64_1(typing.Generic[AsInt64_1_T1]):
            AsInt64_1_T = Vector128_0.AsInt64_MethodGroup.AsInt64_1_T1
            def __call__(self, vector: Vector128_1[AsInt64_1_T]) -> Vector128_1[int]:...


    # Skipped AsNInt due to it being static, abstract and generic.

    AsNInt : AsNInt_MethodGroup
    class AsNInt_MethodGroup:
        def __getitem__(self, t:typing.Type[AsNInt_1_T1]) -> AsNInt_1[AsNInt_1_T1]: ...

        AsNInt_1_T1 = typing.TypeVar('AsNInt_1_T1')
        class AsNInt_1(typing.Generic[AsNInt_1_T1]):
            AsNInt_1_T = Vector128_0.AsNInt_MethodGroup.AsNInt_1_T1
            def __call__(self, vector: Vector128_1[AsNInt_1_T]) -> Vector128_1[int]:...


    # Skipped AsNUInt due to it being static, abstract and generic.

    AsNUInt : AsNUInt_MethodGroup
    class AsNUInt_MethodGroup:
        def __getitem__(self, t:typing.Type[AsNUInt_1_T1]) -> AsNUInt_1[AsNUInt_1_T1]: ...

        AsNUInt_1_T1 = typing.TypeVar('AsNUInt_1_T1')
        class AsNUInt_1(typing.Generic[AsNUInt_1_T1]):
            AsNUInt_1_T = Vector128_0.AsNUInt_MethodGroup.AsNUInt_1_T1
            def __call__(self, vector: Vector128_1[AsNUInt_1_T]) -> Vector128_1[UIntPtr]:...


    # Skipped AsSByte due to it being static, abstract and generic.

    AsSByte : AsSByte_MethodGroup
    class AsSByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsSByte_1_T1]) -> AsSByte_1[AsSByte_1_T1]: ...

        AsSByte_1_T1 = typing.TypeVar('AsSByte_1_T1')
        class AsSByte_1(typing.Generic[AsSByte_1_T1]):
            AsSByte_1_T = Vector128_0.AsSByte_MethodGroup.AsSByte_1_T1
            def __call__(self, vector: Vector128_1[AsSByte_1_T]) -> Vector128_1[int]:...


    # Skipped AsSingle due to it being static, abstract and generic.

    AsSingle : AsSingle_MethodGroup
    class AsSingle_MethodGroup:
        def __getitem__(self, t:typing.Type[AsSingle_1_T1]) -> AsSingle_1[AsSingle_1_T1]: ...

        AsSingle_1_T1 = typing.TypeVar('AsSingle_1_T1')
        class AsSingle_1(typing.Generic[AsSingle_1_T1]):
            AsSingle_1_T = Vector128_0.AsSingle_MethodGroup.AsSingle_1_T1
            def __call__(self, vector: Vector128_1[AsSingle_1_T]) -> Vector128_1[float]:...


    # Skipped AsUInt16 due to it being static, abstract and generic.

    AsUInt16 : AsUInt16_MethodGroup
    class AsUInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt16_1_T1]) -> AsUInt16_1[AsUInt16_1_T1]: ...

        AsUInt16_1_T1 = typing.TypeVar('AsUInt16_1_T1')
        class AsUInt16_1(typing.Generic[AsUInt16_1_T1]):
            AsUInt16_1_T = Vector128_0.AsUInt16_MethodGroup.AsUInt16_1_T1
            def __call__(self, vector: Vector128_1[AsUInt16_1_T]) -> Vector128_1[int]:...


    # Skipped AsUInt32 due to it being static, abstract and generic.

    AsUInt32 : AsUInt32_MethodGroup
    class AsUInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt32_1_T1]) -> AsUInt32_1[AsUInt32_1_T1]: ...

        AsUInt32_1_T1 = typing.TypeVar('AsUInt32_1_T1')
        class AsUInt32_1(typing.Generic[AsUInt32_1_T1]):
            AsUInt32_1_T = Vector128_0.AsUInt32_MethodGroup.AsUInt32_1_T1
            def __call__(self, vector: Vector128_1[AsUInt32_1_T]) -> Vector128_1[int]:...


    # Skipped AsUInt64 due to it being static, abstract and generic.

    AsUInt64 : AsUInt64_MethodGroup
    class AsUInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt64_1_T1]) -> AsUInt64_1[AsUInt64_1_T1]: ...

        AsUInt64_1_T1 = typing.TypeVar('AsUInt64_1_T1')
        class AsUInt64_1(typing.Generic[AsUInt64_1_T1]):
            AsUInt64_1_T = Vector128_0.AsUInt64_MethodGroup.AsUInt64_1_T1
            def __call__(self, vector: Vector128_1[AsUInt64_1_T]) -> Vector128_1[int]:...


    # Skipped AsVector due to it being static, abstract and generic.

    AsVector : AsVector_MethodGroup
    class AsVector_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVector_1_T1]) -> AsVector_1[AsVector_1_T1]: ...

        AsVector_1_T1 = typing.TypeVar('AsVector_1_T1')
        class AsVector_1(typing.Generic[AsVector_1_T1]):
            AsVector_1_T = Vector128_0.AsVector_MethodGroup.AsVector_1_T1
            def __call__(self, value: Vector128_1[AsVector_1_T]) -> Vector_1[AsVector_1_T]:...


    # Skipped AsVector128 due to it being static, abstract and generic.

    AsVector128 : AsVector128_MethodGroup
    class AsVector128_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVector128_1_T1]) -> AsVector128_1[AsVector128_1_T1]: ...

        AsVector128_1_T1 = typing.TypeVar('AsVector128_1_T1')
        class AsVector128_1(typing.Generic[AsVector128_1_T1]):
            AsVector128_1_T = Vector128_0.AsVector128_MethodGroup.AsVector128_1_T1
            def __call__(self, value: Vector_1[AsVector128_1_T]) -> Vector128_1[AsVector128_1_T]:...

        @typing.overload
        def __call__(self, value: Plane) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, value: Quaternion) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, value: Vector2) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, value: Vector3) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, value: Vector4) -> Vector128_1[float]:...

    # Skipped AsVector128Unsafe due to it being static, abstract and generic.

    AsVector128Unsafe : AsVector128Unsafe_MethodGroup
    class AsVector128Unsafe_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector2) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, value: Vector3) -> Vector128_1[float]:...

    # Skipped BitwiseAnd due to it being static, abstract and generic.

    BitwiseAnd : BitwiseAnd_MethodGroup
    class BitwiseAnd_MethodGroup:
        def __getitem__(self, t:typing.Type[BitwiseAnd_1_T1]) -> BitwiseAnd_1[BitwiseAnd_1_T1]: ...

        BitwiseAnd_1_T1 = typing.TypeVar('BitwiseAnd_1_T1')
        class BitwiseAnd_1(typing.Generic[BitwiseAnd_1_T1]):
            BitwiseAnd_1_T = Vector128_0.BitwiseAnd_MethodGroup.BitwiseAnd_1_T1
            def __call__(self, left: Vector128_1[BitwiseAnd_1_T], right: Vector128_1[BitwiseAnd_1_T]) -> Vector128_1[BitwiseAnd_1_T]:...


    # Skipped BitwiseOr due to it being static, abstract and generic.

    BitwiseOr : BitwiseOr_MethodGroup
    class BitwiseOr_MethodGroup:
        def __getitem__(self, t:typing.Type[BitwiseOr_1_T1]) -> BitwiseOr_1[BitwiseOr_1_T1]: ...

        BitwiseOr_1_T1 = typing.TypeVar('BitwiseOr_1_T1')
        class BitwiseOr_1(typing.Generic[BitwiseOr_1_T1]):
            BitwiseOr_1_T = Vector128_0.BitwiseOr_MethodGroup.BitwiseOr_1_T1
            def __call__(self, left: Vector128_1[BitwiseOr_1_T], right: Vector128_1[BitwiseOr_1_T]) -> Vector128_1[BitwiseOr_1_T]:...


    # Skipped Ceiling due to it being static, abstract and generic.

    Ceiling : Ceiling_MethodGroup
    class Ceiling_MethodGroup:
        def __call__(self, vector: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Ceiling(vector : Vector128`1) was skipped since it collides with above method

    # Skipped Clamp due to it being static, abstract and generic.

    Clamp : Clamp_MethodGroup
    class Clamp_MethodGroup:
        def __getitem__(self, t:typing.Type[Clamp_1_T1]) -> Clamp_1[Clamp_1_T1]: ...

        Clamp_1_T1 = typing.TypeVar('Clamp_1_T1')
        class Clamp_1(typing.Generic[Clamp_1_T1]):
            Clamp_1_T = Vector128_0.Clamp_MethodGroup.Clamp_1_T1
            def __call__(self, value: Vector128_1[Clamp_1_T], min: Vector128_1[Clamp_1_T], max: Vector128_1[Clamp_1_T]) -> Vector128_1[Clamp_1_T]:...


    # Skipped ClampNative due to it being static, abstract and generic.

    ClampNative : ClampNative_MethodGroup
    class ClampNative_MethodGroup:
        def __getitem__(self, t:typing.Type[ClampNative_1_T1]) -> ClampNative_1[ClampNative_1_T1]: ...

        ClampNative_1_T1 = typing.TypeVar('ClampNative_1_T1')
        class ClampNative_1(typing.Generic[ClampNative_1_T1]):
            ClampNative_1_T = Vector128_0.ClampNative_MethodGroup.ClampNative_1_T1
            def __call__(self, value: Vector128_1[ClampNative_1_T], min: Vector128_1[ClampNative_1_T], max: Vector128_1[ClampNative_1_T]) -> Vector128_1[ClampNative_1_T]:...


    # Skipped ConditionalSelect due to it being static, abstract and generic.

    ConditionalSelect : ConditionalSelect_MethodGroup
    class ConditionalSelect_MethodGroup:
        def __getitem__(self, t:typing.Type[ConditionalSelect_1_T1]) -> ConditionalSelect_1[ConditionalSelect_1_T1]: ...

        ConditionalSelect_1_T1 = typing.TypeVar('ConditionalSelect_1_T1')
        class ConditionalSelect_1(typing.Generic[ConditionalSelect_1_T1]):
            ConditionalSelect_1_T = Vector128_0.ConditionalSelect_MethodGroup.ConditionalSelect_1_T1
            def __call__(self, condition: Vector128_1[ConditionalSelect_1_T], left: Vector128_1[ConditionalSelect_1_T], right: Vector128_1[ConditionalSelect_1_T]) -> Vector128_1[ConditionalSelect_1_T]:...


    # Skipped ConvertToDouble due to it being static, abstract and generic.

    ConvertToDouble : ConvertToDouble_MethodGroup
    class ConvertToDouble_MethodGroup:
        def __call__(self, vector: Vector128_1[int]) -> Vector128_1[float]:...
        # Method ConvertToDouble(vector : Vector128`1) was skipped since it collides with above method

    # Skipped ConvertToSingle due to it being static, abstract and generic.

    ConvertToSingle : ConvertToSingle_MethodGroup
    class ConvertToSingle_MethodGroup:
        def __call__(self, vector: Vector128_1[int]) -> Vector128_1[float]:...
        # Method ConvertToSingle(vector : Vector128`1) was skipped since it collides with above method

    # Skipped CopySign due to it being static, abstract and generic.

    CopySign : CopySign_MethodGroup
    class CopySign_MethodGroup:
        def __getitem__(self, t:typing.Type[CopySign_1_T1]) -> CopySign_1[CopySign_1_T1]: ...

        CopySign_1_T1 = typing.TypeVar('CopySign_1_T1')
        class CopySign_1(typing.Generic[CopySign_1_T1]):
            CopySign_1_T = Vector128_0.CopySign_MethodGroup.CopySign_1_T1
            def __call__(self, value: Vector128_1[CopySign_1_T], sign: Vector128_1[CopySign_1_T]) -> Vector128_1[CopySign_1_T]:...


    # Skipped CopyTo due to it being static, abstract and generic.

    CopyTo : CopyTo_MethodGroup
    class CopyTo_MethodGroup:
        def __getitem__(self, t:typing.Type[CopyTo_1_T1]) -> CopyTo_1[CopyTo_1_T1]: ...

        CopyTo_1_T1 = typing.TypeVar('CopyTo_1_T1')
        class CopyTo_1(typing.Generic[CopyTo_1_T1]):
            CopyTo_1_T = Vector128_0.CopyTo_MethodGroup.CopyTo_1_T1
            @typing.overload
            def __call__(self, vector: Vector128_1[CopyTo_1_T], destination: Array_1[CopyTo_1_T]) -> None:...
            @typing.overload
            def __call__(self, vector: Vector128_1[CopyTo_1_T], destination: Span_1[CopyTo_1_T]) -> None:...
            @typing.overload
            def __call__(self, vector: Vector128_1[CopyTo_1_T], destination: Array_1[CopyTo_1_T], startIndex: int) -> None:...


    # Skipped Cos due to it being static, abstract and generic.

    Cos : Cos_MethodGroup
    class Cos_MethodGroup:
        def __call__(self, vector: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Cos(vector : Vector128`1) was skipped since it collides with above method

    # Skipped Count due to it being static, abstract and generic.

    Count : Count_MethodGroup
    class Count_MethodGroup:
        def __getitem__(self, t:typing.Type[Count_1_T1]) -> Count_1[Count_1_T1]: ...

        Count_1_T1 = typing.TypeVar('Count_1_T1')
        class Count_1(typing.Generic[Count_1_T1]):
            Count_1_T = Vector128_0.Count_MethodGroup.Count_1_T1
            def __call__(self, vector: Vector128_1[Count_1_T], value: Count_1_T) -> int:...


    # Skipped CountWhereAllBitsSet due to it being static, abstract and generic.

    CountWhereAllBitsSet : CountWhereAllBitsSet_MethodGroup
    class CountWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[CountWhereAllBitsSet_1_T1]) -> CountWhereAllBitsSet_1[CountWhereAllBitsSet_1_T1]: ...

        CountWhereAllBitsSet_1_T1 = typing.TypeVar('CountWhereAllBitsSet_1_T1')
        class CountWhereAllBitsSet_1(typing.Generic[CountWhereAllBitsSet_1_T1]):
            CountWhereAllBitsSet_1_T = Vector128_0.CountWhereAllBitsSet_MethodGroup.CountWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector128_1[CountWhereAllBitsSet_1_T]) -> int:...


    # Skipped Create due to it being static, abstract and generic.

    Create : Create_MethodGroup
    class Create_MethodGroup:
        def __getitem__(self, t:typing.Type[Create_1_T1]) -> Create_1[Create_1_T1]: ...

        Create_1_T1 = typing.TypeVar('Create_1_T1')
        class Create_1(typing.Generic[Create_1_T1]):
            Create_1_T = Vector128_0.Create_MethodGroup.Create_1_T1
            @typing.overload
            def __call__(self, values: Array_1[Create_1_T]) -> Vector128_1[Create_1_T]:...
            @typing.overload
            def __call__(self, value: Vector64_1[Create_1_T]) -> Vector128_1[Create_1_T]:...
            @typing.overload
            def __call__(self, values: ReadOnlySpan_1[Create_1_T]) -> Vector128_1[Create_1_T]:...
            @typing.overload
            def __call__(self, value: Create_1_T) -> Vector128_1[Create_1_T]:...
            @typing.overload
            def __call__(self, values: Array_1[Create_1_T], index: int) -> Vector128_1[Create_1_T]:...
            @typing.overload
            def __call__(self, lower: Vector64_1[Create_1_T], upper: Vector64_1[Create_1_T]) -> Vector128_1[Create_1_T]:...

        @typing.overload
        def __call__(self, value: float) -> Vector128_1[float]:...
        # Method Create(value : Single) was skipped since it collides with above method
        # Method Create(value : Byte) was skipped since it collides with above method
        # Method Create(value : Int16) was skipped since it collides with above method
        # Method Create(value : Int32) was skipped since it collides with above method
        # Method Create(value : Int64) was skipped since it collides with above method
        # Method Create(value : SByte) was skipped since it collides with above method
        # Method Create(value : UInt16) was skipped since it collides with above method
        # Method Create(value : UInt32) was skipped since it collides with above method
        # Method Create(value : UInt64) was skipped since it collides with above method
        # Method Create(value : IntPtr) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: UIntPtr) -> Vector128_1[UIntPtr]:...
        @typing.overload
        def __call__(self, e0: float, e1: float) -> Vector128_1[float]:...
        # Method Create(e0 : Int64, e1 : Int64) was skipped since it collides with above method
        # Method Create(e0 : UInt64, e1 : UInt64) was skipped since it collides with above method
        @typing.overload
        def __call__(self, lower: Vector64_1[float], upper: Vector64_1[float]) -> Vector128_1[float]:...
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Create(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, lower: Vector64_1[UIntPtr], upper: Vector64_1[UIntPtr]) -> Vector128_1[UIntPtr]:...
        @typing.overload
        def __call__(self, e0: float, e1: float, e2: float, e3: float) -> Vector128_1[float]:...
        # Method Create(e0 : Int32, e1 : Int32, e2 : Int32, e3 : Int32) was skipped since it collides with above method
        # Method Create(e0 : UInt32, e1 : UInt32, e2 : UInt32, e3 : UInt32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int) -> Vector128_1[int]:...
        # Method Create(e0 : UInt16, e1 : UInt16, e2 : UInt16, e3 : UInt16, e4 : UInt16, e5 : UInt16, e6 : UInt16, e7 : UInt16) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int, e8: int, e9: int, e10: int, e11: int, e12: int, e13: int, e14: int, e15: int) -> Vector128_1[int]:...
        # Method Create(e0 : SByte, e1 : SByte, e2 : SByte, e3 : SByte, e4 : SByte, e5 : SByte, e6 : SByte, e7 : SByte, e8 : SByte, e9 : SByte, e10 : SByte, e11 : SByte, e12 : SByte, e13 : SByte, e14 : SByte, e15 : SByte) was skipped since it collides with above method

    # Skipped CreateScalar due to it being static, abstract and generic.

    CreateScalar : CreateScalar_MethodGroup
    class CreateScalar_MethodGroup:
        def __getitem__(self, t:typing.Type[CreateScalar_1_T1]) -> CreateScalar_1[CreateScalar_1_T1]: ...

        CreateScalar_1_T1 = typing.TypeVar('CreateScalar_1_T1')
        class CreateScalar_1(typing.Generic[CreateScalar_1_T1]):
            CreateScalar_1_T = Vector128_0.CreateScalar_MethodGroup.CreateScalar_1_T1
            def __call__(self, value: CreateScalar_1_T) -> Vector128_1[CreateScalar_1_T]:...

        @typing.overload
        def __call__(self, value: float) -> Vector128_1[float]:...
        # Method CreateScalar(value : Single) was skipped since it collides with above method
        # Method CreateScalar(value : Byte) was skipped since it collides with above method
        # Method CreateScalar(value : Int16) was skipped since it collides with above method
        # Method CreateScalar(value : Int32) was skipped since it collides with above method
        # Method CreateScalar(value : Int64) was skipped since it collides with above method
        # Method CreateScalar(value : SByte) was skipped since it collides with above method
        # Method CreateScalar(value : UInt16) was skipped since it collides with above method
        # Method CreateScalar(value : UInt32) was skipped since it collides with above method
        # Method CreateScalar(value : UInt64) was skipped since it collides with above method
        # Method CreateScalar(value : IntPtr) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: UIntPtr) -> Vector128_1[UIntPtr]:...

    # Skipped CreateScalarUnsafe due to it being static, abstract and generic.

    CreateScalarUnsafe : CreateScalarUnsafe_MethodGroup
    class CreateScalarUnsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[CreateScalarUnsafe_1_T1]) -> CreateScalarUnsafe_1[CreateScalarUnsafe_1_T1]: ...

        CreateScalarUnsafe_1_T1 = typing.TypeVar('CreateScalarUnsafe_1_T1')
        class CreateScalarUnsafe_1(typing.Generic[CreateScalarUnsafe_1_T1]):
            CreateScalarUnsafe_1_T = Vector128_0.CreateScalarUnsafe_MethodGroup.CreateScalarUnsafe_1_T1
            def __call__(self, value: CreateScalarUnsafe_1_T) -> Vector128_1[CreateScalarUnsafe_1_T]:...

        @typing.overload
        def __call__(self, value: float) -> Vector128_1[float]:...
        # Method CreateScalarUnsafe(value : Single) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Byte) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int16) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int32) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int64) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : SByte) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt16) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt32) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt64) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : IntPtr) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: UIntPtr) -> Vector128_1[UIntPtr]:...

    # Skipped CreateSequence due to it being static, abstract and generic.

    CreateSequence : CreateSequence_MethodGroup
    class CreateSequence_MethodGroup:
        def __getitem__(self, t:typing.Type[CreateSequence_1_T1]) -> CreateSequence_1[CreateSequence_1_T1]: ...

        CreateSequence_1_T1 = typing.TypeVar('CreateSequence_1_T1')
        class CreateSequence_1(typing.Generic[CreateSequence_1_T1]):
            CreateSequence_1_T = Vector128_0.CreateSequence_MethodGroup.CreateSequence_1_T1
            def __call__(self, start: CreateSequence_1_T, step: CreateSequence_1_T) -> Vector128_1[CreateSequence_1_T]:...


    # Skipped DegreesToRadians due to it being static, abstract and generic.

    DegreesToRadians : DegreesToRadians_MethodGroup
    class DegreesToRadians_MethodGroup:
        def __call__(self, degrees: Vector128_1[float]) -> Vector128_1[float]:...
        # Method DegreesToRadians(degrees : Vector128`1) was skipped since it collides with above method

    # Skipped Divide due to it being static, abstract and generic.

    Divide : Divide_MethodGroup
    class Divide_MethodGroup:
        def __getitem__(self, t:typing.Type[Divide_1_T1]) -> Divide_1[Divide_1_T1]: ...

        Divide_1_T1 = typing.TypeVar('Divide_1_T1')
        class Divide_1(typing.Generic[Divide_1_T1]):
            Divide_1_T = Vector128_0.Divide_MethodGroup.Divide_1_T1
            @typing.overload
            def __call__(self, left: Vector128_1[Divide_1_T], right: Vector128_1[Divide_1_T]) -> Vector128_1[Divide_1_T]:...
            @typing.overload
            def __call__(self, left: Vector128_1[Divide_1_T], right: Divide_1_T) -> Vector128_1[Divide_1_T]:...


    # Skipped Dot due to it being static, abstract and generic.

    Dot : Dot_MethodGroup
    class Dot_MethodGroup:
        def __getitem__(self, t:typing.Type[Dot_1_T1]) -> Dot_1[Dot_1_T1]: ...

        Dot_1_T1 = typing.TypeVar('Dot_1_T1')
        class Dot_1(typing.Generic[Dot_1_T1]):
            Dot_1_T = Vector128_0.Dot_MethodGroup.Dot_1_T1
            def __call__(self, left: Vector128_1[Dot_1_T], right: Vector128_1[Dot_1_T]) -> Dot_1_T:...


    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        def __getitem__(self, t:typing.Type[Equals_1_T1]) -> Equals_1[Equals_1_T1]: ...

        Equals_1_T1 = typing.TypeVar('Equals_1_T1')
        class Equals_1(typing.Generic[Equals_1_T1]):
            Equals_1_T = Vector128_0.Equals_MethodGroup.Equals_1_T1
            def __call__(self, left: Vector128_1[Equals_1_T], right: Vector128_1[Equals_1_T]) -> Vector128_1[Equals_1_T]:...


    # Skipped EqualsAll due to it being static, abstract and generic.

    EqualsAll : EqualsAll_MethodGroup
    class EqualsAll_MethodGroup:
        def __getitem__(self, t:typing.Type[EqualsAll_1_T1]) -> EqualsAll_1[EqualsAll_1_T1]: ...

        EqualsAll_1_T1 = typing.TypeVar('EqualsAll_1_T1')
        class EqualsAll_1(typing.Generic[EqualsAll_1_T1]):
            EqualsAll_1_T = Vector128_0.EqualsAll_MethodGroup.EqualsAll_1_T1
            def __call__(self, left: Vector128_1[EqualsAll_1_T], right: Vector128_1[EqualsAll_1_T]) -> bool:...


    # Skipped EqualsAny due to it being static, abstract and generic.

    EqualsAny : EqualsAny_MethodGroup
    class EqualsAny_MethodGroup:
        def __getitem__(self, t:typing.Type[EqualsAny_1_T1]) -> EqualsAny_1[EqualsAny_1_T1]: ...

        EqualsAny_1_T1 = typing.TypeVar('EqualsAny_1_T1')
        class EqualsAny_1(typing.Generic[EqualsAny_1_T1]):
            EqualsAny_1_T = Vector128_0.EqualsAny_MethodGroup.EqualsAny_1_T1
            def __call__(self, left: Vector128_1[EqualsAny_1_T], right: Vector128_1[EqualsAny_1_T]) -> bool:...


    # Skipped Exp due to it being static, abstract and generic.

    Exp : Exp_MethodGroup
    class Exp_MethodGroup:
        def __call__(self, vector: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Exp(vector : Vector128`1) was skipped since it collides with above method

    # Skipped ExtractMostSignificantBits due to it being static, abstract and generic.

    ExtractMostSignificantBits : ExtractMostSignificantBits_MethodGroup
    class ExtractMostSignificantBits_MethodGroup:
        def __getitem__(self, t:typing.Type[ExtractMostSignificantBits_1_T1]) -> ExtractMostSignificantBits_1[ExtractMostSignificantBits_1_T1]: ...

        ExtractMostSignificantBits_1_T1 = typing.TypeVar('ExtractMostSignificantBits_1_T1')
        class ExtractMostSignificantBits_1(typing.Generic[ExtractMostSignificantBits_1_T1]):
            ExtractMostSignificantBits_1_T = Vector128_0.ExtractMostSignificantBits_MethodGroup.ExtractMostSignificantBits_1_T1
            def __call__(self, vector: Vector128_1[ExtractMostSignificantBits_1_T]) -> int:...


    # Skipped Floor due to it being static, abstract and generic.

    Floor : Floor_MethodGroup
    class Floor_MethodGroup:
        def __call__(self, vector: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Floor(vector : Vector128`1) was skipped since it collides with above method

    # Skipped FusedMultiplyAdd due to it being static, abstract and generic.

    FusedMultiplyAdd : FusedMultiplyAdd_MethodGroup
    class FusedMultiplyAdd_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float], addend: Vector128_1[float]) -> Vector128_1[float]:...
        # Method FusedMultiplyAdd(left : Vector128`1, right : Vector128`1, addend : Vector128`1) was skipped since it collides with above method

    # Skipped GetElement due to it being static, abstract and generic.

    GetElement : GetElement_MethodGroup
    class GetElement_MethodGroup:
        def __getitem__(self, t:typing.Type[GetElement_1_T1]) -> GetElement_1[GetElement_1_T1]: ...

        GetElement_1_T1 = typing.TypeVar('GetElement_1_T1')
        class GetElement_1(typing.Generic[GetElement_1_T1]):
            GetElement_1_T = Vector128_0.GetElement_MethodGroup.GetElement_1_T1
            def __call__(self, vector: Vector128_1[GetElement_1_T], index: int) -> GetElement_1_T:...


    # Skipped GetLower due to it being static, abstract and generic.

    GetLower : GetLower_MethodGroup
    class GetLower_MethodGroup:
        def __getitem__(self, t:typing.Type[GetLower_1_T1]) -> GetLower_1[GetLower_1_T1]: ...

        GetLower_1_T1 = typing.TypeVar('GetLower_1_T1')
        class GetLower_1(typing.Generic[GetLower_1_T1]):
            GetLower_1_T = Vector128_0.GetLower_MethodGroup.GetLower_1_T1
            def __call__(self, vector: Vector128_1[GetLower_1_T]) -> Vector64_1[GetLower_1_T]:...


    # Skipped GetUpper due to it being static, abstract and generic.

    GetUpper : GetUpper_MethodGroup
    class GetUpper_MethodGroup:
        def __getitem__(self, t:typing.Type[GetUpper_1_T1]) -> GetUpper_1[GetUpper_1_T1]: ...

        GetUpper_1_T1 = typing.TypeVar('GetUpper_1_T1')
        class GetUpper_1(typing.Generic[GetUpper_1_T1]):
            GetUpper_1_T = Vector128_0.GetUpper_MethodGroup.GetUpper_1_T1
            def __call__(self, vector: Vector128_1[GetUpper_1_T]) -> Vector64_1[GetUpper_1_T]:...


    # Skipped GreaterThan due to it being static, abstract and generic.

    GreaterThan : GreaterThan_MethodGroup
    class GreaterThan_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThan_1_T1]) -> GreaterThan_1[GreaterThan_1_T1]: ...

        GreaterThan_1_T1 = typing.TypeVar('GreaterThan_1_T1')
        class GreaterThan_1(typing.Generic[GreaterThan_1_T1]):
            GreaterThan_1_T = Vector128_0.GreaterThan_MethodGroup.GreaterThan_1_T1
            def __call__(self, left: Vector128_1[GreaterThan_1_T], right: Vector128_1[GreaterThan_1_T]) -> Vector128_1[GreaterThan_1_T]:...


    # Skipped GreaterThanAll due to it being static, abstract and generic.

    GreaterThanAll : GreaterThanAll_MethodGroup
    class GreaterThanAll_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanAll_1_T1]) -> GreaterThanAll_1[GreaterThanAll_1_T1]: ...

        GreaterThanAll_1_T1 = typing.TypeVar('GreaterThanAll_1_T1')
        class GreaterThanAll_1(typing.Generic[GreaterThanAll_1_T1]):
            GreaterThanAll_1_T = Vector128_0.GreaterThanAll_MethodGroup.GreaterThanAll_1_T1
            def __call__(self, left: Vector128_1[GreaterThanAll_1_T], right: Vector128_1[GreaterThanAll_1_T]) -> bool:...


    # Skipped GreaterThanAny due to it being static, abstract and generic.

    GreaterThanAny : GreaterThanAny_MethodGroup
    class GreaterThanAny_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanAny_1_T1]) -> GreaterThanAny_1[GreaterThanAny_1_T1]: ...

        GreaterThanAny_1_T1 = typing.TypeVar('GreaterThanAny_1_T1')
        class GreaterThanAny_1(typing.Generic[GreaterThanAny_1_T1]):
            GreaterThanAny_1_T = Vector128_0.GreaterThanAny_MethodGroup.GreaterThanAny_1_T1
            def __call__(self, left: Vector128_1[GreaterThanAny_1_T], right: Vector128_1[GreaterThanAny_1_T]) -> bool:...


    # Skipped GreaterThanOrEqual due to it being static, abstract and generic.

    GreaterThanOrEqual : GreaterThanOrEqual_MethodGroup
    class GreaterThanOrEqual_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqual_1_T1]) -> GreaterThanOrEqual_1[GreaterThanOrEqual_1_T1]: ...

        GreaterThanOrEqual_1_T1 = typing.TypeVar('GreaterThanOrEqual_1_T1')
        class GreaterThanOrEqual_1(typing.Generic[GreaterThanOrEqual_1_T1]):
            GreaterThanOrEqual_1_T = Vector128_0.GreaterThanOrEqual_MethodGroup.GreaterThanOrEqual_1_T1
            def __call__(self, left: Vector128_1[GreaterThanOrEqual_1_T], right: Vector128_1[GreaterThanOrEqual_1_T]) -> Vector128_1[GreaterThanOrEqual_1_T]:...


    # Skipped GreaterThanOrEqualAll due to it being static, abstract and generic.

    GreaterThanOrEqualAll : GreaterThanOrEqualAll_MethodGroup
    class GreaterThanOrEqualAll_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqualAll_1_T1]) -> GreaterThanOrEqualAll_1[GreaterThanOrEqualAll_1_T1]: ...

        GreaterThanOrEqualAll_1_T1 = typing.TypeVar('GreaterThanOrEqualAll_1_T1')
        class GreaterThanOrEqualAll_1(typing.Generic[GreaterThanOrEqualAll_1_T1]):
            GreaterThanOrEqualAll_1_T = Vector128_0.GreaterThanOrEqualAll_MethodGroup.GreaterThanOrEqualAll_1_T1
            def __call__(self, left: Vector128_1[GreaterThanOrEqualAll_1_T], right: Vector128_1[GreaterThanOrEqualAll_1_T]) -> bool:...


    # Skipped GreaterThanOrEqualAny due to it being static, abstract and generic.

    GreaterThanOrEqualAny : GreaterThanOrEqualAny_MethodGroup
    class GreaterThanOrEqualAny_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqualAny_1_T1]) -> GreaterThanOrEqualAny_1[GreaterThanOrEqualAny_1_T1]: ...

        GreaterThanOrEqualAny_1_T1 = typing.TypeVar('GreaterThanOrEqualAny_1_T1')
        class GreaterThanOrEqualAny_1(typing.Generic[GreaterThanOrEqualAny_1_T1]):
            GreaterThanOrEqualAny_1_T = Vector128_0.GreaterThanOrEqualAny_MethodGroup.GreaterThanOrEqualAny_1_T1
            def __call__(self, left: Vector128_1[GreaterThanOrEqualAny_1_T], right: Vector128_1[GreaterThanOrEqualAny_1_T]) -> bool:...


    # Skipped Hypot due to it being static, abstract and generic.

    Hypot : Hypot_MethodGroup
    class Hypot_MethodGroup:
        def __call__(self, x: Vector128_1[float], y: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Hypot(x : Vector128`1, y : Vector128`1) was skipped since it collides with above method

    # Skipped IndexOf due to it being static, abstract and generic.

    IndexOf : IndexOf_MethodGroup
    class IndexOf_MethodGroup:
        def __getitem__(self, t:typing.Type[IndexOf_1_T1]) -> IndexOf_1[IndexOf_1_T1]: ...

        IndexOf_1_T1 = typing.TypeVar('IndexOf_1_T1')
        class IndexOf_1(typing.Generic[IndexOf_1_T1]):
            IndexOf_1_T = Vector128_0.IndexOf_MethodGroup.IndexOf_1_T1
            def __call__(self, vector: Vector128_1[IndexOf_1_T], value: IndexOf_1_T) -> int:...


    # Skipped IndexOfWhereAllBitsSet due to it being static, abstract and generic.

    IndexOfWhereAllBitsSet : IndexOfWhereAllBitsSet_MethodGroup
    class IndexOfWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[IndexOfWhereAllBitsSet_1_T1]) -> IndexOfWhereAllBitsSet_1[IndexOfWhereAllBitsSet_1_T1]: ...

        IndexOfWhereAllBitsSet_1_T1 = typing.TypeVar('IndexOfWhereAllBitsSet_1_T1')
        class IndexOfWhereAllBitsSet_1(typing.Generic[IndexOfWhereAllBitsSet_1_T1]):
            IndexOfWhereAllBitsSet_1_T = Vector128_0.IndexOfWhereAllBitsSet_MethodGroup.IndexOfWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector128_1[IndexOfWhereAllBitsSet_1_T]) -> int:...


    # Skipped IsEvenInteger due to it being static, abstract and generic.

    IsEvenInteger : IsEvenInteger_MethodGroup
    class IsEvenInteger_MethodGroup:
        def __getitem__(self, t:typing.Type[IsEvenInteger_1_T1]) -> IsEvenInteger_1[IsEvenInteger_1_T1]: ...

        IsEvenInteger_1_T1 = typing.TypeVar('IsEvenInteger_1_T1')
        class IsEvenInteger_1(typing.Generic[IsEvenInteger_1_T1]):
            IsEvenInteger_1_T = Vector128_0.IsEvenInteger_MethodGroup.IsEvenInteger_1_T1
            def __call__(self, vector: Vector128_1[IsEvenInteger_1_T]) -> Vector128_1[IsEvenInteger_1_T]:...


    # Skipped IsFinite due to it being static, abstract and generic.

    IsFinite : IsFinite_MethodGroup
    class IsFinite_MethodGroup:
        def __getitem__(self, t:typing.Type[IsFinite_1_T1]) -> IsFinite_1[IsFinite_1_T1]: ...

        IsFinite_1_T1 = typing.TypeVar('IsFinite_1_T1')
        class IsFinite_1(typing.Generic[IsFinite_1_T1]):
            IsFinite_1_T = Vector128_0.IsFinite_MethodGroup.IsFinite_1_T1
            def __call__(self, vector: Vector128_1[IsFinite_1_T]) -> Vector128_1[IsFinite_1_T]:...


    # Skipped IsInfinity due to it being static, abstract and generic.

    IsInfinity : IsInfinity_MethodGroup
    class IsInfinity_MethodGroup:
        def __getitem__(self, t:typing.Type[IsInfinity_1_T1]) -> IsInfinity_1[IsInfinity_1_T1]: ...

        IsInfinity_1_T1 = typing.TypeVar('IsInfinity_1_T1')
        class IsInfinity_1(typing.Generic[IsInfinity_1_T1]):
            IsInfinity_1_T = Vector128_0.IsInfinity_MethodGroup.IsInfinity_1_T1
            def __call__(self, vector: Vector128_1[IsInfinity_1_T]) -> Vector128_1[IsInfinity_1_T]:...


    # Skipped IsInteger due to it being static, abstract and generic.

    IsInteger : IsInteger_MethodGroup
    class IsInteger_MethodGroup:
        def __getitem__(self, t:typing.Type[IsInteger_1_T1]) -> IsInteger_1[IsInteger_1_T1]: ...

        IsInteger_1_T1 = typing.TypeVar('IsInteger_1_T1')
        class IsInteger_1(typing.Generic[IsInteger_1_T1]):
            IsInteger_1_T = Vector128_0.IsInteger_MethodGroup.IsInteger_1_T1
            def __call__(self, vector: Vector128_1[IsInteger_1_T]) -> Vector128_1[IsInteger_1_T]:...


    # Skipped IsNaN due to it being static, abstract and generic.

    IsNaN : IsNaN_MethodGroup
    class IsNaN_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNaN_1_T1]) -> IsNaN_1[IsNaN_1_T1]: ...

        IsNaN_1_T1 = typing.TypeVar('IsNaN_1_T1')
        class IsNaN_1(typing.Generic[IsNaN_1_T1]):
            IsNaN_1_T = Vector128_0.IsNaN_MethodGroup.IsNaN_1_T1
            def __call__(self, vector: Vector128_1[IsNaN_1_T]) -> Vector128_1[IsNaN_1_T]:...


    # Skipped IsNegative due to it being static, abstract and generic.

    IsNegative : IsNegative_MethodGroup
    class IsNegative_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNegative_1_T1]) -> IsNegative_1[IsNegative_1_T1]: ...

        IsNegative_1_T1 = typing.TypeVar('IsNegative_1_T1')
        class IsNegative_1(typing.Generic[IsNegative_1_T1]):
            IsNegative_1_T = Vector128_0.IsNegative_MethodGroup.IsNegative_1_T1
            def __call__(self, vector: Vector128_1[IsNegative_1_T]) -> Vector128_1[IsNegative_1_T]:...


    # Skipped IsNegativeInfinity due to it being static, abstract and generic.

    IsNegativeInfinity : IsNegativeInfinity_MethodGroup
    class IsNegativeInfinity_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNegativeInfinity_1_T1]) -> IsNegativeInfinity_1[IsNegativeInfinity_1_T1]: ...

        IsNegativeInfinity_1_T1 = typing.TypeVar('IsNegativeInfinity_1_T1')
        class IsNegativeInfinity_1(typing.Generic[IsNegativeInfinity_1_T1]):
            IsNegativeInfinity_1_T = Vector128_0.IsNegativeInfinity_MethodGroup.IsNegativeInfinity_1_T1
            def __call__(self, vector: Vector128_1[IsNegativeInfinity_1_T]) -> Vector128_1[IsNegativeInfinity_1_T]:...


    # Skipped IsNormal due to it being static, abstract and generic.

    IsNormal : IsNormal_MethodGroup
    class IsNormal_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNormal_1_T1]) -> IsNormal_1[IsNormal_1_T1]: ...

        IsNormal_1_T1 = typing.TypeVar('IsNormal_1_T1')
        class IsNormal_1(typing.Generic[IsNormal_1_T1]):
            IsNormal_1_T = Vector128_0.IsNormal_MethodGroup.IsNormal_1_T1
            def __call__(self, vector: Vector128_1[IsNormal_1_T]) -> Vector128_1[IsNormal_1_T]:...


    # Skipped IsOddInteger due to it being static, abstract and generic.

    IsOddInteger : IsOddInteger_MethodGroup
    class IsOddInteger_MethodGroup:
        def __getitem__(self, t:typing.Type[IsOddInteger_1_T1]) -> IsOddInteger_1[IsOddInteger_1_T1]: ...

        IsOddInteger_1_T1 = typing.TypeVar('IsOddInteger_1_T1')
        class IsOddInteger_1(typing.Generic[IsOddInteger_1_T1]):
            IsOddInteger_1_T = Vector128_0.IsOddInteger_MethodGroup.IsOddInteger_1_T1
            def __call__(self, vector: Vector128_1[IsOddInteger_1_T]) -> Vector128_1[IsOddInteger_1_T]:...


    # Skipped IsPositive due to it being static, abstract and generic.

    IsPositive : IsPositive_MethodGroup
    class IsPositive_MethodGroup:
        def __getitem__(self, t:typing.Type[IsPositive_1_T1]) -> IsPositive_1[IsPositive_1_T1]: ...

        IsPositive_1_T1 = typing.TypeVar('IsPositive_1_T1')
        class IsPositive_1(typing.Generic[IsPositive_1_T1]):
            IsPositive_1_T = Vector128_0.IsPositive_MethodGroup.IsPositive_1_T1
            def __call__(self, vector: Vector128_1[IsPositive_1_T]) -> Vector128_1[IsPositive_1_T]:...


    # Skipped IsPositiveInfinity due to it being static, abstract and generic.

    IsPositiveInfinity : IsPositiveInfinity_MethodGroup
    class IsPositiveInfinity_MethodGroup:
        def __getitem__(self, t:typing.Type[IsPositiveInfinity_1_T1]) -> IsPositiveInfinity_1[IsPositiveInfinity_1_T1]: ...

        IsPositiveInfinity_1_T1 = typing.TypeVar('IsPositiveInfinity_1_T1')
        class IsPositiveInfinity_1(typing.Generic[IsPositiveInfinity_1_T1]):
            IsPositiveInfinity_1_T = Vector128_0.IsPositiveInfinity_MethodGroup.IsPositiveInfinity_1_T1
            def __call__(self, vector: Vector128_1[IsPositiveInfinity_1_T]) -> Vector128_1[IsPositiveInfinity_1_T]:...


    # Skipped IsSubnormal due to it being static, abstract and generic.

    IsSubnormal : IsSubnormal_MethodGroup
    class IsSubnormal_MethodGroup:
        def __getitem__(self, t:typing.Type[IsSubnormal_1_T1]) -> IsSubnormal_1[IsSubnormal_1_T1]: ...

        IsSubnormal_1_T1 = typing.TypeVar('IsSubnormal_1_T1')
        class IsSubnormal_1(typing.Generic[IsSubnormal_1_T1]):
            IsSubnormal_1_T = Vector128_0.IsSubnormal_MethodGroup.IsSubnormal_1_T1
            def __call__(self, vector: Vector128_1[IsSubnormal_1_T]) -> Vector128_1[IsSubnormal_1_T]:...


    # Skipped IsZero due to it being static, abstract and generic.

    IsZero : IsZero_MethodGroup
    class IsZero_MethodGroup:
        def __getitem__(self, t:typing.Type[IsZero_1_T1]) -> IsZero_1[IsZero_1_T1]: ...

        IsZero_1_T1 = typing.TypeVar('IsZero_1_T1')
        class IsZero_1(typing.Generic[IsZero_1_T1]):
            IsZero_1_T = Vector128_0.IsZero_MethodGroup.IsZero_1_T1
            def __call__(self, vector: Vector128_1[IsZero_1_T]) -> Vector128_1[IsZero_1_T]:...


    # Skipped LastIndexOf due to it being static, abstract and generic.

    LastIndexOf : LastIndexOf_MethodGroup
    class LastIndexOf_MethodGroup:
        def __getitem__(self, t:typing.Type[LastIndexOf_1_T1]) -> LastIndexOf_1[LastIndexOf_1_T1]: ...

        LastIndexOf_1_T1 = typing.TypeVar('LastIndexOf_1_T1')
        class LastIndexOf_1(typing.Generic[LastIndexOf_1_T1]):
            LastIndexOf_1_T = Vector128_0.LastIndexOf_MethodGroup.LastIndexOf_1_T1
            def __call__(self, vector: Vector128_1[LastIndexOf_1_T], value: LastIndexOf_1_T) -> int:...


    # Skipped LastIndexOfWhereAllBitsSet due to it being static, abstract and generic.

    LastIndexOfWhereAllBitsSet : LastIndexOfWhereAllBitsSet_MethodGroup
    class LastIndexOfWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[LastIndexOfWhereAllBitsSet_1_T1]) -> LastIndexOfWhereAllBitsSet_1[LastIndexOfWhereAllBitsSet_1_T1]: ...

        LastIndexOfWhereAllBitsSet_1_T1 = typing.TypeVar('LastIndexOfWhereAllBitsSet_1_T1')
        class LastIndexOfWhereAllBitsSet_1(typing.Generic[LastIndexOfWhereAllBitsSet_1_T1]):
            LastIndexOfWhereAllBitsSet_1_T = Vector128_0.LastIndexOfWhereAllBitsSet_MethodGroup.LastIndexOfWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector128_1[LastIndexOfWhereAllBitsSet_1_T]) -> int:...


    # Skipped Lerp due to it being static, abstract and generic.

    Lerp : Lerp_MethodGroup
    class Lerp_MethodGroup:
        def __call__(self, x: Vector128_1[float], y: Vector128_1[float], amount: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Lerp(x : Vector128`1, y : Vector128`1, amount : Vector128`1) was skipped since it collides with above method

    # Skipped LessThan due to it being static, abstract and generic.

    LessThan : LessThan_MethodGroup
    class LessThan_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThan_1_T1]) -> LessThan_1[LessThan_1_T1]: ...

        LessThan_1_T1 = typing.TypeVar('LessThan_1_T1')
        class LessThan_1(typing.Generic[LessThan_1_T1]):
            LessThan_1_T = Vector128_0.LessThan_MethodGroup.LessThan_1_T1
            def __call__(self, left: Vector128_1[LessThan_1_T], right: Vector128_1[LessThan_1_T]) -> Vector128_1[LessThan_1_T]:...


    # Skipped LessThanAll due to it being static, abstract and generic.

    LessThanAll : LessThanAll_MethodGroup
    class LessThanAll_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanAll_1_T1]) -> LessThanAll_1[LessThanAll_1_T1]: ...

        LessThanAll_1_T1 = typing.TypeVar('LessThanAll_1_T1')
        class LessThanAll_1(typing.Generic[LessThanAll_1_T1]):
            LessThanAll_1_T = Vector128_0.LessThanAll_MethodGroup.LessThanAll_1_T1
            def __call__(self, left: Vector128_1[LessThanAll_1_T], right: Vector128_1[LessThanAll_1_T]) -> bool:...


    # Skipped LessThanAny due to it being static, abstract and generic.

    LessThanAny : LessThanAny_MethodGroup
    class LessThanAny_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanAny_1_T1]) -> LessThanAny_1[LessThanAny_1_T1]: ...

        LessThanAny_1_T1 = typing.TypeVar('LessThanAny_1_T1')
        class LessThanAny_1(typing.Generic[LessThanAny_1_T1]):
            LessThanAny_1_T = Vector128_0.LessThanAny_MethodGroup.LessThanAny_1_T1
            def __call__(self, left: Vector128_1[LessThanAny_1_T], right: Vector128_1[LessThanAny_1_T]) -> bool:...


    # Skipped LessThanOrEqual due to it being static, abstract and generic.

    LessThanOrEqual : LessThanOrEqual_MethodGroup
    class LessThanOrEqual_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqual_1_T1]) -> LessThanOrEqual_1[LessThanOrEqual_1_T1]: ...

        LessThanOrEqual_1_T1 = typing.TypeVar('LessThanOrEqual_1_T1')
        class LessThanOrEqual_1(typing.Generic[LessThanOrEqual_1_T1]):
            LessThanOrEqual_1_T = Vector128_0.LessThanOrEqual_MethodGroup.LessThanOrEqual_1_T1
            def __call__(self, left: Vector128_1[LessThanOrEqual_1_T], right: Vector128_1[LessThanOrEqual_1_T]) -> Vector128_1[LessThanOrEqual_1_T]:...


    # Skipped LessThanOrEqualAll due to it being static, abstract and generic.

    LessThanOrEqualAll : LessThanOrEqualAll_MethodGroup
    class LessThanOrEqualAll_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqualAll_1_T1]) -> LessThanOrEqualAll_1[LessThanOrEqualAll_1_T1]: ...

        LessThanOrEqualAll_1_T1 = typing.TypeVar('LessThanOrEqualAll_1_T1')
        class LessThanOrEqualAll_1(typing.Generic[LessThanOrEqualAll_1_T1]):
            LessThanOrEqualAll_1_T = Vector128_0.LessThanOrEqualAll_MethodGroup.LessThanOrEqualAll_1_T1
            def __call__(self, left: Vector128_1[LessThanOrEqualAll_1_T], right: Vector128_1[LessThanOrEqualAll_1_T]) -> bool:...


    # Skipped LessThanOrEqualAny due to it being static, abstract and generic.

    LessThanOrEqualAny : LessThanOrEqualAny_MethodGroup
    class LessThanOrEqualAny_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqualAny_1_T1]) -> LessThanOrEqualAny_1[LessThanOrEqualAny_1_T1]: ...

        LessThanOrEqualAny_1_T1 = typing.TypeVar('LessThanOrEqualAny_1_T1')
        class LessThanOrEqualAny_1(typing.Generic[LessThanOrEqualAny_1_T1]):
            LessThanOrEqualAny_1_T = Vector128_0.LessThanOrEqualAny_MethodGroup.LessThanOrEqualAny_1_T1
            def __call__(self, left: Vector128_1[LessThanOrEqualAny_1_T], right: Vector128_1[LessThanOrEqualAny_1_T]) -> bool:...


    # Skipped Load due to it being static, abstract and generic.

    Load : Load_MethodGroup
    class Load_MethodGroup:
        def __getitem__(self, t:typing.Type[Load_1_T1]) -> Load_1[Load_1_T1]: ...

        Load_1_T1 = typing.TypeVar('Load_1_T1')
        class Load_1(typing.Generic[Load_1_T1]):
            Load_1_T = Vector128_0.Load_MethodGroup.Load_1_T1
            def __call__(self, source: clr.Reference[Load_1_T]) -> Vector128_1[Load_1_T]:...


    # Skipped LoadAligned due to it being static, abstract and generic.

    LoadAligned : LoadAligned_MethodGroup
    class LoadAligned_MethodGroup:
        def __getitem__(self, t:typing.Type[LoadAligned_1_T1]) -> LoadAligned_1[LoadAligned_1_T1]: ...

        LoadAligned_1_T1 = typing.TypeVar('LoadAligned_1_T1')
        class LoadAligned_1(typing.Generic[LoadAligned_1_T1]):
            LoadAligned_1_T = Vector128_0.LoadAligned_MethodGroup.LoadAligned_1_T1
            def __call__(self, source: clr.Reference[LoadAligned_1_T]) -> Vector128_1[LoadAligned_1_T]:...


    # Skipped LoadAlignedNonTemporal due to it being static, abstract and generic.

    LoadAlignedNonTemporal : LoadAlignedNonTemporal_MethodGroup
    class LoadAlignedNonTemporal_MethodGroup:
        def __getitem__(self, t:typing.Type[LoadAlignedNonTemporal_1_T1]) -> LoadAlignedNonTemporal_1[LoadAlignedNonTemporal_1_T1]: ...

        LoadAlignedNonTemporal_1_T1 = typing.TypeVar('LoadAlignedNonTemporal_1_T1')
        class LoadAlignedNonTemporal_1(typing.Generic[LoadAlignedNonTemporal_1_T1]):
            LoadAlignedNonTemporal_1_T = Vector128_0.LoadAlignedNonTemporal_MethodGroup.LoadAlignedNonTemporal_1_T1
            def __call__(self, source: clr.Reference[LoadAlignedNonTemporal_1_T]) -> Vector128_1[LoadAlignedNonTemporal_1_T]:...


    # Skipped LoadUnsafe due to it being static, abstract and generic.

    LoadUnsafe : LoadUnsafe_MethodGroup
    class LoadUnsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[LoadUnsafe_1_T1]) -> LoadUnsafe_1[LoadUnsafe_1_T1]: ...

        LoadUnsafe_1_T1 = typing.TypeVar('LoadUnsafe_1_T1')
        class LoadUnsafe_1(typing.Generic[LoadUnsafe_1_T1]):
            LoadUnsafe_1_T = Vector128_0.LoadUnsafe_MethodGroup.LoadUnsafe_1_T1
            @typing.overload
            def __call__(self, source: clr.Reference[LoadUnsafe_1_T]) -> Vector128_1[LoadUnsafe_1_T]:...
            @typing.overload
            def __call__(self, source: clr.Reference[LoadUnsafe_1_T], elementOffset: UIntPtr) -> Vector128_1[LoadUnsafe_1_T]:...


    # Skipped Log due to it being static, abstract and generic.

    Log : Log_MethodGroup
    class Log_MethodGroup:
        def __call__(self, vector: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Log(vector : Vector128`1) was skipped since it collides with above method

    # Skipped Log2 due to it being static, abstract and generic.

    Log2 : Log2_MethodGroup
    class Log2_MethodGroup:
        def __call__(self, vector: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Log2(vector : Vector128`1) was skipped since it collides with above method

    # Skipped Max due to it being static, abstract and generic.

    Max : Max_MethodGroup
    class Max_MethodGroup:
        def __getitem__(self, t:typing.Type[Max_1_T1]) -> Max_1[Max_1_T1]: ...

        Max_1_T1 = typing.TypeVar('Max_1_T1')
        class Max_1(typing.Generic[Max_1_T1]):
            Max_1_T = Vector128_0.Max_MethodGroup.Max_1_T1
            def __call__(self, left: Vector128_1[Max_1_T], right: Vector128_1[Max_1_T]) -> Vector128_1[Max_1_T]:...


    # Skipped MaxMagnitude due to it being static, abstract and generic.

    MaxMagnitude : MaxMagnitude_MethodGroup
    class MaxMagnitude_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxMagnitude_1_T1]) -> MaxMagnitude_1[MaxMagnitude_1_T1]: ...

        MaxMagnitude_1_T1 = typing.TypeVar('MaxMagnitude_1_T1')
        class MaxMagnitude_1(typing.Generic[MaxMagnitude_1_T1]):
            MaxMagnitude_1_T = Vector128_0.MaxMagnitude_MethodGroup.MaxMagnitude_1_T1
            def __call__(self, left: Vector128_1[MaxMagnitude_1_T], right: Vector128_1[MaxMagnitude_1_T]) -> Vector128_1[MaxMagnitude_1_T]:...


    # Skipped MaxMagnitudeNumber due to it being static, abstract and generic.

    MaxMagnitudeNumber : MaxMagnitudeNumber_MethodGroup
    class MaxMagnitudeNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxMagnitudeNumber_1_T1]) -> MaxMagnitudeNumber_1[MaxMagnitudeNumber_1_T1]: ...

        MaxMagnitudeNumber_1_T1 = typing.TypeVar('MaxMagnitudeNumber_1_T1')
        class MaxMagnitudeNumber_1(typing.Generic[MaxMagnitudeNumber_1_T1]):
            MaxMagnitudeNumber_1_T = Vector128_0.MaxMagnitudeNumber_MethodGroup.MaxMagnitudeNumber_1_T1
            def __call__(self, left: Vector128_1[MaxMagnitudeNumber_1_T], right: Vector128_1[MaxMagnitudeNumber_1_T]) -> Vector128_1[MaxMagnitudeNumber_1_T]:...


    # Skipped MaxNative due to it being static, abstract and generic.

    MaxNative : MaxNative_MethodGroup
    class MaxNative_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxNative_1_T1]) -> MaxNative_1[MaxNative_1_T1]: ...

        MaxNative_1_T1 = typing.TypeVar('MaxNative_1_T1')
        class MaxNative_1(typing.Generic[MaxNative_1_T1]):
            MaxNative_1_T = Vector128_0.MaxNative_MethodGroup.MaxNative_1_T1
            def __call__(self, left: Vector128_1[MaxNative_1_T], right: Vector128_1[MaxNative_1_T]) -> Vector128_1[MaxNative_1_T]:...


    # Skipped MaxNumber due to it being static, abstract and generic.

    MaxNumber : MaxNumber_MethodGroup
    class MaxNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxNumber_1_T1]) -> MaxNumber_1[MaxNumber_1_T1]: ...

        MaxNumber_1_T1 = typing.TypeVar('MaxNumber_1_T1')
        class MaxNumber_1(typing.Generic[MaxNumber_1_T1]):
            MaxNumber_1_T = Vector128_0.MaxNumber_MethodGroup.MaxNumber_1_T1
            def __call__(self, left: Vector128_1[MaxNumber_1_T], right: Vector128_1[MaxNumber_1_T]) -> Vector128_1[MaxNumber_1_T]:...


    # Skipped Min due to it being static, abstract and generic.

    Min : Min_MethodGroup
    class Min_MethodGroup:
        def __getitem__(self, t:typing.Type[Min_1_T1]) -> Min_1[Min_1_T1]: ...

        Min_1_T1 = typing.TypeVar('Min_1_T1')
        class Min_1(typing.Generic[Min_1_T1]):
            Min_1_T = Vector128_0.Min_MethodGroup.Min_1_T1
            def __call__(self, left: Vector128_1[Min_1_T], right: Vector128_1[Min_1_T]) -> Vector128_1[Min_1_T]:...


    # Skipped MinMagnitude due to it being static, abstract and generic.

    MinMagnitude : MinMagnitude_MethodGroup
    class MinMagnitude_MethodGroup:
        def __getitem__(self, t:typing.Type[MinMagnitude_1_T1]) -> MinMagnitude_1[MinMagnitude_1_T1]: ...

        MinMagnitude_1_T1 = typing.TypeVar('MinMagnitude_1_T1')
        class MinMagnitude_1(typing.Generic[MinMagnitude_1_T1]):
            MinMagnitude_1_T = Vector128_0.MinMagnitude_MethodGroup.MinMagnitude_1_T1
            def __call__(self, left: Vector128_1[MinMagnitude_1_T], right: Vector128_1[MinMagnitude_1_T]) -> Vector128_1[MinMagnitude_1_T]:...


    # Skipped MinMagnitudeNumber due to it being static, abstract and generic.

    MinMagnitudeNumber : MinMagnitudeNumber_MethodGroup
    class MinMagnitudeNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MinMagnitudeNumber_1_T1]) -> MinMagnitudeNumber_1[MinMagnitudeNumber_1_T1]: ...

        MinMagnitudeNumber_1_T1 = typing.TypeVar('MinMagnitudeNumber_1_T1')
        class MinMagnitudeNumber_1(typing.Generic[MinMagnitudeNumber_1_T1]):
            MinMagnitudeNumber_1_T = Vector128_0.MinMagnitudeNumber_MethodGroup.MinMagnitudeNumber_1_T1
            def __call__(self, left: Vector128_1[MinMagnitudeNumber_1_T], right: Vector128_1[MinMagnitudeNumber_1_T]) -> Vector128_1[MinMagnitudeNumber_1_T]:...


    # Skipped MinNative due to it being static, abstract and generic.

    MinNative : MinNative_MethodGroup
    class MinNative_MethodGroup:
        def __getitem__(self, t:typing.Type[MinNative_1_T1]) -> MinNative_1[MinNative_1_T1]: ...

        MinNative_1_T1 = typing.TypeVar('MinNative_1_T1')
        class MinNative_1(typing.Generic[MinNative_1_T1]):
            MinNative_1_T = Vector128_0.MinNative_MethodGroup.MinNative_1_T1
            def __call__(self, left: Vector128_1[MinNative_1_T], right: Vector128_1[MinNative_1_T]) -> Vector128_1[MinNative_1_T]:...


    # Skipped MinNumber due to it being static, abstract and generic.

    MinNumber : MinNumber_MethodGroup
    class MinNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MinNumber_1_T1]) -> MinNumber_1[MinNumber_1_T1]: ...

        MinNumber_1_T1 = typing.TypeVar('MinNumber_1_T1')
        class MinNumber_1(typing.Generic[MinNumber_1_T1]):
            MinNumber_1_T = Vector128_0.MinNumber_MethodGroup.MinNumber_1_T1
            def __call__(self, left: Vector128_1[MinNumber_1_T], right: Vector128_1[MinNumber_1_T]) -> Vector128_1[MinNumber_1_T]:...


    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        def __getitem__(self, t:typing.Type[Multiply_1_T1]) -> Multiply_1[Multiply_1_T1]: ...

        Multiply_1_T1 = typing.TypeVar('Multiply_1_T1')
        class Multiply_1(typing.Generic[Multiply_1_T1]):
            Multiply_1_T = Vector128_0.Multiply_MethodGroup.Multiply_1_T1
            @typing.overload
            def __call__(self, left: Vector128_1[Multiply_1_T], right: Vector128_1[Multiply_1_T]) -> Vector128_1[Multiply_1_T]:...
            @typing.overload
            def __call__(self, left: Vector128_1[Multiply_1_T], right: Multiply_1_T) -> Vector128_1[Multiply_1_T]:...
            @typing.overload
            def __call__(self, left: Multiply_1_T, right: Vector128_1[Multiply_1_T]) -> Vector128_1[Multiply_1_T]:...


    # Skipped MultiplyAddEstimate due to it being static, abstract and generic.

    MultiplyAddEstimate : MultiplyAddEstimate_MethodGroup
    class MultiplyAddEstimate_MethodGroup:
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float], addend: Vector128_1[float]) -> Vector128_1[float]:...
        # Method MultiplyAddEstimate(left : Vector128`1, right : Vector128`1, addend : Vector128`1) was skipped since it collides with above method

    # Skipped Narrow due to it being static, abstract and generic.

    Narrow : Narrow_MethodGroup
    class Narrow_MethodGroup:
        def __call__(self, lower: Vector128_1[float], upper: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Narrow(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method

    # Skipped NarrowWithSaturation due to it being static, abstract and generic.

    NarrowWithSaturation : NarrowWithSaturation_MethodGroup
    class NarrowWithSaturation_MethodGroup:
        def __call__(self, lower: Vector128_1[float], upper: Vector128_1[float]) -> Vector128_1[float]:...
        # Method NarrowWithSaturation(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method

    # Skipped Negate due to it being static, abstract and generic.

    Negate : Negate_MethodGroup
    class Negate_MethodGroup:
        def __getitem__(self, t:typing.Type[Negate_1_T1]) -> Negate_1[Negate_1_T1]: ...

        Negate_1_T1 = typing.TypeVar('Negate_1_T1')
        class Negate_1(typing.Generic[Negate_1_T1]):
            Negate_1_T = Vector128_0.Negate_MethodGroup.Negate_1_T1
            def __call__(self, vector: Vector128_1[Negate_1_T]) -> Vector128_1[Negate_1_T]:...


    # Skipped None due to it being static, abstract and generic.

    None : None_MethodGroup
    class None_MethodGroup:
        def __getitem__(self, t:typing.Type[None_1_T1]) -> None_1[None_1_T1]: ...

        None_1_T1 = typing.TypeVar('None_1_T1')
        class None_1(typing.Generic[None_1_T1]):
            None_1_T = Vector128_0.None_MethodGroup.None_1_T1
            def __call__(self, vector: Vector128_1[None_1_T], value: None_1_T) -> bool:...


    # Skipped NoneWhereAllBitsSet due to it being static, abstract and generic.

    NoneWhereAllBitsSet : NoneWhereAllBitsSet_MethodGroup
    class NoneWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[NoneWhereAllBitsSet_1_T1]) -> NoneWhereAllBitsSet_1[NoneWhereAllBitsSet_1_T1]: ...

        NoneWhereAllBitsSet_1_T1 = typing.TypeVar('NoneWhereAllBitsSet_1_T1')
        class NoneWhereAllBitsSet_1(typing.Generic[NoneWhereAllBitsSet_1_T1]):
            NoneWhereAllBitsSet_1_T = Vector128_0.NoneWhereAllBitsSet_MethodGroup.NoneWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector128_1[NoneWhereAllBitsSet_1_T]) -> bool:...


    # Skipped OnesComplement due to it being static, abstract and generic.

    OnesComplement : OnesComplement_MethodGroup
    class OnesComplement_MethodGroup:
        def __getitem__(self, t:typing.Type[OnesComplement_1_T1]) -> OnesComplement_1[OnesComplement_1_T1]: ...

        OnesComplement_1_T1 = typing.TypeVar('OnesComplement_1_T1')
        class OnesComplement_1(typing.Generic[OnesComplement_1_T1]):
            OnesComplement_1_T = Vector128_0.OnesComplement_MethodGroup.OnesComplement_1_T1
            def __call__(self, vector: Vector128_1[OnesComplement_1_T]) -> Vector128_1[OnesComplement_1_T]:...


    # Skipped RadiansToDegrees due to it being static, abstract and generic.

    RadiansToDegrees : RadiansToDegrees_MethodGroup
    class RadiansToDegrees_MethodGroup:
        def __call__(self, radians: Vector128_1[float]) -> Vector128_1[float]:...
        # Method RadiansToDegrees(radians : Vector128`1) was skipped since it collides with above method

    # Skipped Round due to it being static, abstract and generic.

    Round : Round_MethodGroup
    class Round_MethodGroup:
        @typing.overload
        def __call__(self, vector: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Round(vector : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, vector: Vector128_1[float], mode: MidpointRounding) -> Vector128_1[float]:...
        # Method Round(vector : Vector128`1, mode : MidpointRounding) was skipped since it collides with above method

    # Skipped ShiftLeft due to it being static, abstract and generic.

    ShiftLeft : ShiftLeft_MethodGroup
    class ShiftLeft_MethodGroup:
        @typing.overload
        def __call__(self, vector: Vector128_1[int], shiftCount: int) -> Vector128_1[int]:...
        # Method ShiftLeft(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, vector: Vector128_1[UIntPtr], shiftCount: int) -> Vector128_1[UIntPtr]:...

    # Skipped ShiftRightArithmetic due to it being static, abstract and generic.

    ShiftRightArithmetic : ShiftRightArithmetic_MethodGroup
    class ShiftRightArithmetic_MethodGroup:
        def __call__(self, vector: Vector128_1[int], shiftCount: int) -> Vector128_1[int]:...
        # Method ShiftRightArithmetic(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightArithmetic(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightArithmetic(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightArithmetic(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method

    # Skipped ShiftRightLogical due to it being static, abstract and generic.

    ShiftRightLogical : ShiftRightLogical_MethodGroup
    class ShiftRightLogical_MethodGroup:
        @typing.overload
        def __call__(self, vector: Vector128_1[int], shiftCount: int) -> Vector128_1[int]:...
        # Method ShiftRightLogical(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector128`1, shiftCount : Int32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, vector: Vector128_1[UIntPtr], shiftCount: int) -> Vector128_1[UIntPtr]:...

    # Skipped Shuffle due to it being static, abstract and generic.

    Shuffle : Shuffle_MethodGroup
    class Shuffle_MethodGroup:
        def __call__(self, vector: Vector128_1[float], indices: Vector128_1[int]) -> Vector128_1[float]:...
        # Method Shuffle(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method

    # Skipped ShuffleNative due to it being static, abstract and generic.

    ShuffleNative : ShuffleNative_MethodGroup
    class ShuffleNative_MethodGroup:
        def __call__(self, vector: Vector128_1[float], indices: Vector128_1[int]) -> Vector128_1[float]:...
        # Method ShuffleNative(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector128`1, indices : Vector128`1) was skipped since it collides with above method

    # Skipped Sin due to it being static, abstract and generic.

    Sin : Sin_MethodGroup
    class Sin_MethodGroup:
        def __call__(self, vector: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Sin(vector : Vector128`1) was skipped since it collides with above method

    # Skipped SinCos due to it being static, abstract and generic.

    SinCos : SinCos_MethodGroup
    class SinCos_MethodGroup:
        def __call__(self, vector: Vector128_1[float]) -> ValueTuple_2[Vector128_1[float], Vector128_1[float]]:...
        # Method SinCos(vector : Vector128`1) was skipped since it collides with above method

    # Skipped Sqrt due to it being static, abstract and generic.

    Sqrt : Sqrt_MethodGroup
    class Sqrt_MethodGroup:
        def __getitem__(self, t:typing.Type[Sqrt_1_T1]) -> Sqrt_1[Sqrt_1_T1]: ...

        Sqrt_1_T1 = typing.TypeVar('Sqrt_1_T1')
        class Sqrt_1(typing.Generic[Sqrt_1_T1]):
            Sqrt_1_T = Vector128_0.Sqrt_MethodGroup.Sqrt_1_T1
            def __call__(self, vector: Vector128_1[Sqrt_1_T]) -> Vector128_1[Sqrt_1_T]:...


    # Skipped Store due to it being static, abstract and generic.

    Store : Store_MethodGroup
    class Store_MethodGroup:
        def __getitem__(self, t:typing.Type[Store_1_T1]) -> Store_1[Store_1_T1]: ...

        Store_1_T1 = typing.TypeVar('Store_1_T1')
        class Store_1(typing.Generic[Store_1_T1]):
            Store_1_T = Vector128_0.Store_MethodGroup.Store_1_T1
            def __call__(self, source: Vector128_1[Store_1_T], destination: clr.Reference[Store_1_T]) -> None:...


    # Skipped StoreAligned due to it being static, abstract and generic.

    StoreAligned : StoreAligned_MethodGroup
    class StoreAligned_MethodGroup:
        def __getitem__(self, t:typing.Type[StoreAligned_1_T1]) -> StoreAligned_1[StoreAligned_1_T1]: ...

        StoreAligned_1_T1 = typing.TypeVar('StoreAligned_1_T1')
        class StoreAligned_1(typing.Generic[StoreAligned_1_T1]):
            StoreAligned_1_T = Vector128_0.StoreAligned_MethodGroup.StoreAligned_1_T1
            def __call__(self, source: Vector128_1[StoreAligned_1_T], destination: clr.Reference[StoreAligned_1_T]) -> None:...


    # Skipped StoreAlignedNonTemporal due to it being static, abstract and generic.

    StoreAlignedNonTemporal : StoreAlignedNonTemporal_MethodGroup
    class StoreAlignedNonTemporal_MethodGroup:
        def __getitem__(self, t:typing.Type[StoreAlignedNonTemporal_1_T1]) -> StoreAlignedNonTemporal_1[StoreAlignedNonTemporal_1_T1]: ...

        StoreAlignedNonTemporal_1_T1 = typing.TypeVar('StoreAlignedNonTemporal_1_T1')
        class StoreAlignedNonTemporal_1(typing.Generic[StoreAlignedNonTemporal_1_T1]):
            StoreAlignedNonTemporal_1_T = Vector128_0.StoreAlignedNonTemporal_MethodGroup.StoreAlignedNonTemporal_1_T1
            def __call__(self, source: Vector128_1[StoreAlignedNonTemporal_1_T], destination: clr.Reference[StoreAlignedNonTemporal_1_T]) -> None:...


    # Skipped StoreUnsafe due to it being static, abstract and generic.

    StoreUnsafe : StoreUnsafe_MethodGroup
    class StoreUnsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[StoreUnsafe_1_T1]) -> StoreUnsafe_1[StoreUnsafe_1_T1]: ...

        StoreUnsafe_1_T1 = typing.TypeVar('StoreUnsafe_1_T1')
        class StoreUnsafe_1(typing.Generic[StoreUnsafe_1_T1]):
            StoreUnsafe_1_T = Vector128_0.StoreUnsafe_MethodGroup.StoreUnsafe_1_T1
            @typing.overload
            def __call__(self, source: Vector128_1[StoreUnsafe_1_T], destination: clr.Reference[StoreUnsafe_1_T]) -> None:...
            @typing.overload
            def __call__(self, source: Vector128_1[StoreUnsafe_1_T], destination: clr.Reference[StoreUnsafe_1_T], elementOffset: UIntPtr) -> None:...


    # Skipped Subtract due to it being static, abstract and generic.

    Subtract : Subtract_MethodGroup
    class Subtract_MethodGroup:
        def __getitem__(self, t:typing.Type[Subtract_1_T1]) -> Subtract_1[Subtract_1_T1]: ...

        Subtract_1_T1 = typing.TypeVar('Subtract_1_T1')
        class Subtract_1(typing.Generic[Subtract_1_T1]):
            Subtract_1_T = Vector128_0.Subtract_MethodGroup.Subtract_1_T1
            def __call__(self, left: Vector128_1[Subtract_1_T], right: Vector128_1[Subtract_1_T]) -> Vector128_1[Subtract_1_T]:...


    # Skipped SubtractSaturate due to it being static, abstract and generic.

    SubtractSaturate : SubtractSaturate_MethodGroup
    class SubtractSaturate_MethodGroup:
        def __getitem__(self, t:typing.Type[SubtractSaturate_1_T1]) -> SubtractSaturate_1[SubtractSaturate_1_T1]: ...

        SubtractSaturate_1_T1 = typing.TypeVar('SubtractSaturate_1_T1')
        class SubtractSaturate_1(typing.Generic[SubtractSaturate_1_T1]):
            SubtractSaturate_1_T = Vector128_0.SubtractSaturate_MethodGroup.SubtractSaturate_1_T1
            def __call__(self, left: Vector128_1[SubtractSaturate_1_T], right: Vector128_1[SubtractSaturate_1_T]) -> Vector128_1[SubtractSaturate_1_T]:...


    # Skipped Sum due to it being static, abstract and generic.

    Sum : Sum_MethodGroup
    class Sum_MethodGroup:
        def __getitem__(self, t:typing.Type[Sum_1_T1]) -> Sum_1[Sum_1_T1]: ...

        Sum_1_T1 = typing.TypeVar('Sum_1_T1')
        class Sum_1(typing.Generic[Sum_1_T1]):
            Sum_1_T = Vector128_0.Sum_MethodGroup.Sum_1_T1
            def __call__(self, vector: Vector128_1[Sum_1_T]) -> Sum_1_T:...


    # Skipped ToScalar due to it being static, abstract and generic.

    ToScalar : ToScalar_MethodGroup
    class ToScalar_MethodGroup:
        def __getitem__(self, t:typing.Type[ToScalar_1_T1]) -> ToScalar_1[ToScalar_1_T1]: ...

        ToScalar_1_T1 = typing.TypeVar('ToScalar_1_T1')
        class ToScalar_1(typing.Generic[ToScalar_1_T1]):
            ToScalar_1_T = Vector128_0.ToScalar_MethodGroup.ToScalar_1_T1
            def __call__(self, vector: Vector128_1[ToScalar_1_T]) -> ToScalar_1_T:...


    # Skipped ToVector256 due to it being static, abstract and generic.

    ToVector256 : ToVector256_MethodGroup
    class ToVector256_MethodGroup:
        def __getitem__(self, t:typing.Type[ToVector256_1_T1]) -> ToVector256_1[ToVector256_1_T1]: ...

        ToVector256_1_T1 = typing.TypeVar('ToVector256_1_T1')
        class ToVector256_1(typing.Generic[ToVector256_1_T1]):
            ToVector256_1_T = Vector128_0.ToVector256_MethodGroup.ToVector256_1_T1
            def __call__(self, vector: Vector128_1[ToVector256_1_T]) -> Vector256_1[ToVector256_1_T]:...


    # Skipped ToVector256Unsafe due to it being static, abstract and generic.

    ToVector256Unsafe : ToVector256Unsafe_MethodGroup
    class ToVector256Unsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[ToVector256Unsafe_1_T1]) -> ToVector256Unsafe_1[ToVector256Unsafe_1_T1]: ...

        ToVector256Unsafe_1_T1 = typing.TypeVar('ToVector256Unsafe_1_T1')
        class ToVector256Unsafe_1(typing.Generic[ToVector256Unsafe_1_T1]):
            ToVector256Unsafe_1_T = Vector128_0.ToVector256Unsafe_MethodGroup.ToVector256Unsafe_1_T1
            def __call__(self, vector: Vector128_1[ToVector256Unsafe_1_T]) -> Vector256_1[ToVector256Unsafe_1_T]:...


    # Skipped Truncate due to it being static, abstract and generic.

    Truncate : Truncate_MethodGroup
    class Truncate_MethodGroup:
        def __call__(self, vector: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Truncate(vector : Vector128`1) was skipped since it collides with above method

    # Skipped TryCopyTo due to it being static, abstract and generic.

    TryCopyTo : TryCopyTo_MethodGroup
    class TryCopyTo_MethodGroup:
        def __getitem__(self, t:typing.Type[TryCopyTo_1_T1]) -> TryCopyTo_1[TryCopyTo_1_T1]: ...

        TryCopyTo_1_T1 = typing.TypeVar('TryCopyTo_1_T1')
        class TryCopyTo_1(typing.Generic[TryCopyTo_1_T1]):
            TryCopyTo_1_T = Vector128_0.TryCopyTo_MethodGroup.TryCopyTo_1_T1
            def __call__(self, vector: Vector128_1[TryCopyTo_1_T], destination: Span_1[TryCopyTo_1_T]) -> bool:...


    # Skipped Widen due to it being static, abstract and generic.

    Widen : Widen_MethodGroup
    class Widen_MethodGroup:
        def __call__(self, source: Vector128_1[float]) -> ValueTuple_2[Vector128_1[float], Vector128_1[float]]:...
        # Method Widen(source : Vector128`1) was skipped since it collides with above method
        # Method Widen(source : Vector128`1) was skipped since it collides with above method
        # Method Widen(source : Vector128`1) was skipped since it collides with above method
        # Method Widen(source : Vector128`1) was skipped since it collides with above method
        # Method Widen(source : Vector128`1) was skipped since it collides with above method
        # Method Widen(source : Vector128`1) was skipped since it collides with above method

    # Skipped WidenLower due to it being static, abstract and generic.

    WidenLower : WidenLower_MethodGroup
    class WidenLower_MethodGroup:
        def __call__(self, source: Vector128_1[float]) -> Vector128_1[float]:...
        # Method WidenLower(source : Vector128`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector128`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector128`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector128`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector128`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector128`1) was skipped since it collides with above method

    # Skipped WidenUpper due to it being static, abstract and generic.

    WidenUpper : WidenUpper_MethodGroup
    class WidenUpper_MethodGroup:
        def __call__(self, source: Vector128_1[float]) -> Vector128_1[float]:...
        # Method WidenUpper(source : Vector128`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector128`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector128`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector128`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector128`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector128`1) was skipped since it collides with above method

    # Skipped WithElement due to it being static, abstract and generic.

    WithElement : WithElement_MethodGroup
    class WithElement_MethodGroup:
        def __getitem__(self, t:typing.Type[WithElement_1_T1]) -> WithElement_1[WithElement_1_T1]: ...

        WithElement_1_T1 = typing.TypeVar('WithElement_1_T1')
        class WithElement_1(typing.Generic[WithElement_1_T1]):
            WithElement_1_T = Vector128_0.WithElement_MethodGroup.WithElement_1_T1
            def __call__(self, vector: Vector128_1[WithElement_1_T], index: int, value: WithElement_1_T) -> Vector128_1[WithElement_1_T]:...


    # Skipped WithLower due to it being static, abstract and generic.

    WithLower : WithLower_MethodGroup
    class WithLower_MethodGroup:
        def __getitem__(self, t:typing.Type[WithLower_1_T1]) -> WithLower_1[WithLower_1_T1]: ...

        WithLower_1_T1 = typing.TypeVar('WithLower_1_T1')
        class WithLower_1(typing.Generic[WithLower_1_T1]):
            WithLower_1_T = Vector128_0.WithLower_MethodGroup.WithLower_1_T1
            def __call__(self, vector: Vector128_1[WithLower_1_T], value: Vector64_1[WithLower_1_T]) -> Vector128_1[WithLower_1_T]:...


    # Skipped WithUpper due to it being static, abstract and generic.

    WithUpper : WithUpper_MethodGroup
    class WithUpper_MethodGroup:
        def __getitem__(self, t:typing.Type[WithUpper_1_T1]) -> WithUpper_1[WithUpper_1_T1]: ...

        WithUpper_1_T1 = typing.TypeVar('WithUpper_1_T1')
        class WithUpper_1(typing.Generic[WithUpper_1_T1]):
            WithUpper_1_T = Vector128_0.WithUpper_MethodGroup.WithUpper_1_T1
            def __call__(self, vector: Vector128_1[WithUpper_1_T], value: Vector64_1[WithUpper_1_T]) -> Vector128_1[WithUpper_1_T]:...


    # Skipped Xor due to it being static, abstract and generic.

    Xor : Xor_MethodGroup
    class Xor_MethodGroup:
        def __getitem__(self, t:typing.Type[Xor_1_T1]) -> Xor_1[Xor_1_T1]: ...

        Xor_1_T1 = typing.TypeVar('Xor_1_T1')
        class Xor_1(typing.Generic[Xor_1_T1]):
            Xor_1_T = Vector128_0.Xor_MethodGroup.Xor_1_T1
            def __call__(self, left: Vector128_1[Xor_1_T], right: Vector128_1[Xor_1_T]) -> Vector128_1[Xor_1_T]:...




Vector128_1_T = typing.TypeVar('Vector128_1_T')
class Vector128_1(typing.Generic[Vector128_1_T]):
    @classmethod
    @property
    def AllBitsSet(cls) -> Vector128_1[Vector128_1_T]: ...
    @classmethod
    @property
    def Count(cls) -> int: ...
    @classmethod
    @property
    def Indices(cls) -> Vector128_1[Vector128_1_T]: ...
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @property
    def Item(self) -> Vector128_1_T: ...
    @classmethod
    @property
    def One(cls) -> Vector128_1[Vector128_1_T]: ...
    @classmethod
    @property
    def Zero(cls) -> Vector128_1[Vector128_1_T]: ...
    def GetHashCode(self) -> int: ...
    def __add__(self, left: Vector128_1[Vector128_1_T], right: Vector128_1[Vector128_1_T]) -> Vector128_1[Vector128_1_T]: ...
    def __and__(self, left: Vector128_1[Vector128_1_T], right: Vector128_1[Vector128_1_T]) -> Vector128_1[Vector128_1_T]: ...
    def __or__(self, left: Vector128_1[Vector128_1_T], right: Vector128_1[Vector128_1_T]) -> Vector128_1[Vector128_1_T]: ...
    @typing.overload
    def __truediv__(self, left: Vector128_1[Vector128_1_T], right: Vector128_1[Vector128_1_T]) -> Vector128_1[Vector128_1_T]: ...
    @typing.overload
    def __truediv__(self, left: Vector128_1[Vector128_1_T], right: Vector128_1_T) -> Vector128_1[Vector128_1_T]: ...
    def __eq__(self, left: Vector128_1[Vector128_1_T], right: Vector128_1[Vector128_1_T]) -> bool: ...
    def __xor__(self, left: Vector128_1[Vector128_1_T], right: Vector128_1[Vector128_1_T]) -> Vector128_1[Vector128_1_T]: ...
    def __ne__(self, left: Vector128_1[Vector128_1_T], right: Vector128_1[Vector128_1_T]) -> bool: ...
    def __lshift__(self, value: Vector128_1[Vector128_1_T], shiftCount: int) -> Vector128_1[Vector128_1_T]: ...
    @typing.overload
    def __mul__(self, left: Vector128_1[Vector128_1_T], right: Vector128_1[Vector128_1_T]) -> Vector128_1[Vector128_1_T]: ...
    @typing.overload
    def __mul__(self, left: Vector128_1[Vector128_1_T], right: Vector128_1_T) -> Vector128_1[Vector128_1_T]: ...
    @typing.overload
    def __mul__(self, left: Vector128_1_T, right: Vector128_1[Vector128_1_T]) -> Vector128_1[Vector128_1_T]: ...
    def __invert__(self, vector: Vector128_1[Vector128_1_T]) -> Vector128_1[Vector128_1_T]: ...
    def __rshift__(self, value: Vector128_1[Vector128_1_T], shiftCount: int) -> Vector128_1[Vector128_1_T]: ...
    def __sub__(self, left: Vector128_1[Vector128_1_T], right: Vector128_1[Vector128_1_T]) -> Vector128_1[Vector128_1_T]: ...
    def __neg__(self, vector: Vector128_1[Vector128_1_T]) -> Vector128_1[Vector128_1_T]: ...
    def __pos__(self, value: Vector128_1[Vector128_1_T]) -> Vector128_1[Vector128_1_T]: ...
    # Operator not supported op_UnsignedRightShift(value: Vector128`1, shiftCount: Int32)
    def ToString(self) -> str: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup[Vector128_1_T]
    Equals_MethodGroup_Vector128_1_T = typing.TypeVar('Equals_MethodGroup_Vector128_1_T')
    class Equals_MethodGroup(typing.Generic[Equals_MethodGroup_Vector128_1_T]):
        Equals_MethodGroup_Vector128_1_T = Vector128_1.Equals_MethodGroup_Vector128_1_T
        @typing.overload
        def __call__(self, other: Vector128_1[Equals_MethodGroup_Vector128_1_T]) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...



class Vector256_GenericClasses(abc.ABCMeta):
    Generic_Vector256_GenericClasses_Vector256_1_T = typing.TypeVar('Generic_Vector256_GenericClasses_Vector256_1_T')
    def __getitem__(self, types : typing.Type[Generic_Vector256_GenericClasses_Vector256_1_T]) -> typing.Type[Vector256_1[Generic_Vector256_GenericClasses_Vector256_1_T]]: ...

class Vector256(Vector256_0, metaclass =Vector256_GenericClasses): ...

class Vector256_0(abc.ABC):
    @classmethod
    @property
    def IsHardwareAccelerated(cls) -> bool: ...
    @staticmethod
    def ConvertToInt32(vector: Vector256_1[float]) -> Vector256_1[int]: ...
    @staticmethod
    def ConvertToInt32Native(vector: Vector256_1[float]) -> Vector256_1[int]: ...
    @staticmethod
    def ConvertToInt64(vector: Vector256_1[float]) -> Vector256_1[int]: ...
    @staticmethod
    def ConvertToInt64Native(vector: Vector256_1[float]) -> Vector256_1[int]: ...
    @staticmethod
    def ConvertToUInt32(vector: Vector256_1[float]) -> Vector256_1[int]: ...
    @staticmethod
    def ConvertToUInt32Native(vector: Vector256_1[float]) -> Vector256_1[int]: ...
    @staticmethod
    def ConvertToUInt64(vector: Vector256_1[float]) -> Vector256_1[int]: ...
    @staticmethod
    def ConvertToUInt64Native(vector: Vector256_1[float]) -> Vector256_1[int]: ...
    # Skipped Abs due to it being static, abstract and generic.

    Abs : Abs_MethodGroup
    class Abs_MethodGroup:
        def __getitem__(self, t:typing.Type[Abs_1_T1]) -> Abs_1[Abs_1_T1]: ...

        Abs_1_T1 = typing.TypeVar('Abs_1_T1')
        class Abs_1(typing.Generic[Abs_1_T1]):
            Abs_1_T = Vector256_0.Abs_MethodGroup.Abs_1_T1
            def __call__(self, vector: Vector256_1[Abs_1_T]) -> Vector256_1[Abs_1_T]:...


    # Skipped Add due to it being static, abstract and generic.

    Add : Add_MethodGroup
    class Add_MethodGroup:
        def __getitem__(self, t:typing.Type[Add_1_T1]) -> Add_1[Add_1_T1]: ...

        Add_1_T1 = typing.TypeVar('Add_1_T1')
        class Add_1(typing.Generic[Add_1_T1]):
            Add_1_T = Vector256_0.Add_MethodGroup.Add_1_T1
            def __call__(self, left: Vector256_1[Add_1_T], right: Vector256_1[Add_1_T]) -> Vector256_1[Add_1_T]:...


    # Skipped AddSaturate due to it being static, abstract and generic.

    AddSaturate : AddSaturate_MethodGroup
    class AddSaturate_MethodGroup:
        def __getitem__(self, t:typing.Type[AddSaturate_1_T1]) -> AddSaturate_1[AddSaturate_1_T1]: ...

        AddSaturate_1_T1 = typing.TypeVar('AddSaturate_1_T1')
        class AddSaturate_1(typing.Generic[AddSaturate_1_T1]):
            AddSaturate_1_T = Vector256_0.AddSaturate_MethodGroup.AddSaturate_1_T1
            def __call__(self, left: Vector256_1[AddSaturate_1_T], right: Vector256_1[AddSaturate_1_T]) -> Vector256_1[AddSaturate_1_T]:...


    # Skipped All due to it being static, abstract and generic.

    All : All_MethodGroup
    class All_MethodGroup:
        def __getitem__(self, t:typing.Type[All_1_T1]) -> All_1[All_1_T1]: ...

        All_1_T1 = typing.TypeVar('All_1_T1')
        class All_1(typing.Generic[All_1_T1]):
            All_1_T = Vector256_0.All_MethodGroup.All_1_T1
            def __call__(self, vector: Vector256_1[All_1_T], value: All_1_T) -> bool:...


    # Skipped AllWhereAllBitsSet due to it being static, abstract and generic.

    AllWhereAllBitsSet : AllWhereAllBitsSet_MethodGroup
    class AllWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[AllWhereAllBitsSet_1_T1]) -> AllWhereAllBitsSet_1[AllWhereAllBitsSet_1_T1]: ...

        AllWhereAllBitsSet_1_T1 = typing.TypeVar('AllWhereAllBitsSet_1_T1')
        class AllWhereAllBitsSet_1(typing.Generic[AllWhereAllBitsSet_1_T1]):
            AllWhereAllBitsSet_1_T = Vector256_0.AllWhereAllBitsSet_MethodGroup.AllWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector256_1[AllWhereAllBitsSet_1_T]) -> bool:...


    # Skipped AndNot due to it being static, abstract and generic.

    AndNot : AndNot_MethodGroup
    class AndNot_MethodGroup:
        def __getitem__(self, t:typing.Type[AndNot_1_T1]) -> AndNot_1[AndNot_1_T1]: ...

        AndNot_1_T1 = typing.TypeVar('AndNot_1_T1')
        class AndNot_1(typing.Generic[AndNot_1_T1]):
            AndNot_1_T = Vector256_0.AndNot_MethodGroup.AndNot_1_T1
            def __call__(self, left: Vector256_1[AndNot_1_T], right: Vector256_1[AndNot_1_T]) -> Vector256_1[AndNot_1_T]:...


    # Skipped Any due to it being static, abstract and generic.

    Any : Any_MethodGroup
    class Any_MethodGroup:
        def __getitem__(self, t:typing.Type[Any_1_T1]) -> Any_1[Any_1_T1]: ...

        Any_1_T1 = typing.TypeVar('Any_1_T1')
        class Any_1(typing.Generic[Any_1_T1]):
            Any_1_T = Vector256_0.Any_MethodGroup.Any_1_T1
            def __call__(self, vector: Vector256_1[Any_1_T], value: Any_1_T) -> bool:...


    # Skipped AnyWhereAllBitsSet due to it being static, abstract and generic.

    AnyWhereAllBitsSet : AnyWhereAllBitsSet_MethodGroup
    class AnyWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[AnyWhereAllBitsSet_1_T1]) -> AnyWhereAllBitsSet_1[AnyWhereAllBitsSet_1_T1]: ...

        AnyWhereAllBitsSet_1_T1 = typing.TypeVar('AnyWhereAllBitsSet_1_T1')
        class AnyWhereAllBitsSet_1(typing.Generic[AnyWhereAllBitsSet_1_T1]):
            AnyWhereAllBitsSet_1_T = Vector256_0.AnyWhereAllBitsSet_MethodGroup.AnyWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector256_1[AnyWhereAllBitsSet_1_T]) -> bool:...


    # Skipped As due to it being static, abstract and generic.

    As : As_MethodGroup
    class As_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[As_2_T1], typing.Type[As_2_T2]]) -> As_2[As_2_T1, As_2_T2]: ...

        As_2_T1 = typing.TypeVar('As_2_T1')
        As_2_T2 = typing.TypeVar('As_2_T2')
        class As_2(typing.Generic[As_2_T1, As_2_T2]):
            As_2_TFrom = Vector256_0.As_MethodGroup.As_2_T1
            As_2_TTo = Vector256_0.As_MethodGroup.As_2_T2
            def __call__(self, vector: Vector256_1[As_2_TFrom]) -> Vector256_1[As_2_TTo]:...


    # Skipped AsByte due to it being static, abstract and generic.

    AsByte : AsByte_MethodGroup
    class AsByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsByte_1_T1]) -> AsByte_1[AsByte_1_T1]: ...

        AsByte_1_T1 = typing.TypeVar('AsByte_1_T1')
        class AsByte_1(typing.Generic[AsByte_1_T1]):
            AsByte_1_T = Vector256_0.AsByte_MethodGroup.AsByte_1_T1
            def __call__(self, vector: Vector256_1[AsByte_1_T]) -> Vector256_1[int]:...


    # Skipped AsDouble due to it being static, abstract and generic.

    AsDouble : AsDouble_MethodGroup
    class AsDouble_MethodGroup:
        def __getitem__(self, t:typing.Type[AsDouble_1_T1]) -> AsDouble_1[AsDouble_1_T1]: ...

        AsDouble_1_T1 = typing.TypeVar('AsDouble_1_T1')
        class AsDouble_1(typing.Generic[AsDouble_1_T1]):
            AsDouble_1_T = Vector256_0.AsDouble_MethodGroup.AsDouble_1_T1
            def __call__(self, vector: Vector256_1[AsDouble_1_T]) -> Vector256_1[float]:...


    # Skipped AsInt16 due to it being static, abstract and generic.

    AsInt16 : AsInt16_MethodGroup
    class AsInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt16_1_T1]) -> AsInt16_1[AsInt16_1_T1]: ...

        AsInt16_1_T1 = typing.TypeVar('AsInt16_1_T1')
        class AsInt16_1(typing.Generic[AsInt16_1_T1]):
            AsInt16_1_T = Vector256_0.AsInt16_MethodGroup.AsInt16_1_T1
            def __call__(self, vector: Vector256_1[AsInt16_1_T]) -> Vector256_1[int]:...


    # Skipped AsInt32 due to it being static, abstract and generic.

    AsInt32 : AsInt32_MethodGroup
    class AsInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt32_1_T1]) -> AsInt32_1[AsInt32_1_T1]: ...

        AsInt32_1_T1 = typing.TypeVar('AsInt32_1_T1')
        class AsInt32_1(typing.Generic[AsInt32_1_T1]):
            AsInt32_1_T = Vector256_0.AsInt32_MethodGroup.AsInt32_1_T1
            def __call__(self, vector: Vector256_1[AsInt32_1_T]) -> Vector256_1[int]:...


    # Skipped AsInt64 due to it being static, abstract and generic.

    AsInt64 : AsInt64_MethodGroup
    class AsInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt64_1_T1]) -> AsInt64_1[AsInt64_1_T1]: ...

        AsInt64_1_T1 = typing.TypeVar('AsInt64_1_T1')
        class AsInt64_1(typing.Generic[AsInt64_1_T1]):
            AsInt64_1_T = Vector256_0.AsInt64_MethodGroup.AsInt64_1_T1
            def __call__(self, vector: Vector256_1[AsInt64_1_T]) -> Vector256_1[int]:...


    # Skipped AsNInt due to it being static, abstract and generic.

    AsNInt : AsNInt_MethodGroup
    class AsNInt_MethodGroup:
        def __getitem__(self, t:typing.Type[AsNInt_1_T1]) -> AsNInt_1[AsNInt_1_T1]: ...

        AsNInt_1_T1 = typing.TypeVar('AsNInt_1_T1')
        class AsNInt_1(typing.Generic[AsNInt_1_T1]):
            AsNInt_1_T = Vector256_0.AsNInt_MethodGroup.AsNInt_1_T1
            def __call__(self, vector: Vector256_1[AsNInt_1_T]) -> Vector256_1[int]:...


    # Skipped AsNUInt due to it being static, abstract and generic.

    AsNUInt : AsNUInt_MethodGroup
    class AsNUInt_MethodGroup:
        def __getitem__(self, t:typing.Type[AsNUInt_1_T1]) -> AsNUInt_1[AsNUInt_1_T1]: ...

        AsNUInt_1_T1 = typing.TypeVar('AsNUInt_1_T1')
        class AsNUInt_1(typing.Generic[AsNUInt_1_T1]):
            AsNUInt_1_T = Vector256_0.AsNUInt_MethodGroup.AsNUInt_1_T1
            def __call__(self, vector: Vector256_1[AsNUInt_1_T]) -> Vector256_1[UIntPtr]:...


    # Skipped AsSByte due to it being static, abstract and generic.

    AsSByte : AsSByte_MethodGroup
    class AsSByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsSByte_1_T1]) -> AsSByte_1[AsSByte_1_T1]: ...

        AsSByte_1_T1 = typing.TypeVar('AsSByte_1_T1')
        class AsSByte_1(typing.Generic[AsSByte_1_T1]):
            AsSByte_1_T = Vector256_0.AsSByte_MethodGroup.AsSByte_1_T1
            def __call__(self, vector: Vector256_1[AsSByte_1_T]) -> Vector256_1[int]:...


    # Skipped AsSingle due to it being static, abstract and generic.

    AsSingle : AsSingle_MethodGroup
    class AsSingle_MethodGroup:
        def __getitem__(self, t:typing.Type[AsSingle_1_T1]) -> AsSingle_1[AsSingle_1_T1]: ...

        AsSingle_1_T1 = typing.TypeVar('AsSingle_1_T1')
        class AsSingle_1(typing.Generic[AsSingle_1_T1]):
            AsSingle_1_T = Vector256_0.AsSingle_MethodGroup.AsSingle_1_T1
            def __call__(self, vector: Vector256_1[AsSingle_1_T]) -> Vector256_1[float]:...


    # Skipped AsUInt16 due to it being static, abstract and generic.

    AsUInt16 : AsUInt16_MethodGroup
    class AsUInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt16_1_T1]) -> AsUInt16_1[AsUInt16_1_T1]: ...

        AsUInt16_1_T1 = typing.TypeVar('AsUInt16_1_T1')
        class AsUInt16_1(typing.Generic[AsUInt16_1_T1]):
            AsUInt16_1_T = Vector256_0.AsUInt16_MethodGroup.AsUInt16_1_T1
            def __call__(self, vector: Vector256_1[AsUInt16_1_T]) -> Vector256_1[int]:...


    # Skipped AsUInt32 due to it being static, abstract and generic.

    AsUInt32 : AsUInt32_MethodGroup
    class AsUInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt32_1_T1]) -> AsUInt32_1[AsUInt32_1_T1]: ...

        AsUInt32_1_T1 = typing.TypeVar('AsUInt32_1_T1')
        class AsUInt32_1(typing.Generic[AsUInt32_1_T1]):
            AsUInt32_1_T = Vector256_0.AsUInt32_MethodGroup.AsUInt32_1_T1
            def __call__(self, vector: Vector256_1[AsUInt32_1_T]) -> Vector256_1[int]:...


    # Skipped AsUInt64 due to it being static, abstract and generic.

    AsUInt64 : AsUInt64_MethodGroup
    class AsUInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt64_1_T1]) -> AsUInt64_1[AsUInt64_1_T1]: ...

        AsUInt64_1_T1 = typing.TypeVar('AsUInt64_1_T1')
        class AsUInt64_1(typing.Generic[AsUInt64_1_T1]):
            AsUInt64_1_T = Vector256_0.AsUInt64_MethodGroup.AsUInt64_1_T1
            def __call__(self, vector: Vector256_1[AsUInt64_1_T]) -> Vector256_1[int]:...


    # Skipped AsVector due to it being static, abstract and generic.

    AsVector : AsVector_MethodGroup
    class AsVector_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVector_1_T1]) -> AsVector_1[AsVector_1_T1]: ...

        AsVector_1_T1 = typing.TypeVar('AsVector_1_T1')
        class AsVector_1(typing.Generic[AsVector_1_T1]):
            AsVector_1_T = Vector256_0.AsVector_MethodGroup.AsVector_1_T1
            def __call__(self, value: Vector256_1[AsVector_1_T]) -> Vector_1[AsVector_1_T]:...


    # Skipped AsVector256 due to it being static, abstract and generic.

    AsVector256 : AsVector256_MethodGroup
    class AsVector256_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVector256_1_T1]) -> AsVector256_1[AsVector256_1_T1]: ...

        AsVector256_1_T1 = typing.TypeVar('AsVector256_1_T1')
        class AsVector256_1(typing.Generic[AsVector256_1_T1]):
            AsVector256_1_T = Vector256_0.AsVector256_MethodGroup.AsVector256_1_T1
            def __call__(self, value: Vector_1[AsVector256_1_T]) -> Vector256_1[AsVector256_1_T]:...


    # Skipped BitwiseAnd due to it being static, abstract and generic.

    BitwiseAnd : BitwiseAnd_MethodGroup
    class BitwiseAnd_MethodGroup:
        def __getitem__(self, t:typing.Type[BitwiseAnd_1_T1]) -> BitwiseAnd_1[BitwiseAnd_1_T1]: ...

        BitwiseAnd_1_T1 = typing.TypeVar('BitwiseAnd_1_T1')
        class BitwiseAnd_1(typing.Generic[BitwiseAnd_1_T1]):
            BitwiseAnd_1_T = Vector256_0.BitwiseAnd_MethodGroup.BitwiseAnd_1_T1
            def __call__(self, left: Vector256_1[BitwiseAnd_1_T], right: Vector256_1[BitwiseAnd_1_T]) -> Vector256_1[BitwiseAnd_1_T]:...


    # Skipped BitwiseOr due to it being static, abstract and generic.

    BitwiseOr : BitwiseOr_MethodGroup
    class BitwiseOr_MethodGroup:
        def __getitem__(self, t:typing.Type[BitwiseOr_1_T1]) -> BitwiseOr_1[BitwiseOr_1_T1]: ...

        BitwiseOr_1_T1 = typing.TypeVar('BitwiseOr_1_T1')
        class BitwiseOr_1(typing.Generic[BitwiseOr_1_T1]):
            BitwiseOr_1_T = Vector256_0.BitwiseOr_MethodGroup.BitwiseOr_1_T1
            def __call__(self, left: Vector256_1[BitwiseOr_1_T], right: Vector256_1[BitwiseOr_1_T]) -> Vector256_1[BitwiseOr_1_T]:...


    # Skipped Ceiling due to it being static, abstract and generic.

    Ceiling : Ceiling_MethodGroup
    class Ceiling_MethodGroup:
        def __call__(self, vector: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Ceiling(vector : Vector256`1) was skipped since it collides with above method

    # Skipped Clamp due to it being static, abstract and generic.

    Clamp : Clamp_MethodGroup
    class Clamp_MethodGroup:
        def __getitem__(self, t:typing.Type[Clamp_1_T1]) -> Clamp_1[Clamp_1_T1]: ...

        Clamp_1_T1 = typing.TypeVar('Clamp_1_T1')
        class Clamp_1(typing.Generic[Clamp_1_T1]):
            Clamp_1_T = Vector256_0.Clamp_MethodGroup.Clamp_1_T1
            def __call__(self, value: Vector256_1[Clamp_1_T], min: Vector256_1[Clamp_1_T], max: Vector256_1[Clamp_1_T]) -> Vector256_1[Clamp_1_T]:...


    # Skipped ClampNative due to it being static, abstract and generic.

    ClampNative : ClampNative_MethodGroup
    class ClampNative_MethodGroup:
        def __getitem__(self, t:typing.Type[ClampNative_1_T1]) -> ClampNative_1[ClampNative_1_T1]: ...

        ClampNative_1_T1 = typing.TypeVar('ClampNative_1_T1')
        class ClampNative_1(typing.Generic[ClampNative_1_T1]):
            ClampNative_1_T = Vector256_0.ClampNative_MethodGroup.ClampNative_1_T1
            def __call__(self, value: Vector256_1[ClampNative_1_T], min: Vector256_1[ClampNative_1_T], max: Vector256_1[ClampNative_1_T]) -> Vector256_1[ClampNative_1_T]:...


    # Skipped ConditionalSelect due to it being static, abstract and generic.

    ConditionalSelect : ConditionalSelect_MethodGroup
    class ConditionalSelect_MethodGroup:
        def __getitem__(self, t:typing.Type[ConditionalSelect_1_T1]) -> ConditionalSelect_1[ConditionalSelect_1_T1]: ...

        ConditionalSelect_1_T1 = typing.TypeVar('ConditionalSelect_1_T1')
        class ConditionalSelect_1(typing.Generic[ConditionalSelect_1_T1]):
            ConditionalSelect_1_T = Vector256_0.ConditionalSelect_MethodGroup.ConditionalSelect_1_T1
            def __call__(self, condition: Vector256_1[ConditionalSelect_1_T], left: Vector256_1[ConditionalSelect_1_T], right: Vector256_1[ConditionalSelect_1_T]) -> Vector256_1[ConditionalSelect_1_T]:...


    # Skipped ConvertToDouble due to it being static, abstract and generic.

    ConvertToDouble : ConvertToDouble_MethodGroup
    class ConvertToDouble_MethodGroup:
        def __call__(self, vector: Vector256_1[int]) -> Vector256_1[float]:...
        # Method ConvertToDouble(vector : Vector256`1) was skipped since it collides with above method

    # Skipped ConvertToSingle due to it being static, abstract and generic.

    ConvertToSingle : ConvertToSingle_MethodGroup
    class ConvertToSingle_MethodGroup:
        def __call__(self, vector: Vector256_1[int]) -> Vector256_1[float]:...
        # Method ConvertToSingle(vector : Vector256`1) was skipped since it collides with above method

    # Skipped CopySign due to it being static, abstract and generic.

    CopySign : CopySign_MethodGroup
    class CopySign_MethodGroup:
        def __getitem__(self, t:typing.Type[CopySign_1_T1]) -> CopySign_1[CopySign_1_T1]: ...

        CopySign_1_T1 = typing.TypeVar('CopySign_1_T1')
        class CopySign_1(typing.Generic[CopySign_1_T1]):
            CopySign_1_T = Vector256_0.CopySign_MethodGroup.CopySign_1_T1
            def __call__(self, value: Vector256_1[CopySign_1_T], sign: Vector256_1[CopySign_1_T]) -> Vector256_1[CopySign_1_T]:...


    # Skipped CopyTo due to it being static, abstract and generic.

    CopyTo : CopyTo_MethodGroup
    class CopyTo_MethodGroup:
        def __getitem__(self, t:typing.Type[CopyTo_1_T1]) -> CopyTo_1[CopyTo_1_T1]: ...

        CopyTo_1_T1 = typing.TypeVar('CopyTo_1_T1')
        class CopyTo_1(typing.Generic[CopyTo_1_T1]):
            CopyTo_1_T = Vector256_0.CopyTo_MethodGroup.CopyTo_1_T1
            @typing.overload
            def __call__(self, vector: Vector256_1[CopyTo_1_T], destination: Array_1[CopyTo_1_T]) -> None:...
            @typing.overload
            def __call__(self, vector: Vector256_1[CopyTo_1_T], destination: Span_1[CopyTo_1_T]) -> None:...
            @typing.overload
            def __call__(self, vector: Vector256_1[CopyTo_1_T], destination: Array_1[CopyTo_1_T], startIndex: int) -> None:...


    # Skipped Cos due to it being static, abstract and generic.

    Cos : Cos_MethodGroup
    class Cos_MethodGroup:
        def __call__(self, vector: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Cos(vector : Vector256`1) was skipped since it collides with above method

    # Skipped Count due to it being static, abstract and generic.

    Count : Count_MethodGroup
    class Count_MethodGroup:
        def __getitem__(self, t:typing.Type[Count_1_T1]) -> Count_1[Count_1_T1]: ...

        Count_1_T1 = typing.TypeVar('Count_1_T1')
        class Count_1(typing.Generic[Count_1_T1]):
            Count_1_T = Vector256_0.Count_MethodGroup.Count_1_T1
            def __call__(self, vector: Vector256_1[Count_1_T], value: Count_1_T) -> int:...


    # Skipped CountWhereAllBitsSet due to it being static, abstract and generic.

    CountWhereAllBitsSet : CountWhereAllBitsSet_MethodGroup
    class CountWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[CountWhereAllBitsSet_1_T1]) -> CountWhereAllBitsSet_1[CountWhereAllBitsSet_1_T1]: ...

        CountWhereAllBitsSet_1_T1 = typing.TypeVar('CountWhereAllBitsSet_1_T1')
        class CountWhereAllBitsSet_1(typing.Generic[CountWhereAllBitsSet_1_T1]):
            CountWhereAllBitsSet_1_T = Vector256_0.CountWhereAllBitsSet_MethodGroup.CountWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector256_1[CountWhereAllBitsSet_1_T]) -> int:...


    # Skipped Create due to it being static, abstract and generic.

    Create : Create_MethodGroup
    class Create_MethodGroup:
        def __getitem__(self, t:typing.Type[Create_1_T1]) -> Create_1[Create_1_T1]: ...

        Create_1_T1 = typing.TypeVar('Create_1_T1')
        class Create_1(typing.Generic[Create_1_T1]):
            Create_1_T = Vector256_0.Create_MethodGroup.Create_1_T1
            @typing.overload
            def __call__(self, values: Array_1[Create_1_T]) -> Vector256_1[Create_1_T]:...
            @typing.overload
            def __call__(self, value: Vector64_1[Create_1_T]) -> Vector256_1[Create_1_T]:...
            @typing.overload
            def __call__(self, value: Vector128_1[Create_1_T]) -> Vector256_1[Create_1_T]:...
            @typing.overload
            def __call__(self, values: ReadOnlySpan_1[Create_1_T]) -> Vector256_1[Create_1_T]:...
            @typing.overload
            def __call__(self, value: Create_1_T) -> Vector256_1[Create_1_T]:...
            @typing.overload
            def __call__(self, values: Array_1[Create_1_T], index: int) -> Vector256_1[Create_1_T]:...
            @typing.overload
            def __call__(self, lower: Vector128_1[Create_1_T], upper: Vector128_1[Create_1_T]) -> Vector256_1[Create_1_T]:...

        @typing.overload
        def __call__(self, value: float) -> Vector256_1[float]:...
        # Method Create(value : Single) was skipped since it collides with above method
        # Method Create(value : Byte) was skipped since it collides with above method
        # Method Create(value : Int16) was skipped since it collides with above method
        # Method Create(value : Int32) was skipped since it collides with above method
        # Method Create(value : Int64) was skipped since it collides with above method
        # Method Create(value : SByte) was skipped since it collides with above method
        # Method Create(value : UInt16) was skipped since it collides with above method
        # Method Create(value : UInt32) was skipped since it collides with above method
        # Method Create(value : UInt64) was skipped since it collides with above method
        # Method Create(value : IntPtr) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: UIntPtr) -> Vector256_1[UIntPtr]:...
        @typing.overload
        def __call__(self, lower: Vector128_1[float], upper: Vector128_1[float]) -> Vector256_1[float]:...
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        # Method Create(lower : Vector128`1, upper : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, lower: Vector128_1[UIntPtr], upper: Vector128_1[UIntPtr]) -> Vector256_1[UIntPtr]:...
        @typing.overload
        def __call__(self, e0: float, e1: float, e2: float, e3: float) -> Vector256_1[float]:...
        # Method Create(e0 : Int64, e1 : Int64, e2 : Int64, e3 : Int64) was skipped since it collides with above method
        # Method Create(e0 : UInt64, e1 : UInt64, e2 : UInt64, e3 : UInt64) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: float, e1: float, e2: float, e3: float, e4: float, e5: float, e6: float, e7: float) -> Vector256_1[float]:...
        # Method Create(e0 : Int32, e1 : Int32, e2 : Int32, e3 : Int32, e4 : Int32, e5 : Int32, e6 : Int32, e7 : Int32) was skipped since it collides with above method
        # Method Create(e0 : UInt32, e1 : UInt32, e2 : UInt32, e3 : UInt32, e4 : UInt32, e5 : UInt32, e6 : UInt32, e7 : UInt32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int, e8: int, e9: int, e10: int, e11: int, e12: int, e13: int, e14: int, e15: int) -> Vector256_1[int]:...
        # Method Create(e0 : UInt16, e1 : UInt16, e2 : UInt16, e3 : UInt16, e4 : UInt16, e5 : UInt16, e6 : UInt16, e7 : UInt16, e8 : UInt16, e9 : UInt16, e10 : UInt16, e11 : UInt16, e12 : UInt16, e13 : UInt16, e14 : UInt16, e15 : UInt16) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int, e8: int, e9: int, e10: int, e11: int, e12: int, e13: int, e14: int, e15: int, e16: int, e17: int, e18: int, e19: int, e20: int, e21: int, e22: int, e23: int, e24: int, e25: int, e26: int, e27: int, e28: int, e29: int, e30: int, e31: int) -> Vector256_1[int]:...
        # Method Create(e0 : SByte, e1 : SByte, e2 : SByte, e3 : SByte, e4 : SByte, e5 : SByte, e6 : SByte, e7 : SByte, e8 : SByte, e9 : SByte, e10 : SByte, e11 : SByte, e12 : SByte, e13 : SByte, e14 : SByte, e15 : SByte, e16 : SByte, e17 : SByte, e18 : SByte, e19 : SByte, e20 : SByte, e21 : SByte, e22 : SByte, e23 : SByte, e24 : SByte, e25 : SByte, e26 : SByte, e27 : SByte, e28 : SByte, e29 : SByte, e30 : SByte, e31 : SByte) was skipped since it collides with above method

    # Skipped CreateScalar due to it being static, abstract and generic.

    CreateScalar : CreateScalar_MethodGroup
    class CreateScalar_MethodGroup:
        def __getitem__(self, t:typing.Type[CreateScalar_1_T1]) -> CreateScalar_1[CreateScalar_1_T1]: ...

        CreateScalar_1_T1 = typing.TypeVar('CreateScalar_1_T1')
        class CreateScalar_1(typing.Generic[CreateScalar_1_T1]):
            CreateScalar_1_T = Vector256_0.CreateScalar_MethodGroup.CreateScalar_1_T1
            def __call__(self, value: CreateScalar_1_T) -> Vector256_1[CreateScalar_1_T]:...

        @typing.overload
        def __call__(self, value: float) -> Vector256_1[float]:...
        # Method CreateScalar(value : Single) was skipped since it collides with above method
        # Method CreateScalar(value : Byte) was skipped since it collides with above method
        # Method CreateScalar(value : Int16) was skipped since it collides with above method
        # Method CreateScalar(value : Int32) was skipped since it collides with above method
        # Method CreateScalar(value : Int64) was skipped since it collides with above method
        # Method CreateScalar(value : SByte) was skipped since it collides with above method
        # Method CreateScalar(value : UInt16) was skipped since it collides with above method
        # Method CreateScalar(value : UInt32) was skipped since it collides with above method
        # Method CreateScalar(value : UInt64) was skipped since it collides with above method
        # Method CreateScalar(value : IntPtr) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: UIntPtr) -> Vector256_1[UIntPtr]:...

    # Skipped CreateScalarUnsafe due to it being static, abstract and generic.

    CreateScalarUnsafe : CreateScalarUnsafe_MethodGroup
    class CreateScalarUnsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[CreateScalarUnsafe_1_T1]) -> CreateScalarUnsafe_1[CreateScalarUnsafe_1_T1]: ...

        CreateScalarUnsafe_1_T1 = typing.TypeVar('CreateScalarUnsafe_1_T1')
        class CreateScalarUnsafe_1(typing.Generic[CreateScalarUnsafe_1_T1]):
            CreateScalarUnsafe_1_T = Vector256_0.CreateScalarUnsafe_MethodGroup.CreateScalarUnsafe_1_T1
            def __call__(self, value: CreateScalarUnsafe_1_T) -> Vector256_1[CreateScalarUnsafe_1_T]:...

        @typing.overload
        def __call__(self, value: float) -> Vector256_1[float]:...
        # Method CreateScalarUnsafe(value : Single) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Byte) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int16) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int32) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int64) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : SByte) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt16) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt32) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt64) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : IntPtr) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: UIntPtr) -> Vector256_1[UIntPtr]:...

    # Skipped CreateSequence due to it being static, abstract and generic.

    CreateSequence : CreateSequence_MethodGroup
    class CreateSequence_MethodGroup:
        def __getitem__(self, t:typing.Type[CreateSequence_1_T1]) -> CreateSequence_1[CreateSequence_1_T1]: ...

        CreateSequence_1_T1 = typing.TypeVar('CreateSequence_1_T1')
        class CreateSequence_1(typing.Generic[CreateSequence_1_T1]):
            CreateSequence_1_T = Vector256_0.CreateSequence_MethodGroup.CreateSequence_1_T1
            def __call__(self, start: CreateSequence_1_T, step: CreateSequence_1_T) -> Vector256_1[CreateSequence_1_T]:...


    # Skipped DegreesToRadians due to it being static, abstract and generic.

    DegreesToRadians : DegreesToRadians_MethodGroup
    class DegreesToRadians_MethodGroup:
        def __call__(self, degrees: Vector256_1[float]) -> Vector256_1[float]:...
        # Method DegreesToRadians(degrees : Vector256`1) was skipped since it collides with above method

    # Skipped Divide due to it being static, abstract and generic.

    Divide : Divide_MethodGroup
    class Divide_MethodGroup:
        def __getitem__(self, t:typing.Type[Divide_1_T1]) -> Divide_1[Divide_1_T1]: ...

        Divide_1_T1 = typing.TypeVar('Divide_1_T1')
        class Divide_1(typing.Generic[Divide_1_T1]):
            Divide_1_T = Vector256_0.Divide_MethodGroup.Divide_1_T1
            @typing.overload
            def __call__(self, left: Vector256_1[Divide_1_T], right: Vector256_1[Divide_1_T]) -> Vector256_1[Divide_1_T]:...
            @typing.overload
            def __call__(self, left: Vector256_1[Divide_1_T], right: Divide_1_T) -> Vector256_1[Divide_1_T]:...


    # Skipped Dot due to it being static, abstract and generic.

    Dot : Dot_MethodGroup
    class Dot_MethodGroup:
        def __getitem__(self, t:typing.Type[Dot_1_T1]) -> Dot_1[Dot_1_T1]: ...

        Dot_1_T1 = typing.TypeVar('Dot_1_T1')
        class Dot_1(typing.Generic[Dot_1_T1]):
            Dot_1_T = Vector256_0.Dot_MethodGroup.Dot_1_T1
            def __call__(self, left: Vector256_1[Dot_1_T], right: Vector256_1[Dot_1_T]) -> Dot_1_T:...


    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        def __getitem__(self, t:typing.Type[Equals_1_T1]) -> Equals_1[Equals_1_T1]: ...

        Equals_1_T1 = typing.TypeVar('Equals_1_T1')
        class Equals_1(typing.Generic[Equals_1_T1]):
            Equals_1_T = Vector256_0.Equals_MethodGroup.Equals_1_T1
            def __call__(self, left: Vector256_1[Equals_1_T], right: Vector256_1[Equals_1_T]) -> Vector256_1[Equals_1_T]:...


    # Skipped EqualsAll due to it being static, abstract and generic.

    EqualsAll : EqualsAll_MethodGroup
    class EqualsAll_MethodGroup:
        def __getitem__(self, t:typing.Type[EqualsAll_1_T1]) -> EqualsAll_1[EqualsAll_1_T1]: ...

        EqualsAll_1_T1 = typing.TypeVar('EqualsAll_1_T1')
        class EqualsAll_1(typing.Generic[EqualsAll_1_T1]):
            EqualsAll_1_T = Vector256_0.EqualsAll_MethodGroup.EqualsAll_1_T1
            def __call__(self, left: Vector256_1[EqualsAll_1_T], right: Vector256_1[EqualsAll_1_T]) -> bool:...


    # Skipped EqualsAny due to it being static, abstract and generic.

    EqualsAny : EqualsAny_MethodGroup
    class EqualsAny_MethodGroup:
        def __getitem__(self, t:typing.Type[EqualsAny_1_T1]) -> EqualsAny_1[EqualsAny_1_T1]: ...

        EqualsAny_1_T1 = typing.TypeVar('EqualsAny_1_T1')
        class EqualsAny_1(typing.Generic[EqualsAny_1_T1]):
            EqualsAny_1_T = Vector256_0.EqualsAny_MethodGroup.EqualsAny_1_T1
            def __call__(self, left: Vector256_1[EqualsAny_1_T], right: Vector256_1[EqualsAny_1_T]) -> bool:...


    # Skipped Exp due to it being static, abstract and generic.

    Exp : Exp_MethodGroup
    class Exp_MethodGroup:
        def __call__(self, vector: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Exp(vector : Vector256`1) was skipped since it collides with above method

    # Skipped ExtractMostSignificantBits due to it being static, abstract and generic.

    ExtractMostSignificantBits : ExtractMostSignificantBits_MethodGroup
    class ExtractMostSignificantBits_MethodGroup:
        def __getitem__(self, t:typing.Type[ExtractMostSignificantBits_1_T1]) -> ExtractMostSignificantBits_1[ExtractMostSignificantBits_1_T1]: ...

        ExtractMostSignificantBits_1_T1 = typing.TypeVar('ExtractMostSignificantBits_1_T1')
        class ExtractMostSignificantBits_1(typing.Generic[ExtractMostSignificantBits_1_T1]):
            ExtractMostSignificantBits_1_T = Vector256_0.ExtractMostSignificantBits_MethodGroup.ExtractMostSignificantBits_1_T1
            def __call__(self, vector: Vector256_1[ExtractMostSignificantBits_1_T]) -> int:...


    # Skipped Floor due to it being static, abstract and generic.

    Floor : Floor_MethodGroup
    class Floor_MethodGroup:
        def __call__(self, vector: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Floor(vector : Vector256`1) was skipped since it collides with above method

    # Skipped FusedMultiplyAdd due to it being static, abstract and generic.

    FusedMultiplyAdd : FusedMultiplyAdd_MethodGroup
    class FusedMultiplyAdd_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float], addend: Vector256_1[float]) -> Vector256_1[float]:...
        # Method FusedMultiplyAdd(left : Vector256`1, right : Vector256`1, addend : Vector256`1) was skipped since it collides with above method

    # Skipped GetElement due to it being static, abstract and generic.

    GetElement : GetElement_MethodGroup
    class GetElement_MethodGroup:
        def __getitem__(self, t:typing.Type[GetElement_1_T1]) -> GetElement_1[GetElement_1_T1]: ...

        GetElement_1_T1 = typing.TypeVar('GetElement_1_T1')
        class GetElement_1(typing.Generic[GetElement_1_T1]):
            GetElement_1_T = Vector256_0.GetElement_MethodGroup.GetElement_1_T1
            def __call__(self, vector: Vector256_1[GetElement_1_T], index: int) -> GetElement_1_T:...


    # Skipped GetLower due to it being static, abstract and generic.

    GetLower : GetLower_MethodGroup
    class GetLower_MethodGroup:
        def __getitem__(self, t:typing.Type[GetLower_1_T1]) -> GetLower_1[GetLower_1_T1]: ...

        GetLower_1_T1 = typing.TypeVar('GetLower_1_T1')
        class GetLower_1(typing.Generic[GetLower_1_T1]):
            GetLower_1_T = Vector256_0.GetLower_MethodGroup.GetLower_1_T1
            def __call__(self, vector: Vector256_1[GetLower_1_T]) -> Vector128_1[GetLower_1_T]:...


    # Skipped GetUpper due to it being static, abstract and generic.

    GetUpper : GetUpper_MethodGroup
    class GetUpper_MethodGroup:
        def __getitem__(self, t:typing.Type[GetUpper_1_T1]) -> GetUpper_1[GetUpper_1_T1]: ...

        GetUpper_1_T1 = typing.TypeVar('GetUpper_1_T1')
        class GetUpper_1(typing.Generic[GetUpper_1_T1]):
            GetUpper_1_T = Vector256_0.GetUpper_MethodGroup.GetUpper_1_T1
            def __call__(self, vector: Vector256_1[GetUpper_1_T]) -> Vector128_1[GetUpper_1_T]:...


    # Skipped GreaterThan due to it being static, abstract and generic.

    GreaterThan : GreaterThan_MethodGroup
    class GreaterThan_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThan_1_T1]) -> GreaterThan_1[GreaterThan_1_T1]: ...

        GreaterThan_1_T1 = typing.TypeVar('GreaterThan_1_T1')
        class GreaterThan_1(typing.Generic[GreaterThan_1_T1]):
            GreaterThan_1_T = Vector256_0.GreaterThan_MethodGroup.GreaterThan_1_T1
            def __call__(self, left: Vector256_1[GreaterThan_1_T], right: Vector256_1[GreaterThan_1_T]) -> Vector256_1[GreaterThan_1_T]:...


    # Skipped GreaterThanAll due to it being static, abstract and generic.

    GreaterThanAll : GreaterThanAll_MethodGroup
    class GreaterThanAll_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanAll_1_T1]) -> GreaterThanAll_1[GreaterThanAll_1_T1]: ...

        GreaterThanAll_1_T1 = typing.TypeVar('GreaterThanAll_1_T1')
        class GreaterThanAll_1(typing.Generic[GreaterThanAll_1_T1]):
            GreaterThanAll_1_T = Vector256_0.GreaterThanAll_MethodGroup.GreaterThanAll_1_T1
            def __call__(self, left: Vector256_1[GreaterThanAll_1_T], right: Vector256_1[GreaterThanAll_1_T]) -> bool:...


    # Skipped GreaterThanAny due to it being static, abstract and generic.

    GreaterThanAny : GreaterThanAny_MethodGroup
    class GreaterThanAny_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanAny_1_T1]) -> GreaterThanAny_1[GreaterThanAny_1_T1]: ...

        GreaterThanAny_1_T1 = typing.TypeVar('GreaterThanAny_1_T1')
        class GreaterThanAny_1(typing.Generic[GreaterThanAny_1_T1]):
            GreaterThanAny_1_T = Vector256_0.GreaterThanAny_MethodGroup.GreaterThanAny_1_T1
            def __call__(self, left: Vector256_1[GreaterThanAny_1_T], right: Vector256_1[GreaterThanAny_1_T]) -> bool:...


    # Skipped GreaterThanOrEqual due to it being static, abstract and generic.

    GreaterThanOrEqual : GreaterThanOrEqual_MethodGroup
    class GreaterThanOrEqual_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqual_1_T1]) -> GreaterThanOrEqual_1[GreaterThanOrEqual_1_T1]: ...

        GreaterThanOrEqual_1_T1 = typing.TypeVar('GreaterThanOrEqual_1_T1')
        class GreaterThanOrEqual_1(typing.Generic[GreaterThanOrEqual_1_T1]):
            GreaterThanOrEqual_1_T = Vector256_0.GreaterThanOrEqual_MethodGroup.GreaterThanOrEqual_1_T1
            def __call__(self, left: Vector256_1[GreaterThanOrEqual_1_T], right: Vector256_1[GreaterThanOrEqual_1_T]) -> Vector256_1[GreaterThanOrEqual_1_T]:...


    # Skipped GreaterThanOrEqualAll due to it being static, abstract and generic.

    GreaterThanOrEqualAll : GreaterThanOrEqualAll_MethodGroup
    class GreaterThanOrEqualAll_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqualAll_1_T1]) -> GreaterThanOrEqualAll_1[GreaterThanOrEqualAll_1_T1]: ...

        GreaterThanOrEqualAll_1_T1 = typing.TypeVar('GreaterThanOrEqualAll_1_T1')
        class GreaterThanOrEqualAll_1(typing.Generic[GreaterThanOrEqualAll_1_T1]):
            GreaterThanOrEqualAll_1_T = Vector256_0.GreaterThanOrEqualAll_MethodGroup.GreaterThanOrEqualAll_1_T1
            def __call__(self, left: Vector256_1[GreaterThanOrEqualAll_1_T], right: Vector256_1[GreaterThanOrEqualAll_1_T]) -> bool:...


    # Skipped GreaterThanOrEqualAny due to it being static, abstract and generic.

    GreaterThanOrEqualAny : GreaterThanOrEqualAny_MethodGroup
    class GreaterThanOrEqualAny_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqualAny_1_T1]) -> GreaterThanOrEqualAny_1[GreaterThanOrEqualAny_1_T1]: ...

        GreaterThanOrEqualAny_1_T1 = typing.TypeVar('GreaterThanOrEqualAny_1_T1')
        class GreaterThanOrEqualAny_1(typing.Generic[GreaterThanOrEqualAny_1_T1]):
            GreaterThanOrEqualAny_1_T = Vector256_0.GreaterThanOrEqualAny_MethodGroup.GreaterThanOrEqualAny_1_T1
            def __call__(self, left: Vector256_1[GreaterThanOrEqualAny_1_T], right: Vector256_1[GreaterThanOrEqualAny_1_T]) -> bool:...


    # Skipped Hypot due to it being static, abstract and generic.

    Hypot : Hypot_MethodGroup
    class Hypot_MethodGroup:
        def __call__(self, x: Vector256_1[float], y: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Hypot(x : Vector256`1, y : Vector256`1) was skipped since it collides with above method

    # Skipped IndexOf due to it being static, abstract and generic.

    IndexOf : IndexOf_MethodGroup
    class IndexOf_MethodGroup:
        def __getitem__(self, t:typing.Type[IndexOf_1_T1]) -> IndexOf_1[IndexOf_1_T1]: ...

        IndexOf_1_T1 = typing.TypeVar('IndexOf_1_T1')
        class IndexOf_1(typing.Generic[IndexOf_1_T1]):
            IndexOf_1_T = Vector256_0.IndexOf_MethodGroup.IndexOf_1_T1
            def __call__(self, vector: Vector256_1[IndexOf_1_T], value: IndexOf_1_T) -> int:...


    # Skipped IndexOfWhereAllBitsSet due to it being static, abstract and generic.

    IndexOfWhereAllBitsSet : IndexOfWhereAllBitsSet_MethodGroup
    class IndexOfWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[IndexOfWhereAllBitsSet_1_T1]) -> IndexOfWhereAllBitsSet_1[IndexOfWhereAllBitsSet_1_T1]: ...

        IndexOfWhereAllBitsSet_1_T1 = typing.TypeVar('IndexOfWhereAllBitsSet_1_T1')
        class IndexOfWhereAllBitsSet_1(typing.Generic[IndexOfWhereAllBitsSet_1_T1]):
            IndexOfWhereAllBitsSet_1_T = Vector256_0.IndexOfWhereAllBitsSet_MethodGroup.IndexOfWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector256_1[IndexOfWhereAllBitsSet_1_T]) -> int:...


    # Skipped IsEvenInteger due to it being static, abstract and generic.

    IsEvenInteger : IsEvenInteger_MethodGroup
    class IsEvenInteger_MethodGroup:
        def __getitem__(self, t:typing.Type[IsEvenInteger_1_T1]) -> IsEvenInteger_1[IsEvenInteger_1_T1]: ...

        IsEvenInteger_1_T1 = typing.TypeVar('IsEvenInteger_1_T1')
        class IsEvenInteger_1(typing.Generic[IsEvenInteger_1_T1]):
            IsEvenInteger_1_T = Vector256_0.IsEvenInteger_MethodGroup.IsEvenInteger_1_T1
            def __call__(self, vector: Vector256_1[IsEvenInteger_1_T]) -> Vector256_1[IsEvenInteger_1_T]:...


    # Skipped IsFinite due to it being static, abstract and generic.

    IsFinite : IsFinite_MethodGroup
    class IsFinite_MethodGroup:
        def __getitem__(self, t:typing.Type[IsFinite_1_T1]) -> IsFinite_1[IsFinite_1_T1]: ...

        IsFinite_1_T1 = typing.TypeVar('IsFinite_1_T1')
        class IsFinite_1(typing.Generic[IsFinite_1_T1]):
            IsFinite_1_T = Vector256_0.IsFinite_MethodGroup.IsFinite_1_T1
            def __call__(self, vector: Vector256_1[IsFinite_1_T]) -> Vector256_1[IsFinite_1_T]:...


    # Skipped IsInfinity due to it being static, abstract and generic.

    IsInfinity : IsInfinity_MethodGroup
    class IsInfinity_MethodGroup:
        def __getitem__(self, t:typing.Type[IsInfinity_1_T1]) -> IsInfinity_1[IsInfinity_1_T1]: ...

        IsInfinity_1_T1 = typing.TypeVar('IsInfinity_1_T1')
        class IsInfinity_1(typing.Generic[IsInfinity_1_T1]):
            IsInfinity_1_T = Vector256_0.IsInfinity_MethodGroup.IsInfinity_1_T1
            def __call__(self, vector: Vector256_1[IsInfinity_1_T]) -> Vector256_1[IsInfinity_1_T]:...


    # Skipped IsInteger due to it being static, abstract and generic.

    IsInteger : IsInteger_MethodGroup
    class IsInteger_MethodGroup:
        def __getitem__(self, t:typing.Type[IsInteger_1_T1]) -> IsInteger_1[IsInteger_1_T1]: ...

        IsInteger_1_T1 = typing.TypeVar('IsInteger_1_T1')
        class IsInteger_1(typing.Generic[IsInteger_1_T1]):
            IsInteger_1_T = Vector256_0.IsInteger_MethodGroup.IsInteger_1_T1
            def __call__(self, vector: Vector256_1[IsInteger_1_T]) -> Vector256_1[IsInteger_1_T]:...


    # Skipped IsNaN due to it being static, abstract and generic.

    IsNaN : IsNaN_MethodGroup
    class IsNaN_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNaN_1_T1]) -> IsNaN_1[IsNaN_1_T1]: ...

        IsNaN_1_T1 = typing.TypeVar('IsNaN_1_T1')
        class IsNaN_1(typing.Generic[IsNaN_1_T1]):
            IsNaN_1_T = Vector256_0.IsNaN_MethodGroup.IsNaN_1_T1
            def __call__(self, vector: Vector256_1[IsNaN_1_T]) -> Vector256_1[IsNaN_1_T]:...


    # Skipped IsNegative due to it being static, abstract and generic.

    IsNegative : IsNegative_MethodGroup
    class IsNegative_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNegative_1_T1]) -> IsNegative_1[IsNegative_1_T1]: ...

        IsNegative_1_T1 = typing.TypeVar('IsNegative_1_T1')
        class IsNegative_1(typing.Generic[IsNegative_1_T1]):
            IsNegative_1_T = Vector256_0.IsNegative_MethodGroup.IsNegative_1_T1
            def __call__(self, vector: Vector256_1[IsNegative_1_T]) -> Vector256_1[IsNegative_1_T]:...


    # Skipped IsNegativeInfinity due to it being static, abstract and generic.

    IsNegativeInfinity : IsNegativeInfinity_MethodGroup
    class IsNegativeInfinity_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNegativeInfinity_1_T1]) -> IsNegativeInfinity_1[IsNegativeInfinity_1_T1]: ...

        IsNegativeInfinity_1_T1 = typing.TypeVar('IsNegativeInfinity_1_T1')
        class IsNegativeInfinity_1(typing.Generic[IsNegativeInfinity_1_T1]):
            IsNegativeInfinity_1_T = Vector256_0.IsNegativeInfinity_MethodGroup.IsNegativeInfinity_1_T1
            def __call__(self, vector: Vector256_1[IsNegativeInfinity_1_T]) -> Vector256_1[IsNegativeInfinity_1_T]:...


    # Skipped IsNormal due to it being static, abstract and generic.

    IsNormal : IsNormal_MethodGroup
    class IsNormal_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNormal_1_T1]) -> IsNormal_1[IsNormal_1_T1]: ...

        IsNormal_1_T1 = typing.TypeVar('IsNormal_1_T1')
        class IsNormal_1(typing.Generic[IsNormal_1_T1]):
            IsNormal_1_T = Vector256_0.IsNormal_MethodGroup.IsNormal_1_T1
            def __call__(self, vector: Vector256_1[IsNormal_1_T]) -> Vector256_1[IsNormal_1_T]:...


    # Skipped IsOddInteger due to it being static, abstract and generic.

    IsOddInteger : IsOddInteger_MethodGroup
    class IsOddInteger_MethodGroup:
        def __getitem__(self, t:typing.Type[IsOddInteger_1_T1]) -> IsOddInteger_1[IsOddInteger_1_T1]: ...

        IsOddInteger_1_T1 = typing.TypeVar('IsOddInteger_1_T1')
        class IsOddInteger_1(typing.Generic[IsOddInteger_1_T1]):
            IsOddInteger_1_T = Vector256_0.IsOddInteger_MethodGroup.IsOddInteger_1_T1
            def __call__(self, vector: Vector256_1[IsOddInteger_1_T]) -> Vector256_1[IsOddInteger_1_T]:...


    # Skipped IsPositive due to it being static, abstract and generic.

    IsPositive : IsPositive_MethodGroup
    class IsPositive_MethodGroup:
        def __getitem__(self, t:typing.Type[IsPositive_1_T1]) -> IsPositive_1[IsPositive_1_T1]: ...

        IsPositive_1_T1 = typing.TypeVar('IsPositive_1_T1')
        class IsPositive_1(typing.Generic[IsPositive_1_T1]):
            IsPositive_1_T = Vector256_0.IsPositive_MethodGroup.IsPositive_1_T1
            def __call__(self, vector: Vector256_1[IsPositive_1_T]) -> Vector256_1[IsPositive_1_T]:...


    # Skipped IsPositiveInfinity due to it being static, abstract and generic.

    IsPositiveInfinity : IsPositiveInfinity_MethodGroup
    class IsPositiveInfinity_MethodGroup:
        def __getitem__(self, t:typing.Type[IsPositiveInfinity_1_T1]) -> IsPositiveInfinity_1[IsPositiveInfinity_1_T1]: ...

        IsPositiveInfinity_1_T1 = typing.TypeVar('IsPositiveInfinity_1_T1')
        class IsPositiveInfinity_1(typing.Generic[IsPositiveInfinity_1_T1]):
            IsPositiveInfinity_1_T = Vector256_0.IsPositiveInfinity_MethodGroup.IsPositiveInfinity_1_T1
            def __call__(self, vector: Vector256_1[IsPositiveInfinity_1_T]) -> Vector256_1[IsPositiveInfinity_1_T]:...


    # Skipped IsSubnormal due to it being static, abstract and generic.

    IsSubnormal : IsSubnormal_MethodGroup
    class IsSubnormal_MethodGroup:
        def __getitem__(self, t:typing.Type[IsSubnormal_1_T1]) -> IsSubnormal_1[IsSubnormal_1_T1]: ...

        IsSubnormal_1_T1 = typing.TypeVar('IsSubnormal_1_T1')
        class IsSubnormal_1(typing.Generic[IsSubnormal_1_T1]):
            IsSubnormal_1_T = Vector256_0.IsSubnormal_MethodGroup.IsSubnormal_1_T1
            def __call__(self, vector: Vector256_1[IsSubnormal_1_T]) -> Vector256_1[IsSubnormal_1_T]:...


    # Skipped IsZero due to it being static, abstract and generic.

    IsZero : IsZero_MethodGroup
    class IsZero_MethodGroup:
        def __getitem__(self, t:typing.Type[IsZero_1_T1]) -> IsZero_1[IsZero_1_T1]: ...

        IsZero_1_T1 = typing.TypeVar('IsZero_1_T1')
        class IsZero_1(typing.Generic[IsZero_1_T1]):
            IsZero_1_T = Vector256_0.IsZero_MethodGroup.IsZero_1_T1
            def __call__(self, vector: Vector256_1[IsZero_1_T]) -> Vector256_1[IsZero_1_T]:...


    # Skipped LastIndexOf due to it being static, abstract and generic.

    LastIndexOf : LastIndexOf_MethodGroup
    class LastIndexOf_MethodGroup:
        def __getitem__(self, t:typing.Type[LastIndexOf_1_T1]) -> LastIndexOf_1[LastIndexOf_1_T1]: ...

        LastIndexOf_1_T1 = typing.TypeVar('LastIndexOf_1_T1')
        class LastIndexOf_1(typing.Generic[LastIndexOf_1_T1]):
            LastIndexOf_1_T = Vector256_0.LastIndexOf_MethodGroup.LastIndexOf_1_T1
            def __call__(self, vector: Vector256_1[LastIndexOf_1_T], value: LastIndexOf_1_T) -> int:...


    # Skipped LastIndexOfWhereAllBitsSet due to it being static, abstract and generic.

    LastIndexOfWhereAllBitsSet : LastIndexOfWhereAllBitsSet_MethodGroup
    class LastIndexOfWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[LastIndexOfWhereAllBitsSet_1_T1]) -> LastIndexOfWhereAllBitsSet_1[LastIndexOfWhereAllBitsSet_1_T1]: ...

        LastIndexOfWhereAllBitsSet_1_T1 = typing.TypeVar('LastIndexOfWhereAllBitsSet_1_T1')
        class LastIndexOfWhereAllBitsSet_1(typing.Generic[LastIndexOfWhereAllBitsSet_1_T1]):
            LastIndexOfWhereAllBitsSet_1_T = Vector256_0.LastIndexOfWhereAllBitsSet_MethodGroup.LastIndexOfWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector256_1[LastIndexOfWhereAllBitsSet_1_T]) -> int:...


    # Skipped Lerp due to it being static, abstract and generic.

    Lerp : Lerp_MethodGroup
    class Lerp_MethodGroup:
        def __call__(self, x: Vector256_1[float], y: Vector256_1[float], amount: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Lerp(x : Vector256`1, y : Vector256`1, amount : Vector256`1) was skipped since it collides with above method

    # Skipped LessThan due to it being static, abstract and generic.

    LessThan : LessThan_MethodGroup
    class LessThan_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThan_1_T1]) -> LessThan_1[LessThan_1_T1]: ...

        LessThan_1_T1 = typing.TypeVar('LessThan_1_T1')
        class LessThan_1(typing.Generic[LessThan_1_T1]):
            LessThan_1_T = Vector256_0.LessThan_MethodGroup.LessThan_1_T1
            def __call__(self, left: Vector256_1[LessThan_1_T], right: Vector256_1[LessThan_1_T]) -> Vector256_1[LessThan_1_T]:...


    # Skipped LessThanAll due to it being static, abstract and generic.

    LessThanAll : LessThanAll_MethodGroup
    class LessThanAll_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanAll_1_T1]) -> LessThanAll_1[LessThanAll_1_T1]: ...

        LessThanAll_1_T1 = typing.TypeVar('LessThanAll_1_T1')
        class LessThanAll_1(typing.Generic[LessThanAll_1_T1]):
            LessThanAll_1_T = Vector256_0.LessThanAll_MethodGroup.LessThanAll_1_T1
            def __call__(self, left: Vector256_1[LessThanAll_1_T], right: Vector256_1[LessThanAll_1_T]) -> bool:...


    # Skipped LessThanAny due to it being static, abstract and generic.

    LessThanAny : LessThanAny_MethodGroup
    class LessThanAny_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanAny_1_T1]) -> LessThanAny_1[LessThanAny_1_T1]: ...

        LessThanAny_1_T1 = typing.TypeVar('LessThanAny_1_T1')
        class LessThanAny_1(typing.Generic[LessThanAny_1_T1]):
            LessThanAny_1_T = Vector256_0.LessThanAny_MethodGroup.LessThanAny_1_T1
            def __call__(self, left: Vector256_1[LessThanAny_1_T], right: Vector256_1[LessThanAny_1_T]) -> bool:...


    # Skipped LessThanOrEqual due to it being static, abstract and generic.

    LessThanOrEqual : LessThanOrEqual_MethodGroup
    class LessThanOrEqual_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqual_1_T1]) -> LessThanOrEqual_1[LessThanOrEqual_1_T1]: ...

        LessThanOrEqual_1_T1 = typing.TypeVar('LessThanOrEqual_1_T1')
        class LessThanOrEqual_1(typing.Generic[LessThanOrEqual_1_T1]):
            LessThanOrEqual_1_T = Vector256_0.LessThanOrEqual_MethodGroup.LessThanOrEqual_1_T1
            def __call__(self, left: Vector256_1[LessThanOrEqual_1_T], right: Vector256_1[LessThanOrEqual_1_T]) -> Vector256_1[LessThanOrEqual_1_T]:...


    # Skipped LessThanOrEqualAll due to it being static, abstract and generic.

    LessThanOrEqualAll : LessThanOrEqualAll_MethodGroup
    class LessThanOrEqualAll_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqualAll_1_T1]) -> LessThanOrEqualAll_1[LessThanOrEqualAll_1_T1]: ...

        LessThanOrEqualAll_1_T1 = typing.TypeVar('LessThanOrEqualAll_1_T1')
        class LessThanOrEqualAll_1(typing.Generic[LessThanOrEqualAll_1_T1]):
            LessThanOrEqualAll_1_T = Vector256_0.LessThanOrEqualAll_MethodGroup.LessThanOrEqualAll_1_T1
            def __call__(self, left: Vector256_1[LessThanOrEqualAll_1_T], right: Vector256_1[LessThanOrEqualAll_1_T]) -> bool:...


    # Skipped LessThanOrEqualAny due to it being static, abstract and generic.

    LessThanOrEqualAny : LessThanOrEqualAny_MethodGroup
    class LessThanOrEqualAny_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqualAny_1_T1]) -> LessThanOrEqualAny_1[LessThanOrEqualAny_1_T1]: ...

        LessThanOrEqualAny_1_T1 = typing.TypeVar('LessThanOrEqualAny_1_T1')
        class LessThanOrEqualAny_1(typing.Generic[LessThanOrEqualAny_1_T1]):
            LessThanOrEqualAny_1_T = Vector256_0.LessThanOrEqualAny_MethodGroup.LessThanOrEqualAny_1_T1
            def __call__(self, left: Vector256_1[LessThanOrEqualAny_1_T], right: Vector256_1[LessThanOrEqualAny_1_T]) -> bool:...


    # Skipped Load due to it being static, abstract and generic.

    Load : Load_MethodGroup
    class Load_MethodGroup:
        def __getitem__(self, t:typing.Type[Load_1_T1]) -> Load_1[Load_1_T1]: ...

        Load_1_T1 = typing.TypeVar('Load_1_T1')
        class Load_1(typing.Generic[Load_1_T1]):
            Load_1_T = Vector256_0.Load_MethodGroup.Load_1_T1
            def __call__(self, source: clr.Reference[Load_1_T]) -> Vector256_1[Load_1_T]:...


    # Skipped LoadAligned due to it being static, abstract and generic.

    LoadAligned : LoadAligned_MethodGroup
    class LoadAligned_MethodGroup:
        def __getitem__(self, t:typing.Type[LoadAligned_1_T1]) -> LoadAligned_1[LoadAligned_1_T1]: ...

        LoadAligned_1_T1 = typing.TypeVar('LoadAligned_1_T1')
        class LoadAligned_1(typing.Generic[LoadAligned_1_T1]):
            LoadAligned_1_T = Vector256_0.LoadAligned_MethodGroup.LoadAligned_1_T1
            def __call__(self, source: clr.Reference[LoadAligned_1_T]) -> Vector256_1[LoadAligned_1_T]:...


    # Skipped LoadAlignedNonTemporal due to it being static, abstract and generic.

    LoadAlignedNonTemporal : LoadAlignedNonTemporal_MethodGroup
    class LoadAlignedNonTemporal_MethodGroup:
        def __getitem__(self, t:typing.Type[LoadAlignedNonTemporal_1_T1]) -> LoadAlignedNonTemporal_1[LoadAlignedNonTemporal_1_T1]: ...

        LoadAlignedNonTemporal_1_T1 = typing.TypeVar('LoadAlignedNonTemporal_1_T1')
        class LoadAlignedNonTemporal_1(typing.Generic[LoadAlignedNonTemporal_1_T1]):
            LoadAlignedNonTemporal_1_T = Vector256_0.LoadAlignedNonTemporal_MethodGroup.LoadAlignedNonTemporal_1_T1
            def __call__(self, source: clr.Reference[LoadAlignedNonTemporal_1_T]) -> Vector256_1[LoadAlignedNonTemporal_1_T]:...


    # Skipped LoadUnsafe due to it being static, abstract and generic.

    LoadUnsafe : LoadUnsafe_MethodGroup
    class LoadUnsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[LoadUnsafe_1_T1]) -> LoadUnsafe_1[LoadUnsafe_1_T1]: ...

        LoadUnsafe_1_T1 = typing.TypeVar('LoadUnsafe_1_T1')
        class LoadUnsafe_1(typing.Generic[LoadUnsafe_1_T1]):
            LoadUnsafe_1_T = Vector256_0.LoadUnsafe_MethodGroup.LoadUnsafe_1_T1
            @typing.overload
            def __call__(self, source: clr.Reference[LoadUnsafe_1_T]) -> Vector256_1[LoadUnsafe_1_T]:...
            @typing.overload
            def __call__(self, source: clr.Reference[LoadUnsafe_1_T], elementOffset: UIntPtr) -> Vector256_1[LoadUnsafe_1_T]:...


    # Skipped Log due to it being static, abstract and generic.

    Log : Log_MethodGroup
    class Log_MethodGroup:
        def __call__(self, vector: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Log(vector : Vector256`1) was skipped since it collides with above method

    # Skipped Log2 due to it being static, abstract and generic.

    Log2 : Log2_MethodGroup
    class Log2_MethodGroup:
        def __call__(self, vector: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Log2(vector : Vector256`1) was skipped since it collides with above method

    # Skipped Max due to it being static, abstract and generic.

    Max : Max_MethodGroup
    class Max_MethodGroup:
        def __getitem__(self, t:typing.Type[Max_1_T1]) -> Max_1[Max_1_T1]: ...

        Max_1_T1 = typing.TypeVar('Max_1_T1')
        class Max_1(typing.Generic[Max_1_T1]):
            Max_1_T = Vector256_0.Max_MethodGroup.Max_1_T1
            def __call__(self, left: Vector256_1[Max_1_T], right: Vector256_1[Max_1_T]) -> Vector256_1[Max_1_T]:...


    # Skipped MaxMagnitude due to it being static, abstract and generic.

    MaxMagnitude : MaxMagnitude_MethodGroup
    class MaxMagnitude_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxMagnitude_1_T1]) -> MaxMagnitude_1[MaxMagnitude_1_T1]: ...

        MaxMagnitude_1_T1 = typing.TypeVar('MaxMagnitude_1_T1')
        class MaxMagnitude_1(typing.Generic[MaxMagnitude_1_T1]):
            MaxMagnitude_1_T = Vector256_0.MaxMagnitude_MethodGroup.MaxMagnitude_1_T1
            def __call__(self, left: Vector256_1[MaxMagnitude_1_T], right: Vector256_1[MaxMagnitude_1_T]) -> Vector256_1[MaxMagnitude_1_T]:...


    # Skipped MaxMagnitudeNumber due to it being static, abstract and generic.

    MaxMagnitudeNumber : MaxMagnitudeNumber_MethodGroup
    class MaxMagnitudeNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxMagnitudeNumber_1_T1]) -> MaxMagnitudeNumber_1[MaxMagnitudeNumber_1_T1]: ...

        MaxMagnitudeNumber_1_T1 = typing.TypeVar('MaxMagnitudeNumber_1_T1')
        class MaxMagnitudeNumber_1(typing.Generic[MaxMagnitudeNumber_1_T1]):
            MaxMagnitudeNumber_1_T = Vector256_0.MaxMagnitudeNumber_MethodGroup.MaxMagnitudeNumber_1_T1
            def __call__(self, left: Vector256_1[MaxMagnitudeNumber_1_T], right: Vector256_1[MaxMagnitudeNumber_1_T]) -> Vector256_1[MaxMagnitudeNumber_1_T]:...


    # Skipped MaxNative due to it being static, abstract and generic.

    MaxNative : MaxNative_MethodGroup
    class MaxNative_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxNative_1_T1]) -> MaxNative_1[MaxNative_1_T1]: ...

        MaxNative_1_T1 = typing.TypeVar('MaxNative_1_T1')
        class MaxNative_1(typing.Generic[MaxNative_1_T1]):
            MaxNative_1_T = Vector256_0.MaxNative_MethodGroup.MaxNative_1_T1
            def __call__(self, left: Vector256_1[MaxNative_1_T], right: Vector256_1[MaxNative_1_T]) -> Vector256_1[MaxNative_1_T]:...


    # Skipped MaxNumber due to it being static, abstract and generic.

    MaxNumber : MaxNumber_MethodGroup
    class MaxNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxNumber_1_T1]) -> MaxNumber_1[MaxNumber_1_T1]: ...

        MaxNumber_1_T1 = typing.TypeVar('MaxNumber_1_T1')
        class MaxNumber_1(typing.Generic[MaxNumber_1_T1]):
            MaxNumber_1_T = Vector256_0.MaxNumber_MethodGroup.MaxNumber_1_T1
            def __call__(self, left: Vector256_1[MaxNumber_1_T], right: Vector256_1[MaxNumber_1_T]) -> Vector256_1[MaxNumber_1_T]:...


    # Skipped Min due to it being static, abstract and generic.

    Min : Min_MethodGroup
    class Min_MethodGroup:
        def __getitem__(self, t:typing.Type[Min_1_T1]) -> Min_1[Min_1_T1]: ...

        Min_1_T1 = typing.TypeVar('Min_1_T1')
        class Min_1(typing.Generic[Min_1_T1]):
            Min_1_T = Vector256_0.Min_MethodGroup.Min_1_T1
            def __call__(self, left: Vector256_1[Min_1_T], right: Vector256_1[Min_1_T]) -> Vector256_1[Min_1_T]:...


    # Skipped MinMagnitude due to it being static, abstract and generic.

    MinMagnitude : MinMagnitude_MethodGroup
    class MinMagnitude_MethodGroup:
        def __getitem__(self, t:typing.Type[MinMagnitude_1_T1]) -> MinMagnitude_1[MinMagnitude_1_T1]: ...

        MinMagnitude_1_T1 = typing.TypeVar('MinMagnitude_1_T1')
        class MinMagnitude_1(typing.Generic[MinMagnitude_1_T1]):
            MinMagnitude_1_T = Vector256_0.MinMagnitude_MethodGroup.MinMagnitude_1_T1
            def __call__(self, left: Vector256_1[MinMagnitude_1_T], right: Vector256_1[MinMagnitude_1_T]) -> Vector256_1[MinMagnitude_1_T]:...


    # Skipped MinMagnitudeNumber due to it being static, abstract and generic.

    MinMagnitudeNumber : MinMagnitudeNumber_MethodGroup
    class MinMagnitudeNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MinMagnitudeNumber_1_T1]) -> MinMagnitudeNumber_1[MinMagnitudeNumber_1_T1]: ...

        MinMagnitudeNumber_1_T1 = typing.TypeVar('MinMagnitudeNumber_1_T1')
        class MinMagnitudeNumber_1(typing.Generic[MinMagnitudeNumber_1_T1]):
            MinMagnitudeNumber_1_T = Vector256_0.MinMagnitudeNumber_MethodGroup.MinMagnitudeNumber_1_T1
            def __call__(self, left: Vector256_1[MinMagnitudeNumber_1_T], right: Vector256_1[MinMagnitudeNumber_1_T]) -> Vector256_1[MinMagnitudeNumber_1_T]:...


    # Skipped MinNative due to it being static, abstract and generic.

    MinNative : MinNative_MethodGroup
    class MinNative_MethodGroup:
        def __getitem__(self, t:typing.Type[MinNative_1_T1]) -> MinNative_1[MinNative_1_T1]: ...

        MinNative_1_T1 = typing.TypeVar('MinNative_1_T1')
        class MinNative_1(typing.Generic[MinNative_1_T1]):
            MinNative_1_T = Vector256_0.MinNative_MethodGroup.MinNative_1_T1
            def __call__(self, left: Vector256_1[MinNative_1_T], right: Vector256_1[MinNative_1_T]) -> Vector256_1[MinNative_1_T]:...


    # Skipped MinNumber due to it being static, abstract and generic.

    MinNumber : MinNumber_MethodGroup
    class MinNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MinNumber_1_T1]) -> MinNumber_1[MinNumber_1_T1]: ...

        MinNumber_1_T1 = typing.TypeVar('MinNumber_1_T1')
        class MinNumber_1(typing.Generic[MinNumber_1_T1]):
            MinNumber_1_T = Vector256_0.MinNumber_MethodGroup.MinNumber_1_T1
            def __call__(self, left: Vector256_1[MinNumber_1_T], right: Vector256_1[MinNumber_1_T]) -> Vector256_1[MinNumber_1_T]:...


    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        def __getitem__(self, t:typing.Type[Multiply_1_T1]) -> Multiply_1[Multiply_1_T1]: ...

        Multiply_1_T1 = typing.TypeVar('Multiply_1_T1')
        class Multiply_1(typing.Generic[Multiply_1_T1]):
            Multiply_1_T = Vector256_0.Multiply_MethodGroup.Multiply_1_T1
            @typing.overload
            def __call__(self, left: Vector256_1[Multiply_1_T], right: Vector256_1[Multiply_1_T]) -> Vector256_1[Multiply_1_T]:...
            @typing.overload
            def __call__(self, left: Vector256_1[Multiply_1_T], right: Multiply_1_T) -> Vector256_1[Multiply_1_T]:...
            @typing.overload
            def __call__(self, left: Multiply_1_T, right: Vector256_1[Multiply_1_T]) -> Vector256_1[Multiply_1_T]:...


    # Skipped MultiplyAddEstimate due to it being static, abstract and generic.

    MultiplyAddEstimate : MultiplyAddEstimate_MethodGroup
    class MultiplyAddEstimate_MethodGroup:
        def __call__(self, left: Vector256_1[float], right: Vector256_1[float], addend: Vector256_1[float]) -> Vector256_1[float]:...
        # Method MultiplyAddEstimate(left : Vector256`1, right : Vector256`1, addend : Vector256`1) was skipped since it collides with above method

    # Skipped Narrow due to it being static, abstract and generic.

    Narrow : Narrow_MethodGroup
    class Narrow_MethodGroup:
        def __call__(self, lower: Vector256_1[float], upper: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Narrow(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method

    # Skipped NarrowWithSaturation due to it being static, abstract and generic.

    NarrowWithSaturation : NarrowWithSaturation_MethodGroup
    class NarrowWithSaturation_MethodGroup:
        def __call__(self, lower: Vector256_1[float], upper: Vector256_1[float]) -> Vector256_1[float]:...
        # Method NarrowWithSaturation(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method

    # Skipped Negate due to it being static, abstract and generic.

    Negate : Negate_MethodGroup
    class Negate_MethodGroup:
        def __getitem__(self, t:typing.Type[Negate_1_T1]) -> Negate_1[Negate_1_T1]: ...

        Negate_1_T1 = typing.TypeVar('Negate_1_T1')
        class Negate_1(typing.Generic[Negate_1_T1]):
            Negate_1_T = Vector256_0.Negate_MethodGroup.Negate_1_T1
            def __call__(self, vector: Vector256_1[Negate_1_T]) -> Vector256_1[Negate_1_T]:...


    # Skipped None due to it being static, abstract and generic.

    None : None_MethodGroup
    class None_MethodGroup:
        def __getitem__(self, t:typing.Type[None_1_T1]) -> None_1[None_1_T1]: ...

        None_1_T1 = typing.TypeVar('None_1_T1')
        class None_1(typing.Generic[None_1_T1]):
            None_1_T = Vector256_0.None_MethodGroup.None_1_T1
            def __call__(self, vector: Vector256_1[None_1_T], value: None_1_T) -> bool:...


    # Skipped NoneWhereAllBitsSet due to it being static, abstract and generic.

    NoneWhereAllBitsSet : NoneWhereAllBitsSet_MethodGroup
    class NoneWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[NoneWhereAllBitsSet_1_T1]) -> NoneWhereAllBitsSet_1[NoneWhereAllBitsSet_1_T1]: ...

        NoneWhereAllBitsSet_1_T1 = typing.TypeVar('NoneWhereAllBitsSet_1_T1')
        class NoneWhereAllBitsSet_1(typing.Generic[NoneWhereAllBitsSet_1_T1]):
            NoneWhereAllBitsSet_1_T = Vector256_0.NoneWhereAllBitsSet_MethodGroup.NoneWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector256_1[NoneWhereAllBitsSet_1_T]) -> bool:...


    # Skipped OnesComplement due to it being static, abstract and generic.

    OnesComplement : OnesComplement_MethodGroup
    class OnesComplement_MethodGroup:
        def __getitem__(self, t:typing.Type[OnesComplement_1_T1]) -> OnesComplement_1[OnesComplement_1_T1]: ...

        OnesComplement_1_T1 = typing.TypeVar('OnesComplement_1_T1')
        class OnesComplement_1(typing.Generic[OnesComplement_1_T1]):
            OnesComplement_1_T = Vector256_0.OnesComplement_MethodGroup.OnesComplement_1_T1
            def __call__(self, vector: Vector256_1[OnesComplement_1_T]) -> Vector256_1[OnesComplement_1_T]:...


    # Skipped RadiansToDegrees due to it being static, abstract and generic.

    RadiansToDegrees : RadiansToDegrees_MethodGroup
    class RadiansToDegrees_MethodGroup:
        def __call__(self, radians: Vector256_1[float]) -> Vector256_1[float]:...
        # Method RadiansToDegrees(radians : Vector256`1) was skipped since it collides with above method

    # Skipped Round due to it being static, abstract and generic.

    Round : Round_MethodGroup
    class Round_MethodGroup:
        @typing.overload
        def __call__(self, vector: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Round(vector : Vector256`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, vector: Vector256_1[float], mode: MidpointRounding) -> Vector256_1[float]:...
        # Method Round(vector : Vector256`1, mode : MidpointRounding) was skipped since it collides with above method

    # Skipped ShiftLeft due to it being static, abstract and generic.

    ShiftLeft : ShiftLeft_MethodGroup
    class ShiftLeft_MethodGroup:
        @typing.overload
        def __call__(self, vector: Vector256_1[int], shiftCount: int) -> Vector256_1[int]:...
        # Method ShiftLeft(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, vector: Vector256_1[UIntPtr], shiftCount: int) -> Vector256_1[UIntPtr]:...

    # Skipped ShiftRightArithmetic due to it being static, abstract and generic.

    ShiftRightArithmetic : ShiftRightArithmetic_MethodGroup
    class ShiftRightArithmetic_MethodGroup:
        def __call__(self, vector: Vector256_1[int], shiftCount: int) -> Vector256_1[int]:...
        # Method ShiftRightArithmetic(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightArithmetic(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightArithmetic(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightArithmetic(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method

    # Skipped ShiftRightLogical due to it being static, abstract and generic.

    ShiftRightLogical : ShiftRightLogical_MethodGroup
    class ShiftRightLogical_MethodGroup:
        @typing.overload
        def __call__(self, vector: Vector256_1[int], shiftCount: int) -> Vector256_1[int]:...
        # Method ShiftRightLogical(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector256`1, shiftCount : Int32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, vector: Vector256_1[UIntPtr], shiftCount: int) -> Vector256_1[UIntPtr]:...

    # Skipped Shuffle due to it being static, abstract and generic.

    Shuffle : Shuffle_MethodGroup
    class Shuffle_MethodGroup:
        def __call__(self, vector: Vector256_1[float], indices: Vector256_1[int]) -> Vector256_1[float]:...
        # Method Shuffle(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method

    # Skipped ShuffleNative due to it being static, abstract and generic.

    ShuffleNative : ShuffleNative_MethodGroup
    class ShuffleNative_MethodGroup:
        def __call__(self, vector: Vector256_1[float], indices: Vector256_1[int]) -> Vector256_1[float]:...
        # Method ShuffleNative(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector256`1, indices : Vector256`1) was skipped since it collides with above method

    # Skipped Sin due to it being static, abstract and generic.

    Sin : Sin_MethodGroup
    class Sin_MethodGroup:
        def __call__(self, vector: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Sin(vector : Vector256`1) was skipped since it collides with above method

    # Skipped SinCos due to it being static, abstract and generic.

    SinCos : SinCos_MethodGroup
    class SinCos_MethodGroup:
        def __call__(self, vector: Vector256_1[float]) -> ValueTuple_2[Vector256_1[float], Vector256_1[float]]:...
        # Method SinCos(vector : Vector256`1) was skipped since it collides with above method

    # Skipped Sqrt due to it being static, abstract and generic.

    Sqrt : Sqrt_MethodGroup
    class Sqrt_MethodGroup:
        def __getitem__(self, t:typing.Type[Sqrt_1_T1]) -> Sqrt_1[Sqrt_1_T1]: ...

        Sqrt_1_T1 = typing.TypeVar('Sqrt_1_T1')
        class Sqrt_1(typing.Generic[Sqrt_1_T1]):
            Sqrt_1_T = Vector256_0.Sqrt_MethodGroup.Sqrt_1_T1
            def __call__(self, vector: Vector256_1[Sqrt_1_T]) -> Vector256_1[Sqrt_1_T]:...


    # Skipped Store due to it being static, abstract and generic.

    Store : Store_MethodGroup
    class Store_MethodGroup:
        def __getitem__(self, t:typing.Type[Store_1_T1]) -> Store_1[Store_1_T1]: ...

        Store_1_T1 = typing.TypeVar('Store_1_T1')
        class Store_1(typing.Generic[Store_1_T1]):
            Store_1_T = Vector256_0.Store_MethodGroup.Store_1_T1
            def __call__(self, source: Vector256_1[Store_1_T], destination: clr.Reference[Store_1_T]) -> None:...


    # Skipped StoreAligned due to it being static, abstract and generic.

    StoreAligned : StoreAligned_MethodGroup
    class StoreAligned_MethodGroup:
        def __getitem__(self, t:typing.Type[StoreAligned_1_T1]) -> StoreAligned_1[StoreAligned_1_T1]: ...

        StoreAligned_1_T1 = typing.TypeVar('StoreAligned_1_T1')
        class StoreAligned_1(typing.Generic[StoreAligned_1_T1]):
            StoreAligned_1_T = Vector256_0.StoreAligned_MethodGroup.StoreAligned_1_T1
            def __call__(self, source: Vector256_1[StoreAligned_1_T], destination: clr.Reference[StoreAligned_1_T]) -> None:...


    # Skipped StoreAlignedNonTemporal due to it being static, abstract and generic.

    StoreAlignedNonTemporal : StoreAlignedNonTemporal_MethodGroup
    class StoreAlignedNonTemporal_MethodGroup:
        def __getitem__(self, t:typing.Type[StoreAlignedNonTemporal_1_T1]) -> StoreAlignedNonTemporal_1[StoreAlignedNonTemporal_1_T1]: ...

        StoreAlignedNonTemporal_1_T1 = typing.TypeVar('StoreAlignedNonTemporal_1_T1')
        class StoreAlignedNonTemporal_1(typing.Generic[StoreAlignedNonTemporal_1_T1]):
            StoreAlignedNonTemporal_1_T = Vector256_0.StoreAlignedNonTemporal_MethodGroup.StoreAlignedNonTemporal_1_T1
            def __call__(self, source: Vector256_1[StoreAlignedNonTemporal_1_T], destination: clr.Reference[StoreAlignedNonTemporal_1_T]) -> None:...


    # Skipped StoreUnsafe due to it being static, abstract and generic.

    StoreUnsafe : StoreUnsafe_MethodGroup
    class StoreUnsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[StoreUnsafe_1_T1]) -> StoreUnsafe_1[StoreUnsafe_1_T1]: ...

        StoreUnsafe_1_T1 = typing.TypeVar('StoreUnsafe_1_T1')
        class StoreUnsafe_1(typing.Generic[StoreUnsafe_1_T1]):
            StoreUnsafe_1_T = Vector256_0.StoreUnsafe_MethodGroup.StoreUnsafe_1_T1
            @typing.overload
            def __call__(self, source: Vector256_1[StoreUnsafe_1_T], destination: clr.Reference[StoreUnsafe_1_T]) -> None:...
            @typing.overload
            def __call__(self, source: Vector256_1[StoreUnsafe_1_T], destination: clr.Reference[StoreUnsafe_1_T], elementOffset: UIntPtr) -> None:...


    # Skipped Subtract due to it being static, abstract and generic.

    Subtract : Subtract_MethodGroup
    class Subtract_MethodGroup:
        def __getitem__(self, t:typing.Type[Subtract_1_T1]) -> Subtract_1[Subtract_1_T1]: ...

        Subtract_1_T1 = typing.TypeVar('Subtract_1_T1')
        class Subtract_1(typing.Generic[Subtract_1_T1]):
            Subtract_1_T = Vector256_0.Subtract_MethodGroup.Subtract_1_T1
            def __call__(self, left: Vector256_1[Subtract_1_T], right: Vector256_1[Subtract_1_T]) -> Vector256_1[Subtract_1_T]:...


    # Skipped SubtractSaturate due to it being static, abstract and generic.

    SubtractSaturate : SubtractSaturate_MethodGroup
    class SubtractSaturate_MethodGroup:
        def __getitem__(self, t:typing.Type[SubtractSaturate_1_T1]) -> SubtractSaturate_1[SubtractSaturate_1_T1]: ...

        SubtractSaturate_1_T1 = typing.TypeVar('SubtractSaturate_1_T1')
        class SubtractSaturate_1(typing.Generic[SubtractSaturate_1_T1]):
            SubtractSaturate_1_T = Vector256_0.SubtractSaturate_MethodGroup.SubtractSaturate_1_T1
            def __call__(self, left: Vector256_1[SubtractSaturate_1_T], right: Vector256_1[SubtractSaturate_1_T]) -> Vector256_1[SubtractSaturate_1_T]:...


    # Skipped Sum due to it being static, abstract and generic.

    Sum : Sum_MethodGroup
    class Sum_MethodGroup:
        def __getitem__(self, t:typing.Type[Sum_1_T1]) -> Sum_1[Sum_1_T1]: ...

        Sum_1_T1 = typing.TypeVar('Sum_1_T1')
        class Sum_1(typing.Generic[Sum_1_T1]):
            Sum_1_T = Vector256_0.Sum_MethodGroup.Sum_1_T1
            def __call__(self, vector: Vector256_1[Sum_1_T]) -> Sum_1_T:...


    # Skipped ToScalar due to it being static, abstract and generic.

    ToScalar : ToScalar_MethodGroup
    class ToScalar_MethodGroup:
        def __getitem__(self, t:typing.Type[ToScalar_1_T1]) -> ToScalar_1[ToScalar_1_T1]: ...

        ToScalar_1_T1 = typing.TypeVar('ToScalar_1_T1')
        class ToScalar_1(typing.Generic[ToScalar_1_T1]):
            ToScalar_1_T = Vector256_0.ToScalar_MethodGroup.ToScalar_1_T1
            def __call__(self, vector: Vector256_1[ToScalar_1_T]) -> ToScalar_1_T:...


    # Skipped ToVector512 due to it being static, abstract and generic.

    ToVector512 : ToVector512_MethodGroup
    class ToVector512_MethodGroup:
        def __getitem__(self, t:typing.Type[ToVector512_1_T1]) -> ToVector512_1[ToVector512_1_T1]: ...

        ToVector512_1_T1 = typing.TypeVar('ToVector512_1_T1')
        class ToVector512_1(typing.Generic[ToVector512_1_T1]):
            ToVector512_1_T = Vector256_0.ToVector512_MethodGroup.ToVector512_1_T1
            def __call__(self, vector: Vector256_1[ToVector512_1_T]) -> Vector512_1[ToVector512_1_T]:...


    # Skipped ToVector512Unsafe due to it being static, abstract and generic.

    ToVector512Unsafe : ToVector512Unsafe_MethodGroup
    class ToVector512Unsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[ToVector512Unsafe_1_T1]) -> ToVector512Unsafe_1[ToVector512Unsafe_1_T1]: ...

        ToVector512Unsafe_1_T1 = typing.TypeVar('ToVector512Unsafe_1_T1')
        class ToVector512Unsafe_1(typing.Generic[ToVector512Unsafe_1_T1]):
            ToVector512Unsafe_1_T = Vector256_0.ToVector512Unsafe_MethodGroup.ToVector512Unsafe_1_T1
            def __call__(self, vector: Vector256_1[ToVector512Unsafe_1_T]) -> Vector512_1[ToVector512Unsafe_1_T]:...


    # Skipped Truncate due to it being static, abstract and generic.

    Truncate : Truncate_MethodGroup
    class Truncate_MethodGroup:
        def __call__(self, vector: Vector256_1[float]) -> Vector256_1[float]:...
        # Method Truncate(vector : Vector256`1) was skipped since it collides with above method

    # Skipped TryCopyTo due to it being static, abstract and generic.

    TryCopyTo : TryCopyTo_MethodGroup
    class TryCopyTo_MethodGroup:
        def __getitem__(self, t:typing.Type[TryCopyTo_1_T1]) -> TryCopyTo_1[TryCopyTo_1_T1]: ...

        TryCopyTo_1_T1 = typing.TypeVar('TryCopyTo_1_T1')
        class TryCopyTo_1(typing.Generic[TryCopyTo_1_T1]):
            TryCopyTo_1_T = Vector256_0.TryCopyTo_MethodGroup.TryCopyTo_1_T1
            def __call__(self, vector: Vector256_1[TryCopyTo_1_T], destination: Span_1[TryCopyTo_1_T]) -> bool:...


    # Skipped Widen due to it being static, abstract and generic.

    Widen : Widen_MethodGroup
    class Widen_MethodGroup:
        def __call__(self, source: Vector256_1[float]) -> ValueTuple_2[Vector256_1[float], Vector256_1[float]]:...
        # Method Widen(source : Vector256`1) was skipped since it collides with above method
        # Method Widen(source : Vector256`1) was skipped since it collides with above method
        # Method Widen(source : Vector256`1) was skipped since it collides with above method
        # Method Widen(source : Vector256`1) was skipped since it collides with above method
        # Method Widen(source : Vector256`1) was skipped since it collides with above method
        # Method Widen(source : Vector256`1) was skipped since it collides with above method

    # Skipped WidenLower due to it being static, abstract and generic.

    WidenLower : WidenLower_MethodGroup
    class WidenLower_MethodGroup:
        def __call__(self, source: Vector256_1[float]) -> Vector256_1[float]:...
        # Method WidenLower(source : Vector256`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector256`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector256`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector256`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector256`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector256`1) was skipped since it collides with above method

    # Skipped WidenUpper due to it being static, abstract and generic.

    WidenUpper : WidenUpper_MethodGroup
    class WidenUpper_MethodGroup:
        def __call__(self, source: Vector256_1[float]) -> Vector256_1[float]:...
        # Method WidenUpper(source : Vector256`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector256`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector256`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector256`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector256`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector256`1) was skipped since it collides with above method

    # Skipped WithElement due to it being static, abstract and generic.

    WithElement : WithElement_MethodGroup
    class WithElement_MethodGroup:
        def __getitem__(self, t:typing.Type[WithElement_1_T1]) -> WithElement_1[WithElement_1_T1]: ...

        WithElement_1_T1 = typing.TypeVar('WithElement_1_T1')
        class WithElement_1(typing.Generic[WithElement_1_T1]):
            WithElement_1_T = Vector256_0.WithElement_MethodGroup.WithElement_1_T1
            def __call__(self, vector: Vector256_1[WithElement_1_T], index: int, value: WithElement_1_T) -> Vector256_1[WithElement_1_T]:...


    # Skipped WithLower due to it being static, abstract and generic.

    WithLower : WithLower_MethodGroup
    class WithLower_MethodGroup:
        def __getitem__(self, t:typing.Type[WithLower_1_T1]) -> WithLower_1[WithLower_1_T1]: ...

        WithLower_1_T1 = typing.TypeVar('WithLower_1_T1')
        class WithLower_1(typing.Generic[WithLower_1_T1]):
            WithLower_1_T = Vector256_0.WithLower_MethodGroup.WithLower_1_T1
            def __call__(self, vector: Vector256_1[WithLower_1_T], value: Vector128_1[WithLower_1_T]) -> Vector256_1[WithLower_1_T]:...


    # Skipped WithUpper due to it being static, abstract and generic.

    WithUpper : WithUpper_MethodGroup
    class WithUpper_MethodGroup:
        def __getitem__(self, t:typing.Type[WithUpper_1_T1]) -> WithUpper_1[WithUpper_1_T1]: ...

        WithUpper_1_T1 = typing.TypeVar('WithUpper_1_T1')
        class WithUpper_1(typing.Generic[WithUpper_1_T1]):
            WithUpper_1_T = Vector256_0.WithUpper_MethodGroup.WithUpper_1_T1
            def __call__(self, vector: Vector256_1[WithUpper_1_T], value: Vector128_1[WithUpper_1_T]) -> Vector256_1[WithUpper_1_T]:...


    # Skipped Xor due to it being static, abstract and generic.

    Xor : Xor_MethodGroup
    class Xor_MethodGroup:
        def __getitem__(self, t:typing.Type[Xor_1_T1]) -> Xor_1[Xor_1_T1]: ...

        Xor_1_T1 = typing.TypeVar('Xor_1_T1')
        class Xor_1(typing.Generic[Xor_1_T1]):
            Xor_1_T = Vector256_0.Xor_MethodGroup.Xor_1_T1
            def __call__(self, left: Vector256_1[Xor_1_T], right: Vector256_1[Xor_1_T]) -> Vector256_1[Xor_1_T]:...




Vector256_1_T = typing.TypeVar('Vector256_1_T')
class Vector256_1(typing.Generic[Vector256_1_T]):
    @classmethod
    @property
    def AllBitsSet(cls) -> Vector256_1[Vector256_1_T]: ...
    @classmethod
    @property
    def Count(cls) -> int: ...
    @classmethod
    @property
    def Indices(cls) -> Vector256_1[Vector256_1_T]: ...
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @property
    def Item(self) -> Vector256_1_T: ...
    @classmethod
    @property
    def One(cls) -> Vector256_1[Vector256_1_T]: ...
    @classmethod
    @property
    def Zero(cls) -> Vector256_1[Vector256_1_T]: ...
    def GetHashCode(self) -> int: ...
    def __add__(self, left: Vector256_1[Vector256_1_T], right: Vector256_1[Vector256_1_T]) -> Vector256_1[Vector256_1_T]: ...
    def __and__(self, left: Vector256_1[Vector256_1_T], right: Vector256_1[Vector256_1_T]) -> Vector256_1[Vector256_1_T]: ...
    def __or__(self, left: Vector256_1[Vector256_1_T], right: Vector256_1[Vector256_1_T]) -> Vector256_1[Vector256_1_T]: ...
    @typing.overload
    def __truediv__(self, left: Vector256_1[Vector256_1_T], right: Vector256_1[Vector256_1_T]) -> Vector256_1[Vector256_1_T]: ...
    @typing.overload
    def __truediv__(self, left: Vector256_1[Vector256_1_T], right: Vector256_1_T) -> Vector256_1[Vector256_1_T]: ...
    def __eq__(self, left: Vector256_1[Vector256_1_T], right: Vector256_1[Vector256_1_T]) -> bool: ...
    def __xor__(self, left: Vector256_1[Vector256_1_T], right: Vector256_1[Vector256_1_T]) -> Vector256_1[Vector256_1_T]: ...
    def __ne__(self, left: Vector256_1[Vector256_1_T], right: Vector256_1[Vector256_1_T]) -> bool: ...
    def __lshift__(self, value: Vector256_1[Vector256_1_T], shiftCount: int) -> Vector256_1[Vector256_1_T]: ...
    @typing.overload
    def __mul__(self, left: Vector256_1[Vector256_1_T], right: Vector256_1[Vector256_1_T]) -> Vector256_1[Vector256_1_T]: ...
    @typing.overload
    def __mul__(self, left: Vector256_1[Vector256_1_T], right: Vector256_1_T) -> Vector256_1[Vector256_1_T]: ...
    @typing.overload
    def __mul__(self, left: Vector256_1_T, right: Vector256_1[Vector256_1_T]) -> Vector256_1[Vector256_1_T]: ...
    def __invert__(self, vector: Vector256_1[Vector256_1_T]) -> Vector256_1[Vector256_1_T]: ...
    def __rshift__(self, value: Vector256_1[Vector256_1_T], shiftCount: int) -> Vector256_1[Vector256_1_T]: ...
    def __sub__(self, left: Vector256_1[Vector256_1_T], right: Vector256_1[Vector256_1_T]) -> Vector256_1[Vector256_1_T]: ...
    def __neg__(self, vector: Vector256_1[Vector256_1_T]) -> Vector256_1[Vector256_1_T]: ...
    def __pos__(self, value: Vector256_1[Vector256_1_T]) -> Vector256_1[Vector256_1_T]: ...
    # Operator not supported op_UnsignedRightShift(value: Vector256`1, shiftCount: Int32)
    def ToString(self) -> str: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup[Vector256_1_T]
    Equals_MethodGroup_Vector256_1_T = typing.TypeVar('Equals_MethodGroup_Vector256_1_T')
    class Equals_MethodGroup(typing.Generic[Equals_MethodGroup_Vector256_1_T]):
        Equals_MethodGroup_Vector256_1_T = Vector256_1.Equals_MethodGroup_Vector256_1_T
        @typing.overload
        def __call__(self, other: Vector256_1[Equals_MethodGroup_Vector256_1_T]) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...



class Vector512_GenericClasses(abc.ABCMeta):
    Generic_Vector512_GenericClasses_Vector512_1_T = typing.TypeVar('Generic_Vector512_GenericClasses_Vector512_1_T')
    def __getitem__(self, types : typing.Type[Generic_Vector512_GenericClasses_Vector512_1_T]) -> typing.Type[Vector512_1[Generic_Vector512_GenericClasses_Vector512_1_T]]: ...

class Vector512(Vector512_0, metaclass =Vector512_GenericClasses): ...

class Vector512_0(abc.ABC):
    @classmethod
    @property
    def IsHardwareAccelerated(cls) -> bool: ...
    @staticmethod
    def ConvertToInt32(vector: Vector512_1[float]) -> Vector512_1[int]: ...
    @staticmethod
    def ConvertToInt32Native(vector: Vector512_1[float]) -> Vector512_1[int]: ...
    @staticmethod
    def ConvertToInt64(vector: Vector512_1[float]) -> Vector512_1[int]: ...
    @staticmethod
    def ConvertToInt64Native(vector: Vector512_1[float]) -> Vector512_1[int]: ...
    @staticmethod
    def ConvertToUInt32(vector: Vector512_1[float]) -> Vector512_1[int]: ...
    @staticmethod
    def ConvertToUInt32Native(vector: Vector512_1[float]) -> Vector512_1[int]: ...
    @staticmethod
    def ConvertToUInt64(vector: Vector512_1[float]) -> Vector512_1[int]: ...
    @staticmethod
    def ConvertToUInt64Native(vector: Vector512_1[float]) -> Vector512_1[int]: ...
    # Skipped Abs due to it being static, abstract and generic.

    Abs : Abs_MethodGroup
    class Abs_MethodGroup:
        def __getitem__(self, t:typing.Type[Abs_1_T1]) -> Abs_1[Abs_1_T1]: ...

        Abs_1_T1 = typing.TypeVar('Abs_1_T1')
        class Abs_1(typing.Generic[Abs_1_T1]):
            Abs_1_T = Vector512_0.Abs_MethodGroup.Abs_1_T1
            def __call__(self, vector: Vector512_1[Abs_1_T]) -> Vector512_1[Abs_1_T]:...


    # Skipped Add due to it being static, abstract and generic.

    Add : Add_MethodGroup
    class Add_MethodGroup:
        def __getitem__(self, t:typing.Type[Add_1_T1]) -> Add_1[Add_1_T1]: ...

        Add_1_T1 = typing.TypeVar('Add_1_T1')
        class Add_1(typing.Generic[Add_1_T1]):
            Add_1_T = Vector512_0.Add_MethodGroup.Add_1_T1
            def __call__(self, left: Vector512_1[Add_1_T], right: Vector512_1[Add_1_T]) -> Vector512_1[Add_1_T]:...


    # Skipped AddSaturate due to it being static, abstract and generic.

    AddSaturate : AddSaturate_MethodGroup
    class AddSaturate_MethodGroup:
        def __getitem__(self, t:typing.Type[AddSaturate_1_T1]) -> AddSaturate_1[AddSaturate_1_T1]: ...

        AddSaturate_1_T1 = typing.TypeVar('AddSaturate_1_T1')
        class AddSaturate_1(typing.Generic[AddSaturate_1_T1]):
            AddSaturate_1_T = Vector512_0.AddSaturate_MethodGroup.AddSaturate_1_T1
            def __call__(self, left: Vector512_1[AddSaturate_1_T], right: Vector512_1[AddSaturate_1_T]) -> Vector512_1[AddSaturate_1_T]:...


    # Skipped All due to it being static, abstract and generic.

    All : All_MethodGroup
    class All_MethodGroup:
        def __getitem__(self, t:typing.Type[All_1_T1]) -> All_1[All_1_T1]: ...

        All_1_T1 = typing.TypeVar('All_1_T1')
        class All_1(typing.Generic[All_1_T1]):
            All_1_T = Vector512_0.All_MethodGroup.All_1_T1
            def __call__(self, vector: Vector512_1[All_1_T], value: All_1_T) -> bool:...


    # Skipped AllWhereAllBitsSet due to it being static, abstract and generic.

    AllWhereAllBitsSet : AllWhereAllBitsSet_MethodGroup
    class AllWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[AllWhereAllBitsSet_1_T1]) -> AllWhereAllBitsSet_1[AllWhereAllBitsSet_1_T1]: ...

        AllWhereAllBitsSet_1_T1 = typing.TypeVar('AllWhereAllBitsSet_1_T1')
        class AllWhereAllBitsSet_1(typing.Generic[AllWhereAllBitsSet_1_T1]):
            AllWhereAllBitsSet_1_T = Vector512_0.AllWhereAllBitsSet_MethodGroup.AllWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector512_1[AllWhereAllBitsSet_1_T]) -> bool:...


    # Skipped AndNot due to it being static, abstract and generic.

    AndNot : AndNot_MethodGroup
    class AndNot_MethodGroup:
        def __getitem__(self, t:typing.Type[AndNot_1_T1]) -> AndNot_1[AndNot_1_T1]: ...

        AndNot_1_T1 = typing.TypeVar('AndNot_1_T1')
        class AndNot_1(typing.Generic[AndNot_1_T1]):
            AndNot_1_T = Vector512_0.AndNot_MethodGroup.AndNot_1_T1
            def __call__(self, left: Vector512_1[AndNot_1_T], right: Vector512_1[AndNot_1_T]) -> Vector512_1[AndNot_1_T]:...


    # Skipped Any due to it being static, abstract and generic.

    Any : Any_MethodGroup
    class Any_MethodGroup:
        def __getitem__(self, t:typing.Type[Any_1_T1]) -> Any_1[Any_1_T1]: ...

        Any_1_T1 = typing.TypeVar('Any_1_T1')
        class Any_1(typing.Generic[Any_1_T1]):
            Any_1_T = Vector512_0.Any_MethodGroup.Any_1_T1
            def __call__(self, vector: Vector512_1[Any_1_T], value: Any_1_T) -> bool:...


    # Skipped AnyWhereAllBitsSet due to it being static, abstract and generic.

    AnyWhereAllBitsSet : AnyWhereAllBitsSet_MethodGroup
    class AnyWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[AnyWhereAllBitsSet_1_T1]) -> AnyWhereAllBitsSet_1[AnyWhereAllBitsSet_1_T1]: ...

        AnyWhereAllBitsSet_1_T1 = typing.TypeVar('AnyWhereAllBitsSet_1_T1')
        class AnyWhereAllBitsSet_1(typing.Generic[AnyWhereAllBitsSet_1_T1]):
            AnyWhereAllBitsSet_1_T = Vector512_0.AnyWhereAllBitsSet_MethodGroup.AnyWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector512_1[AnyWhereAllBitsSet_1_T]) -> bool:...


    # Skipped As due to it being static, abstract and generic.

    As : As_MethodGroup
    class As_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[As_2_T1], typing.Type[As_2_T2]]) -> As_2[As_2_T1, As_2_T2]: ...

        As_2_T1 = typing.TypeVar('As_2_T1')
        As_2_T2 = typing.TypeVar('As_2_T2')
        class As_2(typing.Generic[As_2_T1, As_2_T2]):
            As_2_TFrom = Vector512_0.As_MethodGroup.As_2_T1
            As_2_TTo = Vector512_0.As_MethodGroup.As_2_T2
            def __call__(self, vector: Vector512_1[As_2_TFrom]) -> Vector512_1[As_2_TTo]:...


    # Skipped AsByte due to it being static, abstract and generic.

    AsByte : AsByte_MethodGroup
    class AsByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsByte_1_T1]) -> AsByte_1[AsByte_1_T1]: ...

        AsByte_1_T1 = typing.TypeVar('AsByte_1_T1')
        class AsByte_1(typing.Generic[AsByte_1_T1]):
            AsByte_1_T = Vector512_0.AsByte_MethodGroup.AsByte_1_T1
            def __call__(self, vector: Vector512_1[AsByte_1_T]) -> Vector512_1[int]:...


    # Skipped AsDouble due to it being static, abstract and generic.

    AsDouble : AsDouble_MethodGroup
    class AsDouble_MethodGroup:
        def __getitem__(self, t:typing.Type[AsDouble_1_T1]) -> AsDouble_1[AsDouble_1_T1]: ...

        AsDouble_1_T1 = typing.TypeVar('AsDouble_1_T1')
        class AsDouble_1(typing.Generic[AsDouble_1_T1]):
            AsDouble_1_T = Vector512_0.AsDouble_MethodGroup.AsDouble_1_T1
            def __call__(self, vector: Vector512_1[AsDouble_1_T]) -> Vector512_1[float]:...


    # Skipped AsInt16 due to it being static, abstract and generic.

    AsInt16 : AsInt16_MethodGroup
    class AsInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt16_1_T1]) -> AsInt16_1[AsInt16_1_T1]: ...

        AsInt16_1_T1 = typing.TypeVar('AsInt16_1_T1')
        class AsInt16_1(typing.Generic[AsInt16_1_T1]):
            AsInt16_1_T = Vector512_0.AsInt16_MethodGroup.AsInt16_1_T1
            def __call__(self, vector: Vector512_1[AsInt16_1_T]) -> Vector512_1[int]:...


    # Skipped AsInt32 due to it being static, abstract and generic.

    AsInt32 : AsInt32_MethodGroup
    class AsInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt32_1_T1]) -> AsInt32_1[AsInt32_1_T1]: ...

        AsInt32_1_T1 = typing.TypeVar('AsInt32_1_T1')
        class AsInt32_1(typing.Generic[AsInt32_1_T1]):
            AsInt32_1_T = Vector512_0.AsInt32_MethodGroup.AsInt32_1_T1
            def __call__(self, vector: Vector512_1[AsInt32_1_T]) -> Vector512_1[int]:...


    # Skipped AsInt64 due to it being static, abstract and generic.

    AsInt64 : AsInt64_MethodGroup
    class AsInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt64_1_T1]) -> AsInt64_1[AsInt64_1_T1]: ...

        AsInt64_1_T1 = typing.TypeVar('AsInt64_1_T1')
        class AsInt64_1(typing.Generic[AsInt64_1_T1]):
            AsInt64_1_T = Vector512_0.AsInt64_MethodGroup.AsInt64_1_T1
            def __call__(self, vector: Vector512_1[AsInt64_1_T]) -> Vector512_1[int]:...


    # Skipped AsNInt due to it being static, abstract and generic.

    AsNInt : AsNInt_MethodGroup
    class AsNInt_MethodGroup:
        def __getitem__(self, t:typing.Type[AsNInt_1_T1]) -> AsNInt_1[AsNInt_1_T1]: ...

        AsNInt_1_T1 = typing.TypeVar('AsNInt_1_T1')
        class AsNInt_1(typing.Generic[AsNInt_1_T1]):
            AsNInt_1_T = Vector512_0.AsNInt_MethodGroup.AsNInt_1_T1
            def __call__(self, vector: Vector512_1[AsNInt_1_T]) -> Vector512_1[int]:...


    # Skipped AsNUInt due to it being static, abstract and generic.

    AsNUInt : AsNUInt_MethodGroup
    class AsNUInt_MethodGroup:
        def __getitem__(self, t:typing.Type[AsNUInt_1_T1]) -> AsNUInt_1[AsNUInt_1_T1]: ...

        AsNUInt_1_T1 = typing.TypeVar('AsNUInt_1_T1')
        class AsNUInt_1(typing.Generic[AsNUInt_1_T1]):
            AsNUInt_1_T = Vector512_0.AsNUInt_MethodGroup.AsNUInt_1_T1
            def __call__(self, vector: Vector512_1[AsNUInt_1_T]) -> Vector512_1[UIntPtr]:...


    # Skipped AsSByte due to it being static, abstract and generic.

    AsSByte : AsSByte_MethodGroup
    class AsSByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsSByte_1_T1]) -> AsSByte_1[AsSByte_1_T1]: ...

        AsSByte_1_T1 = typing.TypeVar('AsSByte_1_T1')
        class AsSByte_1(typing.Generic[AsSByte_1_T1]):
            AsSByte_1_T = Vector512_0.AsSByte_MethodGroup.AsSByte_1_T1
            def __call__(self, vector: Vector512_1[AsSByte_1_T]) -> Vector512_1[int]:...


    # Skipped AsSingle due to it being static, abstract and generic.

    AsSingle : AsSingle_MethodGroup
    class AsSingle_MethodGroup:
        def __getitem__(self, t:typing.Type[AsSingle_1_T1]) -> AsSingle_1[AsSingle_1_T1]: ...

        AsSingle_1_T1 = typing.TypeVar('AsSingle_1_T1')
        class AsSingle_1(typing.Generic[AsSingle_1_T1]):
            AsSingle_1_T = Vector512_0.AsSingle_MethodGroup.AsSingle_1_T1
            def __call__(self, vector: Vector512_1[AsSingle_1_T]) -> Vector512_1[float]:...


    # Skipped AsUInt16 due to it being static, abstract and generic.

    AsUInt16 : AsUInt16_MethodGroup
    class AsUInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt16_1_T1]) -> AsUInt16_1[AsUInt16_1_T1]: ...

        AsUInt16_1_T1 = typing.TypeVar('AsUInt16_1_T1')
        class AsUInt16_1(typing.Generic[AsUInt16_1_T1]):
            AsUInt16_1_T = Vector512_0.AsUInt16_MethodGroup.AsUInt16_1_T1
            def __call__(self, vector: Vector512_1[AsUInt16_1_T]) -> Vector512_1[int]:...


    # Skipped AsUInt32 due to it being static, abstract and generic.

    AsUInt32 : AsUInt32_MethodGroup
    class AsUInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt32_1_T1]) -> AsUInt32_1[AsUInt32_1_T1]: ...

        AsUInt32_1_T1 = typing.TypeVar('AsUInt32_1_T1')
        class AsUInt32_1(typing.Generic[AsUInt32_1_T1]):
            AsUInt32_1_T = Vector512_0.AsUInt32_MethodGroup.AsUInt32_1_T1
            def __call__(self, vector: Vector512_1[AsUInt32_1_T]) -> Vector512_1[int]:...


    # Skipped AsUInt64 due to it being static, abstract and generic.

    AsUInt64 : AsUInt64_MethodGroup
    class AsUInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt64_1_T1]) -> AsUInt64_1[AsUInt64_1_T1]: ...

        AsUInt64_1_T1 = typing.TypeVar('AsUInt64_1_T1')
        class AsUInt64_1(typing.Generic[AsUInt64_1_T1]):
            AsUInt64_1_T = Vector512_0.AsUInt64_MethodGroup.AsUInt64_1_T1
            def __call__(self, vector: Vector512_1[AsUInt64_1_T]) -> Vector512_1[int]:...


    # Skipped AsVector due to it being static, abstract and generic.

    AsVector : AsVector_MethodGroup
    class AsVector_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVector_1_T1]) -> AsVector_1[AsVector_1_T1]: ...

        AsVector_1_T1 = typing.TypeVar('AsVector_1_T1')
        class AsVector_1(typing.Generic[AsVector_1_T1]):
            AsVector_1_T = Vector512_0.AsVector_MethodGroup.AsVector_1_T1
            def __call__(self, value: Vector512_1[AsVector_1_T]) -> Vector_1[AsVector_1_T]:...


    # Skipped AsVector512 due to it being static, abstract and generic.

    AsVector512 : AsVector512_MethodGroup
    class AsVector512_MethodGroup:
        def __getitem__(self, t:typing.Type[AsVector512_1_T1]) -> AsVector512_1[AsVector512_1_T1]: ...

        AsVector512_1_T1 = typing.TypeVar('AsVector512_1_T1')
        class AsVector512_1(typing.Generic[AsVector512_1_T1]):
            AsVector512_1_T = Vector512_0.AsVector512_MethodGroup.AsVector512_1_T1
            def __call__(self, value: Vector_1[AsVector512_1_T]) -> Vector512_1[AsVector512_1_T]:...


    # Skipped BitwiseAnd due to it being static, abstract and generic.

    BitwiseAnd : BitwiseAnd_MethodGroup
    class BitwiseAnd_MethodGroup:
        def __getitem__(self, t:typing.Type[BitwiseAnd_1_T1]) -> BitwiseAnd_1[BitwiseAnd_1_T1]: ...

        BitwiseAnd_1_T1 = typing.TypeVar('BitwiseAnd_1_T1')
        class BitwiseAnd_1(typing.Generic[BitwiseAnd_1_T1]):
            BitwiseAnd_1_T = Vector512_0.BitwiseAnd_MethodGroup.BitwiseAnd_1_T1
            def __call__(self, left: Vector512_1[BitwiseAnd_1_T], right: Vector512_1[BitwiseAnd_1_T]) -> Vector512_1[BitwiseAnd_1_T]:...


    # Skipped BitwiseOr due to it being static, abstract and generic.

    BitwiseOr : BitwiseOr_MethodGroup
    class BitwiseOr_MethodGroup:
        def __getitem__(self, t:typing.Type[BitwiseOr_1_T1]) -> BitwiseOr_1[BitwiseOr_1_T1]: ...

        BitwiseOr_1_T1 = typing.TypeVar('BitwiseOr_1_T1')
        class BitwiseOr_1(typing.Generic[BitwiseOr_1_T1]):
            BitwiseOr_1_T = Vector512_0.BitwiseOr_MethodGroup.BitwiseOr_1_T1
            def __call__(self, left: Vector512_1[BitwiseOr_1_T], right: Vector512_1[BitwiseOr_1_T]) -> Vector512_1[BitwiseOr_1_T]:...


    # Skipped Ceiling due to it being static, abstract and generic.

    Ceiling : Ceiling_MethodGroup
    class Ceiling_MethodGroup:
        def __call__(self, vector: Vector512_1[float]) -> Vector512_1[float]:...
        # Method Ceiling(vector : Vector512`1) was skipped since it collides with above method

    # Skipped Clamp due to it being static, abstract and generic.

    Clamp : Clamp_MethodGroup
    class Clamp_MethodGroup:
        def __getitem__(self, t:typing.Type[Clamp_1_T1]) -> Clamp_1[Clamp_1_T1]: ...

        Clamp_1_T1 = typing.TypeVar('Clamp_1_T1')
        class Clamp_1(typing.Generic[Clamp_1_T1]):
            Clamp_1_T = Vector512_0.Clamp_MethodGroup.Clamp_1_T1
            def __call__(self, value: Vector512_1[Clamp_1_T], min: Vector512_1[Clamp_1_T], max: Vector512_1[Clamp_1_T]) -> Vector512_1[Clamp_1_T]:...


    # Skipped ClampNative due to it being static, abstract and generic.

    ClampNative : ClampNative_MethodGroup
    class ClampNative_MethodGroup:
        def __getitem__(self, t:typing.Type[ClampNative_1_T1]) -> ClampNative_1[ClampNative_1_T1]: ...

        ClampNative_1_T1 = typing.TypeVar('ClampNative_1_T1')
        class ClampNative_1(typing.Generic[ClampNative_1_T1]):
            ClampNative_1_T = Vector512_0.ClampNative_MethodGroup.ClampNative_1_T1
            def __call__(self, value: Vector512_1[ClampNative_1_T], min: Vector512_1[ClampNative_1_T], max: Vector512_1[ClampNative_1_T]) -> Vector512_1[ClampNative_1_T]:...


    # Skipped ConditionalSelect due to it being static, abstract and generic.

    ConditionalSelect : ConditionalSelect_MethodGroup
    class ConditionalSelect_MethodGroup:
        def __getitem__(self, t:typing.Type[ConditionalSelect_1_T1]) -> ConditionalSelect_1[ConditionalSelect_1_T1]: ...

        ConditionalSelect_1_T1 = typing.TypeVar('ConditionalSelect_1_T1')
        class ConditionalSelect_1(typing.Generic[ConditionalSelect_1_T1]):
            ConditionalSelect_1_T = Vector512_0.ConditionalSelect_MethodGroup.ConditionalSelect_1_T1
            def __call__(self, condition: Vector512_1[ConditionalSelect_1_T], left: Vector512_1[ConditionalSelect_1_T], right: Vector512_1[ConditionalSelect_1_T]) -> Vector512_1[ConditionalSelect_1_T]:...


    # Skipped ConvertToDouble due to it being static, abstract and generic.

    ConvertToDouble : ConvertToDouble_MethodGroup
    class ConvertToDouble_MethodGroup:
        def __call__(self, vector: Vector512_1[int]) -> Vector512_1[float]:...
        # Method ConvertToDouble(vector : Vector512`1) was skipped since it collides with above method

    # Skipped ConvertToSingle due to it being static, abstract and generic.

    ConvertToSingle : ConvertToSingle_MethodGroup
    class ConvertToSingle_MethodGroup:
        def __call__(self, vector: Vector512_1[int]) -> Vector512_1[float]:...
        # Method ConvertToSingle(vector : Vector512`1) was skipped since it collides with above method

    # Skipped CopySign due to it being static, abstract and generic.

    CopySign : CopySign_MethodGroup
    class CopySign_MethodGroup:
        def __getitem__(self, t:typing.Type[CopySign_1_T1]) -> CopySign_1[CopySign_1_T1]: ...

        CopySign_1_T1 = typing.TypeVar('CopySign_1_T1')
        class CopySign_1(typing.Generic[CopySign_1_T1]):
            CopySign_1_T = Vector512_0.CopySign_MethodGroup.CopySign_1_T1
            def __call__(self, value: Vector512_1[CopySign_1_T], sign: Vector512_1[CopySign_1_T]) -> Vector512_1[CopySign_1_T]:...


    # Skipped CopyTo due to it being static, abstract and generic.

    CopyTo : CopyTo_MethodGroup
    class CopyTo_MethodGroup:
        def __getitem__(self, t:typing.Type[CopyTo_1_T1]) -> CopyTo_1[CopyTo_1_T1]: ...

        CopyTo_1_T1 = typing.TypeVar('CopyTo_1_T1')
        class CopyTo_1(typing.Generic[CopyTo_1_T1]):
            CopyTo_1_T = Vector512_0.CopyTo_MethodGroup.CopyTo_1_T1
            @typing.overload
            def __call__(self, vector: Vector512_1[CopyTo_1_T], destination: Array_1[CopyTo_1_T]) -> None:...
            @typing.overload
            def __call__(self, vector: Vector512_1[CopyTo_1_T], destination: Span_1[CopyTo_1_T]) -> None:...
            @typing.overload
            def __call__(self, vector: Vector512_1[CopyTo_1_T], destination: Array_1[CopyTo_1_T], startIndex: int) -> None:...


    # Skipped Cos due to it being static, abstract and generic.

    Cos : Cos_MethodGroup
    class Cos_MethodGroup:
        def __call__(self, vector: Vector512_1[float]) -> Vector512_1[float]:...
        # Method Cos(vector : Vector512`1) was skipped since it collides with above method

    # Skipped Count due to it being static, abstract and generic.

    Count : Count_MethodGroup
    class Count_MethodGroup:
        def __getitem__(self, t:typing.Type[Count_1_T1]) -> Count_1[Count_1_T1]: ...

        Count_1_T1 = typing.TypeVar('Count_1_T1')
        class Count_1(typing.Generic[Count_1_T1]):
            Count_1_T = Vector512_0.Count_MethodGroup.Count_1_T1
            def __call__(self, vector: Vector512_1[Count_1_T], value: Count_1_T) -> int:...


    # Skipped CountWhereAllBitsSet due to it being static, abstract and generic.

    CountWhereAllBitsSet : CountWhereAllBitsSet_MethodGroup
    class CountWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[CountWhereAllBitsSet_1_T1]) -> CountWhereAllBitsSet_1[CountWhereAllBitsSet_1_T1]: ...

        CountWhereAllBitsSet_1_T1 = typing.TypeVar('CountWhereAllBitsSet_1_T1')
        class CountWhereAllBitsSet_1(typing.Generic[CountWhereAllBitsSet_1_T1]):
            CountWhereAllBitsSet_1_T = Vector512_0.CountWhereAllBitsSet_MethodGroup.CountWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector512_1[CountWhereAllBitsSet_1_T]) -> int:...


    # Skipped Create due to it being static, abstract and generic.

    Create : Create_MethodGroup
    class Create_MethodGroup:
        def __getitem__(self, t:typing.Type[Create_1_T1]) -> Create_1[Create_1_T1]: ...

        Create_1_T1 = typing.TypeVar('Create_1_T1')
        class Create_1(typing.Generic[Create_1_T1]):
            Create_1_T = Vector512_0.Create_MethodGroup.Create_1_T1
            @typing.overload
            def __call__(self, values: Array_1[Create_1_T]) -> Vector512_1[Create_1_T]:...
            @typing.overload
            def __call__(self, value: Vector64_1[Create_1_T]) -> Vector512_1[Create_1_T]:...
            @typing.overload
            def __call__(self, value: Vector128_1[Create_1_T]) -> Vector512_1[Create_1_T]:...
            @typing.overload
            def __call__(self, value: Vector256_1[Create_1_T]) -> Vector512_1[Create_1_T]:...
            @typing.overload
            def __call__(self, values: ReadOnlySpan_1[Create_1_T]) -> Vector512_1[Create_1_T]:...
            @typing.overload
            def __call__(self, value: Create_1_T) -> Vector512_1[Create_1_T]:...
            @typing.overload
            def __call__(self, values: Array_1[Create_1_T], index: int) -> Vector512_1[Create_1_T]:...
            @typing.overload
            def __call__(self, lower: Vector256_1[Create_1_T], upper: Vector256_1[Create_1_T]) -> Vector512_1[Create_1_T]:...

        @typing.overload
        def __call__(self, value: float) -> Vector512_1[float]:...
        # Method Create(value : Single) was skipped since it collides with above method
        # Method Create(value : Byte) was skipped since it collides with above method
        # Method Create(value : Int16) was skipped since it collides with above method
        # Method Create(value : Int32) was skipped since it collides with above method
        # Method Create(value : Int64) was skipped since it collides with above method
        # Method Create(value : SByte) was skipped since it collides with above method
        # Method Create(value : UInt16) was skipped since it collides with above method
        # Method Create(value : UInt32) was skipped since it collides with above method
        # Method Create(value : UInt64) was skipped since it collides with above method
        # Method Create(value : IntPtr) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: UIntPtr) -> Vector512_1[UIntPtr]:...
        @typing.overload
        def __call__(self, lower: Vector256_1[float], upper: Vector256_1[float]) -> Vector512_1[float]:...
        # Method Create(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method Create(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method Create(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method Create(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method Create(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method Create(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method Create(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method Create(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method Create(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        # Method Create(lower : Vector256`1, upper : Vector256`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, lower: Vector256_1[UIntPtr], upper: Vector256_1[UIntPtr]) -> Vector512_1[UIntPtr]:...
        @typing.overload
        def __call__(self, e0: float, e1: float, e2: float, e3: float, e4: float, e5: float, e6: float, e7: float) -> Vector512_1[float]:...
        # Method Create(e0 : Int64, e1 : Int64, e2 : Int64, e3 : Int64, e4 : Int64, e5 : Int64, e6 : Int64, e7 : Int64) was skipped since it collides with above method
        # Method Create(e0 : UInt64, e1 : UInt64, e2 : UInt64, e3 : UInt64, e4 : UInt64, e5 : UInt64, e6 : UInt64, e7 : UInt64) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: float, e1: float, e2: float, e3: float, e4: float, e5: float, e6: float, e7: float, e8: float, e9: float, e10: float, e11: float, e12: float, e13: float, e14: float, e15: float) -> Vector512_1[float]:...
        # Method Create(e0 : Int32, e1 : Int32, e2 : Int32, e3 : Int32, e4 : Int32, e5 : Int32, e6 : Int32, e7 : Int32, e8 : Int32, e9 : Int32, e10 : Int32, e11 : Int32, e12 : Int32, e13 : Int32, e14 : Int32, e15 : Int32) was skipped since it collides with above method
        # Method Create(e0 : UInt32, e1 : UInt32, e2 : UInt32, e3 : UInt32, e4 : UInt32, e5 : UInt32, e6 : UInt32, e7 : UInt32, e8 : UInt32, e9 : UInt32, e10 : UInt32, e11 : UInt32, e12 : UInt32, e13 : UInt32, e14 : UInt32, e15 : UInt32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int, e8: int, e9: int, e10: int, e11: int, e12: int, e13: int, e14: int, e15: int, e16: int, e17: int, e18: int, e19: int, e20: int, e21: int, e22: int, e23: int, e24: int, e25: int, e26: int, e27: int, e28: int, e29: int, e30: int, e31: int) -> Vector512_1[int]:...
        # Method Create(e0 : UInt16, e1 : UInt16, e2 : UInt16, e3 : UInt16, e4 : UInt16, e5 : UInt16, e6 : UInt16, e7 : UInt16, e8 : UInt16, e9 : UInt16, e10 : UInt16, e11 : UInt16, e12 : UInt16, e13 : UInt16, e14 : UInt16, e15 : UInt16, e16 : UInt16, e17 : UInt16, e18 : UInt16, e19 : UInt16, e20 : UInt16, e21 : UInt16, e22 : UInt16, e23 : UInt16, e24 : UInt16, e25 : UInt16, e26 : UInt16, e27 : UInt16, e28 : UInt16, e29 : UInt16, e30 : UInt16, e31 : UInt16) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int, e8: int, e9: int, e10: int, e11: int, e12: int, e13: int, e14: int, e15: int, e16: int, e17: int, e18: int, e19: int, e20: int, e21: int, e22: int, e23: int, e24: int, e25: int, e26: int, e27: int, e28: int, e29: int, e30: int, e31: int, e32: int, e33: int, e34: int, e35: int, e36: int, e37: int, e38: int, e39: int, e40: int, e41: int, e42: int, e43: int, e44: int, e45: int, e46: int, e47: int, e48: int, e49: int, e50: int, e51: int, e52: int, e53: int, e54: int, e55: int, e56: int, e57: int, e58: int, e59: int, e60: int, e61: int, e62: int, e63: int) -> Vector512_1[int]:...
        # Method Create(e0 : SByte, e1 : SByte, e2 : SByte, e3 : SByte, e4 : SByte, e5 : SByte, e6 : SByte, e7 : SByte, e8 : SByte, e9 : SByte, e10 : SByte, e11 : SByte, e12 : SByte, e13 : SByte, e14 : SByte, e15 : SByte, e16 : SByte, e17 : SByte, e18 : SByte, e19 : SByte, e20 : SByte, e21 : SByte, e22 : SByte, e23 : SByte, e24 : SByte, e25 : SByte, e26 : SByte, e27 : SByte, e28 : SByte, e29 : SByte, e30 : SByte, e31 : SByte, e32 : SByte, e33 : SByte, e34 : SByte, e35 : SByte, e36 : SByte, e37 : SByte, e38 : SByte, e39 : SByte, e40 : SByte, e41 : SByte, e42 : SByte, e43 : SByte, e44 : SByte, e45 : SByte, e46 : SByte, e47 : SByte, e48 : SByte, e49 : SByte, e50 : SByte, e51 : SByte, e52 : SByte, e53 : SByte, e54 : SByte, e55 : SByte, e56 : SByte, e57 : SByte, e58 : SByte, e59 : SByte, e60 : SByte, e61 : SByte, e62 : SByte, e63 : SByte) was skipped since it collides with above method

    # Skipped CreateScalar due to it being static, abstract and generic.

    CreateScalar : CreateScalar_MethodGroup
    class CreateScalar_MethodGroup:
        def __getitem__(self, t:typing.Type[CreateScalar_1_T1]) -> CreateScalar_1[CreateScalar_1_T1]: ...

        CreateScalar_1_T1 = typing.TypeVar('CreateScalar_1_T1')
        class CreateScalar_1(typing.Generic[CreateScalar_1_T1]):
            CreateScalar_1_T = Vector512_0.CreateScalar_MethodGroup.CreateScalar_1_T1
            def __call__(self, value: CreateScalar_1_T) -> Vector512_1[CreateScalar_1_T]:...

        @typing.overload
        def __call__(self, value: float) -> Vector512_1[float]:...
        # Method CreateScalar(value : Single) was skipped since it collides with above method
        # Method CreateScalar(value : Byte) was skipped since it collides with above method
        # Method CreateScalar(value : Int16) was skipped since it collides with above method
        # Method CreateScalar(value : Int32) was skipped since it collides with above method
        # Method CreateScalar(value : Int64) was skipped since it collides with above method
        # Method CreateScalar(value : SByte) was skipped since it collides with above method
        # Method CreateScalar(value : UInt16) was skipped since it collides with above method
        # Method CreateScalar(value : UInt32) was skipped since it collides with above method
        # Method CreateScalar(value : UInt64) was skipped since it collides with above method
        # Method CreateScalar(value : IntPtr) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: UIntPtr) -> Vector512_1[UIntPtr]:...

    # Skipped CreateScalarUnsafe due to it being static, abstract and generic.

    CreateScalarUnsafe : CreateScalarUnsafe_MethodGroup
    class CreateScalarUnsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[CreateScalarUnsafe_1_T1]) -> CreateScalarUnsafe_1[CreateScalarUnsafe_1_T1]: ...

        CreateScalarUnsafe_1_T1 = typing.TypeVar('CreateScalarUnsafe_1_T1')
        class CreateScalarUnsafe_1(typing.Generic[CreateScalarUnsafe_1_T1]):
            CreateScalarUnsafe_1_T = Vector512_0.CreateScalarUnsafe_MethodGroup.CreateScalarUnsafe_1_T1
            def __call__(self, value: CreateScalarUnsafe_1_T) -> Vector512_1[CreateScalarUnsafe_1_T]:...

        @typing.overload
        def __call__(self, value: float) -> Vector512_1[float]:...
        # Method CreateScalarUnsafe(value : Single) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Byte) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int16) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int32) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int64) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : SByte) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt16) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt32) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt64) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : IntPtr) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: UIntPtr) -> Vector512_1[UIntPtr]:...

    # Skipped CreateSequence due to it being static, abstract and generic.

    CreateSequence : CreateSequence_MethodGroup
    class CreateSequence_MethodGroup:
        def __getitem__(self, t:typing.Type[CreateSequence_1_T1]) -> CreateSequence_1[CreateSequence_1_T1]: ...

        CreateSequence_1_T1 = typing.TypeVar('CreateSequence_1_T1')
        class CreateSequence_1(typing.Generic[CreateSequence_1_T1]):
            CreateSequence_1_T = Vector512_0.CreateSequence_MethodGroup.CreateSequence_1_T1
            def __call__(self, start: CreateSequence_1_T, step: CreateSequence_1_T) -> Vector512_1[CreateSequence_1_T]:...


    # Skipped DegreesToRadians due to it being static, abstract and generic.

    DegreesToRadians : DegreesToRadians_MethodGroup
    class DegreesToRadians_MethodGroup:
        def __call__(self, degrees: Vector512_1[float]) -> Vector512_1[float]:...
        # Method DegreesToRadians(degrees : Vector512`1) was skipped since it collides with above method

    # Skipped Divide due to it being static, abstract and generic.

    Divide : Divide_MethodGroup
    class Divide_MethodGroup:
        def __getitem__(self, t:typing.Type[Divide_1_T1]) -> Divide_1[Divide_1_T1]: ...

        Divide_1_T1 = typing.TypeVar('Divide_1_T1')
        class Divide_1(typing.Generic[Divide_1_T1]):
            Divide_1_T = Vector512_0.Divide_MethodGroup.Divide_1_T1
            @typing.overload
            def __call__(self, left: Vector512_1[Divide_1_T], right: Vector512_1[Divide_1_T]) -> Vector512_1[Divide_1_T]:...
            @typing.overload
            def __call__(self, left: Vector512_1[Divide_1_T], right: Divide_1_T) -> Vector512_1[Divide_1_T]:...


    # Skipped Dot due to it being static, abstract and generic.

    Dot : Dot_MethodGroup
    class Dot_MethodGroup:
        def __getitem__(self, t:typing.Type[Dot_1_T1]) -> Dot_1[Dot_1_T1]: ...

        Dot_1_T1 = typing.TypeVar('Dot_1_T1')
        class Dot_1(typing.Generic[Dot_1_T1]):
            Dot_1_T = Vector512_0.Dot_MethodGroup.Dot_1_T1
            def __call__(self, left: Vector512_1[Dot_1_T], right: Vector512_1[Dot_1_T]) -> Dot_1_T:...


    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        def __getitem__(self, t:typing.Type[Equals_1_T1]) -> Equals_1[Equals_1_T1]: ...

        Equals_1_T1 = typing.TypeVar('Equals_1_T1')
        class Equals_1(typing.Generic[Equals_1_T1]):
            Equals_1_T = Vector512_0.Equals_MethodGroup.Equals_1_T1
            def __call__(self, left: Vector512_1[Equals_1_T], right: Vector512_1[Equals_1_T]) -> Vector512_1[Equals_1_T]:...


    # Skipped EqualsAll due to it being static, abstract and generic.

    EqualsAll : EqualsAll_MethodGroup
    class EqualsAll_MethodGroup:
        def __getitem__(self, t:typing.Type[EqualsAll_1_T1]) -> EqualsAll_1[EqualsAll_1_T1]: ...

        EqualsAll_1_T1 = typing.TypeVar('EqualsAll_1_T1')
        class EqualsAll_1(typing.Generic[EqualsAll_1_T1]):
            EqualsAll_1_T = Vector512_0.EqualsAll_MethodGroup.EqualsAll_1_T1
            def __call__(self, left: Vector512_1[EqualsAll_1_T], right: Vector512_1[EqualsAll_1_T]) -> bool:...


    # Skipped EqualsAny due to it being static, abstract and generic.

    EqualsAny : EqualsAny_MethodGroup
    class EqualsAny_MethodGroup:
        def __getitem__(self, t:typing.Type[EqualsAny_1_T1]) -> EqualsAny_1[EqualsAny_1_T1]: ...

        EqualsAny_1_T1 = typing.TypeVar('EqualsAny_1_T1')
        class EqualsAny_1(typing.Generic[EqualsAny_1_T1]):
            EqualsAny_1_T = Vector512_0.EqualsAny_MethodGroup.EqualsAny_1_T1
            def __call__(self, left: Vector512_1[EqualsAny_1_T], right: Vector512_1[EqualsAny_1_T]) -> bool:...


    # Skipped Exp due to it being static, abstract and generic.

    Exp : Exp_MethodGroup
    class Exp_MethodGroup:
        def __call__(self, vector: Vector512_1[float]) -> Vector512_1[float]:...
        # Method Exp(vector : Vector512`1) was skipped since it collides with above method

    # Skipped ExtractMostSignificantBits due to it being static, abstract and generic.

    ExtractMostSignificantBits : ExtractMostSignificantBits_MethodGroup
    class ExtractMostSignificantBits_MethodGroup:
        def __getitem__(self, t:typing.Type[ExtractMostSignificantBits_1_T1]) -> ExtractMostSignificantBits_1[ExtractMostSignificantBits_1_T1]: ...

        ExtractMostSignificantBits_1_T1 = typing.TypeVar('ExtractMostSignificantBits_1_T1')
        class ExtractMostSignificantBits_1(typing.Generic[ExtractMostSignificantBits_1_T1]):
            ExtractMostSignificantBits_1_T = Vector512_0.ExtractMostSignificantBits_MethodGroup.ExtractMostSignificantBits_1_T1
            def __call__(self, vector: Vector512_1[ExtractMostSignificantBits_1_T]) -> int:...


    # Skipped Floor due to it being static, abstract and generic.

    Floor : Floor_MethodGroup
    class Floor_MethodGroup:
        def __call__(self, vector: Vector512_1[float]) -> Vector512_1[float]:...
        # Method Floor(vector : Vector512`1) was skipped since it collides with above method

    # Skipped FusedMultiplyAdd due to it being static, abstract and generic.

    FusedMultiplyAdd : FusedMultiplyAdd_MethodGroup
    class FusedMultiplyAdd_MethodGroup:
        def __call__(self, left: Vector512_1[float], right: Vector512_1[float], addend: Vector512_1[float]) -> Vector512_1[float]:...
        # Method FusedMultiplyAdd(left : Vector512`1, right : Vector512`1, addend : Vector512`1) was skipped since it collides with above method

    # Skipped GetElement due to it being static, abstract and generic.

    GetElement : GetElement_MethodGroup
    class GetElement_MethodGroup:
        def __getitem__(self, t:typing.Type[GetElement_1_T1]) -> GetElement_1[GetElement_1_T1]: ...

        GetElement_1_T1 = typing.TypeVar('GetElement_1_T1')
        class GetElement_1(typing.Generic[GetElement_1_T1]):
            GetElement_1_T = Vector512_0.GetElement_MethodGroup.GetElement_1_T1
            def __call__(self, vector: Vector512_1[GetElement_1_T], index: int) -> GetElement_1_T:...


    # Skipped GetLower due to it being static, abstract and generic.

    GetLower : GetLower_MethodGroup
    class GetLower_MethodGroup:
        def __getitem__(self, t:typing.Type[GetLower_1_T1]) -> GetLower_1[GetLower_1_T1]: ...

        GetLower_1_T1 = typing.TypeVar('GetLower_1_T1')
        class GetLower_1(typing.Generic[GetLower_1_T1]):
            GetLower_1_T = Vector512_0.GetLower_MethodGroup.GetLower_1_T1
            def __call__(self, vector: Vector512_1[GetLower_1_T]) -> Vector256_1[GetLower_1_T]:...


    # Skipped GetUpper due to it being static, abstract and generic.

    GetUpper : GetUpper_MethodGroup
    class GetUpper_MethodGroup:
        def __getitem__(self, t:typing.Type[GetUpper_1_T1]) -> GetUpper_1[GetUpper_1_T1]: ...

        GetUpper_1_T1 = typing.TypeVar('GetUpper_1_T1')
        class GetUpper_1(typing.Generic[GetUpper_1_T1]):
            GetUpper_1_T = Vector512_0.GetUpper_MethodGroup.GetUpper_1_T1
            def __call__(self, vector: Vector512_1[GetUpper_1_T]) -> Vector256_1[GetUpper_1_T]:...


    # Skipped GreaterThan due to it being static, abstract and generic.

    GreaterThan : GreaterThan_MethodGroup
    class GreaterThan_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThan_1_T1]) -> GreaterThan_1[GreaterThan_1_T1]: ...

        GreaterThan_1_T1 = typing.TypeVar('GreaterThan_1_T1')
        class GreaterThan_1(typing.Generic[GreaterThan_1_T1]):
            GreaterThan_1_T = Vector512_0.GreaterThan_MethodGroup.GreaterThan_1_T1
            def __call__(self, left: Vector512_1[GreaterThan_1_T], right: Vector512_1[GreaterThan_1_T]) -> Vector512_1[GreaterThan_1_T]:...


    # Skipped GreaterThanAll due to it being static, abstract and generic.

    GreaterThanAll : GreaterThanAll_MethodGroup
    class GreaterThanAll_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanAll_1_T1]) -> GreaterThanAll_1[GreaterThanAll_1_T1]: ...

        GreaterThanAll_1_T1 = typing.TypeVar('GreaterThanAll_1_T1')
        class GreaterThanAll_1(typing.Generic[GreaterThanAll_1_T1]):
            GreaterThanAll_1_T = Vector512_0.GreaterThanAll_MethodGroup.GreaterThanAll_1_T1
            def __call__(self, left: Vector512_1[GreaterThanAll_1_T], right: Vector512_1[GreaterThanAll_1_T]) -> bool:...


    # Skipped GreaterThanAny due to it being static, abstract and generic.

    GreaterThanAny : GreaterThanAny_MethodGroup
    class GreaterThanAny_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanAny_1_T1]) -> GreaterThanAny_1[GreaterThanAny_1_T1]: ...

        GreaterThanAny_1_T1 = typing.TypeVar('GreaterThanAny_1_T1')
        class GreaterThanAny_1(typing.Generic[GreaterThanAny_1_T1]):
            GreaterThanAny_1_T = Vector512_0.GreaterThanAny_MethodGroup.GreaterThanAny_1_T1
            def __call__(self, left: Vector512_1[GreaterThanAny_1_T], right: Vector512_1[GreaterThanAny_1_T]) -> bool:...


    # Skipped GreaterThanOrEqual due to it being static, abstract and generic.

    GreaterThanOrEqual : GreaterThanOrEqual_MethodGroup
    class GreaterThanOrEqual_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqual_1_T1]) -> GreaterThanOrEqual_1[GreaterThanOrEqual_1_T1]: ...

        GreaterThanOrEqual_1_T1 = typing.TypeVar('GreaterThanOrEqual_1_T1')
        class GreaterThanOrEqual_1(typing.Generic[GreaterThanOrEqual_1_T1]):
            GreaterThanOrEqual_1_T = Vector512_0.GreaterThanOrEqual_MethodGroup.GreaterThanOrEqual_1_T1
            def __call__(self, left: Vector512_1[GreaterThanOrEqual_1_T], right: Vector512_1[GreaterThanOrEqual_1_T]) -> Vector512_1[GreaterThanOrEqual_1_T]:...


    # Skipped GreaterThanOrEqualAll due to it being static, abstract and generic.

    GreaterThanOrEqualAll : GreaterThanOrEqualAll_MethodGroup
    class GreaterThanOrEqualAll_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqualAll_1_T1]) -> GreaterThanOrEqualAll_1[GreaterThanOrEqualAll_1_T1]: ...

        GreaterThanOrEqualAll_1_T1 = typing.TypeVar('GreaterThanOrEqualAll_1_T1')
        class GreaterThanOrEqualAll_1(typing.Generic[GreaterThanOrEqualAll_1_T1]):
            GreaterThanOrEqualAll_1_T = Vector512_0.GreaterThanOrEqualAll_MethodGroup.GreaterThanOrEqualAll_1_T1
            def __call__(self, left: Vector512_1[GreaterThanOrEqualAll_1_T], right: Vector512_1[GreaterThanOrEqualAll_1_T]) -> bool:...


    # Skipped GreaterThanOrEqualAny due to it being static, abstract and generic.

    GreaterThanOrEqualAny : GreaterThanOrEqualAny_MethodGroup
    class GreaterThanOrEqualAny_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqualAny_1_T1]) -> GreaterThanOrEqualAny_1[GreaterThanOrEqualAny_1_T1]: ...

        GreaterThanOrEqualAny_1_T1 = typing.TypeVar('GreaterThanOrEqualAny_1_T1')
        class GreaterThanOrEqualAny_1(typing.Generic[GreaterThanOrEqualAny_1_T1]):
            GreaterThanOrEqualAny_1_T = Vector512_0.GreaterThanOrEqualAny_MethodGroup.GreaterThanOrEqualAny_1_T1
            def __call__(self, left: Vector512_1[GreaterThanOrEqualAny_1_T], right: Vector512_1[GreaterThanOrEqualAny_1_T]) -> bool:...


    # Skipped Hypot due to it being static, abstract and generic.

    Hypot : Hypot_MethodGroup
    class Hypot_MethodGroup:
        def __call__(self, x: Vector512_1[float], y: Vector512_1[float]) -> Vector512_1[float]:...
        # Method Hypot(x : Vector512`1, y : Vector512`1) was skipped since it collides with above method

    # Skipped IndexOf due to it being static, abstract and generic.

    IndexOf : IndexOf_MethodGroup
    class IndexOf_MethodGroup:
        def __getitem__(self, t:typing.Type[IndexOf_1_T1]) -> IndexOf_1[IndexOf_1_T1]: ...

        IndexOf_1_T1 = typing.TypeVar('IndexOf_1_T1')
        class IndexOf_1(typing.Generic[IndexOf_1_T1]):
            IndexOf_1_T = Vector512_0.IndexOf_MethodGroup.IndexOf_1_T1
            def __call__(self, vector: Vector512_1[IndexOf_1_T], value: IndexOf_1_T) -> int:...


    # Skipped IndexOfWhereAllBitsSet due to it being static, abstract and generic.

    IndexOfWhereAllBitsSet : IndexOfWhereAllBitsSet_MethodGroup
    class IndexOfWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[IndexOfWhereAllBitsSet_1_T1]) -> IndexOfWhereAllBitsSet_1[IndexOfWhereAllBitsSet_1_T1]: ...

        IndexOfWhereAllBitsSet_1_T1 = typing.TypeVar('IndexOfWhereAllBitsSet_1_T1')
        class IndexOfWhereAllBitsSet_1(typing.Generic[IndexOfWhereAllBitsSet_1_T1]):
            IndexOfWhereAllBitsSet_1_T = Vector512_0.IndexOfWhereAllBitsSet_MethodGroup.IndexOfWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector512_1[IndexOfWhereAllBitsSet_1_T]) -> int:...


    # Skipped IsEvenInteger due to it being static, abstract and generic.

    IsEvenInteger : IsEvenInteger_MethodGroup
    class IsEvenInteger_MethodGroup:
        def __getitem__(self, t:typing.Type[IsEvenInteger_1_T1]) -> IsEvenInteger_1[IsEvenInteger_1_T1]: ...

        IsEvenInteger_1_T1 = typing.TypeVar('IsEvenInteger_1_T1')
        class IsEvenInteger_1(typing.Generic[IsEvenInteger_1_T1]):
            IsEvenInteger_1_T = Vector512_0.IsEvenInteger_MethodGroup.IsEvenInteger_1_T1
            def __call__(self, vector: Vector512_1[IsEvenInteger_1_T]) -> Vector512_1[IsEvenInteger_1_T]:...


    # Skipped IsFinite due to it being static, abstract and generic.

    IsFinite : IsFinite_MethodGroup
    class IsFinite_MethodGroup:
        def __getitem__(self, t:typing.Type[IsFinite_1_T1]) -> IsFinite_1[IsFinite_1_T1]: ...

        IsFinite_1_T1 = typing.TypeVar('IsFinite_1_T1')
        class IsFinite_1(typing.Generic[IsFinite_1_T1]):
            IsFinite_1_T = Vector512_0.IsFinite_MethodGroup.IsFinite_1_T1
            def __call__(self, vector: Vector512_1[IsFinite_1_T]) -> Vector512_1[IsFinite_1_T]:...


    # Skipped IsInfinity due to it being static, abstract and generic.

    IsInfinity : IsInfinity_MethodGroup
    class IsInfinity_MethodGroup:
        def __getitem__(self, t:typing.Type[IsInfinity_1_T1]) -> IsInfinity_1[IsInfinity_1_T1]: ...

        IsInfinity_1_T1 = typing.TypeVar('IsInfinity_1_T1')
        class IsInfinity_1(typing.Generic[IsInfinity_1_T1]):
            IsInfinity_1_T = Vector512_0.IsInfinity_MethodGroup.IsInfinity_1_T1
            def __call__(self, vector: Vector512_1[IsInfinity_1_T]) -> Vector512_1[IsInfinity_1_T]:...


    # Skipped IsInteger due to it being static, abstract and generic.

    IsInteger : IsInteger_MethodGroup
    class IsInteger_MethodGroup:
        def __getitem__(self, t:typing.Type[IsInteger_1_T1]) -> IsInteger_1[IsInteger_1_T1]: ...

        IsInteger_1_T1 = typing.TypeVar('IsInteger_1_T1')
        class IsInteger_1(typing.Generic[IsInteger_1_T1]):
            IsInteger_1_T = Vector512_0.IsInteger_MethodGroup.IsInteger_1_T1
            def __call__(self, vector: Vector512_1[IsInteger_1_T]) -> Vector512_1[IsInteger_1_T]:...


    # Skipped IsNaN due to it being static, abstract and generic.

    IsNaN : IsNaN_MethodGroup
    class IsNaN_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNaN_1_T1]) -> IsNaN_1[IsNaN_1_T1]: ...

        IsNaN_1_T1 = typing.TypeVar('IsNaN_1_T1')
        class IsNaN_1(typing.Generic[IsNaN_1_T1]):
            IsNaN_1_T = Vector512_0.IsNaN_MethodGroup.IsNaN_1_T1
            def __call__(self, vector: Vector512_1[IsNaN_1_T]) -> Vector512_1[IsNaN_1_T]:...


    # Skipped IsNegative due to it being static, abstract and generic.

    IsNegative : IsNegative_MethodGroup
    class IsNegative_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNegative_1_T1]) -> IsNegative_1[IsNegative_1_T1]: ...

        IsNegative_1_T1 = typing.TypeVar('IsNegative_1_T1')
        class IsNegative_1(typing.Generic[IsNegative_1_T1]):
            IsNegative_1_T = Vector512_0.IsNegative_MethodGroup.IsNegative_1_T1
            def __call__(self, vector: Vector512_1[IsNegative_1_T]) -> Vector512_1[IsNegative_1_T]:...


    # Skipped IsNegativeInfinity due to it being static, abstract and generic.

    IsNegativeInfinity : IsNegativeInfinity_MethodGroup
    class IsNegativeInfinity_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNegativeInfinity_1_T1]) -> IsNegativeInfinity_1[IsNegativeInfinity_1_T1]: ...

        IsNegativeInfinity_1_T1 = typing.TypeVar('IsNegativeInfinity_1_T1')
        class IsNegativeInfinity_1(typing.Generic[IsNegativeInfinity_1_T1]):
            IsNegativeInfinity_1_T = Vector512_0.IsNegativeInfinity_MethodGroup.IsNegativeInfinity_1_T1
            def __call__(self, vector: Vector512_1[IsNegativeInfinity_1_T]) -> Vector512_1[IsNegativeInfinity_1_T]:...


    # Skipped IsNormal due to it being static, abstract and generic.

    IsNormal : IsNormal_MethodGroup
    class IsNormal_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNormal_1_T1]) -> IsNormal_1[IsNormal_1_T1]: ...

        IsNormal_1_T1 = typing.TypeVar('IsNormal_1_T1')
        class IsNormal_1(typing.Generic[IsNormal_1_T1]):
            IsNormal_1_T = Vector512_0.IsNormal_MethodGroup.IsNormal_1_T1
            def __call__(self, vector: Vector512_1[IsNormal_1_T]) -> Vector512_1[IsNormal_1_T]:...


    # Skipped IsOddInteger due to it being static, abstract and generic.

    IsOddInteger : IsOddInteger_MethodGroup
    class IsOddInteger_MethodGroup:
        def __getitem__(self, t:typing.Type[IsOddInteger_1_T1]) -> IsOddInteger_1[IsOddInteger_1_T1]: ...

        IsOddInteger_1_T1 = typing.TypeVar('IsOddInteger_1_T1')
        class IsOddInteger_1(typing.Generic[IsOddInteger_1_T1]):
            IsOddInteger_1_T = Vector512_0.IsOddInteger_MethodGroup.IsOddInteger_1_T1
            def __call__(self, vector: Vector512_1[IsOddInteger_1_T]) -> Vector512_1[IsOddInteger_1_T]:...


    # Skipped IsPositive due to it being static, abstract and generic.

    IsPositive : IsPositive_MethodGroup
    class IsPositive_MethodGroup:
        def __getitem__(self, t:typing.Type[IsPositive_1_T1]) -> IsPositive_1[IsPositive_1_T1]: ...

        IsPositive_1_T1 = typing.TypeVar('IsPositive_1_T1')
        class IsPositive_1(typing.Generic[IsPositive_1_T1]):
            IsPositive_1_T = Vector512_0.IsPositive_MethodGroup.IsPositive_1_T1
            def __call__(self, vector: Vector512_1[IsPositive_1_T]) -> Vector512_1[IsPositive_1_T]:...


    # Skipped IsPositiveInfinity due to it being static, abstract and generic.

    IsPositiveInfinity : IsPositiveInfinity_MethodGroup
    class IsPositiveInfinity_MethodGroup:
        def __getitem__(self, t:typing.Type[IsPositiveInfinity_1_T1]) -> IsPositiveInfinity_1[IsPositiveInfinity_1_T1]: ...

        IsPositiveInfinity_1_T1 = typing.TypeVar('IsPositiveInfinity_1_T1')
        class IsPositiveInfinity_1(typing.Generic[IsPositiveInfinity_1_T1]):
            IsPositiveInfinity_1_T = Vector512_0.IsPositiveInfinity_MethodGroup.IsPositiveInfinity_1_T1
            def __call__(self, vector: Vector512_1[IsPositiveInfinity_1_T]) -> Vector512_1[IsPositiveInfinity_1_T]:...


    # Skipped IsSubnormal due to it being static, abstract and generic.

    IsSubnormal : IsSubnormal_MethodGroup
    class IsSubnormal_MethodGroup:
        def __getitem__(self, t:typing.Type[IsSubnormal_1_T1]) -> IsSubnormal_1[IsSubnormal_1_T1]: ...

        IsSubnormal_1_T1 = typing.TypeVar('IsSubnormal_1_T1')
        class IsSubnormal_1(typing.Generic[IsSubnormal_1_T1]):
            IsSubnormal_1_T = Vector512_0.IsSubnormal_MethodGroup.IsSubnormal_1_T1
            def __call__(self, vector: Vector512_1[IsSubnormal_1_T]) -> Vector512_1[IsSubnormal_1_T]:...


    # Skipped IsZero due to it being static, abstract and generic.

    IsZero : IsZero_MethodGroup
    class IsZero_MethodGroup:
        def __getitem__(self, t:typing.Type[IsZero_1_T1]) -> IsZero_1[IsZero_1_T1]: ...

        IsZero_1_T1 = typing.TypeVar('IsZero_1_T1')
        class IsZero_1(typing.Generic[IsZero_1_T1]):
            IsZero_1_T = Vector512_0.IsZero_MethodGroup.IsZero_1_T1
            def __call__(self, vector: Vector512_1[IsZero_1_T]) -> Vector512_1[IsZero_1_T]:...


    # Skipped LastIndexOf due to it being static, abstract and generic.

    LastIndexOf : LastIndexOf_MethodGroup
    class LastIndexOf_MethodGroup:
        def __getitem__(self, t:typing.Type[LastIndexOf_1_T1]) -> LastIndexOf_1[LastIndexOf_1_T1]: ...

        LastIndexOf_1_T1 = typing.TypeVar('LastIndexOf_1_T1')
        class LastIndexOf_1(typing.Generic[LastIndexOf_1_T1]):
            LastIndexOf_1_T = Vector512_0.LastIndexOf_MethodGroup.LastIndexOf_1_T1
            def __call__(self, vector: Vector512_1[LastIndexOf_1_T], value: LastIndexOf_1_T) -> int:...


    # Skipped LastIndexOfWhereAllBitsSet due to it being static, abstract and generic.

    LastIndexOfWhereAllBitsSet : LastIndexOfWhereAllBitsSet_MethodGroup
    class LastIndexOfWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[LastIndexOfWhereAllBitsSet_1_T1]) -> LastIndexOfWhereAllBitsSet_1[LastIndexOfWhereAllBitsSet_1_T1]: ...

        LastIndexOfWhereAllBitsSet_1_T1 = typing.TypeVar('LastIndexOfWhereAllBitsSet_1_T1')
        class LastIndexOfWhereAllBitsSet_1(typing.Generic[LastIndexOfWhereAllBitsSet_1_T1]):
            LastIndexOfWhereAllBitsSet_1_T = Vector512_0.LastIndexOfWhereAllBitsSet_MethodGroup.LastIndexOfWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector512_1[LastIndexOfWhereAllBitsSet_1_T]) -> int:...


    # Skipped Lerp due to it being static, abstract and generic.

    Lerp : Lerp_MethodGroup
    class Lerp_MethodGroup:
        def __call__(self, x: Vector512_1[float], y: Vector512_1[float], amount: Vector512_1[float]) -> Vector512_1[float]:...
        # Method Lerp(x : Vector512`1, y : Vector512`1, amount : Vector512`1) was skipped since it collides with above method

    # Skipped LessThan due to it being static, abstract and generic.

    LessThan : LessThan_MethodGroup
    class LessThan_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThan_1_T1]) -> LessThan_1[LessThan_1_T1]: ...

        LessThan_1_T1 = typing.TypeVar('LessThan_1_T1')
        class LessThan_1(typing.Generic[LessThan_1_T1]):
            LessThan_1_T = Vector512_0.LessThan_MethodGroup.LessThan_1_T1
            def __call__(self, left: Vector512_1[LessThan_1_T], right: Vector512_1[LessThan_1_T]) -> Vector512_1[LessThan_1_T]:...


    # Skipped LessThanAll due to it being static, abstract and generic.

    LessThanAll : LessThanAll_MethodGroup
    class LessThanAll_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanAll_1_T1]) -> LessThanAll_1[LessThanAll_1_T1]: ...

        LessThanAll_1_T1 = typing.TypeVar('LessThanAll_1_T1')
        class LessThanAll_1(typing.Generic[LessThanAll_1_T1]):
            LessThanAll_1_T = Vector512_0.LessThanAll_MethodGroup.LessThanAll_1_T1
            def __call__(self, left: Vector512_1[LessThanAll_1_T], right: Vector512_1[LessThanAll_1_T]) -> bool:...


    # Skipped LessThanAny due to it being static, abstract and generic.

    LessThanAny : LessThanAny_MethodGroup
    class LessThanAny_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanAny_1_T1]) -> LessThanAny_1[LessThanAny_1_T1]: ...

        LessThanAny_1_T1 = typing.TypeVar('LessThanAny_1_T1')
        class LessThanAny_1(typing.Generic[LessThanAny_1_T1]):
            LessThanAny_1_T = Vector512_0.LessThanAny_MethodGroup.LessThanAny_1_T1
            def __call__(self, left: Vector512_1[LessThanAny_1_T], right: Vector512_1[LessThanAny_1_T]) -> bool:...


    # Skipped LessThanOrEqual due to it being static, abstract and generic.

    LessThanOrEqual : LessThanOrEqual_MethodGroup
    class LessThanOrEqual_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqual_1_T1]) -> LessThanOrEqual_1[LessThanOrEqual_1_T1]: ...

        LessThanOrEqual_1_T1 = typing.TypeVar('LessThanOrEqual_1_T1')
        class LessThanOrEqual_1(typing.Generic[LessThanOrEqual_1_T1]):
            LessThanOrEqual_1_T = Vector512_0.LessThanOrEqual_MethodGroup.LessThanOrEqual_1_T1
            def __call__(self, left: Vector512_1[LessThanOrEqual_1_T], right: Vector512_1[LessThanOrEqual_1_T]) -> Vector512_1[LessThanOrEqual_1_T]:...


    # Skipped LessThanOrEqualAll due to it being static, abstract and generic.

    LessThanOrEqualAll : LessThanOrEqualAll_MethodGroup
    class LessThanOrEqualAll_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqualAll_1_T1]) -> LessThanOrEqualAll_1[LessThanOrEqualAll_1_T1]: ...

        LessThanOrEqualAll_1_T1 = typing.TypeVar('LessThanOrEqualAll_1_T1')
        class LessThanOrEqualAll_1(typing.Generic[LessThanOrEqualAll_1_T1]):
            LessThanOrEqualAll_1_T = Vector512_0.LessThanOrEqualAll_MethodGroup.LessThanOrEqualAll_1_T1
            def __call__(self, left: Vector512_1[LessThanOrEqualAll_1_T], right: Vector512_1[LessThanOrEqualAll_1_T]) -> bool:...


    # Skipped LessThanOrEqualAny due to it being static, abstract and generic.

    LessThanOrEqualAny : LessThanOrEqualAny_MethodGroup
    class LessThanOrEqualAny_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqualAny_1_T1]) -> LessThanOrEqualAny_1[LessThanOrEqualAny_1_T1]: ...

        LessThanOrEqualAny_1_T1 = typing.TypeVar('LessThanOrEqualAny_1_T1')
        class LessThanOrEqualAny_1(typing.Generic[LessThanOrEqualAny_1_T1]):
            LessThanOrEqualAny_1_T = Vector512_0.LessThanOrEqualAny_MethodGroup.LessThanOrEqualAny_1_T1
            def __call__(self, left: Vector512_1[LessThanOrEqualAny_1_T], right: Vector512_1[LessThanOrEqualAny_1_T]) -> bool:...


    # Skipped Load due to it being static, abstract and generic.

    Load : Load_MethodGroup
    class Load_MethodGroup:
        def __getitem__(self, t:typing.Type[Load_1_T1]) -> Load_1[Load_1_T1]: ...

        Load_1_T1 = typing.TypeVar('Load_1_T1')
        class Load_1(typing.Generic[Load_1_T1]):
            Load_1_T = Vector512_0.Load_MethodGroup.Load_1_T1
            def __call__(self, source: clr.Reference[Load_1_T]) -> Vector512_1[Load_1_T]:...


    # Skipped LoadAligned due to it being static, abstract and generic.

    LoadAligned : LoadAligned_MethodGroup
    class LoadAligned_MethodGroup:
        def __getitem__(self, t:typing.Type[LoadAligned_1_T1]) -> LoadAligned_1[LoadAligned_1_T1]: ...

        LoadAligned_1_T1 = typing.TypeVar('LoadAligned_1_T1')
        class LoadAligned_1(typing.Generic[LoadAligned_1_T1]):
            LoadAligned_1_T = Vector512_0.LoadAligned_MethodGroup.LoadAligned_1_T1
            def __call__(self, source: clr.Reference[LoadAligned_1_T]) -> Vector512_1[LoadAligned_1_T]:...


    # Skipped LoadAlignedNonTemporal due to it being static, abstract and generic.

    LoadAlignedNonTemporal : LoadAlignedNonTemporal_MethodGroup
    class LoadAlignedNonTemporal_MethodGroup:
        def __getitem__(self, t:typing.Type[LoadAlignedNonTemporal_1_T1]) -> LoadAlignedNonTemporal_1[LoadAlignedNonTemporal_1_T1]: ...

        LoadAlignedNonTemporal_1_T1 = typing.TypeVar('LoadAlignedNonTemporal_1_T1')
        class LoadAlignedNonTemporal_1(typing.Generic[LoadAlignedNonTemporal_1_T1]):
            LoadAlignedNonTemporal_1_T = Vector512_0.LoadAlignedNonTemporal_MethodGroup.LoadAlignedNonTemporal_1_T1
            def __call__(self, source: clr.Reference[LoadAlignedNonTemporal_1_T]) -> Vector512_1[LoadAlignedNonTemporal_1_T]:...


    # Skipped LoadUnsafe due to it being static, abstract and generic.

    LoadUnsafe : LoadUnsafe_MethodGroup
    class LoadUnsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[LoadUnsafe_1_T1]) -> LoadUnsafe_1[LoadUnsafe_1_T1]: ...

        LoadUnsafe_1_T1 = typing.TypeVar('LoadUnsafe_1_T1')
        class LoadUnsafe_1(typing.Generic[LoadUnsafe_1_T1]):
            LoadUnsafe_1_T = Vector512_0.LoadUnsafe_MethodGroup.LoadUnsafe_1_T1
            @typing.overload
            def __call__(self, source: clr.Reference[LoadUnsafe_1_T]) -> Vector512_1[LoadUnsafe_1_T]:...
            @typing.overload
            def __call__(self, source: clr.Reference[LoadUnsafe_1_T], elementOffset: UIntPtr) -> Vector512_1[LoadUnsafe_1_T]:...


    # Skipped Log due to it being static, abstract and generic.

    Log : Log_MethodGroup
    class Log_MethodGroup:
        def __call__(self, vector: Vector512_1[float]) -> Vector512_1[float]:...
        # Method Log(vector : Vector512`1) was skipped since it collides with above method

    # Skipped Log2 due to it being static, abstract and generic.

    Log2 : Log2_MethodGroup
    class Log2_MethodGroup:
        def __call__(self, vector: Vector512_1[float]) -> Vector512_1[float]:...
        # Method Log2(vector : Vector512`1) was skipped since it collides with above method

    # Skipped Max due to it being static, abstract and generic.

    Max : Max_MethodGroup
    class Max_MethodGroup:
        def __getitem__(self, t:typing.Type[Max_1_T1]) -> Max_1[Max_1_T1]: ...

        Max_1_T1 = typing.TypeVar('Max_1_T1')
        class Max_1(typing.Generic[Max_1_T1]):
            Max_1_T = Vector512_0.Max_MethodGroup.Max_1_T1
            def __call__(self, left: Vector512_1[Max_1_T], right: Vector512_1[Max_1_T]) -> Vector512_1[Max_1_T]:...


    # Skipped MaxMagnitude due to it being static, abstract and generic.

    MaxMagnitude : MaxMagnitude_MethodGroup
    class MaxMagnitude_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxMagnitude_1_T1]) -> MaxMagnitude_1[MaxMagnitude_1_T1]: ...

        MaxMagnitude_1_T1 = typing.TypeVar('MaxMagnitude_1_T1')
        class MaxMagnitude_1(typing.Generic[MaxMagnitude_1_T1]):
            MaxMagnitude_1_T = Vector512_0.MaxMagnitude_MethodGroup.MaxMagnitude_1_T1
            def __call__(self, left: Vector512_1[MaxMagnitude_1_T], right: Vector512_1[MaxMagnitude_1_T]) -> Vector512_1[MaxMagnitude_1_T]:...


    # Skipped MaxMagnitudeNumber due to it being static, abstract and generic.

    MaxMagnitudeNumber : MaxMagnitudeNumber_MethodGroup
    class MaxMagnitudeNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxMagnitudeNumber_1_T1]) -> MaxMagnitudeNumber_1[MaxMagnitudeNumber_1_T1]: ...

        MaxMagnitudeNumber_1_T1 = typing.TypeVar('MaxMagnitudeNumber_1_T1')
        class MaxMagnitudeNumber_1(typing.Generic[MaxMagnitudeNumber_1_T1]):
            MaxMagnitudeNumber_1_T = Vector512_0.MaxMagnitudeNumber_MethodGroup.MaxMagnitudeNumber_1_T1
            def __call__(self, left: Vector512_1[MaxMagnitudeNumber_1_T], right: Vector512_1[MaxMagnitudeNumber_1_T]) -> Vector512_1[MaxMagnitudeNumber_1_T]:...


    # Skipped MaxNative due to it being static, abstract and generic.

    MaxNative : MaxNative_MethodGroup
    class MaxNative_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxNative_1_T1]) -> MaxNative_1[MaxNative_1_T1]: ...

        MaxNative_1_T1 = typing.TypeVar('MaxNative_1_T1')
        class MaxNative_1(typing.Generic[MaxNative_1_T1]):
            MaxNative_1_T = Vector512_0.MaxNative_MethodGroup.MaxNative_1_T1
            def __call__(self, left: Vector512_1[MaxNative_1_T], right: Vector512_1[MaxNative_1_T]) -> Vector512_1[MaxNative_1_T]:...


    # Skipped MaxNumber due to it being static, abstract and generic.

    MaxNumber : MaxNumber_MethodGroup
    class MaxNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxNumber_1_T1]) -> MaxNumber_1[MaxNumber_1_T1]: ...

        MaxNumber_1_T1 = typing.TypeVar('MaxNumber_1_T1')
        class MaxNumber_1(typing.Generic[MaxNumber_1_T1]):
            MaxNumber_1_T = Vector512_0.MaxNumber_MethodGroup.MaxNumber_1_T1
            def __call__(self, left: Vector512_1[MaxNumber_1_T], right: Vector512_1[MaxNumber_1_T]) -> Vector512_1[MaxNumber_1_T]:...


    # Skipped Min due to it being static, abstract and generic.

    Min : Min_MethodGroup
    class Min_MethodGroup:
        def __getitem__(self, t:typing.Type[Min_1_T1]) -> Min_1[Min_1_T1]: ...

        Min_1_T1 = typing.TypeVar('Min_1_T1')
        class Min_1(typing.Generic[Min_1_T1]):
            Min_1_T = Vector512_0.Min_MethodGroup.Min_1_T1
            def __call__(self, left: Vector512_1[Min_1_T], right: Vector512_1[Min_1_T]) -> Vector512_1[Min_1_T]:...


    # Skipped MinMagnitude due to it being static, abstract and generic.

    MinMagnitude : MinMagnitude_MethodGroup
    class MinMagnitude_MethodGroup:
        def __getitem__(self, t:typing.Type[MinMagnitude_1_T1]) -> MinMagnitude_1[MinMagnitude_1_T1]: ...

        MinMagnitude_1_T1 = typing.TypeVar('MinMagnitude_1_T1')
        class MinMagnitude_1(typing.Generic[MinMagnitude_1_T1]):
            MinMagnitude_1_T = Vector512_0.MinMagnitude_MethodGroup.MinMagnitude_1_T1
            def __call__(self, left: Vector512_1[MinMagnitude_1_T], right: Vector512_1[MinMagnitude_1_T]) -> Vector512_1[MinMagnitude_1_T]:...


    # Skipped MinMagnitudeNumber due to it being static, abstract and generic.

    MinMagnitudeNumber : MinMagnitudeNumber_MethodGroup
    class MinMagnitudeNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MinMagnitudeNumber_1_T1]) -> MinMagnitudeNumber_1[MinMagnitudeNumber_1_T1]: ...

        MinMagnitudeNumber_1_T1 = typing.TypeVar('MinMagnitudeNumber_1_T1')
        class MinMagnitudeNumber_1(typing.Generic[MinMagnitudeNumber_1_T1]):
            MinMagnitudeNumber_1_T = Vector512_0.MinMagnitudeNumber_MethodGroup.MinMagnitudeNumber_1_T1
            def __call__(self, left: Vector512_1[MinMagnitudeNumber_1_T], right: Vector512_1[MinMagnitudeNumber_1_T]) -> Vector512_1[MinMagnitudeNumber_1_T]:...


    # Skipped MinNative due to it being static, abstract and generic.

    MinNative : MinNative_MethodGroup
    class MinNative_MethodGroup:
        def __getitem__(self, t:typing.Type[MinNative_1_T1]) -> MinNative_1[MinNative_1_T1]: ...

        MinNative_1_T1 = typing.TypeVar('MinNative_1_T1')
        class MinNative_1(typing.Generic[MinNative_1_T1]):
            MinNative_1_T = Vector512_0.MinNative_MethodGroup.MinNative_1_T1
            def __call__(self, left: Vector512_1[MinNative_1_T], right: Vector512_1[MinNative_1_T]) -> Vector512_1[MinNative_1_T]:...


    # Skipped MinNumber due to it being static, abstract and generic.

    MinNumber : MinNumber_MethodGroup
    class MinNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MinNumber_1_T1]) -> MinNumber_1[MinNumber_1_T1]: ...

        MinNumber_1_T1 = typing.TypeVar('MinNumber_1_T1')
        class MinNumber_1(typing.Generic[MinNumber_1_T1]):
            MinNumber_1_T = Vector512_0.MinNumber_MethodGroup.MinNumber_1_T1
            def __call__(self, left: Vector512_1[MinNumber_1_T], right: Vector512_1[MinNumber_1_T]) -> Vector512_1[MinNumber_1_T]:...


    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        def __getitem__(self, t:typing.Type[Multiply_1_T1]) -> Multiply_1[Multiply_1_T1]: ...

        Multiply_1_T1 = typing.TypeVar('Multiply_1_T1')
        class Multiply_1(typing.Generic[Multiply_1_T1]):
            Multiply_1_T = Vector512_0.Multiply_MethodGroup.Multiply_1_T1
            @typing.overload
            def __call__(self, left: Vector512_1[Multiply_1_T], right: Vector512_1[Multiply_1_T]) -> Vector512_1[Multiply_1_T]:...
            @typing.overload
            def __call__(self, left: Vector512_1[Multiply_1_T], right: Multiply_1_T) -> Vector512_1[Multiply_1_T]:...
            @typing.overload
            def __call__(self, left: Multiply_1_T, right: Vector512_1[Multiply_1_T]) -> Vector512_1[Multiply_1_T]:...


    # Skipped MultiplyAddEstimate due to it being static, abstract and generic.

    MultiplyAddEstimate : MultiplyAddEstimate_MethodGroup
    class MultiplyAddEstimate_MethodGroup:
        def __call__(self, left: Vector512_1[float], right: Vector512_1[float], addend: Vector512_1[float]) -> Vector512_1[float]:...
        # Method MultiplyAddEstimate(left : Vector512`1, right : Vector512`1, addend : Vector512`1) was skipped since it collides with above method

    # Skipped Narrow due to it being static, abstract and generic.

    Narrow : Narrow_MethodGroup
    class Narrow_MethodGroup:
        def __call__(self, lower: Vector512_1[float], upper: Vector512_1[float]) -> Vector512_1[float]:...
        # Method Narrow(lower : Vector512`1, upper : Vector512`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector512`1, upper : Vector512`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector512`1, upper : Vector512`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector512`1, upper : Vector512`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector512`1, upper : Vector512`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector512`1, upper : Vector512`1) was skipped since it collides with above method

    # Skipped NarrowWithSaturation due to it being static, abstract and generic.

    NarrowWithSaturation : NarrowWithSaturation_MethodGroup
    class NarrowWithSaturation_MethodGroup:
        def __call__(self, lower: Vector512_1[float], upper: Vector512_1[float]) -> Vector512_1[float]:...
        # Method NarrowWithSaturation(lower : Vector512`1, upper : Vector512`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector512`1, upper : Vector512`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector512`1, upper : Vector512`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector512`1, upper : Vector512`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector512`1, upper : Vector512`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector512`1, upper : Vector512`1) was skipped since it collides with above method

    # Skipped Negate due to it being static, abstract and generic.

    Negate : Negate_MethodGroup
    class Negate_MethodGroup:
        def __getitem__(self, t:typing.Type[Negate_1_T1]) -> Negate_1[Negate_1_T1]: ...

        Negate_1_T1 = typing.TypeVar('Negate_1_T1')
        class Negate_1(typing.Generic[Negate_1_T1]):
            Negate_1_T = Vector512_0.Negate_MethodGroup.Negate_1_T1
            def __call__(self, vector: Vector512_1[Negate_1_T]) -> Vector512_1[Negate_1_T]:...


    # Skipped None due to it being static, abstract and generic.

    None : None_MethodGroup
    class None_MethodGroup:
        def __getitem__(self, t:typing.Type[None_1_T1]) -> None_1[None_1_T1]: ...

        None_1_T1 = typing.TypeVar('None_1_T1')
        class None_1(typing.Generic[None_1_T1]):
            None_1_T = Vector512_0.None_MethodGroup.None_1_T1
            def __call__(self, vector: Vector512_1[None_1_T], value: None_1_T) -> bool:...


    # Skipped NoneWhereAllBitsSet due to it being static, abstract and generic.

    NoneWhereAllBitsSet : NoneWhereAllBitsSet_MethodGroup
    class NoneWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[NoneWhereAllBitsSet_1_T1]) -> NoneWhereAllBitsSet_1[NoneWhereAllBitsSet_1_T1]: ...

        NoneWhereAllBitsSet_1_T1 = typing.TypeVar('NoneWhereAllBitsSet_1_T1')
        class NoneWhereAllBitsSet_1(typing.Generic[NoneWhereAllBitsSet_1_T1]):
            NoneWhereAllBitsSet_1_T = Vector512_0.NoneWhereAllBitsSet_MethodGroup.NoneWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector512_1[NoneWhereAllBitsSet_1_T]) -> bool:...


    # Skipped OnesComplement due to it being static, abstract and generic.

    OnesComplement : OnesComplement_MethodGroup
    class OnesComplement_MethodGroup:
        def __getitem__(self, t:typing.Type[OnesComplement_1_T1]) -> OnesComplement_1[OnesComplement_1_T1]: ...

        OnesComplement_1_T1 = typing.TypeVar('OnesComplement_1_T1')
        class OnesComplement_1(typing.Generic[OnesComplement_1_T1]):
            OnesComplement_1_T = Vector512_0.OnesComplement_MethodGroup.OnesComplement_1_T1
            def __call__(self, vector: Vector512_1[OnesComplement_1_T]) -> Vector512_1[OnesComplement_1_T]:...


    # Skipped RadiansToDegrees due to it being static, abstract and generic.

    RadiansToDegrees : RadiansToDegrees_MethodGroup
    class RadiansToDegrees_MethodGroup:
        def __call__(self, radians: Vector512_1[float]) -> Vector512_1[float]:...
        # Method RadiansToDegrees(radians : Vector512`1) was skipped since it collides with above method

    # Skipped Round due to it being static, abstract and generic.

    Round : Round_MethodGroup
    class Round_MethodGroup:
        @typing.overload
        def __call__(self, vector: Vector512_1[float]) -> Vector512_1[float]:...
        # Method Round(vector : Vector512`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, vector: Vector512_1[float], mode: MidpointRounding) -> Vector512_1[float]:...
        # Method Round(vector : Vector512`1, mode : MidpointRounding) was skipped since it collides with above method

    # Skipped ShiftLeft due to it being static, abstract and generic.

    ShiftLeft : ShiftLeft_MethodGroup
    class ShiftLeft_MethodGroup:
        @typing.overload
        def __call__(self, vector: Vector512_1[int], shiftCount: int) -> Vector512_1[int]:...
        # Method ShiftLeft(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, vector: Vector512_1[UIntPtr], shiftCount: int) -> Vector512_1[UIntPtr]:...

    # Skipped ShiftRightArithmetic due to it being static, abstract and generic.

    ShiftRightArithmetic : ShiftRightArithmetic_MethodGroup
    class ShiftRightArithmetic_MethodGroup:
        def __call__(self, vector: Vector512_1[int], shiftCount: int) -> Vector512_1[int]:...
        # Method ShiftRightArithmetic(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightArithmetic(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightArithmetic(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightArithmetic(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method

    # Skipped ShiftRightLogical due to it being static, abstract and generic.

    ShiftRightLogical : ShiftRightLogical_MethodGroup
    class ShiftRightLogical_MethodGroup:
        @typing.overload
        def __call__(self, vector: Vector512_1[int], shiftCount: int) -> Vector512_1[int]:...
        # Method ShiftRightLogical(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector512`1, shiftCount : Int32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, vector: Vector512_1[UIntPtr], shiftCount: int) -> Vector512_1[UIntPtr]:...

    # Skipped Shuffle due to it being static, abstract and generic.

    Shuffle : Shuffle_MethodGroup
    class Shuffle_MethodGroup:
        def __call__(self, vector: Vector512_1[float], indices: Vector512_1[int]) -> Vector512_1[float]:...
        # Method Shuffle(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method

    # Skipped ShuffleNative due to it being static, abstract and generic.

    ShuffleNative : ShuffleNative_MethodGroup
    class ShuffleNative_MethodGroup:
        def __call__(self, vector: Vector512_1[float], indices: Vector512_1[int]) -> Vector512_1[float]:...
        # Method ShuffleNative(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector512`1, indices : Vector512`1) was skipped since it collides with above method

    # Skipped Sin due to it being static, abstract and generic.

    Sin : Sin_MethodGroup
    class Sin_MethodGroup:
        def __call__(self, vector: Vector512_1[float]) -> Vector512_1[float]:...
        # Method Sin(vector : Vector512`1) was skipped since it collides with above method

    # Skipped SinCos due to it being static, abstract and generic.

    SinCos : SinCos_MethodGroup
    class SinCos_MethodGroup:
        def __call__(self, vector: Vector512_1[float]) -> ValueTuple_2[Vector512_1[float], Vector512_1[float]]:...
        # Method SinCos(vector : Vector512`1) was skipped since it collides with above method

    # Skipped Sqrt due to it being static, abstract and generic.

    Sqrt : Sqrt_MethodGroup
    class Sqrt_MethodGroup:
        def __getitem__(self, t:typing.Type[Sqrt_1_T1]) -> Sqrt_1[Sqrt_1_T1]: ...

        Sqrt_1_T1 = typing.TypeVar('Sqrt_1_T1')
        class Sqrt_1(typing.Generic[Sqrt_1_T1]):
            Sqrt_1_T = Vector512_0.Sqrt_MethodGroup.Sqrt_1_T1
            def __call__(self, vector: Vector512_1[Sqrt_1_T]) -> Vector512_1[Sqrt_1_T]:...


    # Skipped Store due to it being static, abstract and generic.

    Store : Store_MethodGroup
    class Store_MethodGroup:
        def __getitem__(self, t:typing.Type[Store_1_T1]) -> Store_1[Store_1_T1]: ...

        Store_1_T1 = typing.TypeVar('Store_1_T1')
        class Store_1(typing.Generic[Store_1_T1]):
            Store_1_T = Vector512_0.Store_MethodGroup.Store_1_T1
            def __call__(self, source: Vector512_1[Store_1_T], destination: clr.Reference[Store_1_T]) -> None:...


    # Skipped StoreAligned due to it being static, abstract and generic.

    StoreAligned : StoreAligned_MethodGroup
    class StoreAligned_MethodGroup:
        def __getitem__(self, t:typing.Type[StoreAligned_1_T1]) -> StoreAligned_1[StoreAligned_1_T1]: ...

        StoreAligned_1_T1 = typing.TypeVar('StoreAligned_1_T1')
        class StoreAligned_1(typing.Generic[StoreAligned_1_T1]):
            StoreAligned_1_T = Vector512_0.StoreAligned_MethodGroup.StoreAligned_1_T1
            def __call__(self, source: Vector512_1[StoreAligned_1_T], destination: clr.Reference[StoreAligned_1_T]) -> None:...


    # Skipped StoreAlignedNonTemporal due to it being static, abstract and generic.

    StoreAlignedNonTemporal : StoreAlignedNonTemporal_MethodGroup
    class StoreAlignedNonTemporal_MethodGroup:
        def __getitem__(self, t:typing.Type[StoreAlignedNonTemporal_1_T1]) -> StoreAlignedNonTemporal_1[StoreAlignedNonTemporal_1_T1]: ...

        StoreAlignedNonTemporal_1_T1 = typing.TypeVar('StoreAlignedNonTemporal_1_T1')
        class StoreAlignedNonTemporal_1(typing.Generic[StoreAlignedNonTemporal_1_T1]):
            StoreAlignedNonTemporal_1_T = Vector512_0.StoreAlignedNonTemporal_MethodGroup.StoreAlignedNonTemporal_1_T1
            def __call__(self, source: Vector512_1[StoreAlignedNonTemporal_1_T], destination: clr.Reference[StoreAlignedNonTemporal_1_T]) -> None:...


    # Skipped StoreUnsafe due to it being static, abstract and generic.

    StoreUnsafe : StoreUnsafe_MethodGroup
    class StoreUnsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[StoreUnsafe_1_T1]) -> StoreUnsafe_1[StoreUnsafe_1_T1]: ...

        StoreUnsafe_1_T1 = typing.TypeVar('StoreUnsafe_1_T1')
        class StoreUnsafe_1(typing.Generic[StoreUnsafe_1_T1]):
            StoreUnsafe_1_T = Vector512_0.StoreUnsafe_MethodGroup.StoreUnsafe_1_T1
            @typing.overload
            def __call__(self, source: Vector512_1[StoreUnsafe_1_T], destination: clr.Reference[StoreUnsafe_1_T]) -> None:...
            @typing.overload
            def __call__(self, source: Vector512_1[StoreUnsafe_1_T], destination: clr.Reference[StoreUnsafe_1_T], elementOffset: UIntPtr) -> None:...


    # Skipped Subtract due to it being static, abstract and generic.

    Subtract : Subtract_MethodGroup
    class Subtract_MethodGroup:
        def __getitem__(self, t:typing.Type[Subtract_1_T1]) -> Subtract_1[Subtract_1_T1]: ...

        Subtract_1_T1 = typing.TypeVar('Subtract_1_T1')
        class Subtract_1(typing.Generic[Subtract_1_T1]):
            Subtract_1_T = Vector512_0.Subtract_MethodGroup.Subtract_1_T1
            def __call__(self, left: Vector512_1[Subtract_1_T], right: Vector512_1[Subtract_1_T]) -> Vector512_1[Subtract_1_T]:...


    # Skipped SubtractSaturate due to it being static, abstract and generic.

    SubtractSaturate : SubtractSaturate_MethodGroup
    class SubtractSaturate_MethodGroup:
        def __getitem__(self, t:typing.Type[SubtractSaturate_1_T1]) -> SubtractSaturate_1[SubtractSaturate_1_T1]: ...

        SubtractSaturate_1_T1 = typing.TypeVar('SubtractSaturate_1_T1')
        class SubtractSaturate_1(typing.Generic[SubtractSaturate_1_T1]):
            SubtractSaturate_1_T = Vector512_0.SubtractSaturate_MethodGroup.SubtractSaturate_1_T1
            def __call__(self, left: Vector512_1[SubtractSaturate_1_T], right: Vector512_1[SubtractSaturate_1_T]) -> Vector512_1[SubtractSaturate_1_T]:...


    # Skipped Sum due to it being static, abstract and generic.

    Sum : Sum_MethodGroup
    class Sum_MethodGroup:
        def __getitem__(self, t:typing.Type[Sum_1_T1]) -> Sum_1[Sum_1_T1]: ...

        Sum_1_T1 = typing.TypeVar('Sum_1_T1')
        class Sum_1(typing.Generic[Sum_1_T1]):
            Sum_1_T = Vector512_0.Sum_MethodGroup.Sum_1_T1
            def __call__(self, vector: Vector512_1[Sum_1_T]) -> Sum_1_T:...


    # Skipped ToScalar due to it being static, abstract and generic.

    ToScalar : ToScalar_MethodGroup
    class ToScalar_MethodGroup:
        def __getitem__(self, t:typing.Type[ToScalar_1_T1]) -> ToScalar_1[ToScalar_1_T1]: ...

        ToScalar_1_T1 = typing.TypeVar('ToScalar_1_T1')
        class ToScalar_1(typing.Generic[ToScalar_1_T1]):
            ToScalar_1_T = Vector512_0.ToScalar_MethodGroup.ToScalar_1_T1
            def __call__(self, vector: Vector512_1[ToScalar_1_T]) -> ToScalar_1_T:...


    # Skipped Truncate due to it being static, abstract and generic.

    Truncate : Truncate_MethodGroup
    class Truncate_MethodGroup:
        def __call__(self, vector: Vector512_1[float]) -> Vector512_1[float]:...
        # Method Truncate(vector : Vector512`1) was skipped since it collides with above method

    # Skipped TryCopyTo due to it being static, abstract and generic.

    TryCopyTo : TryCopyTo_MethodGroup
    class TryCopyTo_MethodGroup:
        def __getitem__(self, t:typing.Type[TryCopyTo_1_T1]) -> TryCopyTo_1[TryCopyTo_1_T1]: ...

        TryCopyTo_1_T1 = typing.TypeVar('TryCopyTo_1_T1')
        class TryCopyTo_1(typing.Generic[TryCopyTo_1_T1]):
            TryCopyTo_1_T = Vector512_0.TryCopyTo_MethodGroup.TryCopyTo_1_T1
            def __call__(self, vector: Vector512_1[TryCopyTo_1_T], destination: Span_1[TryCopyTo_1_T]) -> bool:...


    # Skipped Widen due to it being static, abstract and generic.

    Widen : Widen_MethodGroup
    class Widen_MethodGroup:
        def __call__(self, source: Vector512_1[float]) -> ValueTuple_2[Vector512_1[float], Vector512_1[float]]:...
        # Method Widen(source : Vector512`1) was skipped since it collides with above method
        # Method Widen(source : Vector512`1) was skipped since it collides with above method
        # Method Widen(source : Vector512`1) was skipped since it collides with above method
        # Method Widen(source : Vector512`1) was skipped since it collides with above method
        # Method Widen(source : Vector512`1) was skipped since it collides with above method
        # Method Widen(source : Vector512`1) was skipped since it collides with above method

    # Skipped WidenLower due to it being static, abstract and generic.

    WidenLower : WidenLower_MethodGroup
    class WidenLower_MethodGroup:
        def __call__(self, source: Vector512_1[float]) -> Vector512_1[float]:...
        # Method WidenLower(source : Vector512`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector512`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector512`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector512`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector512`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector512`1) was skipped since it collides with above method

    # Skipped WidenUpper due to it being static, abstract and generic.

    WidenUpper : WidenUpper_MethodGroup
    class WidenUpper_MethodGroup:
        def __call__(self, source: Vector512_1[float]) -> Vector512_1[float]:...
        # Method WidenUpper(source : Vector512`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector512`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector512`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector512`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector512`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector512`1) was skipped since it collides with above method

    # Skipped WithElement due to it being static, abstract and generic.

    WithElement : WithElement_MethodGroup
    class WithElement_MethodGroup:
        def __getitem__(self, t:typing.Type[WithElement_1_T1]) -> WithElement_1[WithElement_1_T1]: ...

        WithElement_1_T1 = typing.TypeVar('WithElement_1_T1')
        class WithElement_1(typing.Generic[WithElement_1_T1]):
            WithElement_1_T = Vector512_0.WithElement_MethodGroup.WithElement_1_T1
            def __call__(self, vector: Vector512_1[WithElement_1_T], index: int, value: WithElement_1_T) -> Vector512_1[WithElement_1_T]:...


    # Skipped WithLower due to it being static, abstract and generic.

    WithLower : WithLower_MethodGroup
    class WithLower_MethodGroup:
        def __getitem__(self, t:typing.Type[WithLower_1_T1]) -> WithLower_1[WithLower_1_T1]: ...

        WithLower_1_T1 = typing.TypeVar('WithLower_1_T1')
        class WithLower_1(typing.Generic[WithLower_1_T1]):
            WithLower_1_T = Vector512_0.WithLower_MethodGroup.WithLower_1_T1
            def __call__(self, vector: Vector512_1[WithLower_1_T], value: Vector256_1[WithLower_1_T]) -> Vector512_1[WithLower_1_T]:...


    # Skipped WithUpper due to it being static, abstract and generic.

    WithUpper : WithUpper_MethodGroup
    class WithUpper_MethodGroup:
        def __getitem__(self, t:typing.Type[WithUpper_1_T1]) -> WithUpper_1[WithUpper_1_T1]: ...

        WithUpper_1_T1 = typing.TypeVar('WithUpper_1_T1')
        class WithUpper_1(typing.Generic[WithUpper_1_T1]):
            WithUpper_1_T = Vector512_0.WithUpper_MethodGroup.WithUpper_1_T1
            def __call__(self, vector: Vector512_1[WithUpper_1_T], value: Vector256_1[WithUpper_1_T]) -> Vector512_1[WithUpper_1_T]:...


    # Skipped Xor due to it being static, abstract and generic.

    Xor : Xor_MethodGroup
    class Xor_MethodGroup:
        def __getitem__(self, t:typing.Type[Xor_1_T1]) -> Xor_1[Xor_1_T1]: ...

        Xor_1_T1 = typing.TypeVar('Xor_1_T1')
        class Xor_1(typing.Generic[Xor_1_T1]):
            Xor_1_T = Vector512_0.Xor_MethodGroup.Xor_1_T1
            def __call__(self, left: Vector512_1[Xor_1_T], right: Vector512_1[Xor_1_T]) -> Vector512_1[Xor_1_T]:...




Vector512_1_T = typing.TypeVar('Vector512_1_T')
class Vector512_1(typing.Generic[Vector512_1_T]):
    @classmethod
    @property
    def AllBitsSet(cls) -> Vector512_1[Vector512_1_T]: ...
    @classmethod
    @property
    def Count(cls) -> int: ...
    @classmethod
    @property
    def Indices(cls) -> Vector512_1[Vector512_1_T]: ...
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @property
    def Item(self) -> Vector512_1_T: ...
    @classmethod
    @property
    def One(cls) -> Vector512_1[Vector512_1_T]: ...
    @classmethod
    @property
    def Zero(cls) -> Vector512_1[Vector512_1_T]: ...
    def GetHashCode(self) -> int: ...
    def __add__(self, left: Vector512_1[Vector512_1_T], right: Vector512_1[Vector512_1_T]) -> Vector512_1[Vector512_1_T]: ...
    def __and__(self, left: Vector512_1[Vector512_1_T], right: Vector512_1[Vector512_1_T]) -> Vector512_1[Vector512_1_T]: ...
    def __or__(self, left: Vector512_1[Vector512_1_T], right: Vector512_1[Vector512_1_T]) -> Vector512_1[Vector512_1_T]: ...
    @typing.overload
    def __truediv__(self, left: Vector512_1[Vector512_1_T], right: Vector512_1[Vector512_1_T]) -> Vector512_1[Vector512_1_T]: ...
    @typing.overload
    def __truediv__(self, left: Vector512_1[Vector512_1_T], right: Vector512_1_T) -> Vector512_1[Vector512_1_T]: ...
    def __eq__(self, left: Vector512_1[Vector512_1_T], right: Vector512_1[Vector512_1_T]) -> bool: ...
    def __xor__(self, left: Vector512_1[Vector512_1_T], right: Vector512_1[Vector512_1_T]) -> Vector512_1[Vector512_1_T]: ...
    def __ne__(self, left: Vector512_1[Vector512_1_T], right: Vector512_1[Vector512_1_T]) -> bool: ...
    def __lshift__(self, value: Vector512_1[Vector512_1_T], shiftCount: int) -> Vector512_1[Vector512_1_T]: ...
    @typing.overload
    def __mul__(self, left: Vector512_1[Vector512_1_T], right: Vector512_1[Vector512_1_T]) -> Vector512_1[Vector512_1_T]: ...
    @typing.overload
    def __mul__(self, left: Vector512_1[Vector512_1_T], right: Vector512_1_T) -> Vector512_1[Vector512_1_T]: ...
    @typing.overload
    def __mul__(self, left: Vector512_1_T, right: Vector512_1[Vector512_1_T]) -> Vector512_1[Vector512_1_T]: ...
    def __invert__(self, vector: Vector512_1[Vector512_1_T]) -> Vector512_1[Vector512_1_T]: ...
    def __rshift__(self, value: Vector512_1[Vector512_1_T], shiftCount: int) -> Vector512_1[Vector512_1_T]: ...
    def __sub__(self, left: Vector512_1[Vector512_1_T], right: Vector512_1[Vector512_1_T]) -> Vector512_1[Vector512_1_T]: ...
    def __neg__(self, vector: Vector512_1[Vector512_1_T]) -> Vector512_1[Vector512_1_T]: ...
    def __pos__(self, value: Vector512_1[Vector512_1_T]) -> Vector512_1[Vector512_1_T]: ...
    # Operator not supported op_UnsignedRightShift(value: Vector512`1, shiftCount: Int32)
    def ToString(self) -> str: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup[Vector512_1_T]
    Equals_MethodGroup_Vector512_1_T = typing.TypeVar('Equals_MethodGroup_Vector512_1_T')
    class Equals_MethodGroup(typing.Generic[Equals_MethodGroup_Vector512_1_T]):
        Equals_MethodGroup_Vector512_1_T = Vector512_1.Equals_MethodGroup_Vector512_1_T
        @typing.overload
        def __call__(self, other: Vector512_1[Equals_MethodGroup_Vector512_1_T]) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...



class Vector64_GenericClasses(abc.ABCMeta):
    Generic_Vector64_GenericClasses_Vector64_1_T = typing.TypeVar('Generic_Vector64_GenericClasses_Vector64_1_T')
    def __getitem__(self, types : typing.Type[Generic_Vector64_GenericClasses_Vector64_1_T]) -> typing.Type[Vector64_1[Generic_Vector64_GenericClasses_Vector64_1_T]]: ...

class Vector64(Vector64_0, metaclass =Vector64_GenericClasses): ...

class Vector64_0(abc.ABC):
    @classmethod
    @property
    def IsHardwareAccelerated(cls) -> bool: ...
    @staticmethod
    def ConvertToInt32(vector: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToInt32Native(vector: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToInt64(vector: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToInt64Native(vector: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToUInt32(vector: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToUInt32Native(vector: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToUInt64(vector: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToUInt64Native(vector: Vector64_1[float]) -> Vector64_1[int]: ...
    # Skipped Abs due to it being static, abstract and generic.

    Abs : Abs_MethodGroup
    class Abs_MethodGroup:
        def __getitem__(self, t:typing.Type[Abs_1_T1]) -> Abs_1[Abs_1_T1]: ...

        Abs_1_T1 = typing.TypeVar('Abs_1_T1')
        class Abs_1(typing.Generic[Abs_1_T1]):
            Abs_1_T = Vector64_0.Abs_MethodGroup.Abs_1_T1
            def __call__(self, vector: Vector64_1[Abs_1_T]) -> Vector64_1[Abs_1_T]:...


    # Skipped Add due to it being static, abstract and generic.

    Add : Add_MethodGroup
    class Add_MethodGroup:
        def __getitem__(self, t:typing.Type[Add_1_T1]) -> Add_1[Add_1_T1]: ...

        Add_1_T1 = typing.TypeVar('Add_1_T1')
        class Add_1(typing.Generic[Add_1_T1]):
            Add_1_T = Vector64_0.Add_MethodGroup.Add_1_T1
            def __call__(self, left: Vector64_1[Add_1_T], right: Vector64_1[Add_1_T]) -> Vector64_1[Add_1_T]:...


    # Skipped AddSaturate due to it being static, abstract and generic.

    AddSaturate : AddSaturate_MethodGroup
    class AddSaturate_MethodGroup:
        def __getitem__(self, t:typing.Type[AddSaturate_1_T1]) -> AddSaturate_1[AddSaturate_1_T1]: ...

        AddSaturate_1_T1 = typing.TypeVar('AddSaturate_1_T1')
        class AddSaturate_1(typing.Generic[AddSaturate_1_T1]):
            AddSaturate_1_T = Vector64_0.AddSaturate_MethodGroup.AddSaturate_1_T1
            def __call__(self, left: Vector64_1[AddSaturate_1_T], right: Vector64_1[AddSaturate_1_T]) -> Vector64_1[AddSaturate_1_T]:...


    # Skipped All due to it being static, abstract and generic.

    All : All_MethodGroup
    class All_MethodGroup:
        def __getitem__(self, t:typing.Type[All_1_T1]) -> All_1[All_1_T1]: ...

        All_1_T1 = typing.TypeVar('All_1_T1')
        class All_1(typing.Generic[All_1_T1]):
            All_1_T = Vector64_0.All_MethodGroup.All_1_T1
            def __call__(self, vector: Vector64_1[All_1_T], value: All_1_T) -> bool:...


    # Skipped AllWhereAllBitsSet due to it being static, abstract and generic.

    AllWhereAllBitsSet : AllWhereAllBitsSet_MethodGroup
    class AllWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[AllWhereAllBitsSet_1_T1]) -> AllWhereAllBitsSet_1[AllWhereAllBitsSet_1_T1]: ...

        AllWhereAllBitsSet_1_T1 = typing.TypeVar('AllWhereAllBitsSet_1_T1')
        class AllWhereAllBitsSet_1(typing.Generic[AllWhereAllBitsSet_1_T1]):
            AllWhereAllBitsSet_1_T = Vector64_0.AllWhereAllBitsSet_MethodGroup.AllWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector64_1[AllWhereAllBitsSet_1_T]) -> bool:...


    # Skipped AndNot due to it being static, abstract and generic.

    AndNot : AndNot_MethodGroup
    class AndNot_MethodGroup:
        def __getitem__(self, t:typing.Type[AndNot_1_T1]) -> AndNot_1[AndNot_1_T1]: ...

        AndNot_1_T1 = typing.TypeVar('AndNot_1_T1')
        class AndNot_1(typing.Generic[AndNot_1_T1]):
            AndNot_1_T = Vector64_0.AndNot_MethodGroup.AndNot_1_T1
            def __call__(self, left: Vector64_1[AndNot_1_T], right: Vector64_1[AndNot_1_T]) -> Vector64_1[AndNot_1_T]:...


    # Skipped Any due to it being static, abstract and generic.

    Any : Any_MethodGroup
    class Any_MethodGroup:
        def __getitem__(self, t:typing.Type[Any_1_T1]) -> Any_1[Any_1_T1]: ...

        Any_1_T1 = typing.TypeVar('Any_1_T1')
        class Any_1(typing.Generic[Any_1_T1]):
            Any_1_T = Vector64_0.Any_MethodGroup.Any_1_T1
            def __call__(self, vector: Vector64_1[Any_1_T], value: Any_1_T) -> bool:...


    # Skipped AnyWhereAllBitsSet due to it being static, abstract and generic.

    AnyWhereAllBitsSet : AnyWhereAllBitsSet_MethodGroup
    class AnyWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[AnyWhereAllBitsSet_1_T1]) -> AnyWhereAllBitsSet_1[AnyWhereAllBitsSet_1_T1]: ...

        AnyWhereAllBitsSet_1_T1 = typing.TypeVar('AnyWhereAllBitsSet_1_T1')
        class AnyWhereAllBitsSet_1(typing.Generic[AnyWhereAllBitsSet_1_T1]):
            AnyWhereAllBitsSet_1_T = Vector64_0.AnyWhereAllBitsSet_MethodGroup.AnyWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector64_1[AnyWhereAllBitsSet_1_T]) -> bool:...


    # Skipped As due to it being static, abstract and generic.

    As : As_MethodGroup
    class As_MethodGroup:
        def __getitem__(self, t:typing.Tuple[typing.Type[As_2_T1], typing.Type[As_2_T2]]) -> As_2[As_2_T1, As_2_T2]: ...

        As_2_T1 = typing.TypeVar('As_2_T1')
        As_2_T2 = typing.TypeVar('As_2_T2')
        class As_2(typing.Generic[As_2_T1, As_2_T2]):
            As_2_TFrom = Vector64_0.As_MethodGroup.As_2_T1
            As_2_TTo = Vector64_0.As_MethodGroup.As_2_T2
            def __call__(self, vector: Vector64_1[As_2_TFrom]) -> Vector64_1[As_2_TTo]:...


    # Skipped AsByte due to it being static, abstract and generic.

    AsByte : AsByte_MethodGroup
    class AsByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsByte_1_T1]) -> AsByte_1[AsByte_1_T1]: ...

        AsByte_1_T1 = typing.TypeVar('AsByte_1_T1')
        class AsByte_1(typing.Generic[AsByte_1_T1]):
            AsByte_1_T = Vector64_0.AsByte_MethodGroup.AsByte_1_T1
            def __call__(self, vector: Vector64_1[AsByte_1_T]) -> Vector64_1[int]:...


    # Skipped AsDouble due to it being static, abstract and generic.

    AsDouble : AsDouble_MethodGroup
    class AsDouble_MethodGroup:
        def __getitem__(self, t:typing.Type[AsDouble_1_T1]) -> AsDouble_1[AsDouble_1_T1]: ...

        AsDouble_1_T1 = typing.TypeVar('AsDouble_1_T1')
        class AsDouble_1(typing.Generic[AsDouble_1_T1]):
            AsDouble_1_T = Vector64_0.AsDouble_MethodGroup.AsDouble_1_T1
            def __call__(self, vector: Vector64_1[AsDouble_1_T]) -> Vector64_1[float]:...


    # Skipped AsInt16 due to it being static, abstract and generic.

    AsInt16 : AsInt16_MethodGroup
    class AsInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt16_1_T1]) -> AsInt16_1[AsInt16_1_T1]: ...

        AsInt16_1_T1 = typing.TypeVar('AsInt16_1_T1')
        class AsInt16_1(typing.Generic[AsInt16_1_T1]):
            AsInt16_1_T = Vector64_0.AsInt16_MethodGroup.AsInt16_1_T1
            def __call__(self, vector: Vector64_1[AsInt16_1_T]) -> Vector64_1[int]:...


    # Skipped AsInt32 due to it being static, abstract and generic.

    AsInt32 : AsInt32_MethodGroup
    class AsInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt32_1_T1]) -> AsInt32_1[AsInt32_1_T1]: ...

        AsInt32_1_T1 = typing.TypeVar('AsInt32_1_T1')
        class AsInt32_1(typing.Generic[AsInt32_1_T1]):
            AsInt32_1_T = Vector64_0.AsInt32_MethodGroup.AsInt32_1_T1
            def __call__(self, vector: Vector64_1[AsInt32_1_T]) -> Vector64_1[int]:...


    # Skipped AsInt64 due to it being static, abstract and generic.

    AsInt64 : AsInt64_MethodGroup
    class AsInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsInt64_1_T1]) -> AsInt64_1[AsInt64_1_T1]: ...

        AsInt64_1_T1 = typing.TypeVar('AsInt64_1_T1')
        class AsInt64_1(typing.Generic[AsInt64_1_T1]):
            AsInt64_1_T = Vector64_0.AsInt64_MethodGroup.AsInt64_1_T1
            def __call__(self, vector: Vector64_1[AsInt64_1_T]) -> Vector64_1[int]:...


    # Skipped AsNInt due to it being static, abstract and generic.

    AsNInt : AsNInt_MethodGroup
    class AsNInt_MethodGroup:
        def __getitem__(self, t:typing.Type[AsNInt_1_T1]) -> AsNInt_1[AsNInt_1_T1]: ...

        AsNInt_1_T1 = typing.TypeVar('AsNInt_1_T1')
        class AsNInt_1(typing.Generic[AsNInt_1_T1]):
            AsNInt_1_T = Vector64_0.AsNInt_MethodGroup.AsNInt_1_T1
            def __call__(self, vector: Vector64_1[AsNInt_1_T]) -> Vector64_1[int]:...


    # Skipped AsNUInt due to it being static, abstract and generic.

    AsNUInt : AsNUInt_MethodGroup
    class AsNUInt_MethodGroup:
        def __getitem__(self, t:typing.Type[AsNUInt_1_T1]) -> AsNUInt_1[AsNUInt_1_T1]: ...

        AsNUInt_1_T1 = typing.TypeVar('AsNUInt_1_T1')
        class AsNUInt_1(typing.Generic[AsNUInt_1_T1]):
            AsNUInt_1_T = Vector64_0.AsNUInt_MethodGroup.AsNUInt_1_T1
            def __call__(self, vector: Vector64_1[AsNUInt_1_T]) -> Vector64_1[UIntPtr]:...


    # Skipped AsSByte due to it being static, abstract and generic.

    AsSByte : AsSByte_MethodGroup
    class AsSByte_MethodGroup:
        def __getitem__(self, t:typing.Type[AsSByte_1_T1]) -> AsSByte_1[AsSByte_1_T1]: ...

        AsSByte_1_T1 = typing.TypeVar('AsSByte_1_T1')
        class AsSByte_1(typing.Generic[AsSByte_1_T1]):
            AsSByte_1_T = Vector64_0.AsSByte_MethodGroup.AsSByte_1_T1
            def __call__(self, vector: Vector64_1[AsSByte_1_T]) -> Vector64_1[int]:...


    # Skipped AsSingle due to it being static, abstract and generic.

    AsSingle : AsSingle_MethodGroup
    class AsSingle_MethodGroup:
        def __getitem__(self, t:typing.Type[AsSingle_1_T1]) -> AsSingle_1[AsSingle_1_T1]: ...

        AsSingle_1_T1 = typing.TypeVar('AsSingle_1_T1')
        class AsSingle_1(typing.Generic[AsSingle_1_T1]):
            AsSingle_1_T = Vector64_0.AsSingle_MethodGroup.AsSingle_1_T1
            def __call__(self, vector: Vector64_1[AsSingle_1_T]) -> Vector64_1[float]:...


    # Skipped AsUInt16 due to it being static, abstract and generic.

    AsUInt16 : AsUInt16_MethodGroup
    class AsUInt16_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt16_1_T1]) -> AsUInt16_1[AsUInt16_1_T1]: ...

        AsUInt16_1_T1 = typing.TypeVar('AsUInt16_1_T1')
        class AsUInt16_1(typing.Generic[AsUInt16_1_T1]):
            AsUInt16_1_T = Vector64_0.AsUInt16_MethodGroup.AsUInt16_1_T1
            def __call__(self, vector: Vector64_1[AsUInt16_1_T]) -> Vector64_1[int]:...


    # Skipped AsUInt32 due to it being static, abstract and generic.

    AsUInt32 : AsUInt32_MethodGroup
    class AsUInt32_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt32_1_T1]) -> AsUInt32_1[AsUInt32_1_T1]: ...

        AsUInt32_1_T1 = typing.TypeVar('AsUInt32_1_T1')
        class AsUInt32_1(typing.Generic[AsUInt32_1_T1]):
            AsUInt32_1_T = Vector64_0.AsUInt32_MethodGroup.AsUInt32_1_T1
            def __call__(self, vector: Vector64_1[AsUInt32_1_T]) -> Vector64_1[int]:...


    # Skipped AsUInt64 due to it being static, abstract and generic.

    AsUInt64 : AsUInt64_MethodGroup
    class AsUInt64_MethodGroup:
        def __getitem__(self, t:typing.Type[AsUInt64_1_T1]) -> AsUInt64_1[AsUInt64_1_T1]: ...

        AsUInt64_1_T1 = typing.TypeVar('AsUInt64_1_T1')
        class AsUInt64_1(typing.Generic[AsUInt64_1_T1]):
            AsUInt64_1_T = Vector64_0.AsUInt64_MethodGroup.AsUInt64_1_T1
            def __call__(self, vector: Vector64_1[AsUInt64_1_T]) -> Vector64_1[int]:...


    # Skipped BitwiseAnd due to it being static, abstract and generic.

    BitwiseAnd : BitwiseAnd_MethodGroup
    class BitwiseAnd_MethodGroup:
        def __getitem__(self, t:typing.Type[BitwiseAnd_1_T1]) -> BitwiseAnd_1[BitwiseAnd_1_T1]: ...

        BitwiseAnd_1_T1 = typing.TypeVar('BitwiseAnd_1_T1')
        class BitwiseAnd_1(typing.Generic[BitwiseAnd_1_T1]):
            BitwiseAnd_1_T = Vector64_0.BitwiseAnd_MethodGroup.BitwiseAnd_1_T1
            def __call__(self, left: Vector64_1[BitwiseAnd_1_T], right: Vector64_1[BitwiseAnd_1_T]) -> Vector64_1[BitwiseAnd_1_T]:...


    # Skipped BitwiseOr due to it being static, abstract and generic.

    BitwiseOr : BitwiseOr_MethodGroup
    class BitwiseOr_MethodGroup:
        def __getitem__(self, t:typing.Type[BitwiseOr_1_T1]) -> BitwiseOr_1[BitwiseOr_1_T1]: ...

        BitwiseOr_1_T1 = typing.TypeVar('BitwiseOr_1_T1')
        class BitwiseOr_1(typing.Generic[BitwiseOr_1_T1]):
            BitwiseOr_1_T = Vector64_0.BitwiseOr_MethodGroup.BitwiseOr_1_T1
            def __call__(self, left: Vector64_1[BitwiseOr_1_T], right: Vector64_1[BitwiseOr_1_T]) -> Vector64_1[BitwiseOr_1_T]:...


    # Skipped Ceiling due to it being static, abstract and generic.

    Ceiling : Ceiling_MethodGroup
    class Ceiling_MethodGroup:
        def __call__(self, vector: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Ceiling(vector : Vector64`1) was skipped since it collides with above method

    # Skipped Clamp due to it being static, abstract and generic.

    Clamp : Clamp_MethodGroup
    class Clamp_MethodGroup:
        def __getitem__(self, t:typing.Type[Clamp_1_T1]) -> Clamp_1[Clamp_1_T1]: ...

        Clamp_1_T1 = typing.TypeVar('Clamp_1_T1')
        class Clamp_1(typing.Generic[Clamp_1_T1]):
            Clamp_1_T = Vector64_0.Clamp_MethodGroup.Clamp_1_T1
            def __call__(self, value: Vector64_1[Clamp_1_T], min: Vector64_1[Clamp_1_T], max: Vector64_1[Clamp_1_T]) -> Vector64_1[Clamp_1_T]:...


    # Skipped ClampNative due to it being static, abstract and generic.

    ClampNative : ClampNative_MethodGroup
    class ClampNative_MethodGroup:
        def __getitem__(self, t:typing.Type[ClampNative_1_T1]) -> ClampNative_1[ClampNative_1_T1]: ...

        ClampNative_1_T1 = typing.TypeVar('ClampNative_1_T1')
        class ClampNative_1(typing.Generic[ClampNative_1_T1]):
            ClampNative_1_T = Vector64_0.ClampNative_MethodGroup.ClampNative_1_T1
            def __call__(self, value: Vector64_1[ClampNative_1_T], min: Vector64_1[ClampNative_1_T], max: Vector64_1[ClampNative_1_T]) -> Vector64_1[ClampNative_1_T]:...


    # Skipped ConditionalSelect due to it being static, abstract and generic.

    ConditionalSelect : ConditionalSelect_MethodGroup
    class ConditionalSelect_MethodGroup:
        def __getitem__(self, t:typing.Type[ConditionalSelect_1_T1]) -> ConditionalSelect_1[ConditionalSelect_1_T1]: ...

        ConditionalSelect_1_T1 = typing.TypeVar('ConditionalSelect_1_T1')
        class ConditionalSelect_1(typing.Generic[ConditionalSelect_1_T1]):
            ConditionalSelect_1_T = Vector64_0.ConditionalSelect_MethodGroup.ConditionalSelect_1_T1
            def __call__(self, condition: Vector64_1[ConditionalSelect_1_T], left: Vector64_1[ConditionalSelect_1_T], right: Vector64_1[ConditionalSelect_1_T]) -> Vector64_1[ConditionalSelect_1_T]:...


    # Skipped ConvertToDouble due to it being static, abstract and generic.

    ConvertToDouble : ConvertToDouble_MethodGroup
    class ConvertToDouble_MethodGroup:
        def __call__(self, vector: Vector64_1[int]) -> Vector64_1[float]:...
        # Method ConvertToDouble(vector : Vector64`1) was skipped since it collides with above method

    # Skipped ConvertToSingle due to it being static, abstract and generic.

    ConvertToSingle : ConvertToSingle_MethodGroup
    class ConvertToSingle_MethodGroup:
        def __call__(self, vector: Vector64_1[int]) -> Vector64_1[float]:...
        # Method ConvertToSingle(vector : Vector64`1) was skipped since it collides with above method

    # Skipped CopySign due to it being static, abstract and generic.

    CopySign : CopySign_MethodGroup
    class CopySign_MethodGroup:
        def __getitem__(self, t:typing.Type[CopySign_1_T1]) -> CopySign_1[CopySign_1_T1]: ...

        CopySign_1_T1 = typing.TypeVar('CopySign_1_T1')
        class CopySign_1(typing.Generic[CopySign_1_T1]):
            CopySign_1_T = Vector64_0.CopySign_MethodGroup.CopySign_1_T1
            def __call__(self, value: Vector64_1[CopySign_1_T], sign: Vector64_1[CopySign_1_T]) -> Vector64_1[CopySign_1_T]:...


    # Skipped CopyTo due to it being static, abstract and generic.

    CopyTo : CopyTo_MethodGroup
    class CopyTo_MethodGroup:
        def __getitem__(self, t:typing.Type[CopyTo_1_T1]) -> CopyTo_1[CopyTo_1_T1]: ...

        CopyTo_1_T1 = typing.TypeVar('CopyTo_1_T1')
        class CopyTo_1(typing.Generic[CopyTo_1_T1]):
            CopyTo_1_T = Vector64_0.CopyTo_MethodGroup.CopyTo_1_T1
            @typing.overload
            def __call__(self, vector: Vector64_1[CopyTo_1_T], destination: Array_1[CopyTo_1_T]) -> None:...
            @typing.overload
            def __call__(self, vector: Vector64_1[CopyTo_1_T], destination: Span_1[CopyTo_1_T]) -> None:...
            @typing.overload
            def __call__(self, vector: Vector64_1[CopyTo_1_T], destination: Array_1[CopyTo_1_T], startIndex: int) -> None:...


    # Skipped Cos due to it being static, abstract and generic.

    Cos : Cos_MethodGroup
    class Cos_MethodGroup:
        def __call__(self, vector: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Cos(vector : Vector64`1) was skipped since it collides with above method

    # Skipped Count due to it being static, abstract and generic.

    Count : Count_MethodGroup
    class Count_MethodGroup:
        def __getitem__(self, t:typing.Type[Count_1_T1]) -> Count_1[Count_1_T1]: ...

        Count_1_T1 = typing.TypeVar('Count_1_T1')
        class Count_1(typing.Generic[Count_1_T1]):
            Count_1_T = Vector64_0.Count_MethodGroup.Count_1_T1
            def __call__(self, vector: Vector64_1[Count_1_T], value: Count_1_T) -> int:...


    # Skipped CountWhereAllBitsSet due to it being static, abstract and generic.

    CountWhereAllBitsSet : CountWhereAllBitsSet_MethodGroup
    class CountWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[CountWhereAllBitsSet_1_T1]) -> CountWhereAllBitsSet_1[CountWhereAllBitsSet_1_T1]: ...

        CountWhereAllBitsSet_1_T1 = typing.TypeVar('CountWhereAllBitsSet_1_T1')
        class CountWhereAllBitsSet_1(typing.Generic[CountWhereAllBitsSet_1_T1]):
            CountWhereAllBitsSet_1_T = Vector64_0.CountWhereAllBitsSet_MethodGroup.CountWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector64_1[CountWhereAllBitsSet_1_T]) -> int:...


    # Skipped Create due to it being static, abstract and generic.

    Create : Create_MethodGroup
    class Create_MethodGroup:
        def __getitem__(self, t:typing.Type[Create_1_T1]) -> Create_1[Create_1_T1]: ...

        Create_1_T1 = typing.TypeVar('Create_1_T1')
        class Create_1(typing.Generic[Create_1_T1]):
            Create_1_T = Vector64_0.Create_MethodGroup.Create_1_T1
            @typing.overload
            def __call__(self, values: Array_1[Create_1_T]) -> Vector64_1[Create_1_T]:...
            @typing.overload
            def __call__(self, values: ReadOnlySpan_1[Create_1_T]) -> Vector64_1[Create_1_T]:...
            @typing.overload
            def __call__(self, value: Create_1_T) -> Vector64_1[Create_1_T]:...
            @typing.overload
            def __call__(self, values: Array_1[Create_1_T], index: int) -> Vector64_1[Create_1_T]:...

        @typing.overload
        def __call__(self, value: float) -> Vector64_1[float]:...
        # Method Create(value : Single) was skipped since it collides with above method
        # Method Create(value : Byte) was skipped since it collides with above method
        # Method Create(value : Int16) was skipped since it collides with above method
        # Method Create(value : Int32) was skipped since it collides with above method
        # Method Create(value : Int64) was skipped since it collides with above method
        # Method Create(value : SByte) was skipped since it collides with above method
        # Method Create(value : UInt16) was skipped since it collides with above method
        # Method Create(value : UInt32) was skipped since it collides with above method
        # Method Create(value : UInt64) was skipped since it collides with above method
        # Method Create(value : IntPtr) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: UIntPtr) -> Vector64_1[UIntPtr]:...
        @typing.overload
        def __call__(self, e0: float, e1: float) -> Vector64_1[float]:...
        # Method Create(e0 : Int32, e1 : Int32) was skipped since it collides with above method
        # Method Create(e0 : UInt32, e1 : UInt32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: int, e1: int, e2: int, e3: int) -> Vector64_1[int]:...
        # Method Create(e0 : UInt16, e1 : UInt16, e2 : UInt16, e3 : UInt16) was skipped since it collides with above method
        @typing.overload
        def __call__(self, e0: int, e1: int, e2: int, e3: int, e4: int, e5: int, e6: int, e7: int) -> Vector64_1[int]:...
        # Method Create(e0 : SByte, e1 : SByte, e2 : SByte, e3 : SByte, e4 : SByte, e5 : SByte, e6 : SByte, e7 : SByte) was skipped since it collides with above method

    # Skipped CreateScalar due to it being static, abstract and generic.

    CreateScalar : CreateScalar_MethodGroup
    class CreateScalar_MethodGroup:
        def __getitem__(self, t:typing.Type[CreateScalar_1_T1]) -> CreateScalar_1[CreateScalar_1_T1]: ...

        CreateScalar_1_T1 = typing.TypeVar('CreateScalar_1_T1')
        class CreateScalar_1(typing.Generic[CreateScalar_1_T1]):
            CreateScalar_1_T = Vector64_0.CreateScalar_MethodGroup.CreateScalar_1_T1
            def __call__(self, value: CreateScalar_1_T) -> Vector64_1[CreateScalar_1_T]:...

        @typing.overload
        def __call__(self, value: float) -> Vector64_1[float]:...
        # Method CreateScalar(value : Single) was skipped since it collides with above method
        # Method CreateScalar(value : Byte) was skipped since it collides with above method
        # Method CreateScalar(value : Int16) was skipped since it collides with above method
        # Method CreateScalar(value : Int32) was skipped since it collides with above method
        # Method CreateScalar(value : Int64) was skipped since it collides with above method
        # Method CreateScalar(value : SByte) was skipped since it collides with above method
        # Method CreateScalar(value : UInt16) was skipped since it collides with above method
        # Method CreateScalar(value : UInt32) was skipped since it collides with above method
        # Method CreateScalar(value : UInt64) was skipped since it collides with above method
        # Method CreateScalar(value : IntPtr) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: UIntPtr) -> Vector64_1[UIntPtr]:...

    # Skipped CreateScalarUnsafe due to it being static, abstract and generic.

    CreateScalarUnsafe : CreateScalarUnsafe_MethodGroup
    class CreateScalarUnsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[CreateScalarUnsafe_1_T1]) -> CreateScalarUnsafe_1[CreateScalarUnsafe_1_T1]: ...

        CreateScalarUnsafe_1_T1 = typing.TypeVar('CreateScalarUnsafe_1_T1')
        class CreateScalarUnsafe_1(typing.Generic[CreateScalarUnsafe_1_T1]):
            CreateScalarUnsafe_1_T = Vector64_0.CreateScalarUnsafe_MethodGroup.CreateScalarUnsafe_1_T1
            def __call__(self, value: CreateScalarUnsafe_1_T) -> Vector64_1[CreateScalarUnsafe_1_T]:...

        @typing.overload
        def __call__(self, value: float) -> Vector64_1[float]:...
        # Method CreateScalarUnsafe(value : Single) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Byte) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int16) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int32) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : Int64) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : SByte) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt16) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt32) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : UInt64) was skipped since it collides with above method
        # Method CreateScalarUnsafe(value : IntPtr) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: UIntPtr) -> Vector64_1[UIntPtr]:...

    # Skipped CreateSequence due to it being static, abstract and generic.

    CreateSequence : CreateSequence_MethodGroup
    class CreateSequence_MethodGroup:
        def __getitem__(self, t:typing.Type[CreateSequence_1_T1]) -> CreateSequence_1[CreateSequence_1_T1]: ...

        CreateSequence_1_T1 = typing.TypeVar('CreateSequence_1_T1')
        class CreateSequence_1(typing.Generic[CreateSequence_1_T1]):
            CreateSequence_1_T = Vector64_0.CreateSequence_MethodGroup.CreateSequence_1_T1
            def __call__(self, start: CreateSequence_1_T, step: CreateSequence_1_T) -> Vector64_1[CreateSequence_1_T]:...


    # Skipped DegreesToRadians due to it being static, abstract and generic.

    DegreesToRadians : DegreesToRadians_MethodGroup
    class DegreesToRadians_MethodGroup:
        def __call__(self, degrees: Vector64_1[float]) -> Vector64_1[float]:...
        # Method DegreesToRadians(degrees : Vector64`1) was skipped since it collides with above method

    # Skipped Divide due to it being static, abstract and generic.

    Divide : Divide_MethodGroup
    class Divide_MethodGroup:
        def __getitem__(self, t:typing.Type[Divide_1_T1]) -> Divide_1[Divide_1_T1]: ...

        Divide_1_T1 = typing.TypeVar('Divide_1_T1')
        class Divide_1(typing.Generic[Divide_1_T1]):
            Divide_1_T = Vector64_0.Divide_MethodGroup.Divide_1_T1
            @typing.overload
            def __call__(self, left: Vector64_1[Divide_1_T], right: Vector64_1[Divide_1_T]) -> Vector64_1[Divide_1_T]:...
            @typing.overload
            def __call__(self, left: Vector64_1[Divide_1_T], right: Divide_1_T) -> Vector64_1[Divide_1_T]:...


    # Skipped Dot due to it being static, abstract and generic.

    Dot : Dot_MethodGroup
    class Dot_MethodGroup:
        def __getitem__(self, t:typing.Type[Dot_1_T1]) -> Dot_1[Dot_1_T1]: ...

        Dot_1_T1 = typing.TypeVar('Dot_1_T1')
        class Dot_1(typing.Generic[Dot_1_T1]):
            Dot_1_T = Vector64_0.Dot_MethodGroup.Dot_1_T1
            def __call__(self, left: Vector64_1[Dot_1_T], right: Vector64_1[Dot_1_T]) -> Dot_1_T:...


    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup
    class Equals_MethodGroup:
        def __getitem__(self, t:typing.Type[Equals_1_T1]) -> Equals_1[Equals_1_T1]: ...

        Equals_1_T1 = typing.TypeVar('Equals_1_T1')
        class Equals_1(typing.Generic[Equals_1_T1]):
            Equals_1_T = Vector64_0.Equals_MethodGroup.Equals_1_T1
            def __call__(self, left: Vector64_1[Equals_1_T], right: Vector64_1[Equals_1_T]) -> Vector64_1[Equals_1_T]:...


    # Skipped EqualsAll due to it being static, abstract and generic.

    EqualsAll : EqualsAll_MethodGroup
    class EqualsAll_MethodGroup:
        def __getitem__(self, t:typing.Type[EqualsAll_1_T1]) -> EqualsAll_1[EqualsAll_1_T1]: ...

        EqualsAll_1_T1 = typing.TypeVar('EqualsAll_1_T1')
        class EqualsAll_1(typing.Generic[EqualsAll_1_T1]):
            EqualsAll_1_T = Vector64_0.EqualsAll_MethodGroup.EqualsAll_1_T1
            def __call__(self, left: Vector64_1[EqualsAll_1_T], right: Vector64_1[EqualsAll_1_T]) -> bool:...


    # Skipped EqualsAny due to it being static, abstract and generic.

    EqualsAny : EqualsAny_MethodGroup
    class EqualsAny_MethodGroup:
        def __getitem__(self, t:typing.Type[EqualsAny_1_T1]) -> EqualsAny_1[EqualsAny_1_T1]: ...

        EqualsAny_1_T1 = typing.TypeVar('EqualsAny_1_T1')
        class EqualsAny_1(typing.Generic[EqualsAny_1_T1]):
            EqualsAny_1_T = Vector64_0.EqualsAny_MethodGroup.EqualsAny_1_T1
            def __call__(self, left: Vector64_1[EqualsAny_1_T], right: Vector64_1[EqualsAny_1_T]) -> bool:...


    # Skipped Exp due to it being static, abstract and generic.

    Exp : Exp_MethodGroup
    class Exp_MethodGroup:
        def __call__(self, vector: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Exp(vector : Vector64`1) was skipped since it collides with above method

    # Skipped ExtractMostSignificantBits due to it being static, abstract and generic.

    ExtractMostSignificantBits : ExtractMostSignificantBits_MethodGroup
    class ExtractMostSignificantBits_MethodGroup:
        def __getitem__(self, t:typing.Type[ExtractMostSignificantBits_1_T1]) -> ExtractMostSignificantBits_1[ExtractMostSignificantBits_1_T1]: ...

        ExtractMostSignificantBits_1_T1 = typing.TypeVar('ExtractMostSignificantBits_1_T1')
        class ExtractMostSignificantBits_1(typing.Generic[ExtractMostSignificantBits_1_T1]):
            ExtractMostSignificantBits_1_T = Vector64_0.ExtractMostSignificantBits_MethodGroup.ExtractMostSignificantBits_1_T1
            def __call__(self, vector: Vector64_1[ExtractMostSignificantBits_1_T]) -> int:...


    # Skipped Floor due to it being static, abstract and generic.

    Floor : Floor_MethodGroup
    class Floor_MethodGroup:
        def __call__(self, vector: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Floor(vector : Vector64`1) was skipped since it collides with above method

    # Skipped FusedMultiplyAdd due to it being static, abstract and generic.

    FusedMultiplyAdd : FusedMultiplyAdd_MethodGroup
    class FusedMultiplyAdd_MethodGroup:
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float], addend: Vector64_1[float]) -> Vector64_1[float]:...
        # Method FusedMultiplyAdd(left : Vector64`1, right : Vector64`1, addend : Vector64`1) was skipped since it collides with above method

    # Skipped GetElement due to it being static, abstract and generic.

    GetElement : GetElement_MethodGroup
    class GetElement_MethodGroup:
        def __getitem__(self, t:typing.Type[GetElement_1_T1]) -> GetElement_1[GetElement_1_T1]: ...

        GetElement_1_T1 = typing.TypeVar('GetElement_1_T1')
        class GetElement_1(typing.Generic[GetElement_1_T1]):
            GetElement_1_T = Vector64_0.GetElement_MethodGroup.GetElement_1_T1
            def __call__(self, vector: Vector64_1[GetElement_1_T], index: int) -> GetElement_1_T:...


    # Skipped GreaterThan due to it being static, abstract and generic.

    GreaterThan : GreaterThan_MethodGroup
    class GreaterThan_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThan_1_T1]) -> GreaterThan_1[GreaterThan_1_T1]: ...

        GreaterThan_1_T1 = typing.TypeVar('GreaterThan_1_T1')
        class GreaterThan_1(typing.Generic[GreaterThan_1_T1]):
            GreaterThan_1_T = Vector64_0.GreaterThan_MethodGroup.GreaterThan_1_T1
            def __call__(self, left: Vector64_1[GreaterThan_1_T], right: Vector64_1[GreaterThan_1_T]) -> Vector64_1[GreaterThan_1_T]:...


    # Skipped GreaterThanAll due to it being static, abstract and generic.

    GreaterThanAll : GreaterThanAll_MethodGroup
    class GreaterThanAll_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanAll_1_T1]) -> GreaterThanAll_1[GreaterThanAll_1_T1]: ...

        GreaterThanAll_1_T1 = typing.TypeVar('GreaterThanAll_1_T1')
        class GreaterThanAll_1(typing.Generic[GreaterThanAll_1_T1]):
            GreaterThanAll_1_T = Vector64_0.GreaterThanAll_MethodGroup.GreaterThanAll_1_T1
            def __call__(self, left: Vector64_1[GreaterThanAll_1_T], right: Vector64_1[GreaterThanAll_1_T]) -> bool:...


    # Skipped GreaterThanAny due to it being static, abstract and generic.

    GreaterThanAny : GreaterThanAny_MethodGroup
    class GreaterThanAny_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanAny_1_T1]) -> GreaterThanAny_1[GreaterThanAny_1_T1]: ...

        GreaterThanAny_1_T1 = typing.TypeVar('GreaterThanAny_1_T1')
        class GreaterThanAny_1(typing.Generic[GreaterThanAny_1_T1]):
            GreaterThanAny_1_T = Vector64_0.GreaterThanAny_MethodGroup.GreaterThanAny_1_T1
            def __call__(self, left: Vector64_1[GreaterThanAny_1_T], right: Vector64_1[GreaterThanAny_1_T]) -> bool:...


    # Skipped GreaterThanOrEqual due to it being static, abstract and generic.

    GreaterThanOrEqual : GreaterThanOrEqual_MethodGroup
    class GreaterThanOrEqual_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqual_1_T1]) -> GreaterThanOrEqual_1[GreaterThanOrEqual_1_T1]: ...

        GreaterThanOrEqual_1_T1 = typing.TypeVar('GreaterThanOrEqual_1_T1')
        class GreaterThanOrEqual_1(typing.Generic[GreaterThanOrEqual_1_T1]):
            GreaterThanOrEqual_1_T = Vector64_0.GreaterThanOrEqual_MethodGroup.GreaterThanOrEqual_1_T1
            def __call__(self, left: Vector64_1[GreaterThanOrEqual_1_T], right: Vector64_1[GreaterThanOrEqual_1_T]) -> Vector64_1[GreaterThanOrEqual_1_T]:...


    # Skipped GreaterThanOrEqualAll due to it being static, abstract and generic.

    GreaterThanOrEqualAll : GreaterThanOrEqualAll_MethodGroup
    class GreaterThanOrEqualAll_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqualAll_1_T1]) -> GreaterThanOrEqualAll_1[GreaterThanOrEqualAll_1_T1]: ...

        GreaterThanOrEqualAll_1_T1 = typing.TypeVar('GreaterThanOrEqualAll_1_T1')
        class GreaterThanOrEqualAll_1(typing.Generic[GreaterThanOrEqualAll_1_T1]):
            GreaterThanOrEqualAll_1_T = Vector64_0.GreaterThanOrEqualAll_MethodGroup.GreaterThanOrEqualAll_1_T1
            def __call__(self, left: Vector64_1[GreaterThanOrEqualAll_1_T], right: Vector64_1[GreaterThanOrEqualAll_1_T]) -> bool:...


    # Skipped GreaterThanOrEqualAny due to it being static, abstract and generic.

    GreaterThanOrEqualAny : GreaterThanOrEqualAny_MethodGroup
    class GreaterThanOrEqualAny_MethodGroup:
        def __getitem__(self, t:typing.Type[GreaterThanOrEqualAny_1_T1]) -> GreaterThanOrEqualAny_1[GreaterThanOrEqualAny_1_T1]: ...

        GreaterThanOrEqualAny_1_T1 = typing.TypeVar('GreaterThanOrEqualAny_1_T1')
        class GreaterThanOrEqualAny_1(typing.Generic[GreaterThanOrEqualAny_1_T1]):
            GreaterThanOrEqualAny_1_T = Vector64_0.GreaterThanOrEqualAny_MethodGroup.GreaterThanOrEqualAny_1_T1
            def __call__(self, left: Vector64_1[GreaterThanOrEqualAny_1_T], right: Vector64_1[GreaterThanOrEqualAny_1_T]) -> bool:...


    # Skipped Hypot due to it being static, abstract and generic.

    Hypot : Hypot_MethodGroup
    class Hypot_MethodGroup:
        def __call__(self, x: Vector64_1[float], y: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Hypot(x : Vector64`1, y : Vector64`1) was skipped since it collides with above method

    # Skipped IndexOf due to it being static, abstract and generic.

    IndexOf : IndexOf_MethodGroup
    class IndexOf_MethodGroup:
        def __getitem__(self, t:typing.Type[IndexOf_1_T1]) -> IndexOf_1[IndexOf_1_T1]: ...

        IndexOf_1_T1 = typing.TypeVar('IndexOf_1_T1')
        class IndexOf_1(typing.Generic[IndexOf_1_T1]):
            IndexOf_1_T = Vector64_0.IndexOf_MethodGroup.IndexOf_1_T1
            def __call__(self, vector: Vector64_1[IndexOf_1_T], value: IndexOf_1_T) -> int:...


    # Skipped IndexOfWhereAllBitsSet due to it being static, abstract and generic.

    IndexOfWhereAllBitsSet : IndexOfWhereAllBitsSet_MethodGroup
    class IndexOfWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[IndexOfWhereAllBitsSet_1_T1]) -> IndexOfWhereAllBitsSet_1[IndexOfWhereAllBitsSet_1_T1]: ...

        IndexOfWhereAllBitsSet_1_T1 = typing.TypeVar('IndexOfWhereAllBitsSet_1_T1')
        class IndexOfWhereAllBitsSet_1(typing.Generic[IndexOfWhereAllBitsSet_1_T1]):
            IndexOfWhereAllBitsSet_1_T = Vector64_0.IndexOfWhereAllBitsSet_MethodGroup.IndexOfWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector64_1[IndexOfWhereAllBitsSet_1_T]) -> int:...


    # Skipped IsEvenInteger due to it being static, abstract and generic.

    IsEvenInteger : IsEvenInteger_MethodGroup
    class IsEvenInteger_MethodGroup:
        def __getitem__(self, t:typing.Type[IsEvenInteger_1_T1]) -> IsEvenInteger_1[IsEvenInteger_1_T1]: ...

        IsEvenInteger_1_T1 = typing.TypeVar('IsEvenInteger_1_T1')
        class IsEvenInteger_1(typing.Generic[IsEvenInteger_1_T1]):
            IsEvenInteger_1_T = Vector64_0.IsEvenInteger_MethodGroup.IsEvenInteger_1_T1
            def __call__(self, vector: Vector64_1[IsEvenInteger_1_T]) -> Vector64_1[IsEvenInteger_1_T]:...


    # Skipped IsFinite due to it being static, abstract and generic.

    IsFinite : IsFinite_MethodGroup
    class IsFinite_MethodGroup:
        def __getitem__(self, t:typing.Type[IsFinite_1_T1]) -> IsFinite_1[IsFinite_1_T1]: ...

        IsFinite_1_T1 = typing.TypeVar('IsFinite_1_T1')
        class IsFinite_1(typing.Generic[IsFinite_1_T1]):
            IsFinite_1_T = Vector64_0.IsFinite_MethodGroup.IsFinite_1_T1
            def __call__(self, vector: Vector64_1[IsFinite_1_T]) -> Vector64_1[IsFinite_1_T]:...


    # Skipped IsInfinity due to it being static, abstract and generic.

    IsInfinity : IsInfinity_MethodGroup
    class IsInfinity_MethodGroup:
        def __getitem__(self, t:typing.Type[IsInfinity_1_T1]) -> IsInfinity_1[IsInfinity_1_T1]: ...

        IsInfinity_1_T1 = typing.TypeVar('IsInfinity_1_T1')
        class IsInfinity_1(typing.Generic[IsInfinity_1_T1]):
            IsInfinity_1_T = Vector64_0.IsInfinity_MethodGroup.IsInfinity_1_T1
            def __call__(self, vector: Vector64_1[IsInfinity_1_T]) -> Vector64_1[IsInfinity_1_T]:...


    # Skipped IsInteger due to it being static, abstract and generic.

    IsInteger : IsInteger_MethodGroup
    class IsInteger_MethodGroup:
        def __getitem__(self, t:typing.Type[IsInteger_1_T1]) -> IsInteger_1[IsInteger_1_T1]: ...

        IsInteger_1_T1 = typing.TypeVar('IsInteger_1_T1')
        class IsInteger_1(typing.Generic[IsInteger_1_T1]):
            IsInteger_1_T = Vector64_0.IsInteger_MethodGroup.IsInteger_1_T1
            def __call__(self, vector: Vector64_1[IsInteger_1_T]) -> Vector64_1[IsInteger_1_T]:...


    # Skipped IsNaN due to it being static, abstract and generic.

    IsNaN : IsNaN_MethodGroup
    class IsNaN_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNaN_1_T1]) -> IsNaN_1[IsNaN_1_T1]: ...

        IsNaN_1_T1 = typing.TypeVar('IsNaN_1_T1')
        class IsNaN_1(typing.Generic[IsNaN_1_T1]):
            IsNaN_1_T = Vector64_0.IsNaN_MethodGroup.IsNaN_1_T1
            def __call__(self, vector: Vector64_1[IsNaN_1_T]) -> Vector64_1[IsNaN_1_T]:...


    # Skipped IsNegative due to it being static, abstract and generic.

    IsNegative : IsNegative_MethodGroup
    class IsNegative_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNegative_1_T1]) -> IsNegative_1[IsNegative_1_T1]: ...

        IsNegative_1_T1 = typing.TypeVar('IsNegative_1_T1')
        class IsNegative_1(typing.Generic[IsNegative_1_T1]):
            IsNegative_1_T = Vector64_0.IsNegative_MethodGroup.IsNegative_1_T1
            def __call__(self, vector: Vector64_1[IsNegative_1_T]) -> Vector64_1[IsNegative_1_T]:...


    # Skipped IsNegativeInfinity due to it being static, abstract and generic.

    IsNegativeInfinity : IsNegativeInfinity_MethodGroup
    class IsNegativeInfinity_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNegativeInfinity_1_T1]) -> IsNegativeInfinity_1[IsNegativeInfinity_1_T1]: ...

        IsNegativeInfinity_1_T1 = typing.TypeVar('IsNegativeInfinity_1_T1')
        class IsNegativeInfinity_1(typing.Generic[IsNegativeInfinity_1_T1]):
            IsNegativeInfinity_1_T = Vector64_0.IsNegativeInfinity_MethodGroup.IsNegativeInfinity_1_T1
            def __call__(self, vector: Vector64_1[IsNegativeInfinity_1_T]) -> Vector64_1[IsNegativeInfinity_1_T]:...


    # Skipped IsNormal due to it being static, abstract and generic.

    IsNormal : IsNormal_MethodGroup
    class IsNormal_MethodGroup:
        def __getitem__(self, t:typing.Type[IsNormal_1_T1]) -> IsNormal_1[IsNormal_1_T1]: ...

        IsNormal_1_T1 = typing.TypeVar('IsNormal_1_T1')
        class IsNormal_1(typing.Generic[IsNormal_1_T1]):
            IsNormal_1_T = Vector64_0.IsNormal_MethodGroup.IsNormal_1_T1
            def __call__(self, vector: Vector64_1[IsNormal_1_T]) -> Vector64_1[IsNormal_1_T]:...


    # Skipped IsOddInteger due to it being static, abstract and generic.

    IsOddInteger : IsOddInteger_MethodGroup
    class IsOddInteger_MethodGroup:
        def __getitem__(self, t:typing.Type[IsOddInteger_1_T1]) -> IsOddInteger_1[IsOddInteger_1_T1]: ...

        IsOddInteger_1_T1 = typing.TypeVar('IsOddInteger_1_T1')
        class IsOddInteger_1(typing.Generic[IsOddInteger_1_T1]):
            IsOddInteger_1_T = Vector64_0.IsOddInteger_MethodGroup.IsOddInteger_1_T1
            def __call__(self, vector: Vector64_1[IsOddInteger_1_T]) -> Vector64_1[IsOddInteger_1_T]:...


    # Skipped IsPositive due to it being static, abstract and generic.

    IsPositive : IsPositive_MethodGroup
    class IsPositive_MethodGroup:
        def __getitem__(self, t:typing.Type[IsPositive_1_T1]) -> IsPositive_1[IsPositive_1_T1]: ...

        IsPositive_1_T1 = typing.TypeVar('IsPositive_1_T1')
        class IsPositive_1(typing.Generic[IsPositive_1_T1]):
            IsPositive_1_T = Vector64_0.IsPositive_MethodGroup.IsPositive_1_T1
            def __call__(self, vector: Vector64_1[IsPositive_1_T]) -> Vector64_1[IsPositive_1_T]:...


    # Skipped IsPositiveInfinity due to it being static, abstract and generic.

    IsPositiveInfinity : IsPositiveInfinity_MethodGroup
    class IsPositiveInfinity_MethodGroup:
        def __getitem__(self, t:typing.Type[IsPositiveInfinity_1_T1]) -> IsPositiveInfinity_1[IsPositiveInfinity_1_T1]: ...

        IsPositiveInfinity_1_T1 = typing.TypeVar('IsPositiveInfinity_1_T1')
        class IsPositiveInfinity_1(typing.Generic[IsPositiveInfinity_1_T1]):
            IsPositiveInfinity_1_T = Vector64_0.IsPositiveInfinity_MethodGroup.IsPositiveInfinity_1_T1
            def __call__(self, vector: Vector64_1[IsPositiveInfinity_1_T]) -> Vector64_1[IsPositiveInfinity_1_T]:...


    # Skipped IsSubnormal due to it being static, abstract and generic.

    IsSubnormal : IsSubnormal_MethodGroup
    class IsSubnormal_MethodGroup:
        def __getitem__(self, t:typing.Type[IsSubnormal_1_T1]) -> IsSubnormal_1[IsSubnormal_1_T1]: ...

        IsSubnormal_1_T1 = typing.TypeVar('IsSubnormal_1_T1')
        class IsSubnormal_1(typing.Generic[IsSubnormal_1_T1]):
            IsSubnormal_1_T = Vector64_0.IsSubnormal_MethodGroup.IsSubnormal_1_T1
            def __call__(self, vector: Vector64_1[IsSubnormal_1_T]) -> Vector64_1[IsSubnormal_1_T]:...


    # Skipped IsZero due to it being static, abstract and generic.

    IsZero : IsZero_MethodGroup
    class IsZero_MethodGroup:
        def __getitem__(self, t:typing.Type[IsZero_1_T1]) -> IsZero_1[IsZero_1_T1]: ...

        IsZero_1_T1 = typing.TypeVar('IsZero_1_T1')
        class IsZero_1(typing.Generic[IsZero_1_T1]):
            IsZero_1_T = Vector64_0.IsZero_MethodGroup.IsZero_1_T1
            def __call__(self, vector: Vector64_1[IsZero_1_T]) -> Vector64_1[IsZero_1_T]:...


    # Skipped LastIndexOf due to it being static, abstract and generic.

    LastIndexOf : LastIndexOf_MethodGroup
    class LastIndexOf_MethodGroup:
        def __getitem__(self, t:typing.Type[LastIndexOf_1_T1]) -> LastIndexOf_1[LastIndexOf_1_T1]: ...

        LastIndexOf_1_T1 = typing.TypeVar('LastIndexOf_1_T1')
        class LastIndexOf_1(typing.Generic[LastIndexOf_1_T1]):
            LastIndexOf_1_T = Vector64_0.LastIndexOf_MethodGroup.LastIndexOf_1_T1
            def __call__(self, vector: Vector64_1[LastIndexOf_1_T], value: LastIndexOf_1_T) -> int:...


    # Skipped LastIndexOfWhereAllBitsSet due to it being static, abstract and generic.

    LastIndexOfWhereAllBitsSet : LastIndexOfWhereAllBitsSet_MethodGroup
    class LastIndexOfWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[LastIndexOfWhereAllBitsSet_1_T1]) -> LastIndexOfWhereAllBitsSet_1[LastIndexOfWhereAllBitsSet_1_T1]: ...

        LastIndexOfWhereAllBitsSet_1_T1 = typing.TypeVar('LastIndexOfWhereAllBitsSet_1_T1')
        class LastIndexOfWhereAllBitsSet_1(typing.Generic[LastIndexOfWhereAllBitsSet_1_T1]):
            LastIndexOfWhereAllBitsSet_1_T = Vector64_0.LastIndexOfWhereAllBitsSet_MethodGroup.LastIndexOfWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector64_1[LastIndexOfWhereAllBitsSet_1_T]) -> int:...


    # Skipped Lerp due to it being static, abstract and generic.

    Lerp : Lerp_MethodGroup
    class Lerp_MethodGroup:
        def __call__(self, x: Vector64_1[float], y: Vector64_1[float], amount: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Lerp(x : Vector64`1, y : Vector64`1, amount : Vector64`1) was skipped since it collides with above method

    # Skipped LessThan due to it being static, abstract and generic.

    LessThan : LessThan_MethodGroup
    class LessThan_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThan_1_T1]) -> LessThan_1[LessThan_1_T1]: ...

        LessThan_1_T1 = typing.TypeVar('LessThan_1_T1')
        class LessThan_1(typing.Generic[LessThan_1_T1]):
            LessThan_1_T = Vector64_0.LessThan_MethodGroup.LessThan_1_T1
            def __call__(self, left: Vector64_1[LessThan_1_T], right: Vector64_1[LessThan_1_T]) -> Vector64_1[LessThan_1_T]:...


    # Skipped LessThanAll due to it being static, abstract and generic.

    LessThanAll : LessThanAll_MethodGroup
    class LessThanAll_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanAll_1_T1]) -> LessThanAll_1[LessThanAll_1_T1]: ...

        LessThanAll_1_T1 = typing.TypeVar('LessThanAll_1_T1')
        class LessThanAll_1(typing.Generic[LessThanAll_1_T1]):
            LessThanAll_1_T = Vector64_0.LessThanAll_MethodGroup.LessThanAll_1_T1
            def __call__(self, left: Vector64_1[LessThanAll_1_T], right: Vector64_1[LessThanAll_1_T]) -> bool:...


    # Skipped LessThanAny due to it being static, abstract and generic.

    LessThanAny : LessThanAny_MethodGroup
    class LessThanAny_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanAny_1_T1]) -> LessThanAny_1[LessThanAny_1_T1]: ...

        LessThanAny_1_T1 = typing.TypeVar('LessThanAny_1_T1')
        class LessThanAny_1(typing.Generic[LessThanAny_1_T1]):
            LessThanAny_1_T = Vector64_0.LessThanAny_MethodGroup.LessThanAny_1_T1
            def __call__(self, left: Vector64_1[LessThanAny_1_T], right: Vector64_1[LessThanAny_1_T]) -> bool:...


    # Skipped LessThanOrEqual due to it being static, abstract and generic.

    LessThanOrEqual : LessThanOrEqual_MethodGroup
    class LessThanOrEqual_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqual_1_T1]) -> LessThanOrEqual_1[LessThanOrEqual_1_T1]: ...

        LessThanOrEqual_1_T1 = typing.TypeVar('LessThanOrEqual_1_T1')
        class LessThanOrEqual_1(typing.Generic[LessThanOrEqual_1_T1]):
            LessThanOrEqual_1_T = Vector64_0.LessThanOrEqual_MethodGroup.LessThanOrEqual_1_T1
            def __call__(self, left: Vector64_1[LessThanOrEqual_1_T], right: Vector64_1[LessThanOrEqual_1_T]) -> Vector64_1[LessThanOrEqual_1_T]:...


    # Skipped LessThanOrEqualAll due to it being static, abstract and generic.

    LessThanOrEqualAll : LessThanOrEqualAll_MethodGroup
    class LessThanOrEqualAll_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqualAll_1_T1]) -> LessThanOrEqualAll_1[LessThanOrEqualAll_1_T1]: ...

        LessThanOrEqualAll_1_T1 = typing.TypeVar('LessThanOrEqualAll_1_T1')
        class LessThanOrEqualAll_1(typing.Generic[LessThanOrEqualAll_1_T1]):
            LessThanOrEqualAll_1_T = Vector64_0.LessThanOrEqualAll_MethodGroup.LessThanOrEqualAll_1_T1
            def __call__(self, left: Vector64_1[LessThanOrEqualAll_1_T], right: Vector64_1[LessThanOrEqualAll_1_T]) -> bool:...


    # Skipped LessThanOrEqualAny due to it being static, abstract and generic.

    LessThanOrEqualAny : LessThanOrEqualAny_MethodGroup
    class LessThanOrEqualAny_MethodGroup:
        def __getitem__(self, t:typing.Type[LessThanOrEqualAny_1_T1]) -> LessThanOrEqualAny_1[LessThanOrEqualAny_1_T1]: ...

        LessThanOrEqualAny_1_T1 = typing.TypeVar('LessThanOrEqualAny_1_T1')
        class LessThanOrEqualAny_1(typing.Generic[LessThanOrEqualAny_1_T1]):
            LessThanOrEqualAny_1_T = Vector64_0.LessThanOrEqualAny_MethodGroup.LessThanOrEqualAny_1_T1
            def __call__(self, left: Vector64_1[LessThanOrEqualAny_1_T], right: Vector64_1[LessThanOrEqualAny_1_T]) -> bool:...


    # Skipped Load due to it being static, abstract and generic.

    Load : Load_MethodGroup
    class Load_MethodGroup:
        def __getitem__(self, t:typing.Type[Load_1_T1]) -> Load_1[Load_1_T1]: ...

        Load_1_T1 = typing.TypeVar('Load_1_T1')
        class Load_1(typing.Generic[Load_1_T1]):
            Load_1_T = Vector64_0.Load_MethodGroup.Load_1_T1
            def __call__(self, source: clr.Reference[Load_1_T]) -> Vector64_1[Load_1_T]:...


    # Skipped LoadAligned due to it being static, abstract and generic.

    LoadAligned : LoadAligned_MethodGroup
    class LoadAligned_MethodGroup:
        def __getitem__(self, t:typing.Type[LoadAligned_1_T1]) -> LoadAligned_1[LoadAligned_1_T1]: ...

        LoadAligned_1_T1 = typing.TypeVar('LoadAligned_1_T1')
        class LoadAligned_1(typing.Generic[LoadAligned_1_T1]):
            LoadAligned_1_T = Vector64_0.LoadAligned_MethodGroup.LoadAligned_1_T1
            def __call__(self, source: clr.Reference[LoadAligned_1_T]) -> Vector64_1[LoadAligned_1_T]:...


    # Skipped LoadAlignedNonTemporal due to it being static, abstract and generic.

    LoadAlignedNonTemporal : LoadAlignedNonTemporal_MethodGroup
    class LoadAlignedNonTemporal_MethodGroup:
        def __getitem__(self, t:typing.Type[LoadAlignedNonTemporal_1_T1]) -> LoadAlignedNonTemporal_1[LoadAlignedNonTemporal_1_T1]: ...

        LoadAlignedNonTemporal_1_T1 = typing.TypeVar('LoadAlignedNonTemporal_1_T1')
        class LoadAlignedNonTemporal_1(typing.Generic[LoadAlignedNonTemporal_1_T1]):
            LoadAlignedNonTemporal_1_T = Vector64_0.LoadAlignedNonTemporal_MethodGroup.LoadAlignedNonTemporal_1_T1
            def __call__(self, source: clr.Reference[LoadAlignedNonTemporal_1_T]) -> Vector64_1[LoadAlignedNonTemporal_1_T]:...


    # Skipped LoadUnsafe due to it being static, abstract and generic.

    LoadUnsafe : LoadUnsafe_MethodGroup
    class LoadUnsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[LoadUnsafe_1_T1]) -> LoadUnsafe_1[LoadUnsafe_1_T1]: ...

        LoadUnsafe_1_T1 = typing.TypeVar('LoadUnsafe_1_T1')
        class LoadUnsafe_1(typing.Generic[LoadUnsafe_1_T1]):
            LoadUnsafe_1_T = Vector64_0.LoadUnsafe_MethodGroup.LoadUnsafe_1_T1
            @typing.overload
            def __call__(self, source: clr.Reference[LoadUnsafe_1_T]) -> Vector64_1[LoadUnsafe_1_T]:...
            @typing.overload
            def __call__(self, source: clr.Reference[LoadUnsafe_1_T], elementOffset: UIntPtr) -> Vector64_1[LoadUnsafe_1_T]:...


    # Skipped Log due to it being static, abstract and generic.

    Log : Log_MethodGroup
    class Log_MethodGroup:
        def __call__(self, vector: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Log(vector : Vector64`1) was skipped since it collides with above method

    # Skipped Log2 due to it being static, abstract and generic.

    Log2 : Log2_MethodGroup
    class Log2_MethodGroup:
        def __call__(self, vector: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Log2(vector : Vector64`1) was skipped since it collides with above method

    # Skipped Max due to it being static, abstract and generic.

    Max : Max_MethodGroup
    class Max_MethodGroup:
        def __getitem__(self, t:typing.Type[Max_1_T1]) -> Max_1[Max_1_T1]: ...

        Max_1_T1 = typing.TypeVar('Max_1_T1')
        class Max_1(typing.Generic[Max_1_T1]):
            Max_1_T = Vector64_0.Max_MethodGroup.Max_1_T1
            def __call__(self, left: Vector64_1[Max_1_T], right: Vector64_1[Max_1_T]) -> Vector64_1[Max_1_T]:...


    # Skipped MaxMagnitude due to it being static, abstract and generic.

    MaxMagnitude : MaxMagnitude_MethodGroup
    class MaxMagnitude_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxMagnitude_1_T1]) -> MaxMagnitude_1[MaxMagnitude_1_T1]: ...

        MaxMagnitude_1_T1 = typing.TypeVar('MaxMagnitude_1_T1')
        class MaxMagnitude_1(typing.Generic[MaxMagnitude_1_T1]):
            MaxMagnitude_1_T = Vector64_0.MaxMagnitude_MethodGroup.MaxMagnitude_1_T1
            def __call__(self, left: Vector64_1[MaxMagnitude_1_T], right: Vector64_1[MaxMagnitude_1_T]) -> Vector64_1[MaxMagnitude_1_T]:...


    # Skipped MaxMagnitudeNumber due to it being static, abstract and generic.

    MaxMagnitudeNumber : MaxMagnitudeNumber_MethodGroup
    class MaxMagnitudeNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxMagnitudeNumber_1_T1]) -> MaxMagnitudeNumber_1[MaxMagnitudeNumber_1_T1]: ...

        MaxMagnitudeNumber_1_T1 = typing.TypeVar('MaxMagnitudeNumber_1_T1')
        class MaxMagnitudeNumber_1(typing.Generic[MaxMagnitudeNumber_1_T1]):
            MaxMagnitudeNumber_1_T = Vector64_0.MaxMagnitudeNumber_MethodGroup.MaxMagnitudeNumber_1_T1
            def __call__(self, left: Vector64_1[MaxMagnitudeNumber_1_T], right: Vector64_1[MaxMagnitudeNumber_1_T]) -> Vector64_1[MaxMagnitudeNumber_1_T]:...


    # Skipped MaxNative due to it being static, abstract and generic.

    MaxNative : MaxNative_MethodGroup
    class MaxNative_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxNative_1_T1]) -> MaxNative_1[MaxNative_1_T1]: ...

        MaxNative_1_T1 = typing.TypeVar('MaxNative_1_T1')
        class MaxNative_1(typing.Generic[MaxNative_1_T1]):
            MaxNative_1_T = Vector64_0.MaxNative_MethodGroup.MaxNative_1_T1
            def __call__(self, left: Vector64_1[MaxNative_1_T], right: Vector64_1[MaxNative_1_T]) -> Vector64_1[MaxNative_1_T]:...


    # Skipped MaxNumber due to it being static, abstract and generic.

    MaxNumber : MaxNumber_MethodGroup
    class MaxNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MaxNumber_1_T1]) -> MaxNumber_1[MaxNumber_1_T1]: ...

        MaxNumber_1_T1 = typing.TypeVar('MaxNumber_1_T1')
        class MaxNumber_1(typing.Generic[MaxNumber_1_T1]):
            MaxNumber_1_T = Vector64_0.MaxNumber_MethodGroup.MaxNumber_1_T1
            def __call__(self, left: Vector64_1[MaxNumber_1_T], right: Vector64_1[MaxNumber_1_T]) -> Vector64_1[MaxNumber_1_T]:...


    # Skipped Min due to it being static, abstract and generic.

    Min : Min_MethodGroup
    class Min_MethodGroup:
        def __getitem__(self, t:typing.Type[Min_1_T1]) -> Min_1[Min_1_T1]: ...

        Min_1_T1 = typing.TypeVar('Min_1_T1')
        class Min_1(typing.Generic[Min_1_T1]):
            Min_1_T = Vector64_0.Min_MethodGroup.Min_1_T1
            def __call__(self, left: Vector64_1[Min_1_T], right: Vector64_1[Min_1_T]) -> Vector64_1[Min_1_T]:...


    # Skipped MinMagnitude due to it being static, abstract and generic.

    MinMagnitude : MinMagnitude_MethodGroup
    class MinMagnitude_MethodGroup:
        def __getitem__(self, t:typing.Type[MinMagnitude_1_T1]) -> MinMagnitude_1[MinMagnitude_1_T1]: ...

        MinMagnitude_1_T1 = typing.TypeVar('MinMagnitude_1_T1')
        class MinMagnitude_1(typing.Generic[MinMagnitude_1_T1]):
            MinMagnitude_1_T = Vector64_0.MinMagnitude_MethodGroup.MinMagnitude_1_T1
            def __call__(self, left: Vector64_1[MinMagnitude_1_T], right: Vector64_1[MinMagnitude_1_T]) -> Vector64_1[MinMagnitude_1_T]:...


    # Skipped MinMagnitudeNumber due to it being static, abstract and generic.

    MinMagnitudeNumber : MinMagnitudeNumber_MethodGroup
    class MinMagnitudeNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MinMagnitudeNumber_1_T1]) -> MinMagnitudeNumber_1[MinMagnitudeNumber_1_T1]: ...

        MinMagnitudeNumber_1_T1 = typing.TypeVar('MinMagnitudeNumber_1_T1')
        class MinMagnitudeNumber_1(typing.Generic[MinMagnitudeNumber_1_T1]):
            MinMagnitudeNumber_1_T = Vector64_0.MinMagnitudeNumber_MethodGroup.MinMagnitudeNumber_1_T1
            def __call__(self, left: Vector64_1[MinMagnitudeNumber_1_T], right: Vector64_1[MinMagnitudeNumber_1_T]) -> Vector64_1[MinMagnitudeNumber_1_T]:...


    # Skipped MinNative due to it being static, abstract and generic.

    MinNative : MinNative_MethodGroup
    class MinNative_MethodGroup:
        def __getitem__(self, t:typing.Type[MinNative_1_T1]) -> MinNative_1[MinNative_1_T1]: ...

        MinNative_1_T1 = typing.TypeVar('MinNative_1_T1')
        class MinNative_1(typing.Generic[MinNative_1_T1]):
            MinNative_1_T = Vector64_0.MinNative_MethodGroup.MinNative_1_T1
            def __call__(self, left: Vector64_1[MinNative_1_T], right: Vector64_1[MinNative_1_T]) -> Vector64_1[MinNative_1_T]:...


    # Skipped MinNumber due to it being static, abstract and generic.

    MinNumber : MinNumber_MethodGroup
    class MinNumber_MethodGroup:
        def __getitem__(self, t:typing.Type[MinNumber_1_T1]) -> MinNumber_1[MinNumber_1_T1]: ...

        MinNumber_1_T1 = typing.TypeVar('MinNumber_1_T1')
        class MinNumber_1(typing.Generic[MinNumber_1_T1]):
            MinNumber_1_T = Vector64_0.MinNumber_MethodGroup.MinNumber_1_T1
            def __call__(self, left: Vector64_1[MinNumber_1_T], right: Vector64_1[MinNumber_1_T]) -> Vector64_1[MinNumber_1_T]:...


    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        def __getitem__(self, t:typing.Type[Multiply_1_T1]) -> Multiply_1[Multiply_1_T1]: ...

        Multiply_1_T1 = typing.TypeVar('Multiply_1_T1')
        class Multiply_1(typing.Generic[Multiply_1_T1]):
            Multiply_1_T = Vector64_0.Multiply_MethodGroup.Multiply_1_T1
            @typing.overload
            def __call__(self, left: Vector64_1[Multiply_1_T], right: Vector64_1[Multiply_1_T]) -> Vector64_1[Multiply_1_T]:...
            @typing.overload
            def __call__(self, left: Vector64_1[Multiply_1_T], right: Multiply_1_T) -> Vector64_1[Multiply_1_T]:...
            @typing.overload
            def __call__(self, left: Multiply_1_T, right: Vector64_1[Multiply_1_T]) -> Vector64_1[Multiply_1_T]:...


    # Skipped MultiplyAddEstimate due to it being static, abstract and generic.

    MultiplyAddEstimate : MultiplyAddEstimate_MethodGroup
    class MultiplyAddEstimate_MethodGroup:
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float], addend: Vector64_1[float]) -> Vector64_1[float]:...
        # Method MultiplyAddEstimate(left : Vector64`1, right : Vector64`1, addend : Vector64`1) was skipped since it collides with above method

    # Skipped Narrow due to it being static, abstract and generic.

    Narrow : Narrow_MethodGroup
    class Narrow_MethodGroup:
        def __call__(self, lower: Vector64_1[float], upper: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Narrow(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method Narrow(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method

    # Skipped NarrowWithSaturation due to it being static, abstract and generic.

    NarrowWithSaturation : NarrowWithSaturation_MethodGroup
    class NarrowWithSaturation_MethodGroup:
        def __call__(self, lower: Vector64_1[float], upper: Vector64_1[float]) -> Vector64_1[float]:...
        # Method NarrowWithSaturation(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method
        # Method NarrowWithSaturation(lower : Vector64`1, upper : Vector64`1) was skipped since it collides with above method

    # Skipped Negate due to it being static, abstract and generic.

    Negate : Negate_MethodGroup
    class Negate_MethodGroup:
        def __getitem__(self, t:typing.Type[Negate_1_T1]) -> Negate_1[Negate_1_T1]: ...

        Negate_1_T1 = typing.TypeVar('Negate_1_T1')
        class Negate_1(typing.Generic[Negate_1_T1]):
            Negate_1_T = Vector64_0.Negate_MethodGroup.Negate_1_T1
            def __call__(self, vector: Vector64_1[Negate_1_T]) -> Vector64_1[Negate_1_T]:...


    # Skipped None due to it being static, abstract and generic.

    None : None_MethodGroup
    class None_MethodGroup:
        def __getitem__(self, t:typing.Type[None_1_T1]) -> None_1[None_1_T1]: ...

        None_1_T1 = typing.TypeVar('None_1_T1')
        class None_1(typing.Generic[None_1_T1]):
            None_1_T = Vector64_0.None_MethodGroup.None_1_T1
            def __call__(self, vector: Vector64_1[None_1_T], value: None_1_T) -> bool:...


    # Skipped NoneWhereAllBitsSet due to it being static, abstract and generic.

    NoneWhereAllBitsSet : NoneWhereAllBitsSet_MethodGroup
    class NoneWhereAllBitsSet_MethodGroup:
        def __getitem__(self, t:typing.Type[NoneWhereAllBitsSet_1_T1]) -> NoneWhereAllBitsSet_1[NoneWhereAllBitsSet_1_T1]: ...

        NoneWhereAllBitsSet_1_T1 = typing.TypeVar('NoneWhereAllBitsSet_1_T1')
        class NoneWhereAllBitsSet_1(typing.Generic[NoneWhereAllBitsSet_1_T1]):
            NoneWhereAllBitsSet_1_T = Vector64_0.NoneWhereAllBitsSet_MethodGroup.NoneWhereAllBitsSet_1_T1
            def __call__(self, vector: Vector64_1[NoneWhereAllBitsSet_1_T]) -> bool:...


    # Skipped OnesComplement due to it being static, abstract and generic.

    OnesComplement : OnesComplement_MethodGroup
    class OnesComplement_MethodGroup:
        def __getitem__(self, t:typing.Type[OnesComplement_1_T1]) -> OnesComplement_1[OnesComplement_1_T1]: ...

        OnesComplement_1_T1 = typing.TypeVar('OnesComplement_1_T1')
        class OnesComplement_1(typing.Generic[OnesComplement_1_T1]):
            OnesComplement_1_T = Vector64_0.OnesComplement_MethodGroup.OnesComplement_1_T1
            def __call__(self, vector: Vector64_1[OnesComplement_1_T]) -> Vector64_1[OnesComplement_1_T]:...


    # Skipped RadiansToDegrees due to it being static, abstract and generic.

    RadiansToDegrees : RadiansToDegrees_MethodGroup
    class RadiansToDegrees_MethodGroup:
        def __call__(self, radians: Vector64_1[float]) -> Vector64_1[float]:...
        # Method RadiansToDegrees(radians : Vector64`1) was skipped since it collides with above method

    # Skipped Round due to it being static, abstract and generic.

    Round : Round_MethodGroup
    class Round_MethodGroup:
        @typing.overload
        def __call__(self, vector: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Round(vector : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, vector: Vector64_1[float], mode: MidpointRounding) -> Vector64_1[float]:...
        # Method Round(vector : Vector64`1, mode : MidpointRounding) was skipped since it collides with above method

    # Skipped ShiftLeft due to it being static, abstract and generic.

    ShiftLeft : ShiftLeft_MethodGroup
    class ShiftLeft_MethodGroup:
        @typing.overload
        def __call__(self, vector: Vector64_1[int], shiftCount: int) -> Vector64_1[int]:...
        # Method ShiftLeft(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftLeft(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, vector: Vector64_1[UIntPtr], shiftCount: int) -> Vector64_1[UIntPtr]:...

    # Skipped ShiftRightArithmetic due to it being static, abstract and generic.

    ShiftRightArithmetic : ShiftRightArithmetic_MethodGroup
    class ShiftRightArithmetic_MethodGroup:
        def __call__(self, vector: Vector64_1[int], shiftCount: int) -> Vector64_1[int]:...
        # Method ShiftRightArithmetic(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightArithmetic(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightArithmetic(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightArithmetic(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method

    # Skipped ShiftRightLogical due to it being static, abstract and generic.

    ShiftRightLogical : ShiftRightLogical_MethodGroup
    class ShiftRightLogical_MethodGroup:
        @typing.overload
        def __call__(self, vector: Vector64_1[int], shiftCount: int) -> Vector64_1[int]:...
        # Method ShiftRightLogical(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        # Method ShiftRightLogical(vector : Vector64`1, shiftCount : Int32) was skipped since it collides with above method
        @typing.overload
        def __call__(self, vector: Vector64_1[UIntPtr], shiftCount: int) -> Vector64_1[UIntPtr]:...

    # Skipped Shuffle due to it being static, abstract and generic.

    Shuffle : Shuffle_MethodGroup
    class Shuffle_MethodGroup:
        def __call__(self, vector: Vector64_1[float], indices: Vector64_1[int]) -> Vector64_1[float]:...
        # Method Shuffle(vector : Vector64`1, indices : Vector64`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector64`1, indices : Vector64`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector64`1, indices : Vector64`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector64`1, indices : Vector64`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector64`1, indices : Vector64`1) was skipped since it collides with above method
        # Method Shuffle(vector : Vector64`1, indices : Vector64`1) was skipped since it collides with above method

    # Skipped ShuffleNative due to it being static, abstract and generic.

    ShuffleNative : ShuffleNative_MethodGroup
    class ShuffleNative_MethodGroup:
        def __call__(self, vector: Vector64_1[float], indices: Vector64_1[int]) -> Vector64_1[float]:...
        # Method ShuffleNative(vector : Vector64`1, indices : Vector64`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector64`1, indices : Vector64`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector64`1, indices : Vector64`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector64`1, indices : Vector64`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector64`1, indices : Vector64`1) was skipped since it collides with above method
        # Method ShuffleNative(vector : Vector64`1, indices : Vector64`1) was skipped since it collides with above method

    # Skipped Sin due to it being static, abstract and generic.

    Sin : Sin_MethodGroup
    class Sin_MethodGroup:
        def __call__(self, vector: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Sin(vector : Vector64`1) was skipped since it collides with above method

    # Skipped SinCos due to it being static, abstract and generic.

    SinCos : SinCos_MethodGroup
    class SinCos_MethodGroup:
        def __call__(self, vector: Vector64_1[float]) -> ValueTuple_2[Vector64_1[float], Vector64_1[float]]:...
        # Method SinCos(vector : Vector64`1) was skipped since it collides with above method

    # Skipped Sqrt due to it being static, abstract and generic.

    Sqrt : Sqrt_MethodGroup
    class Sqrt_MethodGroup:
        def __getitem__(self, t:typing.Type[Sqrt_1_T1]) -> Sqrt_1[Sqrt_1_T1]: ...

        Sqrt_1_T1 = typing.TypeVar('Sqrt_1_T1')
        class Sqrt_1(typing.Generic[Sqrt_1_T1]):
            Sqrt_1_T = Vector64_0.Sqrt_MethodGroup.Sqrt_1_T1
            def __call__(self, vector: Vector64_1[Sqrt_1_T]) -> Vector64_1[Sqrt_1_T]:...


    # Skipped Store due to it being static, abstract and generic.

    Store : Store_MethodGroup
    class Store_MethodGroup:
        def __getitem__(self, t:typing.Type[Store_1_T1]) -> Store_1[Store_1_T1]: ...

        Store_1_T1 = typing.TypeVar('Store_1_T1')
        class Store_1(typing.Generic[Store_1_T1]):
            Store_1_T = Vector64_0.Store_MethodGroup.Store_1_T1
            def __call__(self, source: Vector64_1[Store_1_T], destination: clr.Reference[Store_1_T]) -> None:...


    # Skipped StoreAligned due to it being static, abstract and generic.

    StoreAligned : StoreAligned_MethodGroup
    class StoreAligned_MethodGroup:
        def __getitem__(self, t:typing.Type[StoreAligned_1_T1]) -> StoreAligned_1[StoreAligned_1_T1]: ...

        StoreAligned_1_T1 = typing.TypeVar('StoreAligned_1_T1')
        class StoreAligned_1(typing.Generic[StoreAligned_1_T1]):
            StoreAligned_1_T = Vector64_0.StoreAligned_MethodGroup.StoreAligned_1_T1
            def __call__(self, source: Vector64_1[StoreAligned_1_T], destination: clr.Reference[StoreAligned_1_T]) -> None:...


    # Skipped StoreAlignedNonTemporal due to it being static, abstract and generic.

    StoreAlignedNonTemporal : StoreAlignedNonTemporal_MethodGroup
    class StoreAlignedNonTemporal_MethodGroup:
        def __getitem__(self, t:typing.Type[StoreAlignedNonTemporal_1_T1]) -> StoreAlignedNonTemporal_1[StoreAlignedNonTemporal_1_T1]: ...

        StoreAlignedNonTemporal_1_T1 = typing.TypeVar('StoreAlignedNonTemporal_1_T1')
        class StoreAlignedNonTemporal_1(typing.Generic[StoreAlignedNonTemporal_1_T1]):
            StoreAlignedNonTemporal_1_T = Vector64_0.StoreAlignedNonTemporal_MethodGroup.StoreAlignedNonTemporal_1_T1
            def __call__(self, source: Vector64_1[StoreAlignedNonTemporal_1_T], destination: clr.Reference[StoreAlignedNonTemporal_1_T]) -> None:...


    # Skipped StoreUnsafe due to it being static, abstract and generic.

    StoreUnsafe : StoreUnsafe_MethodGroup
    class StoreUnsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[StoreUnsafe_1_T1]) -> StoreUnsafe_1[StoreUnsafe_1_T1]: ...

        StoreUnsafe_1_T1 = typing.TypeVar('StoreUnsafe_1_T1')
        class StoreUnsafe_1(typing.Generic[StoreUnsafe_1_T1]):
            StoreUnsafe_1_T = Vector64_0.StoreUnsafe_MethodGroup.StoreUnsafe_1_T1
            @typing.overload
            def __call__(self, source: Vector64_1[StoreUnsafe_1_T], destination: clr.Reference[StoreUnsafe_1_T]) -> None:...
            @typing.overload
            def __call__(self, source: Vector64_1[StoreUnsafe_1_T], destination: clr.Reference[StoreUnsafe_1_T], elementOffset: UIntPtr) -> None:...


    # Skipped Subtract due to it being static, abstract and generic.

    Subtract : Subtract_MethodGroup
    class Subtract_MethodGroup:
        def __getitem__(self, t:typing.Type[Subtract_1_T1]) -> Subtract_1[Subtract_1_T1]: ...

        Subtract_1_T1 = typing.TypeVar('Subtract_1_T1')
        class Subtract_1(typing.Generic[Subtract_1_T1]):
            Subtract_1_T = Vector64_0.Subtract_MethodGroup.Subtract_1_T1
            def __call__(self, left: Vector64_1[Subtract_1_T], right: Vector64_1[Subtract_1_T]) -> Vector64_1[Subtract_1_T]:...


    # Skipped SubtractSaturate due to it being static, abstract and generic.

    SubtractSaturate : SubtractSaturate_MethodGroup
    class SubtractSaturate_MethodGroup:
        def __getitem__(self, t:typing.Type[SubtractSaturate_1_T1]) -> SubtractSaturate_1[SubtractSaturate_1_T1]: ...

        SubtractSaturate_1_T1 = typing.TypeVar('SubtractSaturate_1_T1')
        class SubtractSaturate_1(typing.Generic[SubtractSaturate_1_T1]):
            SubtractSaturate_1_T = Vector64_0.SubtractSaturate_MethodGroup.SubtractSaturate_1_T1
            def __call__(self, left: Vector64_1[SubtractSaturate_1_T], right: Vector64_1[SubtractSaturate_1_T]) -> Vector64_1[SubtractSaturate_1_T]:...


    # Skipped Sum due to it being static, abstract and generic.

    Sum : Sum_MethodGroup
    class Sum_MethodGroup:
        def __getitem__(self, t:typing.Type[Sum_1_T1]) -> Sum_1[Sum_1_T1]: ...

        Sum_1_T1 = typing.TypeVar('Sum_1_T1')
        class Sum_1(typing.Generic[Sum_1_T1]):
            Sum_1_T = Vector64_0.Sum_MethodGroup.Sum_1_T1
            def __call__(self, vector: Vector64_1[Sum_1_T]) -> Sum_1_T:...


    # Skipped ToScalar due to it being static, abstract and generic.

    ToScalar : ToScalar_MethodGroup
    class ToScalar_MethodGroup:
        def __getitem__(self, t:typing.Type[ToScalar_1_T1]) -> ToScalar_1[ToScalar_1_T1]: ...

        ToScalar_1_T1 = typing.TypeVar('ToScalar_1_T1')
        class ToScalar_1(typing.Generic[ToScalar_1_T1]):
            ToScalar_1_T = Vector64_0.ToScalar_MethodGroup.ToScalar_1_T1
            def __call__(self, vector: Vector64_1[ToScalar_1_T]) -> ToScalar_1_T:...


    # Skipped ToVector128 due to it being static, abstract and generic.

    ToVector128 : ToVector128_MethodGroup
    class ToVector128_MethodGroup:
        def __getitem__(self, t:typing.Type[ToVector128_1_T1]) -> ToVector128_1[ToVector128_1_T1]: ...

        ToVector128_1_T1 = typing.TypeVar('ToVector128_1_T1')
        class ToVector128_1(typing.Generic[ToVector128_1_T1]):
            ToVector128_1_T = Vector64_0.ToVector128_MethodGroup.ToVector128_1_T1
            def __call__(self, vector: Vector64_1[ToVector128_1_T]) -> Vector128_1[ToVector128_1_T]:...


    # Skipped ToVector128Unsafe due to it being static, abstract and generic.

    ToVector128Unsafe : ToVector128Unsafe_MethodGroup
    class ToVector128Unsafe_MethodGroup:
        def __getitem__(self, t:typing.Type[ToVector128Unsafe_1_T1]) -> ToVector128Unsafe_1[ToVector128Unsafe_1_T1]: ...

        ToVector128Unsafe_1_T1 = typing.TypeVar('ToVector128Unsafe_1_T1')
        class ToVector128Unsafe_1(typing.Generic[ToVector128Unsafe_1_T1]):
            ToVector128Unsafe_1_T = Vector64_0.ToVector128Unsafe_MethodGroup.ToVector128Unsafe_1_T1
            def __call__(self, vector: Vector64_1[ToVector128Unsafe_1_T]) -> Vector128_1[ToVector128Unsafe_1_T]:...


    # Skipped Truncate due to it being static, abstract and generic.

    Truncate : Truncate_MethodGroup
    class Truncate_MethodGroup:
        def __call__(self, vector: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Truncate(vector : Vector64`1) was skipped since it collides with above method

    # Skipped TryCopyTo due to it being static, abstract and generic.

    TryCopyTo : TryCopyTo_MethodGroup
    class TryCopyTo_MethodGroup:
        def __getitem__(self, t:typing.Type[TryCopyTo_1_T1]) -> TryCopyTo_1[TryCopyTo_1_T1]: ...

        TryCopyTo_1_T1 = typing.TypeVar('TryCopyTo_1_T1')
        class TryCopyTo_1(typing.Generic[TryCopyTo_1_T1]):
            TryCopyTo_1_T = Vector64_0.TryCopyTo_MethodGroup.TryCopyTo_1_T1
            def __call__(self, vector: Vector64_1[TryCopyTo_1_T], destination: Span_1[TryCopyTo_1_T]) -> bool:...


    # Skipped Widen due to it being static, abstract and generic.

    Widen : Widen_MethodGroup
    class Widen_MethodGroup:
        def __call__(self, source: Vector64_1[float]) -> ValueTuple_2[Vector64_1[float], Vector64_1[float]]:...
        # Method Widen(source : Vector64`1) was skipped since it collides with above method
        # Method Widen(source : Vector64`1) was skipped since it collides with above method
        # Method Widen(source : Vector64`1) was skipped since it collides with above method
        # Method Widen(source : Vector64`1) was skipped since it collides with above method
        # Method Widen(source : Vector64`1) was skipped since it collides with above method
        # Method Widen(source : Vector64`1) was skipped since it collides with above method

    # Skipped WidenLower due to it being static, abstract and generic.

    WidenLower : WidenLower_MethodGroup
    class WidenLower_MethodGroup:
        def __call__(self, source: Vector64_1[float]) -> Vector64_1[float]:...
        # Method WidenLower(source : Vector64`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector64`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector64`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector64`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector64`1) was skipped since it collides with above method
        # Method WidenLower(source : Vector64`1) was skipped since it collides with above method

    # Skipped WidenUpper due to it being static, abstract and generic.

    WidenUpper : WidenUpper_MethodGroup
    class WidenUpper_MethodGroup:
        def __call__(self, source: Vector64_1[float]) -> Vector64_1[float]:...
        # Method WidenUpper(source : Vector64`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector64`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector64`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector64`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector64`1) was skipped since it collides with above method
        # Method WidenUpper(source : Vector64`1) was skipped since it collides with above method

    # Skipped WithElement due to it being static, abstract and generic.

    WithElement : WithElement_MethodGroup
    class WithElement_MethodGroup:
        def __getitem__(self, t:typing.Type[WithElement_1_T1]) -> WithElement_1[WithElement_1_T1]: ...

        WithElement_1_T1 = typing.TypeVar('WithElement_1_T1')
        class WithElement_1(typing.Generic[WithElement_1_T1]):
            WithElement_1_T = Vector64_0.WithElement_MethodGroup.WithElement_1_T1
            def __call__(self, vector: Vector64_1[WithElement_1_T], index: int, value: WithElement_1_T) -> Vector64_1[WithElement_1_T]:...


    # Skipped Xor due to it being static, abstract and generic.

    Xor : Xor_MethodGroup
    class Xor_MethodGroup:
        def __getitem__(self, t:typing.Type[Xor_1_T1]) -> Xor_1[Xor_1_T1]: ...

        Xor_1_T1 = typing.TypeVar('Xor_1_T1')
        class Xor_1(typing.Generic[Xor_1_T1]):
            Xor_1_T = Vector64_0.Xor_MethodGroup.Xor_1_T1
            def __call__(self, left: Vector64_1[Xor_1_T], right: Vector64_1[Xor_1_T]) -> Vector64_1[Xor_1_T]:...




Vector64_1_T = typing.TypeVar('Vector64_1_T')
class Vector64_1(typing.Generic[Vector64_1_T]):
    @classmethod
    @property
    def AllBitsSet(cls) -> Vector64_1[Vector64_1_T]: ...
    @classmethod
    @property
    def Count(cls) -> int: ...
    @classmethod
    @property
    def Indices(cls) -> Vector64_1[Vector64_1_T]: ...
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @property
    def Item(self) -> Vector64_1_T: ...
    @classmethod
    @property
    def One(cls) -> Vector64_1[Vector64_1_T]: ...
    @classmethod
    @property
    def Zero(cls) -> Vector64_1[Vector64_1_T]: ...
    def GetHashCode(self) -> int: ...
    def __add__(self, left: Vector64_1[Vector64_1_T], right: Vector64_1[Vector64_1_T]) -> Vector64_1[Vector64_1_T]: ...
    def __and__(self, left: Vector64_1[Vector64_1_T], right: Vector64_1[Vector64_1_T]) -> Vector64_1[Vector64_1_T]: ...
    def __or__(self, left: Vector64_1[Vector64_1_T], right: Vector64_1[Vector64_1_T]) -> Vector64_1[Vector64_1_T]: ...
    @typing.overload
    def __truediv__(self, left: Vector64_1[Vector64_1_T], right: Vector64_1[Vector64_1_T]) -> Vector64_1[Vector64_1_T]: ...
    @typing.overload
    def __truediv__(self, left: Vector64_1[Vector64_1_T], right: Vector64_1_T) -> Vector64_1[Vector64_1_T]: ...
    def __eq__(self, left: Vector64_1[Vector64_1_T], right: Vector64_1[Vector64_1_T]) -> bool: ...
    def __xor__(self, left: Vector64_1[Vector64_1_T], right: Vector64_1[Vector64_1_T]) -> Vector64_1[Vector64_1_T]: ...
    def __ne__(self, left: Vector64_1[Vector64_1_T], right: Vector64_1[Vector64_1_T]) -> bool: ...
    def __lshift__(self, value: Vector64_1[Vector64_1_T], shiftCount: int) -> Vector64_1[Vector64_1_T]: ...
    @typing.overload
    def __mul__(self, left: Vector64_1[Vector64_1_T], right: Vector64_1[Vector64_1_T]) -> Vector64_1[Vector64_1_T]: ...
    @typing.overload
    def __mul__(self, left: Vector64_1[Vector64_1_T], right: Vector64_1_T) -> Vector64_1[Vector64_1_T]: ...
    @typing.overload
    def __mul__(self, left: Vector64_1_T, right: Vector64_1[Vector64_1_T]) -> Vector64_1[Vector64_1_T]: ...
    def __invert__(self, vector: Vector64_1[Vector64_1_T]) -> Vector64_1[Vector64_1_T]: ...
    def __rshift__(self, value: Vector64_1[Vector64_1_T], shiftCount: int) -> Vector64_1[Vector64_1_T]: ...
    def __sub__(self, left: Vector64_1[Vector64_1_T], right: Vector64_1[Vector64_1_T]) -> Vector64_1[Vector64_1_T]: ...
    def __neg__(self, vector: Vector64_1[Vector64_1_T]) -> Vector64_1[Vector64_1_T]: ...
    def __pos__(self, value: Vector64_1[Vector64_1_T]) -> Vector64_1[Vector64_1_T]: ...
    # Operator not supported op_UnsignedRightShift(value: Vector64`1, shiftCount: Int32)
    def ToString(self) -> str: ...
    # Skipped Equals due to it being static, abstract and generic.

    Equals : Equals_MethodGroup[Vector64_1_T]
    Equals_MethodGroup_Vector64_1_T = typing.TypeVar('Equals_MethodGroup_Vector64_1_T')
    class Equals_MethodGroup(typing.Generic[Equals_MethodGroup_Vector64_1_T]):
        Equals_MethodGroup_Vector64_1_T = Vector64_1.Equals_MethodGroup_Vector64_1_T
        @typing.overload
        def __call__(self, other: Vector64_1[Equals_MethodGroup_Vector64_1_T]) -> bool:...
        @typing.overload
        def __call__(self, obj: typing.Any) -> bool:...


