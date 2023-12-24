import shutil
import os
from typing import Optional
from contextlib import contextmanager



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
    if not string:
        return string
    if preffix:
        parts = [
            f"{preffix}{' ' * sep_padding}{string[i:i+split_size]}" 
            for i in range(0, len(string), split_size)
        ]
    else:
        parts = [string[i:i+split_size] for i in range(0, len(string), split_size)]
    if as_multistring:
        return newline_sep.join(parts)
    return parts if not as_generator else iter(parts)


# [DEPRECATED] => Useless since rtoml does not allow multi-line list definitions.
# def fit_iterable(l: list | tuple):
#     """Returns a list formated as a multiline list.
#     Example:
#     >>> l = [1,2,3,4]
#     >>> print(str(l)) #output: "[1,2,3,4]"
    
#     >>> print(fit_list(l)) 
#     >>> [
#         1,
#         2,
#         3,
#         4
#     ]
#     """
#     s= """[\n{}\n]""" if isinstance(l, list) else """(\n{}\n)"""
#     return s.format(",\n".join(l))

def stringfy(obj):
    if isinstance(obj, bool):
        return str(obj).lower()     # make booleans lowercase to be recognizable to config file using getboolean()
    if isinstance(obj, type(None)):
        return ""                   # Represent None as empty string
    return str(obj)

 
@contextmanager
def safe_open(file_path, return_both=False):
    """
    Usage:
        with safe_open(_file) as file_path:
            # Solo obtén la ruta de file_path
            # En caso de excepción, el contenido original será restaurado

        with safe_open(_file, return_both=True) as (file_path, temp_file_path):
            # Obtén ambas rutas: file_path y temp_file_path
            # En caso de excepción, el contenido original será restaurado
    """
    temp_file_path = make_temp_copy(file_path)
    try:
        if return_both:
            yield file_path, temp_file_path
        else:
            yield file_path
    except Exception as e:
        # En caso de excepción, restaura el contenido original
        shutil.copyfile(temp_file_path, file_path)
        raise e
    finally:
        # En cualquier caso, elimina el archivo temporal
        os.remove(temp_file_path)

# Fuera del bloque with, el archivo temporal ya se habrá eliminado o el contenido original se habrá restaurado.

def make_temp_copy(_file):
    temp_file_path = _file.with_name(f"{_file.stem}.temp")
    shutil.copyfile(_file, temp_file_path)
    return temp_file_path


