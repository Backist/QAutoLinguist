import shutil
import os
from typing import Optional, Union
from pathlib import Path
from contextlib import contextmanager
from qautolinguist.exceptions import IOFailure, RequiredDirError, RequiredFileError


def fit_string(
    string: str, 
    split_size:  int           = 50, 
    *,    
    newline_sep: str           = "\n",
    preffix: str               = None,     
    as_generator: bool         = False,
    as_multistring: bool       = True, 
    sep_padding: Optional[int] = 1
):
    """Devuelve una lista o una string dividida en partes de n caracteres.
    Si ``prefix`` no es None, se añade el prefijo delante de cada parte.\n
    Si ``as_multistring`` es True, se devuelve un string con las partes en cada linea.
    Si ``preffix`` es True y ``sep_padding`` también, se separa las partes de los preffix ``sep_padding`` espacios en blanco
    ``newline_sep`` representa el separador usado para crear saltos de linea. 
    Es posible que necesites esto para hacer textos multilinea mas legibles en formatos TOML o JSON.
    """
    if not string or split_size >= len(string):
        return string if preffix is None else f"{preffix}{' ' * sep_padding}{string}"
    
    parts = [
        f"{preffix}{' ' * sep_padding}{string[i:i+split_size]}" 
        for i in range(0, len(string), split_size)
    ] if preffix is not None else [
        string[i:i+split_size] 
        for i in range(0, len(string), split_size)
    ]
    
    if as_multistring:
        return newline_sep.join(parts)
    return iter(parts) if as_generator else parts


def stringfy(obj):
    if isinstance(obj, bool):
        return str(obj).lower()     # make booleans lowercase to be recognizable to config file using configparser.getboolean()
    return "" if isinstance(obj, type(None)) else str(obj)

def make_temp_copy(file_: Union[str, Path]):
    "Makes a temporally file with the content of ``file_`` and return temp file path"
    file_ = file_ if isinstance(file_, Path) else Path(file_)
    temp_file_path = file_.with_name(f"{file_.stem}.temp")
    shutil.copy(file_, temp_file_path)
    return temp_file_path

def remove_temp_copy(temp: Union[str, Path], file_: Union[str, Path]):
    "Copy the content of ``temp`` to ``file_`` and return ``file_`` path"
    file_ = file_ if isinstance(file_, Path) else Path(file_)
    shutil.copyfile(temp, file_)   
    os.remove(temp)
    return file_

@contextmanager
def safe_open(file_path: Union[str, Path], both_paths=False, **kwargs):
    """
    @param kwargs can be any parameter that you can pass to ``builtins.open()`` function.
    
    Usage:
        with safe_open(_file) as file_path:
            # Solo obtén la ruta de file_path
            # En caso de excepción, el contenido original será restaurado

        with safe_open(_file, return_both=True) as (file_path, temp_file_path):
            # Obtén ambas rutas: file_path y temp_file_path
            # En caso de excepción, el contenido original será restaurado
    """
    file_path = file_path if isinstance(file_path, Path) else Path(file_path)
    temp_file_path = make_temp_copy(file_path)
    original_io   = open(file_path, **kwargs)
    temp_io       = open(temp_file_path, **kwargs)
    
    try:
        if both_paths:
            yield original_io, temp_io
        else:
            yield original_io
    except Exception as e:
        remove_temp_copy(temp_file_path, file_path) # restaura el contenido de temp a file y borra temp
        raise e
    finally:
        original_io.close()
        if temp_file_path:
            temp_io.close()
        os.remove(temp_file_path)         # En cualquier caso, elimina el archivo temporal
        

def process_loc(loc: Path, dir_okay: bool = False):
    "Comprueba que el path existe y es un directorio o archivo valido"
    loc = loc.resolve() if isinstance(loc,Path) else Path(loc).resolve()
    if not loc.exists():
        raise IOFailure("This path does not exist in your machine. Please, pass a valid path.")
    if dir_okay and not loc.is_dir():
        raise RequiredDirError("This path does not point to a directory.")
    if not dir_okay and loc.is_dir():
        raise RequiredFileError("This path does not point to a file.")
