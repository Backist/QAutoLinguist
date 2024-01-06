from pathlib import Path 
#from dataclasses import dataclass


#--  Common paths --
CMD_CWD         = Path().resolve()
RUNTIME_FOLDER  = Path(__file__).parent.resolve()

#-- Config shared consts and paths --
CONFIG_FILENAME = ".qal-config.ini" 
PARAM_DECLS = RUNTIME_FOLDER / "param_decls.json"


VALID_PYLUPDATE_OPTIONS = [
    "-idbased",
    "-compress",   
    "-nounfinished",
    "-removeidentical",
    "-markuntranslated <prefix>"
    "-project <filename>",
    "-silent",
    "-version",
]
VALID_PYLRELEASE_OPTIONS = [
    ""
]



     