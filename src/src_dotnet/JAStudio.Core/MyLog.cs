using Compze.Utilities.SystemCE;
using JAStudio.Core.TestUtils;
using System;

namespace JAStudio.Core;

public static class MyLog
{
    private static LazyCE<ILogger> _logger = new(() => GetLogger());

    private static ILogger GetLogger()
    {
        return new ConsoleLogger();
    }

    public static void Debug(string msg)
    {
        if (!ExPytest.IsTesting)
        {
            _logger.Value.Debug(msg);
        }
    }

    public static void Info(string msg)
    {
        if (!ExPytest.IsTesting)
        {
            _logger.Value.Info(msg);
        }
    }

    public static void Warning(string msg)
    {
        _logger.Value.Warning(msg);
    }

    public static void Error(string msg)
    {
        _logger.Value.Error(msg);
    }

    public static void SetLoggerFactory(LazyCE<ILogger> logger)
    {
        _logger = logger;
    }
}

public interface ILogger
{
    void Debug(string message);
    void Info(string message);
    void Warning(string message);
    void Error(string message);
}

public class ConsoleLogger : ILogger
{
    public void Debug(string message)
    {
        Console.WriteLine($"DEBUG: {message}");
    }

    public void Info(string message)
    {
        Console.WriteLine($"INFO: {message}");
    }

    public void Warning(string message)
    {
        Console.WriteLine($"WARNING: {message}");
    }

    public void Error(string message)
    {
        Console.WriteLine($"ERROR: {message}");
    }
}
