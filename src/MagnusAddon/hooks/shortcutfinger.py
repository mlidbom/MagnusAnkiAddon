from collections.abc import Callable

def _format_finger(finger: str, text:str) -> str: return f"""&{finger} {text}"""

def home1(text: str) -> str: return _format_finger("u", text)
def home2(text: str) -> str: return _format_finger("e", text)
def home3(text: str) -> str: return _format_finger("o", text)
def home4(text: str) -> str: return _format_finger("a", text)
def home5(text: str) -> str: return _format_finger("i", text)
def home6(text: str) -> str: return _format_finger("d", text)

def up1(text: str) -> str: return _format_finger("p", text)
def up2(text: str) -> str: return _format_finger("ö", text)
def up3(text: str) -> str: return _format_finger("ä", text)
def up4(text: str) -> str: return _format_finger("å", text)
def up5(text: str) -> str: return _format_finger("y", text)
def up6(text: str) -> str: return _format_finger("f", text)

def down1(text: str) -> str: return _format_finger("k", text)
def down2(text: str) -> str: return _format_finger("j", text)
def down3(text: str) -> str: return _format_finger("q", text)
#def down4(text: str) -> str: return _format_finger(".", text)
def down5(text: str) -> str: return _format_finger("x", text)
def down6(text: str) -> str: return _format_finger("b", text)

def none(text:str) -> str: return text

_index_functions: list[Callable[[str], str]] = [home1, home2, home3, home4, up1, up2, up3, up4, down1, down2, down3, home6, up6, down6]
def index(index:int, text:str) -> str:
    if index < len(_index_functions): return _index_functions[index](text)
    return none(text)