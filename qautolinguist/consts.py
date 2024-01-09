from pathlib import Path 
#from dataclasses import dataclass


#--  Common paths --
CMD_CWD         = Path().resolve()
RUNTIME_ROOT  = Path(__file__).parent.resolve()

#-- Config shared consts and paths --
CONFIG_FILENAME = ".qal-config.ini" 
PARAM_DECLS_PATH = RUNTIME_ROOT / "config_decls.json"


VALID_PYLUPDATE_OPTIONS = [
    "-idbased",
    "-compress",   
    "-nounfinished",
    "-removeidentical",
    "-markuntranslated"
    "-project",
    "-silent",
    "-version",
]
VALID_PYLRELEASE_OPTIONS = [
    ""
]



     