import rtoml
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional, Iterable

__all__: list[str] = ["Config"]

@dataclass
class Config:           
    source_file:            str                   # .ui | .py file to search for "tr" funcs
    available_locales:      List[str]         # locales to make a translation file for each one, MUST BE <xx_XX> type locale    
    default_locale:         str = "en_EN"         # reference locale, took as a reference to make other translations
    translations_folder:    Optional[str] = None  # folder to save translations. IF NONE, CREATE A NEW DIR IN CWD>
    auto_translate:         bool = True           # Requires internet.
    make_cache:             bool = False
    debug_mode:             bool = False          # Enabled debug logging
    verbose:                bool = False          # Verbose all called private methods
    BUILD_DONE:             bool = False
    
    
    def _process_dict(self):
        return {"Meta": self.__dict__}
        
    def make_config_file(self):
        rtoml.dump(obj=self._process_dict(), file=Path(self.CONFIG_PATH), pretty=True)
    
    
        

    
    