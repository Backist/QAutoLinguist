"""
QAutoLinguist - Automatic and user-friendly configurable Translator to internationalize Qt (.ts) proyects though a simple CLI.

=======================================================================
lupdate -- Translation File Generator for Qt Applications
=======================================================================
lupdate is part of Qt's Linguist tool chain and 
can be used as a stand-alone tool to convert translation source file to
XML-based TS file. (Qt Translation file)

Extracts translatable messages from:
    Qt UI files, 
    C++, 
    Java,
    JavaScript/QtScript source code.

Extracted messages are stored in textual translation source files (typically
Qt TS XML). New and modified messages can be merged into existing TS files.

Passing .pro files to lupdate is deprecated.
Use the lupdate-pro tool instead.

--
BASIC SYNTAX:
--
  pyside6-lupdate [OPTIONS] source_file -ts <dst_path>

  source_file:    Source file to search for translatable messages.
  dst_path: Generated translation file location. lupdate will create a file if the localtion doesn-t point to a file

lupdate will take the files with the translation sources and create a TS (XML based) file.



=======================================================================
lrelease -- Qt Translation File Compiler
=======================================================================
lrelease is part of Qt's Linguist tool chain. 
It can be used as a stand-alone tool to convert XML-based translations files in the TS
format into the 'compiled' QM format used by QTranslator objects.

Passing .pro files to lrelease is deprecated.
Use the lrelease-pro tool instead, or use qmake's lrelease.prf
feature.

--
BASIC SYNTAX:
--

  pyside6-lrelease ts_file -qm file.qm

  ts_file:           Translation file (.ts) generated by pyside6-lupdate.
  file.qm:  Compiled binary translation file (.qm).

lrelease will take to .ts file to generate binary translation files (.qm) used by the application.
These binary files are used to provide translation at runtime.
This command will compile the translation file form.ts into the binary file form.qm


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
    :param available_locales: ``A list of languages/locales that your aplication will support. Langs or locales can be put either as <xx_XX> or typing the lang directly (english, spanish, etc).``
    :param default_locale: ``Reference locale, took as a reference to make other translations.``
    :param source_files_folder: ``Folder that contains the .ts files (Qt translation Files). If not specified, a folder will be created in CWD where you put the command.``
    :param translations_folder: ``Folder that contains the .qm file (Final translation files that your app will use). If not specified, a folder will be created in CWD where you put the command.``
    :param translatables_folder: ``Folder that contains the .toml files (editable translation files). If not specified, a folder will be created in CWD where you put the command.``
    :param use_default_on_failure: ``When True, translation reference will be use in case one translation in one language fails. When False a FailedTranslation exception wil be raised.``
    :param revise_after_build: ``Allow to see and edit translated translations in case you want to modify some words or phrases after compile the files.``
    :param clean: ``Removes all runtime directories created (translatables & font_files folders) and keeps the folder that contains the final translations. Essentially a clean build.``
    :param debug_mode: ``Displays information about the state of the build.``
    :param verbose: ``Displays more information about the processes done. DEBUG_MODE must be True to enable that option.``
    """
    
    _TS_EXT                    = ".ts"              #Explicit written extension 
    _TOML_EXT                  = ".toml"            # //
    _QM_EXT                    = ".qm"              # //
    _SOURCE_FILES_FOLDER_NAME  = "qt_font_files"    # static folder names
    _TRANSLATIONS_FOLDER_NAME  = "translations"     # //
    _TRANSLATABLES_FOLDER_NAME = "translatables"    # //
    # SOURCE FILES:         Contain the Qt Translation sources files (.ts files)
    # TRANSLATION FILES:    Contain compiled final-use translation files (.qm files)
    # TRANSLATABLE FILES:   Contain .toml files with translation sources. 
    
    
    def __init__(
        self,
        source_file:            Union[str, Path],        # .ui | .py file to search for "tr" funcs
        available_locales:      List[str],               # locales to make a translation file for each one, MUST BE <xx_XX> type locale    
        *,                                               # can be passed the lang in two ways. english or en (language or abreviation)
        default_locale:         str = "en",              # reference locale, took as a reference to make other translations
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
        
        if not available_locales:
            raise ValueError("List is empty.")
        
        # -- validating languages --
        self.translator = Translator()                   # Inicializamos el translator que traducirá las fuentes con una API
        if not self.translator.validate_languages(available_locales):
            raise exceptions.InvalidLanguage("Found invalid or not supported languages in available_locales")
        
        if default_locale in available_locales:
            available_locales = [lang for lang in available_locales if lang != default_locale]     
        elif not self.translator.validate_language(default_locale):
            raise exceptions.InvalidLanguage(f"{default_locale!r} (default-language) is not a supported language or its format is incorrect")
        
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
        
        self.default_locale                    = default_locale
        self.available_locales                 = available_locales 
        self.use_default_on_failure              = use_default_on_failure
        self.revise_after_build                  = revise_after_build
        self.clean                               = clean  
        self.debug_mode                          = debug_mode                                          
        self.verbose                             = verbose     
        
        self._ts_reference_file                  = self.source_files_folder / f"{self.default_locale}{self._TS_EXT}"
        self.map: dict[str, List[Path]]        = {locale: [] for locale in self.available_locales}  
            # mapping para guardar las rutas de los archivos de cada lenguaje
            # dict[language: [font_file (.ts), translatable_file (.toml), qm_file (.qm)]  
            
        self._build_done: bool = False       # Runtime variable to check if a build has done or not since its nessesary to make a
        # instance to build one                      
    
    
    @staticmethod
    def _init_dir(
        loc: Union[str, Path], 
        create_empty: bool = True, 
        mode: int = 751,
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
                loc.mkdir(mode=mode, parents=parents,exist_ok=exist_ok)    # mode = 0o511 -> Requires admin to delete the folder. See UNIX file permissions
            except OSError as e:
                raise exceptions.IOFailure(f"Could not be created directory: {loc}. Detailed error: {e}") from e
            
            return loc.resolve(strict)      # when strict=True raises FileNotFoundError
        
        if loc.exists() and loc.is_dir():
            if consts.IS_POSIX:
                return loc.resolve(strict).as_posix()
            
            return loc.resolve(strict)      # when strict=True raises FileNotFoundError
        
        raise exceptions.RequiredDirError("Expected path must point to a directory")
    
    @staticmethod
    def _init_file(
        loc: Union[str, Path], 
        create_empty: bool = True, 
        mode: int = 751,
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
                loc.touch(mode=mode, exist_ok=exist_ok)   # mode = 0o511 -> Requires admin to delete the folder. See UNIX file permissions
            except OSError as e:
                raise exceptions.IOFailure(f"Could not be created file: {loc}. Detailed error: {e}") from e

            return loc.resolve(strict)      # when strict=True raises FileNotFoundError
        
        if loc.exists() and loc.is_file():
            if consts.IS_POSIX:
                return loc.resolve(strict).as_posix()
            
            return loc.resolve(strict)      # when strict=True raises FileNotFoundError
        
        raise exceptions.RequiredFileError("Expected path must point to a file.")

    
    #& --  INTERNAL FUNCTIONS  --
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
                f"Unexpected error while trying to extract sources from TS file with root {ts_file}. Detailed error: {e}"
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


    def _compose_groups_dict(self, fonts: Dict[str, List[str]]) -> Dict[str, Dict[str, str]]:
        """
        Returns a static mapping with the structure ``dict[Group{idx}: {location, source,translation}]`` to be
        used to create source-translation groups in translatable file.    
        """
        #{group{idx}: {location, source, translation}}
        return {
                f"Group{idx}": {
                    "location": f"line {loc} extracted from '{self.source_file}'", 
                    "SOURCE": source, 
                    "TRANSLATION": source
                }
                for idx, (source, loc) in enumerate(fonts.items())
        }
    

    def _create_translatable(self, ts_file: Path) -> Path:  
        """
        Creates a plain translatable file from a .ts file.

        ### Args:
            @param ts_file: The path to the .ts file (Path).
        ### Raises:
            - ``TOMLConversionError``: Raised when tried to create a TOML file.
        """

        extracted_source_fonts = self._extract_translation_sources(ts_file)  #retorna un diccionario de la forma {source: [lines]}
        name = ts_file.stem+self._TOML_EXT                                   # tanto los translatable files como los translations tienen el mismo nombre  
        composed_path = self.translatables_folder / name                     # name= <locale>.toml
        to_dict_fonts = self._compose_groups_dict(extracted_source_fonts)    # dict[group{idx}: {location:str, source:str, translation:str}]
        
        try:
            with open(composed_path, mode="w") as file_:
                file_.write(
                    helpers.fit_string(consts.TRANSLATABLE_HEADER_DEFINITION, 80,  preffix="#", as_generator=True)
                )
                file_.write(pytomlpp.dumps(to_dict_fonts))
        except (ValueError, OSError) as e:
            raise exceptions.TOMLConversionError(
                f"Unexpected error during the creation of translatable file for {ts_file}. Detailed error: {e}"
            ) from e
        
        if self.debug_mode and self.verbose:
           echo(DebugLogs.verbose(f"Translatable file created correctly from {ts_file}"))
        return composed_path   


    def _translatable2list(self, file_: Path) -> List[str]: 
        """
        Extract translations from translatable file

        ### Args:
            @param file_: The path to the plain text file to be converted.
        ### Raises:
            - ``TOMLConversionError``: Raised when tried to read and process a TOML file.
        """
        try:
            file_data = pytomlpp.load(file_, encoding="utf-8")      
        except (ValueError, OSError) as e:
            raise exceptions.TOMLConversionError(f"Unexpected error during loading the file {file_!r}. Detailed error: {e}") from e
        
        t =  [
            group_data.get('TRANSLATION', '') 
            for group_data in file_data.values()
        ]
    
        if self.debug_mode and self.verbose:
           echo(DebugLogs.verbose(f"Sucessfully created list containing translation sources of TS file -> {file_}"))

        return t


    def _insert_translations_to_translatable(self, content: List[str], file_: Path) -> None:
        """
        Read a valid ``TOML`` file and inserts the new content to the file.
        
        ### Raises:
            - ``ValueError``: If content length does not match to file content length.
        """
        data = pytomlpp.load(file_, encoding="utf-8")     # dict[group{idx}: {location, source, translation}]
        
        if len(data.values()) != len(content):
            raise ValueError("Content length does not match to file content length.")
        
        for items, translation in zip(data.values(), content):      # number of items in content must match with the number of groups, and then translations.
            items["TRANSLATION"] = translation
            
        pytomlpp.dump(data, file_, encoding="utf-8")


    def _insert_translated_sources(self, ts_file: Path, translatable_file: Path) -> None:
        """
        Insert translated sources into a Qt translation source file (.ts).

        ### Args:
            @param ts_file: The path to the Qt translation source file (.ts)
            @param translatable_file: The path to the file containing the translated sources.
            
        ### Raises:
            - ``TranslationFailed``: If the number of translations does not match the existing translations in the .ts file.
        """     
        try:
            self._process_insertion_from_source(ts_file, translatable_file)        # Extract method here. We are NEVER NESTER DEVELOPER
        except (ValueError, OSError) as e:
            raise exceptions.TranslationFailed(f"Unable to insert translated sources of {ts_file} in {translatable_file}. Detailed error: {e}") from e
            
        if self.debug_mode and self.verbose:
           echo(DebugLogs.verbose(f"Sources in {translatable_file} inserted with sucess in {ts_file}"))


    def _process_insertion_from_source(self, ts_file: Path, translatable_file: Path) -> None: 
        """
        Processes a .ts file by updating the translations based in sources contanined in translatable_file.
        
        ### Args:
            @param ts_file: The path to the .ts file to be processed. (To update <translation> with source)
            @param translatable_file: The path to the translatable file.
            
        ### Raises:
            - ``TranslationFailed``: If the number of translations in the .ts file does not match the number of translations in the translatable file.
            
        NOTE: ``Method that is called only in _insert_translated_sources()``
        NOTE: ``The method used only works for Qt6 versions and subversions.``
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


    def _make_qm_file(self,  ts_file: Path, dst_path: Optional[str] = None, options: Optional[List[str]] = None) -> None: 
        """
        Generate a Qt translation file (.qm) from a Qt translation source file (.ts).

        ### Args:
            @param ts_file: The path to the Qt translation source file (.ts).
            @param options: Additional options to be passed to the pyside6-lrelease command. Defaults to None.
            
        ### Raises:
            - ``InvalidOptions``: If any option in the options list is not a string or does not start with "--".
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
            raise exceptions.CompilationError(f"Unable to compile into qm file. Detailed error: {e.stdout}") from None
            
        if self.debug_mode and self.verbose:
           echo(DebugLogs.verbose(f"Compiled qm file sucessfully done at {final_path}."))
    
 
    
    #& ----------  PUBLIC FUNCTIONS  ------------         
    def create_reference_file(self, options: Optional[List[str]] = None) -> None:
        """
        Creates the .ts of the ``default_locale`` parameter using ``pyside6-lupdate``. 
        The file created will be token as a reference to make the .ts of each lang in ``available_locales``

        ### Args:
            @param options: Optional list of options to pass to `pyside6-lupdate` command (list).
            
        ### Raises:
            - ``InvalidOptions``: If the options list is invalid.
            - ``CompilationError``: If there is an error during the creation of the .ts reference file.

        """
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
                f"Unable to create TS reference file located in {self._ts_reference_file}. Detailed error: {e.stdout}"
            ) from None

        if self.debug_mode:
            echo(DebugLogs.info(f"TS file sucessfully created at {self._ts_reference_file}."))
    

    def create_translation_files_from_locales(self) -> None:
        """
        Creates translation files for each available_locale.
        
        ### Raises:
            - `QALBaseException`: When `OSError`.
        """
        for lang in self.available_locales:
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
            echo(DebugLogs.info(f"Translation files created correctly using {self._ts_reference_file}, saved in {self.source_files_folder}"))


    def create_translatables_from_locales(self) -> None:
        #? Podemos crear también los translatables con los translation files también; Ya están creados.
        for lang in self.available_locales:
            if not self.map[lang]:          # Aún no se ha creado los archivos (lista vacia). Suele pasar cuando se llama manualmente al método
                raise exceptions.QALBaseException("Call create_translation_files_from_locales() method to create translation files first.")
            
            ts_file = self.map[lang][0]         # cogemos el Path del translation file ya creado a partir del locale ubicado en idx 0
            toml_file = self._create_translatable(ts_file)   #los tsf se crean con el ts de cada locale, que por ahora son solo copias con el locale <defaut_locale>
            self.map[lang].insert(1, toml_file)       # guardamos el path en el idx1
        
        if self.debug_mode: 
           echo(DebugLogs.info(f"Translatable files created created correctly in {self.translatables_folder}"))
    

    def insert_translated_sources(self) -> None:
        for ts_file, tsf_file in self.map.values():
            if not ts_file or not tsf_file:         # Aún no se ha creado los archivos. Suele pasar cuando se llama manualmente al método
                raise DebugLogs.error(
                    "Translation files have not been created yet. Call create_translation_files_from_locales() and create_translatables_from_locales() in this order."
                )
            
            self._insert_translated_sources(ts_file, tsf_file)
            
        if self.debug_mode: 
           echo(DebugLogs.info(f"Translatables inserted corretly in ts files from {self.translatables_folder}"))


    def translate_translatables(self, never_fail: bool = True) -> None:
        
        to_translate = self._translatable2list(self.map[self.available_locales[0]][1])    # Tomamos el texto del .toml (idx 1) del primer lenguaje disponible puesto que el texto a traducir es el mismo.
        
        for lang, paths in self.map.items():
            try:
                result = self.translator.translate_batch(
                    batch=to_translate,
                    target_lang=lang, 
                    source_lang=self.default_locale, 
                    fast_translation=True, 
                    never_fail=never_fail
                )
            except Exception as e:
                raise exceptions.QALBaseException("Unexpected error thrown while translating translatables") from e
        
            self._insert_translations_to_translatable(result, paths[1])    # el resultado del texto, el Path del archivo .toml
        
        if self.debug_mode:
            echo(DebugLogs.info(f"Translatables translated with sucess contained in {self.translatables_folder}"))


    def make_qm_files(self, options: List = None) -> None:    
        for files in self.map.values():
            ts_file = files[0]
            self._make_qm_file(ts_file, options)
            
        if self.debug_mode:
           echo(DebugLogs.info("Binarios realizados correctamente"))


    def build(self, with_progress_bar: bool = False) -> None:
        """Call all the public methods to make a build.
        If ``clean_build`` is set to True, all directories used to make the build will be removed except the one that contains the binaries.
        """
        if self._build_done:
            raise exceptions.QALBaseException("Build has been done before. Use restore() or update() functions instead.")
        
        echo(DebugLogs.info("Preparing build..."))

        try:
            if with_progress_bar:
                self.run_build_with_bar()
            else:
                self._run_build()
        except KeyboardInterrupt as e:
            self.restore()          # elimina todos los archivos o directorios creados por build, aparte de limpiar el diccionario.
            raise exceptions.QALBaseException("Build stoped") from e 
        except exceptions.QALBaseException as e:
            self.restore()          # elimina todos los archivos o directorios creados por build, aparte de limpiar el diccionario.
            raise exceptions.QALBaseException(f"Something went wrong during the build. Detailed error: {e}") from None


    def _run_build(self) -> None:
        """Method that calls all QAutoLinguist methods to run the build"""
        self._build_done = True
        self.create_reference_file()                
        self.create_translation_files_from_locales()         
        self.create_translatables_from_locales()          
        self.translate_translatables()
        if self.revise_after_build:
            echo(
                DebugLogs.warning(
                "Build completed with sucess.\n CAUTION: The build is incomplete, manually translates and modifies the .tsf and calls the .compose_qm_files() method"
                )
            )
            self._gen_cache()
        else:
            self.insert_translated_sources()
            self.make_qm_files()
            if self.clean:
                self._sanitize_after_build()


    def _sanitize_after_build(self) -> None:
        """Elimina todos directorios creados durante la build menos el que contiene los .qm.
        NOTE: Se eliminarán de manera permanente el ``source_files_folder`` y ``translatables_folder``
        """
        shutil.rmtree(self.source_files_folder)    
        shutil.rmtree(self.translatables_folder)                  
    
    
    @staticmethod
    def compose_qm_files(map: Dict[str, List[str]], config: Dict) -> None:
        """Crea los binarios de partir de los .ts ya creados. ``Usar este método cuando se han modificado los translatables, usualmente, de forma manual.``
        Esta función llamará a ``insert_translated_sources()`` y ``make_qm_files()``
        """
        ...


    def restore(self) -> None:
        """Borra todo el proceso hecho por .build()
        NOTA: Este método solo podrá llamarse si se ha llamado previamente el método build()
        """
        self.reinitiaze()       # Borra el diccionario que contiene las rutas por si build es llamado de nuevo. reinitialize NO BORRA LOS DIRECTORIOS

        master_parent = self.translations_folder

        if self.source_files_folder.parent != master_parent:
            shutil.rmtree(self.source_files_folder)
        if self.translatables_folder.parent != master_parent:
            shutil.rmtree(self.translatables_folder)
        else:
            shutil.rmtree(master_parent)
    

    def reinitiaze(self) -> None:
        "Restaura el diccionario que contiene las rutas y eliminando todos los archivos creados PERO NO LOS DIRECTORIOS."
        self.map = {locale: [] for locale in self.available_locales}      # overwritting new one; Fast and easy peasy :)
        self._build_done = False # update _build_done is case was True
        echo(DebugLogs.info("Restored mappings with sucess"))


    def update(self) -> None:
        """Elimina todo y vuelve a crear una build. ``Usar este método cuando tienen que ser actualizados los .ts``"""
        if not self._build_done:
            raise exceptions.QALBaseException("Unable to found a build. Create one with build().")
        self.restore()
        self.build()


    def run_build_with_bar(self) -> None:
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


    def _gen_cache(self):
        "Experimental cache implementation that enables with user wants to revise translatables."
        
        from json import dump

        cache_data = {}
        config_data = {
            "debug": self.debug_mode,
            "verbose": self.verbose,
        }

        for lang, paths in self.map.items():
            paths_ = [str(path) for path in paths]
            cache_data[lang] = paths_

        cache_path = consts.CMD_CWD / ".qal_cache"
        cache_path.mkdir(exist_ok=True)
    
        with open(cache_path / "nodes", mode="w", encoding="utf-8") as fp:
            dump(cache_data, fp, indent=4)
        
        with open(cache_path / "config", mode="w", encoding="utf-8") as fp:
            dump(config_data, fp, indent=4)
        
         
#;EOF