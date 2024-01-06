import configparser
import consts
import helpers
import exceptions
import json
from ast import literal_eval      # para convertir listas y otras estructuras de datos de str a su tipo original
from config_template import INI_FILE_TEMPLATE
from pathlib import Path
from typing import Dict, Optional, Union


__all__: list[str] = ["Config"]


class Config:
    """
    Class that represents a Configuration File and its attributes.
    
    This class only uses its own way to make ``.ini`` files and uses ``configparser.ConfigParser`` to read .ini files.
    """
    
    def __init__(self):  
        self._parser = configparser.ConfigParser(allow_no_value=False, empty_lines_in_values=False)
        self._data = self._format_dict_data()       # datos del diccionario con el cual se va a crear la config (valores predeterminados.)

    #& ----------------------------------- INTERNAL FUNCTIONS -------------------------------------
    def _process_dict_data(self):
        """Devuelve un diccinario  ``dict[param:(value,comment)]`` tomando ``self.__dict__`` y ``consts.PARAMS_DESCRIPTION``
        NOTE: ``Es importante que todos los atributos que quieran incluir en la config estén definidos como atributos de instancia y no empiezen por '_'
        """ 
        with open(consts.PARAM_DECLS) as fp:
            self.params = json.load(fp)  
        # -- Importamos el diccionario estatico que contiene los comentarios, es de la forma dict[param: (comment, default)] --
        # -- default es el valor por defecto que da QAutoLinguist.
        return {
            param: (
                helpers.stringfy(param_info['default']),
                helpers.fit_string(param_info['comment'], split_size=75, preffix="#"),
            )
            for param, param_info in self.params.items()
        }

    def _format_dict_data(self):
        """
        A partir del diccionario devuelto por self._process_dict_data, se reformatea el diccionario en la forma:
        Pasamos de ``dict[key: (value, comment)]`` a ``dict[key: key, key_value: value, key_comment: comment]``
        El diccionario devuelto es el que se pasa para formatear el config template, que corresponde al formato
        estático del archivo de configuracion
        """
        dict_data = self._process_dict_data()           # structure => {param: (default, comment)}
        d = {}
        for param, (default, comment) in dict_data.items():
            d[param] = param
            d[f"{param}_default"] = default
            d[f"{param}_comment"] = comment
        return d
    
    def _process_template(self):
        return INI_FILE_TEMPLATE.format(**self._data)   
    
    def _conv_value_type(self, raw, original):
        """
        This function gets a string and tries to convert into a python valid format type and tries to convert to python datatype        
        NOTE: ``This function actually converts that types specified below:``
        - ``List, Tuple, Set``
        - ``bool, str, int, float, complex``
        - [NotImplemented] ``pathlib.Path``
        """
        raw = raw.strip().lower()
        converter = None

        if not raw:     # si es una cadena vacia, devolvemos None (no vemos si su valor original es None porque no es relevante si esta vacia)
            return None
        if original is None:
            return raw or None
        if isinstance(original, str):
            return raw 

        if isinstance(original, bool):
            positive_cases = {"true", "on", "yes", "1"}
            negative_cases = {"false", "off", "no", "0"}
            if raw in positive_cases:
                return True
            if raw in negative_cases:
                return False
            else: 
                raise exceptions.ConfigWrongParamFormat(f"Failed trying to format {raw!r} into a bool type, valid boolean formats are {positive_cases} or {negative_cases}")
        if isinstance(original, int):
            converter = int     # raises ValueError on failure
        elif isinstance(original, float):
            converter = float  # raises ValueError on failure
        elif isinstance(original, (list, tuple)):
            converter = literal_eval           # para convertir listas y otras estructuras de datos de str a su tipo original
            # raises SyntaxError on failure

    
        try:
            return converter(raw) 
        except (ValueError, SyntaxError, OSError) as e:
            raise exceptions.ConfigWrongParamFormat(
                f"Cant convert {raw!r} to python datatype, invalid param. Tried to convert param to {converter.__name__!r}. \nDetailed error: {e}"
            ) from e

            

    def _check_missing_params(self, data: Dict[str, str]):
        """Toma un diccionario y comprueba que todas las llaves tengan un valor no nulo"""
        for option,value in data.items():
            if not value:
                raise exceptions.UncompletedConfig(f"{option!r} param is missing, no value for {option!r} found.")
            
    def _process_read(self):
        """Toma el proxy obtenido de ``ConfigParser.items()`` y devuelve el tipo de los parametros a tipos de Python"""
        joined_dict = self._get_items_from_load()                   # devuelve un dict[section: {option1:value, option2:value, ...}]
        d  = {}
        
        self._check_missing_params(joined_dict["Required"])   # queremos saber si todos los parametros de [Required] estan completos
        # raisea exceptions.UncompletedConfig si alguno esta incompleto
        
        for section, options in joined_dict.items():              
            for key,value in options.items():
                try:
                    d[key] = self._conv_value_type(value, self.params[key]["default"])   # pasamos el valor en string y el valor original 
                except exceptions.ConfigWrongParamFormat as e:
                    raise exceptions.ConfigWrongParamFormat(
                        f"Wrong param format in section '{section}' key: '{key}'. Detailed error: {e}"
                    ) from None
        return d
    
    def _get_items_from_load(self):
        """
        Toma el view proporcionado por ``ConfigParser.read`` y lo transforma a un diccionario de la forma 
        ``dict[section: {option1:value, option2:value, ...}]``
        """
        return {section: dict(self._parser.items(section)) for section in self._parser.sections()}  # -- .sections() dont include 'default' section
    
    
    #& ----------------------------------- PUBLIC FUNCTIONS -------------------------------------
    def create(self, loc: Union[str, Path], overwrite: bool = False):
        self.config_path = Path(loc).resolve() #? Creamos un atributo de clase para compartir la ruta del configFile.
        if self.config_path.suffix != ".ini":
            self.config_path = self.config_path.with_suffix(".ini")
        
        if self.config_path.exists() and not overwrite:
            raise exceptions.ConfigFileAlreadyCreated(f"Config File already created in {self.config_path}. If you created an empty one, delete it, otherwise run ``qautolinguist build run`` if you have already edited the file.")
        
        processed_template = self._process_template()    #creamos una instancia con los valores vacios y procesamos el template con esos
        with self.config_path.open("w", encoding="utf-8") as file_:
            file_.write(processed_template)
        
        return self.config_path
    
    def load_config(self, loc: Optional[Union[str, Path]] = None):
        loc = Path(loc).resolve() if loc is not None else None

        if loc is not None and loc.exists():                                # si el path pasado es valido, seguimos adelante
            pass
        elif consts.CMD_CWD.joinpath(consts.CONFIG_FILENAME).exists():             # existe en el CWD del comando. Si el usuario a especificado un nombre para el archivo
            loc = consts.CMD_CWD / consts.CONFIG_FILENAME                          # debe pasar la ruta, no sabemos el nombre del archivo.
        elif hasattr(self, "config_path"):                  
            if consts.CMD_CWD.joinpath(self.config_path.name).exists():
                loc = consts.CMD_CWD.joinpath(self.config_path.name)  # se verifica si al usar create() se ha usado el CMD del comando
            else:  
                loc = self.config_path    # se ha utilizado create en el mismo tiempo de ejecuccion
    
        if loc is not None:               # No se ha encontrado el archivo, se deberá pasar la ruta en este caso.
            self._parser.read(loc, encoding="utf-8")
            return self._process_read()

        raise exceptions.MissingConfigFile("Unable to find Config file. Create a config file with Config.create() or pass a valid path.")
            
         


