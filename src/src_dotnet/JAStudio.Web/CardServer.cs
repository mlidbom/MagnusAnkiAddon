using System;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Net;
using System.Threading;
using System.Threading.Tasks;
using JAStudio.Core;
using JAStudio.Core.Configuration;
using JAStudio.Core.Note.Collection;
using JAStudio.Core.Storage.Media;
using JAStudio.Core.UI.Web;
using JAStudio.Core.ViewModels.KanjiList;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
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
   /// Starts the Kestrel web server, reusing the previously saved port if available.
   /// Falls back to an OS-assigned port if the saved port is unavailable.
   /// Call from Python on addon startup.
   /// </summary>
   // ReSharper disable once UnusedMember.Global — called from Python
   public void Start()
   {
      // Prevent ASP.NET from scanning for hosting startup assemblies (we're hosted in Anki's process)
      Environment.SetEnvironmentVariable("ASPNETCORE_PREVENTHOSTINGSTARTUP", "true");

      var preferredPort = LoadSavedPort();
      if(preferredPort > 0)
      {
         try
         {
            StartOnPort(preferredPort);
            return;
         }
         catch(IOException)
         {
            Console.WriteLine($"[CardServer] Port {preferredPort} unavailable, falling back to OS-assigned port");
         }
      }

      StartOnPort(0);
   }

   void StartOnPort(int port)
   {
      var assemblyDir = Path.GetDirectoryName(typeof(CardServer).Assembly.Location)!;
      var builder = WebApplication.CreateBuilder(new WebApplicationOptions
      {
         EnvironmentName = "Production",
         ApplicationName = typeof(CardServer).Assembly.GetName().Name!,
         ContentRootPath = assemblyDir,
         WebRootPath = Path.Combine(assemblyDir, "wwwroot"),
      });
      builder.WebHost.ConfigureKestrel(options => options.Listen(IPAddress.Loopback, port));
      builder.WebHost.UseStaticWebAssets();

      builder.Services.AddRazorComponents()
                      .AddInteractiveServerComponents();

      // Bridge domain services from the Compze service locator into Blazor DI.
      // These are singletons managed by the Core bootstrapper.
      builder.Services.AddSingleton(_ => TemporaryServiceCollection.Instance.CoreApp.Collection);
      builder.Services.AddSingleton(_ => TemporaryServiceCollection.Instance.CoreApp.Collection.Kanji);
      builder.Services.AddSingleton(_ => TemporaryServiceCollection.Instance.CoreApp.Collection.Vocab);
      builder.Services.AddSingleton(_ => TemporaryServiceCollection.Instance.ServiceLocator.Resolve<MediaFileIndex>());
      builder.Services.AddSingleton(_ => TemporaryServiceCollection.Instance.ServiceLocator.Resolve<SentenceKanjiListViewModel>());
      builder.Services.AddSingleton(_ => TemporaryServiceCollection.Instance.ServiceLocator.Resolve<Settings>());
      builder.Services.AddSingleton(_ => TemporaryServiceCollection.Instance.ServiceLocator.Resolve<JapaneseConfig>());

      builder.Services.AddCors(options =>
         options.AddDefaultPolicy(policy =>
            policy.AllowAnyOrigin()
                  .AllowAnyHeader()
                  .AllowAnyMethod()));

      _app = builder.Build();

      _app.UseCors();
      _app.UseStaticFiles();
      _app.UseAntiforgery();

      // UseAntiforgery() adds 'frame-ancestors: self' which blocks cross-origin iframes.
      // Override it so Anki's reviewer webview (on a different port) can frame our pages.
      _app.Use(async (context, next) =>
      {
         context.Response.OnStarting(() =>
         {
            context.Response.Headers["Content-Security-Policy"] = "frame-ancestors *";
            return Task.CompletedTask;
         });
         await next();
      });

      _app.MapRazorComponents<Components.App>()
          .AddInteractiveServerRenderMode();

      // Serve media files from the storage directory by MediaFileId (GUID).
      // URL: /media/{guid}
      _app.MapGet("/media/{id}", (string id, MediaFileIndex index) =>
      {
         var mediaId = MediaFileId.Parse(id);
         var attachment = index.TryGetAttachment(mediaId)
                       ?? throw new InvalidOperationException($"No media attachment found for ID {id}");

         var contentType = Path.GetExtension(attachment.FilePath).ToLowerInvariant() switch
         {
            ".mp3" => "audio/mpeg",
            ".ogg" => "audio/ogg",
            ".wav" => "audio/wav",
            ".m4a" => "audio/mp4",
            ".jpg" or ".jpeg" => "image/jpeg",
            ".png" => "image/png",
            ".gif" => "image/gif",
            ".webp" => "image/webp",
            ".svg" => "image/svg+xml",
            _ => "application/octet-stream"
         };

         return Results.File(attachment.FilePath, contentType, enableRangeProcessing: true);
      });

      // API endpoint for opening a note card in the system browser.
      // Called by NoteLink when clicked during review mode (avoids navigating away from the reviewed card).
      _app.MapGet("/api/open-in-browser/{noteType}/{noteId}", (string noteType, string noteId) =>
      {
         var url = $"{BaseUrl}/card/{noteType}/back?NoteId={noteId}";
         System.Diagnostics.Process.Start(new System.Diagnostics.ProcessStartInfo(url) { UseShellExecute = true });
         return Results.Ok();
      });

      _app.RunAsync();

      // Resolve the actual port assigned by the OS
      var address = _app.Urls.First();
      Port = new Uri(address).Port;
      CardServerUrl.BaseUrl = BaseUrl;
      SavePort(Port);
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

   static string PortFilePath => Path.Combine(
      Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData),
      "JAStudio",
      "cardserver-port.txt");

   /// <summary>
   /// Returns the previously saved port, or 0 (let OS pick) if none saved or the saved port is unavailable.
   /// </summary>
   static int LoadSavedPort()
   {
      try
      {
         if(!File.Exists(PortFilePath)) return 0;
         var text = File.ReadAllText(PortFilePath).Trim();
         return int.TryParse(text, out var port) && port > 0 ? port : 0;
      }
      catch
      {
         return 0;
      }
   }

   static void SavePort(int port)
   {
      try
      {
         var dir = Path.GetDirectoryName(PortFilePath)!;
         Directory.CreateDirectory(dir);
         File.WriteAllText(PortFilePath, port.ToString());
      }
      catch(Exception ex)
      {
         Console.WriteLine($"[CardServer] Failed to save port: {ex.Message}");
      }
   }
}
