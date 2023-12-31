from qautolinguist.debugstyles import DebugLogs


class QALBaseException(Exception):
    """Base exception for QAutoLinguist.
    Supports color-formatted messages with ``DebugLogs`` classes or subclasses. Default ``DebugLogs.error``
    """
    formatter: DebugLogs = DebugLogs.error
    def __init__(self, msg: str = "Unexpected error raised"):
        super().__init__(self.formatter(msg))
        
class QALConfigException(QALBaseException):
    "Subclassed Group Exception to errors related with ``Config()`` class and config process"
    pass

class QALTranslatorException(QALBaseException):
    "Subclassed Group Exception to errors related with ``Translator()`` class"
    pass  

class IOFailure(QALBaseException, OSError):
    """Exception raised when a resource was not found in the system or IO operation fails. 
    
    This exception is subclass of ``QalBaseException`` and ``OSError``
    """
    pass
   
class RequiredFileError(IOFailure):
    "Exception raised when a process expected a directory path."
    pass
        
class RequiredDirError(IOFailure):
    "Exception raised when a process expected a file path."
    pass
        
class CompilationError(QALBaseException):
    "Exception raised when an error raised during the compilation of .qm files"
    pass

class InvalidLanguage(QALTranslatorException):
    "Exception raised when a language is not either supported or is invalid"
    def __init__(self, msg: str, invalid_language: list | None = None):
        if invalid_language is not None: 
            self._failed_lang = invalid_language
        super().__init__(msg)  
              
    @property
    def failed_lang(self):
        return self._failed_option

class InvalidOptions(QALTranslatorException):    
    "Exception raised when an invalid option is passed to either ``pylupdate`` or ``pylrelease``"
    def __init__(self, msg: str, invalid_option: list | None = None):
        if invalid_option is not None: 
            self._failed_option = invalid_option
        super().__init__(msg)

    @property
    def failed_option(self):
        return self._failed_option

class TranslationFailed(QALTranslatorException):
    "Exception raised when unexpected error is raised during translating a .ts file with the API"
    pass
        
class TranslatorConnectionError(QALTranslatorException):
    "Exception raised when failed to connect/access to the server."
    pass
     
class ConfigFileAlreadyCreated(QALConfigException):
    "Exception raised when trying to create/initialize a file that already exists"
    formatter: DebugLogs = DebugLogs.warning

class ConfigWrongParamFormat(QALConfigException):
    "Exception raised when an unexpected error is raised during the conversion of config file params to python types"
    pass

class UncompletedConfig(QALConfigException):
    "Exception raised when config file has uncompleted or empty values."
    pass
        
class MissingConfigFile(QALConfigException):
    "Exception raised when trying to load a config_file with Config.load_config but Config.create_config wasnt called."
    pass
    



        
         





