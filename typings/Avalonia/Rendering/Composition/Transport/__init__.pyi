from System.Threading.Tasks import Task

class CompositionBatch:
    @property
    def Processed(self) -> Task: ...
    @property
    def Rendered(self) -> Task: ...

