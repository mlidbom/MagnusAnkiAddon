using System;
using JAStudio.Core.TestUtils;

namespace JAStudio.Core;

public static class MyLog
{
   public static void Debug(string message) => Log("DEBUG", message, !TestEnvDetector.IsTesting);
   public static void Info(string message) => Log("INFO", message, !TestEnvDetector.IsTesting);
   public static void Warning(string message) => Log($"WARNING", message);
   public static void Error(string message) => Log("ERROR", message);

   static void Log(string prefix, string message, bool shouldLog = true)
   {
      if(shouldLog) Console.WriteLine($"{prefix}: {message}");
   }
}
