using System;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Web;
using Microsoft.AspNetCore.WebUtilities;
using Microsoft.JSInterop;
using MudBlazor;

namespace JAStudio.Web.Components.Layout;

public partial class MainLayout : IAsyncDisposable
{
   [Inject] public IJSRuntime JS { get; set; } = null!;

   bool _drawerOpen;
   bool _shellVisible;
   bool _isInIframe;
   DotNetObjectReference<MainLayout>? _dotNetRef;

   readonly MudTheme _theme = new()
   {
      PaletteLight = new PaletteLight
      {
         Primary = "#1d4ed8",
         AppbarBackground = "#1e293b"
      },
      PaletteDark = new PaletteDark
      {
         Primary = "#60a5fa",
         AppbarBackground = "#1e293b",
         Surface = "#1e1e2e",
         Background = "#11111b",
         DrawerBackground = "#1e1e2e"
      }
   };

   protected override void OnParametersSet()
   {
      var uri = new Uri(Navigation.Uri);
      var query = QueryHelpers.ParseQuery(uri.Query);
      _isInIframe = query.ContainsKey("DisplayContext");

      // In browser: shell visible by default. In Anki iframe: hidden.
      _shellVisible = !_isInIframe;
   }

   protected override async Task OnAfterRenderAsync(bool firstRender)
   {
      if(firstRender)
      {
         _dotNetRef = DotNetObjectReference.Create(this);
         await JS.InvokeVoidAsync("jaStudioShell.registerToggle", _dotNetRef);
      }
   }

   [JSInvokable]
   public void ToggleShellFromJs()
   {
      _shellVisible = !_shellVisible;
      StateHasChanged();
   }

   void ToggleDrawer() => _drawerOpen = !_drawerOpen;
   void HideShell() => _shellVisible = false;

   public async ValueTask DisposeAsync()
   {
      if(_dotNetRef != null)
      {
         await JS.InvokeVoidAsync("jaStudioShell.unregisterToggle");
         _dotNetRef.Dispose();
      }
   }
}
