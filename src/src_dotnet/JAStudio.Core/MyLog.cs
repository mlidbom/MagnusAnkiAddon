using System;
using JAStudio.Core.TestUtils;

namespace JAStudio.Core;

public class MyLog
{
   readonly TemporaryServiceCollection _services;
   internal MyLog(TemporaryServiceCollection services) => _services = services;

   public static void Debug(string message) => Log("DEBUG", message, !ExPytest.IsTesting);
   public static void Info(string message) => Log("INFO", message, !ExPytest.IsTesting);
   public static void Warning(string message) => Log($"WARNING", message);
   public static void Error(string message) => Log("ERROR", message);

   static void Log(string prefix, string message, bool shouldLog = true)
   {
      if(shouldLog) Console.WriteLine($"{prefix}: {message}");
   }
}
