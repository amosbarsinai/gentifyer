from rich.console import Console, Group
from rich.align   import          Align
from rich.panel   import          Panel
from rich.text    import           Text
from getkey       import   getkey, keys

class ScreenException(Exception):
    """Raised when the screen cannot be displayed for some reason."""
    pass

class ScreenComponent:
    pass

class TextBlock(ScreenComponent):
    def __init__(self, s: str):
        self.content: str = s

class Menu(ScreenComponent):
    def __init__(self, id: str, title: str, options: list, allow_empty: bool = None):
        self.id:          str                   =          id
        self.title:       str                   =       title
        self.options:     list[Menu.MenuOption] =     options
        self.hovered:     int                   =        None
        self.selected:    list[bool]            =        None
        self.allow_empty: bool                  = allow_empty # if allow_empty is false you can continue only if nothing is selectable

        # Find the first selectable menu option
        i = 0
        while not options[i].selectable:
            i += 1
            if i > len(options) - 1:
                break # no selectable options
        if i != None:
            self.hovered = i
    class MenuOption:
        def __init__(self, id: str, name: str, selectable: bool, unselectable: str, immediate: bool = False):
            self.id:           str  =           id
            self.name:         str  =         name
            self.selectable:   bool =   selectable
            self.unselectable: str  = unselectable
            self.immediate:   bool  =    immediate


class Screen:
    def __init__(self, title: str, components: list[ScreenComponent]):
        self.title: str                        =      title
        self.components: list[ScreenComponent] = components
        self.menu: Menu                        =       None # cache the screen's menu so we don't have to search for it every time
        for i, component in enumerate(self.components):
            if isinstance(component, Menu):
                if self.menu:
                    raise ScreenException(f"Cannot have more than one Menu ScreenComponent per Screen, found second inside {id(self.components)} at index {i}")
                else:
                    self.menu = component

def panel_content(screen: Screen):
    content: list[Text] = list()
    for component in screen.components:
        if isinstance(component, TextBlock):
            content.append(Align.left(component.content + '\n'))
        elif isinstance(component, Menu):
            content.append(Align.center(component.title, style="bold"))
            if not sum(option.selectable for option in component.options):
                content.append(Align.center("None of the following menu's options are selectable.", style="dim"))
            for i, option in enumerate(component.options):
                style = ""
                if option.selectable:
                    if component.hovered == i:
                        style = "reverse"
                else:
                    style = "dim"
                content.append(
                    Text(
                        f"{
                            '' if component.options[i].immediate else ('(x)' if component.selected == i else '( )')
                        } {
                            option.name
                        } {
                            f"({option.unselectable})" if not option.selectable else ""
                        }",
                        style=style
                    )
                )

    panel = Panel(
        Group(*content),
        title=screen.title
    )
    return panel

def screen_loop(screen: Screen, rich_console: Console, can_recurse=True) -> dict[str, str] | None:
    running = True
    while running:
        panel = panel_content(screen)
        rich_console.clear()
        rich_console.print(panel)
        key = getkey()
        match key:
            case keys.UP:
                if screen.menu:
                    if screen.menu.hovered != None:
                        screen.menu.hovered -= 1
                        screen.menu.hovered %= len(screen.menu.options)
                        while not screen.menu.options[screen.menu.hovered].selectable:
                            screen.menu.hovered -= 1
                            screen.menu.hovered %= len(screen.menu.options)
                    else:
                        # None of the menu's options are selectable
                        pass
                else:
                    # Screen has no menu, redraw on key press anyway
                    pass
            case keys.DOWN:
                if screen.menu:
                    if screen.menu.hovered != None:
                        screen.menu.hovered += 1
                        screen.menu.hovered %= len(screen.menu.options)
                        while not screen.menu.options[screen.menu.hovered].selectable:
                            screen.menu.hovered += 1
                            screen.menu.hovered %= len(screen.menu.options)
                    else:
                        # None of the menu's options are selectable
                        pass
                else:
                    # Screen has no menu, redraw on key press anyway
                    pass
            case keys.ENTER:
                if screen.menu:
                    if screen.menu.selected == screen.menu.hovered:
                        screen.menu.selected = None
                    else:
                        screen.menu.selected = screen.menu.hovered
                        if screen.menu.options[screen.menu.selected].immediate:
                            running = False
            case keys.ESC:
                if can_recurse:
                    answer = screen_loop(
                        Screen(
                            "Confirm Exit",
                            [
                                Menu(
                                    "confirm_exit",
                                    "Are you sure you want to exit the installer? Your system may be left in an unusable state!",
                                    [
                                        Menu.MenuOption("y", "Yes, I'm sure", True, None, True),
                                        Menu.MenuOption("n", "No, go back", True, None, True)
                                    ]
                                )
                            ]
                        ), 
                        rich_console,
                        can_recurse=False
                    )
                    if answer:
                        if answer == "y":
                            running = False
            case keys.SPACE:
                if screen.menu:
                    if screen.menu.allow_empty:
                        running = False
                    elif screen.menu.allow_empty == None:
                        if screen.menu.selected != None or not any(option.selectable for option in screen.menu.options):
                            running = False
                    else:
                        pass

    if screen.menu:
        if screen.menu.selected != None:
            return screen.menu.options[screen.menu.selected].id
        else:
            return

def screen_loop_wrapper(screen: Screen):
    console = Console()
    with console.screen():
        return screen_loop(screen, console)
