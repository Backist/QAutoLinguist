import configparser
import json
import consts
import helpers
import exceptions

from config_template import INI_FILE_TEMPLATE
from ast import literal_eval      # para convertir listas y otras estructuras de datos de str a su tipo original
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, Union


__all__: list[str] = ["Config"]


class Config:
    """
    Class that represents a Configuration File and its attributes.
    
    This class only uses its own way to make ``.ini`` files and uses ``configparser.ConfigParser`` to read .ini files.
    """
    
    def __init__(self):  
        self._parser = configparser.ConfigParser(
            allow_no_value=False,       # allow keys with empty value
            empty_lines_in_values=False,   
            inline_comment_prefixes= "#", 
        )

    #& ----------------------------------- INTERNAL FUNCTIONS -------------------------------------
    def _process_dict_data(self) -> Dict[str, Tuple[str, str]]:
        "Devuelve un diccinario  ``dict[param:(value,comment)]`` tomando a partir de los parametros requeridos por ``QAutoLinguist``" 
        
        with open(consts.PARAM_DECLS_PATH) as fp:
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

    def _format_dict_data(self) -> Dict[str, str]:
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
    
    def _process_template(self) -> str:
        return INI_FILE_TEMPLATE.format(**self._format_dict_data())   
    
    def _conv_value_type(self, raw, original) -> Union[str, int, float, bool, tuple, list, None]:
        """
        This function gets a string and tries to convert into a python valid format type and tries to convert to python datatype        
        NOTE: ``This function actually converts that types specified below:``
        - ``List, Tuple, Set``
        - ``bool, str, int, float, complex``
        - [NotImplemented] ``pathlib.Path``
        
        ### Raises:
        - ``ConfigWrongParamFormat``: If some value in configuration file was not able to convert to its original type.
        """
        raw = raw.strip().lower()
        converter = None

        if not raw:   
            return None
        if original is None:
            return raw or None
        if isinstance(original, str):
            return raw 

        if isinstance(original, bool):
            positive_cases = {"true", "t", "on", "yes", "1"}
            negative_cases = {"false", "f", "off", "no", "0"}
            if raw in positive_cases:
                return True
            if raw in negative_cases:
                return False
            else: 
                raise exceptions.ConfigWrongParamFormat(
                    f"Failed trying to format {raw!r} into a bool type, valid boolean formats are {positive_cases} or {negative_cases}"
                )  # raise specific exceptions when refering to booleans to show valid and invalid types.
                
        if isinstance(original, int):
            converter = int     # raises ValueError on failure
        elif isinstance(original, float):
            converter = float  # raises ValueError on failure
        elif isinstance(original, (list, tuple)):
            converter = literal_eval           # para convertir listas y otras estructuras de datos de str a su tipo original
            # raises SyntaxError on failure
            
        if converter is None:
            raise exceptions.ConfigWrongParamFormat(
                "Given object was not able to convert. Reason: No implemented type convertion."
            )
        
        return converter(raw)

    def _check_missing_params(self, data: Dict[str, str]) -> None:
        """
        Toma un diccionario y comprueba que todas las llaves tengan un valor no nulo
    
        ### Raises:
        - ``UncompletedConfig``: If some parameter is missing in ``Required`` section.
        """
        for option,value in data.items():
            if not value:
                raise exceptions.UncompletedConfig(f"{option!r} param is missing, no value for {option!r} found.")
            
    def _process_read(self) -> Dict[str, Any]:
        """
        Toma el proxy obtenido de ``ConfigParser.items()`` y devuelve el tipo de los parametros a tipos de Python
        
        ### Raises:
        - ``ConfigWrongParamFormat``: If some value in configuration file was not able to convert to its original type.
        - ``UncompletedConfig``: If some parameter in ``Required`` section is missing.
        """
        with open(consts.PARAM_DECLS_PATH) as fp:
            original_params = json.load(fp)  
            
        raw_data = self._get_dict_from_load() # dict[section: {option1:value, option2:value, ...}]
        d  = {}
        
        self._check_missing_params(raw_data["Required"])  

        for section, options in raw_data.items():              
            for key,value in options.items():
                try:
                    d[key] = self._conv_value_type(value, original_params[key]["default"])  # value, type(original value), since raw values were converted to str.
                except exceptions.ConfigWrongParamFormat as e:
                    raise exceptions.ConfigWrongParamFormat(
                        f"Wrong param format in section '{section}' key: '{key}'. Detailed error: {e}"
                    ) from None
        return d
    
    def _get_dict_from_load(self) -> Dict[str, Dict[str, str]]:
        """
        Toma el view proporcionado por ``ConfigParser.read`` y lo transforma a un diccionario de la forma 
        ``dict[section: {option1:value, option2:value, ...}]``
        """
        return {section: dict(self._parser.items(section)) for section in self._parser.sections()}  # -- .sections() do not include 'default' section
    
    
    #& ----------------------------------- PUBLIC FUNCTIONS -------------------------------------
    def create(self, loc: Union[str, Path], overwrite: bool = False) -> Path:
        """
        Create a configuration file in loc.
        
        ### Raises:
        - ``RequiredFileError``: If loc does not point to a file.
        - ``ConfigAlreadyCreated``: Thrown when create was called before.
        """
        self.config_path = Path(loc).resolve()
        
        if self.config_path.exists():
            if not overwrite:
                raise exceptions.ConfigFileAlreadyCreated(
                f"Config File already created in {self.config_path}. If you created an empty one, delete it, otherwise run ``qautolinguist build run`` if you have already edited the file."
                )
                
            if not self.config_path.is_file():
                raise exceptions.RequiredFileError("'loc' must be a path pointing to a file.")
  
        if self.config_path.suffix != ".ini":
            self.config_path = self.config_path.with_suffix(".ini")
            
        processed_template = self._process_template()    #creamos una instancia con los valores vacios y procesamos el template con esos
        with self.config_path.open("w", encoding="utf-8") as file_:
            file_.write(processed_template)
        
        return self.config_path
    
    def load_config(self, loc: Optional[Union[str, Path]] = None) -> Dict[str, Any]:
        """
        Load configuration file and returns a dict containing section-options values.
        
        ### Raises:
        - ``RequiredFileError``: If loc does not point to a file.
        - ``MissingConfigFile``: Thrown when loc is None and ``.create()`` was not called.
        - ``IOFailure``: If loc does not exist.
        """
        if loc is None:
            if hasattr(self, "config_path"):                  
                loc = self.config_path    # se ha utilizado create en el mismo tiempo de ejecuccion
            elif consts.CMD_CWD.joinpath(consts.CONFIG_FILENAME).exists():             # existe en el CWD del comando. Si el usuario a especificado un nombre para el archivo
                loc = consts.CMD_CWD / consts.CONFIG_FILENAME                          # debe pasar la ruta, no sabemos el nombre del archivo.
        else:
            helpers.process_loc(loc)
                
        if loc is not None:               
            self._parser.read(loc.resolve(), encoding="utf-8")
            return self._process_read()
        
        raise exceptions.MissingConfigFile("Unable to find Config file. Create a config file with Config.create() or pass a valid path.") # No se ha encontrado el archivo, se deberá pasar la ruta en este caso.
            
       
            