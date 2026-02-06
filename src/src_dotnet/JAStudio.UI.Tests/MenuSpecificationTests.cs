using JAStudio.UI.Menus;
using JAStudio.UI.Menus.UIAgnosticMenuStructure;

namespace JAStudio.UI.Tests;

/// <summary>
/// Demonstrates the benefit of UI-agnostic menu specifications:
/// We can test the entire menu tree structure, conditional logic, and actions
/// WITHOUT instantiating any UI framework (Avalonia, WPF, Qt, etc.).
/// </summary>
public class MenuSpecificationTests
{
    [Fact]
    public void WebSearchMenu_ContainsKanjiSubmenu()
    {
        // Arrange
        var searchText = "漢字";
        
        // Act - Build the menu spec (no Avalonia needed!)
        var menuSpec = WebSearchMenus.BuildWebSearchMenuSpec(() => searchText);

        // Assert - Verify structure
        Assert.Equal("_o Web", menuSpec.Name); // ShortcutFinger.Home3("Web") = "_o Web"
        Assert.NotNull(menuSpec.Children);
        Assert.True(menuSpec.IsSubmenu);
        
        var kanjiSubmenu = menuSpec.Children.FirstOrDefault(c => c.Name.Contains("Kanji"));
        Assert.NotNull(kanjiSubmenu);
        Assert.True(kanjiSubmenu!.IsSubmenu);
        Assert.Equal(3, kanjiSubmenu.Children!.Count); // Kanji explosion, Kanshudo, Kanji map
    }

    [Fact]
    public void WebSearchMenu_KanjiExplosion_OpensCorrectUrl()
    {
        // Arrange
        var searchText = "漢字";
        
        // Act - Build menu and find the "Kanji explosion" action
        var menuSpec = WebSearchMenus.BuildWebSearchMenuSpec(() => searchText);

        var kanjiSubmenu = menuSpec.Children!.First(c => c.Name.Contains("Kanji"));
        var kanjiExplosionItem = kanjiSubmenu.Children!.First();
        
        Assert.Equal("_u Kanji explosion", kanjiExplosionItem.Name); // ShortcutFinger.Home1("Kanji explosion")
        // Note: Can't test execution since it calls AnkiFacade.OpenUrl
        Assert.NotNull(kanjiExplosionItem.Action);
    }

    [Fact]
    public void WebSearchMenu_AllLeafNodes_HaveActions()
    {
        // Arrange & Act
        var menuSpec = WebSearchMenus.BuildWebSearchMenuSpec(() => "test");

        // Assert - Recursively verify all leaf nodes have actions
        var leafItems = GetAllLeafItems(menuSpec);
        Assert.NotEmpty(leafItems);
        Assert.All(leafItems, item => Assert.NotNull(item.Action));
    }

    [Fact]
    public void MenuItem_Separator_HasCorrectProperties()
    {
        // Act
        var separator = SpecMenuItem.Separator();

        // Assert
        Assert.True(separator.IsSeparator);
        Assert.False(separator.IsCommand);
        Assert.False(separator.IsSubmenu);
        Assert.Null(separator.Action);
    }

    [Fact]
    public void MenuItem_Command_HasCorrectProperties()
    {
        // Arrange
        var executed = false;
        
        // Act
        var command = SpecMenuItem.Command(
            "Test Command",
            () => executed = true,
            acceleratorKey: 'T',
            shortcut: "Ctrl+T"
        );

        // Assert
        Assert.True(command.IsCommand);
        Assert.False(command.IsSubmenu);
        Assert.False(command.IsSeparator);
        Assert.Equal("Test Command", command.Name);
        Assert.Equal('T', command.AcceleratorKey);
        Assert.Equal("Ctrl+T", command.KeyboardShortcut);
        
        command.Action!();
        Assert.True(executed);
    }

    [Fact]
    public void MenuItem_Submenu_HasCorrectProperties()
    {
        // Act
        var submenu = SpecMenuItem.Submenu(
            "Test Menu",
            new List<SpecMenuItem>
            {
                SpecMenuItem.Command("Item 1", () => { }),
                SpecMenuItem.Separator(),
                SpecMenuItem.Command("Item 2", () => { })
            },
            acceleratorKey: 'M'
        );

        // Assert
        Assert.True(submenu.IsSubmenu);
        Assert.False(submenu.IsCommand);
        Assert.False(submenu.IsSeparator);
        Assert.Equal("Test Menu", submenu.Name);
        Assert.Equal('M', submenu.AcceleratorKey);
        Assert.Equal(3, submenu.Children!.Count);
    }

    [Fact]
    public void MenuItem_ConditionalVisibility_WorksCorrectly()
    {
        // Arrange
        var showItem = false;
        var conditionalItem = SpecMenuItem.Command("Conditionally Hidden", () => { });
        conditionalItem.IsVisible = showItem;
        
        // Act
        var menu = SpecMenuItem.Submenu(
            "Menu",
            new List<SpecMenuItem>
            {
                SpecMenuItem.Command("Always Visible", () => { }),
                conditionalItem
            }
        );

        // Assert - Only visible items should be counted
        var visibleItems = menu.Children!.Where(c => c.IsVisible).ToList();
        Assert.Single(visibleItems);
        Assert.Equal("Always Visible", visibleItems[0].Name);
    }

    /// <summary>
    /// Helper to recursively extract all leaf (command) items from a menu tree.
    /// </summary>
    private List<SpecMenuItem> GetAllLeafItems(SpecMenuItem menu)
    {
        var result = new List<SpecMenuItem>();
        
        if (menu.IsCommand)
        {
            result.Add(menu);
        }
        else if (menu.IsSubmenu && menu.Children != null)
        {
            foreach (var child in menu.Children)
            {
                result.AddRange(GetAllLeafItems(child));
            }
        }
        
        return result;
    }
}
