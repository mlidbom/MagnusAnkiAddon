"""Type stubs for the clr module from Python.NET"""

from typing import Any, overload

def AddReference(*names: str) -> list[Any]:
    """
    Add references to multiple .NET assemblies.
    
    Args:
        names: Multiple assembly names or paths
        
    Returns:
        List of loaded assembly references
    """
    ...

def GetClrType(type: type) -> Any:
    """Get the CLR type for a Python type."""
    ...

def SetCommandLine(*args: str) -> None:
    """Set command line arguments for the CLR."""
    ...

# Additional commonly used functions
def ListAssemblies() -> list[str]:
    """List all loaded assemblies."""
    ...

def FindAssembly(name: str) -> Any:
    """Find a loaded assembly by name."""
    ...
