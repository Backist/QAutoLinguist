"Flavored pathlib.Path subclass that implements some helpful methods to work with Paths."

import os
import pathlib
import exceptions as exceptions
from debugstyles import DebugLogs
from typing import Union


IS_POSIX = os.name != "nt"


class Path(pathlib.Path):
    "Flavored shadow ``pathlib.Path`` subclass that implements some helpful methods to work with Paths."
    
    _flavour = pathlib._posix_flavour if IS_POSIX else pathlib._windows_flavour
    #pathlib.Path expects to have been invoked via either WindowsPath() or PosixPath(),
    #which both provide a _flavour class attribute via multiple inheritance. 
    # It must also be provided when subclassing.
    
    def __new__(cls, *args, **kwargs):
        return super(Path, cls).__new__(cls, *args, **kwargs)
    
    def prepare(
        self,
        *,
        is_dir: bool = True,
        create_empty: bool = True, 
        mode: int = 751,
        parents: bool = True, 
        exist_ok: bool = True, 
        strict: bool = False
    ):
        "Method that pretends to initialize a path resolving it and creating an empty resource if it is not created yet."

        if is_dir:
            self._init_dir(
                loc=self, 
                create_empty=create_empty, 
                mode=mode,
                parents=parents, 
                exist_ok=exist_ok, 
                strict=strict
            )
        else:
            self._init_file(
                loc=self, 
                create_empty=create_empty, 
                mode=mode,
                exist_ok=exist_ok, 
                strict=strict
            )

        return self
        
        
    @staticmethod
    def _init_dir(
        *,
        loc: Union[str, pathlib.Path], 
        create_empty: bool = True, 
        mode: int = 751,
        parents: bool = True, 
        exist_ok: bool = True, 
        strict: bool = False
    ) -> pathlib.Path:    
        """
        Creates a ``pathlib.Path`` object and normalises it. It will also verify that the path refers to a valid directory and exists.
        If ``mkdir`` is True, it will attempt to create an empty one.
        
        Raises:
        - ``FileNotFoundError`` -> Raised when tried to resolve but path was not found (raised by ``pathlib.resolve()``)
        - ``IOFailure`` -> When the path does not exist
        - ``RequiredDirError`` -> Whether a path does not point to a directory.
        """ 
        loc = loc if isinstance(loc, Path) else Path(loc)
        
        if create_empty:
            if loc.exists():
                print(DebugLogs.warning(f"Found existing folder '{loc.name}', content inside will be overwritten."))
            
            try:
                loc.mkdir(mode=mode, parents=parents,exist_ok=exist_ok)    # mode = 0o511 -> Requires admin to delete the folder. See UNIX file permissions
            except OSError as e:
                raise exceptions.IOFailure(f"Could not be created directory: {loc}. Detailed error: {e}") from e
            
        if loc.exists() and loc.is_dir():
            return loc.resolve(strict)   # when strict=True raises FileNotFoundError
        
        raise exceptions.RequiredDirError("Expected path must point to a directory or must exist.")
    
    @staticmethod
    def _init_file(
        *,
        loc: Union[str, pathlib.Path], 
        create_empty: bool = True, 
        mode: int = 751,
        exist_ok: bool = True, 
        strict: bool = False
    ) -> pathlib.Path:
        """
        Create a ``Path`` object with ``loc``, normalize it and try to create an empty file if ``mkfile=True``\n
        NOTE: ``Path object can be passed to loc, but unless you want to create an empty file, this funcion will be useless,
        since it will return the resolved Path only``\n
        The aim of that function is to transform loc to Path object, caching exceptions, and also allowing to initialize it by 
        creating the file
        
        Raises:
        - ``FileNotFoundError`` -> Raised when tried to resolve but path was not found (raised by ``pathlib.resolve()``)
        - ``IOFailure`` -> When the path does not exist
        - ``RequiredFileError`` -> Whether a path does not point to a file.
        """
        loc = loc if isinstance(loc, Path) else Path(loc)
        
        if create_empty:
            if loc.exists():
                print(DebugLogs.warning(f"Found existing file '{loc.name}', content inside will be overwritten."))
                
            try:
                loc.touch(mode=mode, exist_ok=exist_ok)   # INFO mode = 0o511 -> Requires admin to delete the folder. See UNIX file permissions
            except OSError as e:
                raise exceptions.IOFailure(f"Could not be created file: {loc}. Detailed error: {e}") from e

            return loc.resolve(strict)   
        
        if loc.exists() and loc.is_file():
            return loc.resolve(strict)      # when strict=True raises FileNotFoundError
        
        raise exceptions.RequiredFileError("Expected path must point to a file or must exist.")
    
