from __future__ import annotations

import os

import mylog
from pythonnet import load  # pyright: ignore [reportMissingTypeStubs]

config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dotnet_runtimeconfig.json")

def load_clr() -> None:
    try:
        load("coreclr", runtime_config=config_file)
        # load("coreclr", runtime_config="path/to/runtimeconfig.json")
        mylog.info("Loaded .NET runtime")
        import clr
        mylog.info("Loaded clr module")
    except RuntimeError as e:
        if "Failed to create a .NET runtime" in str(e):
            # Show user-friendly error with installation instructions
            mylog.error(
                    "This addon requires .NET 8.0 or newer.\n"
                    "Please install from: https://dotnet.microsoft.com/download"
            )
        raise
    except ImportError as e:
        mylog.error(f"Python.NET package {e.name} not found.")
        raise
