import typing
from System import IServiceProvider

class !AvaloniaResources:
    pass


class !XamlLoader:
    # Skipped TryLoad due to it being static, abstract and generic.

    TryLoad : TryLoad_MethodGroup
    class TryLoad_MethodGroup:
        @typing.overload
        def __call__(self, : str) -> typing.Any:...
        @typing.overload
        def __call__(self, : IServiceProvider, : str) -> typing.Any:...


