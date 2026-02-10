import abc
from System.ComponentModel import INotifyPropertyChanging, INotifyPropertyChanged

class ObservableObject(INotifyPropertyChanging, INotifyPropertyChanged, abc.ABC):
    pass

