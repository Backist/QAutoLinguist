import configparser
import helpers
import exceptions
import consts
from dataclasses import dataclass
from functools import lru_cache
from ast import literal_eval      # para convertir listas y otras estructuras de datos de str a su tipo original
from pathlib import Path
from typing import List, Dict, Optional, Union

__all__: list[str] = ["Config"]


#? Pongo los comentarios en el doc de la clase porque hace dos funciones: Explicar que son los parametros de la clase y a la vez ser los comentarios
#? que se pondrán en el config.ini
class Config:
    """
    Class that represents a Configuration File and its attributes.
    
    This class only uses its own way to make ``.ini`` files and uses ``configparser.ConfigParser`` to read .ini files.
    """
    
    #! Los atributos pedidos son los mismos que pide QAutoLinguist, REVISAR si SON IGUALES SIEMPRE.
    #! Si se modifica consts.PARAMS_DESCRIPTION, QAutoLinguist o este, debemos incorporar los cambios a cada uno, puesto comparten parametros.
    def __init__(
        self,
        source_file:            Union[str, Path],                   # .ui | .py file to search for "tr" funcs
        available_languages:    List[str],              # locales to make a translation file for each one, MUST BE <xx_XX> type locale    
        *,
        default_language:       str = "en",          # reference locale, took as a reference to make other translations
        source_files_folder:    Union[str, Path] = None,              #.ts files.  
        translations_folder:    Union[str, Path] = None,              # .qm files. 
        translatables_folder:   Union[str, Path] = None,              #.toml files. 
        use_default_on_failure: bool = True,            # Se debe usar la traduccion del default si la de alguno falla. When False a FailedTranslation exception wil be raised
        revise_after_build:     bool = False,           # Permite al usuario ver las traducciones y modificarlas antes de ser compiladas a .qm
        clean:                  bool = True,            # Elimina todos los directorios y archivo de configuracion creados excepto la de las traducciones. 
        debug_mode:             bool = False,           # Enabled debug logging
        verbose:                bool = False,           # Verbose all called private methods  
    ):  
        self.source_file               = source_file               
        self.available_languages       = available_languages
        self.default_language          = default_language
        self.source_files_folder       = source_files_folder
        self.translations_folder       = translations_folder
        self.translatables_folder      = translatables_folder 
        self.use_default_on_failure    = use_default_on_failure
        self.revise_after_build        = revise_after_build
        self.clean                     = clean
        self.debug_mode                = debug_mode
        self.verbose                   = verbose

        self._parser = configparser.ConfigParser(allow_no_value=False, empty_lines_in_values=False)



    #& ----------------------------------- INTERNAL FUNCTIONS -------------------------------------
    #* [DEPRECATED] Esta funcion se encargaba de parsear el __doc__ donde estaban las explicaciones de los parametros. 
    #* en su lugar ahora usamos un diccionario estatico que esta en consts.consts.PARAMS_DESCRIPTION
    # def _get_comments(self): 
    #     """
    #     Usa el docstring de la clase para extraer los comentarios de los parametros de la clase y se retorna
    #     un dict de la forma ``dict[key: comment]``"""
    #     from re import findall 
    #     # comments match the form => :param <name_attr>: ``comment``
    #     params_match = findall(r':param\s+([\w_]+):\s+``(.+?)``', Config.__doc__) # Toma los comentarios del __doc__ de la clase
    #     return dict(params_match)
    
    
    def _process_dict_data(self):
        """Devuelve un diccinario  ``dict[param:comment]`` tomando ``self.__dict__`` y ``consts.PARAMS_DESCRIPTION``
        NOTE: ``Es importante que todos los atributos que quieran incluir en la config estén definidos como atributos de instancia y no empiezen por '_'
        """ 
        param_comments = consts.PARAMS_DESCRIPTION  #! Importamos el diccionario estatico que contiene los comentarios, es de la forma dict[param: comment]
        return {
            key: (
                helpers.stringfy(value),    # convertimos el valor a str (configparser convierte todo a str)
                helpers.fit_string(param_comments.get(key, ""), split_size=75, preffix="#")      # si no se encuentra el parametro en el diccionario de comentarios, ese parametro no tiene comentario
                ) 
            for key,value in self.__dict__.items() if not key.startswith("_") # consideramos parametros validos aquellos que no sean privados (que se toman como necesarios para que la clase funcione)
        }

    def _format_dict_data(self):
        """
        A partir del diccionario devuelto por self._process_dict_data, se reformatea el diccionario en la forma:
        Pasamos de ``dict[key: (value, comment)]`` a ``dict[key: key, key_value: value, key_comment: comment]``
        El diccionario devuelto es el que se pasa para formatear el consts.INI_FILE_TEMPLATE, que corresponde al formato
        estático del archivo de configuracion
        """
        dict_data = self._process_dict_data()           # structure => {key: (value, comment)}
        d = {}
        for key, (value, comment) in dict_data.items():
            d[key] = key
            d[f"{key}_value"] = value
            d[f"{key}_comment"] = comment
        return d
    
    def _process_template(self):
        return consts.INI_FILE_TEMPLATE.format(**self._format_dict_data())   
    
    def _conv_value_type(self, raw, original):
        """
        This function gets a string and tries to convert into a python valid format type and tries to convert to python datatype        
        NOTE: ``This function actually converts that types specified below:``
        - ``List, Tuple, Set``
        - ``bool, str, int, float, complex``
        - [NotImplemented] ``pathlib.Path``
        """
        raw             = raw.strip().lower()
        converter       = None
        
        if not raw:     # si es una cadena vacia, devolvemos None (no vemos si su valor original es None porque no es relevante si esta vacia)
            return None
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
            raise exceptions.ConfigWrongParamFormat(f"Cant convert {raw!r} to python datatype, invalid param. Tried to convert param to {converter.__name__!r}. \nDetailed error: {e}")
        
        
    def _check_missing_params(self, data: Dict[str, str]):
        """Toma un diccionario y comprueba que todas las llaves tengan un valor no nulo"""
        for option,value in data.items():
            if not value:
                raise exceptions.UncompletedConfig(f"{option!r} param is missing, no value for {option!r} found.")
            
    def _process_read(self):
        """Toma el proxy obtenido de ``ConfigParser.items()`` y devuelve el tipo de los parametros a tipos de Python"""
        joined_dict = self._get_items_from_load()                   # devuelve un dict[section: {option1:value, option2:value, ...}]
        final_dict  = {}
        
        self._check_missing_params(joined_dict["Required"])   # queremos saber si todos los parametros de [Required] estan completos
        # raisea exceptions.UncompletedConfig si alguno esta incompleto
        
        for section, options in joined_dict.items():                        # despreciamos section aqui, no nos hace falta
            for key,value in options.items():
                try:
                    final_dict[key] = self._conv_value_type(value, self.__dict__[key])   # pasamos el valor en string y el valor original 
                except exceptions.ConfigWrongParamFormat as e:
                    raise exceptions.ConfigWrongParamFormat(
                        f"Wrong param format in section '{section}' key: '{key}'. Detailed error: {e}"
                    ) from None
        return final_dict
    
    def _get_items_from_load(self):
        """
        Toma el view proporcionado por ``ConfigParser.read`` y lo transforma a un diccionario de la forma 
        ``dict[section: {option1:value, option2:value, ...}]``
        """
        return {section: dict(self._parser.items(section)) for section in self._parser.sections() if section != "Internal"}
    
    
    #& ----------------------------------- PUBLIC FUNCTIONS -------------------------------------
    def create(self, loc: Union[str, Path]):
        self.config_path = Path(loc).resolve() #? Creamos un atributo de clase para compartir la ruta del configFile.
        if self.config_path.suffix != ".ini":
            self.config_path = self.config_path.with_suffix(".ini")
        
        if self.config_path.exists():
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
            
            
if __name__ == "__main__":
    
    c = Config("C:", ["spanish", "spanish", "spanish", "spanish", "spanish","spanish", "spanish"])
    p = c.create(consts.RUNTIME_FOLDER / "testhahaha.ini")
    print(c.load_config())
    

