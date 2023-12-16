import shutil
import os
from contextlib import contextmanager


def echo(smt):
    print(smt)
    
    
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


