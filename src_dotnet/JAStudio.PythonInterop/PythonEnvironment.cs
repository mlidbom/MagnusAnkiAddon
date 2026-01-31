namespace JAStudio.PythonInterop;

using System;
using System.IO;
using System.Linq;
using Python.Runtime;

/// <summary>
/// Manages Python environment initialization for the application.
/// Ensures the correct venv is used with all required packages.
/// </summary>
public static class PythonEnvironment
{
    private static readonly object _lock = new();
    private static bool _initialized = false;

    /// <summary>
    /// Initialize the Python runtime using the project's venv.
    /// Safe to call multiple times - will only initialize once.
    /// </summary>
    /// <param name="venvPath">Optional path to venv. If not provided, uses JASTUDIO_VENV_PATH environment variable or auto-detects.</param>
    public static void Initialize(string? venvPath = null)
    {
        lock (_lock)
        {
            if (_initialized || PythonEngine.IsInitialized)
            {
                return;
            }

            venvPath ??= GetVenvPath();

            if (!Directory.Exists(venvPath))
            {
                throw new Exception(
                    $"Python venv not found at: {venvPath}\n" +
                    $"Please set JASTUDIO_VENV_PATH environment variable to your venv location.\n" +
                    $"Current directory: {Directory.GetCurrentDirectory()}"
                );
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

            _initialized = true;
        }
    }

    /// <summary>
    /// Get the venv path from environment variable or auto-detect.
    /// </summary>
    private static string GetVenvPath()
    {
        // First try environment variable (required for NCrunch and other test runners)
        var envPath = Environment.GetEnvironmentVariable("JASTUDIO_VENV_PATH");
        if (!string.IsNullOrEmpty(envPath))
        {
            return envPath;
        }

        // Fallback: try to find venv relative to current directory
        // This works when running from the project directory
        // Navigate up from bin/Debug/net10.0 (3 levels) + JAStudio.Core.Tests (1 level) + src_dotnet (1 level) = 5 levels
        var projectRoot = Path.GetFullPath(Path.Combine(
            Directory.GetCurrentDirectory(),
            "..", "..", "..", "..", ".."
        ));
        return Path.Combine(projectRoot, "venv");
    }

    /// <summary>
    /// Read pyvenv.cfg to find the base Python installation path.
    /// </summary>
    private static string? GetBasePythonFromConfig(string pyvenvCfgPath)
    {
        foreach (var line in File.ReadAllLines(pyvenvCfgPath))
        {
            if (line.StartsWith("home = "))
            {
                return line.Substring(7).Trim();
            }
        }
        return null;
    }

    /// <summary>
    /// Find the Python DLL, preferring version-specific DLLs over generic ones.
    /// </summary>
    private static string? FindPythonDll(string venvPath, string basePython)
    {
        // Prefer version-specific DLLs (python313.dll) over generic (python3.dll)
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

        // Fallback to base Python
        if (Directory.Exists(basePython))
        {
            return Directory.GetFiles(basePython, "python3??.dll")
                .OrderByDescending(f => f)
                .FirstOrDefault();
        }

        return null;
    }

    /// <summary>
    /// Check if Python environment is initialized.
    /// </summary>
    public static bool IsInitialized => _initialized && PythonEngine.IsInitialized;
}
