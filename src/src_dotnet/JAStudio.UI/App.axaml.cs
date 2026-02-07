using Avalonia;
using Avalonia.Controls.ApplicationLifetimes;
using Avalonia.Markup.Xaml;

namespace JAStudio.UI;

public class App : Application
{
    public override void Initialize() => AvaloniaXamlLoader.Load(this);

    public override void OnFrameworkInitializationCompleted()
    {
        if (ApplicationLifetime is IClassicDesktopStyleApplicationLifetime desktop)
        {
            // No main window - we're hosted by Anki/Python
            // Windows are shown on-demand via JAStudioAppRoot
        }

        base.OnFrameworkInitializationCompleted();
    }
}
