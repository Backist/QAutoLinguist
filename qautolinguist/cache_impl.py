from pathlib import Path
from json import dumps, load
from qautolinguist.consts import CMD_CWD
from qautolinguist.debugstyles import DebugLogs
from typing import Dict, Any, Optional


class CacheImpl:
    """
    Simple light-weight cache implementation to save, access and track data.
    
    Usage:

    ``This implementation only works when working with dicts/mappings.``
    
    There will be created two files: 
        - ``nodes``: That essentially contains a dict with data.
        - ``external``: That contain the configuration parameters
        
    Data is expected to be a dict containing semantic key-values.
    External/Config must contain configuration parameters or useful information to process the data.
    """
    
    def __init__(
        self,
        data: Dict,
        external: Dict,
        *,
        cwd_dir: Path = CMD_CWD,
        folder_name: str = ".qal_cache",
        private_folder: bool = False,
    ) -> None:
        
        self._data = data
        self.external = external
        self.cwd_dir = cwd_dir
        self.folder_name = folder_name
        self.private_folder = private_folder
        
        self.cache_path = self.cwd_dir / folder_name
    
    @property
    def data(self):
        return self._data
   
    @property
    def root(self):
        return self.cache_path.resolve()
    
    def build_cache(self):
        "Call this method to build the cache."
        self._init_folder()
        self._add_data()
        self._add_externals()
        return self
        
    def _init_folder(self):
        mode= 555 if self.private_folder else 755

        try:
            self.cache_path.mkdir(mode=mode, parents=True, exist_ok=True)
        except OSError as e:
            raise OSError(f"Unexpected error while creating cache folder: {e}") from None
    
    def _add_data(self):
        with open(self.cache_path / "nodes", mode="w", encoding="utf-8") as fp:
            fp.write(self._process_data(self._data))      
        
    def _add_externals(self):
        with open(self.cache_path / "external", mode="w", encoding="utf-8") as fp:
            fp.write(self._process_data(self.external))
    
    @staticmethod
    def _process_data(data: Any):
        "Dumps either an indented dict or raw str depending if data is a dict or not."
        return dumps(data, indent=4) if isinstance(data, Dict) else str(data)
    
    @staticmethod
    def get_data(cwd_dir: Path = CMD_CWD, cache_folder: Optional[str] = None):
        "Search for `cache_folder` in `cwd_dir`. If `cache_folder` is not specified, will search `.qal_cache` folder."
        
        if not cache_folder:
            cache_folder = ".qal_cache"
            
        cache_path = cwd_dir / cache_folder
        
        if not cache_path.exists():
            raise OSError(f"Unable to found cache folder in root -> {cwd_dir!r}.")
        
        nodes = cache_path / "nodes"
        externals = cache_path / "external"
        
        if not nodes.exists():
            raise OSError(f"data file was not found in folder cache contained in root -> {cwd_dir!r}.")
        if not externals.exists():
            raise OSError(f"config/externals file was not found in folder cache contained in root -> {cwd_dir!r}.")
        
        data = {}
        
        with open(nodes, mode="r", encoding="utf-8") as nodes, \
            open(externals, mode="r", encoding="utf-8") as externals: 
            data["nodes"] = load(nodes)
            data["external"] = load(externals) 
        
        return data
