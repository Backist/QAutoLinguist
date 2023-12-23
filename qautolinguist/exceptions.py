from debugstyles import DebugLogs


class QALBaseException(Exception):
    """Base exception for QAutoLinguist.
    Supports color-formatted messages with ``DebugLogs`` classes or subclasses. Default ``DebugLogs.error``
    """
    formatter: DebugLogs = DebugLogs.error
    def __init__(self, msg: str):
        super().__init__(self.formatter(msg))

class QALConfigException(QALBaseException):
    """Subclassed Group Exception to errors related with ``Config()`` class and config process"""
    pass

class QALTranslatorException(QALBaseException):
    """Subclassed Group Exception to errors related with ``Translator()`` class"""
    pass  

class IOFailure(QALBaseException, OSError):
    """Exception raised when OSError. This exception is subclass of ``QalBaseException`` and ``OSError``"""
    pass

class InvalidOptions(QALBaseException):
    """Exception raised on invalid options in methods"""
    pass
   
class FileNotExist(QALBaseException):
    """Exception raised when tried to operate with a file that doesnt exist"""
    pass
        
class DirNotExist(QALBaseException):
    """Exception raised when tried to operate with a directory that doesnt exist"""
    pass
        
class CompilationError(QALBaseException):
    """Exception raised when an error raised during the compilation of .qm files"""
    pass

class TOMLConversionException(QALBaseException):
    """
    Exception raised when unexpected error during the conversion of a TOML file is encountered.
    This exception is exclusive to mark processes which uses ``rtoml`` module.
    """
    pass

class InvalidLanguage(QALTranslatorException):
    """Exception raised when a language is not either supported or is invalid"""
    def __init__(self, msg: str, invalid_language: list | None = None):
        if invalid_language is not None: 
            self._failed_lang = invalid_language
        super().__init__(msg)  
              
    @property
    def failed_lang(self):
        return self._failed_option

class InvalidOptions(QALTranslatorException):    
    """Exception raised when an invalid option is passed to either ``pylupdate`` or ``pylrelease``"""
    def __init__(self, msg: str, invalid_option: list | None = None):
        if invalid_option is not None: 
            self._failed_option = invalid_option
        super().__init__(msg)

    @property
    def failed_option(self):
        return self._failed_option

class TranslationFailed(QALTranslatorException):
    """Exception raised when unexpected error is raised during translating a .ts file with the API"""
    pass
        
class TranslatorConnectionError(QALTranslatorException):
    """Exception raised when failed to connect/access to the server."""
    pass
     
class ConfigFileAlreadyCreated(QALConfigException):
    """Exception raised when trying to create/initialize a file that already exists"""
    formatter: DebugLogs = DebugLogs.warning

class ConfigWrongParamFormat(QALConfigException):
    """Exception raised when an unexpected error is raised during the conversion of config file params to python types"""
    pass

class UncompletedConfig(QALConfigException):
    """Exception raised when config file has uncompleted or empty values."""
    pass
        
class MissingConfigFile(QALConfigException):
    """Exception raised when trying to load a config_file with Config.load_config but Config.create_config wasnt called."""
    pass
    



        
         





