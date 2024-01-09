import colorama
colorama.init(autoreset=True, convert=True)     # To be used to debug

__all__: list[str] = ["DebugLogs"]

class DebugLogs:
    """Light class that contains set DebugLogs"""
    
    @staticmethod
    def verbose(
        msg: str,
        bold: bool = True, 
        back: colorama.Back = None,
        msg_clr: colorama.Fore = colorama.Fore.LIGHTBLACK_EX, 
        caption_clr: colorama.Fore = colorama.Fore.LIGHTBLUE_EX,
    ):
        return (
            f"{colorama.Style.BRIGHT if bold else colorama.Style.NORMAL}{caption_clr}"
            f"[Verbose]: {back if back is not None else ' '}"
            f"{msg_clr}{msg}"
        )
           
    @staticmethod
    def info(
        msg: str,
        bold: bool = True, 
        back: colorama.Back = None,
        msg_clr: colorama.Fore = colorama.Fore.WHITE, 
        caption_clr: colorama.Fore = colorama.Fore.LIGHTGREEN_EX,
    ):
        return (
            f"{colorama.Style.BRIGHT if bold else colorama.Style.NORMAL}{caption_clr}"
            f"[Info]: {back if back is not None else ' '}"
            f"{msg_clr}{msg}"
        )
        
    @staticmethod
    def warning(
        msg: str,
        bold: bool = True, 
        back: colorama.Back = None,
        msg_clr: colorama.Fore = colorama.Fore.RESET, 
        caption_clr: colorama.Fore = colorama.Fore.LIGHTYELLOW_EX,
    ):
        return (
            f"{colorama.Style.BRIGHT if bold else colorama.Style.NORMAL}{caption_clr}"
            f"[Warning]: {back if back is not None else ' '}"
            f"{msg_clr}{msg}"
        )
        
    @staticmethod
    def error(
        msg: str,
        bold: bool = True, 
        back: colorama.Back = None,
        msg_clr: colorama.Fore = colorama.Fore.LIGHTWHITE_EX, 
        caption_clr: colorama.Fore = colorama.Fore.LIGHTRED_EX,
    ):
        return (
            f"{colorama.Style.BRIGHT if bold else colorama.Style.NORMAL}{caption_clr}"
            f"[Error]: {back if back is not None else ' '}"
            f"{msg_clr}{msg}"
        )
        
if __name__ == "__main__":
    print(DebugLogs.info("Esto es un texto de prueba. Nivel: info"))
    print(DebugLogs.verbose("Esto es un texto de prueba. Nivel: verbose"))
    print(DebugLogs.warning("Esto es un texto de prueba. Nivel: warning"))
    print(DebugLogs.error("Esto es un texto de prueba. Nivel: error"))