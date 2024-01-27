"Light-Weight class containing default log levels to display nice debugs and echos."

from click import style
from typing import Union, Optional, Union, Tuple, Any

__all__: list[str] = ["DebugLogs"]

class DebugLogs:
    """Light class that contains default log levels through a nice colored and styled output.
    
    If the terminal supports it, log colors may also be specified as:

    An integer in the interval [0, 255]. The terminal must support 8-bit/256-color mode.
    An RGB tuple of three integers in [0, 255]. The terminal must support 24-bit/true-color mode.
    """
    
     
    @staticmethod
    def info(
        msg: Any,
        caption_clr: Optional[Union[int, str, Tuple[int, int, int]]] = "white",
        fg: Optional[Union[int, str, Tuple[int, int, int]]] = "bright_green",
        bg: Optional[Union[int, str, Tuple[int, int, int]]] = None,
        bold: Optional[bool] = True,
        dim: Optional[bool] = False,
        underline: Optional[bool] = True,
        overline: Optional[bool] = False,
        italic: Optional[bool] = None,
        blink: Optional[bool] = True,
        reverse: Optional[bool] = None,
        strikethrough: Optional[bool] = None,
        reset: Optional[bool] = True
    ) -> str:
        msg = style(
            text=msg, 
            fg=fg, 
            bg=bg,
            bold=bold,
            dim=dim,
            underline=underline,
            overline=overline,
            italic=italic,
            blink=blink,
            reverse=reverse,
            strikethrough=strikethrough,
            reset=reset
        )
        caption = style("[INFO]:: ", fg=caption_clr, bold=True)
        
        return caption + msg
    

    @staticmethod
    def warning(
        msg: Any,
        caption_clr: Optional[Union[int, str, Tuple[int, int, int]]] = "bright_yellow",
        fg: Optional[Union[int, str, Tuple[int, int, int]]] = "yellow",
        bg: Optional[Union[int, str, Tuple[int, int, int]]] = None,
        bold: Optional[bool] = False,
        dim: Optional[bool] = False,
        underline: Optional[bool] = True,
        overline: Optional[bool] = True,
        italic: Optional[bool] = None,
        blink: Optional[bool] = True,
        reverse: Optional[bool] = None,
        strikethrough: Optional[bool] = None,
        reset: Optional[bool] = True
    ) -> str:
        msg = style(
            text=msg, 
            fg=fg, 
            bg=bg,
            bold=bold,
            dim=dim,
            underline=underline,
            overline=overline,
            italic=italic,
            blink=blink,
            reverse=reverse,
            strikethrough=strikethrough,
            reset=reset
        )
        caption = style("[WARNING]:: ", fg=caption_clr, bold=True)
        
        return caption + msg
    

    @staticmethod
    def verbose(
        msg: Any,
        caption_clr: Optional[Union[int, str, Tuple[int, int, int]]] = "bright_blue",
        fg: Optional[Union[int, str, Tuple[int, int, int]]] = "bright_black",
        bg: Optional[Union[int, str, Tuple[int, int, int]]] = None,
        bold: Optional[bool] = True,
        dim: Optional[bool] = False,
        underline: Optional[bool] = False,
        overline: Optional[bool] = False,
        italic: Optional[bool] = True,
        blink: Optional[bool] = True,
        reverse: Optional[bool] = None,
        strikethrough: Optional[bool] = None,
        reset: Optional[bool] = True
    ) -> str:
        msg = style(
            text=msg, 
            fg=fg, 
            bg=bg,
            bold=bold,
            dim=dim,
            underline=underline,
            overline=overline,
            italic=italic,
            blink=blink,
            reverse=reverse,
            strikethrough=strikethrough,
            reset=reset
        )
        caption = style("[VERBOSE]:: ", fg=caption_clr, bold=True)
        
        return caption + msg
    

    @staticmethod
    def error(
        msg: Any,
        caption_clr: Optional[Union[int, str, Tuple[int, int, int]]] = "bright_red",
        fg: Optional[Union[int, str, Tuple[int, int, int]]] = "bright_white",
        bg: Optional[Union[int, str, Tuple[int, int, int]]] = None,
        bold: Optional[bool] = True,
        dim: Optional[bool] = False,
        underline: Optional[bool] = True,
        overline: Optional[bool] = False,
        italic: Optional[bool] = None,
        blink: Optional[bool] = True,
        reverse: Optional[bool] = None,
        strikethrough: Optional[bool] = None,
        reset: Optional[bool] = True
    ) -> str:
        msg = style(
            text=msg, 
            fg=fg, 
            bg=bg,
            bold=bold,
            dim=dim,
            underline=underline,
            overline=overline,
            italic=italic,
            blink=blink,
            reverse=reverse,
            strikethrough=strikethrough,
            reset=reset
        )
        caption = style("[ERROR]:: ", fg=caption_clr, bold=True)
        
        return caption + msg
    

        
if __name__ == "__main__":
    print(DebugLogs.info("Esto es un texto de prueba."))
    print(DebugLogs.verbose("Esto es un texto de prueba"))
    print(DebugLogs.warning("Esto es un texto de prueba."))
    print(DebugLogs.error("Esto es un texto de prueba."))