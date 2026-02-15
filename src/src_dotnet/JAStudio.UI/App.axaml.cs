using System;
using System.Threading;
using Avalonia;
using Avalonia.Markup.Xaml;

namespace JAStudio.UI;

public class App : Application
{
   static readonly ManualResetEventSlim Initialized = new();

   public override void Initialize() => AvaloniaXamlLoader.Load(this);

   public override void OnFrameworkInitializationCompleted()
   {
      base.OnFrameworkInitializationCompleted();
      Initialized.Set();
   }

   internal static void WaitForInitialization(TimeSpan timeout)
   {
      if(!Initialized.Wait(timeout))
      {
         throw new TimeoutException(
            $"Avalonia did not initialize within {timeout.TotalSeconds}s.");
      }
   }
}
