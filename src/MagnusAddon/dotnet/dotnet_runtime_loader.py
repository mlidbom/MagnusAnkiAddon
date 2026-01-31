from __future__ import annotations

import os

import mylog
from pythonnet import load

config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runtimeconfig.json")

loaded: bool = False
def ensure_clr_loaded() -> None:
    global loaded
    if loaded: return
    try:
        load("coreclr", runtime_config=config_file)
        # load("coreclr", runtime_config="path/to/runtimeconfig.json")
        mylog.info("Loaded .NET runtime")
        import clr  # pyright: ignore [reportMissingTypeStubs]
        clr.AddReference("System.Runtime")  # pyright: ignore [reportAttributeAccessIssue, reportUnknownMemberType]
        from System import Environment  # pyright: ignore [reportMissingModuleSource]
        dotnet_version = Environment.Version
        print(f"Running .NET version: {dotnet_version}")
    except RuntimeError as e:
        if "Failed to create a .NET runtime" in str(e):
            # Show user-friendly error with installation instructions
            mylog.error(
                    """This addon requires .NET 10.0 or newer.
                    Please install from: https://dotnet.microsoft.com/download"""
            )
        raise
    except ImportError as e:
        mylog.error(f"Python.NET package {e.name} not found.")
        raise
    loaded = True
