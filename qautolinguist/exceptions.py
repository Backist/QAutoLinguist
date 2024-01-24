"QAutoLinguist related exceptions thats implements nice output with colors"

from qautolinguist.debugstyles import DebugLogs
from typing import Optional, List

class QALBaseException(Exception):
    """Base exception for QAutoLinguist.
    Supports color-formatted messages with ``DebugLogs`` classes or subclasses. Default ``DebugLogs.error``
    """
    formatter: DebugLogs = DebugLogs.error
    reason: str
    def __init__(self, reason: str = "Unexpected error raised"):
        self.reason = reason
        super().__init__(self.formatter(self.reason))
        
        
#& -- Specific Exceptions --
class QALConfigException(QALBaseException):
    "Subclassed Group Exception to errors related with ``Config()`` class and config process"
    def __init__(self, reason: Optional[str] = "Something went wrong during the config process"):
        self.reason = reason

class QALTranslatorException(QALBaseException):
    "Subclassed Group Exception to errors related with ``Translator()`` class"
    def __init__(self, reason: Optional[str] = "Something went wrong during the translation process"):
        self.reason = reason


#& -- Top-level Exceptions --
class IOFailure(QALBaseException, OSError):
    """Exception raised when a resource was not found in the system or IO operation fails. 
    
    This exception is subclass of ``QalBaseException`` and ``OSError``
    """
    def __init__(self, reason: Optional[str] = "Something went wrong while trying to handle IO process"):
        self.reason = reason
   
class InvalidLanguage(QALTranslatorException):
    "Exception raised when a language is not either supported or is invalid"
    def __init__(
            self, 
            reason: str = "Invalid languages found.",
            invalid_lang: Optional[List] = None,
    ):
        if invalid_lang is not None: 
            self._failed_lang = invalid_lang
        self.reason = reason
              
    @property
    def failed_lang(self):
        return self._failed_lang

class InvalidOptions(QALTranslatorException):    
    "Exception raised when an invalid option is passed to either ``pylupdate`` or ``pylrelease``"
    def __init__(
            self, 
            reason: str = "Invalid options found.",
            invalid_option: Optional[List] = None,
    ):
        if invalid_option is not None: 
            self._failed_option = invalid_option
        self.reason = reason
        
    @property
    def failed_option(self):
        return self._failed_option
    
class RequiredFileError(IOFailure, IsADirectoryError):
    """Exception raised when a process expected a directory path.
    
    This class subclasses `IsADirectoryError` for convenience.
    """
    pass
        
class RequiredDirError(IOFailure, NotADirectoryError):
    """Exception raised when a process expected a file path.
    
    This class subclasses `NotADirectoryError` for convenience.
    """
    pass
        
class CompilationError(QALBaseException):
    "Exception raised when an error raised during the compilation of .qm files"
    pass

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

class TOMLConversionError(QALBaseException):
    "Exception raised when trying to convert any python object into a TOML file format."
    pass

class UncompletedConfig(QALConfigException):
    "Exception raised when config file has uncompleted or empty values."
    pass
        
class MissingConfigFile(QALConfigException):
    "Exception raised when trying to load a config_file with Config.load_config but Config.create_config wasnt called."
    pass


