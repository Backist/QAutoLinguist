import click
import consts
import exceptions

from pathlib import Path
from qal import QAutoLinguist
from config import Config
from cli.start_page import startup_page

__all__ = ["qautolinguist"]


inst = Config() 
#? creamos una instancia con los valores vacíos para que sean rellenados por el usuario.
#? Para el momento de leer el archivo debería haber escrito los valores requeridos


#& -- Command Groups --
@click.group()
def qautolinguist():
    pass


@qautolinguist.group()
def build():
    """
    Comandos relacionados con la construcción.
    """
    pass

@qautolinguist.group()
def rebuild():
    """
    Comandos relacionados con la construcción.
    """
    pass



#& -- Commands --
@build.command()
@click.argument(
    'filename', 
    required=False, 
    default=consts.CONFIG_FILENAME, 
)
def init(filename):
    """
    Crea binarios con archivos de traducción.
    """
    _path = consts.CMD_CWD / filename
    config_path = inst.create(_path)         
    click.secho(f'Archivo de configuracion creado correctamente en  {config_path}',fg="green")
    click.secho('Encárguese de editar los campos requeridos y luego ejecute "qautolinguist build run [<config_path>]"',fg="green")

@build.command()
@click.option(
    '-revised', 
    is_flag=True, 
)
@click.argument(
    'file_path', 
    required=False, 
)
def run(file_path, revised):
    """
    Crea binarios con archivos de traducción.
    """
    
    if revised:
        QAutoLinguist.compose_qm_files()  
        return
    
    if file_path:
        file_path = Path(file_path).resolve()
    else:
        file_path = consts.CMD_CWD / consts.CONFIG_FILENAME

    if not file_path.exists():
        while not file_path.exists():
            click.secho("No se encontró ningún archivo de configuracion en el directorio actual.", fg="yellow")
            file_path = click.prompt("Indica la ruta del archivo (Crtl+C to cancel)", confirmation_prompt=True, type=click.STRING)
            file_path = Path(file_path).resolve(True)
    
    content = inst.load_config(file_path)
    qal_inst = QAutoLinguist(**content)
    
    try:
        qal_inst.build()
    except exceptions.QALBaseException as e:
        raise e

 
def run_cli():
    startup_page()
    qautolinguist()