using System;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
using JAStudio.Core.UI.Web;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;

namespace JAStudio.Web;

/// <summary>
/// Hosts a Blazor Server application on localhost.
/// Started in-process by the Anki addon via pythonnet.
/// The iframe in the Anki card template points at this server.
/// </summary>
public class CardServer
{
   WebApplication? _app;

   public int Port { get; private set; }
   public string BaseUrl => $"http://localhost:{Port}";

   /// <summary>
   /// Starts the Kestrel web server on a random available port.
   /// Call from Python on addon startup.
   /// </summary>
   // ReSharper disable once UnusedMember.Global — called from Python
   public void Start()
   {
      var builder = WebApplication.CreateBuilder();
      builder.WebHost.ConfigureKestrel(options => options.Listen(System.Net.IPAddress.Loopback, 0));

      builder.Services.AddRazorComponents()
                      .AddInteractiveServerComponents();

      _app = builder.Build();

      _app.UseStaticFiles();
      _app.UseAntiforgery();

      _app.MapRazorComponents<Components.App>()
          .AddInteractiveServerRenderMode();

      _app.RunAsync();

      // Resolve the actual port assigned by the OS
      var address = _app.Urls.First();
      Port = new Uri(address).Port;
      CardServerUrl.BaseUrl = BaseUrl;
      Console.WriteLine($"[CardServer] Listening on {BaseUrl}");
   }

   /// <summary>
   /// Stops the web server. Call on addon shutdown.
   /// </summary>
   // ReSharper disable once UnusedMember.Global — called from Python
   public async Task StopAsync()
   {
      if(_app != null)
      {
         await _app.StopAsync(CancellationToken.None);
         await _app.DisposeAsync();
         _app = null;
         Console.WriteLine("[CardServer] Stopped");
      }
   }
}
