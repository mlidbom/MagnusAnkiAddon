import typing, clr, abc
from System.Runtime.Intrinsics import Vector64_1, Vector128_1
from System import ValueTuple_2, ValueTuple_3, ValueTuple_4
from System.Numerics import Vector_1

class AdvSimd(ArmBase):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def ConvertToInt32RoundAwayFromZeroScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToInt32RoundToEvenScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToInt32RoundToNegativeInfinityScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToInt32RoundToPositiveInfinityScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToInt32RoundToZeroScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToUInt32RoundAwayFromZeroScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToUInt32RoundToEvenScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToUInt32RoundToNegativeInfinityScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToUInt32RoundToPositiveInfinityScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ConvertToUInt32RoundToZeroScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
    @staticmethod
    def ShiftArithmeticRoundedSaturateScalar(value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]: ...
    @staticmethod
    def ShiftArithmeticRoundedScalar(value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]: ...
    @staticmethod
    def ShiftArithmeticSaturateScalar(value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]: ...
    @staticmethod
    def ShiftArithmeticScalar(value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]: ...
    @staticmethod
    def ShiftLeftLogicalSaturateUnsignedScalar(value: Vector64_1[int], count: int) -> Vector64_1[int]: ...
    @staticmethod
    def ShiftRightArithmeticAddScalar(addend: Vector64_1[int], value: Vector64_1[int], count: int) -> Vector64_1[int]: ...
    @staticmethod
    def ShiftRightArithmeticRoundedAddScalar(addend: Vector64_1[int], value: Vector64_1[int], count: int) -> Vector64_1[int]: ...
    @staticmethod
    def ShiftRightArithmeticRoundedScalar(value: Vector64_1[int], count: int) -> Vector64_1[int]: ...
    @staticmethod
    def ShiftRightArithmeticScalar(value: Vector64_1[int], count: int) -> Vector64_1[int]: ...
    # Skipped Abs due to it being static, abstract and generic.

    Abs : Abs_MethodGroup
    class Abs_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Abs(value : Vector64`1) was skipped since it collides with above method
        # Method Abs(value : Vector64`1) was skipped since it collides with above method
        # Method Abs(value : Vector64`1) was skipped since it collides with above method
        # Method Abs(value : Vector128`1) was skipped since it collides with above method
        # Method Abs(value : Vector128`1) was skipped since it collides with above method
        # Method Abs(value : Vector128`1) was skipped since it collides with above method

    # Skipped AbsoluteCompareGreaterThan due to it being static, abstract and generic.

    AbsoluteCompareGreaterThan : AbsoluteCompareGreaterThan_MethodGroup
    class AbsoluteCompareGreaterThan_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped AbsoluteCompareGreaterThanOrEqual due to it being static, abstract and generic.

    AbsoluteCompareGreaterThanOrEqual : AbsoluteCompareGreaterThanOrEqual_MethodGroup
    class AbsoluteCompareGreaterThanOrEqual_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped AbsoluteCompareLessThan due to it being static, abstract and generic.

    AbsoluteCompareLessThan : AbsoluteCompareLessThan_MethodGroup
    class AbsoluteCompareLessThan_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped AbsoluteCompareLessThanOrEqual due to it being static, abstract and generic.

    AbsoluteCompareLessThanOrEqual : AbsoluteCompareLessThanOrEqual_MethodGroup
    class AbsoluteCompareLessThanOrEqual_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped AbsoluteDifference due to it being static, abstract and generic.

    AbsoluteDifference : AbsoluteDifference_MethodGroup
    class AbsoluteDifference_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method AbsoluteDifference(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped AbsoluteDifferenceAdd due to it being static, abstract and generic.

    AbsoluteDifferenceAdd : AbsoluteDifferenceAdd_MethodGroup
    class AbsoluteDifferenceAdd_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method AbsoluteDifferenceAdd(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceAdd(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceAdd(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceAdd(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceAdd(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method AbsoluteDifferenceAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped AbsoluteDifferenceWideningLower due to it being static, abstract and generic.

    AbsoluteDifferenceWideningLower : AbsoluteDifferenceWideningLower_MethodGroup
    class AbsoluteDifferenceWideningLower_MethodGroup:
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method AbsoluteDifferenceWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped AbsoluteDifferenceWideningLowerAndAdd due to it being static, abstract and generic.

    AbsoluteDifferenceWideningLowerAndAdd : AbsoluteDifferenceWideningLowerAndAdd_MethodGroup
    class AbsoluteDifferenceWideningLowerAndAdd_MethodGroup:
        def __call__(self, addend: Vector128_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method AbsoluteDifferenceWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped AbsoluteDifferenceWideningUpper due to it being static, abstract and generic.

    AbsoluteDifferenceWideningUpper : AbsoluteDifferenceWideningUpper_MethodGroup
    class AbsoluteDifferenceWideningUpper_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method AbsoluteDifferenceWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped AbsoluteDifferenceWideningUpperAndAdd due to it being static, abstract and generic.

    AbsoluteDifferenceWideningUpperAndAdd : AbsoluteDifferenceWideningUpperAndAdd_MethodGroup
    class AbsoluteDifferenceWideningUpperAndAdd_MethodGroup:
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method AbsoluteDifferenceWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped AbsSaturate due to it being static, abstract and generic.

    AbsSaturate : AbsSaturate_MethodGroup
    class AbsSaturate_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
        # Method AbsSaturate(value : Vector64`1) was skipped since it collides with above method
        # Method AbsSaturate(value : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method AbsSaturate(value : Vector128`1) was skipped since it collides with above method
        # Method AbsSaturate(value : Vector128`1) was skipped since it collides with above method

    # Skipped AbsScalar due to it being static, abstract and generic.

    AbsScalar : AbsScalar_MethodGroup
    class AbsScalar_MethodGroup:
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        # Method AbsScalar(value : Vector64`1) was skipped since it collides with above method

    # Skipped Add due to it being static, abstract and generic.

    Add : Add_MethodGroup
    class Add_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Add(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Add(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Add(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Add(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Add(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Add(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Add(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped AddHighNarrowingLower due to it being static, abstract and generic.

    AddHighNarrowingLower : AddHighNarrowingLower_MethodGroup
    class AddHighNarrowingLower_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector64_1[int]:...
        # Method AddHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped AddHighNarrowingUpper due to it being static, abstract and generic.

    AddHighNarrowingUpper : AddHighNarrowingUpper_MethodGroup
    class AddHighNarrowingUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method AddHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped AddPairwise due to it being static, abstract and generic.

    AddPairwise : AddPairwise_MethodGroup
    class AddPairwise_MethodGroup:
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method AddPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped AddPairwiseWidening due to it being static, abstract and generic.

    AddPairwiseWidening : AddPairwiseWidening_MethodGroup
    class AddPairwiseWidening_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
        # Method AddPairwiseWidening(value : Vector64`1) was skipped since it collides with above method
        # Method AddPairwiseWidening(value : Vector64`1) was skipped since it collides with above method
        # Method AddPairwiseWidening(value : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method AddPairwiseWidening(value : Vector128`1) was skipped since it collides with above method
        # Method AddPairwiseWidening(value : Vector128`1) was skipped since it collides with above method
        # Method AddPairwiseWidening(value : Vector128`1) was skipped since it collides with above method
        # Method AddPairwiseWidening(value : Vector128`1) was skipped since it collides with above method
        # Method AddPairwiseWidening(value : Vector128`1) was skipped since it collides with above method

    # Skipped AddPairwiseWideningAndAdd due to it being static, abstract and generic.

    AddPairwiseWideningAndAdd : AddPairwiseWideningAndAdd_MethodGroup
    class AddPairwiseWideningAndAdd_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector64_1[int], value: Vector64_1[int]) -> Vector64_1[int]:...
        # Method AddPairwiseWideningAndAdd(addend : Vector64`1, value : Vector64`1) was skipped since it collides with above method
        # Method AddPairwiseWideningAndAdd(addend : Vector64`1, value : Vector64`1) was skipped since it collides with above method
        # Method AddPairwiseWideningAndAdd(addend : Vector64`1, value : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector128_1[int], value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method AddPairwiseWideningAndAdd(addend : Vector128`1, value : Vector128`1) was skipped since it collides with above method
        # Method AddPairwiseWideningAndAdd(addend : Vector128`1, value : Vector128`1) was skipped since it collides with above method
        # Method AddPairwiseWideningAndAdd(addend : Vector128`1, value : Vector128`1) was skipped since it collides with above method
        # Method AddPairwiseWideningAndAdd(addend : Vector128`1, value : Vector128`1) was skipped since it collides with above method
        # Method AddPairwiseWideningAndAdd(addend : Vector128`1, value : Vector128`1) was skipped since it collides with above method

    # Skipped AddPairwiseWideningAndAddScalar due to it being static, abstract and generic.

    AddPairwiseWideningAndAddScalar : AddPairwiseWideningAndAddScalar_MethodGroup
    class AddPairwiseWideningAndAddScalar_MethodGroup:
        def __call__(self, addend: Vector64_1[int], value: Vector64_1[int]) -> Vector64_1[int]:...
        # Method AddPairwiseWideningAndAddScalar(addend : Vector64`1, value : Vector64`1) was skipped since it collides with above method

    # Skipped AddPairwiseWideningScalar due to it being static, abstract and generic.

    AddPairwiseWideningScalar : AddPairwiseWideningScalar_MethodGroup
    class AddPairwiseWideningScalar_MethodGroup:
        def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
        # Method AddPairwiseWideningScalar(value : Vector64`1) was skipped since it collides with above method

    # Skipped AddRoundedHighNarrowingLower due to it being static, abstract and generic.

    AddRoundedHighNarrowingLower : AddRoundedHighNarrowingLower_MethodGroup
    class AddRoundedHighNarrowingLower_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector64_1[int]:...
        # Method AddRoundedHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped AddRoundedHighNarrowingUpper due to it being static, abstract and generic.

    AddRoundedHighNarrowingUpper : AddRoundedHighNarrowingUpper_MethodGroup
    class AddRoundedHighNarrowingUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method AddRoundedHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped AddSaturate due to it being static, abstract and generic.

    AddSaturate : AddSaturate_MethodGroup
    class AddSaturate_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method AddSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped AddSaturateScalar due to it being static, abstract and generic.

    AddSaturateScalar : AddSaturateScalar_MethodGroup
    class AddSaturateScalar_MethodGroup:
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method AddSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped AddScalar due to it being static, abstract and generic.

    AddScalar : AddScalar_MethodGroup
    class AddScalar_MethodGroup:
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method AddScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped AddWideningLower due to it being static, abstract and generic.

    AddWideningLower : AddWideningLower_MethodGroup
    class AddWideningLower_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method AddWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method AddWideningLower(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddWideningLower(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddWideningLower(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddWideningLower(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method AddWideningLower(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped AddWideningUpper due to it being static, abstract and generic.

    AddWideningUpper : AddWideningUpper_MethodGroup
    class AddWideningUpper_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method AddWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method AddWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped And due to it being static, abstract and generic.

    And : And_MethodGroup
    class And_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method And(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method And(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method And(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method And(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method And(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method And(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method And(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method And(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method And(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped BitwiseClear due to it being static, abstract and generic.

    BitwiseClear : BitwiseClear_MethodGroup
    class BitwiseClear_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float], mask: Vector64_1[float]) -> Vector64_1[float]:...
        # Method BitwiseClear(value : Vector64`1, mask : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[float], mask: Vector128_1[float]) -> Vector128_1[float]:...
        # Method BitwiseClear(value : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector64`1, mask : Vector64`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector64`1, mask : Vector64`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector64`1, mask : Vector64`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector64`1, mask : Vector64`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector64`1, mask : Vector64`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector64`1, mask : Vector64`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector64`1, mask : Vector64`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector64`1, mask : Vector64`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector128`1, mask : Vector128`1) was skipped since it collides with above method
        # Method BitwiseClear(value : Vector128`1, mask : Vector128`1) was skipped since it collides with above method

    # Skipped BitwiseSelect due to it being static, abstract and generic.

    BitwiseSelect : BitwiseSelect_MethodGroup
    class BitwiseSelect_MethodGroup:
        @typing.overload
        def __call__(self, select: Vector64_1[float], left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method BitwiseSelect(select : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, select: Vector128_1[float], left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method BitwiseSelect(select : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped Ceiling due to it being static, abstract and generic.

    Ceiling : Ceiling_MethodGroup
    class Ceiling_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped CeilingScalar due to it being static, abstract and generic.

    CeilingScalar : CeilingScalar_MethodGroup
    class CeilingScalar_MethodGroup:
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        # Method CeilingScalar(value : Vector64`1) was skipped since it collides with above method

    # Skipped CompareEqual due to it being static, abstract and generic.

    CompareEqual : CompareEqual_MethodGroup
    class CompareEqual_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method CompareEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped CompareGreaterThan due to it being static, abstract and generic.

    CompareGreaterThan : CompareGreaterThan_MethodGroup
    class CompareGreaterThan_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method CompareGreaterThan(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped CompareGreaterThanOrEqual due to it being static, abstract and generic.

    CompareGreaterThanOrEqual : CompareGreaterThanOrEqual_MethodGroup
    class CompareGreaterThanOrEqual_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method CompareGreaterThanOrEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped CompareLessThan due to it being static, abstract and generic.

    CompareLessThan : CompareLessThan_MethodGroup
    class CompareLessThan_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method CompareLessThan(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped CompareLessThanOrEqual due to it being static, abstract and generic.

    CompareLessThanOrEqual : CompareLessThanOrEqual_MethodGroup
    class CompareLessThanOrEqual_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method CompareLessThanOrEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped CompareTest due to it being static, abstract and generic.

    CompareTest : CompareTest_MethodGroup
    class CompareTest_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method CompareTest(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareTest(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareTest(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareTest(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareTest(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareTest(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method CompareTest(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareTest(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareTest(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareTest(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareTest(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method CompareTest(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped ConvertToInt32RoundAwayFromZero due to it being static, abstract and generic.

    ConvertToInt32RoundAwayFromZero : ConvertToInt32RoundAwayFromZero_MethodGroup
    class ConvertToInt32RoundAwayFromZero_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[int]:...

    # Skipped ConvertToInt32RoundToEven due to it being static, abstract and generic.

    ConvertToInt32RoundToEven : ConvertToInt32RoundToEven_MethodGroup
    class ConvertToInt32RoundToEven_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[int]:...

    # Skipped ConvertToInt32RoundToNegativeInfinity due to it being static, abstract and generic.

    ConvertToInt32RoundToNegativeInfinity : ConvertToInt32RoundToNegativeInfinity_MethodGroup
    class ConvertToInt32RoundToNegativeInfinity_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[int]:...

    # Skipped ConvertToInt32RoundToPositiveInfinity due to it being static, abstract and generic.

    ConvertToInt32RoundToPositiveInfinity : ConvertToInt32RoundToPositiveInfinity_MethodGroup
    class ConvertToInt32RoundToPositiveInfinity_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[int]:...

    # Skipped ConvertToInt32RoundToZero due to it being static, abstract and generic.

    ConvertToInt32RoundToZero : ConvertToInt32RoundToZero_MethodGroup
    class ConvertToInt32RoundToZero_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[int]:...

    # Skipped ConvertToSingle due to it being static, abstract and generic.

    ConvertToSingle : ConvertToSingle_MethodGroup
    class ConvertToSingle_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int]) -> Vector64_1[float]:...
        # Method ConvertToSingle(value : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[float]:...
        # Method ConvertToSingle(value : Vector128`1) was skipped since it collides with above method

    # Skipped ConvertToSingleScalar due to it being static, abstract and generic.

    ConvertToSingleScalar : ConvertToSingleScalar_MethodGroup
    class ConvertToSingleScalar_MethodGroup:
        def __call__(self, value: Vector64_1[int]) -> Vector64_1[float]:...
        # Method ConvertToSingleScalar(value : Vector64`1) was skipped since it collides with above method

    # Skipped ConvertToUInt32RoundAwayFromZero due to it being static, abstract and generic.

    ConvertToUInt32RoundAwayFromZero : ConvertToUInt32RoundAwayFromZero_MethodGroup
    class ConvertToUInt32RoundAwayFromZero_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[int]:...

    # Skipped ConvertToUInt32RoundToEven due to it being static, abstract and generic.

    ConvertToUInt32RoundToEven : ConvertToUInt32RoundToEven_MethodGroup
    class ConvertToUInt32RoundToEven_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[int]:...

    # Skipped ConvertToUInt32RoundToNegativeInfinity due to it being static, abstract and generic.

    ConvertToUInt32RoundToNegativeInfinity : ConvertToUInt32RoundToNegativeInfinity_MethodGroup
    class ConvertToUInt32RoundToNegativeInfinity_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[int]:...

    # Skipped ConvertToUInt32RoundToPositiveInfinity due to it being static, abstract and generic.

    ConvertToUInt32RoundToPositiveInfinity : ConvertToUInt32RoundToPositiveInfinity_MethodGroup
    class ConvertToUInt32RoundToPositiveInfinity_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[int]:...

    # Skipped ConvertToUInt32RoundToZero due to it being static, abstract and generic.

    ConvertToUInt32RoundToZero : ConvertToUInt32RoundToZero_MethodGroup
    class ConvertToUInt32RoundToZero_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[int]:...

    # Skipped DivideScalar due to it being static, abstract and generic.

    DivideScalar : DivideScalar_MethodGroup
    class DivideScalar_MethodGroup:
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method DivideScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped DuplicateSelectedScalarToVector128 due to it being static, abstract and generic.

    DuplicateSelectedScalarToVector128 : DuplicateSelectedScalarToVector128_MethodGroup
    class DuplicateSelectedScalarToVector128_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float], index: int) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float], index: int) -> Vector128_1[float]:...
        # Method DuplicateSelectedScalarToVector128(value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector128(value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector128(value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector128(value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector128(value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector128(value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector128(value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector128(value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector128(value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector128(value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector128(value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector128(value : Vector128`1, index : Byte) was skipped since it collides with above method

    # Skipped DuplicateSelectedScalarToVector64 due to it being static, abstract and generic.

    DuplicateSelectedScalarToVector64 : DuplicateSelectedScalarToVector64_MethodGroup
    class DuplicateSelectedScalarToVector64_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float], index: int) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float], index: int) -> Vector64_1[float]:...
        # Method DuplicateSelectedScalarToVector64(value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector64(value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector64(value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector64(value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector64(value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector64(value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector64(value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector64(value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector64(value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector64(value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector64(value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector64(value : Vector128`1, index : Byte) was skipped since it collides with above method

    # Skipped DuplicateToVector128 due to it being static, abstract and generic.

    DuplicateToVector128 : DuplicateToVector128_MethodGroup
    class DuplicateToVector128_MethodGroup:
        def __call__(self, value: float) -> Vector128_1[float]:...
        # Method DuplicateToVector128(value : Byte) was skipped since it collides with above method
        # Method DuplicateToVector128(value : Int16) was skipped since it collides with above method
        # Method DuplicateToVector128(value : Int32) was skipped since it collides with above method
        # Method DuplicateToVector128(value : SByte) was skipped since it collides with above method
        # Method DuplicateToVector128(value : UInt16) was skipped since it collides with above method
        # Method DuplicateToVector128(value : UInt32) was skipped since it collides with above method

    # Skipped DuplicateToVector64 due to it being static, abstract and generic.

    DuplicateToVector64 : DuplicateToVector64_MethodGroup
    class DuplicateToVector64_MethodGroup:
        def __call__(self, value: float) -> Vector64_1[float]:...
        # Method DuplicateToVector64(value : Byte) was skipped since it collides with above method
        # Method DuplicateToVector64(value : Int16) was skipped since it collides with above method
        # Method DuplicateToVector64(value : Int32) was skipped since it collides with above method
        # Method DuplicateToVector64(value : SByte) was skipped since it collides with above method
        # Method DuplicateToVector64(value : UInt16) was skipped since it collides with above method
        # Method DuplicateToVector64(value : UInt32) was skipped since it collides with above method

    # Skipped Extract due to it being static, abstract and generic.

    Extract : Extract_MethodGroup
    class Extract_MethodGroup:
        @typing.overload
        def __call__(self, vector: Vector64_1[float], index: int) -> float:...
        @typing.overload
        def __call__(self, vector: Vector128_1[float], index: int) -> float:...
        # Method Extract(vector : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method Extract(vector : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method Extract(vector : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method Extract(vector : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method Extract(vector : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method Extract(vector : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method Extract(vector : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method Extract(vector : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method Extract(vector : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method Extract(vector : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method Extract(vector : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method Extract(vector : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method Extract(vector : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method Extract(vector : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method Extract(vector : Vector128`1, index : Byte) was skipped since it collides with above method

    # Skipped ExtractNarrowingLower due to it being static, abstract and generic.

    ExtractNarrowingLower : ExtractNarrowingLower_MethodGroup
    class ExtractNarrowingLower_MethodGroup:
        def __call__(self, value: Vector128_1[int]) -> Vector64_1[int]:...
        # Method ExtractNarrowingLower(value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingLower(value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingLower(value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingLower(value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingLower(value : Vector128`1) was skipped since it collides with above method

    # Skipped ExtractNarrowingSaturateLower due to it being static, abstract and generic.

    ExtractNarrowingSaturateLower : ExtractNarrowingSaturateLower_MethodGroup
    class ExtractNarrowingSaturateLower_MethodGroup:
        def __call__(self, value: Vector128_1[int]) -> Vector64_1[int]:...
        # Method ExtractNarrowingSaturateLower(value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingSaturateLower(value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingSaturateLower(value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingSaturateLower(value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingSaturateLower(value : Vector128`1) was skipped since it collides with above method

    # Skipped ExtractNarrowingSaturateUnsignedLower due to it being static, abstract and generic.

    ExtractNarrowingSaturateUnsignedLower : ExtractNarrowingSaturateUnsignedLower_MethodGroup
    class ExtractNarrowingSaturateUnsignedLower_MethodGroup:
        def __call__(self, value: Vector128_1[int]) -> Vector64_1[int]:...
        # Method ExtractNarrowingSaturateUnsignedLower(value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingSaturateUnsignedLower(value : Vector128`1) was skipped since it collides with above method

    # Skipped ExtractNarrowingSaturateUnsignedUpper due to it being static, abstract and generic.

    ExtractNarrowingSaturateUnsignedUpper : ExtractNarrowingSaturateUnsignedUpper_MethodGroup
    class ExtractNarrowingSaturateUnsignedUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ExtractNarrowingSaturateUnsignedUpper(lower : Vector64`1, value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingSaturateUnsignedUpper(lower : Vector64`1, value : Vector128`1) was skipped since it collides with above method

    # Skipped ExtractNarrowingSaturateUpper due to it being static, abstract and generic.

    ExtractNarrowingSaturateUpper : ExtractNarrowingSaturateUpper_MethodGroup
    class ExtractNarrowingSaturateUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ExtractNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1) was skipped since it collides with above method

    # Skipped ExtractNarrowingUpper due to it being static, abstract and generic.

    ExtractNarrowingUpper : ExtractNarrowingUpper_MethodGroup
    class ExtractNarrowingUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ExtractNarrowingUpper(lower : Vector64`1, value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingUpper(lower : Vector64`1, value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingUpper(lower : Vector64`1, value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingUpper(lower : Vector64`1, value : Vector128`1) was skipped since it collides with above method
        # Method ExtractNarrowingUpper(lower : Vector64`1, value : Vector128`1) was skipped since it collides with above method

    # Skipped ExtractVector128 due to it being static, abstract and generic.

    ExtractVector128 : ExtractVector128_MethodGroup
    class ExtractVector128_MethodGroup:
        def __call__(self, upper: Vector128_1[float], lower: Vector128_1[float], index: int) -> Vector128_1[float]:...
        # Method ExtractVector128(upper : Vector128`1, lower : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(upper : Vector128`1, lower : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(upper : Vector128`1, lower : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(upper : Vector128`1, lower : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(upper : Vector128`1, lower : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(upper : Vector128`1, lower : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(upper : Vector128`1, lower : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(upper : Vector128`1, lower : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector128(upper : Vector128`1, lower : Vector128`1, index : Byte) was skipped since it collides with above method

    # Skipped ExtractVector64 due to it being static, abstract and generic.

    ExtractVector64 : ExtractVector64_MethodGroup
    class ExtractVector64_MethodGroup:
        def __call__(self, upper: Vector64_1[float], lower: Vector64_1[float], index: int) -> Vector64_1[float]:...
        # Method ExtractVector64(upper : Vector64`1, lower : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector64(upper : Vector64`1, lower : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector64(upper : Vector64`1, lower : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector64(upper : Vector64`1, lower : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector64(upper : Vector64`1, lower : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector64(upper : Vector64`1, lower : Vector64`1, index : Byte) was skipped since it collides with above method

    # Skipped Floor due to it being static, abstract and generic.

    Floor : Floor_MethodGroup
    class Floor_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped FloorScalar due to it being static, abstract and generic.

    FloorScalar : FloorScalar_MethodGroup
    class FloorScalar_MethodGroup:
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        # Method FloorScalar(value : Vector64`1) was skipped since it collides with above method

    # Skipped FusedAddHalving due to it being static, abstract and generic.

    FusedAddHalving : FusedAddHalving_MethodGroup
    class FusedAddHalving_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method FusedAddHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method FusedAddHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method FusedAddHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method FusedAddHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method FusedAddHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method FusedAddHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method FusedAddHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method FusedAddHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method FusedAddHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method FusedAddHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped FusedAddRoundedHalving due to it being static, abstract and generic.

    FusedAddRoundedHalving : FusedAddRoundedHalving_MethodGroup
    class FusedAddRoundedHalving_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method FusedAddRoundedHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method FusedAddRoundedHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method FusedAddRoundedHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method FusedAddRoundedHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method FusedAddRoundedHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method FusedAddRoundedHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method FusedAddRoundedHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method FusedAddRoundedHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method FusedAddRoundedHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method FusedAddRoundedHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped FusedMultiplyAdd due to it being static, abstract and generic.

    FusedMultiplyAdd : FusedMultiplyAdd_MethodGroup
    class FusedMultiplyAdd_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector64_1[float], left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, addend: Vector128_1[float], left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped FusedMultiplyAddNegatedScalar due to it being static, abstract and generic.

    FusedMultiplyAddNegatedScalar : FusedMultiplyAddNegatedScalar_MethodGroup
    class FusedMultiplyAddNegatedScalar_MethodGroup:
        def __call__(self, addend: Vector64_1[float], left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method FusedMultiplyAddNegatedScalar(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped FusedMultiplyAddScalar due to it being static, abstract and generic.

    FusedMultiplyAddScalar : FusedMultiplyAddScalar_MethodGroup
    class FusedMultiplyAddScalar_MethodGroup:
        def __call__(self, addend: Vector64_1[float], left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method FusedMultiplyAddScalar(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped FusedMultiplySubtract due to it being static, abstract and generic.

    FusedMultiplySubtract : FusedMultiplySubtract_MethodGroup
    class FusedMultiplySubtract_MethodGroup:
        @typing.overload
        def __call__(self, minuend: Vector64_1[float], left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, minuend: Vector128_1[float], left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped FusedMultiplySubtractNegatedScalar due to it being static, abstract and generic.

    FusedMultiplySubtractNegatedScalar : FusedMultiplySubtractNegatedScalar_MethodGroup
    class FusedMultiplySubtractNegatedScalar_MethodGroup:
        def __call__(self, minuend: Vector64_1[float], left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method FusedMultiplySubtractNegatedScalar(minuend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped FusedMultiplySubtractScalar due to it being static, abstract and generic.

    FusedMultiplySubtractScalar : FusedMultiplySubtractScalar_MethodGroup
    class FusedMultiplySubtractScalar_MethodGroup:
        def __call__(self, minuend: Vector64_1[float], left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method FusedMultiplySubtractScalar(minuend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped FusedSubtractHalving due to it being static, abstract and generic.

    FusedSubtractHalving : FusedSubtractHalving_MethodGroup
    class FusedSubtractHalving_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method FusedSubtractHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method FusedSubtractHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method FusedSubtractHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method FusedSubtractHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method FusedSubtractHalving(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method FusedSubtractHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method FusedSubtractHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method FusedSubtractHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method FusedSubtractHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method FusedSubtractHalving(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped Insert due to it being static, abstract and generic.

    Insert : Insert_MethodGroup
    class Insert_MethodGroup:
        @typing.overload
        def __call__(self, vector: Vector64_1[float], index: int, data: float) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, vector: Vector128_1[float], index: int, data: float) -> Vector128_1[float]:...
        # Method Insert(vector : Vector128`1, index : Byte, data : Single) was skipped since it collides with above method
        # Method Insert(vector : Vector64`1, index : Byte, data : Byte) was skipped since it collides with above method
        # Method Insert(vector : Vector64`1, index : Byte, data : Int16) was skipped since it collides with above method
        # Method Insert(vector : Vector64`1, index : Byte, data : Int32) was skipped since it collides with above method
        # Method Insert(vector : Vector64`1, index : Byte, data : SByte) was skipped since it collides with above method
        # Method Insert(vector : Vector64`1, index : Byte, data : UInt16) was skipped since it collides with above method
        # Method Insert(vector : Vector64`1, index : Byte, data : UInt32) was skipped since it collides with above method
        # Method Insert(vector : Vector128`1, index : Byte, data : Byte) was skipped since it collides with above method
        # Method Insert(vector : Vector128`1, index : Byte, data : Int16) was skipped since it collides with above method
        # Method Insert(vector : Vector128`1, index : Byte, data : Int32) was skipped since it collides with above method
        # Method Insert(vector : Vector128`1, index : Byte, data : Int64) was skipped since it collides with above method
        # Method Insert(vector : Vector128`1, index : Byte, data : SByte) was skipped since it collides with above method
        # Method Insert(vector : Vector128`1, index : Byte, data : UInt16) was skipped since it collides with above method
        # Method Insert(vector : Vector128`1, index : Byte, data : UInt32) was skipped since it collides with above method
        # Method Insert(vector : Vector128`1, index : Byte, data : UInt64) was skipped since it collides with above method

    # Skipped InsertScalar due to it being static, abstract and generic.

    InsertScalar : InsertScalar_MethodGroup
    class InsertScalar_MethodGroup:
        def __call__(self, result: Vector128_1[float], resultIndex: int, value: Vector64_1[float]) -> Vector128_1[float]:...
        # Method InsertScalar(result : Vector128`1, resultIndex : Byte, value : Vector64`1) was skipped since it collides with above method
        # Method InsertScalar(result : Vector128`1, resultIndex : Byte, value : Vector64`1) was skipped since it collides with above method

    # Skipped LeadingSignCount due to it being static, abstract and generic.

    LeadingSignCount : LeadingSignCount_MethodGroup
    class LeadingSignCount_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
        # Method LeadingSignCount(value : Vector64`1) was skipped since it collides with above method
        # Method LeadingSignCount(value : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method LeadingSignCount(value : Vector128`1) was skipped since it collides with above method
        # Method LeadingSignCount(value : Vector128`1) was skipped since it collides with above method

    # Skipped LeadingZeroCount due to it being static, abstract and generic.

    LeadingZeroCount : LeadingZeroCount_MethodGroup
    class LeadingZeroCount_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
        # Method LeadingZeroCount(value : Vector64`1) was skipped since it collides with above method
        # Method LeadingZeroCount(value : Vector64`1) was skipped since it collides with above method
        # Method LeadingZeroCount(value : Vector64`1) was skipped since it collides with above method
        # Method LeadingZeroCount(value : Vector64`1) was skipped since it collides with above method
        # Method LeadingZeroCount(value : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method LeadingZeroCount(value : Vector128`1) was skipped since it collides with above method
        # Method LeadingZeroCount(value : Vector128`1) was skipped since it collides with above method
        # Method LeadingZeroCount(value : Vector128`1) was skipped since it collides with above method
        # Method LeadingZeroCount(value : Vector128`1) was skipped since it collides with above method
        # Method LeadingZeroCount(value : Vector128`1) was skipped since it collides with above method

    # Skipped Load2xVector64 due to it being static, abstract and generic.

    Load2xVector64 : Load2xVector64_MethodGroup
    class Load2xVector64_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> ValueTuple_2[Vector64_1[float], Vector64_1[float]]:...
        # Method Load2xVector64(address : Byte*) was skipped since it collides with above method
        # Method Load2xVector64(address : SByte*) was skipped since it collides with above method
        # Method Load2xVector64(address : Int16*) was skipped since it collides with above method
        # Method Load2xVector64(address : UInt16*) was skipped since it collides with above method
        # Method Load2xVector64(address : Int32*) was skipped since it collides with above method
        # Method Load2xVector64(address : UInt32*) was skipped since it collides with above method

    # Skipped Load2xVector64AndUnzip due to it being static, abstract and generic.

    Load2xVector64AndUnzip : Load2xVector64AndUnzip_MethodGroup
    class Load2xVector64AndUnzip_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> ValueTuple_2[Vector64_1[float], Vector64_1[float]]:...
        # Method Load2xVector64AndUnzip(address : Byte*) was skipped since it collides with above method
        # Method Load2xVector64AndUnzip(address : SByte*) was skipped since it collides with above method
        # Method Load2xVector64AndUnzip(address : Int16*) was skipped since it collides with above method
        # Method Load2xVector64AndUnzip(address : UInt16*) was skipped since it collides with above method
        # Method Load2xVector64AndUnzip(address : Int32*) was skipped since it collides with above method
        # Method Load2xVector64AndUnzip(address : UInt32*) was skipped since it collides with above method

    # Skipped Load3xVector64 due to it being static, abstract and generic.

    Load3xVector64 : Load3xVector64_MethodGroup
    class Load3xVector64_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> ValueTuple_3[Vector64_1[float], Vector64_1[float], Vector64_1[float]]:...
        # Method Load3xVector64(address : Byte*) was skipped since it collides with above method
        # Method Load3xVector64(address : SByte*) was skipped since it collides with above method
        # Method Load3xVector64(address : Int16*) was skipped since it collides with above method
        # Method Load3xVector64(address : UInt16*) was skipped since it collides with above method
        # Method Load3xVector64(address : Int32*) was skipped since it collides with above method
        # Method Load3xVector64(address : UInt32*) was skipped since it collides with above method

    # Skipped Load3xVector64AndUnzip due to it being static, abstract and generic.

    Load3xVector64AndUnzip : Load3xVector64AndUnzip_MethodGroup
    class Load3xVector64AndUnzip_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> ValueTuple_3[Vector64_1[float], Vector64_1[float], Vector64_1[float]]:...
        # Method Load3xVector64AndUnzip(address : Byte*) was skipped since it collides with above method
        # Method Load3xVector64AndUnzip(address : SByte*) was skipped since it collides with above method
        # Method Load3xVector64AndUnzip(address : Int16*) was skipped since it collides with above method
        # Method Load3xVector64AndUnzip(address : UInt16*) was skipped since it collides with above method
        # Method Load3xVector64AndUnzip(address : Int32*) was skipped since it collides with above method
        # Method Load3xVector64AndUnzip(address : UInt32*) was skipped since it collides with above method

    # Skipped Load4xVector64 due to it being static, abstract and generic.

    Load4xVector64 : Load4xVector64_MethodGroup
    class Load4xVector64_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> ValueTuple_4[Vector64_1[float], Vector64_1[float], Vector64_1[float], Vector64_1[float]]:...
        # Method Load4xVector64(address : Byte*) was skipped since it collides with above method
        # Method Load4xVector64(address : SByte*) was skipped since it collides with above method
        # Method Load4xVector64(address : Int16*) was skipped since it collides with above method
        # Method Load4xVector64(address : UInt16*) was skipped since it collides with above method
        # Method Load4xVector64(address : Int32*) was skipped since it collides with above method
        # Method Load4xVector64(address : UInt32*) was skipped since it collides with above method

    # Skipped Load4xVector64AndUnzip due to it being static, abstract and generic.

    Load4xVector64AndUnzip : Load4xVector64AndUnzip_MethodGroup
    class Load4xVector64AndUnzip_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> ValueTuple_4[Vector64_1[float], Vector64_1[float], Vector64_1[float], Vector64_1[float]]:...
        # Method Load4xVector64AndUnzip(address : Byte*) was skipped since it collides with above method
        # Method Load4xVector64AndUnzip(address : SByte*) was skipped since it collides with above method
        # Method Load4xVector64AndUnzip(address : Int16*) was skipped since it collides with above method
        # Method Load4xVector64AndUnzip(address : UInt16*) was skipped since it collides with above method
        # Method Load4xVector64AndUnzip(address : Int32*) was skipped since it collides with above method
        # Method Load4xVector64AndUnzip(address : UInt32*) was skipped since it collides with above method

    # Skipped LoadAndInsertScalar due to it being static, abstract and generic.

    LoadAndInsertScalar : LoadAndInsertScalar_MethodGroup
    class LoadAndInsertScalar_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float], index: int, address: clr.Reference[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float], index: int, address: clr.Reference[float]) -> Vector128_1[float]:...
        # Method LoadAndInsertScalar(value : Vector128`1, index : Byte, address : Single*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(value : Vector64`1, index : Byte, address : Byte*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(value : Vector64`1, index : Byte, address : Int16*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(value : Vector64`1, index : Byte, address : Int32*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(value : Vector64`1, index : Byte, address : SByte*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(value : Vector64`1, index : Byte, address : UInt16*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(value : Vector64`1, index : Byte, address : UInt32*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(value : Vector128`1, index : Byte, address : Byte*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(value : Vector128`1, index : Byte, address : Int16*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(value : Vector128`1, index : Byte, address : Int32*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(value : Vector128`1, index : Byte, address : Int64*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(value : Vector128`1, index : Byte, address : SByte*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(value : Vector128`1, index : Byte, address : UInt16*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(value : Vector128`1, index : Byte, address : UInt32*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(value : Vector128`1, index : Byte, address : UInt64*) was skipped since it collides with above method
        @typing.overload
        def __call__(self, values: ValueTuple_2[Vector64_1[float], Vector64_1[float]], index: int, address: clr.Reference[float]) -> ValueTuple_2[Vector64_1[float], Vector64_1[float]]:...
        @typing.overload
        def __call__(self, values: ValueTuple_3[Vector64_1[float], Vector64_1[float], Vector64_1[float]], index: int, address: clr.Reference[float]) -> ValueTuple_3[Vector64_1[float], Vector64_1[float], Vector64_1[float]]:...
        @typing.overload
        def __call__(self, values: ValueTuple_4[Vector64_1[float], Vector64_1[float], Vector64_1[float], Vector64_1[float]], index: int, address: clr.Reference[float]) -> ValueTuple_4[Vector64_1[float], Vector64_1[float], Vector64_1[float], Vector64_1[float]]:...
        # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : Byte*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : SByte*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : Int16*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : UInt16*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : Int32*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : UInt32*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : Byte*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : SByte*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : Int16*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : UInt16*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : Int32*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : UInt32*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : Byte*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : SByte*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : Int16*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : UInt16*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : Int32*) was skipped since it collides with above method
        # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : UInt32*) was skipped since it collides with above method

    # Skipped LoadAndReplicateToVector128 due to it being static, abstract and generic.

    LoadAndReplicateToVector128 : LoadAndReplicateToVector128_MethodGroup
    class LoadAndReplicateToVector128_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> Vector128_1[float]:...
        # Method LoadAndReplicateToVector128(address : Byte*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector128(address : Int16*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector128(address : Int32*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector128(address : SByte*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector128(address : UInt16*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector128(address : UInt32*) was skipped since it collides with above method

    # Skipped LoadAndReplicateToVector64 due to it being static, abstract and generic.

    LoadAndReplicateToVector64 : LoadAndReplicateToVector64_MethodGroup
    class LoadAndReplicateToVector64_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> Vector64_1[float]:...
        # Method LoadAndReplicateToVector64(address : Byte*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64(address : Int16*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64(address : Int32*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64(address : SByte*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64(address : UInt16*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64(address : UInt32*) was skipped since it collides with above method

    # Skipped LoadAndReplicateToVector64x2 due to it being static, abstract and generic.

    LoadAndReplicateToVector64x2 : LoadAndReplicateToVector64x2_MethodGroup
    class LoadAndReplicateToVector64x2_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> ValueTuple_2[Vector64_1[float], Vector64_1[float]]:...
        # Method LoadAndReplicateToVector64x2(address : Byte*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x2(address : SByte*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x2(address : Int16*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x2(address : UInt16*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x2(address : Int32*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x2(address : UInt32*) was skipped since it collides with above method

    # Skipped LoadAndReplicateToVector64x3 due to it being static, abstract and generic.

    LoadAndReplicateToVector64x3 : LoadAndReplicateToVector64x3_MethodGroup
    class LoadAndReplicateToVector64x3_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> ValueTuple_3[Vector64_1[float], Vector64_1[float], Vector64_1[float]]:...
        # Method LoadAndReplicateToVector64x3(address : Byte*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x3(address : SByte*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x3(address : Int16*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x3(address : UInt16*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x3(address : Int32*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x3(address : UInt32*) was skipped since it collides with above method

    # Skipped LoadAndReplicateToVector64x4 due to it being static, abstract and generic.

    LoadAndReplicateToVector64x4 : LoadAndReplicateToVector64x4_MethodGroup
    class LoadAndReplicateToVector64x4_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> ValueTuple_4[Vector64_1[float], Vector64_1[float], Vector64_1[float], Vector64_1[float]]:...
        # Method LoadAndReplicateToVector64x4(address : Byte*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x4(address : SByte*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x4(address : Int16*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x4(address : UInt16*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x4(address : Int32*) was skipped since it collides with above method
        # Method LoadAndReplicateToVector64x4(address : UInt32*) was skipped since it collides with above method

    # Skipped LoadVector128 due to it being static, abstract and generic.

    LoadVector128 : LoadVector128_MethodGroup
    class LoadVector128_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> Vector128_1[float]:...
        # Method LoadVector128(address : Single*) was skipped since it collides with above method
        # Method LoadVector128(address : Byte*) was skipped since it collides with above method
        # Method LoadVector128(address : Int16*) was skipped since it collides with above method
        # Method LoadVector128(address : Int32*) was skipped since it collides with above method
        # Method LoadVector128(address : Int64*) was skipped since it collides with above method
        # Method LoadVector128(address : SByte*) was skipped since it collides with above method
        # Method LoadVector128(address : UInt16*) was skipped since it collides with above method
        # Method LoadVector128(address : UInt32*) was skipped since it collides with above method
        # Method LoadVector128(address : UInt64*) was skipped since it collides with above method

    # Skipped LoadVector64 due to it being static, abstract and generic.

    LoadVector64 : LoadVector64_MethodGroup
    class LoadVector64_MethodGroup:
        def __call__(self, address: clr.Reference[float]) -> Vector64_1[float]:...
        # Method LoadVector64(address : Single*) was skipped since it collides with above method
        # Method LoadVector64(address : Byte*) was skipped since it collides with above method
        # Method LoadVector64(address : Int16*) was skipped since it collides with above method
        # Method LoadVector64(address : Int32*) was skipped since it collides with above method
        # Method LoadVector64(address : Int64*) was skipped since it collides with above method
        # Method LoadVector64(address : SByte*) was skipped since it collides with above method
        # Method LoadVector64(address : UInt16*) was skipped since it collides with above method
        # Method LoadVector64(address : UInt32*) was skipped since it collides with above method
        # Method LoadVector64(address : UInt64*) was skipped since it collides with above method

    # Skipped Max due to it being static, abstract and generic.

    Max : Max_MethodGroup
    class Max_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Max(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Max(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Max(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Max(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Max(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Max(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Max(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Max(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Max(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Max(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Max(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Max(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MaxNumber due to it being static, abstract and generic.

    MaxNumber : MaxNumber_MethodGroup
    class MaxNumber_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped MaxNumberScalar due to it being static, abstract and generic.

    MaxNumberScalar : MaxNumberScalar_MethodGroup
    class MaxNumberScalar_MethodGroup:
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method MaxNumberScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MaxPairwise due to it being static, abstract and generic.

    MaxPairwise : MaxPairwise_MethodGroup
    class MaxPairwise_MethodGroup:
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method MaxPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MaxPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MaxPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MaxPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MaxPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MaxPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped Min due to it being static, abstract and generic.

    Min : Min_MethodGroup
    class Min_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Min(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Min(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Min(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Min(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Min(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Min(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Min(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Min(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Min(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Min(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Min(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Min(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MinNumber due to it being static, abstract and generic.

    MinNumber : MinNumber_MethodGroup
    class MinNumber_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped MinNumberScalar due to it being static, abstract and generic.

    MinNumberScalar : MinNumberScalar_MethodGroup
    class MinNumberScalar_MethodGroup:
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method MinNumberScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MinPairwise due to it being static, abstract and generic.

    MinPairwise : MinPairwise_MethodGroup
    class MinPairwise_MethodGroup:
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method MinPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MinPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MinPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MinPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MinPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MinPairwise(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Multiply(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Multiply(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Multiply(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Multiply(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Multiply(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Multiply(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Multiply(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Multiply(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Multiply(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Multiply(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Multiply(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Multiply(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyAdd due to it being static, abstract and generic.

    MultiplyAdd : MultiplyAdd_MethodGroup
    class MultiplyAdd_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method MultiplyAdd(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyAdd(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyAdd(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyAdd(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyAdd(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyAddByScalar due to it being static, abstract and generic.

    MultiplyAddByScalar : MultiplyAddByScalar_MethodGroup
    class MultiplyAddByScalar_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method MultiplyAddByScalar(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyAddByScalar(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyAddByScalar(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyAddByScalar(addend : Vector128`1, left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyAddByScalar(addend : Vector128`1, left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyAddByScalar(addend : Vector128`1, left : Vector128`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyAddBySelectedScalar due to it being static, abstract and generic.

    MultiplyAddBySelectedScalar : MultiplyAddBySelectedScalar_MethodGroup
    class MultiplyAddBySelectedScalar_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector64_1[int]:...
        # Method MultiplyAddBySelectedScalar(addend : Vector64`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyAddBySelectedScalar(addend : Vector64`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyAddBySelectedScalar(addend : Vector64`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyAddBySelectedScalar(addend : Vector64`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyAddBySelectedScalar(addend : Vector64`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyAddBySelectedScalar(addend : Vector64`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyAddBySelectedScalar(addend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyAddBySelectedScalar(addend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyAddBySelectedScalar(addend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyAddBySelectedScalar(addend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyAddBySelectedScalar(addend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyAddBySelectedScalar(addend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyByScalar due to it being static, abstract and generic.

    MultiplyByScalar : MultiplyByScalar_MethodGroup
    class MultiplyByScalar_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector64_1[float]) -> Vector128_1[float]:...
        # Method MultiplyByScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyByScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyByScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyByScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyByScalar(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyByScalar(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyByScalar(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyByScalar(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalar due to it being static, abstract and generic.

    MultiplyBySelectedScalar : MultiplyBySelectedScalar_MethodGroup
    class MultiplyBySelectedScalar_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float], rightIndex: int) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector128_1[float], rightIndex: int) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector64_1[float], rightIndex: int) -> Vector128_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float], rightIndex: int) -> Vector128_1[float]:...
        # Method MultiplyBySelectedScalar(left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalarWideningLower due to it being static, abstract and generic.

    MultiplyBySelectedScalarWideningLower : MultiplyBySelectedScalarWideningLower_MethodGroup
    class MultiplyBySelectedScalarWideningLower_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyBySelectedScalarWideningLower(left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLower(left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLower(left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLower(left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLower(left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLower(left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalarWideningLowerAndAdd due to it being static, abstract and generic.

    MultiplyBySelectedScalarWideningLowerAndAdd : MultiplyBySelectedScalarWideningLowerAndAdd_MethodGroup
    class MultiplyBySelectedScalarWideningLowerAndAdd_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyBySelectedScalarWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalarWideningLowerAndSubtract due to it being static, abstract and generic.

    MultiplyBySelectedScalarWideningLowerAndSubtract : MultiplyBySelectedScalarWideningLowerAndSubtract_MethodGroup
    class MultiplyBySelectedScalarWideningLowerAndSubtract_MethodGroup:
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyBySelectedScalarWideningLowerAndSubtract(minuend : Vector128`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLowerAndSubtract(minuend : Vector128`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLowerAndSubtract(minuend : Vector128`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLowerAndSubtract(minuend : Vector128`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLowerAndSubtract(minuend : Vector128`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningLowerAndSubtract(minuend : Vector128`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalarWideningUpper due to it being static, abstract and generic.

    MultiplyBySelectedScalarWideningUpper : MultiplyBySelectedScalarWideningUpper_MethodGroup
    class MultiplyBySelectedScalarWideningUpper_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyBySelectedScalarWideningUpper(left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpper(left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpper(left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpper(left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpper(left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpper(left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalarWideningUpperAndAdd due to it being static, abstract and generic.

    MultiplyBySelectedScalarWideningUpperAndAdd : MultiplyBySelectedScalarWideningUpperAndAdd_MethodGroup
    class MultiplyBySelectedScalarWideningUpperAndAdd_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyBySelectedScalarWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalarWideningUpperAndSubtract due to it being static, abstract and generic.

    MultiplyBySelectedScalarWideningUpperAndSubtract : MultiplyBySelectedScalarWideningUpperAndSubtract_MethodGroup
    class MultiplyBySelectedScalarWideningUpperAndSubtract_MethodGroup:
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector128_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyBySelectedScalarWideningUpperAndSubtract(minuend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpperAndSubtract(minuend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpperAndSubtract(minuend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpperAndSubtract(minuend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpperAndSubtract(minuend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningUpperAndSubtract(minuend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyDoublingByScalarSaturateHigh due to it being static, abstract and generic.

    MultiplyDoublingByScalarSaturateHigh : MultiplyDoublingByScalarSaturateHigh_MethodGroup
    class MultiplyDoublingByScalarSaturateHigh_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method MultiplyDoublingByScalarSaturateHigh(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyDoublingByScalarSaturateHigh(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingBySelectedScalarSaturateHigh due to it being static, abstract and generic.

    MultiplyDoublingBySelectedScalarSaturateHigh : MultiplyDoublingBySelectedScalarSaturateHigh_MethodGroup
    class MultiplyDoublingBySelectedScalarSaturateHigh_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector64_1[int]:...
        # Method MultiplyDoublingBySelectedScalarSaturateHigh(left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyDoublingBySelectedScalarSaturateHigh(left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyDoublingBySelectedScalarSaturateHigh(left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyDoublingBySelectedScalarSaturateHigh(left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyDoublingSaturateHigh due to it being static, abstract and generic.

    MultiplyDoublingSaturateHigh : MultiplyDoublingSaturateHigh_MethodGroup
    class MultiplyDoublingSaturateHigh_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method MultiplyDoublingSaturateHigh(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyDoublingSaturateHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningLowerAndAddSaturate due to it being static, abstract and generic.

    MultiplyDoublingWideningLowerAndAddSaturate : MultiplyDoublingWideningLowerAndAddSaturate_MethodGroup
    class MultiplyDoublingWideningLowerAndAddSaturate_MethodGroup:
        def __call__(self, addend: Vector128_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningLowerAndAddSaturate(addend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningLowerAndSubtractSaturate due to it being static, abstract and generic.

    MultiplyDoublingWideningLowerAndSubtractSaturate : MultiplyDoublingWideningLowerAndSubtractSaturate_MethodGroup
    class MultiplyDoublingWideningLowerAndSubtractSaturate_MethodGroup:
        def __call__(self, minuend: Vector128_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningLowerAndSubtractSaturate(minuend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningLowerByScalarAndAddSaturate due to it being static, abstract and generic.

    MultiplyDoublingWideningLowerByScalarAndAddSaturate : MultiplyDoublingWideningLowerByScalarAndAddSaturate_MethodGroup
    class MultiplyDoublingWideningLowerByScalarAndAddSaturate_MethodGroup:
        def __call__(self, addend: Vector128_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningLowerByScalarAndAddSaturate(addend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningLowerByScalarAndSubtractSaturate due to it being static, abstract and generic.

    MultiplyDoublingWideningLowerByScalarAndSubtractSaturate : MultiplyDoublingWideningLowerByScalarAndSubtractSaturate_MethodGroup
    class MultiplyDoublingWideningLowerByScalarAndSubtractSaturate_MethodGroup:
        def __call__(self, minuend: Vector128_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningLowerByScalarAndSubtractSaturate(minuend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningLowerBySelectedScalarAndAddSaturate due to it being static, abstract and generic.

    MultiplyDoublingWideningLowerBySelectedScalarAndAddSaturate : MultiplyDoublingWideningLowerBySelectedScalarAndAddSaturate_MethodGroup
    class MultiplyDoublingWideningLowerBySelectedScalarAndAddSaturate_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningLowerBySelectedScalarAndAddSaturate(addend : Vector128`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyDoublingWideningLowerBySelectedScalarAndAddSaturate(addend : Vector128`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningLowerBySelectedScalarAndSubtractSaturate due to it being static, abstract and generic.

    MultiplyDoublingWideningLowerBySelectedScalarAndSubtractSaturate : MultiplyDoublingWideningLowerBySelectedScalarAndSubtractSaturate_MethodGroup
    class MultiplyDoublingWideningLowerBySelectedScalarAndSubtractSaturate_MethodGroup:
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningLowerBySelectedScalarAndSubtractSaturate(minuend : Vector128`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyDoublingWideningLowerBySelectedScalarAndSubtractSaturate(minuend : Vector128`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningSaturateLower due to it being static, abstract and generic.

    MultiplyDoublingWideningSaturateLower : MultiplyDoublingWideningSaturateLower_MethodGroup
    class MultiplyDoublingWideningSaturateLower_MethodGroup:
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningSaturateLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningSaturateLowerByScalar due to it being static, abstract and generic.

    MultiplyDoublingWideningSaturateLowerByScalar : MultiplyDoublingWideningSaturateLowerByScalar_MethodGroup
    class MultiplyDoublingWideningSaturateLowerByScalar_MethodGroup:
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningSaturateLowerByScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningSaturateLowerBySelectedScalar due to it being static, abstract and generic.

    MultiplyDoublingWideningSaturateLowerBySelectedScalar : MultiplyDoublingWideningSaturateLowerBySelectedScalar_MethodGroup
    class MultiplyDoublingWideningSaturateLowerBySelectedScalar_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningSaturateLowerBySelectedScalar(left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyDoublingWideningSaturateLowerBySelectedScalar(left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningSaturateUpper due to it being static, abstract and generic.

    MultiplyDoublingWideningSaturateUpper : MultiplyDoublingWideningSaturateUpper_MethodGroup
    class MultiplyDoublingWideningSaturateUpper_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningSaturateUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningSaturateUpperByScalar due to it being static, abstract and generic.

    MultiplyDoublingWideningSaturateUpperByScalar : MultiplyDoublingWideningSaturateUpperByScalar_MethodGroup
    class MultiplyDoublingWideningSaturateUpperByScalar_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningSaturateUpperByScalar(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningSaturateUpperBySelectedScalar due to it being static, abstract and generic.

    MultiplyDoublingWideningSaturateUpperBySelectedScalar : MultiplyDoublingWideningSaturateUpperBySelectedScalar_MethodGroup
    class MultiplyDoublingWideningSaturateUpperBySelectedScalar_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningSaturateUpperBySelectedScalar(left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyDoublingWideningSaturateUpperBySelectedScalar(left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningUpperAndAddSaturate due to it being static, abstract and generic.

    MultiplyDoublingWideningUpperAndAddSaturate : MultiplyDoublingWideningUpperAndAddSaturate_MethodGroup
    class MultiplyDoublingWideningUpperAndAddSaturate_MethodGroup:
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningUpperAndAddSaturate(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningUpperAndSubtractSaturate due to it being static, abstract and generic.

    MultiplyDoublingWideningUpperAndSubtractSaturate : MultiplyDoublingWideningUpperAndSubtractSaturate_MethodGroup
    class MultiplyDoublingWideningUpperAndSubtractSaturate_MethodGroup:
        def __call__(self, minuend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningUpperAndSubtractSaturate(minuend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningUpperByScalarAndAddSaturate due to it being static, abstract and generic.

    MultiplyDoublingWideningUpperByScalarAndAddSaturate : MultiplyDoublingWideningUpperByScalarAndAddSaturate_MethodGroup
    class MultiplyDoublingWideningUpperByScalarAndAddSaturate_MethodGroup:
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningUpperByScalarAndAddSaturate(addend : Vector128`1, left : Vector128`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningUpperByScalarAndSubtractSaturate due to it being static, abstract and generic.

    MultiplyDoublingWideningUpperByScalarAndSubtractSaturate : MultiplyDoublingWideningUpperByScalarAndSubtractSaturate_MethodGroup
    class MultiplyDoublingWideningUpperByScalarAndSubtractSaturate_MethodGroup:
        def __call__(self, minuend: Vector128_1[int], left: Vector128_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningUpperByScalarAndSubtractSaturate(minuend : Vector128`1, left : Vector128`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningUpperBySelectedScalarAndAddSaturate due to it being static, abstract and generic.

    MultiplyDoublingWideningUpperBySelectedScalarAndAddSaturate : MultiplyDoublingWideningUpperBySelectedScalarAndAddSaturate_MethodGroup
    class MultiplyDoublingWideningUpperBySelectedScalarAndAddSaturate_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningUpperBySelectedScalarAndAddSaturate(addend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyDoublingWideningUpperBySelectedScalarAndAddSaturate(addend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningUpperBySelectedScalarAndSubtractSaturate due to it being static, abstract and generic.

    MultiplyDoublingWideningUpperBySelectedScalarAndSubtractSaturate : MultiplyDoublingWideningUpperBySelectedScalarAndSubtractSaturate_MethodGroup
    class MultiplyDoublingWideningUpperBySelectedScalarAndSubtractSaturate_MethodGroup:
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector128_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyDoublingWideningUpperBySelectedScalarAndSubtractSaturate(minuend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyDoublingWideningUpperBySelectedScalarAndSubtractSaturate(minuend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyRoundedDoublingByScalarSaturateHigh due to it being static, abstract and generic.

    MultiplyRoundedDoublingByScalarSaturateHigh : MultiplyRoundedDoublingByScalarSaturateHigh_MethodGroup
    class MultiplyRoundedDoublingByScalarSaturateHigh_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method MultiplyRoundedDoublingByScalarSaturateHigh(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyRoundedDoublingByScalarSaturateHigh(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyRoundedDoublingBySelectedScalarSaturateHigh due to it being static, abstract and generic.

    MultiplyRoundedDoublingBySelectedScalarSaturateHigh : MultiplyRoundedDoublingBySelectedScalarSaturateHigh_MethodGroup
    class MultiplyRoundedDoublingBySelectedScalarSaturateHigh_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector64_1[int]:...
        # Method MultiplyRoundedDoublingBySelectedScalarSaturateHigh(left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingBySelectedScalarSaturateHigh(left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyRoundedDoublingBySelectedScalarSaturateHigh(left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingBySelectedScalarSaturateHigh(left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyRoundedDoublingSaturateHigh due to it being static, abstract and generic.

    MultiplyRoundedDoublingSaturateHigh : MultiplyRoundedDoublingSaturateHigh_MethodGroup
    class MultiplyRoundedDoublingSaturateHigh_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method MultiplyRoundedDoublingSaturateHigh(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyRoundedDoublingSaturateHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyScalar due to it being static, abstract and generic.

    MultiplyScalar : MultiplyScalar_MethodGroup
    class MultiplyScalar_MethodGroup:
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method MultiplyScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyScalarBySelectedScalar due to it being static, abstract and generic.

    MultiplyScalarBySelectedScalar : MultiplyScalarBySelectedScalar_MethodGroup
    class MultiplyScalarBySelectedScalar_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float], rightIndex: int) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector128_1[float], rightIndex: int) -> Vector64_1[float]:...

    # Skipped MultiplySubtract due to it being static, abstract and generic.

    MultiplySubtract : MultiplySubtract_MethodGroup
    class MultiplySubtract_MethodGroup:
        @typing.overload
        def __call__(self, minuend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method MultiplySubtract(minuend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplySubtract(minuend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplySubtract(minuend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplySubtract(minuend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplySubtract(minuend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplySubtract(minuend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplySubtract(minuend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplySubtract(minuend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplySubtract(minuend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplySubtract(minuend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplySubtractByScalar due to it being static, abstract and generic.

    MultiplySubtractByScalar : MultiplySubtractByScalar_MethodGroup
    class MultiplySubtractByScalar_MethodGroup:
        @typing.overload
        def __call__(self, minuend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method MultiplySubtractByScalar(minuend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplySubtractByScalar(minuend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplySubtractByScalar(minuend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector128_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplySubtractByScalar(minuend : Vector128`1, left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplySubtractByScalar(minuend : Vector128`1, left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplySubtractByScalar(minuend : Vector128`1, left : Vector128`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplySubtractBySelectedScalar due to it being static, abstract and generic.

    MultiplySubtractBySelectedScalar : MultiplySubtractBySelectedScalar_MethodGroup
    class MultiplySubtractBySelectedScalar_MethodGroup:
        @typing.overload
        def __call__(self, minuend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, minuend: Vector64_1[int], left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector64_1[int]:...
        # Method MultiplySubtractBySelectedScalar(minuend : Vector64`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplySubtractBySelectedScalar(minuend : Vector64`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplySubtractBySelectedScalar(minuend : Vector64`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplySubtractBySelectedScalar(minuend : Vector64`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplySubtractBySelectedScalar(minuend : Vector64`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplySubtractBySelectedScalar(minuend : Vector64`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector128_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplySubtractBySelectedScalar(minuend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplySubtractBySelectedScalar(minuend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplySubtractBySelectedScalar(minuend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplySubtractBySelectedScalar(minuend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplySubtractBySelectedScalar(minuend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplySubtractBySelectedScalar(minuend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyWideningLower due to it being static, abstract and generic.

    MultiplyWideningLower : MultiplyWideningLower_MethodGroup
    class MultiplyWideningLower_MethodGroup:
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyWideningLowerAndAdd due to it being static, abstract and generic.

    MultiplyWideningLowerAndAdd : MultiplyWideningLowerAndAdd_MethodGroup
    class MultiplyWideningLowerAndAdd_MethodGroup:
        def __call__(self, addend: Vector128_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyWideningLowerAndAdd(addend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyWideningLowerAndSubtract due to it being static, abstract and generic.

    MultiplyWideningLowerAndSubtract : MultiplyWideningLowerAndSubtract_MethodGroup
    class MultiplyWideningLowerAndSubtract_MethodGroup:
        def __call__(self, minuend: Vector128_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method MultiplyWideningLowerAndSubtract(minuend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyWideningLowerAndSubtract(minuend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyWideningLowerAndSubtract(minuend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyWideningLowerAndSubtract(minuend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method MultiplyWideningLowerAndSubtract(minuend : Vector128`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped MultiplyWideningUpper due to it being static, abstract and generic.

    MultiplyWideningUpper : MultiplyWideningUpper_MethodGroup
    class MultiplyWideningUpper_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyWideningUpperAndAdd due to it being static, abstract and generic.

    MultiplyWideningUpperAndAdd : MultiplyWideningUpperAndAdd_MethodGroup
    class MultiplyWideningUpperAndAdd_MethodGroup:
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyWideningUpperAndAdd(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyWideningUpperAndSubtract due to it being static, abstract and generic.

    MultiplyWideningUpperAndSubtract : MultiplyWideningUpperAndSubtract_MethodGroup
    class MultiplyWideningUpperAndSubtract_MethodGroup:
        def __call__(self, minuend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyWideningUpperAndSubtract(minuend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyWideningUpperAndSubtract(minuend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyWideningUpperAndSubtract(minuend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyWideningUpperAndSubtract(minuend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method MultiplyWideningUpperAndSubtract(minuend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped Negate due to it being static, abstract and generic.

    Negate : Negate_MethodGroup
    class Negate_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Negate(value : Vector64`1) was skipped since it collides with above method
        # Method Negate(value : Vector64`1) was skipped since it collides with above method
        # Method Negate(value : Vector64`1) was skipped since it collides with above method
        # Method Negate(value : Vector128`1) was skipped since it collides with above method
        # Method Negate(value : Vector128`1) was skipped since it collides with above method
        # Method Negate(value : Vector128`1) was skipped since it collides with above method

    # Skipped NegateSaturate due to it being static, abstract and generic.

    NegateSaturate : NegateSaturate_MethodGroup
    class NegateSaturate_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
        # Method NegateSaturate(value : Vector64`1) was skipped since it collides with above method
        # Method NegateSaturate(value : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method NegateSaturate(value : Vector128`1) was skipped since it collides with above method
        # Method NegateSaturate(value : Vector128`1) was skipped since it collides with above method

    # Skipped NegateScalar due to it being static, abstract and generic.

    NegateScalar : NegateScalar_MethodGroup
    class NegateScalar_MethodGroup:
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        # Method NegateScalar(value : Vector64`1) was skipped since it collides with above method

    # Skipped Not due to it being static, abstract and generic.

    Not : Not_MethodGroup
    class Not_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Not(value : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Not(value : Vector128`1) was skipped since it collides with above method
        # Method Not(value : Vector64`1) was skipped since it collides with above method
        # Method Not(value : Vector64`1) was skipped since it collides with above method
        # Method Not(value : Vector64`1) was skipped since it collides with above method
        # Method Not(value : Vector64`1) was skipped since it collides with above method
        # Method Not(value : Vector64`1) was skipped since it collides with above method
        # Method Not(value : Vector64`1) was skipped since it collides with above method
        # Method Not(value : Vector64`1) was skipped since it collides with above method
        # Method Not(value : Vector64`1) was skipped since it collides with above method
        # Method Not(value : Vector128`1) was skipped since it collides with above method
        # Method Not(value : Vector128`1) was skipped since it collides with above method
        # Method Not(value : Vector128`1) was skipped since it collides with above method
        # Method Not(value : Vector128`1) was skipped since it collides with above method
        # Method Not(value : Vector128`1) was skipped since it collides with above method
        # Method Not(value : Vector128`1) was skipped since it collides with above method
        # Method Not(value : Vector128`1) was skipped since it collides with above method
        # Method Not(value : Vector128`1) was skipped since it collides with above method

    # Skipped Or due to it being static, abstract and generic.

    Or : Or_MethodGroup
    class Or_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Or(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Or(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Or(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Or(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Or(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Or(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Or(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Or(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Or(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped OrNot due to it being static, abstract and generic.

    OrNot : OrNot_MethodGroup
    class OrNot_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method OrNot(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method OrNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method OrNot(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method OrNot(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method OrNot(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method OrNot(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method OrNot(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method OrNot(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method OrNot(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method OrNot(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method OrNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method OrNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method OrNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method OrNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method OrNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method OrNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method OrNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method OrNot(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped PolynomialMultiply due to it being static, abstract and generic.

    PolynomialMultiply : PolynomialMultiply_MethodGroup
    class PolynomialMultiply_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method PolynomialMultiply(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method PolynomialMultiply(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped PolynomialMultiplyWideningLower due to it being static, abstract and generic.

    PolynomialMultiplyWideningLower : PolynomialMultiplyWideningLower_MethodGroup
    class PolynomialMultiplyWideningLower_MethodGroup:
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method PolynomialMultiplyWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped PolynomialMultiplyWideningUpper due to it being static, abstract and generic.

    PolynomialMultiplyWideningUpper : PolynomialMultiplyWideningUpper_MethodGroup
    class PolynomialMultiplyWideningUpper_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method PolynomialMultiplyWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped PopCount due to it being static, abstract and generic.

    PopCount : PopCount_MethodGroup
    class PopCount_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
        # Method PopCount(value : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method PopCount(value : Vector128`1) was skipped since it collides with above method

    # Skipped ReciprocalEstimate due to it being static, abstract and generic.

    ReciprocalEstimate : ReciprocalEstimate_MethodGroup
    class ReciprocalEstimate_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method ReciprocalEstimate(value : Vector64`1) was skipped since it collides with above method
        # Method ReciprocalEstimate(value : Vector128`1) was skipped since it collides with above method

    # Skipped ReciprocalSquareRootEstimate due to it being static, abstract and generic.

    ReciprocalSquareRootEstimate : ReciprocalSquareRootEstimate_MethodGroup
    class ReciprocalSquareRootEstimate_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
        # Method ReciprocalSquareRootEstimate(value : Vector64`1) was skipped since it collides with above method
        # Method ReciprocalSquareRootEstimate(value : Vector128`1) was skipped since it collides with above method

    # Skipped ReciprocalSquareRootStep due to it being static, abstract and generic.

    ReciprocalSquareRootStep : ReciprocalSquareRootStep_MethodGroup
    class ReciprocalSquareRootStep_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped ReciprocalStep due to it being static, abstract and generic.

    ReciprocalStep : ReciprocalStep_MethodGroup
    class ReciprocalStep_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped ReverseElement16 due to it being static, abstract and generic.

    ReverseElement16 : ReverseElement16_MethodGroup
    class ReverseElement16_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ReverseElement16(value : Vector64`1) was skipped since it collides with above method
        # Method ReverseElement16(value : Vector64`1) was skipped since it collides with above method
        # Method ReverseElement16(value : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ReverseElement16(value : Vector128`1) was skipped since it collides with above method
        # Method ReverseElement16(value : Vector128`1) was skipped since it collides with above method
        # Method ReverseElement16(value : Vector128`1) was skipped since it collides with above method

    # Skipped ReverseElement32 due to it being static, abstract and generic.

    ReverseElement32 : ReverseElement32_MethodGroup
    class ReverseElement32_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ReverseElement32(value : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ReverseElement32(value : Vector128`1) was skipped since it collides with above method

    # Skipped ReverseElement8 due to it being static, abstract and generic.

    ReverseElement8 : ReverseElement8_MethodGroup
    class ReverseElement8_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ReverseElement8(value : Vector64`1) was skipped since it collides with above method
        # Method ReverseElement8(value : Vector64`1) was skipped since it collides with above method
        # Method ReverseElement8(value : Vector64`1) was skipped since it collides with above method
        # Method ReverseElement8(value : Vector64`1) was skipped since it collides with above method
        # Method ReverseElement8(value : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ReverseElement8(value : Vector128`1) was skipped since it collides with above method
        # Method ReverseElement8(value : Vector128`1) was skipped since it collides with above method
        # Method ReverseElement8(value : Vector128`1) was skipped since it collides with above method
        # Method ReverseElement8(value : Vector128`1) was skipped since it collides with above method
        # Method ReverseElement8(value : Vector128`1) was skipped since it collides with above method

    # Skipped RoundAwayFromZero due to it being static, abstract and generic.

    RoundAwayFromZero : RoundAwayFromZero_MethodGroup
    class RoundAwayFromZero_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped RoundAwayFromZeroScalar due to it being static, abstract and generic.

    RoundAwayFromZeroScalar : RoundAwayFromZeroScalar_MethodGroup
    class RoundAwayFromZeroScalar_MethodGroup:
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        # Method RoundAwayFromZeroScalar(value : Vector64`1) was skipped since it collides with above method

    # Skipped RoundToNearest due to it being static, abstract and generic.

    RoundToNearest : RoundToNearest_MethodGroup
    class RoundToNearest_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped RoundToNearestScalar due to it being static, abstract and generic.

    RoundToNearestScalar : RoundToNearestScalar_MethodGroup
    class RoundToNearestScalar_MethodGroup:
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        # Method RoundToNearestScalar(value : Vector64`1) was skipped since it collides with above method

    # Skipped RoundToNegativeInfinity due to it being static, abstract and generic.

    RoundToNegativeInfinity : RoundToNegativeInfinity_MethodGroup
    class RoundToNegativeInfinity_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped RoundToNegativeInfinityScalar due to it being static, abstract and generic.

    RoundToNegativeInfinityScalar : RoundToNegativeInfinityScalar_MethodGroup
    class RoundToNegativeInfinityScalar_MethodGroup:
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        # Method RoundToNegativeInfinityScalar(value : Vector64`1) was skipped since it collides with above method

    # Skipped RoundToPositiveInfinity due to it being static, abstract and generic.

    RoundToPositiveInfinity : RoundToPositiveInfinity_MethodGroup
    class RoundToPositiveInfinity_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped RoundToPositiveInfinityScalar due to it being static, abstract and generic.

    RoundToPositiveInfinityScalar : RoundToPositiveInfinityScalar_MethodGroup
    class RoundToPositiveInfinityScalar_MethodGroup:
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        # Method RoundToPositiveInfinityScalar(value : Vector64`1) was skipped since it collides with above method

    # Skipped RoundToZero due to it being static, abstract and generic.

    RoundToZero : RoundToZero_MethodGroup
    class RoundToZero_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...

    # Skipped RoundToZeroScalar due to it being static, abstract and generic.

    RoundToZeroScalar : RoundToZeroScalar_MethodGroup
    class RoundToZeroScalar_MethodGroup:
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        # Method RoundToZeroScalar(value : Vector64`1) was skipped since it collides with above method

    # Skipped ShiftArithmetic due to it being static, abstract and generic.

    ShiftArithmetic : ShiftArithmetic_MethodGroup
    class ShiftArithmetic_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ShiftArithmetic(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftArithmetic(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ShiftArithmetic(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftArithmetic(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftArithmetic(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftArithmeticRounded due to it being static, abstract and generic.

    ShiftArithmeticRounded : ShiftArithmeticRounded_MethodGroup
    class ShiftArithmeticRounded_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ShiftArithmeticRounded(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftArithmeticRounded(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ShiftArithmeticRounded(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftArithmeticRounded(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftArithmeticRounded(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftArithmeticRoundedSaturate due to it being static, abstract and generic.

    ShiftArithmeticRoundedSaturate : ShiftArithmeticRoundedSaturate_MethodGroup
    class ShiftArithmeticRoundedSaturate_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ShiftArithmeticRoundedSaturate(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftArithmeticRoundedSaturate(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ShiftArithmeticRoundedSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftArithmeticRoundedSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftArithmeticRoundedSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftArithmeticSaturate due to it being static, abstract and generic.

    ShiftArithmeticSaturate : ShiftArithmeticSaturate_MethodGroup
    class ShiftArithmeticSaturate_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ShiftArithmeticSaturate(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftArithmeticSaturate(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ShiftArithmeticSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftArithmeticSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftArithmeticSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftLeftAndInsert due to it being static, abstract and generic.

    ShiftLeftAndInsert : ShiftLeftAndInsert_MethodGroup
    class ShiftLeftAndInsert_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int], shift: int) -> Vector64_1[int]:...
        # Method ShiftLeftAndInsert(left : Vector64`1, right : Vector64`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector64`1, right : Vector64`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector64`1, right : Vector64`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector64`1, right : Vector64`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector64`1, right : Vector64`1, shift : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int], shift: int) -> Vector128_1[int]:...
        # Method ShiftLeftAndInsert(left : Vector128`1, right : Vector128`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector128`1, right : Vector128`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector128`1, right : Vector128`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector128`1, right : Vector128`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector128`1, right : Vector128`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector128`1, right : Vector128`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector128`1, right : Vector128`1, shift : Byte) was skipped since it collides with above method

    # Skipped ShiftLeftAndInsertScalar due to it being static, abstract and generic.

    ShiftLeftAndInsertScalar : ShiftLeftAndInsertScalar_MethodGroup
    class ShiftLeftAndInsertScalar_MethodGroup:
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int], shift: int) -> Vector64_1[int]:...
        # Method ShiftLeftAndInsertScalar(left : Vector64`1, right : Vector64`1, shift : Byte) was skipped since it collides with above method

    # Skipped ShiftLeftLogical due to it being static, abstract and generic.

    ShiftLeftLogical : ShiftLeftLogical_MethodGroup
    class ShiftLeftLogical_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftLeftLogical(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector64`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftLeftLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftLeftLogicalSaturate due to it being static, abstract and generic.

    ShiftLeftLogicalSaturate : ShiftLeftLogicalSaturate_MethodGroup
    class ShiftLeftLogicalSaturate_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftLeftLogicalSaturate(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturate(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturate(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturate(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturate(value : Vector64`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftLeftLogicalSaturate(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturate(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturate(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturate(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturate(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturate(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturate(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftLeftLogicalSaturateScalar due to it being static, abstract and generic.

    ShiftLeftLogicalSaturateScalar : ShiftLeftLogicalSaturateScalar_MethodGroup
    class ShiftLeftLogicalSaturateScalar_MethodGroup:
        def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftLeftLogicalSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftLeftLogicalSaturateUnsigned due to it being static, abstract and generic.

    ShiftLeftLogicalSaturateUnsigned : ShiftLeftLogicalSaturateUnsigned_MethodGroup
    class ShiftLeftLogicalSaturateUnsigned_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftLeftLogicalSaturateUnsigned(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturateUnsigned(value : Vector64`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftLeftLogicalSaturateUnsigned(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturateUnsigned(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturateUnsigned(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftLeftLogicalScalar due to it being static, abstract and generic.

    ShiftLeftLogicalScalar : ShiftLeftLogicalScalar_MethodGroup
    class ShiftLeftLogicalScalar_MethodGroup:
        def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftLeftLogicalScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftLeftLogicalWideningLower due to it being static, abstract and generic.

    ShiftLeftLogicalWideningLower : ShiftLeftLogicalWideningLower_MethodGroup
    class ShiftLeftLogicalWideningLower_MethodGroup:
        def __call__(self, value: Vector64_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftLeftLogicalWideningLower(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningLower(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningLower(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningLower(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningLower(value : Vector64`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftLeftLogicalWideningUpper due to it being static, abstract and generic.

    ShiftLeftLogicalWideningUpper : ShiftLeftLogicalWideningUpper_MethodGroup
    class ShiftLeftLogicalWideningUpper_MethodGroup:
        def __call__(self, value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftLeftLogicalWideningUpper(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningUpper(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningUpper(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningUpper(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningUpper(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftLogical due to it being static, abstract and generic.

    ShiftLogical : ShiftLogical_MethodGroup
    class ShiftLogical_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ShiftLogical(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogical(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogical(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogical(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogical(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ShiftLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogical(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftLogicalRounded due to it being static, abstract and generic.

    ShiftLogicalRounded : ShiftLogicalRounded_MethodGroup
    class ShiftLogicalRounded_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ShiftLogicalRounded(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogicalRounded(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogicalRounded(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogicalRounded(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogicalRounded(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ShiftLogicalRounded(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalRounded(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalRounded(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalRounded(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalRounded(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalRounded(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalRounded(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftLogicalRoundedSaturate due to it being static, abstract and generic.

    ShiftLogicalRoundedSaturate : ShiftLogicalRoundedSaturate_MethodGroup
    class ShiftLogicalRoundedSaturate_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ShiftLogicalRoundedSaturate(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogicalRoundedSaturate(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogicalRoundedSaturate(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogicalRoundedSaturate(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogicalRoundedSaturate(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ShiftLogicalRoundedSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalRoundedSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalRoundedSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalRoundedSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalRoundedSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalRoundedSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalRoundedSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftLogicalRoundedSaturateScalar due to it being static, abstract and generic.

    ShiftLogicalRoundedSaturateScalar : ShiftLogicalRoundedSaturateScalar_MethodGroup
    class ShiftLogicalRoundedSaturateScalar_MethodGroup:
        def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ShiftLogicalRoundedSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method

    # Skipped ShiftLogicalRoundedScalar due to it being static, abstract and generic.

    ShiftLogicalRoundedScalar : ShiftLogicalRoundedScalar_MethodGroup
    class ShiftLogicalRoundedScalar_MethodGroup:
        def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ShiftLogicalRoundedScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method

    # Skipped ShiftLogicalSaturate due to it being static, abstract and generic.

    ShiftLogicalSaturate : ShiftLogicalSaturate_MethodGroup
    class ShiftLogicalSaturate_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ShiftLogicalSaturate(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogicalSaturate(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogicalSaturate(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogicalSaturate(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        # Method ShiftLogicalSaturate(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ShiftLogicalSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method
        # Method ShiftLogicalSaturate(value : Vector128`1, count : Vector128`1) was skipped since it collides with above method

    # Skipped ShiftLogicalSaturateScalar due to it being static, abstract and generic.

    ShiftLogicalSaturateScalar : ShiftLogicalSaturateScalar_MethodGroup
    class ShiftLogicalSaturateScalar_MethodGroup:
        def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ShiftLogicalSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method

    # Skipped ShiftLogicalScalar due to it being static, abstract and generic.

    ShiftLogicalScalar : ShiftLogicalScalar_MethodGroup
    class ShiftLogicalScalar_MethodGroup:
        def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
        # Method ShiftLogicalScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method

    # Skipped ShiftRightAndInsert due to it being static, abstract and generic.

    ShiftRightAndInsert : ShiftRightAndInsert_MethodGroup
    class ShiftRightAndInsert_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int], shift: int) -> Vector64_1[int]:...
        # Method ShiftRightAndInsert(left : Vector64`1, right : Vector64`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector64`1, right : Vector64`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector64`1, right : Vector64`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector64`1, right : Vector64`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector64`1, right : Vector64`1, shift : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int], shift: int) -> Vector128_1[int]:...
        # Method ShiftRightAndInsert(left : Vector128`1, right : Vector128`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector128`1, right : Vector128`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector128`1, right : Vector128`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector128`1, right : Vector128`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector128`1, right : Vector128`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector128`1, right : Vector128`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector128`1, right : Vector128`1, shift : Byte) was skipped since it collides with above method

    # Skipped ShiftRightAndInsertScalar due to it being static, abstract and generic.

    ShiftRightAndInsertScalar : ShiftRightAndInsertScalar_MethodGroup
    class ShiftRightAndInsertScalar_MethodGroup:
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int], shift: int) -> Vector64_1[int]:...
        # Method ShiftRightAndInsertScalar(left : Vector64`1, right : Vector64`1, shift : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmetic due to it being static, abstract and generic.

    ShiftRightArithmetic : ShiftRightArithmetic_MethodGroup
    class ShiftRightArithmetic_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightArithmetic(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmetic(value : Vector64`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightArithmetic(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmetic(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmetic(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticAdd due to it being static, abstract and generic.

    ShiftRightArithmeticAdd : ShiftRightArithmeticAdd_MethodGroup
    class ShiftRightArithmeticAdd_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector64_1[int], value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightArithmeticAdd(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticAdd(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector128_1[int], value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightArithmeticAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticNarrowingSaturateLower due to it being static, abstract and generic.

    ShiftRightArithmeticNarrowingSaturateLower : ShiftRightArithmeticNarrowingSaturateLower_MethodGroup
    class ShiftRightArithmeticNarrowingSaturateLower_MethodGroup:
        def __call__(self, value: Vector128_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightArithmeticNarrowingSaturateLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticNarrowingSaturateLower(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticNarrowingSaturateUnsignedLower due to it being static, abstract and generic.

    ShiftRightArithmeticNarrowingSaturateUnsignedLower : ShiftRightArithmeticNarrowingSaturateUnsignedLower_MethodGroup
    class ShiftRightArithmeticNarrowingSaturateUnsignedLower_MethodGroup:
        def __call__(self, value: Vector128_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightArithmeticNarrowingSaturateUnsignedLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticNarrowingSaturateUnsignedLower(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticNarrowingSaturateUnsignedUpper due to it being static, abstract and generic.

    ShiftRightArithmeticNarrowingSaturateUnsignedUpper : ShiftRightArithmeticNarrowingSaturateUnsignedUpper_MethodGroup
    class ShiftRightArithmeticNarrowingSaturateUnsignedUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightArithmeticNarrowingSaturateUnsignedUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticNarrowingSaturateUnsignedUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticNarrowingSaturateUpper due to it being static, abstract and generic.

    ShiftRightArithmeticNarrowingSaturateUpper : ShiftRightArithmeticNarrowingSaturateUpper_MethodGroup
    class ShiftRightArithmeticNarrowingSaturateUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightArithmeticNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticRounded due to it being static, abstract and generic.

    ShiftRightArithmeticRounded : ShiftRightArithmeticRounded_MethodGroup
    class ShiftRightArithmeticRounded_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightArithmeticRounded(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRounded(value : Vector64`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightArithmeticRounded(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRounded(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRounded(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticRoundedAdd due to it being static, abstract and generic.

    ShiftRightArithmeticRoundedAdd : ShiftRightArithmeticRoundedAdd_MethodGroup
    class ShiftRightArithmeticRoundedAdd_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector64_1[int], value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightArithmeticRoundedAdd(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRoundedAdd(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector128_1[int], value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightArithmeticRoundedAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRoundedAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRoundedAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticRoundedNarrowingSaturateLower due to it being static, abstract and generic.

    ShiftRightArithmeticRoundedNarrowingSaturateLower : ShiftRightArithmeticRoundedNarrowingSaturateLower_MethodGroup
    class ShiftRightArithmeticRoundedNarrowingSaturateLower_MethodGroup:
        def __call__(self, value: Vector128_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightArithmeticRoundedNarrowingSaturateLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRoundedNarrowingSaturateLower(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticRoundedNarrowingSaturateUnsignedLower due to it being static, abstract and generic.

    ShiftRightArithmeticRoundedNarrowingSaturateUnsignedLower : ShiftRightArithmeticRoundedNarrowingSaturateUnsignedLower_MethodGroup
    class ShiftRightArithmeticRoundedNarrowingSaturateUnsignedLower_MethodGroup:
        def __call__(self, value: Vector128_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightArithmeticRoundedNarrowingSaturateUnsignedLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRoundedNarrowingSaturateUnsignedLower(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticRoundedNarrowingSaturateUnsignedUpper due to it being static, abstract and generic.

    ShiftRightArithmeticRoundedNarrowingSaturateUnsignedUpper : ShiftRightArithmeticRoundedNarrowingSaturateUnsignedUpper_MethodGroup
    class ShiftRightArithmeticRoundedNarrowingSaturateUnsignedUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightArithmeticRoundedNarrowingSaturateUnsignedUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRoundedNarrowingSaturateUnsignedUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticRoundedNarrowingSaturateUpper due to it being static, abstract and generic.

    ShiftRightArithmeticRoundedNarrowingSaturateUpper : ShiftRightArithmeticRoundedNarrowingSaturateUpper_MethodGroup
    class ShiftRightArithmeticRoundedNarrowingSaturateUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightArithmeticRoundedNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRoundedNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogical due to it being static, abstract and generic.

    ShiftRightLogical : ShiftRightLogical_MethodGroup
    class ShiftRightLogical_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightLogical(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector64`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogical(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalAdd due to it being static, abstract and generic.

    ShiftRightLogicalAdd : ShiftRightLogicalAdd_MethodGroup
    class ShiftRightLogicalAdd_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector64_1[int], value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightLogicalAdd(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalAdd(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalAdd(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalAdd(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalAdd(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector128_1[int], value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightLogicalAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalAddScalar due to it being static, abstract and generic.

    ShiftRightLogicalAddScalar : ShiftRightLogicalAddScalar_MethodGroup
    class ShiftRightLogicalAddScalar_MethodGroup:
        def __call__(self, addend: Vector64_1[int], value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightLogicalAddScalar(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalNarrowingLower due to it being static, abstract and generic.

    ShiftRightLogicalNarrowingLower : ShiftRightLogicalNarrowingLower_MethodGroup
    class ShiftRightLogicalNarrowingLower_MethodGroup:
        def __call__(self, value: Vector128_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightLogicalNarrowingLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingLower(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalNarrowingSaturateLower due to it being static, abstract and generic.

    ShiftRightLogicalNarrowingSaturateLower : ShiftRightLogicalNarrowingSaturateLower_MethodGroup
    class ShiftRightLogicalNarrowingSaturateLower_MethodGroup:
        def __call__(self, value: Vector128_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightLogicalNarrowingSaturateLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingSaturateLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingSaturateLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingSaturateLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingSaturateLower(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalNarrowingSaturateUpper due to it being static, abstract and generic.

    ShiftRightLogicalNarrowingSaturateUpper : ShiftRightLogicalNarrowingSaturateUpper_MethodGroup
    class ShiftRightLogicalNarrowingSaturateUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightLogicalNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalNarrowingUpper due to it being static, abstract and generic.

    ShiftRightLogicalNarrowingUpper : ShiftRightLogicalNarrowingUpper_MethodGroup
    class ShiftRightLogicalNarrowingUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightLogicalNarrowingUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalRounded due to it being static, abstract and generic.

    ShiftRightLogicalRounded : ShiftRightLogicalRounded_MethodGroup
    class ShiftRightLogicalRounded_MethodGroup:
        @typing.overload
        def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightLogicalRounded(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRounded(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRounded(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRounded(value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRounded(value : Vector64`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightLogicalRounded(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRounded(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRounded(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRounded(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRounded(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRounded(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRounded(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalRoundedAdd due to it being static, abstract and generic.

    ShiftRightLogicalRoundedAdd : ShiftRightLogicalRoundedAdd_MethodGroup
    class ShiftRightLogicalRoundedAdd_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector64_1[int], value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightLogicalRoundedAdd(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedAdd(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedAdd(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedAdd(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedAdd(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector128_1[int], value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightLogicalRoundedAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedAdd(addend : Vector128`1, value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalRoundedAddScalar due to it being static, abstract and generic.

    ShiftRightLogicalRoundedAddScalar : ShiftRightLogicalRoundedAddScalar_MethodGroup
    class ShiftRightLogicalRoundedAddScalar_MethodGroup:
        def __call__(self, addend: Vector64_1[int], value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightLogicalRoundedAddScalar(addend : Vector64`1, value : Vector64`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalRoundedNarrowingLower due to it being static, abstract and generic.

    ShiftRightLogicalRoundedNarrowingLower : ShiftRightLogicalRoundedNarrowingLower_MethodGroup
    class ShiftRightLogicalRoundedNarrowingLower_MethodGroup:
        def __call__(self, value: Vector128_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightLogicalRoundedNarrowingLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingLower(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalRoundedNarrowingSaturateLower due to it being static, abstract and generic.

    ShiftRightLogicalRoundedNarrowingSaturateLower : ShiftRightLogicalRoundedNarrowingSaturateLower_MethodGroup
    class ShiftRightLogicalRoundedNarrowingSaturateLower_MethodGroup:
        def __call__(self, value: Vector128_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightLogicalRoundedNarrowingSaturateLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingSaturateLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingSaturateLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingSaturateLower(value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingSaturateLower(value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalRoundedNarrowingSaturateUpper due to it being static, abstract and generic.

    ShiftRightLogicalRoundedNarrowingSaturateUpper : ShiftRightLogicalRoundedNarrowingSaturateUpper_MethodGroup
    class ShiftRightLogicalRoundedNarrowingSaturateUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightLogicalRoundedNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingSaturateUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalRoundedNarrowingUpper due to it being static, abstract and generic.

    ShiftRightLogicalRoundedNarrowingUpper : ShiftRightLogicalRoundedNarrowingUpper_MethodGroup
    class ShiftRightLogicalRoundedNarrowingUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], value: Vector128_1[int], count: int) -> Vector128_1[int]:...
        # Method ShiftRightLogicalRoundedNarrowingUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingUpper(lower : Vector64`1, value : Vector128`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalRoundedScalar due to it being static, abstract and generic.

    ShiftRightLogicalRoundedScalar : ShiftRightLogicalRoundedScalar_MethodGroup
    class ShiftRightLogicalRoundedScalar_MethodGroup:
        def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightLogicalRoundedScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalScalar due to it being static, abstract and generic.

    ShiftRightLogicalScalar : ShiftRightLogicalScalar_MethodGroup
    class ShiftRightLogicalScalar_MethodGroup:
        def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
        # Method ShiftRightLogicalScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method

    # Skipped SignExtendWideningLower due to it being static, abstract and generic.

    SignExtendWideningLower : SignExtendWideningLower_MethodGroup
    class SignExtendWideningLower_MethodGroup:
        def __call__(self, value: Vector64_1[int]) -> Vector128_1[int]:...
        # Method SignExtendWideningLower(value : Vector64`1) was skipped since it collides with above method
        # Method SignExtendWideningLower(value : Vector64`1) was skipped since it collides with above method

    # Skipped SignExtendWideningUpper due to it being static, abstract and generic.

    SignExtendWideningUpper : SignExtendWideningUpper_MethodGroup
    class SignExtendWideningUpper_MethodGroup:
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method SignExtendWideningUpper(value : Vector128`1) was skipped since it collides with above method
        # Method SignExtendWideningUpper(value : Vector128`1) was skipped since it collides with above method

    # Skipped SqrtScalar due to it being static, abstract and generic.

    SqrtScalar : SqrtScalar_MethodGroup
    class SqrtScalar_MethodGroup:
        def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
        # Method SqrtScalar(value : Vector64`1) was skipped since it collides with above method

    # Skipped Store due to it being static, abstract and generic.

    Store : Store_MethodGroup
    class Store_MethodGroup:
        @typing.overload
        def __call__(self, address: clr.Reference[float], source: Vector64_1[float]) -> None:...
        # Method Store(address : Single*, source : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, address: clr.Reference[float], source: Vector128_1[float]) -> None:...
        # Method Store(address : Single*, source : Vector128`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, address: clr.Reference[float], value: ValueTuple_2[Vector64_1[float], Vector64_1[float]]) -> None:...
        @typing.overload
        def __call__(self, address: clr.Reference[float], value: ValueTuple_3[Vector64_1[float], Vector64_1[float], Vector64_1[float]]) -> None:...
        @typing.overload
        def __call__(self, address: clr.Reference[float], value: ValueTuple_4[Vector64_1[float], Vector64_1[float], Vector64_1[float], Vector64_1[float]]) -> None:...
        # Method Store(address : Byte*, source : Vector64`1) was skipped since it collides with above method
        # Method Store(address : Int16*, source : Vector64`1) was skipped since it collides with above method
        # Method Store(address : Int32*, source : Vector64`1) was skipped since it collides with above method
        # Method Store(address : Int64*, source : Vector64`1) was skipped since it collides with above method
        # Method Store(address : SByte*, source : Vector64`1) was skipped since it collides with above method
        # Method Store(address : UInt16*, source : Vector64`1) was skipped since it collides with above method
        # Method Store(address : UInt32*, source : Vector64`1) was skipped since it collides with above method
        # Method Store(address : UInt64*, source : Vector64`1) was skipped since it collides with above method
        # Method Store(address : Byte*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : Int16*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : Int32*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : Int64*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : SByte*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : UInt16*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : UInt32*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : UInt64*, source : Vector128`1) was skipped since it collides with above method
        # Method Store(address : Byte*, value : ValueTuple`2) was skipped since it collides with above method
        # Method Store(address : SByte*, value : ValueTuple`2) was skipped since it collides with above method
        # Method Store(address : Int16*, value : ValueTuple`2) was skipped since it collides with above method
        # Method Store(address : UInt16*, value : ValueTuple`2) was skipped since it collides with above method
        # Method Store(address : Int32*, value : ValueTuple`2) was skipped since it collides with above method
        # Method Store(address : UInt32*, value : ValueTuple`2) was skipped since it collides with above method
        # Method Store(address : Byte*, value : ValueTuple`3) was skipped since it collides with above method
        # Method Store(address : SByte*, value : ValueTuple`3) was skipped since it collides with above method
        # Method Store(address : Int16*, value : ValueTuple`3) was skipped since it collides with above method
        # Method Store(address : UInt16*, value : ValueTuple`3) was skipped since it collides with above method
        # Method Store(address : Int32*, value : ValueTuple`3) was skipped since it collides with above method
        # Method Store(address : UInt32*, value : ValueTuple`3) was skipped since it collides with above method
        # Method Store(address : Byte*, value : ValueTuple`4) was skipped since it collides with above method
        # Method Store(address : SByte*, value : ValueTuple`4) was skipped since it collides with above method
        # Method Store(address : Int16*, value : ValueTuple`4) was skipped since it collides with above method
        # Method Store(address : UInt16*, value : ValueTuple`4) was skipped since it collides with above method
        # Method Store(address : Int32*, value : ValueTuple`4) was skipped since it collides with above method
        # Method Store(address : UInt32*, value : ValueTuple`4) was skipped since it collides with above method

    # Skipped StoreSelectedScalar due to it being static, abstract and generic.

    StoreSelectedScalar : StoreSelectedScalar_MethodGroup
    class StoreSelectedScalar_MethodGroup:
        @typing.overload
        def __call__(self, address: clr.Reference[float], value: Vector64_1[float], index: int) -> None:...
        @typing.overload
        def __call__(self, address: clr.Reference[float], value: Vector128_1[float], index: int) -> None:...
        # Method StoreSelectedScalar(address : Single*, value : Vector128`1, index : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, address: clr.Reference[float], value: ValueTuple_2[Vector64_1[float], Vector64_1[float]], index: int) -> None:...
        @typing.overload
        def __call__(self, address: clr.Reference[float], value: ValueTuple_3[Vector64_1[float], Vector64_1[float], Vector64_1[float]], index: int) -> None:...
        @typing.overload
        def __call__(self, address: clr.Reference[float], value: ValueTuple_4[Vector64_1[float], Vector64_1[float], Vector64_1[float], Vector64_1[float]], index: int) -> None:...
        # Method StoreSelectedScalar(address : Byte*, value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Int16*, value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Int32*, value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : SByte*, value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : UInt16*, value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : UInt32*, value : Vector64`1, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Byte*, value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Int16*, value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Int32*, value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Int64*, value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : SByte*, value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : UInt16*, value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : UInt32*, value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : UInt64*, value : Vector128`1, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Byte*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : SByte*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Int16*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : UInt16*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Int32*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : UInt32*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Byte*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : SByte*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Int16*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : UInt16*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Int32*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : UInt32*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Byte*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : SByte*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Int16*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : UInt16*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : Int32*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method
        # Method StoreSelectedScalar(address : UInt32*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method

    # Skipped StoreVectorAndZip due to it being static, abstract and generic.

    StoreVectorAndZip : StoreVectorAndZip_MethodGroup
    class StoreVectorAndZip_MethodGroup:
        @typing.overload
        def __call__(self, address: clr.Reference[float], value: ValueTuple_2[Vector64_1[float], Vector64_1[float]]) -> None:...
        @typing.overload
        def __call__(self, address: clr.Reference[float], value: ValueTuple_3[Vector64_1[float], Vector64_1[float], Vector64_1[float]]) -> None:...
        @typing.overload
        def __call__(self, address: clr.Reference[float], value: ValueTuple_4[Vector64_1[float], Vector64_1[float], Vector64_1[float], Vector64_1[float]]) -> None:...
        # Method StoreVectorAndZip(address : Byte*, value : ValueTuple`2) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : SByte*, value : ValueTuple`2) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : Int16*, value : ValueTuple`2) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : UInt16*, value : ValueTuple`2) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : Int32*, value : ValueTuple`2) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : UInt32*, value : ValueTuple`2) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : Byte*, value : ValueTuple`3) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : SByte*, value : ValueTuple`3) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : Int16*, value : ValueTuple`3) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : UInt16*, value : ValueTuple`3) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : Int32*, value : ValueTuple`3) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : UInt32*, value : ValueTuple`3) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : Byte*, value : ValueTuple`4) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : SByte*, value : ValueTuple`4) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : Int16*, value : ValueTuple`4) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : UInt16*, value : ValueTuple`4) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : Int32*, value : ValueTuple`4) was skipped since it collides with above method
        # Method StoreVectorAndZip(address : UInt32*, value : ValueTuple`4) was skipped since it collides with above method

    # Skipped Subtract due to it being static, abstract and generic.

    Subtract : Subtract_MethodGroup
    class Subtract_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Subtract(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Subtract(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Subtract(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Subtract(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Subtract(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Subtract(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Subtract(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped SubtractHighNarrowingLower due to it being static, abstract and generic.

    SubtractHighNarrowingLower : SubtractHighNarrowingLower_MethodGroup
    class SubtractHighNarrowingLower_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector64_1[int]:...
        # Method SubtractHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped SubtractHighNarrowingUpper due to it being static, abstract and generic.

    SubtractHighNarrowingUpper : SubtractHighNarrowingUpper_MethodGroup
    class SubtractHighNarrowingUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method SubtractHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped SubtractRoundedHighNarrowingLower due to it being static, abstract and generic.

    SubtractRoundedHighNarrowingLower : SubtractRoundedHighNarrowingLower_MethodGroup
    class SubtractRoundedHighNarrowingLower_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector64_1[int]:...
        # Method SubtractRoundedHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingLower(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped SubtractRoundedHighNarrowingUpper due to it being static, abstract and generic.

    SubtractRoundedHighNarrowingUpper : SubtractRoundedHighNarrowingUpper_MethodGroup
    class SubtractRoundedHighNarrowingUpper_MethodGroup:
        def __call__(self, lower: Vector64_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method SubtractRoundedHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingUpper(lower : Vector64`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped SubtractSaturate due to it being static, abstract and generic.

    SubtractSaturate : SubtractSaturate_MethodGroup
    class SubtractSaturate_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method SubtractSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method SubtractSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped SubtractSaturateScalar due to it being static, abstract and generic.

    SubtractSaturateScalar : SubtractSaturateScalar_MethodGroup
    class SubtractSaturateScalar_MethodGroup:
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method SubtractSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped SubtractScalar due to it being static, abstract and generic.

    SubtractScalar : SubtractScalar_MethodGroup
    class SubtractScalar_MethodGroup:
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method SubtractScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method SubtractScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method SubtractScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped SubtractWideningLower due to it being static, abstract and generic.

    SubtractWideningLower : SubtractWideningLower_MethodGroup
    class SubtractWideningLower_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method SubtractWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method SubtractWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method SubtractWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method SubtractWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method SubtractWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method SubtractWideningLower(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method SubtractWideningLower(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method SubtractWideningLower(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method SubtractWideningLower(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method
        # Method SubtractWideningLower(left : Vector128`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped SubtractWideningUpper due to it being static, abstract and generic.

    SubtractWideningUpper : SubtractWideningUpper_MethodGroup
    class SubtractWideningUpper_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method SubtractWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method SubtractWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped VectorTableLookup due to it being static, abstract and generic.

    VectorTableLookup : VectorTableLookup_MethodGroup
    class VectorTableLookup_MethodGroup:
        @typing.overload
        def __call__(self, table: Vector128_1[int], byteIndexes: Vector64_1[int]) -> Vector64_1[int]:...
        # Method VectorTableLookup(table : Vector128`1, byteIndexes : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, table: ValueTuple_2[Vector128_1[int], Vector128_1[int]], byteIndexes: Vector64_1[int]) -> Vector64_1[int]:...
        # Method VectorTableLookup(table : ValueTuple`2, byteIndexes : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, table: ValueTuple_3[Vector128_1[int], Vector128_1[int], Vector128_1[int]], byteIndexes: Vector64_1[int]) -> Vector64_1[int]:...
        # Method VectorTableLookup(table : ValueTuple`3, byteIndexes : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, table: ValueTuple_4[Vector128_1[int], Vector128_1[int], Vector128_1[int], Vector128_1[int]], byteIndexes: Vector64_1[int]) -> Vector64_1[int]:...
        # Method VectorTableLookup(table : ValueTuple`4, byteIndexes : Vector64`1) was skipped since it collides with above method

    # Skipped VectorTableLookupExtension due to it being static, abstract and generic.

    VectorTableLookupExtension : VectorTableLookupExtension_MethodGroup
    class VectorTableLookupExtension_MethodGroup:
        @typing.overload
        def __call__(self, defaultValues: Vector64_1[int], table: Vector128_1[int], byteIndexes: Vector64_1[int]) -> Vector64_1[int]:...
        # Method VectorTableLookupExtension(defaultValues : Vector64`1, table : Vector128`1, byteIndexes : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, defaultValues: Vector64_1[int], table: ValueTuple_2[Vector128_1[int], Vector128_1[int]], byteIndexes: Vector64_1[int]) -> Vector64_1[int]:...
        # Method VectorTableLookupExtension(defaultValues : Vector64`1, table : ValueTuple`2, byteIndexes : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, defaultValues: Vector64_1[int], table: ValueTuple_3[Vector128_1[int], Vector128_1[int], Vector128_1[int]], byteIndexes: Vector64_1[int]) -> Vector64_1[int]:...
        # Method VectorTableLookupExtension(defaultValues : Vector64`1, table : ValueTuple`3, byteIndexes : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, defaultValues: Vector64_1[int], table: ValueTuple_4[Vector128_1[int], Vector128_1[int], Vector128_1[int], Vector128_1[int]], byteIndexes: Vector64_1[int]) -> Vector64_1[int]:...
        # Method VectorTableLookupExtension(defaultValues : Vector64`1, table : ValueTuple`4, byteIndexes : Vector64`1) was skipped since it collides with above method

    # Skipped Xor due to it being static, abstract and generic.

    Xor : Xor_MethodGroup
    class Xor_MethodGroup:
        @typing.overload
        def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
        # Method Xor(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Xor(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Xor(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Xor(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Xor(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Xor(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Xor(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Xor(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
        # Method Xor(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped ZeroExtendWideningLower due to it being static, abstract and generic.

    ZeroExtendWideningLower : ZeroExtendWideningLower_MethodGroup
    class ZeroExtendWideningLower_MethodGroup:
        def __call__(self, value: Vector64_1[int]) -> Vector128_1[int]:...
        # Method ZeroExtendWideningLower(value : Vector64`1) was skipped since it collides with above method
        # Method ZeroExtendWideningLower(value : Vector64`1) was skipped since it collides with above method
        # Method ZeroExtendWideningLower(value : Vector64`1) was skipped since it collides with above method
        # Method ZeroExtendWideningLower(value : Vector64`1) was skipped since it collides with above method
        # Method ZeroExtendWideningLower(value : Vector64`1) was skipped since it collides with above method

    # Skipped ZeroExtendWideningUpper due to it being static, abstract and generic.

    ZeroExtendWideningUpper : ZeroExtendWideningUpper_MethodGroup
    class ZeroExtendWideningUpper_MethodGroup:
        def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
        # Method ZeroExtendWideningUpper(value : Vector128`1) was skipped since it collides with above method
        # Method ZeroExtendWideningUpper(value : Vector128`1) was skipped since it collides with above method
        # Method ZeroExtendWideningUpper(value : Vector128`1) was skipped since it collides with above method
        # Method ZeroExtendWideningUpper(value : Vector128`1) was skipped since it collides with above method
        # Method ZeroExtendWideningUpper(value : Vector128`1) was skipped since it collides with above method


    class Arm64(ArmBase.Arm64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...
        @staticmethod
        def AbsoluteCompareGreaterThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def AbsoluteCompareGreaterThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def AbsoluteCompareLessThan(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def AbsoluteCompareLessThanOrEqual(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def AbsoluteDifference(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def AbsSaturate(value: Vector128_1[int]) -> Vector128_1[int]: ...
        @staticmethod
        def AbsScalar(value: Vector64_1[int]) -> Vector64_1[int]: ...
        @staticmethod
        def Add(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def Ceiling(value: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def ConvertToDoubleUpper(value: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def ConvertToInt64RoundAwayFromZero(value: Vector128_1[float]) -> Vector128_1[int]: ...
        @staticmethod
        def ConvertToInt64RoundAwayFromZeroScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
        @staticmethod
        def ConvertToInt64RoundToEven(value: Vector128_1[float]) -> Vector128_1[int]: ...
        @staticmethod
        def ConvertToInt64RoundToEvenScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
        @staticmethod
        def ConvertToInt64RoundToNegativeInfinity(value: Vector128_1[float]) -> Vector128_1[int]: ...
        @staticmethod
        def ConvertToInt64RoundToNegativeInfinityScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
        @staticmethod
        def ConvertToInt64RoundToPositiveInfinity(value: Vector128_1[float]) -> Vector128_1[int]: ...
        @staticmethod
        def ConvertToInt64RoundToPositiveInfinityScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
        @staticmethod
        def ConvertToInt64RoundToZero(value: Vector128_1[float]) -> Vector128_1[int]: ...
        @staticmethod
        def ConvertToInt64RoundToZeroScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
        @staticmethod
        def ConvertToSingleLower(value: Vector128_1[float]) -> Vector64_1[float]: ...
        @staticmethod
        def ConvertToSingleRoundToOddLower(value: Vector128_1[float]) -> Vector64_1[float]: ...
        @staticmethod
        def ConvertToSingleRoundToOddUpper(lower: Vector64_1[float], value: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def ConvertToSingleUpper(lower: Vector64_1[float], value: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def ConvertToUInt64RoundAwayFromZero(value: Vector128_1[float]) -> Vector128_1[int]: ...
        @staticmethod
        def ConvertToUInt64RoundAwayFromZeroScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
        @staticmethod
        def ConvertToUInt64RoundToEven(value: Vector128_1[float]) -> Vector128_1[int]: ...
        @staticmethod
        def ConvertToUInt64RoundToEvenScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
        @staticmethod
        def ConvertToUInt64RoundToNegativeInfinity(value: Vector128_1[float]) -> Vector128_1[int]: ...
        @staticmethod
        def ConvertToUInt64RoundToNegativeInfinityScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
        @staticmethod
        def ConvertToUInt64RoundToPositiveInfinity(value: Vector128_1[float]) -> Vector128_1[int]: ...
        @staticmethod
        def ConvertToUInt64RoundToPositiveInfinityScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
        @staticmethod
        def ConvertToUInt64RoundToZero(value: Vector128_1[float]) -> Vector128_1[int]: ...
        @staticmethod
        def ConvertToUInt64RoundToZeroScalar(value: Vector64_1[float]) -> Vector64_1[int]: ...
        @staticmethod
        def Floor(value: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def FusedMultiplyAdd(addend: Vector128_1[float], left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def FusedMultiplySubtract(minuend: Vector128_1[float], left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def Max(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def MaxNumber(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def MaxNumberAcross(value: Vector128_1[float]) -> Vector64_1[float]: ...
        @staticmethod
        def Min(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def MinNumber(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def MinNumberAcross(value: Vector128_1[float]) -> Vector64_1[float]: ...
        @staticmethod
        def Multiply(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def MultiplyByScalar(left: Vector128_1[float], right: Vector64_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def MultiplyBySelectedScalar(left: Vector128_1[float], right: Vector128_1[float], rightIndex: int) -> Vector128_1[float]: ...
        @staticmethod
        def MultiplyExtendedByScalar(left: Vector128_1[float], right: Vector64_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def MultiplyScalarBySelectedScalar(left: Vector64_1[float], right: Vector128_1[float], rightIndex: int) -> Vector64_1[float]: ...
        @staticmethod
        def NegateSaturate(value: Vector128_1[int]) -> Vector128_1[int]: ...
        @staticmethod
        def NegateScalar(value: Vector64_1[int]) -> Vector64_1[int]: ...
        @staticmethod
        def ReciprocalEstimate(value: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def ReciprocalSquareRootEstimate(value: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def ReciprocalSquareRootStep(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def ReciprocalStep(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def RoundAwayFromZero(value: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def RoundToNearest(value: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def RoundToNegativeInfinity(value: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def RoundToPositiveInfinity(value: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def RoundToZero(value: Vector128_1[float]) -> Vector128_1[float]: ...
        @staticmethod
        def Subtract(left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]: ...
        # Skipped Abs due to it being static, abstract and generic.

        Abs : Abs_MethodGroup
        class Abs_MethodGroup:
            def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
            # Method Abs(value : Vector128`1) was skipped since it collides with above method

        # Skipped AbsoluteCompareGreaterThanOrEqualScalar due to it being static, abstract and generic.

        AbsoluteCompareGreaterThanOrEqualScalar : AbsoluteCompareGreaterThanOrEqualScalar_MethodGroup
        class AbsoluteCompareGreaterThanOrEqualScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method AbsoluteCompareGreaterThanOrEqualScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped AbsoluteCompareGreaterThanScalar due to it being static, abstract and generic.

        AbsoluteCompareGreaterThanScalar : AbsoluteCompareGreaterThanScalar_MethodGroup
        class AbsoluteCompareGreaterThanScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method AbsoluteCompareGreaterThanScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped AbsoluteCompareLessThanOrEqualScalar due to it being static, abstract and generic.

        AbsoluteCompareLessThanOrEqualScalar : AbsoluteCompareLessThanOrEqualScalar_MethodGroup
        class AbsoluteCompareLessThanOrEqualScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method AbsoluteCompareLessThanOrEqualScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped AbsoluteCompareLessThanScalar due to it being static, abstract and generic.

        AbsoluteCompareLessThanScalar : AbsoluteCompareLessThanScalar_MethodGroup
        class AbsoluteCompareLessThanScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method AbsoluteCompareLessThanScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped AbsoluteDifferenceScalar due to it being static, abstract and generic.

        AbsoluteDifferenceScalar : AbsoluteDifferenceScalar_MethodGroup
        class AbsoluteDifferenceScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method AbsoluteDifferenceScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped AbsSaturateScalar due to it being static, abstract and generic.

        AbsSaturateScalar : AbsSaturateScalar_MethodGroup
        class AbsSaturateScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
            # Method AbsSaturateScalar(value : Vector64`1) was skipped since it collides with above method
            # Method AbsSaturateScalar(value : Vector64`1) was skipped since it collides with above method
            # Method AbsSaturateScalar(value : Vector64`1) was skipped since it collides with above method

        # Skipped AddAcross due to it being static, abstract and generic.

        AddAcross : AddAcross_MethodGroup
        class AddAcross_MethodGroup:
            @typing.overload
            def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
            # Method AddAcross(value : Vector64`1) was skipped since it collides with above method
            # Method AddAcross(value : Vector64`1) was skipped since it collides with above method
            # Method AddAcross(value : Vector64`1) was skipped since it collides with above method
            @typing.overload
            def __call__(self, value: Vector128_1[int]) -> Vector64_1[int]:...
            # Method AddAcross(value : Vector128`1) was skipped since it collides with above method
            # Method AddAcross(value : Vector128`1) was skipped since it collides with above method
            # Method AddAcross(value : Vector128`1) was skipped since it collides with above method
            # Method AddAcross(value : Vector128`1) was skipped since it collides with above method
            # Method AddAcross(value : Vector128`1) was skipped since it collides with above method

        # Skipped AddAcrossWidening due to it being static, abstract and generic.

        AddAcrossWidening : AddAcrossWidening_MethodGroup
        class AddAcrossWidening_MethodGroup:
            @typing.overload
            def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
            # Method AddAcrossWidening(value : Vector64`1) was skipped since it collides with above method
            # Method AddAcrossWidening(value : Vector64`1) was skipped since it collides with above method
            # Method AddAcrossWidening(value : Vector64`1) was skipped since it collides with above method
            @typing.overload
            def __call__(self, value: Vector128_1[int]) -> Vector64_1[int]:...
            # Method AddAcrossWidening(value : Vector128`1) was skipped since it collides with above method
            # Method AddAcrossWidening(value : Vector128`1) was skipped since it collides with above method
            # Method AddAcrossWidening(value : Vector128`1) was skipped since it collides with above method
            # Method AddAcrossWidening(value : Vector128`1) was skipped since it collides with above method
            # Method AddAcrossWidening(value : Vector128`1) was skipped since it collides with above method

        # Skipped AddPairwise due to it being static, abstract and generic.

        AddPairwise : AddPairwise_MethodGroup
        class AddPairwise_MethodGroup:
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method AddPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method AddPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method AddPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method AddPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method AddPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method AddPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method AddPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method AddPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method AddPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped AddPairwiseScalar due to it being static, abstract and generic.

        AddPairwiseScalar : AddPairwiseScalar_MethodGroup
        class AddPairwiseScalar_MethodGroup:
            @typing.overload
            def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, value: Vector128_1[float]) -> Vector64_1[float]:...
            # Method AddPairwiseScalar(value : Vector128`1) was skipped since it collides with above method
            # Method AddPairwiseScalar(value : Vector128`1) was skipped since it collides with above method

        # Skipped AddSaturate due to it being static, abstract and generic.

        AddSaturate : AddSaturate_MethodGroup
        class AddSaturate_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
            # Method AddSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturate(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            @typing.overload
            def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
            # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method AddSaturate(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped AddSaturateScalar due to it being static, abstract and generic.

        AddSaturateScalar : AddSaturateScalar_MethodGroup
        class AddSaturateScalar_MethodGroup:
            def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
            # Method AddSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method AddSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped CompareEqual due to it being static, abstract and generic.

        CompareEqual : CompareEqual_MethodGroup
        class CompareEqual_MethodGroup:
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method CompareEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped CompareEqualScalar due to it being static, abstract and generic.

        CompareEqualScalar : CompareEqualScalar_MethodGroup
        class CompareEqualScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method CompareEqualScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method CompareEqualScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method CompareEqualScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped CompareGreaterThan due to it being static, abstract and generic.

        CompareGreaterThan : CompareGreaterThan_MethodGroup
        class CompareGreaterThan_MethodGroup:
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method CompareGreaterThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method CompareGreaterThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped CompareGreaterThanOrEqual due to it being static, abstract and generic.

        CompareGreaterThanOrEqual : CompareGreaterThanOrEqual_MethodGroup
        class CompareGreaterThanOrEqual_MethodGroup:
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method CompareGreaterThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method CompareGreaterThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped CompareGreaterThanOrEqualScalar due to it being static, abstract and generic.

        CompareGreaterThanOrEqualScalar : CompareGreaterThanOrEqualScalar_MethodGroup
        class CompareGreaterThanOrEqualScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method CompareGreaterThanOrEqualScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method CompareGreaterThanOrEqualScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method CompareGreaterThanOrEqualScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped CompareGreaterThanScalar due to it being static, abstract and generic.

        CompareGreaterThanScalar : CompareGreaterThanScalar_MethodGroup
        class CompareGreaterThanScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method CompareGreaterThanScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method CompareGreaterThanScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method CompareGreaterThanScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped CompareLessThan due to it being static, abstract and generic.

        CompareLessThan : CompareLessThan_MethodGroup
        class CompareLessThan_MethodGroup:
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method CompareLessThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method CompareLessThan(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped CompareLessThanOrEqual due to it being static, abstract and generic.

        CompareLessThanOrEqual : CompareLessThanOrEqual_MethodGroup
        class CompareLessThanOrEqual_MethodGroup:
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method CompareLessThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method CompareLessThanOrEqual(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped CompareLessThanOrEqualScalar due to it being static, abstract and generic.

        CompareLessThanOrEqualScalar : CompareLessThanOrEqualScalar_MethodGroup
        class CompareLessThanOrEqualScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method CompareLessThanOrEqualScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method CompareLessThanOrEqualScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method CompareLessThanOrEqualScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped CompareLessThanScalar due to it being static, abstract and generic.

        CompareLessThanScalar : CompareLessThanScalar_MethodGroup
        class CompareLessThanScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method CompareLessThanScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method CompareLessThanScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method CompareLessThanScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped CompareTest due to it being static, abstract and generic.

        CompareTest : CompareTest_MethodGroup
        class CompareTest_MethodGroup:
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method CompareTest(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method CompareTest(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped CompareTestScalar due to it being static, abstract and generic.

        CompareTestScalar : CompareTestScalar_MethodGroup
        class CompareTestScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method CompareTestScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method CompareTestScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped ConvertToDouble due to it being static, abstract and generic.

        ConvertToDouble : ConvertToDouble_MethodGroup
        class ConvertToDouble_MethodGroup:
            @typing.overload
            def __call__(self, value: Vector64_1[float]) -> Vector128_1[float]:...
            @typing.overload
            def __call__(self, value: Vector128_1[int]) -> Vector128_1[float]:...
            # Method ConvertToDouble(value : Vector128`1) was skipped since it collides with above method

        # Skipped ConvertToDoubleScalar due to it being static, abstract and generic.

        ConvertToDoubleScalar : ConvertToDoubleScalar_MethodGroup
        class ConvertToDoubleScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int]) -> Vector64_1[float]:...
            # Method ConvertToDoubleScalar(value : Vector64`1) was skipped since it collides with above method

        # Skipped Divide due to it being static, abstract and generic.

        Divide : Divide_MethodGroup
        class Divide_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method Divide(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped DuplicateSelectedScalarToVector128 due to it being static, abstract and generic.

        DuplicateSelectedScalarToVector128 : DuplicateSelectedScalarToVector128_MethodGroup
        class DuplicateSelectedScalarToVector128_MethodGroup:
            def __call__(self, value: Vector128_1[float], index: int) -> Vector128_1[float]:...
            # Method DuplicateSelectedScalarToVector128(value : Vector128`1, index : Byte) was skipped since it collides with above method
            # Method DuplicateSelectedScalarToVector128(value : Vector128`1, index : Byte) was skipped since it collides with above method

        # Skipped DuplicateToVector128 due to it being static, abstract and generic.

        DuplicateToVector128 : DuplicateToVector128_MethodGroup
        class DuplicateToVector128_MethodGroup:
            def __call__(self, value: float) -> Vector128_1[float]:...
            # Method DuplicateToVector128(value : Int64) was skipped since it collides with above method
            # Method DuplicateToVector128(value : UInt64) was skipped since it collides with above method

        # Skipped ExtractNarrowingSaturateScalar due to it being static, abstract and generic.

        ExtractNarrowingSaturateScalar : ExtractNarrowingSaturateScalar_MethodGroup
        class ExtractNarrowingSaturateScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
            # Method ExtractNarrowingSaturateScalar(value : Vector64`1) was skipped since it collides with above method
            # Method ExtractNarrowingSaturateScalar(value : Vector64`1) was skipped since it collides with above method
            # Method ExtractNarrowingSaturateScalar(value : Vector64`1) was skipped since it collides with above method
            # Method ExtractNarrowingSaturateScalar(value : Vector64`1) was skipped since it collides with above method
            # Method ExtractNarrowingSaturateScalar(value : Vector64`1) was skipped since it collides with above method

        # Skipped ExtractNarrowingSaturateUnsignedScalar due to it being static, abstract and generic.

        ExtractNarrowingSaturateUnsignedScalar : ExtractNarrowingSaturateUnsignedScalar_MethodGroup
        class ExtractNarrowingSaturateUnsignedScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
            # Method ExtractNarrowingSaturateUnsignedScalar(value : Vector64`1) was skipped since it collides with above method
            # Method ExtractNarrowingSaturateUnsignedScalar(value : Vector64`1) was skipped since it collides with above method

        # Skipped FusedMultiplyAddByScalar due to it being static, abstract and generic.

        FusedMultiplyAddByScalar : FusedMultiplyAddByScalar_MethodGroup
        class FusedMultiplyAddByScalar_MethodGroup:
            @typing.overload
            def __call__(self, addend: Vector64_1[float], left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, addend: Vector128_1[float], left: Vector128_1[float], right: Vector64_1[float]) -> Vector128_1[float]:...
            # Method FusedMultiplyAddByScalar(addend : Vector128`1, left : Vector128`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped FusedMultiplyAddBySelectedScalar due to it being static, abstract and generic.

        FusedMultiplyAddBySelectedScalar : FusedMultiplyAddBySelectedScalar_MethodGroup
        class FusedMultiplyAddBySelectedScalar_MethodGroup:
            @typing.overload
            def __call__(self, addend: Vector64_1[float], left: Vector64_1[float], right: Vector64_1[float], rightIndex: int) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, addend: Vector64_1[float], left: Vector64_1[float], right: Vector128_1[float], rightIndex: int) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, addend: Vector128_1[float], left: Vector128_1[float], right: Vector128_1[float], rightIndex: int) -> Vector128_1[float]:...
            @typing.overload
            def __call__(self, addend: Vector128_1[float], left: Vector128_1[float], right: Vector64_1[float], rightIndex: int) -> Vector128_1[float]:...
            # Method FusedMultiplyAddBySelectedScalar(addend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

        # Skipped FusedMultiplyAddScalarBySelectedScalar due to it being static, abstract and generic.

        FusedMultiplyAddScalarBySelectedScalar : FusedMultiplyAddScalarBySelectedScalar_MethodGroup
        class FusedMultiplyAddScalarBySelectedScalar_MethodGroup:
            @typing.overload
            def __call__(self, addend: Vector64_1[float], left: Vector64_1[float], right: Vector128_1[float], rightIndex: int) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, addend: Vector64_1[float], left: Vector64_1[float], right: Vector64_1[float], rightIndex: int) -> Vector64_1[float]:...
            # Method FusedMultiplyAddScalarBySelectedScalar(addend : Vector64`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

        # Skipped FusedMultiplySubtractByScalar due to it being static, abstract and generic.

        FusedMultiplySubtractByScalar : FusedMultiplySubtractByScalar_MethodGroup
        class FusedMultiplySubtractByScalar_MethodGroup:
            @typing.overload
            def __call__(self, minuend: Vector64_1[float], left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, minuend: Vector128_1[float], left: Vector128_1[float], right: Vector64_1[float]) -> Vector128_1[float]:...
            # Method FusedMultiplySubtractByScalar(minuend : Vector128`1, left : Vector128`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped FusedMultiplySubtractBySelectedScalar due to it being static, abstract and generic.

        FusedMultiplySubtractBySelectedScalar : FusedMultiplySubtractBySelectedScalar_MethodGroup
        class FusedMultiplySubtractBySelectedScalar_MethodGroup:
            @typing.overload
            def __call__(self, minuend: Vector64_1[float], left: Vector64_1[float], right: Vector64_1[float], rightIndex: int) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, minuend: Vector64_1[float], left: Vector64_1[float], right: Vector128_1[float], rightIndex: int) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, minuend: Vector128_1[float], left: Vector128_1[float], right: Vector128_1[float], rightIndex: int) -> Vector128_1[float]:...
            @typing.overload
            def __call__(self, minuend: Vector128_1[float], left: Vector128_1[float], right: Vector64_1[float], rightIndex: int) -> Vector128_1[float]:...
            # Method FusedMultiplySubtractBySelectedScalar(minuend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

        # Skipped FusedMultiplySubtractScalarBySelectedScalar due to it being static, abstract and generic.

        FusedMultiplySubtractScalarBySelectedScalar : FusedMultiplySubtractScalarBySelectedScalar_MethodGroup
        class FusedMultiplySubtractScalarBySelectedScalar_MethodGroup:
            @typing.overload
            def __call__(self, minuend: Vector64_1[float], left: Vector64_1[float], right: Vector128_1[float], rightIndex: int) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, minuend: Vector64_1[float], left: Vector64_1[float], right: Vector64_1[float], rightIndex: int) -> Vector64_1[float]:...
            # Method FusedMultiplySubtractScalarBySelectedScalar(minuend : Vector64`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

        # Skipped InsertSelectedScalar due to it being static, abstract and generic.

        InsertSelectedScalar : InsertSelectedScalar_MethodGroup
        class InsertSelectedScalar_MethodGroup:
            @typing.overload
            def __call__(self, result: Vector64_1[float], resultIndex: int, value: Vector64_1[float], valueIndex: int) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, result: Vector64_1[float], resultIndex: int, value: Vector128_1[float], valueIndex: int) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, result: Vector128_1[float], resultIndex: int, value: Vector128_1[float], valueIndex: int) -> Vector128_1[float]:...
            @typing.overload
            def __call__(self, result: Vector128_1[float], resultIndex: int, value: Vector64_1[float], valueIndex: int) -> Vector128_1[float]:...
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector64`1, resultIndex : Byte, value : Vector64`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector64`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector64`1, resultIndex : Byte, value : Vector64`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector64`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector64`1, resultIndex : Byte, value : Vector64`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector64`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector64`1, resultIndex : Byte, value : Vector64`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector64`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector64`1, resultIndex : Byte, value : Vector64`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector64`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector64`1, resultIndex : Byte, value : Vector64`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector64`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector64`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector64`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector64`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector64`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector64`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector64`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method
            # Method InsertSelectedScalar(result : Vector128`1, resultIndex : Byte, value : Vector128`1, valueIndex : Byte) was skipped since it collides with above method

        # Skipped Load2xVector128 due to it being static, abstract and generic.

        Load2xVector128 : Load2xVector128_MethodGroup
        class Load2xVector128_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_2[Vector128_1[float], Vector128_1[float]]:...
            # Method Load2xVector128(address : Double*) was skipped since it collides with above method
            # Method Load2xVector128(address : Byte*) was skipped since it collides with above method
            # Method Load2xVector128(address : SByte*) was skipped since it collides with above method
            # Method Load2xVector128(address : Int16*) was skipped since it collides with above method
            # Method Load2xVector128(address : UInt16*) was skipped since it collides with above method
            # Method Load2xVector128(address : Int32*) was skipped since it collides with above method
            # Method Load2xVector128(address : UInt32*) was skipped since it collides with above method
            # Method Load2xVector128(address : Int64*) was skipped since it collides with above method
            # Method Load2xVector128(address : UInt64*) was skipped since it collides with above method

        # Skipped Load2xVector128AndUnzip due to it being static, abstract and generic.

        Load2xVector128AndUnzip : Load2xVector128AndUnzip_MethodGroup
        class Load2xVector128AndUnzip_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_2[Vector128_1[float], Vector128_1[float]]:...
            # Method Load2xVector128AndUnzip(address : Double*) was skipped since it collides with above method
            # Method Load2xVector128AndUnzip(address : Byte*) was skipped since it collides with above method
            # Method Load2xVector128AndUnzip(address : SByte*) was skipped since it collides with above method
            # Method Load2xVector128AndUnzip(address : Int16*) was skipped since it collides with above method
            # Method Load2xVector128AndUnzip(address : UInt16*) was skipped since it collides with above method
            # Method Load2xVector128AndUnzip(address : Int32*) was skipped since it collides with above method
            # Method Load2xVector128AndUnzip(address : UInt32*) was skipped since it collides with above method
            # Method Load2xVector128AndUnzip(address : Int64*) was skipped since it collides with above method
            # Method Load2xVector128AndUnzip(address : UInt64*) was skipped since it collides with above method

        # Skipped Load3xVector128 due to it being static, abstract and generic.

        Load3xVector128 : Load3xVector128_MethodGroup
        class Load3xVector128_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_3[Vector128_1[float], Vector128_1[float], Vector128_1[float]]:...
            # Method Load3xVector128(address : Double*) was skipped since it collides with above method
            # Method Load3xVector128(address : Byte*) was skipped since it collides with above method
            # Method Load3xVector128(address : SByte*) was skipped since it collides with above method
            # Method Load3xVector128(address : Int16*) was skipped since it collides with above method
            # Method Load3xVector128(address : UInt16*) was skipped since it collides with above method
            # Method Load3xVector128(address : Int32*) was skipped since it collides with above method
            # Method Load3xVector128(address : UInt32*) was skipped since it collides with above method
            # Method Load3xVector128(address : Int64*) was skipped since it collides with above method
            # Method Load3xVector128(address : UInt64*) was skipped since it collides with above method

        # Skipped Load3xVector128AndUnzip due to it being static, abstract and generic.

        Load3xVector128AndUnzip : Load3xVector128AndUnzip_MethodGroup
        class Load3xVector128AndUnzip_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_3[Vector128_1[float], Vector128_1[float], Vector128_1[float]]:...
            # Method Load3xVector128AndUnzip(address : Double*) was skipped since it collides with above method
            # Method Load3xVector128AndUnzip(address : Byte*) was skipped since it collides with above method
            # Method Load3xVector128AndUnzip(address : SByte*) was skipped since it collides with above method
            # Method Load3xVector128AndUnzip(address : Int16*) was skipped since it collides with above method
            # Method Load3xVector128AndUnzip(address : UInt16*) was skipped since it collides with above method
            # Method Load3xVector128AndUnzip(address : Int32*) was skipped since it collides with above method
            # Method Load3xVector128AndUnzip(address : UInt32*) was skipped since it collides with above method
            # Method Load3xVector128AndUnzip(address : Int64*) was skipped since it collides with above method
            # Method Load3xVector128AndUnzip(address : UInt64*) was skipped since it collides with above method

        # Skipped Load4xVector128 due to it being static, abstract and generic.

        Load4xVector128 : Load4xVector128_MethodGroup
        class Load4xVector128_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_4[Vector128_1[float], Vector128_1[float], Vector128_1[float], Vector128_1[float]]:...
            # Method Load4xVector128(address : Double*) was skipped since it collides with above method
            # Method Load4xVector128(address : Byte*) was skipped since it collides with above method
            # Method Load4xVector128(address : SByte*) was skipped since it collides with above method
            # Method Load4xVector128(address : Int16*) was skipped since it collides with above method
            # Method Load4xVector128(address : UInt16*) was skipped since it collides with above method
            # Method Load4xVector128(address : Int32*) was skipped since it collides with above method
            # Method Load4xVector128(address : UInt32*) was skipped since it collides with above method
            # Method Load4xVector128(address : Int64*) was skipped since it collides with above method
            # Method Load4xVector128(address : UInt64*) was skipped since it collides with above method

        # Skipped Load4xVector128AndUnzip due to it being static, abstract and generic.

        Load4xVector128AndUnzip : Load4xVector128AndUnzip_MethodGroup
        class Load4xVector128AndUnzip_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_4[Vector128_1[float], Vector128_1[float], Vector128_1[float], Vector128_1[float]]:...
            # Method Load4xVector128AndUnzip(address : Double*) was skipped since it collides with above method
            # Method Load4xVector128AndUnzip(address : Byte*) was skipped since it collides with above method
            # Method Load4xVector128AndUnzip(address : SByte*) was skipped since it collides with above method
            # Method Load4xVector128AndUnzip(address : Int16*) was skipped since it collides with above method
            # Method Load4xVector128AndUnzip(address : UInt16*) was skipped since it collides with above method
            # Method Load4xVector128AndUnzip(address : Int32*) was skipped since it collides with above method
            # Method Load4xVector128AndUnzip(address : UInt32*) was skipped since it collides with above method
            # Method Load4xVector128AndUnzip(address : Int64*) was skipped since it collides with above method
            # Method Load4xVector128AndUnzip(address : UInt64*) was skipped since it collides with above method

        # Skipped LoadAndInsertScalar due to it being static, abstract and generic.

        LoadAndInsertScalar : LoadAndInsertScalar_MethodGroup
        class LoadAndInsertScalar_MethodGroup:
            @typing.overload
            def __call__(self, values: ValueTuple_2[Vector128_1[float], Vector128_1[float]], index: int, address: clr.Reference[float]) -> ValueTuple_2[Vector128_1[float], Vector128_1[float]]:...
            # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : Double*) was skipped since it collides with above method
            @typing.overload
            def __call__(self, values: ValueTuple_3[Vector128_1[float], Vector128_1[float], Vector128_1[float]], index: int, address: clr.Reference[float]) -> ValueTuple_3[Vector128_1[float], Vector128_1[float], Vector128_1[float]]:...
            # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : Double*) was skipped since it collides with above method
            @typing.overload
            def __call__(self, values: ValueTuple_4[Vector128_1[float], Vector128_1[float], Vector128_1[float], Vector128_1[float]], index: int, address: clr.Reference[float]) -> ValueTuple_4[Vector128_1[float], Vector128_1[float], Vector128_1[float], Vector128_1[float]]:...
            # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : Double*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : Byte*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : SByte*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : Int16*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : UInt16*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : Int32*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : UInt32*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : Int64*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`2, index : Byte, address : UInt64*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : Byte*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : SByte*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : Int16*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : UInt16*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : Int32*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : UInt32*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : Int64*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`3, index : Byte, address : UInt64*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : Byte*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : SByte*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : Int16*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : UInt16*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : Int32*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : UInt32*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : Int64*) was skipped since it collides with above method
            # Method LoadAndInsertScalar(values : ValueTuple`4, index : Byte, address : UInt64*) was skipped since it collides with above method

        # Skipped LoadAndReplicateToVector128 due to it being static, abstract and generic.

        LoadAndReplicateToVector128 : LoadAndReplicateToVector128_MethodGroup
        class LoadAndReplicateToVector128_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> Vector128_1[float]:...
            # Method LoadAndReplicateToVector128(address : Int64*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128(address : UInt64*) was skipped since it collides with above method

        # Skipped LoadAndReplicateToVector128x2 due to it being static, abstract and generic.

        LoadAndReplicateToVector128x2 : LoadAndReplicateToVector128x2_MethodGroup
        class LoadAndReplicateToVector128x2_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_2[Vector128_1[float], Vector128_1[float]]:...
            # Method LoadAndReplicateToVector128x2(address : Double*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x2(address : Byte*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x2(address : SByte*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x2(address : Int16*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x2(address : UInt16*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x2(address : Int32*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x2(address : UInt32*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x2(address : Int64*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x2(address : UInt64*) was skipped since it collides with above method

        # Skipped LoadAndReplicateToVector128x3 due to it being static, abstract and generic.

        LoadAndReplicateToVector128x3 : LoadAndReplicateToVector128x3_MethodGroup
        class LoadAndReplicateToVector128x3_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_3[Vector128_1[float], Vector128_1[float], Vector128_1[float]]:...
            # Method LoadAndReplicateToVector128x3(address : Double*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x3(address : Byte*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x3(address : SByte*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x3(address : Int16*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x3(address : UInt16*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x3(address : Int32*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x3(address : UInt32*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x3(address : Int64*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x3(address : UInt64*) was skipped since it collides with above method

        # Skipped LoadAndReplicateToVector128x4 due to it being static, abstract and generic.

        LoadAndReplicateToVector128x4 : LoadAndReplicateToVector128x4_MethodGroup
        class LoadAndReplicateToVector128x4_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_4[Vector128_1[float], Vector128_1[float], Vector128_1[float], Vector128_1[float]]:...
            # Method LoadAndReplicateToVector128x4(address : Double*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x4(address : Byte*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x4(address : SByte*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x4(address : Int16*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x4(address : UInt16*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x4(address : Int32*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x4(address : UInt32*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x4(address : Int64*) was skipped since it collides with above method
            # Method LoadAndReplicateToVector128x4(address : UInt64*) was skipped since it collides with above method

        # Skipped LoadPairScalarVector64 due to it being static, abstract and generic.

        LoadPairScalarVector64 : LoadPairScalarVector64_MethodGroup
        class LoadPairScalarVector64_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_2[Vector64_1[float], Vector64_1[float]]:...
            # Method LoadPairScalarVector64(address : Int32*) was skipped since it collides with above method
            # Method LoadPairScalarVector64(address : UInt32*) was skipped since it collides with above method

        # Skipped LoadPairScalarVector64NonTemporal due to it being static, abstract and generic.

        LoadPairScalarVector64NonTemporal : LoadPairScalarVector64NonTemporal_MethodGroup
        class LoadPairScalarVector64NonTemporal_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_2[Vector64_1[float], Vector64_1[float]]:...
            # Method LoadPairScalarVector64NonTemporal(address : Int32*) was skipped since it collides with above method
            # Method LoadPairScalarVector64NonTemporal(address : UInt32*) was skipped since it collides with above method

        # Skipped LoadPairVector128 due to it being static, abstract and generic.

        LoadPairVector128 : LoadPairVector128_MethodGroup
        class LoadPairVector128_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_2[Vector128_1[float], Vector128_1[float]]:...
            # Method LoadPairVector128(address : Single*) was skipped since it collides with above method
            # Method LoadPairVector128(address : Byte*) was skipped since it collides with above method
            # Method LoadPairVector128(address : Int16*) was skipped since it collides with above method
            # Method LoadPairVector128(address : Int32*) was skipped since it collides with above method
            # Method LoadPairVector128(address : Int64*) was skipped since it collides with above method
            # Method LoadPairVector128(address : SByte*) was skipped since it collides with above method
            # Method LoadPairVector128(address : UInt16*) was skipped since it collides with above method
            # Method LoadPairVector128(address : UInt32*) was skipped since it collides with above method
            # Method LoadPairVector128(address : UInt64*) was skipped since it collides with above method

        # Skipped LoadPairVector128NonTemporal due to it being static, abstract and generic.

        LoadPairVector128NonTemporal : LoadPairVector128NonTemporal_MethodGroup
        class LoadPairVector128NonTemporal_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_2[Vector128_1[float], Vector128_1[float]]:...
            # Method LoadPairVector128NonTemporal(address : Single*) was skipped since it collides with above method
            # Method LoadPairVector128NonTemporal(address : Byte*) was skipped since it collides with above method
            # Method LoadPairVector128NonTemporal(address : Int16*) was skipped since it collides with above method
            # Method LoadPairVector128NonTemporal(address : Int32*) was skipped since it collides with above method
            # Method LoadPairVector128NonTemporal(address : Int64*) was skipped since it collides with above method
            # Method LoadPairVector128NonTemporal(address : SByte*) was skipped since it collides with above method
            # Method LoadPairVector128NonTemporal(address : UInt16*) was skipped since it collides with above method
            # Method LoadPairVector128NonTemporal(address : UInt32*) was skipped since it collides with above method
            # Method LoadPairVector128NonTemporal(address : UInt64*) was skipped since it collides with above method

        # Skipped LoadPairVector64 due to it being static, abstract and generic.

        LoadPairVector64 : LoadPairVector64_MethodGroup
        class LoadPairVector64_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_2[Vector64_1[float], Vector64_1[float]]:...
            # Method LoadPairVector64(address : Single*) was skipped since it collides with above method
            # Method LoadPairVector64(address : Byte*) was skipped since it collides with above method
            # Method LoadPairVector64(address : Int16*) was skipped since it collides with above method
            # Method LoadPairVector64(address : Int32*) was skipped since it collides with above method
            # Method LoadPairVector64(address : Int64*) was skipped since it collides with above method
            # Method LoadPairVector64(address : SByte*) was skipped since it collides with above method
            # Method LoadPairVector64(address : UInt16*) was skipped since it collides with above method
            # Method LoadPairVector64(address : UInt32*) was skipped since it collides with above method
            # Method LoadPairVector64(address : UInt64*) was skipped since it collides with above method

        # Skipped LoadPairVector64NonTemporal due to it being static, abstract and generic.

        LoadPairVector64NonTemporal : LoadPairVector64NonTemporal_MethodGroup
        class LoadPairVector64NonTemporal_MethodGroup:
            def __call__(self, address: clr.Reference[float]) -> ValueTuple_2[Vector64_1[float], Vector64_1[float]]:...
            # Method LoadPairVector64NonTemporal(address : Single*) was skipped since it collides with above method
            # Method LoadPairVector64NonTemporal(address : Byte*) was skipped since it collides with above method
            # Method LoadPairVector64NonTemporal(address : Int16*) was skipped since it collides with above method
            # Method LoadPairVector64NonTemporal(address : Int32*) was skipped since it collides with above method
            # Method LoadPairVector64NonTemporal(address : Int64*) was skipped since it collides with above method
            # Method LoadPairVector64NonTemporal(address : SByte*) was skipped since it collides with above method
            # Method LoadPairVector64NonTemporal(address : UInt16*) was skipped since it collides with above method
            # Method LoadPairVector64NonTemporal(address : UInt32*) was skipped since it collides with above method
            # Method LoadPairVector64NonTemporal(address : UInt64*) was skipped since it collides with above method

        # Skipped MaxAcross due to it being static, abstract and generic.

        MaxAcross : MaxAcross_MethodGroup
        class MaxAcross_MethodGroup:
            @typing.overload
            def __call__(self, value: Vector128_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
            # Method MaxAcross(value : Vector64`1) was skipped since it collides with above method
            # Method MaxAcross(value : Vector64`1) was skipped since it collides with above method
            # Method MaxAcross(value : Vector64`1) was skipped since it collides with above method
            # Method MaxAcross(value : Vector128`1) was skipped since it collides with above method
            # Method MaxAcross(value : Vector128`1) was skipped since it collides with above method
            # Method MaxAcross(value : Vector128`1) was skipped since it collides with above method
            # Method MaxAcross(value : Vector128`1) was skipped since it collides with above method
            # Method MaxAcross(value : Vector128`1) was skipped since it collides with above method
            # Method MaxAcross(value : Vector128`1) was skipped since it collides with above method

        # Skipped MaxNumberPairwise due to it being static, abstract and generic.

        MaxNumberPairwise : MaxNumberPairwise_MethodGroup
        class MaxNumberPairwise_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method MaxNumberPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped MaxNumberPairwiseScalar due to it being static, abstract and generic.

        MaxNumberPairwiseScalar : MaxNumberPairwiseScalar_MethodGroup
        class MaxNumberPairwiseScalar_MethodGroup:
            @typing.overload
            def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, value: Vector128_1[float]) -> Vector64_1[float]:...

        # Skipped MaxPairwise due to it being static, abstract and generic.

        MaxPairwise : MaxPairwise_MethodGroup
        class MaxPairwise_MethodGroup:
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method MaxPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method MaxPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method MaxPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method MaxPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method MaxPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method MaxPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method MaxPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped MaxPairwiseScalar due to it being static, abstract and generic.

        MaxPairwiseScalar : MaxPairwiseScalar_MethodGroup
        class MaxPairwiseScalar_MethodGroup:
            @typing.overload
            def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, value: Vector128_1[float]) -> Vector64_1[float]:...

        # Skipped MaxScalar due to it being static, abstract and generic.

        MaxScalar : MaxScalar_MethodGroup
        class MaxScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method MaxScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped MinAcross due to it being static, abstract and generic.

        MinAcross : MinAcross_MethodGroup
        class MinAcross_MethodGroup:
            @typing.overload
            def __call__(self, value: Vector128_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
            # Method MinAcross(value : Vector64`1) was skipped since it collides with above method
            # Method MinAcross(value : Vector64`1) was skipped since it collides with above method
            # Method MinAcross(value : Vector64`1) was skipped since it collides with above method
            # Method MinAcross(value : Vector128`1) was skipped since it collides with above method
            # Method MinAcross(value : Vector128`1) was skipped since it collides with above method
            # Method MinAcross(value : Vector128`1) was skipped since it collides with above method
            # Method MinAcross(value : Vector128`1) was skipped since it collides with above method
            # Method MinAcross(value : Vector128`1) was skipped since it collides with above method
            # Method MinAcross(value : Vector128`1) was skipped since it collides with above method

        # Skipped MinNumberPairwise due to it being static, abstract and generic.

        MinNumberPairwise : MinNumberPairwise_MethodGroup
        class MinNumberPairwise_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method MinNumberPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped MinNumberPairwiseScalar due to it being static, abstract and generic.

        MinNumberPairwiseScalar : MinNumberPairwiseScalar_MethodGroup
        class MinNumberPairwiseScalar_MethodGroup:
            @typing.overload
            def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, value: Vector128_1[float]) -> Vector64_1[float]:...

        # Skipped MinPairwise due to it being static, abstract and generic.

        MinPairwise : MinPairwise_MethodGroup
        class MinPairwise_MethodGroup:
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method MinPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method MinPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method MinPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method MinPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method MinPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method MinPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method MinPairwise(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped MinPairwiseScalar due to it being static, abstract and generic.

        MinPairwiseScalar : MinPairwiseScalar_MethodGroup
        class MinPairwiseScalar_MethodGroup:
            @typing.overload
            def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, value: Vector128_1[float]) -> Vector64_1[float]:...

        # Skipped MinScalar due to it being static, abstract and generic.

        MinScalar : MinScalar_MethodGroup
        class MinScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method MinScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped MultiplyDoublingSaturateHighScalar due to it being static, abstract and generic.

        MultiplyDoublingSaturateHighScalar : MultiplyDoublingSaturateHighScalar_MethodGroup
        class MultiplyDoublingSaturateHighScalar_MethodGroup:
            def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
            # Method MultiplyDoublingSaturateHighScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped MultiplyDoublingScalarBySelectedScalarSaturateHigh due to it being static, abstract and generic.

        MultiplyDoublingScalarBySelectedScalarSaturateHigh : MultiplyDoublingScalarBySelectedScalarSaturateHigh_MethodGroup
        class MultiplyDoublingScalarBySelectedScalarSaturateHigh_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector64_1[int]:...
            @typing.overload
            def __call__(self, left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector64_1[int]:...
            # Method MultiplyDoublingScalarBySelectedScalarSaturateHigh(left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
            # Method MultiplyDoublingScalarBySelectedScalarSaturateHigh(left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

        # Skipped MultiplyDoublingWideningAndAddSaturateScalar due to it being static, abstract and generic.

        MultiplyDoublingWideningAndAddSaturateScalar : MultiplyDoublingWideningAndAddSaturateScalar_MethodGroup
        class MultiplyDoublingWideningAndAddSaturateScalar_MethodGroup:
            def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
            # Method MultiplyDoublingWideningAndAddSaturateScalar(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped MultiplyDoublingWideningAndSubtractSaturateScalar due to it being static, abstract and generic.

        MultiplyDoublingWideningAndSubtractSaturateScalar : MultiplyDoublingWideningAndSubtractSaturateScalar_MethodGroup
        class MultiplyDoublingWideningAndSubtractSaturateScalar_MethodGroup:
            def __call__(self, minuend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
            # Method MultiplyDoublingWideningAndSubtractSaturateScalar(minuend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped MultiplyDoublingWideningSaturateScalar due to it being static, abstract and generic.

        MultiplyDoublingWideningSaturateScalar : MultiplyDoublingWideningSaturateScalar_MethodGroup
        class MultiplyDoublingWideningSaturateScalar_MethodGroup:
            def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
            # Method MultiplyDoublingWideningSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped MultiplyDoublingWideningSaturateScalarBySelectedScalar due to it being static, abstract and generic.

        MultiplyDoublingWideningSaturateScalarBySelectedScalar : MultiplyDoublingWideningSaturateScalarBySelectedScalar_MethodGroup
        class MultiplyDoublingWideningSaturateScalarBySelectedScalar_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector64_1[int]:...
            @typing.overload
            def __call__(self, left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector64_1[int]:...
            # Method MultiplyDoublingWideningSaturateScalarBySelectedScalar(left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
            # Method MultiplyDoublingWideningSaturateScalarBySelectedScalar(left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

        # Skipped MultiplyDoublingWideningScalarBySelectedScalarAndAddSaturate due to it being static, abstract and generic.

        MultiplyDoublingWideningScalarBySelectedScalarAndAddSaturate : MultiplyDoublingWideningScalarBySelectedScalarAndAddSaturate_MethodGroup
        class MultiplyDoublingWideningScalarBySelectedScalarAndAddSaturate_MethodGroup:
            @typing.overload
            def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector64_1[int]:...
            @typing.overload
            def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector64_1[int]:...
            # Method MultiplyDoublingWideningScalarBySelectedScalarAndAddSaturate(addend : Vector64`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
            # Method MultiplyDoublingWideningScalarBySelectedScalarAndAddSaturate(addend : Vector64`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

        # Skipped MultiplyDoublingWideningScalarBySelectedScalarAndSubtractSaturate due to it being static, abstract and generic.

        MultiplyDoublingWideningScalarBySelectedScalarAndSubtractSaturate : MultiplyDoublingWideningScalarBySelectedScalarAndSubtractSaturate_MethodGroup
        class MultiplyDoublingWideningScalarBySelectedScalarAndSubtractSaturate_MethodGroup:
            @typing.overload
            def __call__(self, minuend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector64_1[int]:...
            @typing.overload
            def __call__(self, minuend: Vector64_1[int], left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector64_1[int]:...
            # Method MultiplyDoublingWideningScalarBySelectedScalarAndSubtractSaturate(minuend : Vector64`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
            # Method MultiplyDoublingWideningScalarBySelectedScalarAndSubtractSaturate(minuend : Vector64`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

        # Skipped MultiplyExtended due to it being static, abstract and generic.

        MultiplyExtended : MultiplyExtended_MethodGroup
        class MultiplyExtended_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method MultiplyExtended(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped MultiplyExtendedBySelectedScalar due to it being static, abstract and generic.

        MultiplyExtendedBySelectedScalar : MultiplyExtendedBySelectedScalar_MethodGroup
        class MultiplyExtendedBySelectedScalar_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float], rightIndex: int) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, left: Vector64_1[float], right: Vector128_1[float], rightIndex: int) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float], rightIndex: int) -> Vector128_1[float]:...
            @typing.overload
            def __call__(self, left: Vector128_1[float], right: Vector64_1[float], rightIndex: int) -> Vector128_1[float]:...
            # Method MultiplyExtendedBySelectedScalar(left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

        # Skipped MultiplyExtendedScalar due to it being static, abstract and generic.

        MultiplyExtendedScalar : MultiplyExtendedScalar_MethodGroup
        class MultiplyExtendedScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method MultiplyExtendedScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped MultiplyExtendedScalarBySelectedScalar due to it being static, abstract and generic.

        MultiplyExtendedScalarBySelectedScalar : MultiplyExtendedScalarBySelectedScalar_MethodGroup
        class MultiplyExtendedScalarBySelectedScalar_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[float], right: Vector128_1[float], rightIndex: int) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float], rightIndex: int) -> Vector64_1[float]:...
            # Method MultiplyExtendedScalarBySelectedScalar(left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

        # Skipped MultiplyRoundedDoublingSaturateHighScalar due to it being static, abstract and generic.

        MultiplyRoundedDoublingSaturateHighScalar : MultiplyRoundedDoublingSaturateHighScalar_MethodGroup
        class MultiplyRoundedDoublingSaturateHighScalar_MethodGroup:
            def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
            # Method MultiplyRoundedDoublingSaturateHighScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped MultiplyRoundedDoublingScalarBySelectedScalarSaturateHigh due to it being static, abstract and generic.

        MultiplyRoundedDoublingScalarBySelectedScalarSaturateHigh : MultiplyRoundedDoublingScalarBySelectedScalarSaturateHigh_MethodGroup
        class MultiplyRoundedDoublingScalarBySelectedScalarSaturateHigh_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector64_1[int]:...
            @typing.overload
            def __call__(self, left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector64_1[int]:...
            # Method MultiplyRoundedDoublingScalarBySelectedScalarSaturateHigh(left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
            # Method MultiplyRoundedDoublingScalarBySelectedScalarSaturateHigh(left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

        # Skipped Negate due to it being static, abstract and generic.

        Negate : Negate_MethodGroup
        class Negate_MethodGroup:
            def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
            # Method Negate(value : Vector128`1) was skipped since it collides with above method

        # Skipped NegateSaturateScalar due to it being static, abstract and generic.

        NegateSaturateScalar : NegateSaturateScalar_MethodGroup
        class NegateSaturateScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
            # Method NegateSaturateScalar(value : Vector64`1) was skipped since it collides with above method
            # Method NegateSaturateScalar(value : Vector64`1) was skipped since it collides with above method
            # Method NegateSaturateScalar(value : Vector64`1) was skipped since it collides with above method

        # Skipped ReciprocalEstimateScalar due to it being static, abstract and generic.

        ReciprocalEstimateScalar : ReciprocalEstimateScalar_MethodGroup
        class ReciprocalEstimateScalar_MethodGroup:
            def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
            # Method ReciprocalEstimateScalar(value : Vector64`1) was skipped since it collides with above method

        # Skipped ReciprocalExponentScalar due to it being static, abstract and generic.

        ReciprocalExponentScalar : ReciprocalExponentScalar_MethodGroup
        class ReciprocalExponentScalar_MethodGroup:
            def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
            # Method ReciprocalExponentScalar(value : Vector64`1) was skipped since it collides with above method

        # Skipped ReciprocalSquareRootEstimateScalar due to it being static, abstract and generic.

        ReciprocalSquareRootEstimateScalar : ReciprocalSquareRootEstimateScalar_MethodGroup
        class ReciprocalSquareRootEstimateScalar_MethodGroup:
            def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
            # Method ReciprocalSquareRootEstimateScalar(value : Vector64`1) was skipped since it collides with above method

        # Skipped ReciprocalSquareRootStepScalar due to it being static, abstract and generic.

        ReciprocalSquareRootStepScalar : ReciprocalSquareRootStepScalar_MethodGroup
        class ReciprocalSquareRootStepScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method ReciprocalSquareRootStepScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped ReciprocalStepScalar due to it being static, abstract and generic.

        ReciprocalStepScalar : ReciprocalStepScalar_MethodGroup
        class ReciprocalStepScalar_MethodGroup:
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            # Method ReciprocalStepScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped ReverseElementBits due to it being static, abstract and generic.

        ReverseElementBits : ReverseElementBits_MethodGroup
        class ReverseElementBits_MethodGroup:
            @typing.overload
            def __call__(self, value: Vector64_1[int]) -> Vector64_1[int]:...
            # Method ReverseElementBits(value : Vector64`1) was skipped since it collides with above method
            @typing.overload
            def __call__(self, value: Vector128_1[int]) -> Vector128_1[int]:...
            # Method ReverseElementBits(value : Vector128`1) was skipped since it collides with above method

        # Skipped ShiftArithmeticRoundedSaturateScalar due to it being static, abstract and generic.

        ShiftArithmeticRoundedSaturateScalar : ShiftArithmeticRoundedSaturateScalar_MethodGroup
        class ShiftArithmeticRoundedSaturateScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
            # Method ShiftArithmeticRoundedSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
            # Method ShiftArithmeticRoundedSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method

        # Skipped ShiftArithmeticSaturateScalar due to it being static, abstract and generic.

        ShiftArithmeticSaturateScalar : ShiftArithmeticSaturateScalar_MethodGroup
        class ShiftArithmeticSaturateScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
            # Method ShiftArithmeticSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
            # Method ShiftArithmeticSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method

        # Skipped ShiftLeftLogicalSaturateScalar due to it being static, abstract and generic.

        ShiftLeftLogicalSaturateScalar : ShiftLeftLogicalSaturateScalar_MethodGroup
        class ShiftLeftLogicalSaturateScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
            # Method ShiftLeftLogicalSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftLeftLogicalSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftLeftLogicalSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftLeftLogicalSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftLeftLogicalSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method

        # Skipped ShiftLeftLogicalSaturateUnsignedScalar due to it being static, abstract and generic.

        ShiftLeftLogicalSaturateUnsignedScalar : ShiftLeftLogicalSaturateUnsignedScalar_MethodGroup
        class ShiftLeftLogicalSaturateUnsignedScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
            # Method ShiftLeftLogicalSaturateUnsignedScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftLeftLogicalSaturateUnsignedScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method

        # Skipped ShiftLogicalRoundedSaturateScalar due to it being static, abstract and generic.

        ShiftLogicalRoundedSaturateScalar : ShiftLogicalRoundedSaturateScalar_MethodGroup
        class ShiftLogicalRoundedSaturateScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
            # Method ShiftLogicalRoundedSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
            # Method ShiftLogicalRoundedSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
            # Method ShiftLogicalRoundedSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
            # Method ShiftLogicalRoundedSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
            # Method ShiftLogicalRoundedSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method

        # Skipped ShiftLogicalSaturateScalar due to it being static, abstract and generic.

        ShiftLogicalSaturateScalar : ShiftLogicalSaturateScalar_MethodGroup
        class ShiftLogicalSaturateScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int], count: Vector64_1[int]) -> Vector64_1[int]:...
            # Method ShiftLogicalSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
            # Method ShiftLogicalSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
            # Method ShiftLogicalSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
            # Method ShiftLogicalSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method
            # Method ShiftLogicalSaturateScalar(value : Vector64`1, count : Vector64`1) was skipped since it collides with above method

        # Skipped ShiftRightArithmeticNarrowingSaturateScalar due to it being static, abstract and generic.

        ShiftRightArithmeticNarrowingSaturateScalar : ShiftRightArithmeticNarrowingSaturateScalar_MethodGroup
        class ShiftRightArithmeticNarrowingSaturateScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
            # Method ShiftRightArithmeticNarrowingSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftRightArithmeticNarrowingSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method

        # Skipped ShiftRightArithmeticNarrowingSaturateUnsignedScalar due to it being static, abstract and generic.

        ShiftRightArithmeticNarrowingSaturateUnsignedScalar : ShiftRightArithmeticNarrowingSaturateUnsignedScalar_MethodGroup
        class ShiftRightArithmeticNarrowingSaturateUnsignedScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
            # Method ShiftRightArithmeticNarrowingSaturateUnsignedScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftRightArithmeticNarrowingSaturateUnsignedScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method

        # Skipped ShiftRightArithmeticRoundedNarrowingSaturateScalar due to it being static, abstract and generic.

        ShiftRightArithmeticRoundedNarrowingSaturateScalar : ShiftRightArithmeticRoundedNarrowingSaturateScalar_MethodGroup
        class ShiftRightArithmeticRoundedNarrowingSaturateScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
            # Method ShiftRightArithmeticRoundedNarrowingSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftRightArithmeticRoundedNarrowingSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method

        # Skipped ShiftRightArithmeticRoundedNarrowingSaturateUnsignedScalar due to it being static, abstract and generic.

        ShiftRightArithmeticRoundedNarrowingSaturateUnsignedScalar : ShiftRightArithmeticRoundedNarrowingSaturateUnsignedScalar_MethodGroup
        class ShiftRightArithmeticRoundedNarrowingSaturateUnsignedScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
            # Method ShiftRightArithmeticRoundedNarrowingSaturateUnsignedScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftRightArithmeticRoundedNarrowingSaturateUnsignedScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method

        # Skipped ShiftRightLogicalNarrowingSaturateScalar due to it being static, abstract and generic.

        ShiftRightLogicalNarrowingSaturateScalar : ShiftRightLogicalNarrowingSaturateScalar_MethodGroup
        class ShiftRightLogicalNarrowingSaturateScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
            # Method ShiftRightLogicalNarrowingSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftRightLogicalNarrowingSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftRightLogicalNarrowingSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftRightLogicalNarrowingSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftRightLogicalNarrowingSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method

        # Skipped ShiftRightLogicalRoundedNarrowingSaturateScalar due to it being static, abstract and generic.

        ShiftRightLogicalRoundedNarrowingSaturateScalar : ShiftRightLogicalRoundedNarrowingSaturateScalar_MethodGroup
        class ShiftRightLogicalRoundedNarrowingSaturateScalar_MethodGroup:
            def __call__(self, value: Vector64_1[int], count: int) -> Vector64_1[int]:...
            # Method ShiftRightLogicalRoundedNarrowingSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftRightLogicalRoundedNarrowingSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftRightLogicalRoundedNarrowingSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftRightLogicalRoundedNarrowingSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method
            # Method ShiftRightLogicalRoundedNarrowingSaturateScalar(value : Vector64`1, count : Byte) was skipped since it collides with above method

        # Skipped Sqrt due to it being static, abstract and generic.

        Sqrt : Sqrt_MethodGroup
        class Sqrt_MethodGroup:
            @typing.overload
            def __call__(self, value: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, value: Vector128_1[float]) -> Vector128_1[float]:...
            # Method Sqrt(value : Vector128`1) was skipped since it collides with above method

        # Skipped Store due to it being static, abstract and generic.

        Store : Store_MethodGroup
        class Store_MethodGroup:
            @typing.overload
            def __call__(self, address: clr.Reference[float], value: ValueTuple_2[Vector128_1[float], Vector128_1[float]]) -> None:...
            # Method Store(address : Double*, value : ValueTuple`2) was skipped since it collides with above method
            @typing.overload
            def __call__(self, address: clr.Reference[float], value: ValueTuple_3[Vector128_1[float], Vector128_1[float], Vector128_1[float]]) -> None:...
            # Method Store(address : Double*, value : ValueTuple`3) was skipped since it collides with above method
            @typing.overload
            def __call__(self, address: clr.Reference[float], value: ValueTuple_4[Vector128_1[float], Vector128_1[float], Vector128_1[float], Vector128_1[float]]) -> None:...
            # Method Store(address : Double*, value : ValueTuple`4) was skipped since it collides with above method
            # Method Store(address : Byte*, value : ValueTuple`2) was skipped since it collides with above method
            # Method Store(address : SByte*, value : ValueTuple`2) was skipped since it collides with above method
            # Method Store(address : Int16*, value : ValueTuple`2) was skipped since it collides with above method
            # Method Store(address : UInt16*, value : ValueTuple`2) was skipped since it collides with above method
            # Method Store(address : Int32*, value : ValueTuple`2) was skipped since it collides with above method
            # Method Store(address : UInt32*, value : ValueTuple`2) was skipped since it collides with above method
            # Method Store(address : Int64*, value : ValueTuple`2) was skipped since it collides with above method
            # Method Store(address : UInt64*, value : ValueTuple`2) was skipped since it collides with above method
            # Method Store(address : Byte*, value : ValueTuple`3) was skipped since it collides with above method
            # Method Store(address : SByte*, value : ValueTuple`3) was skipped since it collides with above method
            # Method Store(address : Int16*, value : ValueTuple`3) was skipped since it collides with above method
            # Method Store(address : UInt16*, value : ValueTuple`3) was skipped since it collides with above method
            # Method Store(address : Int32*, value : ValueTuple`3) was skipped since it collides with above method
            # Method Store(address : UInt32*, value : ValueTuple`3) was skipped since it collides with above method
            # Method Store(address : Int64*, value : ValueTuple`3) was skipped since it collides with above method
            # Method Store(address : UInt64*, value : ValueTuple`3) was skipped since it collides with above method
            # Method Store(address : Byte*, value : ValueTuple`4) was skipped since it collides with above method
            # Method Store(address : SByte*, value : ValueTuple`4) was skipped since it collides with above method
            # Method Store(address : Int16*, value : ValueTuple`4) was skipped since it collides with above method
            # Method Store(address : UInt16*, value : ValueTuple`4) was skipped since it collides with above method
            # Method Store(address : Int32*, value : ValueTuple`4) was skipped since it collides with above method
            # Method Store(address : UInt32*, value : ValueTuple`4) was skipped since it collides with above method
            # Method Store(address : Int64*, value : ValueTuple`4) was skipped since it collides with above method
            # Method Store(address : UInt64*, value : ValueTuple`4) was skipped since it collides with above method

        # Skipped StorePair due to it being static, abstract and generic.

        StorePair : StorePair_MethodGroup
        class StorePair_MethodGroup:
            @typing.overload
            def __call__(self, address: clr.Reference[float], value1: Vector64_1[float], value2: Vector64_1[float]) -> None:...
            # Method StorePair(address : Single*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            @typing.overload
            def __call__(self, address: clr.Reference[float], value1: Vector128_1[float], value2: Vector128_1[float]) -> None:...
            # Method StorePair(address : Single*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePair(address : Byte*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePair(address : Int16*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePair(address : Int32*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePair(address : Int64*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePair(address : SByte*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePair(address : UInt16*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePair(address : UInt32*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePair(address : UInt64*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePair(address : Byte*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePair(address : Int16*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePair(address : Int32*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePair(address : Int64*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePair(address : SByte*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePair(address : UInt16*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePair(address : UInt32*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePair(address : UInt64*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method

        # Skipped StorePairNonTemporal due to it being static, abstract and generic.

        StorePairNonTemporal : StorePairNonTemporal_MethodGroup
        class StorePairNonTemporal_MethodGroup:
            @typing.overload
            def __call__(self, address: clr.Reference[float], value1: Vector64_1[float], value2: Vector64_1[float]) -> None:...
            # Method StorePairNonTemporal(address : Single*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            @typing.overload
            def __call__(self, address: clr.Reference[float], value1: Vector128_1[float], value2: Vector128_1[float]) -> None:...
            # Method StorePairNonTemporal(address : Single*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : Byte*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : Int16*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : Int32*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : Int64*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : SByte*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : UInt16*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : UInt32*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : UInt64*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : Byte*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : Int16*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : Int32*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : Int64*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : SByte*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : UInt16*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : UInt32*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method
            # Method StorePairNonTemporal(address : UInt64*, value1 : Vector128`1, value2 : Vector128`1) was skipped since it collides with above method

        # Skipped StorePairScalar due to it being static, abstract and generic.

        StorePairScalar : StorePairScalar_MethodGroup
        class StorePairScalar_MethodGroup:
            def __call__(self, address: clr.Reference[float], value1: Vector64_1[float], value2: Vector64_1[float]) -> None:...
            # Method StorePairScalar(address : Int32*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePairScalar(address : UInt32*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method

        # Skipped StorePairScalarNonTemporal due to it being static, abstract and generic.

        StorePairScalarNonTemporal : StorePairScalarNonTemporal_MethodGroup
        class StorePairScalarNonTemporal_MethodGroup:
            def __call__(self, address: clr.Reference[float], value1: Vector64_1[float], value2: Vector64_1[float]) -> None:...
            # Method StorePairScalarNonTemporal(address : Int32*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method
            # Method StorePairScalarNonTemporal(address : UInt32*, value1 : Vector64`1, value2 : Vector64`1) was skipped since it collides with above method

        # Skipped StoreSelectedScalar due to it being static, abstract and generic.

        StoreSelectedScalar : StoreSelectedScalar_MethodGroup
        class StoreSelectedScalar_MethodGroup:
            @typing.overload
            def __call__(self, address: clr.Reference[float], value: ValueTuple_2[Vector128_1[float], Vector128_1[float]], index: int) -> None:...
            # Method StoreSelectedScalar(address : Double*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
            @typing.overload
            def __call__(self, address: clr.Reference[float], value: ValueTuple_3[Vector128_1[float], Vector128_1[float], Vector128_1[float]], index: int) -> None:...
            # Method StoreSelectedScalar(address : Double*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
            @typing.overload
            def __call__(self, address: clr.Reference[float], value: ValueTuple_4[Vector128_1[float], Vector128_1[float], Vector128_1[float], Vector128_1[float]], index: int) -> None:...
            # Method StoreSelectedScalar(address : Double*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : Byte*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : SByte*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : Int16*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : UInt16*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : Int32*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : UInt32*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : Int64*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : UInt64*, value : ValueTuple`2, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : Byte*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : SByte*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : Int16*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : UInt16*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : Int32*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : UInt32*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : Int64*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : UInt64*, value : ValueTuple`3, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : Byte*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : SByte*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : Int16*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : UInt16*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : Int32*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : UInt32*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : Int64*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method
            # Method StoreSelectedScalar(address : UInt64*, value : ValueTuple`4, index : Byte) was skipped since it collides with above method

        # Skipped StoreVectorAndZip due to it being static, abstract and generic.

        StoreVectorAndZip : StoreVectorAndZip_MethodGroup
        class StoreVectorAndZip_MethodGroup:
            @typing.overload
            def __call__(self, address: clr.Reference[float], value: ValueTuple_2[Vector128_1[float], Vector128_1[float]]) -> None:...
            # Method StoreVectorAndZip(address : Double*, value : ValueTuple`2) was skipped since it collides with above method
            @typing.overload
            def __call__(self, address: clr.Reference[float], value: ValueTuple_3[Vector128_1[float], Vector128_1[float], Vector128_1[float]]) -> None:...
            # Method StoreVectorAndZip(address : Double*, value : ValueTuple`3) was skipped since it collides with above method
            @typing.overload
            def __call__(self, address: clr.Reference[float], value: ValueTuple_4[Vector128_1[float], Vector128_1[float], Vector128_1[float], Vector128_1[float]]) -> None:...
            # Method StoreVectorAndZip(address : Double*, value : ValueTuple`4) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : Byte*, value : ValueTuple`2) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : SByte*, value : ValueTuple`2) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : Int16*, value : ValueTuple`2) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : UInt16*, value : ValueTuple`2) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : Int32*, value : ValueTuple`2) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : UInt32*, value : ValueTuple`2) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : Int64*, value : ValueTuple`2) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : UInt64*, value : ValueTuple`2) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : Byte*, value : ValueTuple`3) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : SByte*, value : ValueTuple`3) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : Int16*, value : ValueTuple`3) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : UInt16*, value : ValueTuple`3) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : Int32*, value : ValueTuple`3) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : UInt32*, value : ValueTuple`3) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : Int64*, value : ValueTuple`3) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : UInt64*, value : ValueTuple`3) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : Byte*, value : ValueTuple`4) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : SByte*, value : ValueTuple`4) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : Int16*, value : ValueTuple`4) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : UInt16*, value : ValueTuple`4) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : Int32*, value : ValueTuple`4) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : UInt32*, value : ValueTuple`4) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : Int64*, value : ValueTuple`4) was skipped since it collides with above method
            # Method StoreVectorAndZip(address : UInt64*, value : ValueTuple`4) was skipped since it collides with above method

        # Skipped SubtractSaturateScalar due to it being static, abstract and generic.

        SubtractSaturateScalar : SubtractSaturateScalar_MethodGroup
        class SubtractSaturateScalar_MethodGroup:
            def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
            # Method SubtractSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method SubtractSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method SubtractSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method SubtractSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method SubtractSaturateScalar(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped TransposeEven due to it being static, abstract and generic.

        TransposeEven : TransposeEven_MethodGroup
        class TransposeEven_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method TransposeEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeEven(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method TransposeEven(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method TransposeEven(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method TransposeEven(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method TransposeEven(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method TransposeEven(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method TransposeEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped TransposeOdd due to it being static, abstract and generic.

        TransposeOdd : TransposeOdd_MethodGroup
        class TransposeOdd_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method TransposeOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeOdd(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method TransposeOdd(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method TransposeOdd(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method TransposeOdd(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method TransposeOdd(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method TransposeOdd(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method TransposeOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method TransposeOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped UnzipEven due to it being static, abstract and generic.

        UnzipEven : UnzipEven_MethodGroup
        class UnzipEven_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method UnzipEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipEven(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method UnzipEven(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method UnzipEven(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method UnzipEven(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method UnzipEven(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method UnzipEven(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method UnzipEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipEven(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped UnzipOdd due to it being static, abstract and generic.

        UnzipOdd : UnzipOdd_MethodGroup
        class UnzipOdd_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method UnzipOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipOdd(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method UnzipOdd(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method UnzipOdd(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method UnzipOdd(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method UnzipOdd(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method UnzipOdd(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method UnzipOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method UnzipOdd(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped VectorTableLookup due to it being static, abstract and generic.

        VectorTableLookup : VectorTableLookup_MethodGroup
        class VectorTableLookup_MethodGroup:
            @typing.overload
            def __call__(self, table: Vector128_1[int], byteIndexes: Vector128_1[int]) -> Vector128_1[int]:...
            # Method VectorTableLookup(table : Vector128`1, byteIndexes : Vector128`1) was skipped since it collides with above method
            @typing.overload
            def __call__(self, table: ValueTuple_2[Vector128_1[int], Vector128_1[int]], byteIndexes: Vector128_1[int]) -> Vector128_1[int]:...
            # Method VectorTableLookup(table : ValueTuple`2, byteIndexes : Vector128`1) was skipped since it collides with above method
            @typing.overload
            def __call__(self, table: ValueTuple_3[Vector128_1[int], Vector128_1[int], Vector128_1[int]], byteIndexes: Vector128_1[int]) -> Vector128_1[int]:...
            # Method VectorTableLookup(table : ValueTuple`3, byteIndexes : Vector128`1) was skipped since it collides with above method
            @typing.overload
            def __call__(self, table: ValueTuple_4[Vector128_1[int], Vector128_1[int], Vector128_1[int], Vector128_1[int]], byteIndexes: Vector128_1[int]) -> Vector128_1[int]:...
            # Method VectorTableLookup(table : ValueTuple`4, byteIndexes : Vector128`1) was skipped since it collides with above method

        # Skipped VectorTableLookupExtension due to it being static, abstract and generic.

        VectorTableLookupExtension : VectorTableLookupExtension_MethodGroup
        class VectorTableLookupExtension_MethodGroup:
            @typing.overload
            def __call__(self, defaultValues: Vector128_1[int], table: Vector128_1[int], byteIndexes: Vector128_1[int]) -> Vector128_1[int]:...
            # Method VectorTableLookupExtension(defaultValues : Vector128`1, table : Vector128`1, byteIndexes : Vector128`1) was skipped since it collides with above method
            @typing.overload
            def __call__(self, defaultValues: Vector128_1[int], table: ValueTuple_2[Vector128_1[int], Vector128_1[int]], byteIndexes: Vector128_1[int]) -> Vector128_1[int]:...
            # Method VectorTableLookupExtension(defaultValues : Vector128`1, table : ValueTuple`2, byteIndexes : Vector128`1) was skipped since it collides with above method
            @typing.overload
            def __call__(self, defaultValues: Vector128_1[int], table: ValueTuple_3[Vector128_1[int], Vector128_1[int], Vector128_1[int]], byteIndexes: Vector128_1[int]) -> Vector128_1[int]:...
            # Method VectorTableLookupExtension(defaultValues : Vector128`1, table : ValueTuple`3, byteIndexes : Vector128`1) was skipped since it collides with above method
            @typing.overload
            def __call__(self, defaultValues: Vector128_1[int], table: ValueTuple_4[Vector128_1[int], Vector128_1[int], Vector128_1[int], Vector128_1[int]], byteIndexes: Vector128_1[int]) -> Vector128_1[int]:...
            # Method VectorTableLookupExtension(defaultValues : Vector128`1, table : ValueTuple`4, byteIndexes : Vector128`1) was skipped since it collides with above method

        # Skipped ZipHigh due to it being static, abstract and generic.

        ZipHigh : ZipHigh_MethodGroup
        class ZipHigh_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method ZipHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipHigh(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method ZipHigh(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method ZipHigh(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method ZipHigh(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method ZipHigh(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method ZipHigh(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method ZipHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipHigh(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

        # Skipped ZipLow due to it being static, abstract and generic.

        ZipLow : ZipLow_MethodGroup
        class ZipLow_MethodGroup:
            @typing.overload
            def __call__(self, left: Vector64_1[float], right: Vector64_1[float]) -> Vector64_1[float]:...
            @typing.overload
            def __call__(self, left: Vector128_1[float], right: Vector128_1[float]) -> Vector128_1[float]:...
            # Method ZipLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipLow(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method ZipLow(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method ZipLow(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method ZipLow(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method ZipLow(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method ZipLow(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
            # Method ZipLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method
            # Method ZipLow(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method




class Aes(ArmBase):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def Decrypt(value: Vector128_1[int], roundKey: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def Encrypt(value: Vector128_1[int], roundKey: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def InverseMixColumns(value: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def MixColumns(value: Vector128_1[int]) -> Vector128_1[int]: ...
    # Skipped PolynomialMultiplyWideningLower due to it being static, abstract and generic.

    PolynomialMultiplyWideningLower : PolynomialMultiplyWideningLower_MethodGroup
    class PolynomialMultiplyWideningLower_MethodGroup:
        def __call__(self, left: Vector64_1[int], right: Vector64_1[int]) -> Vector128_1[int]:...
        # Method PolynomialMultiplyWideningLower(left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

    # Skipped PolynomialMultiplyWideningUpper due to it being static, abstract and generic.

    PolynomialMultiplyWideningUpper : PolynomialMultiplyWideningUpper_MethodGroup
    class PolynomialMultiplyWideningUpper_MethodGroup:
        def __call__(self, left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method PolynomialMultiplyWideningUpper(left : Vector128`1, right : Vector128`1) was skipped since it collides with above method


    class Arm64(ArmBase.Arm64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...



class ArmBase(abc.ABC):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def Yield() -> None: ...
    # Skipped LeadingZeroCount due to it being static, abstract and generic.

    LeadingZeroCount : LeadingZeroCount_MethodGroup
    class LeadingZeroCount_MethodGroup:
        def __call__(self, value: int) -> int:...
        # Method LeadingZeroCount(value : UInt32) was skipped since it collides with above method

    # Skipped ReverseElementBits due to it being static, abstract and generic.

    ReverseElementBits : ReverseElementBits_MethodGroup
    class ReverseElementBits_MethodGroup:
        def __call__(self, value: int) -> int:...
        # Method ReverseElementBits(value : UInt32) was skipped since it collides with above method


    class Arm64(abc.ABC):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...
        # Skipped LeadingSignCount due to it being static, abstract and generic.

        LeadingSignCount : LeadingSignCount_MethodGroup
        class LeadingSignCount_MethodGroup:
            def __call__(self, value: int) -> int:...
            # Method LeadingSignCount(value : Int64) was skipped since it collides with above method

        # Skipped LeadingZeroCount due to it being static, abstract and generic.

        LeadingZeroCount : LeadingZeroCount_MethodGroup
        class LeadingZeroCount_MethodGroup:
            def __call__(self, value: int) -> int:...
            # Method LeadingZeroCount(value : UInt64) was skipped since it collides with above method

        # Skipped MultiplyHigh due to it being static, abstract and generic.

        MultiplyHigh : MultiplyHigh_MethodGroup
        class MultiplyHigh_MethodGroup:
            def __call__(self, left: int, right: int) -> int:...
            # Method MultiplyHigh(left : UInt64, right : UInt64) was skipped since it collides with above method

        # Skipped ReverseElementBits due to it being static, abstract and generic.

        ReverseElementBits : ReverseElementBits_MethodGroup
        class ReverseElementBits_MethodGroup:
            def __call__(self, value: int) -> int:...
            # Method ReverseElementBits(value : UInt64) was skipped since it collides with above method




class Crc32(ArmBase):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    # Skipped ComputeCrc32 due to it being static, abstract and generic.

    ComputeCrc32 : ComputeCrc32_MethodGroup
    class ComputeCrc32_MethodGroup:
        def __call__(self, crc: int, data: int) -> int:...
        # Method ComputeCrc32(crc : UInt32, data : UInt16) was skipped since it collides with above method
        # Method ComputeCrc32(crc : UInt32, data : UInt32) was skipped since it collides with above method

    # Skipped ComputeCrc32C due to it being static, abstract and generic.

    ComputeCrc32C : ComputeCrc32C_MethodGroup
    class ComputeCrc32C_MethodGroup:
        def __call__(self, crc: int, data: int) -> int:...
        # Method ComputeCrc32C(crc : UInt32, data : UInt16) was skipped since it collides with above method
        # Method ComputeCrc32C(crc : UInt32, data : UInt32) was skipped since it collides with above method


    class Arm64(ArmBase.Arm64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...
        @staticmethod
        def ComputeCrc32(crc: int, data: int) -> int: ...
        @staticmethod
        def ComputeCrc32C(crc: int, data: int) -> int: ...



class Dp(AdvSimd):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    # Skipped DotProduct due to it being static, abstract and generic.

    DotProduct : DotProduct_MethodGroup
    class DotProduct_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method DotProduct(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method DotProduct(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped DotProductBySelectedQuadruplet due to it being static, abstract and generic.

    DotProductBySelectedQuadruplet : DotProductBySelectedQuadruplet_MethodGroup
    class DotProductBySelectedQuadruplet_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int], rightScaledIndex: int) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector128_1[int], rightScaledIndex: int) -> Vector64_1[int]:...
        # Method DotProductBySelectedQuadruplet(addend : Vector64`1, left : Vector64`1, right : Vector64`1, rightScaledIndex : Byte) was skipped since it collides with above method
        # Method DotProductBySelectedQuadruplet(addend : Vector64`1, left : Vector64`1, right : Vector128`1, rightScaledIndex : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int], rightScaledIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector64_1[int], rightScaledIndex: int) -> Vector128_1[int]:...
        # Method DotProductBySelectedQuadruplet(addend : Vector128`1, left : Vector128`1, right : Vector128`1, rightScaledIndex : Byte) was skipped since it collides with above method
        # Method DotProductBySelectedQuadruplet(addend : Vector128`1, left : Vector128`1, right : Vector64`1, rightScaledIndex : Byte) was skipped since it collides with above method


    class Arm64(AdvSimd.Arm64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...



class Rdm(AdvSimd):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    # Skipped MultiplyRoundedDoublingAndAddSaturateHigh due to it being static, abstract and generic.

    MultiplyRoundedDoublingAndAddSaturateHigh : MultiplyRoundedDoublingAndAddSaturateHigh_MethodGroup
    class MultiplyRoundedDoublingAndAddSaturateHigh_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method MultiplyRoundedDoublingAndAddSaturateHigh(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyRoundedDoublingAndAddSaturateHigh(addend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyRoundedDoublingAndSubtractSaturateHigh due to it being static, abstract and generic.

    MultiplyRoundedDoublingAndSubtractSaturateHigh : MultiplyRoundedDoublingAndSubtractSaturateHigh_MethodGroup
    class MultiplyRoundedDoublingAndSubtractSaturateHigh_MethodGroup:
        @typing.overload
        def __call__(self, minuend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
        # Method MultiplyRoundedDoublingAndSubtractSaturateHigh(minuend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int]) -> Vector128_1[int]:...
        # Method MultiplyRoundedDoublingAndSubtractSaturateHigh(minuend : Vector128`1, left : Vector128`1, right : Vector128`1) was skipped since it collides with above method

    # Skipped MultiplyRoundedDoublingBySelectedScalarAndAddSaturateHigh due to it being static, abstract and generic.

    MultiplyRoundedDoublingBySelectedScalarAndAddSaturateHigh : MultiplyRoundedDoublingBySelectedScalarAndAddSaturateHigh_MethodGroup
    class MultiplyRoundedDoublingBySelectedScalarAndAddSaturateHigh_MethodGroup:
        @typing.overload
        def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector64_1[int]:...
        # Method MultiplyRoundedDoublingBySelectedScalarAndAddSaturateHigh(addend : Vector64`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingBySelectedScalarAndAddSaturateHigh(addend : Vector64`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, addend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyRoundedDoublingBySelectedScalarAndAddSaturateHigh(addend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingBySelectedScalarAndAddSaturateHigh(addend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyRoundedDoublingBySelectedScalarAndSubtractSaturateHigh due to it being static, abstract and generic.

    MultiplyRoundedDoublingBySelectedScalarAndSubtractSaturateHigh : MultiplyRoundedDoublingBySelectedScalarAndSubtractSaturateHigh_MethodGroup
    class MultiplyRoundedDoublingBySelectedScalarAndSubtractSaturateHigh_MethodGroup:
        @typing.overload
        def __call__(self, minuend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector64_1[int]:...
        @typing.overload
        def __call__(self, minuend: Vector64_1[int], left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector64_1[int]:...
        # Method MultiplyRoundedDoublingBySelectedScalarAndSubtractSaturateHigh(minuend : Vector64`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingBySelectedScalarAndSubtractSaturateHigh(minuend : Vector64`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector128_1[int], right: Vector64_1[int], rightIndex: int) -> Vector128_1[int]:...
        @typing.overload
        def __call__(self, minuend: Vector128_1[int], left: Vector128_1[int], right: Vector128_1[int], rightIndex: int) -> Vector128_1[int]:...
        # Method MultiplyRoundedDoublingBySelectedScalarAndSubtractSaturateHigh(minuend : Vector128`1, left : Vector128`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingBySelectedScalarAndSubtractSaturateHigh(minuend : Vector128`1, left : Vector128`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method


    class Arm64(AdvSimd.Arm64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...
        # Skipped MultiplyRoundedDoublingAndAddSaturateHighScalar due to it being static, abstract and generic.

        MultiplyRoundedDoublingAndAddSaturateHighScalar : MultiplyRoundedDoublingAndAddSaturateHighScalar_MethodGroup
        class MultiplyRoundedDoublingAndAddSaturateHighScalar_MethodGroup:
            def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
            # Method MultiplyRoundedDoublingAndAddSaturateHighScalar(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped MultiplyRoundedDoublingAndSubtractSaturateHighScalar due to it being static, abstract and generic.

        MultiplyRoundedDoublingAndSubtractSaturateHighScalar : MultiplyRoundedDoublingAndSubtractSaturateHighScalar_MethodGroup
        class MultiplyRoundedDoublingAndSubtractSaturateHighScalar_MethodGroup:
            def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int]) -> Vector64_1[int]:...
            # Method MultiplyRoundedDoublingAndSubtractSaturateHighScalar(addend : Vector64`1, left : Vector64`1, right : Vector64`1) was skipped since it collides with above method

        # Skipped MultiplyRoundedDoublingScalarBySelectedScalarAndAddSaturateHigh due to it being static, abstract and generic.

        MultiplyRoundedDoublingScalarBySelectedScalarAndAddSaturateHigh : MultiplyRoundedDoublingScalarBySelectedScalarAndAddSaturateHigh_MethodGroup
        class MultiplyRoundedDoublingScalarBySelectedScalarAndAddSaturateHigh_MethodGroup:
            @typing.overload
            def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector64_1[int]:...
            @typing.overload
            def __call__(self, addend: Vector64_1[int], left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector64_1[int]:...
            # Method MultiplyRoundedDoublingScalarBySelectedScalarAndAddSaturateHigh(addend : Vector64`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
            # Method MultiplyRoundedDoublingScalarBySelectedScalarAndAddSaturateHigh(addend : Vector64`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method

        # Skipped MultiplyRoundedDoublingScalarBySelectedScalarAndSubtractSaturateHigh due to it being static, abstract and generic.

        MultiplyRoundedDoublingScalarBySelectedScalarAndSubtractSaturateHigh : MultiplyRoundedDoublingScalarBySelectedScalarAndSubtractSaturateHigh_MethodGroup
        class MultiplyRoundedDoublingScalarBySelectedScalarAndSubtractSaturateHigh_MethodGroup:
            @typing.overload
            def __call__(self, minuend: Vector64_1[int], left: Vector64_1[int], right: Vector64_1[int], rightIndex: int) -> Vector64_1[int]:...
            @typing.overload
            def __call__(self, minuend: Vector64_1[int], left: Vector64_1[int], right: Vector128_1[int], rightIndex: int) -> Vector64_1[int]:...
            # Method MultiplyRoundedDoublingScalarBySelectedScalarAndSubtractSaturateHigh(minuend : Vector64`1, left : Vector64`1, right : Vector64`1, rightIndex : Byte) was skipped since it collides with above method
            # Method MultiplyRoundedDoublingScalarBySelectedScalarAndSubtractSaturateHigh(minuend : Vector64`1, left : Vector64`1, right : Vector128`1, rightIndex : Byte) was skipped since it collides with above method




class Sha1(ArmBase):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def FixedRotate(hash_e: Vector64_1[int]) -> Vector64_1[int]: ...
    @staticmethod
    def HashUpdateChoose(hash_abcd: Vector128_1[int], hash_e: Vector64_1[int], wk: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def HashUpdateMajority(hash_abcd: Vector128_1[int], hash_e: Vector64_1[int], wk: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def HashUpdateParity(hash_abcd: Vector128_1[int], hash_e: Vector64_1[int], wk: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def ScheduleUpdate0(w0_3: Vector128_1[int], w4_7: Vector128_1[int], w8_11: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def ScheduleUpdate1(tw0_3: Vector128_1[int], w12_15: Vector128_1[int]) -> Vector128_1[int]: ...

    class Arm64(ArmBase.Arm64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...



class Sha256(ArmBase):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def HashUpdate1(hash_abcd: Vector128_1[int], hash_efgh: Vector128_1[int], wk: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def HashUpdate2(hash_efgh: Vector128_1[int], hash_abcd: Vector128_1[int], wk: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def ScheduleUpdate0(w0_3: Vector128_1[int], w4_7: Vector128_1[int]) -> Vector128_1[int]: ...
    @staticmethod
    def ScheduleUpdate1(w0_3: Vector128_1[int], w8_11: Vector128_1[int], w12_15: Vector128_1[int]) -> Vector128_1[int]: ...

    class Arm64(ArmBase.Arm64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...



class Sve(AdvSimd):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def Count16BitElements(pattern: SveMaskPattern = ...) -> int: ...
    @staticmethod
    def Count32BitElements(pattern: SveMaskPattern = ...) -> int: ...
    @staticmethod
    def Count64BitElements(pattern: SveMaskPattern = ...) -> int: ...
    @staticmethod
    def Count8BitElements(pattern: SveMaskPattern = ...) -> int: ...
    @staticmethod
    def CreateFalseMaskByte() -> Vector_1[int]: ...
    @staticmethod
    def CreateFalseMaskDouble() -> Vector_1[float]: ...
    @staticmethod
    def CreateFalseMaskInt16() -> Vector_1[int]: ...
    @staticmethod
    def CreateFalseMaskInt32() -> Vector_1[int]: ...
    @staticmethod
    def CreateFalseMaskInt64() -> Vector_1[int]: ...
    @staticmethod
    def CreateFalseMaskSByte() -> Vector_1[int]: ...
    @staticmethod
    def CreateFalseMaskSingle() -> Vector_1[float]: ...
    @staticmethod
    def CreateFalseMaskUInt16() -> Vector_1[int]: ...
    @staticmethod
    def CreateFalseMaskUInt32() -> Vector_1[int]: ...
    @staticmethod
    def CreateFalseMaskUInt64() -> Vector_1[int]: ...
    @staticmethod
    def CreateTrueMaskByte(pattern: SveMaskPattern = ...) -> Vector_1[int]: ...
    @staticmethod
    def CreateTrueMaskDouble(pattern: SveMaskPattern = ...) -> Vector_1[float]: ...
    @staticmethod
    def CreateTrueMaskInt16(pattern: SveMaskPattern = ...) -> Vector_1[int]: ...
    @staticmethod
    def CreateTrueMaskInt32(pattern: SveMaskPattern = ...) -> Vector_1[int]: ...
    @staticmethod
    def CreateTrueMaskInt64(pattern: SveMaskPattern = ...) -> Vector_1[int]: ...
    @staticmethod
    def CreateTrueMaskSByte(pattern: SveMaskPattern = ...) -> Vector_1[int]: ...
    @staticmethod
    def CreateTrueMaskSingle(pattern: SveMaskPattern = ...) -> Vector_1[float]: ...
    @staticmethod
    def CreateTrueMaskUInt16(pattern: SveMaskPattern = ...) -> Vector_1[int]: ...
    @staticmethod
    def CreateTrueMaskUInt32(pattern: SveMaskPattern = ...) -> Vector_1[int]: ...
    @staticmethod
    def CreateTrueMaskUInt64(pattern: SveMaskPattern = ...) -> Vector_1[int]: ...
    @staticmethod
    def GetFfrByte() -> Vector_1[int]: ...
    @staticmethod
    def GetFfrInt16() -> Vector_1[int]: ...
    @staticmethod
    def GetFfrInt32() -> Vector_1[int]: ...
    @staticmethod
    def GetFfrInt64() -> Vector_1[int]: ...
    @staticmethod
    def GetFfrSByte() -> Vector_1[int]: ...
    @staticmethod
    def GetFfrUInt16() -> Vector_1[int]: ...
    @staticmethod
    def GetFfrUInt32() -> Vector_1[int]: ...
    @staticmethod
    def GetFfrUInt64() -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorByteNonFaultingZeroExtendToInt16(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorByteNonFaultingZeroExtendToInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorByteNonFaultingZeroExtendToInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorByteNonFaultingZeroExtendToUInt16(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorByteNonFaultingZeroExtendToUInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorByteNonFaultingZeroExtendToUInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorByteZeroExtendToInt16(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorByteZeroExtendToInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorByteZeroExtendToInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorByteZeroExtendToUInt16(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorByteZeroExtendToUInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorByteZeroExtendToUInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorInt16NonFaultingSignExtendToInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorInt16NonFaultingSignExtendToInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorInt16NonFaultingSignExtendToUInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorInt16NonFaultingSignExtendToUInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorInt16SignExtendToInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorInt16SignExtendToInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorInt16SignExtendToUInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorInt16SignExtendToUInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorInt32NonFaultingSignExtendToInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorInt32NonFaultingSignExtendToUInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorInt32SignExtendToInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorInt32SignExtendToUInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorSByteNonFaultingSignExtendToInt16(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorSByteNonFaultingSignExtendToInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorSByteNonFaultingSignExtendToInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorSByteNonFaultingSignExtendToUInt16(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorSByteNonFaultingSignExtendToUInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorSByteNonFaultingSignExtendToUInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorSByteSignExtendToInt16(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorSByteSignExtendToInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorSByteSignExtendToInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorSByteSignExtendToUInt16(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorSByteSignExtendToUInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorSByteSignExtendToUInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorUInt16NonFaultingZeroExtendToInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorUInt16NonFaultingZeroExtendToInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorUInt16NonFaultingZeroExtendToUInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorUInt16NonFaultingZeroExtendToUInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorUInt16ZeroExtendToInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorUInt16ZeroExtendToInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorUInt16ZeroExtendToUInt32(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorUInt16ZeroExtendToUInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorUInt32NonFaultingZeroExtendToInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorUInt32NonFaultingZeroExtendToUInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorUInt32ZeroExtendToInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def LoadVectorUInt32ZeroExtendToUInt64(mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]: ...
    @staticmethod
    def MultiplyAddRotateComplexBySelectedScalar(addend: Vector_1[float], left: Vector_1[float], right: Vector_1[float], rightIndex: int, rotation: int) -> Vector_1[float]: ...
    @staticmethod
    def Prefetch16Bit(mask: Vector_1[int], address: clr.Reference[None], prefetchType: SvePrefetchType) -> None: ...
    @staticmethod
    def Prefetch32Bit(mask: Vector_1[int], address: clr.Reference[None], prefetchType: SvePrefetchType) -> None: ...
    @staticmethod
    def Prefetch64Bit(mask: Vector_1[int], address: clr.Reference[None], prefetchType: SvePrefetchType) -> None: ...
    @staticmethod
    def Prefetch8Bit(mask: Vector_1[int], address: clr.Reference[None], prefetchType: SvePrefetchType) -> None: ...
    @staticmethod
    def SignExtend32(value: Vector_1[int]) -> Vector_1[int]: ...
    @staticmethod
    def ZeroExtend32(value: Vector_1[int]) -> Vector_1[int]: ...
    # Skipped Abs due to it being static, abstract and generic.

    Abs : Abs_MethodGroup
    class Abs_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method Abs(value : Vector`1) was skipped since it collides with above method
        # Method Abs(value : Vector`1) was skipped since it collides with above method
        # Method Abs(value : Vector`1) was skipped since it collides with above method
        # Method Abs(value : Vector`1) was skipped since it collides with above method
        # Method Abs(value : Vector`1) was skipped since it collides with above method

    # Skipped AbsoluteCompareGreaterThan due to it being static, abstract and generic.

    AbsoluteCompareGreaterThan : AbsoluteCompareGreaterThan_MethodGroup
    class AbsoluteCompareGreaterThan_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method AbsoluteCompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AbsoluteCompareGreaterThanOrEqual due to it being static, abstract and generic.

    AbsoluteCompareGreaterThanOrEqual : AbsoluteCompareGreaterThanOrEqual_MethodGroup
    class AbsoluteCompareGreaterThanOrEqual_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method AbsoluteCompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AbsoluteCompareLessThan due to it being static, abstract and generic.

    AbsoluteCompareLessThan : AbsoluteCompareLessThan_MethodGroup
    class AbsoluteCompareLessThan_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method AbsoluteCompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AbsoluteCompareLessThanOrEqual due to it being static, abstract and generic.

    AbsoluteCompareLessThanOrEqual : AbsoluteCompareLessThanOrEqual_MethodGroup
    class AbsoluteCompareLessThanOrEqual_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method AbsoluteCompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AbsoluteDifference due to it being static, abstract and generic.

    AbsoluteDifference : AbsoluteDifference_MethodGroup
    class AbsoluteDifference_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method AbsoluteDifference(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifference(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped Add due to it being static, abstract and generic.

    Add : Add_MethodGroup
    class Add_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method Add(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Add(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Add(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Add(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Add(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Add(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Add(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Add(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Add(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AddAcross due to it being static, abstract and generic.

    AddAcross : AddAcross_MethodGroup
    class AddAcross_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method AddAcross(value : Vector`1) was skipped since it collides with above method
        # Method AddAcross(value : Vector`1) was skipped since it collides with above method
        # Method AddAcross(value : Vector`1) was skipped since it collides with above method
        # Method AddAcross(value : Vector`1) was skipped since it collides with above method
        # Method AddAcross(value : Vector`1) was skipped since it collides with above method
        # Method AddAcross(value : Vector`1) was skipped since it collides with above method
        # Method AddAcross(value : Vector`1) was skipped since it collides with above method
        # Method AddAcross(value : Vector`1) was skipped since it collides with above method
        # Method AddAcross(value : Vector`1) was skipped since it collides with above method

    # Skipped AddRotateComplex due to it being static, abstract and generic.

    AddRotateComplex : AddRotateComplex_MethodGroup
    class AddRotateComplex_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float], rotation: int) -> Vector_1[float]:...
        # Method AddRotateComplex(left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method

    # Skipped AddSaturate due to it being static, abstract and generic.

    AddSaturate : AddSaturate_MethodGroup
    class AddSaturate_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AddSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AddSequentialAcross due to it being static, abstract and generic.

    AddSequentialAcross : AddSequentialAcross_MethodGroup
    class AddSequentialAcross_MethodGroup:
        def __call__(self, initial: Vector_1[float], value: Vector_1[float]) -> Vector_1[float]:...
        # Method AddSequentialAcross(initial : Vector`1, value : Vector`1) was skipped since it collides with above method

    # Skipped And due to it being static, abstract and generic.

    And : And_MethodGroup
    class And_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method And(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method And(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method And(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method And(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method And(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method And(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method And(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AndAcross due to it being static, abstract and generic.

    AndAcross : AndAcross_MethodGroup
    class AndAcross_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method AndAcross(value : Vector`1) was skipped since it collides with above method
        # Method AndAcross(value : Vector`1) was skipped since it collides with above method
        # Method AndAcross(value : Vector`1) was skipped since it collides with above method
        # Method AndAcross(value : Vector`1) was skipped since it collides with above method
        # Method AndAcross(value : Vector`1) was skipped since it collides with above method
        # Method AndAcross(value : Vector`1) was skipped since it collides with above method
        # Method AndAcross(value : Vector`1) was skipped since it collides with above method

    # Skipped BitwiseClear due to it being static, abstract and generic.

    BitwiseClear : BitwiseClear_MethodGroup
    class BitwiseClear_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method BitwiseClear(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseClear(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseClear(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseClear(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseClear(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseClear(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseClear(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped BooleanNot due to it being static, abstract and generic.

    BooleanNot : BooleanNot_MethodGroup
    class BooleanNot_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method BooleanNot(value : Vector`1) was skipped since it collides with above method
        # Method BooleanNot(value : Vector`1) was skipped since it collides with above method
        # Method BooleanNot(value : Vector`1) was skipped since it collides with above method
        # Method BooleanNot(value : Vector`1) was skipped since it collides with above method
        # Method BooleanNot(value : Vector`1) was skipped since it collides with above method
        # Method BooleanNot(value : Vector`1) was skipped since it collides with above method
        # Method BooleanNot(value : Vector`1) was skipped since it collides with above method

    # Skipped Compact due to it being static, abstract and generic.

    Compact : Compact_MethodGroup
    class Compact_MethodGroup:
        def __call__(self, mask: Vector_1[float], value: Vector_1[float]) -> Vector_1[float]:...
        # Method Compact(mask : Vector`1, value : Vector`1) was skipped since it collides with above method
        # Method Compact(mask : Vector`1, value : Vector`1) was skipped since it collides with above method
        # Method Compact(mask : Vector`1, value : Vector`1) was skipped since it collides with above method
        # Method Compact(mask : Vector`1, value : Vector`1) was skipped since it collides with above method
        # Method Compact(mask : Vector`1, value : Vector`1) was skipped since it collides with above method

    # Skipped CompareEqual due to it being static, abstract and generic.

    CompareEqual : CompareEqual_MethodGroup
    class CompareEqual_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method CompareEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped CompareGreaterThan due to it being static, abstract and generic.

    CompareGreaterThan : CompareGreaterThan_MethodGroup
    class CompareGreaterThan_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped CompareGreaterThanOrEqual due to it being static, abstract and generic.

    CompareGreaterThanOrEqual : CompareGreaterThanOrEqual_MethodGroup
    class CompareGreaterThanOrEqual_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareGreaterThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped CompareLessThan due to it being static, abstract and generic.

    CompareLessThan : CompareLessThan_MethodGroup
    class CompareLessThan_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThan(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped CompareLessThanOrEqual due to it being static, abstract and generic.

    CompareLessThanOrEqual : CompareLessThanOrEqual_MethodGroup
    class CompareLessThanOrEqual_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareLessThanOrEqual(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped CompareNotEqualTo due to it being static, abstract and generic.

    CompareNotEqualTo : CompareNotEqualTo_MethodGroup
    class CompareNotEqualTo_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method CompareNotEqualTo(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareNotEqualTo(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareNotEqualTo(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareNotEqualTo(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareNotEqualTo(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareNotEqualTo(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareNotEqualTo(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareNotEqualTo(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareNotEqualTo(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareNotEqualTo(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareNotEqualTo(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CompareNotEqualTo(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped CompareUnordered due to it being static, abstract and generic.

    CompareUnordered : CompareUnordered_MethodGroup
    class CompareUnordered_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method CompareUnordered(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped Compute16BitAddresses due to it being static, abstract and generic.

    Compute16BitAddresses : Compute16BitAddresses_MethodGroup
    class Compute16BitAddresses_MethodGroup:
        def __call__(self, bases: Vector_1[int], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method Compute16BitAddresses(bases : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method Compute16BitAddresses(bases : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method Compute16BitAddresses(bases : Vector`1, indices : Vector`1) was skipped since it collides with above method

    # Skipped Compute32BitAddresses due to it being static, abstract and generic.

    Compute32BitAddresses : Compute32BitAddresses_MethodGroup
    class Compute32BitAddresses_MethodGroup:
        def __call__(self, bases: Vector_1[int], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method Compute32BitAddresses(bases : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method Compute32BitAddresses(bases : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method Compute32BitAddresses(bases : Vector`1, indices : Vector`1) was skipped since it collides with above method

    # Skipped Compute64BitAddresses due to it being static, abstract and generic.

    Compute64BitAddresses : Compute64BitAddresses_MethodGroup
    class Compute64BitAddresses_MethodGroup:
        def __call__(self, bases: Vector_1[int], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method Compute64BitAddresses(bases : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method Compute64BitAddresses(bases : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method Compute64BitAddresses(bases : Vector`1, indices : Vector`1) was skipped since it collides with above method

    # Skipped Compute8BitAddresses due to it being static, abstract and generic.

    Compute8BitAddresses : Compute8BitAddresses_MethodGroup
    class Compute8BitAddresses_MethodGroup:
        def __call__(self, bases: Vector_1[int], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method Compute8BitAddresses(bases : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method Compute8BitAddresses(bases : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method Compute8BitAddresses(bases : Vector`1, indices : Vector`1) was skipped since it collides with above method

    # Skipped ConditionalExtractAfterLastActiveElement due to it being static, abstract and generic.

    ConditionalExtractAfterLastActiveElement : ConditionalExtractAfterLastActiveElement_MethodGroup
    class ConditionalExtractAfterLastActiveElement_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[float], defaultValue: float, data: Vector_1[float]) -> float:...
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultValue : Single, data : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[float], defaultScalar: Vector_1[float], data: Vector_1[float]) -> Vector_1[float]:...
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultValue : Byte, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultValue : Int16, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultValue : Int32, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultValue : Int64, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultValue : SByte, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultValue : UInt16, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultValue : UInt32, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultValue : UInt64, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped ConditionalExtractAfterLastActiveElementAndReplicate due to it being static, abstract and generic.

    ConditionalExtractAfterLastActiveElementAndReplicate : ConditionalExtractAfterLastActiveElementAndReplicate_MethodGroup
    class ConditionalExtractAfterLastActiveElementAndReplicate_MethodGroup:
        def __call__(self, mask: Vector_1[float], defaultValues: Vector_1[float], data: Vector_1[float]) -> Vector_1[float]:...
        # Method ConditionalExtractAfterLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractAfterLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped ConditionalExtractLastActiveElement due to it being static, abstract and generic.

    ConditionalExtractLastActiveElement : ConditionalExtractLastActiveElement_MethodGroup
    class ConditionalExtractLastActiveElement_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[float], defaultValue: float, data: Vector_1[float]) -> float:...
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultValue : Single, data : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[float], defaultScalar: Vector_1[float], data: Vector_1[float]) -> Vector_1[float]:...
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultValue : Byte, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultValue : Int16, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultValue : Int32, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultValue : Int64, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultValue : SByte, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultValue : UInt16, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultValue : UInt32, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultValue : UInt64, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElement(mask : Vector`1, defaultScalar : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped ConditionalExtractLastActiveElementAndReplicate due to it being static, abstract and generic.

    ConditionalExtractLastActiveElementAndReplicate : ConditionalExtractLastActiveElementAndReplicate_MethodGroup
    class ConditionalExtractLastActiveElementAndReplicate_MethodGroup:
        def __call__(self, mask: Vector_1[float], defaultValues: Vector_1[float], data: Vector_1[float]) -> Vector_1[float]:...
        # Method ConditionalExtractLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ConditionalExtractLastActiveElementAndReplicate(mask : Vector`1, defaultValues : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped ConditionalSelect due to it being static, abstract and generic.

    ConditionalSelect : ConditionalSelect_MethodGroup
    class ConditionalSelect_MethodGroup:
        def __call__(self, mask: Vector_1[float], left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method ConditionalSelect(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ConditionalSelect(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ConditionalSelect(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ConditionalSelect(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ConditionalSelect(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ConditionalSelect(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ConditionalSelect(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ConditionalSelect(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ConditionalSelect(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped ConvertToDouble due to it being static, abstract and generic.

    ConvertToDouble : ConvertToDouble_MethodGroup
    class ConvertToDouble_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method ConvertToDouble(value : Vector`1) was skipped since it collides with above method
        # Method ConvertToDouble(value : Vector`1) was skipped since it collides with above method
        # Method ConvertToDouble(value : Vector`1) was skipped since it collides with above method
        # Method ConvertToDouble(value : Vector`1) was skipped since it collides with above method

    # Skipped ConvertToInt32 due to it being static, abstract and generic.

    ConvertToInt32 : ConvertToInt32_MethodGroup
    class ConvertToInt32_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[int]:...
        # Method ConvertToInt32(value : Vector`1) was skipped since it collides with above method

    # Skipped ConvertToInt64 due to it being static, abstract and generic.

    ConvertToInt64 : ConvertToInt64_MethodGroup
    class ConvertToInt64_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[int]:...
        # Method ConvertToInt64(value : Vector`1) was skipped since it collides with above method

    # Skipped ConvertToSingle due to it being static, abstract and generic.

    ConvertToSingle : ConvertToSingle_MethodGroup
    class ConvertToSingle_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method ConvertToSingle(value : Vector`1) was skipped since it collides with above method
        # Method ConvertToSingle(value : Vector`1) was skipped since it collides with above method
        # Method ConvertToSingle(value : Vector`1) was skipped since it collides with above method
        # Method ConvertToSingle(value : Vector`1) was skipped since it collides with above method

    # Skipped ConvertToUInt32 due to it being static, abstract and generic.

    ConvertToUInt32 : ConvertToUInt32_MethodGroup
    class ConvertToUInt32_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[int]:...
        # Method ConvertToUInt32(value : Vector`1) was skipped since it collides with above method

    # Skipped ConvertToUInt64 due to it being static, abstract and generic.

    ConvertToUInt64 : ConvertToUInt64_MethodGroup
    class ConvertToUInt64_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[int]:...
        # Method ConvertToUInt64(value : Vector`1) was skipped since it collides with above method

    # Skipped CreateBreakAfterMask due to it being static, abstract and generic.

    CreateBreakAfterMask : CreateBreakAfterMask_MethodGroup
    class CreateBreakAfterMask_MethodGroup:
        def __call__(self, totalMask: Vector_1[int], fromMask: Vector_1[int]) -> Vector_1[int]:...
        # Method CreateBreakAfterMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakAfterMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakAfterMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakAfterMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakAfterMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakAfterMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakAfterMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method

    # Skipped CreateBreakAfterPropagateMask due to it being static, abstract and generic.

    CreateBreakAfterPropagateMask : CreateBreakAfterPropagateMask_MethodGroup
    class CreateBreakAfterPropagateMask_MethodGroup:
        def __call__(self, mask: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method CreateBreakAfterPropagateMask(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CreateBreakAfterPropagateMask(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CreateBreakAfterPropagateMask(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CreateBreakAfterPropagateMask(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CreateBreakAfterPropagateMask(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CreateBreakAfterPropagateMask(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CreateBreakAfterPropagateMask(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped CreateBreakBeforeMask due to it being static, abstract and generic.

    CreateBreakBeforeMask : CreateBreakBeforeMask_MethodGroup
    class CreateBreakBeforeMask_MethodGroup:
        def __call__(self, totalMask: Vector_1[int], fromMask: Vector_1[int]) -> Vector_1[int]:...
        # Method CreateBreakBeforeMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakBeforeMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakBeforeMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakBeforeMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakBeforeMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakBeforeMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakBeforeMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method

    # Skipped CreateBreakBeforePropagateMask due to it being static, abstract and generic.

    CreateBreakBeforePropagateMask : CreateBreakBeforePropagateMask_MethodGroup
    class CreateBreakBeforePropagateMask_MethodGroup:
        def __call__(self, mask: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method CreateBreakBeforePropagateMask(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CreateBreakBeforePropagateMask(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CreateBreakBeforePropagateMask(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CreateBreakBeforePropagateMask(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CreateBreakBeforePropagateMask(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CreateBreakBeforePropagateMask(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method CreateBreakBeforePropagateMask(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped CreateBreakPropagateMask due to it being static, abstract and generic.

    CreateBreakPropagateMask : CreateBreakPropagateMask_MethodGroup
    class CreateBreakPropagateMask_MethodGroup:
        def __call__(self, totalMask: Vector_1[int], fromMask: Vector_1[int]) -> Vector_1[int]:...
        # Method CreateBreakPropagateMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakPropagateMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakPropagateMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakPropagateMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakPropagateMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakPropagateMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateBreakPropagateMask(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method

    # Skipped CreateMaskForFirstActiveElement due to it being static, abstract and generic.

    CreateMaskForFirstActiveElement : CreateMaskForFirstActiveElement_MethodGroup
    class CreateMaskForFirstActiveElement_MethodGroup:
        def __call__(self, totalMask: Vector_1[int], fromMask: Vector_1[int]) -> Vector_1[int]:...
        # Method CreateMaskForFirstActiveElement(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateMaskForFirstActiveElement(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateMaskForFirstActiveElement(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateMaskForFirstActiveElement(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateMaskForFirstActiveElement(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateMaskForFirstActiveElement(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateMaskForFirstActiveElement(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method

    # Skipped CreateMaskForNextActiveElement due to it being static, abstract and generic.

    CreateMaskForNextActiveElement : CreateMaskForNextActiveElement_MethodGroup
    class CreateMaskForNextActiveElement_MethodGroup:
        def __call__(self, totalMask: Vector_1[int], fromMask: Vector_1[int]) -> Vector_1[int]:...
        # Method CreateMaskForNextActiveElement(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateMaskForNextActiveElement(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method
        # Method CreateMaskForNextActiveElement(totalMask : Vector`1, fromMask : Vector`1) was skipped since it collides with above method

    # Skipped CreateWhileLessThanMask16Bit due to it being static, abstract and generic.

    CreateWhileLessThanMask16Bit : CreateWhileLessThanMask16Bit_MethodGroup
    class CreateWhileLessThanMask16Bit_MethodGroup:
        def __call__(self, left: int, right: int) -> Vector_1[int]:...
        # Method CreateWhileLessThanMask16Bit(left : Int64, right : Int64) was skipped since it collides with above method
        # Method CreateWhileLessThanMask16Bit(left : UInt32, right : UInt32) was skipped since it collides with above method
        # Method CreateWhileLessThanMask16Bit(left : UInt64, right : UInt64) was skipped since it collides with above method

    # Skipped CreateWhileLessThanMask32Bit due to it being static, abstract and generic.

    CreateWhileLessThanMask32Bit : CreateWhileLessThanMask32Bit_MethodGroup
    class CreateWhileLessThanMask32Bit_MethodGroup:
        def __call__(self, left: int, right: int) -> Vector_1[int]:...
        # Method CreateWhileLessThanMask32Bit(left : Int64, right : Int64) was skipped since it collides with above method
        # Method CreateWhileLessThanMask32Bit(left : UInt32, right : UInt32) was skipped since it collides with above method
        # Method CreateWhileLessThanMask32Bit(left : UInt64, right : UInt64) was skipped since it collides with above method

    # Skipped CreateWhileLessThanMask64Bit due to it being static, abstract and generic.

    CreateWhileLessThanMask64Bit : CreateWhileLessThanMask64Bit_MethodGroup
    class CreateWhileLessThanMask64Bit_MethodGroup:
        def __call__(self, left: int, right: int) -> Vector_1[int]:...
        # Method CreateWhileLessThanMask64Bit(left : Int64, right : Int64) was skipped since it collides with above method
        # Method CreateWhileLessThanMask64Bit(left : UInt32, right : UInt32) was skipped since it collides with above method
        # Method CreateWhileLessThanMask64Bit(left : UInt64, right : UInt64) was skipped since it collides with above method

    # Skipped CreateWhileLessThanMask8Bit due to it being static, abstract and generic.

    CreateWhileLessThanMask8Bit : CreateWhileLessThanMask8Bit_MethodGroup
    class CreateWhileLessThanMask8Bit_MethodGroup:
        def __call__(self, left: int, right: int) -> Vector_1[int]:...
        # Method CreateWhileLessThanMask8Bit(left : Int64, right : Int64) was skipped since it collides with above method
        # Method CreateWhileLessThanMask8Bit(left : UInt32, right : UInt32) was skipped since it collides with above method
        # Method CreateWhileLessThanMask8Bit(left : UInt64, right : UInt64) was skipped since it collides with above method

    # Skipped CreateWhileLessThanOrEqualMask16Bit due to it being static, abstract and generic.

    CreateWhileLessThanOrEqualMask16Bit : CreateWhileLessThanOrEqualMask16Bit_MethodGroup
    class CreateWhileLessThanOrEqualMask16Bit_MethodGroup:
        def __call__(self, left: int, right: int) -> Vector_1[int]:...
        # Method CreateWhileLessThanOrEqualMask16Bit(left : Int64, right : Int64) was skipped since it collides with above method
        # Method CreateWhileLessThanOrEqualMask16Bit(left : UInt32, right : UInt32) was skipped since it collides with above method
        # Method CreateWhileLessThanOrEqualMask16Bit(left : UInt64, right : UInt64) was skipped since it collides with above method

    # Skipped CreateWhileLessThanOrEqualMask32Bit due to it being static, abstract and generic.

    CreateWhileLessThanOrEqualMask32Bit : CreateWhileLessThanOrEqualMask32Bit_MethodGroup
    class CreateWhileLessThanOrEqualMask32Bit_MethodGroup:
        def __call__(self, left: int, right: int) -> Vector_1[int]:...
        # Method CreateWhileLessThanOrEqualMask32Bit(left : Int64, right : Int64) was skipped since it collides with above method
        # Method CreateWhileLessThanOrEqualMask32Bit(left : UInt32, right : UInt32) was skipped since it collides with above method
        # Method CreateWhileLessThanOrEqualMask32Bit(left : UInt64, right : UInt64) was skipped since it collides with above method

    # Skipped CreateWhileLessThanOrEqualMask64Bit due to it being static, abstract and generic.

    CreateWhileLessThanOrEqualMask64Bit : CreateWhileLessThanOrEqualMask64Bit_MethodGroup
    class CreateWhileLessThanOrEqualMask64Bit_MethodGroup:
        def __call__(self, left: int, right: int) -> Vector_1[int]:...
        # Method CreateWhileLessThanOrEqualMask64Bit(left : Int64, right : Int64) was skipped since it collides with above method
        # Method CreateWhileLessThanOrEqualMask64Bit(left : UInt32, right : UInt32) was skipped since it collides with above method
        # Method CreateWhileLessThanOrEqualMask64Bit(left : UInt64, right : UInt64) was skipped since it collides with above method

    # Skipped CreateWhileLessThanOrEqualMask8Bit due to it being static, abstract and generic.

    CreateWhileLessThanOrEqualMask8Bit : CreateWhileLessThanOrEqualMask8Bit_MethodGroup
    class CreateWhileLessThanOrEqualMask8Bit_MethodGroup:
        def __call__(self, left: int, right: int) -> Vector_1[int]:...
        # Method CreateWhileLessThanOrEqualMask8Bit(left : Int64, right : Int64) was skipped since it collides with above method
        # Method CreateWhileLessThanOrEqualMask8Bit(left : UInt32, right : UInt32) was skipped since it collides with above method
        # Method CreateWhileLessThanOrEqualMask8Bit(left : UInt64, right : UInt64) was skipped since it collides with above method

    # Skipped Divide due to it being static, abstract and generic.

    Divide : Divide_MethodGroup
    class Divide_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method Divide(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped DotProduct due to it being static, abstract and generic.

    DotProduct : DotProduct_MethodGroup
    class DotProduct_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method DotProduct(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method DotProduct(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method DotProduct(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped DotProductBySelectedScalar due to it being static, abstract and generic.

    DotProductBySelectedScalar : DotProductBySelectedScalar_MethodGroup
    class DotProductBySelectedScalar_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method DotProductBySelectedScalar(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method DotProductBySelectedScalar(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method DotProductBySelectedScalar(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped DuplicateSelectedScalarToVector due to it being static, abstract and generic.

    DuplicateSelectedScalarToVector : DuplicateSelectedScalarToVector_MethodGroup
    class DuplicateSelectedScalarToVector_MethodGroup:
        def __call__(self, data: Vector_1[float], index: int) -> Vector_1[float]:...
        # Method DuplicateSelectedScalarToVector(data : Vector`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector(data : Vector`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector(data : Vector`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector(data : Vector`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector(data : Vector`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector(data : Vector`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector(data : Vector`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector(data : Vector`1, index : Byte) was skipped since it collides with above method
        # Method DuplicateSelectedScalarToVector(data : Vector`1, index : Byte) was skipped since it collides with above method

    # Skipped ExtractAfterLastActiveElement due to it being static, abstract and generic.

    ExtractAfterLastActiveElement : ExtractAfterLastActiveElement_MethodGroup
    class ExtractAfterLastActiveElement_MethodGroup:
        def __call__(self, mask: Vector_1[float], data: Vector_1[float]) -> Vector_1[float]:...
        # Method ExtractAfterLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped ExtractAfterLastActiveElementScalar due to it being static, abstract and generic.

    ExtractAfterLastActiveElementScalar : ExtractAfterLastActiveElementScalar_MethodGroup
    class ExtractAfterLastActiveElementScalar_MethodGroup:
        def __call__(self, mask: Vector_1[float], data: Vector_1[float]) -> float:...
        # Method ExtractAfterLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractAfterLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped ExtractLastActiveElement due to it being static, abstract and generic.

    ExtractLastActiveElement : ExtractLastActiveElement_MethodGroup
    class ExtractLastActiveElement_MethodGroup:
        def __call__(self, mask: Vector_1[float], data: Vector_1[float]) -> Vector_1[float]:...
        # Method ExtractLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElement(mask : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped ExtractLastActiveElementScalar due to it being static, abstract and generic.

    ExtractLastActiveElementScalar : ExtractLastActiveElementScalar_MethodGroup
    class ExtractLastActiveElementScalar_MethodGroup:
        def __call__(self, mask: Vector_1[float], data: Vector_1[float]) -> float:...
        # Method ExtractLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ExtractLastActiveElementScalar(mask : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped ExtractVector due to it being static, abstract and generic.

    ExtractVector : ExtractVector_MethodGroup
    class ExtractVector_MethodGroup:
        def __call__(self, upper: Vector_1[float], lower: Vector_1[float], index: int) -> Vector_1[float]:...
        # Method ExtractVector(upper : Vector`1, lower : Vector`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector(upper : Vector`1, lower : Vector`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector(upper : Vector`1, lower : Vector`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector(upper : Vector`1, lower : Vector`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector(upper : Vector`1, lower : Vector`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector(upper : Vector`1, lower : Vector`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector(upper : Vector`1, lower : Vector`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector(upper : Vector`1, lower : Vector`1, index : Byte) was skipped since it collides with above method
        # Method ExtractVector(upper : Vector`1, lower : Vector`1, index : Byte) was skipped since it collides with above method

    # Skipped FloatingPointExponentialAccelerator due to it being static, abstract and generic.

    FloatingPointExponentialAccelerator : FloatingPointExponentialAccelerator_MethodGroup
    class FloatingPointExponentialAccelerator_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[float]:...
        # Method FloatingPointExponentialAccelerator(value : Vector`1) was skipped since it collides with above method

    # Skipped FusedMultiplyAdd due to it being static, abstract and generic.

    FusedMultiplyAdd : FusedMultiplyAdd_MethodGroup
    class FusedMultiplyAdd_MethodGroup:
        def __call__(self, addend: Vector_1[float], left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method FusedMultiplyAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped FusedMultiplyAddBySelectedScalar due to it being static, abstract and generic.

    FusedMultiplyAddBySelectedScalar : FusedMultiplyAddBySelectedScalar_MethodGroup
    class FusedMultiplyAddBySelectedScalar_MethodGroup:
        def __call__(self, addend: Vector_1[float], left: Vector_1[float], right: Vector_1[float], rightIndex: int) -> Vector_1[float]:...
        # Method FusedMultiplyAddBySelectedScalar(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped FusedMultiplyAddNegated due to it being static, abstract and generic.

    FusedMultiplyAddNegated : FusedMultiplyAddNegated_MethodGroup
    class FusedMultiplyAddNegated_MethodGroup:
        def __call__(self, addend: Vector_1[float], left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method FusedMultiplyAddNegated(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped FusedMultiplySubtract due to it being static, abstract and generic.

    FusedMultiplySubtract : FusedMultiplySubtract_MethodGroup
    class FusedMultiplySubtract_MethodGroup:
        def __call__(self, minuend: Vector_1[float], left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method FusedMultiplySubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped FusedMultiplySubtractBySelectedScalar due to it being static, abstract and generic.

    FusedMultiplySubtractBySelectedScalar : FusedMultiplySubtractBySelectedScalar_MethodGroup
    class FusedMultiplySubtractBySelectedScalar_MethodGroup:
        def __call__(self, minuend: Vector_1[float], left: Vector_1[float], right: Vector_1[float], rightIndex: int) -> Vector_1[float]:...
        # Method FusedMultiplySubtractBySelectedScalar(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped FusedMultiplySubtractNegated due to it being static, abstract and generic.

    FusedMultiplySubtractNegated : FusedMultiplySubtractNegated_MethodGroup
    class FusedMultiplySubtractNegated_MethodGroup:
        def __call__(self, minuend: Vector_1[float], left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method FusedMultiplySubtractNegated(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped GatherPrefetch16Bit due to it being static, abstract and generic.

    GatherPrefetch16Bit : GatherPrefetch16Bit_MethodGroup
    class GatherPrefetch16Bit_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int], prefetchType: SvePrefetchType) -> None:...
        # Method GatherPrefetch16Bit(mask : Vector`1, addresses : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[None], indices: Vector_1[int], prefetchType: SvePrefetchType) -> None:...
        # Method GatherPrefetch16Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch16Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch16Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch16Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch16Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch16Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch16Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method

    # Skipped GatherPrefetch32Bit due to it being static, abstract and generic.

    GatherPrefetch32Bit : GatherPrefetch32Bit_MethodGroup
    class GatherPrefetch32Bit_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int], prefetchType: SvePrefetchType) -> None:...
        # Method GatherPrefetch32Bit(mask : Vector`1, addresses : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[None], indices: Vector_1[int], prefetchType: SvePrefetchType) -> None:...
        # Method GatherPrefetch32Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch32Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch32Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch32Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch32Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch32Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch32Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method

    # Skipped GatherPrefetch64Bit due to it being static, abstract and generic.

    GatherPrefetch64Bit : GatherPrefetch64Bit_MethodGroup
    class GatherPrefetch64Bit_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int], prefetchType: SvePrefetchType) -> None:...
        # Method GatherPrefetch64Bit(mask : Vector`1, addresses : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[None], indices: Vector_1[int], prefetchType: SvePrefetchType) -> None:...
        # Method GatherPrefetch64Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch64Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch64Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch64Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch64Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch64Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch64Bit(mask : Vector`1, address : Void*, indices : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method

    # Skipped GatherPrefetch8Bit due to it being static, abstract and generic.

    GatherPrefetch8Bit : GatherPrefetch8Bit_MethodGroup
    class GatherPrefetch8Bit_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int], prefetchType: SvePrefetchType) -> None:...
        # Method GatherPrefetch8Bit(mask : Vector`1, addresses : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[None], offsets: Vector_1[int], prefetchType: SvePrefetchType) -> None:...
        # Method GatherPrefetch8Bit(mask : Vector`1, address : Void*, offsets : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch8Bit(mask : Vector`1, address : Void*, offsets : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch8Bit(mask : Vector`1, address : Void*, offsets : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch8Bit(mask : Vector`1, address : Void*, offsets : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch8Bit(mask : Vector`1, address : Void*, offsets : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch8Bit(mask : Vector`1, address : Void*, offsets : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method
        # Method GatherPrefetch8Bit(mask : Vector`1, address : Void*, offsets : Vector`1, prefetchType : SvePrefetchType) was skipped since it collides with above method

    # Skipped GatherVector due to it being static, abstract and generic.

    GatherVector : GatherVector_MethodGroup
    class GatherVector_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[float], addresses: Vector_1[int]) -> Vector_1[float]:...
        # Method GatherVector(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        # Method GatherVector(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float], indices: Vector_1[int]) -> Vector_1[float]:...
        # Method GatherVector(mask : Vector`1, address : Double*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVector(mask : Vector`1, address : Single*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVector(mask : Vector`1, address : Single*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVector(mask : Vector`1, address : Int32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVector(mask : Vector`1, address : Int32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVector(mask : Vector`1, address : Int64*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVector(mask : Vector`1, address : Int64*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVector(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVector(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVector(mask : Vector`1, address : UInt64*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVector(mask : Vector`1, address : UInt64*, indices : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorByteZeroExtend due to it being static, abstract and generic.

    GatherVectorByteZeroExtend : GatherVectorByteZeroExtend_MethodGroup
    class GatherVectorByteZeroExtend_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorByteZeroExtend(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorByteZeroExtend(mask : Vector`1, address : Byte*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorByteZeroExtend(mask : Vector`1, address : Byte*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorByteZeroExtend(mask : Vector`1, address : Byte*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorByteZeroExtend(mask : Vector`1, address : Byte*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorByteZeroExtend(mask : Vector`1, address : Byte*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorByteZeroExtend(mask : Vector`1, address : Byte*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorByteZeroExtend(mask : Vector`1, address : Byte*, indices : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorByteZeroExtendFirstFaulting due to it being static, abstract and generic.

    GatherVectorByteZeroExtendFirstFaulting : GatherVectorByteZeroExtendFirstFaulting_MethodGroup
    class GatherVectorByteZeroExtendFirstFaulting_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorByteZeroExtendFirstFaulting(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], offsets: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorByteZeroExtendFirstFaulting(mask : Vector`1, address : Byte*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorByteZeroExtendFirstFaulting(mask : Vector`1, address : Byte*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorByteZeroExtendFirstFaulting(mask : Vector`1, address : Byte*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorByteZeroExtendFirstFaulting(mask : Vector`1, address : Byte*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorByteZeroExtendFirstFaulting(mask : Vector`1, address : Byte*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorByteZeroExtendFirstFaulting(mask : Vector`1, address : Byte*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorByteZeroExtendFirstFaulting(mask : Vector`1, address : Byte*, offsets : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorFirstFaulting due to it being static, abstract and generic.

    GatherVectorFirstFaulting : GatherVectorFirstFaulting_MethodGroup
    class GatherVectorFirstFaulting_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[float], addresses: Vector_1[int]) -> Vector_1[float]:...
        # Method GatherVectorFirstFaulting(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        # Method GatherVectorFirstFaulting(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float], indices: Vector_1[int]) -> Vector_1[float]:...
        # Method GatherVectorFirstFaulting(mask : Vector`1, address : Double*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorFirstFaulting(mask : Vector`1, address : Single*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorFirstFaulting(mask : Vector`1, address : Single*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorFirstFaulting(mask : Vector`1, address : Int32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorFirstFaulting(mask : Vector`1, address : Int32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorFirstFaulting(mask : Vector`1, address : Int64*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorFirstFaulting(mask : Vector`1, address : Int64*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorFirstFaulting(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorFirstFaulting(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorFirstFaulting(mask : Vector`1, address : UInt64*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorFirstFaulting(mask : Vector`1, address : UInt64*, indices : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorInt16SignExtend due to it being static, abstract and generic.

    GatherVectorInt16SignExtend : GatherVectorInt16SignExtend_MethodGroup
    class GatherVectorInt16SignExtend_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorInt16SignExtend(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorInt16SignExtend(mask : Vector`1, address : Int16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16SignExtend(mask : Vector`1, address : Int16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16SignExtend(mask : Vector`1, address : Int16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16SignExtend(mask : Vector`1, address : Int16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16SignExtend(mask : Vector`1, address : Int16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16SignExtend(mask : Vector`1, address : Int16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16SignExtend(mask : Vector`1, address : Int16*, indices : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorInt16SignExtendFirstFaulting due to it being static, abstract and generic.

    GatherVectorInt16SignExtendFirstFaulting : GatherVectorInt16SignExtendFirstFaulting_MethodGroup
    class GatherVectorInt16SignExtendFirstFaulting_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorInt16SignExtendFirstFaulting(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorInt16SignExtendFirstFaulting(mask : Vector`1, address : Int16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16SignExtendFirstFaulting(mask : Vector`1, address : Int16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16SignExtendFirstFaulting(mask : Vector`1, address : Int16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16SignExtendFirstFaulting(mask : Vector`1, address : Int16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16SignExtendFirstFaulting(mask : Vector`1, address : Int16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16SignExtendFirstFaulting(mask : Vector`1, address : Int16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16SignExtendFirstFaulting(mask : Vector`1, address : Int16*, indices : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorInt16WithByteOffsetsSignExtend due to it being static, abstract and generic.

    GatherVectorInt16WithByteOffsetsSignExtend : GatherVectorInt16WithByteOffsetsSignExtend_MethodGroup
    class GatherVectorInt16WithByteOffsetsSignExtend_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], offsets: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorInt16WithByteOffsetsSignExtend(mask : Vector`1, address : Int16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16WithByteOffsetsSignExtend(mask : Vector`1, address : Int16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16WithByteOffsetsSignExtend(mask : Vector`1, address : Int16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16WithByteOffsetsSignExtend(mask : Vector`1, address : Int16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16WithByteOffsetsSignExtend(mask : Vector`1, address : Int16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16WithByteOffsetsSignExtend(mask : Vector`1, address : Int16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16WithByteOffsetsSignExtend(mask : Vector`1, address : Int16*, offsets : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorInt16WithByteOffsetsSignExtendFirstFaulting due to it being static, abstract and generic.

    GatherVectorInt16WithByteOffsetsSignExtendFirstFaulting : GatherVectorInt16WithByteOffsetsSignExtendFirstFaulting_MethodGroup
    class GatherVectorInt16WithByteOffsetsSignExtendFirstFaulting_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], offsets: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorInt16WithByteOffsetsSignExtendFirstFaulting(mask : Vector`1, address : Int16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16WithByteOffsetsSignExtendFirstFaulting(mask : Vector`1, address : Int16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16WithByteOffsetsSignExtendFirstFaulting(mask : Vector`1, address : Int16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16WithByteOffsetsSignExtendFirstFaulting(mask : Vector`1, address : Int16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16WithByteOffsetsSignExtendFirstFaulting(mask : Vector`1, address : Int16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16WithByteOffsetsSignExtendFirstFaulting(mask : Vector`1, address : Int16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt16WithByteOffsetsSignExtendFirstFaulting(mask : Vector`1, address : Int16*, offsets : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorInt32SignExtend due to it being static, abstract and generic.

    GatherVectorInt32SignExtend : GatherVectorInt32SignExtend_MethodGroup
    class GatherVectorInt32SignExtend_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorInt32SignExtend(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorInt32SignExtend(mask : Vector`1, address : Int32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt32SignExtend(mask : Vector`1, address : Int32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt32SignExtend(mask : Vector`1, address : Int32*, indices : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorInt32SignExtendFirstFaulting due to it being static, abstract and generic.

    GatherVectorInt32SignExtendFirstFaulting : GatherVectorInt32SignExtendFirstFaulting_MethodGroup
    class GatherVectorInt32SignExtendFirstFaulting_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorInt32SignExtendFirstFaulting(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorInt32SignExtendFirstFaulting(mask : Vector`1, address : Int32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt32SignExtendFirstFaulting(mask : Vector`1, address : Int32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt32SignExtendFirstFaulting(mask : Vector`1, address : Int32*, indices : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorInt32WithByteOffsetsSignExtend due to it being static, abstract and generic.

    GatherVectorInt32WithByteOffsetsSignExtend : GatherVectorInt32WithByteOffsetsSignExtend_MethodGroup
    class GatherVectorInt32WithByteOffsetsSignExtend_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], offsets: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorInt32WithByteOffsetsSignExtend(mask : Vector`1, address : Int32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt32WithByteOffsetsSignExtend(mask : Vector`1, address : Int32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt32WithByteOffsetsSignExtend(mask : Vector`1, address : Int32*, offsets : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorInt32WithByteOffsetsSignExtendFirstFaulting due to it being static, abstract and generic.

    GatherVectorInt32WithByteOffsetsSignExtendFirstFaulting : GatherVectorInt32WithByteOffsetsSignExtendFirstFaulting_MethodGroup
    class GatherVectorInt32WithByteOffsetsSignExtendFirstFaulting_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], offsets: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorInt32WithByteOffsetsSignExtendFirstFaulting(mask : Vector`1, address : Int32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt32WithByteOffsetsSignExtendFirstFaulting(mask : Vector`1, address : Int32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorInt32WithByteOffsetsSignExtendFirstFaulting(mask : Vector`1, address : Int32*, offsets : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorSByteSignExtend due to it being static, abstract and generic.

    GatherVectorSByteSignExtend : GatherVectorSByteSignExtend_MethodGroup
    class GatherVectorSByteSignExtend_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorSByteSignExtend(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorSByteSignExtend(mask : Vector`1, address : SByte*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorSByteSignExtend(mask : Vector`1, address : SByte*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorSByteSignExtend(mask : Vector`1, address : SByte*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorSByteSignExtend(mask : Vector`1, address : SByte*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorSByteSignExtend(mask : Vector`1, address : SByte*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorSByteSignExtend(mask : Vector`1, address : SByte*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorSByteSignExtend(mask : Vector`1, address : SByte*, indices : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorSByteSignExtendFirstFaulting due to it being static, abstract and generic.

    GatherVectorSByteSignExtendFirstFaulting : GatherVectorSByteSignExtendFirstFaulting_MethodGroup
    class GatherVectorSByteSignExtendFirstFaulting_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorSByteSignExtendFirstFaulting(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], offsets: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorSByteSignExtendFirstFaulting(mask : Vector`1, address : SByte*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorSByteSignExtendFirstFaulting(mask : Vector`1, address : SByte*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorSByteSignExtendFirstFaulting(mask : Vector`1, address : SByte*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorSByteSignExtendFirstFaulting(mask : Vector`1, address : SByte*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorSByteSignExtendFirstFaulting(mask : Vector`1, address : SByte*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorSByteSignExtendFirstFaulting(mask : Vector`1, address : SByte*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorSByteSignExtendFirstFaulting(mask : Vector`1, address : SByte*, offsets : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorUInt16WithByteOffsetsZeroExtend due to it being static, abstract and generic.

    GatherVectorUInt16WithByteOffsetsZeroExtend : GatherVectorUInt16WithByteOffsetsZeroExtend_MethodGroup
    class GatherVectorUInt16WithByteOffsetsZeroExtend_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], offsets: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorUInt16WithByteOffsetsZeroExtend(mask : Vector`1, address : UInt16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16WithByteOffsetsZeroExtend(mask : Vector`1, address : UInt16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16WithByteOffsetsZeroExtend(mask : Vector`1, address : UInt16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16WithByteOffsetsZeroExtend(mask : Vector`1, address : UInt16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16WithByteOffsetsZeroExtend(mask : Vector`1, address : UInt16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16WithByteOffsetsZeroExtend(mask : Vector`1, address : UInt16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16WithByteOffsetsZeroExtend(mask : Vector`1, address : UInt16*, offsets : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorUInt16WithByteOffsetsZeroExtendFirstFaulting due to it being static, abstract and generic.

    GatherVectorUInt16WithByteOffsetsZeroExtendFirstFaulting : GatherVectorUInt16WithByteOffsetsZeroExtendFirstFaulting_MethodGroup
    class GatherVectorUInt16WithByteOffsetsZeroExtendFirstFaulting_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], offsets: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorUInt16WithByteOffsetsZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16WithByteOffsetsZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16WithByteOffsetsZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16WithByteOffsetsZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16WithByteOffsetsZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16WithByteOffsetsZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16WithByteOffsetsZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*, offsets : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorUInt16ZeroExtend due to it being static, abstract and generic.

    GatherVectorUInt16ZeroExtend : GatherVectorUInt16ZeroExtend_MethodGroup
    class GatherVectorUInt16ZeroExtend_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorUInt16ZeroExtend(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorUInt16ZeroExtend(mask : Vector`1, address : UInt16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16ZeroExtend(mask : Vector`1, address : UInt16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16ZeroExtend(mask : Vector`1, address : UInt16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16ZeroExtend(mask : Vector`1, address : UInt16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16ZeroExtend(mask : Vector`1, address : UInt16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16ZeroExtend(mask : Vector`1, address : UInt16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16ZeroExtend(mask : Vector`1, address : UInt16*, indices : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorUInt16ZeroExtendFirstFaulting due to it being static, abstract and generic.

    GatherVectorUInt16ZeroExtendFirstFaulting : GatherVectorUInt16ZeroExtendFirstFaulting_MethodGroup
    class GatherVectorUInt16ZeroExtendFirstFaulting_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorUInt16ZeroExtendFirstFaulting(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorUInt16ZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16ZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16ZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16ZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16ZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16ZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt16ZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*, indices : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorUInt32WithByteOffsetsZeroExtend due to it being static, abstract and generic.

    GatherVectorUInt32WithByteOffsetsZeroExtend : GatherVectorUInt32WithByteOffsetsZeroExtend_MethodGroup
    class GatherVectorUInt32WithByteOffsetsZeroExtend_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], offsets: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorUInt32WithByteOffsetsZeroExtend(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32WithByteOffsetsZeroExtend(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32WithByteOffsetsZeroExtend(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32WithByteOffsetsZeroExtend(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32WithByteOffsetsZeroExtend(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32WithByteOffsetsZeroExtend(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32WithByteOffsetsZeroExtend(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorUInt32WithByteOffsetsZeroExtendFirstFaulting due to it being static, abstract and generic.

    GatherVectorUInt32WithByteOffsetsZeroExtendFirstFaulting : GatherVectorUInt32WithByteOffsetsZeroExtendFirstFaulting_MethodGroup
    class GatherVectorUInt32WithByteOffsetsZeroExtendFirstFaulting_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], offsets: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorUInt32WithByteOffsetsZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32WithByteOffsetsZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32WithByteOffsetsZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32WithByteOffsetsZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32WithByteOffsetsZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32WithByteOffsetsZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32WithByteOffsetsZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorUInt32ZeroExtend due to it being static, abstract and generic.

    GatherVectorUInt32ZeroExtend : GatherVectorUInt32ZeroExtend_MethodGroup
    class GatherVectorUInt32ZeroExtend_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorUInt32ZeroExtend(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorUInt32ZeroExtend(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32ZeroExtend(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32ZeroExtend(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32ZeroExtend(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32ZeroExtend(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32ZeroExtend(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32ZeroExtend(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorUInt32ZeroExtendFirstFaulting due to it being static, abstract and generic.

    GatherVectorUInt32ZeroExtendFirstFaulting : GatherVectorUInt32ZeroExtendFirstFaulting_MethodGroup
    class GatherVectorUInt32ZeroExtendFirstFaulting_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorUInt32ZeroExtendFirstFaulting(mask : Vector`1, addresses : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method GatherVectorUInt32ZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32ZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32ZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32ZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32ZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32ZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method
        # Method GatherVectorUInt32ZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*, indices : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorWithByteOffsetFirstFaulting due to it being static, abstract and generic.

    GatherVectorWithByteOffsetFirstFaulting : GatherVectorWithByteOffsetFirstFaulting_MethodGroup
    class GatherVectorWithByteOffsetFirstFaulting_MethodGroup:
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float], offsets: Vector_1[int]) -> Vector_1[float]:...
        # Method GatherVectorWithByteOffsetFirstFaulting(mask : Vector`1, address : Double*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsetFirstFaulting(mask : Vector`1, address : Single*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsetFirstFaulting(mask : Vector`1, address : Single*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsetFirstFaulting(mask : Vector`1, address : Int32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsetFirstFaulting(mask : Vector`1, address : Int32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsetFirstFaulting(mask : Vector`1, address : Int64*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsetFirstFaulting(mask : Vector`1, address : Int64*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsetFirstFaulting(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsetFirstFaulting(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsetFirstFaulting(mask : Vector`1, address : UInt64*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsetFirstFaulting(mask : Vector`1, address : UInt64*, offsets : Vector`1) was skipped since it collides with above method

    # Skipped GatherVectorWithByteOffsets due to it being static, abstract and generic.

    GatherVectorWithByteOffsets : GatherVectorWithByteOffsets_MethodGroup
    class GatherVectorWithByteOffsets_MethodGroup:
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float], offsets: Vector_1[int]) -> Vector_1[float]:...
        # Method GatherVectorWithByteOffsets(mask : Vector`1, address : Double*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsets(mask : Vector`1, address : Single*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsets(mask : Vector`1, address : Single*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsets(mask : Vector`1, address : Int32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsets(mask : Vector`1, address : Int32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsets(mask : Vector`1, address : Int64*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsets(mask : Vector`1, address : Int64*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsets(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsets(mask : Vector`1, address : UInt32*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsets(mask : Vector`1, address : UInt64*, offsets : Vector`1) was skipped since it collides with above method
        # Method GatherVectorWithByteOffsets(mask : Vector`1, address : UInt64*, offsets : Vector`1) was skipped since it collides with above method

    # Skipped GetActiveElementCount due to it being static, abstract and generic.

    GetActiveElementCount : GetActiveElementCount_MethodGroup
    class GetActiveElementCount_MethodGroup:
        def __call__(self, mask: Vector_1[float], from_: Vector_1[float]) -> int:...
        # Method GetActiveElementCount(mask : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method GetActiveElementCount(mask : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method GetActiveElementCount(mask : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method GetActiveElementCount(mask : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method GetActiveElementCount(mask : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method GetActiveElementCount(mask : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method GetActiveElementCount(mask : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method GetActiveElementCount(mask : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method GetActiveElementCount(mask : Vector`1, from : Vector`1) was skipped since it collides with above method

    # Skipped InsertIntoShiftedVector due to it being static, abstract and generic.

    InsertIntoShiftedVector : InsertIntoShiftedVector_MethodGroup
    class InsertIntoShiftedVector_MethodGroup:
        def __call__(self, left: Vector_1[float], right: float) -> Vector_1[float]:...
        # Method InsertIntoShiftedVector(left : Vector`1, right : Single) was skipped since it collides with above method
        # Method InsertIntoShiftedVector(left : Vector`1, right : Byte) was skipped since it collides with above method
        # Method InsertIntoShiftedVector(left : Vector`1, right : Int16) was skipped since it collides with above method
        # Method InsertIntoShiftedVector(left : Vector`1, right : Int32) was skipped since it collides with above method
        # Method InsertIntoShiftedVector(left : Vector`1, right : Int64) was skipped since it collides with above method
        # Method InsertIntoShiftedVector(left : Vector`1, right : SByte) was skipped since it collides with above method
        # Method InsertIntoShiftedVector(left : Vector`1, right : UInt16) was skipped since it collides with above method
        # Method InsertIntoShiftedVector(left : Vector`1, right : UInt32) was skipped since it collides with above method
        # Method InsertIntoShiftedVector(left : Vector`1, right : UInt64) was skipped since it collides with above method

    # Skipped LeadingSignCount due to it being static, abstract and generic.

    LeadingSignCount : LeadingSignCount_MethodGroup
    class LeadingSignCount_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method LeadingSignCount(value : Vector`1) was skipped since it collides with above method
        # Method LeadingSignCount(value : Vector`1) was skipped since it collides with above method
        # Method LeadingSignCount(value : Vector`1) was skipped since it collides with above method

    # Skipped LeadingZeroCount due to it being static, abstract and generic.

    LeadingZeroCount : LeadingZeroCount_MethodGroup
    class LeadingZeroCount_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method LeadingZeroCount(value : Vector`1) was skipped since it collides with above method
        # Method LeadingZeroCount(value : Vector`1) was skipped since it collides with above method
        # Method LeadingZeroCount(value : Vector`1) was skipped since it collides with above method
        # Method LeadingZeroCount(value : Vector`1) was skipped since it collides with above method
        # Method LeadingZeroCount(value : Vector`1) was skipped since it collides with above method
        # Method LeadingZeroCount(value : Vector`1) was skipped since it collides with above method
        # Method LeadingZeroCount(value : Vector`1) was skipped since it collides with above method

    # Skipped Load2xVectorAndUnzip due to it being static, abstract and generic.

    Load2xVectorAndUnzip : Load2xVectorAndUnzip_MethodGroup
    class Load2xVectorAndUnzip_MethodGroup:
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float]) -> ValueTuple_2[Vector_1[float], Vector_1[float]]:...
        # Method Load2xVectorAndUnzip(mask : Vector`1, address : Single*) was skipped since it collides with above method
        # Method Load2xVectorAndUnzip(mask : Vector`1, address : Byte*) was skipped since it collides with above method
        # Method Load2xVectorAndUnzip(mask : Vector`1, address : Int16*) was skipped since it collides with above method
        # Method Load2xVectorAndUnzip(mask : Vector`1, address : Int32*) was skipped since it collides with above method
        # Method Load2xVectorAndUnzip(mask : Vector`1, address : Int64*) was skipped since it collides with above method
        # Method Load2xVectorAndUnzip(mask : Vector`1, address : SByte*) was skipped since it collides with above method
        # Method Load2xVectorAndUnzip(mask : Vector`1, address : UInt16*) was skipped since it collides with above method
        # Method Load2xVectorAndUnzip(mask : Vector`1, address : UInt32*) was skipped since it collides with above method
        # Method Load2xVectorAndUnzip(mask : Vector`1, address : UInt64*) was skipped since it collides with above method

    # Skipped Load3xVectorAndUnzip due to it being static, abstract and generic.

    Load3xVectorAndUnzip : Load3xVectorAndUnzip_MethodGroup
    class Load3xVectorAndUnzip_MethodGroup:
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float]) -> ValueTuple_3[Vector_1[float], Vector_1[float], Vector_1[float]]:...
        # Method Load3xVectorAndUnzip(mask : Vector`1, address : Single*) was skipped since it collides with above method
        # Method Load3xVectorAndUnzip(mask : Vector`1, address : Byte*) was skipped since it collides with above method
        # Method Load3xVectorAndUnzip(mask : Vector`1, address : Int16*) was skipped since it collides with above method
        # Method Load3xVectorAndUnzip(mask : Vector`1, address : Int32*) was skipped since it collides with above method
        # Method Load3xVectorAndUnzip(mask : Vector`1, address : Int64*) was skipped since it collides with above method
        # Method Load3xVectorAndUnzip(mask : Vector`1, address : SByte*) was skipped since it collides with above method
        # Method Load3xVectorAndUnzip(mask : Vector`1, address : UInt16*) was skipped since it collides with above method
        # Method Load3xVectorAndUnzip(mask : Vector`1, address : UInt32*) was skipped since it collides with above method
        # Method Load3xVectorAndUnzip(mask : Vector`1, address : UInt64*) was skipped since it collides with above method

    # Skipped Load4xVectorAndUnzip due to it being static, abstract and generic.

    Load4xVectorAndUnzip : Load4xVectorAndUnzip_MethodGroup
    class Load4xVectorAndUnzip_MethodGroup:
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float]) -> ValueTuple_4[Vector_1[float], Vector_1[float], Vector_1[float], Vector_1[float]]:...
        # Method Load4xVectorAndUnzip(mask : Vector`1, address : Single*) was skipped since it collides with above method
        # Method Load4xVectorAndUnzip(mask : Vector`1, address : Byte*) was skipped since it collides with above method
        # Method Load4xVectorAndUnzip(mask : Vector`1, address : Int16*) was skipped since it collides with above method
        # Method Load4xVectorAndUnzip(mask : Vector`1, address : Int32*) was skipped since it collides with above method
        # Method Load4xVectorAndUnzip(mask : Vector`1, address : Int64*) was skipped since it collides with above method
        # Method Load4xVectorAndUnzip(mask : Vector`1, address : SByte*) was skipped since it collides with above method
        # Method Load4xVectorAndUnzip(mask : Vector`1, address : UInt16*) was skipped since it collides with above method
        # Method Load4xVectorAndUnzip(mask : Vector`1, address : UInt32*) was skipped since it collides with above method
        # Method Load4xVectorAndUnzip(mask : Vector`1, address : UInt64*) was skipped since it collides with above method

    # Skipped LoadVector due to it being static, abstract and generic.

    LoadVector : LoadVector_MethodGroup
    class LoadVector_MethodGroup:
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float]) -> Vector_1[float]:...
        # Method LoadVector(mask : Vector`1, address : Single*) was skipped since it collides with above method
        # Method LoadVector(mask : Vector`1, address : Byte*) was skipped since it collides with above method
        # Method LoadVector(mask : Vector`1, address : Int16*) was skipped since it collides with above method
        # Method LoadVector(mask : Vector`1, address : Int32*) was skipped since it collides with above method
        # Method LoadVector(mask : Vector`1, address : Int64*) was skipped since it collides with above method
        # Method LoadVector(mask : Vector`1, address : SByte*) was skipped since it collides with above method
        # Method LoadVector(mask : Vector`1, address : UInt16*) was skipped since it collides with above method
        # Method LoadVector(mask : Vector`1, address : UInt32*) was skipped since it collides with above method
        # Method LoadVector(mask : Vector`1, address : UInt64*) was skipped since it collides with above method

    # Skipped LoadVector128AndReplicateToVector due to it being static, abstract and generic.

    LoadVector128AndReplicateToVector : LoadVector128AndReplicateToVector_MethodGroup
    class LoadVector128AndReplicateToVector_MethodGroup:
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float]) -> Vector_1[float]:...
        # Method LoadVector128AndReplicateToVector(mask : Vector`1, address : Single*) was skipped since it collides with above method
        # Method LoadVector128AndReplicateToVector(mask : Vector`1, address : Byte*) was skipped since it collides with above method
        # Method LoadVector128AndReplicateToVector(mask : Vector`1, address : Int16*) was skipped since it collides with above method
        # Method LoadVector128AndReplicateToVector(mask : Vector`1, address : Int32*) was skipped since it collides with above method
        # Method LoadVector128AndReplicateToVector(mask : Vector`1, address : Int64*) was skipped since it collides with above method
        # Method LoadVector128AndReplicateToVector(mask : Vector`1, address : SByte*) was skipped since it collides with above method
        # Method LoadVector128AndReplicateToVector(mask : Vector`1, address : UInt16*) was skipped since it collides with above method
        # Method LoadVector128AndReplicateToVector(mask : Vector`1, address : UInt32*) was skipped since it collides with above method
        # Method LoadVector128AndReplicateToVector(mask : Vector`1, address : UInt64*) was skipped since it collides with above method

    # Skipped LoadVectorByteZeroExtendFirstFaulting due to it being static, abstract and generic.

    LoadVectorByteZeroExtendFirstFaulting : LoadVectorByteZeroExtendFirstFaulting_MethodGroup
    class LoadVectorByteZeroExtendFirstFaulting_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]:...
        # Method LoadVectorByteZeroExtendFirstFaulting(mask : Vector`1, address : Byte*) was skipped since it collides with above method
        # Method LoadVectorByteZeroExtendFirstFaulting(mask : Vector`1, address : Byte*) was skipped since it collides with above method
        # Method LoadVectorByteZeroExtendFirstFaulting(mask : Vector`1, address : Byte*) was skipped since it collides with above method
        # Method LoadVectorByteZeroExtendFirstFaulting(mask : Vector`1, address : Byte*) was skipped since it collides with above method
        # Method LoadVectorByteZeroExtendFirstFaulting(mask : Vector`1, address : Byte*) was skipped since it collides with above method

    # Skipped LoadVectorFirstFaulting due to it being static, abstract and generic.

    LoadVectorFirstFaulting : LoadVectorFirstFaulting_MethodGroup
    class LoadVectorFirstFaulting_MethodGroup:
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float]) -> Vector_1[float]:...
        # Method LoadVectorFirstFaulting(mask : Vector`1, address : Single*) was skipped since it collides with above method
        # Method LoadVectorFirstFaulting(mask : Vector`1, address : Byte*) was skipped since it collides with above method
        # Method LoadVectorFirstFaulting(mask : Vector`1, address : Int16*) was skipped since it collides with above method
        # Method LoadVectorFirstFaulting(mask : Vector`1, address : Int32*) was skipped since it collides with above method
        # Method LoadVectorFirstFaulting(mask : Vector`1, address : Int64*) was skipped since it collides with above method
        # Method LoadVectorFirstFaulting(mask : Vector`1, address : SByte*) was skipped since it collides with above method
        # Method LoadVectorFirstFaulting(mask : Vector`1, address : UInt16*) was skipped since it collides with above method
        # Method LoadVectorFirstFaulting(mask : Vector`1, address : UInt32*) was skipped since it collides with above method
        # Method LoadVectorFirstFaulting(mask : Vector`1, address : UInt64*) was skipped since it collides with above method

    # Skipped LoadVectorInt16SignExtendFirstFaulting due to it being static, abstract and generic.

    LoadVectorInt16SignExtendFirstFaulting : LoadVectorInt16SignExtendFirstFaulting_MethodGroup
    class LoadVectorInt16SignExtendFirstFaulting_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]:...
        # Method LoadVectorInt16SignExtendFirstFaulting(mask : Vector`1, address : Int16*) was skipped since it collides with above method
        # Method LoadVectorInt16SignExtendFirstFaulting(mask : Vector`1, address : Int16*) was skipped since it collides with above method
        # Method LoadVectorInt16SignExtendFirstFaulting(mask : Vector`1, address : Int16*) was skipped since it collides with above method

    # Skipped LoadVectorInt32SignExtendFirstFaulting due to it being static, abstract and generic.

    LoadVectorInt32SignExtendFirstFaulting : LoadVectorInt32SignExtendFirstFaulting_MethodGroup
    class LoadVectorInt32SignExtendFirstFaulting_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]:...
        # Method LoadVectorInt32SignExtendFirstFaulting(mask : Vector`1, address : Int32*) was skipped since it collides with above method

    # Skipped LoadVectorNonFaulting due to it being static, abstract and generic.

    LoadVectorNonFaulting : LoadVectorNonFaulting_MethodGroup
    class LoadVectorNonFaulting_MethodGroup:
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float]) -> Vector_1[float]:...
        # Method LoadVectorNonFaulting(mask : Vector`1, address : Single*) was skipped since it collides with above method
        # Method LoadVectorNonFaulting(mask : Vector`1, address : Byte*) was skipped since it collides with above method
        # Method LoadVectorNonFaulting(mask : Vector`1, address : Int16*) was skipped since it collides with above method
        # Method LoadVectorNonFaulting(mask : Vector`1, address : Int32*) was skipped since it collides with above method
        # Method LoadVectorNonFaulting(mask : Vector`1, address : Int64*) was skipped since it collides with above method
        # Method LoadVectorNonFaulting(mask : Vector`1, address : SByte*) was skipped since it collides with above method
        # Method LoadVectorNonFaulting(mask : Vector`1, address : UInt16*) was skipped since it collides with above method
        # Method LoadVectorNonFaulting(mask : Vector`1, address : UInt32*) was skipped since it collides with above method
        # Method LoadVectorNonFaulting(mask : Vector`1, address : UInt64*) was skipped since it collides with above method

    # Skipped LoadVectorNonTemporal due to it being static, abstract and generic.

    LoadVectorNonTemporal : LoadVectorNonTemporal_MethodGroup
    class LoadVectorNonTemporal_MethodGroup:
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float]) -> Vector_1[float]:...
        # Method LoadVectorNonTemporal(mask : Vector`1, address : Single*) was skipped since it collides with above method
        # Method LoadVectorNonTemporal(mask : Vector`1, address : Byte*) was skipped since it collides with above method
        # Method LoadVectorNonTemporal(mask : Vector`1, address : Int16*) was skipped since it collides with above method
        # Method LoadVectorNonTemporal(mask : Vector`1, address : Int32*) was skipped since it collides with above method
        # Method LoadVectorNonTemporal(mask : Vector`1, address : Int64*) was skipped since it collides with above method
        # Method LoadVectorNonTemporal(mask : Vector`1, address : SByte*) was skipped since it collides with above method
        # Method LoadVectorNonTemporal(mask : Vector`1, address : UInt16*) was skipped since it collides with above method
        # Method LoadVectorNonTemporal(mask : Vector`1, address : UInt32*) was skipped since it collides with above method
        # Method LoadVectorNonTemporal(mask : Vector`1, address : UInt64*) was skipped since it collides with above method

    # Skipped LoadVectorSByteSignExtendFirstFaulting due to it being static, abstract and generic.

    LoadVectorSByteSignExtendFirstFaulting : LoadVectorSByteSignExtendFirstFaulting_MethodGroup
    class LoadVectorSByteSignExtendFirstFaulting_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]:...
        # Method LoadVectorSByteSignExtendFirstFaulting(mask : Vector`1, address : SByte*) was skipped since it collides with above method
        # Method LoadVectorSByteSignExtendFirstFaulting(mask : Vector`1, address : SByte*) was skipped since it collides with above method
        # Method LoadVectorSByteSignExtendFirstFaulting(mask : Vector`1, address : SByte*) was skipped since it collides with above method
        # Method LoadVectorSByteSignExtendFirstFaulting(mask : Vector`1, address : SByte*) was skipped since it collides with above method
        # Method LoadVectorSByteSignExtendFirstFaulting(mask : Vector`1, address : SByte*) was skipped since it collides with above method

    # Skipped LoadVectorUInt16ZeroExtendFirstFaulting due to it being static, abstract and generic.

    LoadVectorUInt16ZeroExtendFirstFaulting : LoadVectorUInt16ZeroExtendFirstFaulting_MethodGroup
    class LoadVectorUInt16ZeroExtendFirstFaulting_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]:...
        # Method LoadVectorUInt16ZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*) was skipped since it collides with above method
        # Method LoadVectorUInt16ZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*) was skipped since it collides with above method
        # Method LoadVectorUInt16ZeroExtendFirstFaulting(mask : Vector`1, address : UInt16*) was skipped since it collides with above method

    # Skipped LoadVectorUInt32ZeroExtendFirstFaulting due to it being static, abstract and generic.

    LoadVectorUInt32ZeroExtendFirstFaulting : LoadVectorUInt32ZeroExtendFirstFaulting_MethodGroup
    class LoadVectorUInt32ZeroExtendFirstFaulting_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int]) -> Vector_1[int]:...
        # Method LoadVectorUInt32ZeroExtendFirstFaulting(mask : Vector`1, address : UInt32*) was skipped since it collides with above method

    # Skipped Max due to it being static, abstract and generic.

    Max : Max_MethodGroup
    class Max_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method Max(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Max(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Max(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Max(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Max(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Max(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Max(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Max(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Max(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MaxAcross due to it being static, abstract and generic.

    MaxAcross : MaxAcross_MethodGroup
    class MaxAcross_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method MaxAcross(value : Vector`1) was skipped since it collides with above method
        # Method MaxAcross(value : Vector`1) was skipped since it collides with above method
        # Method MaxAcross(value : Vector`1) was skipped since it collides with above method
        # Method MaxAcross(value : Vector`1) was skipped since it collides with above method
        # Method MaxAcross(value : Vector`1) was skipped since it collides with above method
        # Method MaxAcross(value : Vector`1) was skipped since it collides with above method
        # Method MaxAcross(value : Vector`1) was skipped since it collides with above method
        # Method MaxAcross(value : Vector`1) was skipped since it collides with above method
        # Method MaxAcross(value : Vector`1) was skipped since it collides with above method

    # Skipped MaxNumber due to it being static, abstract and generic.

    MaxNumber : MaxNumber_MethodGroup
    class MaxNumber_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method MaxNumber(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MaxNumberAcross due to it being static, abstract and generic.

    MaxNumberAcross : MaxNumberAcross_MethodGroup
    class MaxNumberAcross_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method MaxNumberAcross(value : Vector`1) was skipped since it collides with above method

    # Skipped Min due to it being static, abstract and generic.

    Min : Min_MethodGroup
    class Min_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method Min(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Min(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Min(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Min(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Min(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Min(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Min(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Min(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Min(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MinAcross due to it being static, abstract and generic.

    MinAcross : MinAcross_MethodGroup
    class MinAcross_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method MinAcross(value : Vector`1) was skipped since it collides with above method
        # Method MinAcross(value : Vector`1) was skipped since it collides with above method
        # Method MinAcross(value : Vector`1) was skipped since it collides with above method
        # Method MinAcross(value : Vector`1) was skipped since it collides with above method
        # Method MinAcross(value : Vector`1) was skipped since it collides with above method
        # Method MinAcross(value : Vector`1) was skipped since it collides with above method
        # Method MinAcross(value : Vector`1) was skipped since it collides with above method
        # Method MinAcross(value : Vector`1) was skipped since it collides with above method
        # Method MinAcross(value : Vector`1) was skipped since it collides with above method

    # Skipped MinNumber due to it being static, abstract and generic.

    MinNumber : MinNumber_MethodGroup
    class MinNumber_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method MinNumber(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MinNumberAcross due to it being static, abstract and generic.

    MinNumberAcross : MinNumberAcross_MethodGroup
    class MinNumberAcross_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method MinNumberAcross(value : Vector`1) was skipped since it collides with above method

    # Skipped Multiply due to it being static, abstract and generic.

    Multiply : Multiply_MethodGroup
    class Multiply_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method Multiply(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Multiply(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Multiply(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Multiply(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Multiply(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Multiply(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Multiply(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Multiply(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Multiply(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyAdd due to it being static, abstract and generic.

    MultiplyAdd : MultiplyAdd_MethodGroup
    class MultiplyAdd_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyAddRotateComplex due to it being static, abstract and generic.

    MultiplyAddRotateComplex : MultiplyAddRotateComplex_MethodGroup
    class MultiplyAddRotateComplex_MethodGroup:
        def __call__(self, addend: Vector_1[float], left: Vector_1[float], right: Vector_1[float], rotation: int) -> Vector_1[float]:...
        # Method MultiplyAddRotateComplex(addend : Vector`1, left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalar due to it being static, abstract and generic.

    MultiplyBySelectedScalar : MultiplyBySelectedScalar_MethodGroup
    class MultiplyBySelectedScalar_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float], rightIndex: int) -> Vector_1[float]:...
        # Method MultiplyBySelectedScalar(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyExtended due to it being static, abstract and generic.

    MultiplyExtended : MultiplyExtended_MethodGroup
    class MultiplyExtended_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method MultiplyExtended(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplySubtract due to it being static, abstract and generic.

    MultiplySubtract : MultiplySubtract_MethodGroup
    class MultiplySubtract_MethodGroup:
        def __call__(self, minuend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplySubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplySubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplySubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplySubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplySubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplySubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplySubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped Negate due to it being static, abstract and generic.

    Negate : Negate_MethodGroup
    class Negate_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method Negate(value : Vector`1) was skipped since it collides with above method
        # Method Negate(value : Vector`1) was skipped since it collides with above method
        # Method Negate(value : Vector`1) was skipped since it collides with above method
        # Method Negate(value : Vector`1) was skipped since it collides with above method
        # Method Negate(value : Vector`1) was skipped since it collides with above method

    # Skipped Not due to it being static, abstract and generic.

    Not : Not_MethodGroup
    class Not_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method Not(value : Vector`1) was skipped since it collides with above method
        # Method Not(value : Vector`1) was skipped since it collides with above method
        # Method Not(value : Vector`1) was skipped since it collides with above method
        # Method Not(value : Vector`1) was skipped since it collides with above method
        # Method Not(value : Vector`1) was skipped since it collides with above method
        # Method Not(value : Vector`1) was skipped since it collides with above method
        # Method Not(value : Vector`1) was skipped since it collides with above method

    # Skipped Or due to it being static, abstract and generic.

    Or : Or_MethodGroup
    class Or_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method Or(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Or(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Or(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Or(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Or(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Or(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Or(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped OrAcross due to it being static, abstract and generic.

    OrAcross : OrAcross_MethodGroup
    class OrAcross_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method OrAcross(value : Vector`1) was skipped since it collides with above method
        # Method OrAcross(value : Vector`1) was skipped since it collides with above method
        # Method OrAcross(value : Vector`1) was skipped since it collides with above method
        # Method OrAcross(value : Vector`1) was skipped since it collides with above method
        # Method OrAcross(value : Vector`1) was skipped since it collides with above method
        # Method OrAcross(value : Vector`1) was skipped since it collides with above method
        # Method OrAcross(value : Vector`1) was skipped since it collides with above method

    # Skipped PopCount due to it being static, abstract and generic.

    PopCount : PopCount_MethodGroup
    class PopCount_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[int]:...
        # Method PopCount(value : Vector`1) was skipped since it collides with above method
        # Method PopCount(value : Vector`1) was skipped since it collides with above method
        # Method PopCount(value : Vector`1) was skipped since it collides with above method
        # Method PopCount(value : Vector`1) was skipped since it collides with above method
        # Method PopCount(value : Vector`1) was skipped since it collides with above method
        # Method PopCount(value : Vector`1) was skipped since it collides with above method
        # Method PopCount(value : Vector`1) was skipped since it collides with above method
        # Method PopCount(value : Vector`1) was skipped since it collides with above method
        # Method PopCount(value : Vector`1) was skipped since it collides with above method

    # Skipped ReciprocalEstimate due to it being static, abstract and generic.

    ReciprocalEstimate : ReciprocalEstimate_MethodGroup
    class ReciprocalEstimate_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method ReciprocalEstimate(value : Vector`1) was skipped since it collides with above method

    # Skipped ReciprocalExponent due to it being static, abstract and generic.

    ReciprocalExponent : ReciprocalExponent_MethodGroup
    class ReciprocalExponent_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method ReciprocalExponent(value : Vector`1) was skipped since it collides with above method

    # Skipped ReciprocalSqrtEstimate due to it being static, abstract and generic.

    ReciprocalSqrtEstimate : ReciprocalSqrtEstimate_MethodGroup
    class ReciprocalSqrtEstimate_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method ReciprocalSqrtEstimate(value : Vector`1) was skipped since it collides with above method

    # Skipped ReciprocalSqrtStep due to it being static, abstract and generic.

    ReciprocalSqrtStep : ReciprocalSqrtStep_MethodGroup
    class ReciprocalSqrtStep_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method ReciprocalSqrtStep(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped ReciprocalStep due to it being static, abstract and generic.

    ReciprocalStep : ReciprocalStep_MethodGroup
    class ReciprocalStep_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method ReciprocalStep(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped ReverseBits due to it being static, abstract and generic.

    ReverseBits : ReverseBits_MethodGroup
    class ReverseBits_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method ReverseBits(value : Vector`1) was skipped since it collides with above method
        # Method ReverseBits(value : Vector`1) was skipped since it collides with above method
        # Method ReverseBits(value : Vector`1) was skipped since it collides with above method
        # Method ReverseBits(value : Vector`1) was skipped since it collides with above method
        # Method ReverseBits(value : Vector`1) was skipped since it collides with above method
        # Method ReverseBits(value : Vector`1) was skipped since it collides with above method
        # Method ReverseBits(value : Vector`1) was skipped since it collides with above method

    # Skipped ReverseElement due to it being static, abstract and generic.

    ReverseElement : ReverseElement_MethodGroup
    class ReverseElement_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method ReverseElement(value : Vector`1) was skipped since it collides with above method
        # Method ReverseElement(value : Vector`1) was skipped since it collides with above method
        # Method ReverseElement(value : Vector`1) was skipped since it collides with above method
        # Method ReverseElement(value : Vector`1) was skipped since it collides with above method
        # Method ReverseElement(value : Vector`1) was skipped since it collides with above method
        # Method ReverseElement(value : Vector`1) was skipped since it collides with above method
        # Method ReverseElement(value : Vector`1) was skipped since it collides with above method
        # Method ReverseElement(value : Vector`1) was skipped since it collides with above method
        # Method ReverseElement(value : Vector`1) was skipped since it collides with above method

    # Skipped ReverseElement16 due to it being static, abstract and generic.

    ReverseElement16 : ReverseElement16_MethodGroup
    class ReverseElement16_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method ReverseElement16(value : Vector`1) was skipped since it collides with above method
        # Method ReverseElement16(value : Vector`1) was skipped since it collides with above method
        # Method ReverseElement16(value : Vector`1) was skipped since it collides with above method

    # Skipped ReverseElement32 due to it being static, abstract and generic.

    ReverseElement32 : ReverseElement32_MethodGroup
    class ReverseElement32_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method ReverseElement32(value : Vector`1) was skipped since it collides with above method

    # Skipped ReverseElement8 due to it being static, abstract and generic.

    ReverseElement8 : ReverseElement8_MethodGroup
    class ReverseElement8_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method ReverseElement8(value : Vector`1) was skipped since it collides with above method
        # Method ReverseElement8(value : Vector`1) was skipped since it collides with above method
        # Method ReverseElement8(value : Vector`1) was skipped since it collides with above method
        # Method ReverseElement8(value : Vector`1) was skipped since it collides with above method
        # Method ReverseElement8(value : Vector`1) was skipped since it collides with above method

    # Skipped RoundAwayFromZero due to it being static, abstract and generic.

    RoundAwayFromZero : RoundAwayFromZero_MethodGroup
    class RoundAwayFromZero_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method RoundAwayFromZero(value : Vector`1) was skipped since it collides with above method

    # Skipped RoundToNearest due to it being static, abstract and generic.

    RoundToNearest : RoundToNearest_MethodGroup
    class RoundToNearest_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method RoundToNearest(value : Vector`1) was skipped since it collides with above method

    # Skipped RoundToNegativeInfinity due to it being static, abstract and generic.

    RoundToNegativeInfinity : RoundToNegativeInfinity_MethodGroup
    class RoundToNegativeInfinity_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method RoundToNegativeInfinity(value : Vector`1) was skipped since it collides with above method

    # Skipped RoundToPositiveInfinity due to it being static, abstract and generic.

    RoundToPositiveInfinity : RoundToPositiveInfinity_MethodGroup
    class RoundToPositiveInfinity_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method RoundToPositiveInfinity(value : Vector`1) was skipped since it collides with above method

    # Skipped RoundToZero due to it being static, abstract and generic.

    RoundToZero : RoundToZero_MethodGroup
    class RoundToZero_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method RoundToZero(value : Vector`1) was skipped since it collides with above method

    # Skipped SaturatingDecrementBy16BitElementCount due to it being static, abstract and generic.

    SaturatingDecrementBy16BitElementCount : SaturatingDecrementBy16BitElementCount_MethodGroup
    class SaturatingDecrementBy16BitElementCount_MethodGroup:
        @typing.overload
        def __call__(self, value: int, scale: int, pattern: SveMaskPattern = ...) -> int:...
        # Method SaturatingDecrementBy16BitElementCount(value : Int64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingDecrementBy16BitElementCount(value : UInt32, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingDecrementBy16BitElementCount(value : UInt64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector_1[int], scale: int, pattern: SveMaskPattern = ...) -> Vector_1[int]:...
        # Method SaturatingDecrementBy16BitElementCount(value : Vector`1, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method

    # Skipped SaturatingDecrementBy32BitElementCount due to it being static, abstract and generic.

    SaturatingDecrementBy32BitElementCount : SaturatingDecrementBy32BitElementCount_MethodGroup
    class SaturatingDecrementBy32BitElementCount_MethodGroup:
        @typing.overload
        def __call__(self, value: int, scale: int, pattern: SveMaskPattern = ...) -> int:...
        # Method SaturatingDecrementBy32BitElementCount(value : Int64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingDecrementBy32BitElementCount(value : UInt32, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingDecrementBy32BitElementCount(value : UInt64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector_1[int], scale: int, pattern: SveMaskPattern = ...) -> Vector_1[int]:...
        # Method SaturatingDecrementBy32BitElementCount(value : Vector`1, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method

    # Skipped SaturatingDecrementBy64BitElementCount due to it being static, abstract and generic.

    SaturatingDecrementBy64BitElementCount : SaturatingDecrementBy64BitElementCount_MethodGroup
    class SaturatingDecrementBy64BitElementCount_MethodGroup:
        @typing.overload
        def __call__(self, value: int, scale: int, pattern: SveMaskPattern = ...) -> int:...
        # Method SaturatingDecrementBy64BitElementCount(value : Int64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingDecrementBy64BitElementCount(value : UInt32, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingDecrementBy64BitElementCount(value : UInt64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector_1[int], scale: int, pattern: SveMaskPattern = ...) -> Vector_1[int]:...
        # Method SaturatingDecrementBy64BitElementCount(value : Vector`1, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method

    # Skipped SaturatingDecrementBy8BitElementCount due to it being static, abstract and generic.

    SaturatingDecrementBy8BitElementCount : SaturatingDecrementBy8BitElementCount_MethodGroup
    class SaturatingDecrementBy8BitElementCount_MethodGroup:
        def __call__(self, value: int, scale: int, pattern: SveMaskPattern = ...) -> int:...
        # Method SaturatingDecrementBy8BitElementCount(value : Int64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingDecrementBy8BitElementCount(value : UInt32, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingDecrementBy8BitElementCount(value : UInt64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method

    # Skipped SaturatingDecrementByActiveElementCount due to it being static, abstract and generic.

    SaturatingDecrementByActiveElementCount : SaturatingDecrementByActiveElementCount_MethodGroup
    class SaturatingDecrementByActiveElementCount_MethodGroup:
        @typing.overload
        def __call__(self, value: int, from_: Vector_1[int]) -> int:...
        # Method SaturatingDecrementByActiveElementCount(value : Int64, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : UInt32, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : UInt64, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : Int32, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : Int64, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : UInt32, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : UInt64, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : Int32, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : Int64, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : UInt32, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : UInt64, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : Int32, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : Int64, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : UInt32, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : UInt64, from : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector_1[int], from_: Vector_1[int]) -> Vector_1[int]:...
        # Method SaturatingDecrementByActiveElementCount(value : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingDecrementByActiveElementCount(value : Vector`1, from : Vector`1) was skipped since it collides with above method

    # Skipped SaturatingIncrementBy16BitElementCount due to it being static, abstract and generic.

    SaturatingIncrementBy16BitElementCount : SaturatingIncrementBy16BitElementCount_MethodGroup
    class SaturatingIncrementBy16BitElementCount_MethodGroup:
        @typing.overload
        def __call__(self, value: int, scale: int, pattern: SveMaskPattern = ...) -> int:...
        # Method SaturatingIncrementBy16BitElementCount(value : Int64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingIncrementBy16BitElementCount(value : UInt32, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingIncrementBy16BitElementCount(value : UInt64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector_1[int], scale: int, pattern: SveMaskPattern = ...) -> Vector_1[int]:...
        # Method SaturatingIncrementBy16BitElementCount(value : Vector`1, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method

    # Skipped SaturatingIncrementBy32BitElementCount due to it being static, abstract and generic.

    SaturatingIncrementBy32BitElementCount : SaturatingIncrementBy32BitElementCount_MethodGroup
    class SaturatingIncrementBy32BitElementCount_MethodGroup:
        @typing.overload
        def __call__(self, value: int, scale: int, pattern: SveMaskPattern = ...) -> int:...
        # Method SaturatingIncrementBy32BitElementCount(value : Int64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingIncrementBy32BitElementCount(value : UInt32, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingIncrementBy32BitElementCount(value : UInt64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector_1[int], scale: int, pattern: SveMaskPattern = ...) -> Vector_1[int]:...
        # Method SaturatingIncrementBy32BitElementCount(value : Vector`1, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method

    # Skipped SaturatingIncrementBy64BitElementCount due to it being static, abstract and generic.

    SaturatingIncrementBy64BitElementCount : SaturatingIncrementBy64BitElementCount_MethodGroup
    class SaturatingIncrementBy64BitElementCount_MethodGroup:
        @typing.overload
        def __call__(self, value: int, scale: int, pattern: SveMaskPattern = ...) -> int:...
        # Method SaturatingIncrementBy64BitElementCount(value : Int64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingIncrementBy64BitElementCount(value : UInt32, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingIncrementBy64BitElementCount(value : UInt64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector_1[int], scale: int, pattern: SveMaskPattern = ...) -> Vector_1[int]:...
        # Method SaturatingIncrementBy64BitElementCount(value : Vector`1, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method

    # Skipped SaturatingIncrementBy8BitElementCount due to it being static, abstract and generic.

    SaturatingIncrementBy8BitElementCount : SaturatingIncrementBy8BitElementCount_MethodGroup
    class SaturatingIncrementBy8BitElementCount_MethodGroup:
        def __call__(self, value: int, scale: int, pattern: SveMaskPattern = ...) -> int:...
        # Method SaturatingIncrementBy8BitElementCount(value : Int64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingIncrementBy8BitElementCount(value : UInt32, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method
        # Method SaturatingIncrementBy8BitElementCount(value : UInt64, scale : Byte, pattern : SveMaskPattern) was skipped since it collides with above method

    # Skipped SaturatingIncrementByActiveElementCount due to it being static, abstract and generic.

    SaturatingIncrementByActiveElementCount : SaturatingIncrementByActiveElementCount_MethodGroup
    class SaturatingIncrementByActiveElementCount_MethodGroup:
        @typing.overload
        def __call__(self, value: int, from_: Vector_1[int]) -> int:...
        # Method SaturatingIncrementByActiveElementCount(value : Int64, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : UInt32, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : UInt64, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : Int32, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : Int64, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : UInt32, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : UInt64, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : Int32, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : Int64, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : UInt32, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : UInt64, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : Int32, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : Int64, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : UInt32, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : UInt64, from : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, value: Vector_1[int], from_: Vector_1[int]) -> Vector_1[int]:...
        # Method SaturatingIncrementByActiveElementCount(value : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : Vector`1, from : Vector`1) was skipped since it collides with above method
        # Method SaturatingIncrementByActiveElementCount(value : Vector`1, from : Vector`1) was skipped since it collides with above method

    # Skipped Scale due to it being static, abstract and generic.

    Scale : Scale_MethodGroup
    class Scale_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[int]) -> Vector_1[float]:...
        # Method Scale(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped Scatter due to it being static, abstract and generic.

    Scatter : Scatter_MethodGroup
    class Scatter_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[float], addresses: Vector_1[int], data: Vector_1[float]) -> None:...
        # Method Scatter(mask : Vector`1, addresses : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter(mask : Vector`1, addresses : Vector`1, data : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float], indicies: Vector_1[int], data: Vector_1[float]) -> None:...
        # Method Scatter(mask : Vector`1, address : Double*, indicies : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter(mask : Vector`1, address : Single*, indicies : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter(mask : Vector`1, address : Single*, indicies : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter(mask : Vector`1, address : Int32*, indicies : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter(mask : Vector`1, address : Int32*, indicies : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter(mask : Vector`1, address : Int64*, indicies : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter(mask : Vector`1, address : Int64*, indicies : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter(mask : Vector`1, address : UInt32*, indicies : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter(mask : Vector`1, address : UInt32*, indicies : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter(mask : Vector`1, address : UInt64*, indicies : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter(mask : Vector`1, address : UInt64*, indicies : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped Scatter16BitNarrowing due to it being static, abstract and generic.

    Scatter16BitNarrowing : Scatter16BitNarrowing_MethodGroup
    class Scatter16BitNarrowing_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int], data: Vector_1[int]) -> None:...
        # Method Scatter16BitNarrowing(mask : Vector`1, addresses : Vector`1, data : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], indices: Vector_1[int], data: Vector_1[int]) -> None:...
        # Method Scatter16BitNarrowing(mask : Vector`1, address : Int16*, indices : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter16BitNarrowing(mask : Vector`1, address : Int16*, indices : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter16BitNarrowing(mask : Vector`1, address : Int16*, indices : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter16BitNarrowing(mask : Vector`1, address : UInt16*, indices : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter16BitNarrowing(mask : Vector`1, address : UInt16*, indices : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter16BitNarrowing(mask : Vector`1, address : UInt16*, indices : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter16BitNarrowing(mask : Vector`1, address : UInt16*, indices : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped Scatter16BitWithByteOffsetsNarrowing due to it being static, abstract and generic.

    Scatter16BitWithByteOffsetsNarrowing : Scatter16BitWithByteOffsetsNarrowing_MethodGroup
    class Scatter16BitWithByteOffsetsNarrowing_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], offsets: Vector_1[int], data: Vector_1[int]) -> None:...
        # Method Scatter16BitWithByteOffsetsNarrowing(mask : Vector`1, address : Int16*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter16BitWithByteOffsetsNarrowing(mask : Vector`1, address : Int16*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter16BitWithByteOffsetsNarrowing(mask : Vector`1, address : Int16*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter16BitWithByteOffsetsNarrowing(mask : Vector`1, address : UInt16*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter16BitWithByteOffsetsNarrowing(mask : Vector`1, address : UInt16*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter16BitWithByteOffsetsNarrowing(mask : Vector`1, address : UInt16*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter16BitWithByteOffsetsNarrowing(mask : Vector`1, address : UInt16*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped Scatter32BitNarrowing due to it being static, abstract and generic.

    Scatter32BitNarrowing : Scatter32BitNarrowing_MethodGroup
    class Scatter32BitNarrowing_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int], data: Vector_1[int]) -> None:...
        # Method Scatter32BitNarrowing(mask : Vector`1, addresses : Vector`1, data : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], indices: Vector_1[int], data: Vector_1[int]) -> None:...
        # Method Scatter32BitNarrowing(mask : Vector`1, address : Int32*, indices : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter32BitNarrowing(mask : Vector`1, address : UInt32*, indices : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter32BitNarrowing(mask : Vector`1, address : UInt32*, indices : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped Scatter32BitWithByteOffsetsNarrowing due to it being static, abstract and generic.

    Scatter32BitWithByteOffsetsNarrowing : Scatter32BitWithByteOffsetsNarrowing_MethodGroup
    class Scatter32BitWithByteOffsetsNarrowing_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], offsets: Vector_1[int], data: Vector_1[int]) -> None:...
        # Method Scatter32BitWithByteOffsetsNarrowing(mask : Vector`1, address : Int32*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter32BitWithByteOffsetsNarrowing(mask : Vector`1, address : UInt32*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter32BitWithByteOffsetsNarrowing(mask : Vector`1, address : UInt32*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped Scatter8BitNarrowing due to it being static, abstract and generic.

    Scatter8BitNarrowing : Scatter8BitNarrowing_MethodGroup
    class Scatter8BitNarrowing_MethodGroup:
        def __call__(self, mask: Vector_1[int], addresses: Vector_1[int], data: Vector_1[int]) -> None:...
        # Method Scatter8BitNarrowing(mask : Vector`1, addresses : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped Scatter8BitWithByteOffsetsNarrowing due to it being static, abstract and generic.

    Scatter8BitWithByteOffsetsNarrowing : Scatter8BitWithByteOffsetsNarrowing_MethodGroup
    class Scatter8BitWithByteOffsetsNarrowing_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], offsets: Vector_1[int], data: Vector_1[int]) -> None:...
        # Method Scatter8BitWithByteOffsetsNarrowing(mask : Vector`1, address : SByte*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter8BitWithByteOffsetsNarrowing(mask : Vector`1, address : SByte*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter8BitWithByteOffsetsNarrowing(mask : Vector`1, address : SByte*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter8BitWithByteOffsetsNarrowing(mask : Vector`1, address : Byte*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter8BitWithByteOffsetsNarrowing(mask : Vector`1, address : Byte*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter8BitWithByteOffsetsNarrowing(mask : Vector`1, address : Byte*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method Scatter8BitWithByteOffsetsNarrowing(mask : Vector`1, address : Byte*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped ScatterWithByteOffsets due to it being static, abstract and generic.

    ScatterWithByteOffsets : ScatterWithByteOffsets_MethodGroup
    class ScatterWithByteOffsets_MethodGroup:
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float], offsets: Vector_1[int], data: Vector_1[float]) -> None:...
        # Method ScatterWithByteOffsets(mask : Vector`1, address : Double*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ScatterWithByteOffsets(mask : Vector`1, address : Single*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ScatterWithByteOffsets(mask : Vector`1, address : Single*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ScatterWithByteOffsets(mask : Vector`1, address : Int32*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ScatterWithByteOffsets(mask : Vector`1, address : Int32*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ScatterWithByteOffsets(mask : Vector`1, address : Int64*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ScatterWithByteOffsets(mask : Vector`1, address : Int64*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ScatterWithByteOffsets(mask : Vector`1, address : UInt32*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ScatterWithByteOffsets(mask : Vector`1, address : UInt32*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ScatterWithByteOffsets(mask : Vector`1, address : UInt64*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method
        # Method ScatterWithByteOffsets(mask : Vector`1, address : UInt64*, offsets : Vector`1, data : Vector`1) was skipped since it collides with above method

    # Skipped SetFfr due to it being static, abstract and generic.

    SetFfr : SetFfr_MethodGroup
    class SetFfr_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> None:...
        # Method SetFfr(value : Vector`1) was skipped since it collides with above method
        # Method SetFfr(value : Vector`1) was skipped since it collides with above method
        # Method SetFfr(value : Vector`1) was skipped since it collides with above method
        # Method SetFfr(value : Vector`1) was skipped since it collides with above method
        # Method SetFfr(value : Vector`1) was skipped since it collides with above method
        # Method SetFfr(value : Vector`1) was skipped since it collides with above method
        # Method SetFfr(value : Vector`1) was skipped since it collides with above method

    # Skipped ShiftLeftLogical due to it being static, abstract and generic.

    ShiftLeftLogical : ShiftLeftLogical_MethodGroup
    class ShiftLeftLogical_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method ShiftLeftLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftLeftLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped ShiftRightArithmetic due to it being static, abstract and generic.

    ShiftRightArithmetic : ShiftRightArithmetic_MethodGroup
    class ShiftRightArithmetic_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method ShiftRightArithmetic(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftRightArithmetic(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftRightArithmetic(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftRightArithmetic(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftRightArithmetic(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftRightArithmetic(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticForDivide due to it being static, abstract and generic.

    ShiftRightArithmeticForDivide : ShiftRightArithmeticForDivide_MethodGroup
    class ShiftRightArithmeticForDivide_MethodGroup:
        def __call__(self, value: Vector_1[int], control: int) -> Vector_1[int]:...
        # Method ShiftRightArithmeticForDivide(value : Vector`1, control : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticForDivide(value : Vector`1, control : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticForDivide(value : Vector`1, control : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogical due to it being static, abstract and generic.

    ShiftRightLogical : ShiftRightLogical_MethodGroup
    class ShiftRightLogical_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method ShiftRightLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftRightLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftRightLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftRightLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftRightLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ShiftRightLogical(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped SignExtend16 due to it being static, abstract and generic.

    SignExtend16 : SignExtend16_MethodGroup
    class SignExtend16_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method SignExtend16(value : Vector`1) was skipped since it collides with above method

    # Skipped SignExtend8 due to it being static, abstract and generic.

    SignExtend8 : SignExtend8_MethodGroup
    class SignExtend8_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method SignExtend8(value : Vector`1) was skipped since it collides with above method
        # Method SignExtend8(value : Vector`1) was skipped since it collides with above method

    # Skipped SignExtendWideningLower due to it being static, abstract and generic.

    SignExtendWideningLower : SignExtendWideningLower_MethodGroup
    class SignExtendWideningLower_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method SignExtendWideningLower(value : Vector`1) was skipped since it collides with above method
        # Method SignExtendWideningLower(value : Vector`1) was skipped since it collides with above method

    # Skipped SignExtendWideningUpper due to it being static, abstract and generic.

    SignExtendWideningUpper : SignExtendWideningUpper_MethodGroup
    class SignExtendWideningUpper_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method SignExtendWideningUpper(value : Vector`1) was skipped since it collides with above method
        # Method SignExtendWideningUpper(value : Vector`1) was skipped since it collides with above method

    # Skipped Splice due to it being static, abstract and generic.

    Splice : Splice_MethodGroup
    class Splice_MethodGroup:
        def __call__(self, mask: Vector_1[float], left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method Splice(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Splice(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Splice(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Splice(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Splice(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Splice(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Splice(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Splice(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Splice(mask : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped Sqrt due to it being static, abstract and generic.

    Sqrt : Sqrt_MethodGroup
    class Sqrt_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[float]:...
        # Method Sqrt(value : Vector`1) was skipped since it collides with above method

    # Skipped StoreAndZip due to it being static, abstract and generic.

    StoreAndZip : StoreAndZip_MethodGroup
    class StoreAndZip_MethodGroup:
        @typing.overload
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float], data: Vector_1[float]) -> None:...
        # Method StoreAndZip(mask : Vector`1, address : Single*, data : Vector`1) was skipped since it collides with above method
        @typing.overload
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float], data: ValueTuple_2[Vector_1[float], Vector_1[float]]) -> None:...
        @typing.overload
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float], data: ValueTuple_3[Vector_1[float], Vector_1[float], Vector_1[float]]) -> None:...
        @typing.overload
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float], data: ValueTuple_4[Vector_1[float], Vector_1[float], Vector_1[float], Vector_1[float]]) -> None:...
        # Method StoreAndZip(mask : Vector`1, address : Single*, data : ValueTuple`2) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Single*, data : ValueTuple`3) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Single*, data : ValueTuple`4) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Byte*, data : Vector`1) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Int16*, data : Vector`1) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Int32*, data : Vector`1) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Int64*, data : Vector`1) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : SByte*, data : Vector`1) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : UInt16*, data : Vector`1) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : UInt32*, data : Vector`1) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : UInt64*, data : Vector`1) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Byte*, data : ValueTuple`2) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Byte*, data : ValueTuple`3) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Byte*, data : ValueTuple`4) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Int16*, data : ValueTuple`2) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Int16*, data : ValueTuple`3) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Int16*, data : ValueTuple`4) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Int32*, data : ValueTuple`2) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Int32*, data : ValueTuple`3) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Int32*, data : ValueTuple`4) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Int64*, data : ValueTuple`2) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Int64*, data : ValueTuple`3) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : Int64*, data : ValueTuple`4) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : SByte*, data : ValueTuple`2) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : SByte*, data : ValueTuple`3) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : SByte*, data : ValueTuple`4) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : UInt16*, data : ValueTuple`2) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : UInt16*, data : ValueTuple`3) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : UInt16*, data : ValueTuple`4) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : UInt32*, data : ValueTuple`2) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : UInt32*, data : ValueTuple`3) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : UInt32*, data : ValueTuple`4) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : UInt64*, data : ValueTuple`2) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : UInt64*, data : ValueTuple`3) was skipped since it collides with above method
        # Method StoreAndZip(mask : Vector`1, address : UInt64*, data : ValueTuple`4) was skipped since it collides with above method

    # Skipped StoreNarrowing due to it being static, abstract and generic.

    StoreNarrowing : StoreNarrowing_MethodGroup
    class StoreNarrowing_MethodGroup:
        def __call__(self, mask: Vector_1[int], address: clr.Reference[int], data: Vector_1[int]) -> None:...
        # Method StoreNarrowing(mask : Vector`1, address : SByte*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNarrowing(mask : Vector`1, address : Int16*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNarrowing(mask : Vector`1, address : SByte*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNarrowing(mask : Vector`1, address : Int16*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNarrowing(mask : Vector`1, address : Int32*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNarrowing(mask : Vector`1, address : Byte*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNarrowing(mask : Vector`1, address : Byte*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNarrowing(mask : Vector`1, address : UInt16*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNarrowing(mask : Vector`1, address : Byte*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNarrowing(mask : Vector`1, address : UInt16*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNarrowing(mask : Vector`1, address : UInt32*, data : Vector`1) was skipped since it collides with above method

    # Skipped StoreNonTemporal due to it being static, abstract and generic.

    StoreNonTemporal : StoreNonTemporal_MethodGroup
    class StoreNonTemporal_MethodGroup:
        def __call__(self, mask: Vector_1[float], address: clr.Reference[float], data: Vector_1[float]) -> None:...
        # Method StoreNonTemporal(mask : Vector`1, address : Single*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNonTemporal(mask : Vector`1, address : Byte*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNonTemporal(mask : Vector`1, address : Int16*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNonTemporal(mask : Vector`1, address : Int32*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNonTemporal(mask : Vector`1, address : Int64*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNonTemporal(mask : Vector`1, address : SByte*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNonTemporal(mask : Vector`1, address : UInt16*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNonTemporal(mask : Vector`1, address : UInt32*, data : Vector`1) was skipped since it collides with above method
        # Method StoreNonTemporal(mask : Vector`1, address : UInt64*, data : Vector`1) was skipped since it collides with above method

    # Skipped Subtract due to it being static, abstract and generic.

    Subtract : Subtract_MethodGroup
    class Subtract_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method Subtract(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Subtract(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Subtract(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Subtract(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Subtract(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Subtract(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Subtract(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Subtract(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Subtract(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped SubtractSaturate due to it being static, abstract and generic.

    SubtractSaturate : SubtractSaturate_MethodGroup
    class SubtractSaturate_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method SubtractSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped TestAnyTrue due to it being static, abstract and generic.

    TestAnyTrue : TestAnyTrue_MethodGroup
    class TestAnyTrue_MethodGroup:
        def __call__(self, mask: Vector_1[int], rightMask: Vector_1[int]) -> bool:...
        # Method TestAnyTrue(mask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestAnyTrue(mask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestAnyTrue(mask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestAnyTrue(mask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestAnyTrue(mask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestAnyTrue(mask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestAnyTrue(mask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method

    # Skipped TestFirstTrue due to it being static, abstract and generic.

    TestFirstTrue : TestFirstTrue_MethodGroup
    class TestFirstTrue_MethodGroup:
        def __call__(self, leftMask: Vector_1[int], rightMask: Vector_1[int]) -> bool:...
        # Method TestFirstTrue(leftMask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestFirstTrue(leftMask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestFirstTrue(leftMask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestFirstTrue(leftMask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestFirstTrue(leftMask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestFirstTrue(leftMask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestFirstTrue(leftMask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method

    # Skipped TestLastTrue due to it being static, abstract and generic.

    TestLastTrue : TestLastTrue_MethodGroup
    class TestLastTrue_MethodGroup:
        def __call__(self, leftMask: Vector_1[int], rightMask: Vector_1[int]) -> bool:...
        # Method TestLastTrue(leftMask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestLastTrue(leftMask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestLastTrue(leftMask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestLastTrue(leftMask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestLastTrue(leftMask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestLastTrue(leftMask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method
        # Method TestLastTrue(leftMask : Vector`1, rightMask : Vector`1) was skipped since it collides with above method

    # Skipped TransposeEven due to it being static, abstract and generic.

    TransposeEven : TransposeEven_MethodGroup
    class TransposeEven_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method TransposeEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped TransposeOdd due to it being static, abstract and generic.

    TransposeOdd : TransposeOdd_MethodGroup
    class TransposeOdd_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method TransposeOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method TransposeOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped TrigonometricMultiplyAddCoefficient due to it being static, abstract and generic.

    TrigonometricMultiplyAddCoefficient : TrigonometricMultiplyAddCoefficient_MethodGroup
    class TrigonometricMultiplyAddCoefficient_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float], control: int) -> Vector_1[float]:...
        # Method TrigonometricMultiplyAddCoefficient(left : Vector`1, right : Vector`1, control : Byte) was skipped since it collides with above method

    # Skipped TrigonometricSelectCoefficient due to it being static, abstract and generic.

    TrigonometricSelectCoefficient : TrigonometricSelectCoefficient_MethodGroup
    class TrigonometricSelectCoefficient_MethodGroup:
        def __call__(self, value: Vector_1[float], selector: Vector_1[int]) -> Vector_1[float]:...
        # Method TrigonometricSelectCoefficient(value : Vector`1, selector : Vector`1) was skipped since it collides with above method

    # Skipped TrigonometricStartingValue due to it being static, abstract and generic.

    TrigonometricStartingValue : TrigonometricStartingValue_MethodGroup
    class TrigonometricStartingValue_MethodGroup:
        def __call__(self, value: Vector_1[float], sign: Vector_1[int]) -> Vector_1[float]:...
        # Method TrigonometricStartingValue(value : Vector`1, sign : Vector`1) was skipped since it collides with above method

    # Skipped UnzipEven due to it being static, abstract and generic.

    UnzipEven : UnzipEven_MethodGroup
    class UnzipEven_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method UnzipEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped UnzipOdd due to it being static, abstract and generic.

    UnzipOdd : UnzipOdd_MethodGroup
    class UnzipOdd_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method UnzipOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method UnzipOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped VectorTableLookup due to it being static, abstract and generic.

    VectorTableLookup : VectorTableLookup_MethodGroup
    class VectorTableLookup_MethodGroup:
        def __call__(self, data: Vector_1[float], indices: Vector_1[int]) -> Vector_1[float]:...
        # Method VectorTableLookup(data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(data : Vector`1, indices : Vector`1) was skipped since it collides with above method

    # Skipped Xor due to it being static, abstract and generic.

    Xor : Xor_MethodGroup
    class Xor_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method Xor(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Xor(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Xor(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Xor(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Xor(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Xor(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method Xor(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped XorAcross due to it being static, abstract and generic.

    XorAcross : XorAcross_MethodGroup
    class XorAcross_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method XorAcross(value : Vector`1) was skipped since it collides with above method
        # Method XorAcross(value : Vector`1) was skipped since it collides with above method
        # Method XorAcross(value : Vector`1) was skipped since it collides with above method
        # Method XorAcross(value : Vector`1) was skipped since it collides with above method
        # Method XorAcross(value : Vector`1) was skipped since it collides with above method
        # Method XorAcross(value : Vector`1) was skipped since it collides with above method
        # Method XorAcross(value : Vector`1) was skipped since it collides with above method

    # Skipped ZeroExtend16 due to it being static, abstract and generic.

    ZeroExtend16 : ZeroExtend16_MethodGroup
    class ZeroExtend16_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method ZeroExtend16(value : Vector`1) was skipped since it collides with above method

    # Skipped ZeroExtend8 due to it being static, abstract and generic.

    ZeroExtend8 : ZeroExtend8_MethodGroup
    class ZeroExtend8_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method ZeroExtend8(value : Vector`1) was skipped since it collides with above method
        # Method ZeroExtend8(value : Vector`1) was skipped since it collides with above method

    # Skipped ZeroExtendWideningLower due to it being static, abstract and generic.

    ZeroExtendWideningLower : ZeroExtendWideningLower_MethodGroup
    class ZeroExtendWideningLower_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method ZeroExtendWideningLower(value : Vector`1) was skipped since it collides with above method
        # Method ZeroExtendWideningLower(value : Vector`1) was skipped since it collides with above method

    # Skipped ZeroExtendWideningUpper due to it being static, abstract and generic.

    ZeroExtendWideningUpper : ZeroExtendWideningUpper_MethodGroup
    class ZeroExtendWideningUpper_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method ZeroExtendWideningUpper(value : Vector`1) was skipped since it collides with above method
        # Method ZeroExtendWideningUpper(value : Vector`1) was skipped since it collides with above method

    # Skipped ZipHigh due to it being static, abstract and generic.

    ZipHigh : ZipHigh_MethodGroup
    class ZipHigh_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method ZipHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped ZipLow due to it being static, abstract and generic.

    ZipLow : ZipLow_MethodGroup
    class ZipLow_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method ZipLow(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipLow(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipLow(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipLow(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipLow(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipLow(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipLow(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipLow(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method ZipLow(left : Vector`1, right : Vector`1) was skipped since it collides with above method


    class Arm64(AdvSimd.Arm64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...



class Sve2(Sve):
    @classmethod
    @property
    def IsSupported(cls) -> bool: ...
    @staticmethod
    def ConvertToDoubleOdd(value: Vector_1[float]) -> Vector_1[float]: ...
    @staticmethod
    def ConvertToSingleEvenRoundToOdd(value: Vector_1[float]) -> Vector_1[float]: ...
    @staticmethod
    def ReciprocalEstimate(value: Vector_1[int]) -> Vector_1[int]: ...
    @staticmethod
    def ReciprocalSqrtEstimate(value: Vector_1[int]) -> Vector_1[int]: ...
    # Skipped AbsoluteDifferenceAdd due to it being static, abstract and generic.

    AbsoluteDifferenceAdd : AbsoluteDifferenceAdd_MethodGroup
    class AbsoluteDifferenceAdd_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AbsoluteDifferenceAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AbsoluteDifferenceWideningEven due to it being static, abstract and generic.

    AbsoluteDifferenceWideningEven : AbsoluteDifferenceWideningEven_MethodGroup
    class AbsoluteDifferenceWideningEven_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AbsoluteDifferenceWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AbsoluteDifferenceWideningLowerAndAddEven due to it being static, abstract and generic.

    AbsoluteDifferenceWideningLowerAndAddEven : AbsoluteDifferenceWideningLowerAndAddEven_MethodGroup
    class AbsoluteDifferenceWideningLowerAndAddEven_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AbsoluteDifferenceWideningLowerAndAddEven(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLowerAndAddEven(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLowerAndAddEven(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLowerAndAddEven(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLowerAndAddEven(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AbsoluteDifferenceWideningLowerAndAddOdd due to it being static, abstract and generic.

    AbsoluteDifferenceWideningLowerAndAddOdd : AbsoluteDifferenceWideningLowerAndAddOdd_MethodGroup
    class AbsoluteDifferenceWideningLowerAndAddOdd_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AbsoluteDifferenceWideningLowerAndAddOdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLowerAndAddOdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLowerAndAddOdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLowerAndAddOdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningLowerAndAddOdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AbsoluteDifferenceWideningOdd due to it being static, abstract and generic.

    AbsoluteDifferenceWideningOdd : AbsoluteDifferenceWideningOdd_MethodGroup
    class AbsoluteDifferenceWideningOdd_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AbsoluteDifferenceWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AbsoluteDifferenceWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AbsSaturate due to it being static, abstract and generic.

    AbsSaturate : AbsSaturate_MethodGroup
    class AbsSaturate_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method AbsSaturate(value : Vector`1) was skipped since it collides with above method
        # Method AbsSaturate(value : Vector`1) was skipped since it collides with above method
        # Method AbsSaturate(value : Vector`1) was skipped since it collides with above method

    # Skipped AddCarryWideningEven due to it being static, abstract and generic.

    AddCarryWideningEven : AddCarryWideningEven_MethodGroup
    class AddCarryWideningEven_MethodGroup:
        def __call__(self, op1: Vector_1[int], op2: Vector_1[int], op3: Vector_1[int]) -> Vector_1[int]:...
        # Method AddCarryWideningEven(op1 : Vector`1, op2 : Vector`1, op3 : Vector`1) was skipped since it collides with above method

    # Skipped AddCarryWideningOdd due to it being static, abstract and generic.

    AddCarryWideningOdd : AddCarryWideningOdd_MethodGroup
    class AddCarryWideningOdd_MethodGroup:
        def __call__(self, op1: Vector_1[int], op2: Vector_1[int], op3: Vector_1[int]) -> Vector_1[int]:...
        # Method AddCarryWideningOdd(op1 : Vector`1, op2 : Vector`1, op3 : Vector`1) was skipped since it collides with above method

    # Skipped AddHighNarrowingEven due to it being static, abstract and generic.

    AddHighNarrowingEven : AddHighNarrowingEven_MethodGroup
    class AddHighNarrowingEven_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AddHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AddHighNarrowingOdd due to it being static, abstract and generic.

    AddHighNarrowingOdd : AddHighNarrowingOdd_MethodGroup
    class AddHighNarrowingOdd_MethodGroup:
        def __call__(self, even: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AddHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AddPairwise due to it being static, abstract and generic.

    AddPairwise : AddPairwise_MethodGroup
    class AddPairwise_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method AddPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AddPairwiseWideningAndAdd due to it being static, abstract and generic.

    AddPairwiseWideningAndAdd : AddPairwiseWideningAndAdd_MethodGroup
    class AddPairwiseWideningAndAdd_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AddPairwiseWideningAndAdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddPairwiseWideningAndAdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddPairwiseWideningAndAdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddPairwiseWideningAndAdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddPairwiseWideningAndAdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AddRotateComplex due to it being static, abstract and generic.

    AddRotateComplex : AddRotateComplex_MethodGroup
    class AddRotateComplex_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int], rotation: int) -> Vector_1[int]:...
        # Method AddRotateComplex(left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method AddRotateComplex(left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method AddRotateComplex(left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method AddRotateComplex(left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method AddRotateComplex(left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method AddRotateComplex(left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method AddRotateComplex(left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method

    # Skipped AddRoundedHighNarrowingEven due to it being static, abstract and generic.

    AddRoundedHighNarrowingEven : AddRoundedHighNarrowingEven_MethodGroup
    class AddRoundedHighNarrowingEven_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AddRoundedHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AddRoundedHighNarrowingOdd due to it being static, abstract and generic.

    AddRoundedHighNarrowingOdd : AddRoundedHighNarrowingOdd_MethodGroup
    class AddRoundedHighNarrowingOdd_MethodGroup:
        def __call__(self, even: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AddRoundedHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddRoundedHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AddSaturate due to it being static, abstract and generic.

    AddSaturate : AddSaturate_MethodGroup
    class AddSaturate_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AddSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AddSaturateRotateComplex due to it being static, abstract and generic.

    AddSaturateRotateComplex : AddSaturateRotateComplex_MethodGroup
    class AddSaturateRotateComplex_MethodGroup:
        def __call__(self, op1: Vector_1[int], op2: Vector_1[int], rotation: int) -> Vector_1[int]:...
        # Method AddSaturateRotateComplex(op1 : Vector`1, op2 : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method AddSaturateRotateComplex(op1 : Vector`1, op2 : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method AddSaturateRotateComplex(op1 : Vector`1, op2 : Vector`1, rotation : Byte) was skipped since it collides with above method

    # Skipped AddSaturateWithSignedAddend due to it being static, abstract and generic.

    AddSaturateWithSignedAddend : AddSaturateWithSignedAddend_MethodGroup
    class AddSaturateWithSignedAddend_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AddSaturateWithSignedAddend(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturateWithSignedAddend(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturateWithSignedAddend(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AddSaturateWithUnsignedAddend due to it being static, abstract and generic.

    AddSaturateWithUnsignedAddend : AddSaturateWithUnsignedAddend_MethodGroup
    class AddSaturateWithUnsignedAddend_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AddSaturateWithUnsignedAddend(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturateWithUnsignedAddend(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddSaturateWithUnsignedAddend(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AddWideningEven due to it being static, abstract and generic.

    AddWideningEven : AddWideningEven_MethodGroup
    class AddWideningEven_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AddWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AddWideningEvenOdd due to it being static, abstract and generic.

    AddWideningEvenOdd : AddWideningEvenOdd_MethodGroup
    class AddWideningEvenOdd_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AddWideningEvenOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningEvenOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped AddWideningOdd due to it being static, abstract and generic.

    AddWideningOdd : AddWideningOdd_MethodGroup
    class AddWideningOdd_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method AddWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method AddWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped BitwiseClearXor due to it being static, abstract and generic.

    BitwiseClearXor : BitwiseClearXor_MethodGroup
    class BitwiseClearXor_MethodGroup:
        def __call__(self, xor: Vector_1[int], value: Vector_1[int], mask: Vector_1[int]) -> Vector_1[int]:...
        # Method BitwiseClearXor(xor : Vector`1, value : Vector`1, mask : Vector`1) was skipped since it collides with above method
        # Method BitwiseClearXor(xor : Vector`1, value : Vector`1, mask : Vector`1) was skipped since it collides with above method
        # Method BitwiseClearXor(xor : Vector`1, value : Vector`1, mask : Vector`1) was skipped since it collides with above method
        # Method BitwiseClearXor(xor : Vector`1, value : Vector`1, mask : Vector`1) was skipped since it collides with above method
        # Method BitwiseClearXor(xor : Vector`1, value : Vector`1, mask : Vector`1) was skipped since it collides with above method
        # Method BitwiseClearXor(xor : Vector`1, value : Vector`1, mask : Vector`1) was skipped since it collides with above method
        # Method BitwiseClearXor(xor : Vector`1, value : Vector`1, mask : Vector`1) was skipped since it collides with above method

    # Skipped BitwiseSelect due to it being static, abstract and generic.

    BitwiseSelect : BitwiseSelect_MethodGroup
    class BitwiseSelect_MethodGroup:
        def __call__(self, select: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method BitwiseSelect(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelect(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped BitwiseSelectLeftInverted due to it being static, abstract and generic.

    BitwiseSelectLeftInverted : BitwiseSelectLeftInverted_MethodGroup
    class BitwiseSelectLeftInverted_MethodGroup:
        def __call__(self, select: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method BitwiseSelectLeftInverted(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelectLeftInverted(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelectLeftInverted(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelectLeftInverted(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelectLeftInverted(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelectLeftInverted(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelectLeftInverted(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped BitwiseSelectRightInverted due to it being static, abstract and generic.

    BitwiseSelectRightInverted : BitwiseSelectRightInverted_MethodGroup
    class BitwiseSelectRightInverted_MethodGroup:
        def __call__(self, select: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method BitwiseSelectRightInverted(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelectRightInverted(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelectRightInverted(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelectRightInverted(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelectRightInverted(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelectRightInverted(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method BitwiseSelectRightInverted(select : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped DotProductRotateComplex due to it being static, abstract and generic.

    DotProductRotateComplex : DotProductRotateComplex_MethodGroup
    class DotProductRotateComplex_MethodGroup:
        def __call__(self, op1: Vector_1[int], op2: Vector_1[int], op3: Vector_1[int], rotation: int) -> Vector_1[int]:...
        # Method DotProductRotateComplex(op1 : Vector`1, op2 : Vector`1, op3 : Vector`1, rotation : Byte) was skipped since it collides with above method

    # Skipped DotProductRotateComplexBySelectedIndex due to it being static, abstract and generic.

    DotProductRotateComplexBySelectedIndex : DotProductRotateComplexBySelectedIndex_MethodGroup
    class DotProductRotateComplexBySelectedIndex_MethodGroup:
        def __call__(self, op1: Vector_1[int], op2: Vector_1[int], op3: Vector_1[int], imm_index: int, rotation: int) -> Vector_1[int]:...
        # Method DotProductRotateComplexBySelectedIndex(op1 : Vector`1, op2 : Vector`1, op3 : Vector`1, imm_index : Byte, rotation : Byte) was skipped since it collides with above method

    # Skipped FusedAddHalving due to it being static, abstract and generic.

    FusedAddHalving : FusedAddHalving_MethodGroup
    class FusedAddHalving_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method FusedAddHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedAddHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedAddHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedAddHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedAddHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedAddHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedAddHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped FusedAddRoundedHalving due to it being static, abstract and generic.

    FusedAddRoundedHalving : FusedAddRoundedHalving_MethodGroup
    class FusedAddRoundedHalving_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method FusedAddRoundedHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedAddRoundedHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedAddRoundedHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedAddRoundedHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedAddRoundedHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedAddRoundedHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedAddRoundedHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped FusedSubtractHalving due to it being static, abstract and generic.

    FusedSubtractHalving : FusedSubtractHalving_MethodGroup
    class FusedSubtractHalving_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method FusedSubtractHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedSubtractHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedSubtractHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedSubtractHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedSubtractHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedSubtractHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method FusedSubtractHalving(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped InterleavingXorEvenOdd due to it being static, abstract and generic.

    InterleavingXorEvenOdd : InterleavingXorEvenOdd_MethodGroup
    class InterleavingXorEvenOdd_MethodGroup:
        def __call__(self, odd: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method InterleavingXorEvenOdd(odd : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method InterleavingXorEvenOdd(odd : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method InterleavingXorEvenOdd(odd : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method InterleavingXorEvenOdd(odd : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method InterleavingXorEvenOdd(odd : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method InterleavingXorEvenOdd(odd : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method InterleavingXorEvenOdd(odd : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped InterleavingXorOddEven due to it being static, abstract and generic.

    InterleavingXorOddEven : InterleavingXorOddEven_MethodGroup
    class InterleavingXorOddEven_MethodGroup:
        def __call__(self, even: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method InterleavingXorOddEven(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method InterleavingXorOddEven(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method InterleavingXorOddEven(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method InterleavingXorOddEven(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method InterleavingXorOddEven(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method InterleavingXorOddEven(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method InterleavingXorOddEven(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped Log2 due to it being static, abstract and generic.

    Log2 : Log2_MethodGroup
    class Log2_MethodGroup:
        def __call__(self, value: Vector_1[float]) -> Vector_1[int]:...
        # Method Log2(value : Vector`1) was skipped since it collides with above method

    # Skipped MaxNumberPairwise due to it being static, abstract and generic.

    MaxNumberPairwise : MaxNumberPairwise_MethodGroup
    class MaxNumberPairwise_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method MaxNumberPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MaxPairwise due to it being static, abstract and generic.

    MaxPairwise : MaxPairwise_MethodGroup
    class MaxPairwise_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method MaxPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MaxPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MaxPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MaxPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MaxPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MaxPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MaxPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MaxPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MaxPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MinNumberPairwise due to it being static, abstract and generic.

    MinNumberPairwise : MinNumberPairwise_MethodGroup
    class MinNumberPairwise_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method MinNumberPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MinPairwise due to it being static, abstract and generic.

    MinPairwise : MinPairwise_MethodGroup
    class MinPairwise_MethodGroup:
        def __call__(self, left: Vector_1[float], right: Vector_1[float]) -> Vector_1[float]:...
        # Method MinPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MinPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MinPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MinPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MinPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MinPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MinPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MinPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MinPairwise(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyAddBySelectedScalar due to it being static, abstract and generic.

    MultiplyAddBySelectedScalar : MultiplyAddBySelectedScalar_MethodGroup
    class MultiplyAddBySelectedScalar_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyAddBySelectedScalar(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyAddBySelectedScalar(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyAddBySelectedScalar(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyAddBySelectedScalar(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyAddBySelectedScalar(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyAddRotateComplex due to it being static, abstract and generic.

    MultiplyAddRotateComplex : MultiplyAddRotateComplex_MethodGroup
    class MultiplyAddRotateComplex_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rotation: int) -> Vector_1[int]:...
        # Method MultiplyAddRotateComplex(addend : Vector`1, left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method MultiplyAddRotateComplex(addend : Vector`1, left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method MultiplyAddRotateComplex(addend : Vector`1, left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method MultiplyAddRotateComplex(addend : Vector`1, left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method MultiplyAddRotateComplex(addend : Vector`1, left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method MultiplyAddRotateComplex(addend : Vector`1, left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method MultiplyAddRotateComplex(addend : Vector`1, left : Vector`1, right : Vector`1, rotation : Byte) was skipped since it collides with above method

    # Skipped MultiplyAddRotateComplexBySelectedScalar due to it being static, abstract and generic.

    MultiplyAddRotateComplexBySelectedScalar : MultiplyAddRotateComplexBySelectedScalar_MethodGroup
    class MultiplyAddRotateComplexBySelectedScalar_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rightIndex: int, rotation: int) -> Vector_1[int]:...
        # Method MultiplyAddRotateComplexBySelectedScalar(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte, rotation : Byte) was skipped since it collides with above method
        # Method MultiplyAddRotateComplexBySelectedScalar(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte, rotation : Byte) was skipped since it collides with above method
        # Method MultiplyAddRotateComplexBySelectedScalar(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte, rotation : Byte) was skipped since it collides with above method

    # Skipped MultiplyAddRoundedDoublingSaturateHighRotateComplex due to it being static, abstract and generic.

    MultiplyAddRoundedDoublingSaturateHighRotateComplex : MultiplyAddRoundedDoublingSaturateHighRotateComplex_MethodGroup
    class MultiplyAddRoundedDoublingSaturateHighRotateComplex_MethodGroup:
        def __call__(self, op1: Vector_1[int], op2: Vector_1[int], op3: Vector_1[int], rotation: int) -> Vector_1[int]:...
        # Method MultiplyAddRoundedDoublingSaturateHighRotateComplex(op1 : Vector`1, op2 : Vector`1, op3 : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method MultiplyAddRoundedDoublingSaturateHighRotateComplex(op1 : Vector`1, op2 : Vector`1, op3 : Vector`1, rotation : Byte) was skipped since it collides with above method
        # Method MultiplyAddRoundedDoublingSaturateHighRotateComplex(op1 : Vector`1, op2 : Vector`1, op3 : Vector`1, rotation : Byte) was skipped since it collides with above method

    # Skipped MultiplyAddRoundedDoublingSaturateHighRotateComplexBySelectedScalar due to it being static, abstract and generic.

    MultiplyAddRoundedDoublingSaturateHighRotateComplexBySelectedScalar : MultiplyAddRoundedDoublingSaturateHighRotateComplexBySelectedScalar_MethodGroup
    class MultiplyAddRoundedDoublingSaturateHighRotateComplexBySelectedScalar_MethodGroup:
        def __call__(self, op1: Vector_1[int], op2: Vector_1[int], op3: Vector_1[int], imm_index: int, rotation: int) -> Vector_1[int]:...
        # Method MultiplyAddRoundedDoublingSaturateHighRotateComplexBySelectedScalar(op1 : Vector`1, op2 : Vector`1, op3 : Vector`1, imm_index : Byte, rotation : Byte) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalar due to it being static, abstract and generic.

    MultiplyBySelectedScalar : MultiplyBySelectedScalar_MethodGroup
    class MultiplyBySelectedScalar_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyBySelectedScalar(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalar(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalarWideningEven due to it being static, abstract and generic.

    MultiplyBySelectedScalarWideningEven : MultiplyBySelectedScalarWideningEven_MethodGroup
    class MultiplyBySelectedScalarWideningEven_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyBySelectedScalarWideningEven(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningEven(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningEven(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalarWideningEvenAndAdd due to it being static, abstract and generic.

    MultiplyBySelectedScalarWideningEvenAndAdd : MultiplyBySelectedScalarWideningEvenAndAdd_MethodGroup
    class MultiplyBySelectedScalarWideningEvenAndAdd_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyBySelectedScalarWideningEvenAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningEvenAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningEvenAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalarWideningEvenAndSubtract due to it being static, abstract and generic.

    MultiplyBySelectedScalarWideningEvenAndSubtract : MultiplyBySelectedScalarWideningEvenAndSubtract_MethodGroup
    class MultiplyBySelectedScalarWideningEvenAndSubtract_MethodGroup:
        def __call__(self, minuend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyBySelectedScalarWideningEvenAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningEvenAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningEvenAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalarWideningOdd due to it being static, abstract and generic.

    MultiplyBySelectedScalarWideningOdd : MultiplyBySelectedScalarWideningOdd_MethodGroup
    class MultiplyBySelectedScalarWideningOdd_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyBySelectedScalarWideningOdd(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningOdd(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningOdd(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalarWideningOddAndAdd due to it being static, abstract and generic.

    MultiplyBySelectedScalarWideningOddAndAdd : MultiplyBySelectedScalarWideningOddAndAdd_MethodGroup
    class MultiplyBySelectedScalarWideningOddAndAdd_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyBySelectedScalarWideningOddAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningOddAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningOddAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyBySelectedScalarWideningOddAndSubtract due to it being static, abstract and generic.

    MultiplyBySelectedScalarWideningOddAndSubtract : MultiplyBySelectedScalarWideningOddAndSubtract_MethodGroup
    class MultiplyBySelectedScalarWideningOddAndSubtract_MethodGroup:
        def __call__(self, minuend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyBySelectedScalarWideningOddAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningOddAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyBySelectedScalarWideningOddAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyDoublingBySelectedScalarSaturateHigh due to it being static, abstract and generic.

    MultiplyDoublingBySelectedScalarSaturateHigh : MultiplyDoublingBySelectedScalarSaturateHigh_MethodGroup
    class MultiplyDoublingBySelectedScalarSaturateHigh_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyDoublingBySelectedScalarSaturateHigh(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyDoublingBySelectedScalarSaturateHigh(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyDoublingSaturateHigh due to it being static, abstract and generic.

    MultiplyDoublingSaturateHigh : MultiplyDoublingSaturateHigh_MethodGroup
    class MultiplyDoublingSaturateHigh_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyDoublingSaturateHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyDoublingSaturateHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyDoublingSaturateHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningAndAddSaturateEven due to it being static, abstract and generic.

    MultiplyDoublingWideningAndAddSaturateEven : MultiplyDoublingWideningAndAddSaturateEven_MethodGroup
    class MultiplyDoublingWideningAndAddSaturateEven_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyDoublingWideningAndAddSaturateEven(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyDoublingWideningAndAddSaturateEven(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningAndAddSaturateEvenOdd due to it being static, abstract and generic.

    MultiplyDoublingWideningAndAddSaturateEvenOdd : MultiplyDoublingWideningAndAddSaturateEvenOdd_MethodGroup
    class MultiplyDoublingWideningAndAddSaturateEvenOdd_MethodGroup:
        def __call__(self, addend: Vector_1[int], leftEven: Vector_1[int], rightOdd: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyDoublingWideningAndAddSaturateEvenOdd(addend : Vector`1, leftEven : Vector`1, rightOdd : Vector`1) was skipped since it collides with above method
        # Method MultiplyDoublingWideningAndAddSaturateEvenOdd(addend : Vector`1, leftEven : Vector`1, rightOdd : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningAndAddSaturateOdd due to it being static, abstract and generic.

    MultiplyDoublingWideningAndAddSaturateOdd : MultiplyDoublingWideningAndAddSaturateOdd_MethodGroup
    class MultiplyDoublingWideningAndAddSaturateOdd_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyDoublingWideningAndAddSaturateOdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyDoublingWideningAndAddSaturateOdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningAndSubtractSaturateEven due to it being static, abstract and generic.

    MultiplyDoublingWideningAndSubtractSaturateEven : MultiplyDoublingWideningAndSubtractSaturateEven_MethodGroup
    class MultiplyDoublingWideningAndSubtractSaturateEven_MethodGroup:
        def __call__(self, minuend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyDoublingWideningAndSubtractSaturateEven(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyDoublingWideningAndSubtractSaturateEven(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningAndSubtractSaturateEvenOdd due to it being static, abstract and generic.

    MultiplyDoublingWideningAndSubtractSaturateEvenOdd : MultiplyDoublingWideningAndSubtractSaturateEvenOdd_MethodGroup
    class MultiplyDoublingWideningAndSubtractSaturateEvenOdd_MethodGroup:
        def __call__(self, minuend: Vector_1[int], leftEven: Vector_1[int], rightOdd: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyDoublingWideningAndSubtractSaturateEvenOdd(minuend : Vector`1, leftEven : Vector`1, rightOdd : Vector`1) was skipped since it collides with above method
        # Method MultiplyDoublingWideningAndSubtractSaturateEvenOdd(minuend : Vector`1, leftEven : Vector`1, rightOdd : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningAndSubtractSaturateOdd due to it being static, abstract and generic.

    MultiplyDoublingWideningAndSubtractSaturateOdd : MultiplyDoublingWideningAndSubtractSaturateOdd_MethodGroup
    class MultiplyDoublingWideningAndSubtractSaturateOdd_MethodGroup:
        def __call__(self, minuend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyDoublingWideningAndSubtractSaturateOdd(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyDoublingWideningAndSubtractSaturateOdd(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningBySelectedScalarAndAddSaturateEven due to it being static, abstract and generic.

    MultiplyDoublingWideningBySelectedScalarAndAddSaturateEven : MultiplyDoublingWideningBySelectedScalarAndAddSaturateEven_MethodGroup
    class MultiplyDoublingWideningBySelectedScalarAndAddSaturateEven_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyDoublingWideningBySelectedScalarAndAddSaturateEven(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningBySelectedScalarAndAddSaturateOdd due to it being static, abstract and generic.

    MultiplyDoublingWideningBySelectedScalarAndAddSaturateOdd : MultiplyDoublingWideningBySelectedScalarAndAddSaturateOdd_MethodGroup
    class MultiplyDoublingWideningBySelectedScalarAndAddSaturateOdd_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyDoublingWideningBySelectedScalarAndAddSaturateOdd(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningBySelectedScalarAndSubtractSaturateEven due to it being static, abstract and generic.

    MultiplyDoublingWideningBySelectedScalarAndSubtractSaturateEven : MultiplyDoublingWideningBySelectedScalarAndSubtractSaturateEven_MethodGroup
    class MultiplyDoublingWideningBySelectedScalarAndSubtractSaturateEven_MethodGroup:
        def __call__(self, minuend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyDoublingWideningBySelectedScalarAndSubtractSaturateEven(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningBySelectedScalarAndSubtractSaturateOdd due to it being static, abstract and generic.

    MultiplyDoublingWideningBySelectedScalarAndSubtractSaturateOdd : MultiplyDoublingWideningBySelectedScalarAndSubtractSaturateOdd_MethodGroup
    class MultiplyDoublingWideningBySelectedScalarAndSubtractSaturateOdd_MethodGroup:
        def __call__(self, minuend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyDoublingWideningBySelectedScalarAndSubtractSaturateOdd(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningSaturateEven due to it being static, abstract and generic.

    MultiplyDoublingWideningSaturateEven : MultiplyDoublingWideningSaturateEven_MethodGroup
    class MultiplyDoublingWideningSaturateEven_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyDoublingWideningSaturateEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyDoublingWideningSaturateEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningSaturateEvenBySelectedScalar due to it being static, abstract and generic.

    MultiplyDoublingWideningSaturateEvenBySelectedScalar : MultiplyDoublingWideningSaturateEvenBySelectedScalar_MethodGroup
    class MultiplyDoublingWideningSaturateEvenBySelectedScalar_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyDoublingWideningSaturateEvenBySelectedScalar(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningSaturateOdd due to it being static, abstract and generic.

    MultiplyDoublingWideningSaturateOdd : MultiplyDoublingWideningSaturateOdd_MethodGroup
    class MultiplyDoublingWideningSaturateOdd_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyDoublingWideningSaturateOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyDoublingWideningSaturateOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyDoublingWideningSaturateOddBySelectedScalar due to it being static, abstract and generic.

    MultiplyDoublingWideningSaturateOddBySelectedScalar : MultiplyDoublingWideningSaturateOddBySelectedScalar_MethodGroup
    class MultiplyDoublingWideningSaturateOddBySelectedScalar_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyDoublingWideningSaturateOddBySelectedScalar(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyRoundedDoublingBySelectedScalarSaturateHigh due to it being static, abstract and generic.

    MultiplyRoundedDoublingBySelectedScalarSaturateHigh : MultiplyRoundedDoublingBySelectedScalarSaturateHigh_MethodGroup
    class MultiplyRoundedDoublingBySelectedScalarSaturateHigh_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyRoundedDoublingBySelectedScalarSaturateHigh(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingBySelectedScalarSaturateHigh(left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyRoundedDoublingSaturateAndAddHigh due to it being static, abstract and generic.

    MultiplyRoundedDoublingSaturateAndAddHigh : MultiplyRoundedDoublingSaturateAndAddHigh_MethodGroup
    class MultiplyRoundedDoublingSaturateAndAddHigh_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyRoundedDoublingSaturateAndAddHigh(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingSaturateAndAddHigh(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingSaturateAndAddHigh(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyRoundedDoublingSaturateAndSubtractHigh due to it being static, abstract and generic.

    MultiplyRoundedDoublingSaturateAndSubtractHigh : MultiplyRoundedDoublingSaturateAndSubtractHigh_MethodGroup
    class MultiplyRoundedDoublingSaturateAndSubtractHigh_MethodGroup:
        def __call__(self, minuend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyRoundedDoublingSaturateAndSubtractHigh(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingSaturateAndSubtractHigh(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingSaturateAndSubtractHigh(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyRoundedDoublingSaturateBySelectedScalarAndAddHigh due to it being static, abstract and generic.

    MultiplyRoundedDoublingSaturateBySelectedScalarAndAddHigh : MultiplyRoundedDoublingSaturateBySelectedScalarAndAddHigh_MethodGroup
    class MultiplyRoundedDoublingSaturateBySelectedScalarAndAddHigh_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyRoundedDoublingSaturateBySelectedScalarAndAddHigh(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingSaturateBySelectedScalarAndAddHigh(addend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyRoundedDoublingSaturateBySelectedScalarAndSubtractHigh due to it being static, abstract and generic.

    MultiplyRoundedDoublingSaturateBySelectedScalarAndSubtractHigh : MultiplyRoundedDoublingSaturateBySelectedScalarAndSubtractHigh_MethodGroup
    class MultiplyRoundedDoublingSaturateBySelectedScalarAndSubtractHigh_MethodGroup:
        def __call__(self, minuend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplyRoundedDoublingSaturateBySelectedScalarAndSubtractHigh(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingSaturateBySelectedScalarAndSubtractHigh(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyRoundedDoublingSaturateHigh due to it being static, abstract and generic.

    MultiplyRoundedDoublingSaturateHigh : MultiplyRoundedDoublingSaturateHigh_MethodGroup
    class MultiplyRoundedDoublingSaturateHigh_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyRoundedDoublingSaturateHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingSaturateHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyRoundedDoublingSaturateHigh(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplySubtractBySelectedScalar due to it being static, abstract and generic.

    MultiplySubtractBySelectedScalar : MultiplySubtractBySelectedScalar_MethodGroup
    class MultiplySubtractBySelectedScalar_MethodGroup:
        def __call__(self, minuend: Vector_1[int], left: Vector_1[int], right: Vector_1[int], rightIndex: int) -> Vector_1[int]:...
        # Method MultiplySubtractBySelectedScalar(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplySubtractBySelectedScalar(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplySubtractBySelectedScalar(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplySubtractBySelectedScalar(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method
        # Method MultiplySubtractBySelectedScalar(minuend : Vector`1, left : Vector`1, right : Vector`1, rightIndex : Byte) was skipped since it collides with above method

    # Skipped MultiplyWideningEven due to it being static, abstract and generic.

    MultiplyWideningEven : MultiplyWideningEven_MethodGroup
    class MultiplyWideningEven_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyWideningEvenAndAdd due to it being static, abstract and generic.

    MultiplyWideningEvenAndAdd : MultiplyWideningEvenAndAdd_MethodGroup
    class MultiplyWideningEvenAndAdd_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyWideningEvenAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningEvenAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningEvenAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningEvenAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningEvenAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyWideningEvenAndSubtract due to it being static, abstract and generic.

    MultiplyWideningEvenAndSubtract : MultiplyWideningEvenAndSubtract_MethodGroup
    class MultiplyWideningEvenAndSubtract_MethodGroup:
        def __call__(self, minuend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyWideningEvenAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningEvenAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningEvenAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningEvenAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningEvenAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyWideningOdd due to it being static, abstract and generic.

    MultiplyWideningOdd : MultiplyWideningOdd_MethodGroup
    class MultiplyWideningOdd_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyWideningOddAndAdd due to it being static, abstract and generic.

    MultiplyWideningOddAndAdd : MultiplyWideningOddAndAdd_MethodGroup
    class MultiplyWideningOddAndAdd_MethodGroup:
        def __call__(self, addend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyWideningOddAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningOddAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningOddAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningOddAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningOddAndAdd(addend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped MultiplyWideningOddAndSubtract due to it being static, abstract and generic.

    MultiplyWideningOddAndSubtract : MultiplyWideningOddAndSubtract_MethodGroup
    class MultiplyWideningOddAndSubtract_MethodGroup:
        def __call__(self, minuend: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method MultiplyWideningOddAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningOddAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningOddAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningOddAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method MultiplyWideningOddAndSubtract(minuend : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped NegateSaturate due to it being static, abstract and generic.

    NegateSaturate : NegateSaturate_MethodGroup
    class NegateSaturate_MethodGroup:
        def __call__(self, value: Vector_1[int]) -> Vector_1[int]:...
        # Method NegateSaturate(value : Vector`1) was skipped since it collides with above method
        # Method NegateSaturate(value : Vector`1) was skipped since it collides with above method
        # Method NegateSaturate(value : Vector`1) was skipped since it collides with above method

    # Skipped PolynomialMultiply due to it being static, abstract and generic.

    PolynomialMultiply : PolynomialMultiply_MethodGroup
    class PolynomialMultiply_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method PolynomialMultiply(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped PolynomialMultiplyWideningEven due to it being static, abstract and generic.

    PolynomialMultiplyWideningEven : PolynomialMultiplyWideningEven_MethodGroup
    class PolynomialMultiplyWideningEven_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method PolynomialMultiplyWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped PolynomialMultiplyWideningOdd due to it being static, abstract and generic.

    PolynomialMultiplyWideningOdd : PolynomialMultiplyWideningOdd_MethodGroup
    class PolynomialMultiplyWideningOdd_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method PolynomialMultiplyWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped ShiftArithmeticRounded due to it being static, abstract and generic.

    ShiftArithmeticRounded : ShiftArithmeticRounded_MethodGroup
    class ShiftArithmeticRounded_MethodGroup:
        def __call__(self, value: Vector_1[int], count: Vector_1[int]) -> Vector_1[int]:...
        # Method ShiftArithmeticRounded(value : Vector`1, count : Vector`1) was skipped since it collides with above method
        # Method ShiftArithmeticRounded(value : Vector`1, count : Vector`1) was skipped since it collides with above method
        # Method ShiftArithmeticRounded(value : Vector`1, count : Vector`1) was skipped since it collides with above method

    # Skipped ShiftArithmeticRoundedSaturate due to it being static, abstract and generic.

    ShiftArithmeticRoundedSaturate : ShiftArithmeticRoundedSaturate_MethodGroup
    class ShiftArithmeticRoundedSaturate_MethodGroup:
        def __call__(self, value: Vector_1[int], count: Vector_1[int]) -> Vector_1[int]:...
        # Method ShiftArithmeticRoundedSaturate(value : Vector`1, count : Vector`1) was skipped since it collides with above method
        # Method ShiftArithmeticRoundedSaturate(value : Vector`1, count : Vector`1) was skipped since it collides with above method
        # Method ShiftArithmeticRoundedSaturate(value : Vector`1, count : Vector`1) was skipped since it collides with above method

    # Skipped ShiftArithmeticSaturate due to it being static, abstract and generic.

    ShiftArithmeticSaturate : ShiftArithmeticSaturate_MethodGroup
    class ShiftArithmeticSaturate_MethodGroup:
        def __call__(self, value: Vector_1[int], count: Vector_1[int]) -> Vector_1[int]:...
        # Method ShiftArithmeticSaturate(value : Vector`1, count : Vector`1) was skipped since it collides with above method
        # Method ShiftArithmeticSaturate(value : Vector`1, count : Vector`1) was skipped since it collides with above method
        # Method ShiftArithmeticSaturate(value : Vector`1, count : Vector`1) was skipped since it collides with above method

    # Skipped ShiftLeftAndInsert due to it being static, abstract and generic.

    ShiftLeftAndInsert : ShiftLeftAndInsert_MethodGroup
    class ShiftLeftAndInsert_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int], shift: int) -> Vector_1[int]:...
        # Method ShiftLeftAndInsert(left : Vector`1, right : Vector`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector`1, right : Vector`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector`1, right : Vector`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector`1, right : Vector`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector`1, right : Vector`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector`1, right : Vector`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftLeftAndInsert(left : Vector`1, right : Vector`1, shift : Byte) was skipped since it collides with above method

    # Skipped ShiftLeftLogicalSaturate due to it being static, abstract and generic.

    ShiftLeftLogicalSaturate : ShiftLeftLogicalSaturate_MethodGroup
    class ShiftLeftLogicalSaturate_MethodGroup:
        def __call__(self, value: Vector_1[int], count: Vector_1[int]) -> Vector_1[int]:...
        # Method ShiftLeftLogicalSaturate(value : Vector`1, count : Vector`1) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturate(value : Vector`1, count : Vector`1) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturate(value : Vector`1, count : Vector`1) was skipped since it collides with above method

    # Skipped ShiftLeftLogicalSaturateUnsigned due to it being static, abstract and generic.

    ShiftLeftLogicalSaturateUnsigned : ShiftLeftLogicalSaturateUnsigned_MethodGroup
    class ShiftLeftLogicalSaturateUnsigned_MethodGroup:
        def __call__(self, value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftLeftLogicalSaturateUnsigned(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturateUnsigned(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalSaturateUnsigned(value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftLeftLogicalWideningEven due to it being static, abstract and generic.

    ShiftLeftLogicalWideningEven : ShiftLeftLogicalWideningEven_MethodGroup
    class ShiftLeftLogicalWideningEven_MethodGroup:
        def __call__(self, value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftLeftLogicalWideningEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningEven(value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftLeftLogicalWideningOdd due to it being static, abstract and generic.

    ShiftLeftLogicalWideningOdd : ShiftLeftLogicalWideningOdd_MethodGroup
    class ShiftLeftLogicalWideningOdd_MethodGroup:
        def __call__(self, value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftLeftLogicalWideningOdd(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningOdd(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningOdd(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningOdd(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftLeftLogicalWideningOdd(value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftLogicalRounded due to it being static, abstract and generic.

    ShiftLogicalRounded : ShiftLogicalRounded_MethodGroup
    class ShiftLogicalRounded_MethodGroup:
        def __call__(self, value: Vector_1[int], count: Vector_1[int]) -> Vector_1[int]:...
        # Method ShiftLogicalRounded(value : Vector`1, count : Vector`1) was skipped since it collides with above method
        # Method ShiftLogicalRounded(value : Vector`1, count : Vector`1) was skipped since it collides with above method
        # Method ShiftLogicalRounded(value : Vector`1, count : Vector`1) was skipped since it collides with above method

    # Skipped ShiftLogicalRoundedSaturate due to it being static, abstract and generic.

    ShiftLogicalRoundedSaturate : ShiftLogicalRoundedSaturate_MethodGroup
    class ShiftLogicalRoundedSaturate_MethodGroup:
        def __call__(self, value: Vector_1[int], count: Vector_1[int]) -> Vector_1[int]:...
        # Method ShiftLogicalRoundedSaturate(value : Vector`1, count : Vector`1) was skipped since it collides with above method
        # Method ShiftLogicalRoundedSaturate(value : Vector`1, count : Vector`1) was skipped since it collides with above method
        # Method ShiftLogicalRoundedSaturate(value : Vector`1, count : Vector`1) was skipped since it collides with above method

    # Skipped ShiftRightAndInsert due to it being static, abstract and generic.

    ShiftRightAndInsert : ShiftRightAndInsert_MethodGroup
    class ShiftRightAndInsert_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int], shift: int) -> Vector_1[int]:...
        # Method ShiftRightAndInsert(left : Vector`1, right : Vector`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector`1, right : Vector`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector`1, right : Vector`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector`1, right : Vector`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector`1, right : Vector`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector`1, right : Vector`1, shift : Byte) was skipped since it collides with above method
        # Method ShiftRightAndInsert(left : Vector`1, right : Vector`1, shift : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticAdd due to it being static, abstract and generic.

    ShiftRightArithmeticAdd : ShiftRightArithmeticAdd_MethodGroup
    class ShiftRightArithmeticAdd_MethodGroup:
        def __call__(self, addend: Vector_1[int], value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightArithmeticAdd(addend : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticAdd(addend : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticAdd(addend : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticNarrowingSaturateEven due to it being static, abstract and generic.

    ShiftRightArithmeticNarrowingSaturateEven : ShiftRightArithmeticNarrowingSaturateEven_MethodGroup
    class ShiftRightArithmeticNarrowingSaturateEven_MethodGroup:
        def __call__(self, value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightArithmeticNarrowingSaturateEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticNarrowingSaturateEven(value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticNarrowingSaturateOdd due to it being static, abstract and generic.

    ShiftRightArithmeticNarrowingSaturateOdd : ShiftRightArithmeticNarrowingSaturateOdd_MethodGroup
    class ShiftRightArithmeticNarrowingSaturateOdd_MethodGroup:
        def __call__(self, even: Vector_1[int], value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightArithmeticNarrowingSaturateOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticNarrowingSaturateOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticNarrowingSaturateUnsignedEven due to it being static, abstract and generic.

    ShiftRightArithmeticNarrowingSaturateUnsignedEven : ShiftRightArithmeticNarrowingSaturateUnsignedEven_MethodGroup
    class ShiftRightArithmeticNarrowingSaturateUnsignedEven_MethodGroup:
        def __call__(self, value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightArithmeticNarrowingSaturateUnsignedEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticNarrowingSaturateUnsignedEven(value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticNarrowingSaturateUnsignedOdd due to it being static, abstract and generic.

    ShiftRightArithmeticNarrowingSaturateUnsignedOdd : ShiftRightArithmeticNarrowingSaturateUnsignedOdd_MethodGroup
    class ShiftRightArithmeticNarrowingSaturateUnsignedOdd_MethodGroup:
        def __call__(self, even: Vector_1[int], value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightArithmeticNarrowingSaturateUnsignedOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticNarrowingSaturateUnsignedOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticRounded due to it being static, abstract and generic.

    ShiftRightArithmeticRounded : ShiftRightArithmeticRounded_MethodGroup
    class ShiftRightArithmeticRounded_MethodGroup:
        def __call__(self, value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightArithmeticRounded(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRounded(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRounded(value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticRoundedAdd due to it being static, abstract and generic.

    ShiftRightArithmeticRoundedAdd : ShiftRightArithmeticRoundedAdd_MethodGroup
    class ShiftRightArithmeticRoundedAdd_MethodGroup:
        def __call__(self, addend: Vector_1[int], value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightArithmeticRoundedAdd(addend : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRoundedAdd(addend : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRoundedAdd(addend : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticRoundedNarrowingSaturateEven due to it being static, abstract and generic.

    ShiftRightArithmeticRoundedNarrowingSaturateEven : ShiftRightArithmeticRoundedNarrowingSaturateEven_MethodGroup
    class ShiftRightArithmeticRoundedNarrowingSaturateEven_MethodGroup:
        def __call__(self, value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightArithmeticRoundedNarrowingSaturateEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRoundedNarrowingSaturateEven(value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticRoundedNarrowingSaturateOdd due to it being static, abstract and generic.

    ShiftRightArithmeticRoundedNarrowingSaturateOdd : ShiftRightArithmeticRoundedNarrowingSaturateOdd_MethodGroup
    class ShiftRightArithmeticRoundedNarrowingSaturateOdd_MethodGroup:
        def __call__(self, even: Vector_1[int], value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightArithmeticRoundedNarrowingSaturateOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRoundedNarrowingSaturateOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticRoundedNarrowingSaturateUnsignedEven due to it being static, abstract and generic.

    ShiftRightArithmeticRoundedNarrowingSaturateUnsignedEven : ShiftRightArithmeticRoundedNarrowingSaturateUnsignedEven_MethodGroup
    class ShiftRightArithmeticRoundedNarrowingSaturateUnsignedEven_MethodGroup:
        def __call__(self, value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightArithmeticRoundedNarrowingSaturateUnsignedEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRoundedNarrowingSaturateUnsignedEven(value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightArithmeticRoundedNarrowingSaturateUnsignedOdd due to it being static, abstract and generic.

    ShiftRightArithmeticRoundedNarrowingSaturateUnsignedOdd : ShiftRightArithmeticRoundedNarrowingSaturateUnsignedOdd_MethodGroup
    class ShiftRightArithmeticRoundedNarrowingSaturateUnsignedOdd_MethodGroup:
        def __call__(self, even: Vector_1[int], value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightArithmeticRoundedNarrowingSaturateUnsignedOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightArithmeticRoundedNarrowingSaturateUnsignedOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalAdd due to it being static, abstract and generic.

    ShiftRightLogicalAdd : ShiftRightLogicalAdd_MethodGroup
    class ShiftRightLogicalAdd_MethodGroup:
        def __call__(self, addend: Vector_1[int], value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightLogicalAdd(addend : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalAdd(addend : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalAdd(addend : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalNarrowingEven due to it being static, abstract and generic.

    ShiftRightLogicalNarrowingEven : ShiftRightLogicalNarrowingEven_MethodGroup
    class ShiftRightLogicalNarrowingEven_MethodGroup:
        def __call__(self, value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightLogicalNarrowingEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingEven(value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalNarrowingOdd due to it being static, abstract and generic.

    ShiftRightLogicalNarrowingOdd : ShiftRightLogicalNarrowingOdd_MethodGroup
    class ShiftRightLogicalNarrowingOdd_MethodGroup:
        def __call__(self, even: Vector_1[int], value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightLogicalNarrowingOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalNarrowingOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalRounded due to it being static, abstract and generic.

    ShiftRightLogicalRounded : ShiftRightLogicalRounded_MethodGroup
    class ShiftRightLogicalRounded_MethodGroup:
        def __call__(self, value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightLogicalRounded(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRounded(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRounded(value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalRoundedAdd due to it being static, abstract and generic.

    ShiftRightLogicalRoundedAdd : ShiftRightLogicalRoundedAdd_MethodGroup
    class ShiftRightLogicalRoundedAdd_MethodGroup:
        def __call__(self, addend: Vector_1[int], value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightLogicalRoundedAdd(addend : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedAdd(addend : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedAdd(addend : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalRoundedNarrowingEven due to it being static, abstract and generic.

    ShiftRightLogicalRoundedNarrowingEven : ShiftRightLogicalRoundedNarrowingEven_MethodGroup
    class ShiftRightLogicalRoundedNarrowingEven_MethodGroup:
        def __call__(self, value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightLogicalRoundedNarrowingEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingEven(value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalRoundedNarrowingOdd due to it being static, abstract and generic.

    ShiftRightLogicalRoundedNarrowingOdd : ShiftRightLogicalRoundedNarrowingOdd_MethodGroup
    class ShiftRightLogicalRoundedNarrowingOdd_MethodGroup:
        def __call__(self, even: Vector_1[int], value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightLogicalRoundedNarrowingOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalRoundedNarrowingSaturateEven due to it being static, abstract and generic.

    ShiftRightLogicalRoundedNarrowingSaturateEven : ShiftRightLogicalRoundedNarrowingSaturateEven_MethodGroup
    class ShiftRightLogicalRoundedNarrowingSaturateEven_MethodGroup:
        def __call__(self, value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightLogicalRoundedNarrowingSaturateEven(value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingSaturateEven(value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped ShiftRightLogicalRoundedNarrowingSaturateOdd due to it being static, abstract and generic.

    ShiftRightLogicalRoundedNarrowingSaturateOdd : ShiftRightLogicalRoundedNarrowingSaturateOdd_MethodGroup
    class ShiftRightLogicalRoundedNarrowingSaturateOdd_MethodGroup:
        def __call__(self, even: Vector_1[int], value: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method ShiftRightLogicalRoundedNarrowingSaturateOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method
        # Method ShiftRightLogicalRoundedNarrowingSaturateOdd(even : Vector`1, value : Vector`1, count : Byte) was skipped since it collides with above method

    # Skipped SubtractBorrowWideningEven due to it being static, abstract and generic.

    SubtractBorrowWideningEven : SubtractBorrowWideningEven_MethodGroup
    class SubtractBorrowWideningEven_MethodGroup:
        def __call__(self, op1: Vector_1[int], op2: Vector_1[int], op3: Vector_1[int]) -> Vector_1[int]:...
        # Method SubtractBorrowWideningEven(op1 : Vector`1, op2 : Vector`1, op3 : Vector`1) was skipped since it collides with above method

    # Skipped SubtractBorrowWideningOdd due to it being static, abstract and generic.

    SubtractBorrowWideningOdd : SubtractBorrowWideningOdd_MethodGroup
    class SubtractBorrowWideningOdd_MethodGroup:
        def __call__(self, op1: Vector_1[int], op2: Vector_1[int], op3: Vector_1[int]) -> Vector_1[int]:...
        # Method SubtractBorrowWideningOdd(op1 : Vector`1, op2 : Vector`1, op3 : Vector`1) was skipped since it collides with above method

    # Skipped SubtractHighNarrowingEven due to it being static, abstract and generic.

    SubtractHighNarrowingEven : SubtractHighNarrowingEven_MethodGroup
    class SubtractHighNarrowingEven_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method SubtractHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped SubtractHighNarrowingOdd due to it being static, abstract and generic.

    SubtractHighNarrowingOdd : SubtractHighNarrowingOdd_MethodGroup
    class SubtractHighNarrowingOdd_MethodGroup:
        def __call__(self, even: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method SubtractHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped SubtractRoundedHighNarrowingEven due to it being static, abstract and generic.

    SubtractRoundedHighNarrowingEven : SubtractRoundedHighNarrowingEven_MethodGroup
    class SubtractRoundedHighNarrowingEven_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method SubtractRoundedHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped SubtractRoundedHighNarrowingOdd due to it being static, abstract and generic.

    SubtractRoundedHighNarrowingOdd : SubtractRoundedHighNarrowingOdd_MethodGroup
    class SubtractRoundedHighNarrowingOdd_MethodGroup:
        def __call__(self, even: Vector_1[int], left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method SubtractRoundedHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractRoundedHighNarrowingOdd(even : Vector`1, left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped SubtractSaturate due to it being static, abstract and generic.

    SubtractSaturate : SubtractSaturate_MethodGroup
    class SubtractSaturate_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method SubtractSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractSaturate(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped SubtractWideningEven due to it being static, abstract and generic.

    SubtractWideningEven : SubtractWideningEven_MethodGroup
    class SubtractWideningEven_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method SubtractWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped SubtractWideningEvenOdd due to it being static, abstract and generic.

    SubtractWideningEvenOdd : SubtractWideningEvenOdd_MethodGroup
    class SubtractWideningEvenOdd_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method SubtractWideningEvenOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningEvenOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped SubtractWideningOdd due to it being static, abstract and generic.

    SubtractWideningOdd : SubtractWideningOdd_MethodGroup
    class SubtractWideningOdd_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method SubtractWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningOdd(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped SubtractWideningOddEven due to it being static, abstract and generic.

    SubtractWideningOddEven : SubtractWideningOddEven_MethodGroup
    class SubtractWideningOddEven_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int]) -> Vector_1[int]:...
        # Method SubtractWideningOddEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method
        # Method SubtractWideningOddEven(left : Vector`1, right : Vector`1) was skipped since it collides with above method

    # Skipped VectorTableLookup due to it being static, abstract and generic.

    VectorTableLookup : VectorTableLookup_MethodGroup
    class VectorTableLookup_MethodGroup:
        def __call__(self, table: ValueTuple_2[Vector_1[int], Vector_1[int]], indices: Vector_1[int]) -> Vector_1[int]:...
        # Method VectorTableLookup(table : ValueTuple`2, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(table : ValueTuple`2, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(table : ValueTuple`2, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(table : ValueTuple`2, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(table : ValueTuple`2, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(table : ValueTuple`2, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(table : ValueTuple`2, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(table : ValueTuple`2, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookup(table : ValueTuple`2, indices : Vector`1) was skipped since it collides with above method

    # Skipped VectorTableLookupExtension due to it being static, abstract and generic.

    VectorTableLookupExtension : VectorTableLookupExtension_MethodGroup
    class VectorTableLookupExtension_MethodGroup:
        def __call__(self, defaultValues: Vector_1[float], data: Vector_1[float], indices: Vector_1[int]) -> Vector_1[float]:...
        # Method VectorTableLookupExtension(defaultValues : Vector`1, data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookupExtension(defaultValues : Vector`1, data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookupExtension(defaultValues : Vector`1, data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookupExtension(defaultValues : Vector`1, data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookupExtension(defaultValues : Vector`1, data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookupExtension(defaultValues : Vector`1, data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookupExtension(defaultValues : Vector`1, data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookupExtension(defaultValues : Vector`1, data : Vector`1, indices : Vector`1) was skipped since it collides with above method
        # Method VectorTableLookupExtension(defaultValues : Vector`1, data : Vector`1, indices : Vector`1) was skipped since it collides with above method

    # Skipped Xor due to it being static, abstract and generic.

    Xor : Xor_MethodGroup
    class Xor_MethodGroup:
        def __call__(self, value1: Vector_1[int], value2: Vector_1[int], value3: Vector_1[int]) -> Vector_1[int]:...
        # Method Xor(value1 : Vector`1, value2 : Vector`1, value3 : Vector`1) was skipped since it collides with above method
        # Method Xor(value1 : Vector`1, value2 : Vector`1, value3 : Vector`1) was skipped since it collides with above method
        # Method Xor(value1 : Vector`1, value2 : Vector`1, value3 : Vector`1) was skipped since it collides with above method
        # Method Xor(value1 : Vector`1, value2 : Vector`1, value3 : Vector`1) was skipped since it collides with above method
        # Method Xor(value1 : Vector`1, value2 : Vector`1, value3 : Vector`1) was skipped since it collides with above method
        # Method Xor(value1 : Vector`1, value2 : Vector`1, value3 : Vector`1) was skipped since it collides with above method
        # Method Xor(value1 : Vector`1, value2 : Vector`1, value3 : Vector`1) was skipped since it collides with above method

    # Skipped XorRotateRight due to it being static, abstract and generic.

    XorRotateRight : XorRotateRight_MethodGroup
    class XorRotateRight_MethodGroup:
        def __call__(self, left: Vector_1[int], right: Vector_1[int], count: int) -> Vector_1[int]:...
        # Method XorRotateRight(left : Vector`1, right : Vector`1, count : Byte) was skipped since it collides with above method
        # Method XorRotateRight(left : Vector`1, right : Vector`1, count : Byte) was skipped since it collides with above method
        # Method XorRotateRight(left : Vector`1, right : Vector`1, count : Byte) was skipped since it collides with above method
        # Method XorRotateRight(left : Vector`1, right : Vector`1, count : Byte) was skipped since it collides with above method
        # Method XorRotateRight(left : Vector`1, right : Vector`1, count : Byte) was skipped since it collides with above method
        # Method XorRotateRight(left : Vector`1, right : Vector`1, count : Byte) was skipped since it collides with above method
        # Method XorRotateRight(left : Vector`1, right : Vector`1, count : Byte) was skipped since it collides with above method


    class Arm64(Sve.Arm64):
        @classmethod
        @property
        def IsSupported(cls) -> bool: ...



class SveMaskPattern(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    LargestPowerOf2 : SveMaskPattern # 0
    VectorCount1 : SveMaskPattern # 1
    VectorCount2 : SveMaskPattern # 2
    VectorCount3 : SveMaskPattern # 3
    VectorCount4 : SveMaskPattern # 4
    VectorCount5 : SveMaskPattern # 5
    VectorCount6 : SveMaskPattern # 6
    VectorCount7 : SveMaskPattern # 7
    VectorCount8 : SveMaskPattern # 8
    VectorCount16 : SveMaskPattern # 9
    VectorCount32 : SveMaskPattern # 10
    VectorCount64 : SveMaskPattern # 11
    VectorCount128 : SveMaskPattern # 12
    VectorCount256 : SveMaskPattern # 13
    LargestMultipleOf4 : SveMaskPattern # 29
    LargestMultipleOf3 : SveMaskPattern # 30
    All : SveMaskPattern # 31


class SvePrefetchType(typing.SupportsInt):
    @typing.overload
    def __init__(self, value : int) -> None: ...
    @typing.overload
    def __init__(self, value : int, force_if_true: bool) -> None: ...
    def __int__(self) -> int: ...
    
    # Values:
    LoadL1Temporal : SvePrefetchType # 0
    LoadL1NonTemporal : SvePrefetchType # 1
    LoadL2Temporal : SvePrefetchType # 2
    LoadL2NonTemporal : SvePrefetchType # 3
    LoadL3Temporal : SvePrefetchType # 4
    LoadL3NonTemporal : SvePrefetchType # 5
    StoreL1Temporal : SvePrefetchType # 8
    StoreL1NonTemporal : SvePrefetchType # 9
    StoreL2Temporal : SvePrefetchType # 10
    StoreL2NonTemporal : SvePrefetchType # 11
    StoreL3Temporal : SvePrefetchType # 12
    StoreL3NonTemporal : SvePrefetchType # 13

