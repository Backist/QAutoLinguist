from pathlib import Path 

#--  Common paths --
# Para manejar recursos del paquete, mirar https://importlib-resources.readthedocs.io/en/latest/using.html
# https://docs.python.org/3/library/importlib.resources.html#module-importlib.resources
# Ya que cuando se empaqueta el proyecto, __file__ no va a estar devolviendo la ruta del archivo, sino la ruta canónica del sistema de archivos.
CMD_CWD = Path().resolve()
RUNTIME_ROOT = Path(__file__).parent.resolve()   # cuando se crea un ZIP o ejecutable esto puede no ser correcto.

#-- Config shared consts and paths --
CONFIG_FILENAME = ".qal_config.ini" 
PARAM_DECLS_RESOURCE = "qautolinguist.static", "config_decls.json" # tupla que contiene el paquete donde se contiene el recurso y el archivo


# lrelease options (version: 6.5.3):
#     -idbased
#            Use IDs instead of source strings for message keying
#     -compress
#            Compress the QM files
#     -nounfinished
#            Do not include unfinished translations
#     -removeidentical
#            If the translated text is the same as
#            the source text, do not include the message
#     -markuntranslated <prefix>
#            If a message has no real translation, use the source text
#            prefixed with the given string instead
#     -project <filename>
#            Name of a file containing the project's description in JSON format.
#            Such a file may be generated from a .pro file using the lprodump tool.
#     -silent
#            Do not explain what is being done
#     -version
#            Display the version of lrelease and exit


# lupdate options (version: 6.5.3):
#     -no-obsolete
#            Drop all obsolete and vanished strings.
#     -extensions <ext>[,<ext>]...
#            Process files with the given extensions only.
#            The extension list must be separated with commas, not with whitespace.
#            Default: 'java,jui,ui,c,c++,cc,cpp,cxx,ch,h,h++,hh,hpp,hxx,js,qs,qml,qrc'.
#     -pluralonly
#            Only include plural form messages.
#     -silent
#            Do not explain what is being done.
#     -no-sort
#            Do not sort contexts in TS files.
#     -no-recursive
#            Do not recursively scan directories.
#     -recursive
#            Recursively scan directories (default).
#     -I <includepath> or -I<includepath>
#            Additional location to look for include files.
#            May be specified multiple times.
#     -locations {absolute|relative|none}
#            Specify/override how source code references are saved in TS files.
#            absolute: Source file path is relative to target file. Absolute line
#                      number is stored.
#            relative: Source file path is relative to target file. Line number is
#                      relative to other entries in the same source file.
#            none: no information about source location is stored.
#            Guessed from existing TS files if not specified.
#            Default is absolute for new files.
#     -no-ui-lines
#            Do not record line numbers in references to UI files.
#     -disable-heuristic {sametext|similartext}
#            Disable the named merge heuristic. Can be specified multiple times.
#     -project <filename>
#            Name of a file containing the project's description in JSON format.
#            Such a file may be generated from a .pro file using the lprodump tool.
#     -pro <filename>
#            Name of a .pro file. Useful for files with .pro file syntax but
#            different file suffix. Projects are recursed into and merged.
#            This option is deprecated. Use the lupdate-pro tool instead.
#     -pro-out <directory>
#            Virtual output directory for processing subsequent .pro files.
#     -pro-debug
#            Trace processing .pro files. Specify twice for more verbosity.
#     -source-language <language>[_<region>]
#            Specify the language of the source strings for new files.
#            Defaults to POSIX if not specified.
#     -target-language <language>[_<region>]
#            Specify the language of the translations for new files.
#            Guessed from the file name if not specified.
#     -tr-function-alias <function>{+=,=}<alias>[,<function>{+=,=}<alias>]...
#            With +=, recognize <alias> as an alternative spelling of <function>.
#            With  =, recognize <alias> as the only spelling of <function>.
#            Available <function>s (with their currently defined aliases) are:
#              Q_DECLARE_TR_FUNCTIONS (=Q_DECLARE_TR_FUNCTIONS)
#              QT_TR_N_NOOP (=QT_TR_N_NOOP)
#              QT_TRID_N_NOOP (=QT_TRID_N_NOOP)
#              QT_TRANSLATE_N_NOOP (=QT_TRANSLATE_N_NOOP)
#              QT_TRANSLATE_N_NOOP3 (=QT_TRANSLATE_N_NOOP3)
#              QT_TR_NOOP (=QT_TR_NOOP)
#              QT_TRID_NOOP (=QT_TRID_NOOP)
#              QT_TRANSLATE_NOOP (=QT_TRANSLATE_NOOP)
#              QT_TRANSLATE_NOOP3 (=QT_TRANSLATE_NOOP3)
#              QT_TR_NOOP_UTF8 (=QT_TR_NOOP_UTF8)
#              QT_TRANSLATE_NOOP_UTF8 (=QT_TRANSLATE_NOOP_UTF8)
#              QT_TRANSLATE_NOOP3_UTF8 (=QT_TRANSLATE_NOOP3_UTF8)
#              findMessage (=findMessage)
#              qtTrId (=qtTrId)
#              tr (=tr)
#              trUtf8 (=trUtf8)
#              translate (=translate)
#              qsTr (=qsTr)
#              qsTrId (=qsTrId)
#              qsTranslate (=qsTranslate)
#     -ts <ts-file>...
#            Specify the output file(s). This will override the TRANSLATIONS.
#     -version
#            Display the version of lupdate and exit.
#     -clang-parser [compilation-database-dir]
#            Use clang to parse cpp files. Otherwise a custom parser is used.
#            This option needs a clang compilation database (compile_commands.json)
#            for the files that needs to be parsed.
#            The path to the directory containing this file can be specified on the
#            command line, directly after the -clang-parser option, or in the .pro file
#            by setting the variable LUPDATE_COMPILE_COMMANDS_PATH.
#            A directory specified on the command line takes precedence.
#            If no path is given, the compilation database will be searched
#            in all parent paths of the first input file.
#     -project-roots <directory>...
#            Specify one or more project root directories.
#            Only files below a project root are considered for translation when using
#            the -clang-parser option.
#     @lst-file
#            Read additional file names (one per line) or includepaths (one per
#            line, and prefixed with -I) from lst-file.




     