using System.Net.Http;
using System.Threading.Tasks;
using Xunit;

namespace JAStudio.Web.Specifications;

public class CardServerTests : IAsyncLifetime
{
   readonly CardServer _server = new();
   readonly HttpClient _http = new();

   public ValueTask InitializeAsync()
   {
      _server.Start();
      return ValueTask.CompletedTask;
   }

   public async ValueTask DisposeAsync()
   {
      _http.Dispose();
      await _server.StopAsync();
   }

   [Fact]
   public async Task Server_starts_and_serves_home_page()
   {
      Assert.True(_server.Port > 0, "Server should bind to a port");

      var response = await _http.GetAsync($"{_server.BaseUrl}/");
      response.EnsureSuccessStatusCode();

      var html = await response.Content.ReadAsStringAsync();
      Assert.Contains("JAStudio", html);
   }

   [Fact]
   public async Task Card_endpoint_returns_html_with_route_parameters()
   {
      var response = await _http.GetAsync($"{_server.BaseUrl}/card/sentence/back?NoteId=12345");
      response.EnsureSuccessStatusCode();

      var html = await response.Content.ReadAsStringAsync();
      Assert.Contains("sentence", html);
   }

   [Fact]
   public async Task Blazor_web_js_is_served()
   {
      var response = await _http.GetAsync($"{_server.BaseUrl}/_framework/blazor.web.js");
      response.EnsureSuccessStatusCode();

      var content = await response.Content.ReadAsStringAsync();
      Assert.True(content.Length > 1000, "blazor.web.js should be a substantial script file");
   }
}
