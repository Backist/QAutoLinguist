import click
import consts
import exceptions
from pathlib import Path
from qal import QAutoLinguist
from config import Config



config_path = ""
inst        = Config("<complete>", ["<complete>"]) 
#? creamos una instancia con los valores vacíos para que sean rellenados por el usuario.
#? Para el momento de leer el archivo debería haber escrito los valores requeridos



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


@build.command()
@click.argument(
    'filename', 
    required=False, 
    default=consts.CONFIG_FILENAME, 
    type=click.STRING
)
def init(filename):
    """
    Crea binarios con archivos de traducción.
    """
    _path = consts.CMD_CWD / filename
    config_path = inst.create(_path)            # anadimos la ruta a la variable global
    click.secho(f'Archivo de configuracion creado correctamente en  {config_path}',fg="green")
    click.secho(f'Encárguese de editar los campos requeridos y luego ejecute "qautolinguist build run [<config_path>]"',fg="green")


@build.command()
@click.argument(
    'file_path', 
    required=False, 
    type=click.Path(exists=True, dir_okay=False, readable=True, resolve_path=True)
)
def run(file_path):
    """
    Crea binarios con archivos de traducción.
    """
    if not file_path:
        file_path = consts.CMD_CWD / consts.CONFIG_FILENAME
    if not consts.CMD_CWD.joinpath(file_path.name).exists():
        while not file_path.exists():
            click.secho("No se encontró ningún archivo de configuracion en el directorio actual.", fg="yellow")
            file_path = click.prompt("Indica la ruta del archivo (Crtl+C to cancel)", confirmation_prompt=True, type=click.STRING)
            file_path = Path(file_path)
    
    content = inst.load_config(file_path)
    
    try:
        QAutoLinguist(**content).build()
    except exceptions.QALBaseException as e:
        raise e
    
    
if __name__ == '__main__':
    qautolinguist()
