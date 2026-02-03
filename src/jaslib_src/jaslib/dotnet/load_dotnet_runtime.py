from __future__ import annotations

import os
from pathlib import Path

from jaslib import mylog
from jaslib.sysutils.timeutil import StopWatch
from pythonnet import load

config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runtimeconfig.json")

def _get_workspace_root() -> Path:
    return Path(os.path.abspath(__file__)).parent.parent.parent.parent

try:
    with StopWatch.log_execution_time("Loading .NET runtime"):
        load("coreclr", runtime_config=config_file)
        mylog.info("Loaded .NET runtime")
        import clr

        clr.AddReference("System.Runtime")
        # noinspection PyPackageRequirements
        from System import Environment

        dotnet_version = Environment.Version
        print(f"Running .NET version: {dotnet_version}")

        # Load JAStudio assemblies
        workspace_root = _get_workspace_root()
        jastudio_dlls = [
                workspace_root / "src_dotnet" / "JAStudio.Core" / "bin" / "Debug" / "net10.0" / "JAStudio.Core.dll",
                workspace_root / "src_dotnet" / "JAStudio.PythonInterop" / "bin" / "Debug" / "net10.0" / "JAStudio.PythonInterop.dll",
        ]

        for dll_path in jastudio_dlls:
            clr.AddReference(str(dll_path))
            mylog.info(f"Loaded assembly: {dll_path.name}")

except RuntimeError as e:
    if "Failed to create a .NET runtime" in str(e):
        mylog.error(
                """This addon requires .NET 10.0 or newer.
                Please install from: https://dotnet.microsoft.com/download"""
        )
    raise
except ImportError as e:
    mylog.error(f"Python.NET package {e.name} not found.")
    raise
