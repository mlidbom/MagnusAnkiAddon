from __future__ import annotations

import os
from pathlib import Path

from jaspythonutils.sysutils.timeutil import StopWatch
from jastudio import mylog
import atexit

from pythonnet import load, unload

config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "runtimeconfig.json")

def _get_workspace_root() -> Path:
    return Path(os.path.abspath(__file__)).parent.parent.parent.parent

try:
    with StopWatch.log_execution_time("Loading .NET runtime"):
        load("coreclr", runtime_config=config_file)
        # pythonnet registers atexit.register(unload) during load(). That unload triggers
        # Runtime.Shutdown() which runs ~86 rounds of GC.Collect()+WaitForPendingFinalizers().
        # With our multi-GB managed heap this takes 8-30+ seconds on process exit.
        # coreclr cannot be unloaded from a process anyway — the OS reclaims all memory on exit.
        atexit.unregister(unload)
        mylog.info("Loaded .NET runtime")
        import clr

        clr.AddReference("System.Runtime")
        # noinspection PyPackageRequirements
        from System import Environment

        dotnet_version = Environment.Version
        print(f"Running .NET version: {dotnet_version}")

        # Load JAStudio assemblies from runtime_binaries folder
        # (copied there by build to avoid locking issues with Anki)
        workspace_root = _get_workspace_root()
        runtime_binaries = workspace_root / "runtime_binaries"
        jastudio_dlls = [
                runtime_binaries / "JAStudio.Core.dll",
                runtime_binaries / "JAStudio.PythonInterop.dll",
                runtime_binaries / "JAStudio.UI.dll",
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
