"""
QAutoLinguist - Automatic and user-friendly configurable Translator for .ts files for Qt proyects, 
using pyside6-lupdate and pyside6-lrelease though a modern and simple CLI.


pyside6-lupdate - Translation File Generator for PySide6 Applications
=======================================================================
BASIC SYNTAX:
  pyside6-lupdate [OPTIONS] source_file -ts <path>

  source_file:    Source file (e.g., .py or .ui).  [pyside6-lupdate can be used with both .ui and .py files.]
  path: Generated translation file location. Pylupdate will create a file if the localtion doesn-t point to a file

OPTIONS:
  -no-obsolete:     Do not include obsolete translations in the .ts file.
  -locations:      Include location information in the .ts file.
  -recursive:      Search recursively in directories.
  -source-language: Define the source language.

ADDITIONAL COMMANDS:
  --version: Show the tool version.
  --help:    Display help information.
  
This .ts file can be translated using tools like pyside6-lrelease to generate binary translation files (.qm) used by the application.

Keep in mind that, in the context of internationalization in Qt, translation files (.ts) are generated from source files, 
and then they are compiled into binary translation files (.qm). These binary files are used to provide translation at runtime.
=======================================================================

pyside6-lrelease - PySide6 Translation File Compiler
=======================================================================
BASIC SYNTAX:
  pyside6-lrelease translation_file -qm compiled_translation_file

  translation_file:           Translation file (.ts) generated by pyside6-lupdate.
  compiled_translation_file:  Compiled binary translation file (.qm).

MAIN OPTIONS:
  -compress:      Compress the translation data to reduce the file size.
  -removeidentical: Remove identical duplicate translations.

ADDITIONAL COMMANDS:
  --version: Show the tool version.
  --help:    Display help information.

USAGE:
  pyside6-lrelease is used to compile translation files (.ts) generated by pyside6-lupdate into binary translation files (.qm).

  Example:
    pyside6-lrelease form.ts -qm form.qm

This command will compile the translation file form.ts into the binary file form.qm.
=======================================================================


When using both pyside6-lupdate and pyside6-lrelease in a translation workflow, the process typically involves the following steps:

1. **Generate Translation File (.ts):**
   - Use pyside6-lupdate to generate a translation file (.ts) from source files (e.g., .py or .ui).

     Example:
     ```bash
     pyside6-lupdate source_file -ts translation_file
     ```
2. **Translate (.ts) File:**
   - Open the generated .ts file with a translation tool, such as Qt Linguist, and provide translations for each string.
3. **Compile Translation (.ts) to Binary (.qm):**
   - Use pyside6-lrelease to compile the translated .ts file into a binary translation file (.qm).
   
     Example:
     ```bash
     pyside6-lrelease translation_file.ts -qm compiled_translation_file.qm
     ```
     
4. **Use Compiled (.qm) File:**
   - Integrate the compiled .qm files with your PySide6 application to enable runtime translation.

The compiled .qm files are used by PySide6 to provide translations for the application's interface at runtime. 
This workflow allows for the separation of translation concerns from the application's source code.


See https://doc.qt.io/qtforpython-6/tutorials/basictutorial/translations.html for further information
"""   

import qautolinguist.consts as consts
import qautolinguist.exceptions as exceptions
import qautolinguist.helpers as helpers
import qautolinguist.pytomlpp as pytomlpp 
import xml.etree.ElementTree as ET
import shutil
import subprocess

from click import echo
from qautolinguist.debugstyles import DebugLogs
from qautolinguist.translator import Translator
from pathlib import Path
from typing import Optional, List, Union, Dict


__all__: List = ["QAutoLinguist"]


class QAutoLinguist:
    """QAutoLinguist main class.
    
    ## Params:
    :param source_file: ``.ui or .py file to search for "tr" funcs.``
    :param available_languages: ``A list of languages/locales that your aplication will support. Langs or locales can be put either as <xx_XX> or typing the lang directly (english, spanish, etc).``
    :param default_language: ``Reference locale, took as a reference to make other translations.``
    :param source_files_folder: ``Folder that contains the .ts files (Qt translation Files). If not specified, a folder will be created in CWD where you put the command.``
    :param translations_folder: ``Folder that contains the .qm file (Final translation files that your app will use). If not specified, a folder will be created in CWD where you put the command.``
    :param translatables_folder: ``Folder that contains the .toml files (editable translation files). If not specified, a folder will be created in CWD where you put the command.``
    :param use_default_on_failure: ``When True, translation reference will be use in case one translation in one language fails. When False a FailedTranslation exception wil be raised.``
    :param revise_after_build: ``Allow to see and edit translated translations in case you want to modify some words or phrases after compile the files.``
    :param clean: ``Removes all runtime directories created (translatables & font_files folders) and keeps the folder that contains the final translations. Essentially a clean build.``
    :param debug_mode: ``Displays information about the state of the build.``
    :param verbose: ``Displays more information about the processes done. DEBUG_MODE must be True to enable that option.``
    """
    
    _TS_EXT                    = ".ts"              #Explicit written
    _TOML_EXT                  = ".toml"            #Explicit written
    _QM_EXT                    = ".qm"              #Explicit written
    _SOURCE_FILES_FOLDER_NAME  = "qt_font_files"   
    _TRANSLATIONS_FOLDER_NAME  = "translations"   
    _TRANSLATABLES_FOLDER_NAME = "translatables"  
    # SOURCE FILES:         Contain the Qt Translation sources files (.ts files)
    # TRANSLATION FILES:    Contain compiled final-use translation files (.qm files)
    # TRANSLATABLE FILES:   Contain .toml files with translation sources. That files make the translation of sources more easier and readable
    # through a styled-clean file format TOML
    
    
    def __init__(
        self,
        source_file:            Union[str, Path],        # .ui | .py file to search for "tr" funcs
        available_languages:    List[str],               # locales to make a translation file for each one, MUST BE <xx_XX> type locale    
        *,                                               # can be passed the lang in two ways. english or en (language or abreviation)
        default_language:       str = "en",              # reference locale, took as a reference to make other translations
        source_files_folder:    Union[str, Path] = None, #.ts files.   If None, will be created a child folder in translation_folder
        translations_folder:    Union[str, Path] = None, # .qm files.  If None, a new folder in CWD is created
        translatables_folder:   Union[str, Path] = None, #.toml files. If None, will be created a child folder in translation_folder
        use_default_on_failure: bool = True,             # Se debe usar la traduccion del default si la de alguno falla. When False a FailedTranslation exception wil be raised
        revise_after_build:     bool = False,            # Permite al usuario ver las traducciones y modificarlas antes de ser compiladas a .qm
        clean:                  bool = True,             # Elimina todos los directorios y archivo de configuracion creados excepto la de las traducciones. 
        debug_mode:             bool = False,            # Enabled debug logging
        verbose:                bool = False,            # Verbose all called private methods  
    ):
        
        # -- checking valid source_file is passed --
        self.source_file = self._init_file(source_file, create_empty=False, strict=True)
        
        # -- validating languages --
        self.translator = Translator()                   # Inicializamos el translator que traducirá las fuentes con una API
        if not self.translator.validate_languages(available_languages):
            raise exceptions.InvalidLanguage("Found invalid or not supported languages in available_languages")
        
        if default_language in available_languages:
            available_languages = [lang for lang in available_languages if lang != default_language]     
        elif not self.translator.validate_language(default_language):
            raise exceptions.InvalidLanguage(f"{default_language!r} (default-language) is not a supported language or its format is incorrect")
        
        # -- checking paths --
        if translations_folder is None:
            translations_folder      = consts.CMD_CWD / self._TRANSLATIONS_FOLDER_NAME      # If None, create new one in CWD
            self.translations_folder = self._init_dir(translations_folder, exist_ok=True)
        else:
            self.translations_folder = self._init_dir(translations_folder, create_empty=False, strict=True) #User specified folder, save there
        
        if source_files_folder is None:
            source_files_folder      = self.translations_folder / self._SOURCE_FILES_FOLDER_NAME 
            self.source_files_folder = self._init_dir(source_files_folder, exist_ok=True)                   # If None, create a child in translations_folder
        else:  
            self.source_files_folder = self._init_dir(source_files_folder, create_empty=False, strict=True) #User specified folder, save there

        if translatables_folder is None:
            translatables_folder      = self.translations_folder / self._TRANSLATABLES_FOLDER_NAME      # If None, create a child in translations_folder
            self.translatables_folder = self._init_dir(translatables_folder, exist_ok=True)        
        else:
            self.translatables_folder = self._init_dir(translatables_folder, create_empty=False, strict=True) #User specified folder, save there
        
        self.default_language                    = default_language
        self.available_languages                 = available_languages 
        self.use_default_on_failure              = use_default_on_failure
        self.revise_after_build                  = revise_after_build
        self.clean                               = clean  
        self.debug_mode                          = debug_mode                                          
        self.verbose                             = verbose     
        
        self._ts_reference_file                  = self.source_files_folder / f"{self.default_language}{self._TS_EXT}"
        self.map: dict[str, List[Path]]        = {locale: [] for locale in self.available_languages}  
            # mapping para guardar las rutas de los archivos de cada lenguaje
            # dict[language: [font_file (.ts), translatable_file (.toml), qm_file (.qm)]  
        
        # if _config_file:
        #     self._refresh_config_file(_config_file)
            
        self._build_done: bool = False       # Runtime trade variable to check if a build has done or not since its nessesary to make a
        # instance to build one                      
        

    @staticmethod
    def _init_dir(
        loc: Union[str, Path], 
        create_empty: bool = True, 
        parents: bool = True, 
        exist_ok: bool = True, 
        strict: bool = False
    ) -> Path:    # when strict=True raises FileNotFoundError
        """
        Creates a ``pathlib.Path`` object and normalises it. It will also verify that the path refers to a valid directory and exists.
        If ``mkdir`` is True, it will attempt to create an empty one.
        
        Raises:
        - ``FileNotFoundError`` -> Raised when tried to resolve but path was not found (raised by ``pathlib.resolve()``)
        - ``IOFailure`` -> When the path does not exist
        - ``RequiredDirError`` -> Whether a path does not point to a directory.
        """ 
        loc = loc if isinstance(loc, Path) else Path(loc)
        if create_empty:
            if loc.exists():
                echo(DebugLogs.warning(f"Found existing folder '{loc.name}', content inside will be overwritten."))
                
            try:
                loc.mkdir(mode=751, parents=parents,exist_ok=exist_ok)    # mode = 0o511 -> Requires admin to delete the folder. See UNIX file permissions
            except OSError as e:
                raise exceptions.IOFailure(f"Could not be created directory: {loc}. Detailed error: {e}") from e
            
            return loc.resolve(strict)      # when strict=True raises FileNotFoundError
        
        helpers.process_loc(loc, dir_okay=True)
        return loc.resolve(strict)      # when strict=True raises FileNotFoundError
    
    @staticmethod
    def _init_file(
        loc: Union[str, Path], 
        create_empty: bool = True, 
        exist_ok: bool = True, 
        strict: bool = False
    ) -> Path:
        """
        Create a ``Path`` object with ``loc``, normalize it and try to create an empty file if ``mkfile=True``\n
        NOTE: ``Path object can be passed to loc, but unless you want to create an empty file, this funcion will be useless,
        since it will return the resolved Path only``\n
        The aim of that function is to transform loc to Path object, caching exceptions, and also allowing to initialize it by 
        creating the file
        
        Raises:
        - ``FileNotFoundError`` -> Raised when tried to resolve but path was not found (raised by ``pathlib.resolve()``)
        - ``IOFailure`` -> When the path does not exist
        - ``RequiredFileError`` -> Whether a path does not point to a file.
        """
        loc = loc if isinstance(loc, Path) else Path(loc)
        if create_empty:
            if loc.exists():
                echo(DebugLogs.warning(f"Found existing file '{loc.name}', content inside will be overwritten."))
                
            try:
                loc.touch(mode=751, exist_ok=exist_ok)   # mode = 0o511 -> Requires admin to delete the folder. See UNIX file permissions
            except OSError as e:
                raise exceptions.IOFailure(f"Could not be created file: {loc}. Detailed error: {e}") from e

            return loc.resolve(strict)      # when strict=True raises FileNotFoundError
        
        helpers.process_loc(loc, dir_okay=False)
        return loc.resolve(strict)      # when strict=True raises FileNotFoundError
        
  
    #& ----------  INTERNAL FUNCTIONS  ----------
    # def _refresh_config_file(self, loc):
    #     inst = Config()
    #     initial_data = inst._process_dict_data()
    #     inst._data = {param:self.__dict__.get(param, "") for param in initial_data.keys()}     # forzamos el valor del diccionario.
    #     inst.create(loc, overwrite=True)
    
    def _validate_options(self, options: List[str], valid_options: List[str] = consts.VALID_PYLUPDATE_OPTIONS):
        if isinstance(options, str):
            return "-" in options
        elif isinstance(options, (list, tuple)):
            if valid_options:
                return all(option in valid_options for option in options)     
            return all("-" in option.lower() for option in options)    

        raise exceptions.InvalidOptions(f"Invalid options found.")
        
    def _extract_translation_sources(self, ts_file: Path) -> Dict[str, List[str]]:
        """
        Extracts the sources from a Qt translation (.ts) file.
        ### Args:
            ts_file (Path): The path to the Qt translation file. Can be either Path object or str
        ### Returns:
            list
        """
        try:
            tree = ET.parse(ts_file)
        except (OSError, KeyError, AttributeError, ET.ParseError) as e:
            raise exceptions.QALBaseException(
                f"Error durante el proceso de extracción de las fuentes del archivo: {ts_file}. Detailed error: {e}"
            ) from e
        
        root = tree.getroot()
        d = {}
        for message_elem in root.findall('.//message'):
            source = message_elem.find('source').text                                                   # siempre va a existir, nunca será None
            lines =  [location_elem.get('line') for location_elem in message_elem.findall('location')]  # al menos habrá un elemento <location> dentro de cada <message>
            d[source] = lines
                    
        if self.debug_mode and self.verbose:
           echo(DebugLogs.verbose(f"Sources extracted correctly from file {ts_file}"))
        return d

    def _compose_groups_dict(self, fonts: Dict[str, List[str]]):
        #{group{idx}: {location, source, translation}}
        return {
                f"Group{idx}": {
                    "location": f"line {loc} extracted from '{self.source_file.relative_to(consts.CMD_CWD)}'", 
                    "SOURCE": source, 
                    "TRANSLATION": source
                }
                for idx, (source, loc) in enumerate(fonts.items())
        }
    
    def _create_translatable(self, ts_file: Path):  
        """
        Creates a plain translatable file from a .ts file.

        Args:
            ts_file: The path to the .ts file (Path).
        Returns:
            The path to the created plain translatable file (Path).
        """

        extracted_source_fonts = self._extract_translation_sources(ts_file)  #retorna un diccionario de la forma {source: [lines]}
        name = ts_file.stem+self._TOML_EXT                                   # tanto los translatable files como los translations tienen el mismo nombre  
        composed_path = self.translatables_folder / name                     # name= <locale>.toml
        to_dict_fonts = self._compose_groups_dict(extracted_source_fonts)    # dict[group{idx}: {location:str, source:str, translation:str}]
        
        try:
            with helpers.safe_open(composed_path, mode="w", encoding="utf-8") as file_:  
                file_.write(
                    helpers.fit_string(consts.TRANSLATABLE_HEADER_DEFINITION, 80,  preffix="#", as_generator=True)
                )
                file_.write(pytomlpp.dumps(to_dict_fonts))
                
        except (ValueError, OSError) as e:
            raise exceptions.TOMLConversionException(
                f"Unexpected error during the creation of translatable file for {ts_file}. Detailed error: {e}"
            ) from e
        
        if self.debug_mode and self.verbose:
           echo(DebugLogs.verbose(f"Translatable file created correctly from {ts_file}"))
        return composed_path   
        
    def _translatable2list(self, file_: Path) -> List[str]: 
        """
        Extract translations from translatable file

        ### Args:
            file_: The path to the plain text file to be converted.
        ### Returns:
            A list of strings, where each string represents a line in the plain text file.
        ### Raises:
            TOMLConversionException: Error during handling TOML files
        """
        try:
            file_data = pytomlpp.load(file_)      
        except (ValueError, OSError) as e:
            raise exceptions.TOMLConversionException(f"Unexpected error during loading the file {file_!r}. Detailed error: {e}") from e
        
        t =  [
            group_data.get('TRANSLATION', '') 
            for group_data in file_data.values()
        ]
    
        if self.debug_mode and self.verbose:
           echo(DebugLogs.verbose(f"Correctly created list with sources of translatable file {file_}"))

        return t

    def _insert_translations_to_translatable(self, content: List[str], file_: Path):
                
        data = pytomlpp.load(file_)     # dict[group{idx}: {location, source, translation}]
        for items, translation in zip(data.values(), content):      # number of items in content must match with the number of groups, and then translations.
            items["TRANSLATION"] = translation
            
        pytomlpp.dump(data, file_)
        
    def _insert_translated_sources(self, ts_file: Path, translatable_file: Path):
        """
        Insert translated sources into a Qt translation source file (.ts).

        ### Args:
            ts_file (str): The path to the Qt translation source file (.ts)
            translatable_file (str): The path to the file containing the translated sources.
        ### Raises:
            ValueError: If the number of translations does not match the existing translations in the .ts file.
            Exception: If there is an error processing the file.
        ### Returns:
            None
        """     
        try:
            self._process_insertion_from_source(ts_file, translatable_file)        # Extract method here. We are NEVER NESTER DEVELOPER
        except (ValueError, OSError) as e:
            raise exceptions.TranslationFailed(f"No se pudo insertar las sources desde {ts_file}. Detailed error: {e}") from e
            
        if self.debug_mode and self.verbose:
           echo(DebugLogs.verbose(f"Fuentes de {translatable_file} insertadas correctamente en {ts_file}"))

    def _process_insertion_from_source(self, ts_file, translatable_file):   #! Esto solo sirve para .ts de PySide6 (version 6.5-6.6)
        """
        Processes a .ts file by updating the translations based in sources contanined in translatable_file.
        Args:
            ts_file (str): The path to the .ts file to be processed. (To update <translation> with source)
            translatable_file (str): The path to the translatable file.
        Raises:
            ValueError: If the number of translations in the .ts file does not match the number of translations in the translatable file.
        Returns:
            None
            
        ``NOTE: Method that is called only in _insert_translated_sources()``
        """
        tree = ET.parse(ts_file)
        root = tree.getroot()
        current_translations = root.findall(".//message/translation")
        translations_list = self._translatable2list(translatable_file)
        if len(current_translations) != len(translations_list):                              #verify the number of translations are equal in translations_list and current
            raise exceptions.TranslationFailed(
                    "The number of sources in the translatable does not match the number of sources in the translation file. \n"
                    "NOTE: If the translatables have been translated manually, it is possible that some sources have been deleted or two sources have been joined in one line."
                )
            
        for idx, translation_tag in enumerate(current_translations):
            translation_tag.set("type", "Finished")                                      # Cambiar el atributo a type="finished" (se puede obviar)
            translation_tag.text = translations_list[idx]
        tree.write(ts_file, encoding="utf-8", xml_declaration=True)                        

    def _make_qm_file(self,  ts_file: Path, options: List = None) -> None: #ts_file can be Path
        """
        Generate a Qt translation file (.qm) from a Qt translation source file (.ts).

        ### Args:
            ts_file (str): The path to the Qt translation source file (.ts).
            options (list, optional): Additional options to be passed to the pyside6-lrelease command. Defaults to None.
        ### Raises:
            AssertionError: If any option in the options list is not a string or does not start with "--".
        ### Returns:
            None
        """
    
        if options is not None and not self._validate_options(options):
            raise exceptions.InvalidOptions("Invalid options passed to pyside6-lrelease.")
        
        name = ts_file.stem+self._QM_EXT
        final_path = self.translations_folder / name
        
        command = [
            "pyside6-lrelease", " ".join(options), str(ts_file), "-qm", str(final_path)
        ] if options is not None else [
            "pyside6-lrelease", str(ts_file), "-qm", str(final_path)
        ] 
       
        try:
            subprocess.check_output(command, text=True)
        except subprocess.CalledProcessError as e:
            raise exceptions.CompilationError(f"No se pudo crear el binario por un error con subprocess. Detailed error: {e.stdout}") from e
            
        if self.debug_mode and self.verbose:
           echo(DebugLogs.verbose(f"Binario realizado correctamente en {final_path}."))
    
 
    #& ----------  PUBLIC FUNCTIONS  ------------         
    def create_reference_file(self, options: Optional[List[str]] = None):
        """
        Creates the .ts of the ``default_language`` parameter using ``pyside6-lupdate``. 
        The file created will be token as a reference to make the .ts of each lang in ``available_languages``

        Args:
            options: Optional list of options to pass to `pyside6-lupdate` command (list).
        Raises:
            TypeError: If the options list is invalid.
            OSError: If there is an error during the creation of the .ts reference file.
        Returns:
            None
        """
        if options is not None and not self._validate_options(options):
            raise exceptions.InvalidOptions("Invalid options passed to pyside6-lupdate")

        command = [
            "pyside6-lupdate",
            options,      
            str(self.source_file),
            "-ts",
            str(self._ts_reference_file)
        ] if options is not None else [
            "pyside6-lupdate",    
            str(self.source_file),
            "-ts",
            str(self._ts_reference_file)
        ]

        try:
            subprocess.check_output(command, text=True)
        except subprocess.CalledProcessError as e:
            raise exceptions.CompilationError(
                f"Error durante la creación del .ts de referencia {self._ts_reference_file}. Detailed error: {e.stdout}"
            ) from e

        if self.debug_mode:
            echo(DebugLogs.info(f"Archivo de referencia de traducción creado correctamente en: {self._ts_reference_file}."))
    
    def create_translation_files_from_langs(self):
        for lang in self.available_languages:
            name = lang.lower() + self._TS_EXT       # <locale>.ts
            ts_path = self.source_files_folder / name
            try:
                shutil.copy(self._ts_reference_file, ts_path)
            except OSError as e:
                raise exceptions.QALBaseException(
                    f"Unable to create .ts for {ts_path}; Check if _create_reference_file() was called to initialize the ts reference file.\n Detailed Error: {e}"
                ) from e
            
            self.map[lang].insert(0, ts_path)   # entramos a la key=locale (ya creada) y guardamos en idx 0 del mapping
        if self.debug_mode: 
            echo(DebugLogs.info(f"Translation files created correctly from {self._ts_reference_file} in {self.source_files_folder}"))
            
    def create_translatables_from_locales(self):
        #? Podemos crear también los translatables con los translation files también; Ya están creados.
        for lang in self.available_languages:
            if not self.map[lang]:          # Aún no se ha creado los archivos (lista vacia). Suele pasar cuando se llama manualmente al método
                raise exceptions.QALBaseException("Call create_translation_files_from_langs() method to create translation files first.")
            
            ts_file = self.map[lang][0]         # cogemos el Path del translation file ya creado a partir del locale ubicado en idx 0
            toml_file = self._create_translatable(ts_file)   #los tsf se crean con el ts de cada locale, que por ahora son solo copias con el locale <defaut_locale>
            self.map[lang].insert(1, toml_file)       # guardamos el path en el idx1
        
        if self.debug_mode: 
           echo(DebugLogs.info(f"Translatable files created created correctly in {self.translatables_folder}"))
    
    def insert_translated_sources(self):
        for ts_file, tsf_file in self.map.values():
            if not ts_file or not tsf_file:         # Aún no se ha creado los archivos. Suele pasar cuando se llama manualmente al método
                raise DebugLogs.error(
                    "Translation files have not been created yet. Call create_translation_files_from_langs() and create_translatables_from_locales() in this order."
                )
            
            self._insert_translated_sources(ts_file, tsf_file)
            
        if self.debug_mode: 
           echo(DebugLogs.info(f"Translatables inserted corretly in ts files from {self.translatables_folder}"))
            
    def translate_translatables(self, never_fail: bool = True):
        
        to_translate = self._translatable2list(self.map[self.available_languages[0]][1])    # Tomamos el texto del .toml (idx 1) del primer lenguaje disponible puesto que el texto a traducir es el mismo.
        
        for lang, paths in self.map.items():
            try:
                result = self.translator.translate_batch(
                    batch=to_translate,
                    target_lang=lang, 
                    source_lang=self.default_language, 
                    fast_translation=True, 
                    never_fail=never_fail
                )
            except Exception as e:
                raise exceptions.QALBaseException("Unexpected error thrown while translating translatables") from e
        
            self._insert_translations_to_translatable(result, paths[1])    # el resultado del texto, el Path del archivo .toml
        
        if self.debug_mode:
            echo(DebugLogs.info(f"Translatables translated with sucess contained in {self.translatables_folder}"))
        
    def make_qm_files(self, options: List = None):    
        for files in self.map.values():
            ts_file = files[0]
            self._make_qm_file(ts_file, options)
            
        if self.debug_mode:
           echo(DebugLogs.info("Binarios realizados correctamente"))
        
    def build(self, with_progress_bar: bool = False):
        """Call all the public methods to make a build.
        If ``clean_build`` is set to True, all directories used to make the build will be removed except the one that contains the binaries.
        """
        if self._build_done:
            raise exceptions.QALBaseException("Build has been done before. Use restore() or update() functions instead.")
        
        echo(DebugLogs.info("Preparing build..."))

        try:
            if with_progress_bar:
                return self.run_build_with_bar()
            self._run_build()
        except KeyboardInterrupt as e:
            self.restore()          # elimina todos los archivos o directorios creados por build, aparte de limpiar el diccionario.
            raise exceptions.QALBaseException("Build stoped") from e 
        except exceptions.QALBaseException as e:
            self.restore()          # elimina todos los archivos o directorios creados por build, aparte de limpiar el diccionario.
            raise exceptions.QALBaseException(f"Something went wrong during the build. Detailed error: {e}") from e

    def _run_build(self):
        """Method that calls all QAutoLinguist methods to run the build"""
        self._build_done = True
        self.create_reference_file()                
        self.create_translation_files_from_langs()         
        self.create_translatables_from_locales()          
        self.translate_translatables()
        if self.revise_after_build:
            echo(
                DebugLogs.warning(
                "Build completed with sucess.\n CAUTION: The build is incomplete, manually translates and modifies the .tsf and calls the .compose_qm_files() method"
                )
            )
            # se podría hacer una copia de seguridad de los archivos (Temporal) por si el usuario la caga
        else:
            self.compose_qm_files()
            if self.clean:
                self._sanitize_after_build()
                
    def _sanitize_after_build(self):
        """Elimina todos directorios creados durante la build menos el que contiene los .qm.
        NOTE: Se eliminarán de manera permanente el ``source_files_folder`` y ``translatables_folder``
        """
        shutil.rmtree(self.source_files_folder)    
        shutil.rmtree(self.translatables_folder)                  
    
    @classmethod
    def compose_qm_files(cls):
        """Crea los binarios de partir de los .ts ya creados. ``Usar este método cuando se han modificado los translatables, usualmente, de forma manual.``
        Esta función llamará a ``insert_translated_sources()`` y ``make_qm_files()``
        """
        cls.insert_translated_sources()
        cls.make_qm_files()

    def restore(self):
        """Borra todo el proceso hecho por .build()
        NOTA: Este método solo podrá llamarse si se ha llamado previamente el método build()
        """
        self.reinitiaze()       # Borra el diccionario que contiene las rutas por si build es llamado de nuevo. reinitialize NO BORRA LOS DIRECTORIOS
     
        master_parent = self.translations_folder.resolve(True)

        if self.source_files_folder.parent != master_parent:
            shutil.rmtree(self.source_files_folder.resolve(True))
        if self.translatables_folder != master_parent:
            shutil.rmtree(self.translatables_folder.resolve(True))
        else:
            shutil.rmtree(master_parent)
    
    def reinitiaze(self):
        "Restaura el diccionario que contiene las rutas y eliminando todos los archivos creados PERO NO LOS DIRECTORIOS."
        self.map = {locale: [] for locale in self.available_languages}      # overwritting new one; Fast and easy peasy :)
        self._build_done = False # update _build_done is case was True
        echo(DebugLogs.info("Restored process done sucessfully"))

    def update(self):
        """Elimina todo y vuelve a crear una build. ``Usar este método cuando tienen que ser actualizados los .ts``"""
        if not self._build_done:
            raise exceptions.QALBaseException("Unable to found a build. Create one with build().")
        self.restore()
        self.build()

    
    def run_build_with_bar(self):
        # from tqdm import tqdm
        
        # if self._build_done:
        #     raise exceptions.QALBaseException("Build has been done before. Use restore() or update() functions instead.")
        
        # echo(DebugLogs.info("Preparing build..."))

        # # Obtén el número total de pasos en la tarea
        # total_steps = 5  # Ajusta esto según la cantidad de métodos llamados en _run_build()
        # # Crea una barra de progreso
        # progress_bar = tqdm(total=total_steps, desc="Building", unit="step")
        # # Llama a _run_build() con la barra de progreso
        # self._run_build(progress_bar)
        # ...
        raise NotImplementedError




    
##EOF