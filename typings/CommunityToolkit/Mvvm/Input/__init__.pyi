import typing, abc
from System.Windows.Input import ICommand

class IRelayCommand(ICommand, typing.Protocol):
    @abc.abstractmethod
    def NotifyCanExecuteChanged(self) -> None: ...

