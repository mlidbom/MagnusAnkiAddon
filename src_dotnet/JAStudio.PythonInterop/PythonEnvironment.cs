using System;
using System.IO;
using System.Linq;
using Python.Runtime;

namespace JAStudio.PythonInterop;

public static class PythonEnvironment
{
    private static readonly object _lock = new();

    /// <param name="venvPath">Optional path to venv. If not provided, uses JASTUDIO_VENV_PATH environment variable or auto-detects.</param>
    public static void EnsureInitialized(string? venvPath = null)
    {
        if (PythonEngine.IsInitialized) return;
        lock (_lock)
        {
            if (PythonEngine.IsInitialized) return;

            venvPath ??= GetVenvPath();

            if (!Directory.Exists(venvPath))
            {
                throw new Exception($"""
                                     Python venv not found at: {venvPath}
                                     Please set JASTUDIO_VENV_PATH environment variable to your venv location.
                                     Current directory: {Directory.GetCurrentDirectory()}
                                     """);
            }

            // Read pyvenv.cfg to find base Python installation
            var pyvenvCfg = Path.Combine(venvPath, "pyvenv.cfg");
            if (!File.Exists(pyvenvCfg))
            {
                throw new Exception($"pyvenv.cfg not found at: {pyvenvCfg}");
            }

            var basePython = GetBasePythonFromConfig(pyvenvCfg);
            if (basePython == null)
            {
                throw new Exception($"Could not find base Python from {pyvenvCfg}");
            }

            // Find the Python DLL
            var pythonDll = FindPythonDll(venvPath, basePython);
            if (pythonDll == null)
            {
                throw new Exception($"Could not find Python DLL in {venvPath} or {basePython}");
            }

            Console.WriteLine($"[PythonEnvironment] Using venv: {venvPath}");
            Console.WriteLine($"[PythonEnvironment] Base Python: {basePython}");
            Console.WriteLine($"[PythonEnvironment] Python DLL: {pythonDll}");

            // Configure Python.NET
            Runtime.PythonDLL = pythonDll;
            PythonEngine.PythonHome = basePython;
            PythonEngine.PythonPath = string.Join(
                Path.PathSeparator.ToString(),
                Path.Combine(basePython, "Lib"),
                Path.Combine(venvPath, "Lib", "site-packages"),
                Path.Combine(basePython, "DLLs")
            );

            PythonEngine.Initialize();
            PythonEngine.BeginAllowThreads();
        }
    }

    private static string GetVenvPath()
    {
        var envPath = Environment.GetEnvironmentVariable("JASTUDIO_VENV_PATH");
        if (!string.IsNullOrEmpty(envPath))
        {
            return envPath;
        }

        var projectRoot = Path.GetFullPath(Path.Combine(
            Directory.GetCurrentDirectory(),
            "..", "..", "..", "..", ".."
        ));
        return Path.Combine(projectRoot, "venv");
    }

    private static string? GetBasePythonFromConfig(string pyvenvCfgPath)
    {
        return File.ReadAllLines(pyvenvCfgPath)
            .Where(line => line.StartsWith("home = "))
            .Select(line => line[7..].Trim())
            .FirstOrDefault();
    }

    private static string? FindPythonDll(string venvPath, string basePython)
    {
        var venvScripts = Path.Combine(venvPath, "Scripts");

        if (Directory.Exists(venvScripts))
        {
            var venvDll = Directory.GetFiles(venvScripts, "python3??.dll")
                .OrderByDescending(f => f)
                .FirstOrDefault();

            if (venvDll != null)
            {
                return venvDll;
            }
        }

        return null;
    }
}