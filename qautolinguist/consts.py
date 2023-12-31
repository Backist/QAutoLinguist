from pathlib import Path 
#from dataclasses import dataclass





#========================  COMMON PATHS AND FILENAMES (common paths) ==================
CMD_CWD         = Path().resolve()
RUNTIME_FOLDER  = Path(__file__).parent.resolve()
#======================================================================================



#========================  TEMPLATES AND HEADERS (used to build config file) ==================
CONFIG_FILENAME: str = ".qal-config.ini"  #filename convention to .ini user-editable file

INI_FILE_TEMPLATE = """
# =============================   QAutoLinguist Configuration File    =====================================
# This file is auto-generated by qautolinguist.Config .
# If you are not very familiar with the configuration file format, 
# just fill in the fields in the "Required" section. 
# Be cautious when placing values.
# Take these measures:
# 1. Do not use "" or '' to specify text strings, even if you want to specify paths containing spaces;
#      the parser parses them internally; it will cause an error if you do.
# 2. This format uses empty lines to detect braces and attributes. 
#      If you have to specify multi-line values, increase the indentation for each new line.
# ===============================================================================

[Required]
{source_file_comment}
{source_file}= {source_file_value} 

{default_language_comment}
{default_language}= {default_language_value}   

{available_languages_comment}
{available_languages}= {available_languages_value}


# =============================   OPTIONALS    =====================================
# Usually you will not need to edit this section.
# Here you can adjust where the generated files are saved and some settings to
# handle the behaviour of the QAutoLinguist
# ==================================================================================

[Optionals]
{translations_folder_comment}
{translations_folder}= {translations_folder_value}

{source_files_folder_comment}
{source_files_folder}= {source_files_folder_value}
     
{translatables_folder_comment}
{translatables_folder}= {translatables_folder_value}
        
{use_default_on_failure_comment}
{use_default_on_failure}= {use_default_on_failure_value}     

{revise_after_build_comment}
{revise_after_build}= {revise_after_build_value}      

{clean_comment}
{clean}= {clean_value}            

{debug_mode_comment}
{debug_mode}= {debug_mode_value}               

{verbose_comment}
{verbose}= {verbose_value}   


# =============================   INTERNAL    ====================================================
# Section containing special values and attributes for the correct functioning of QAutoLinguist. 
# Any changes to these values will prevent QAutoLinguist from working properly.
# ================================================================================================

"""

TRANSLATABLE_HEADER_DEFINITION: str = (
    "This file is auto-generated by TsfComposer. "
    "It contains the translation sources of the .ts files (translation files); "
    "each line is a unique translation. "
    "Please, if you are going to review or modify its content, do it with caution, "
    "any unwanted modification will affect the creation of the binaries.\n\n"
)
#=================================================================================================

PARAMS_DESCRIPTION = {
    'source_file': '.ui or .py file to search for "tr" funcs.', 
    'available_languages': 'A list of languages/locales that your aplication will support. Langs or locales can be put either as <xx_XX> or typing the lang directly (english, spanish, etc).', 'default_language': 'Reference locale, took as a reference to make other translations.', 
    'source_files_folder': 'Folder that contains the .ts files (Qt translation Files). If not specified, a folder will be created in CWD where you put the command.', 
    'translations_folder': 'Folder that contains the .qm files (Final translation files that your app will use). If not specified, a folder will be created in CWD where you put the command.', 
    'translatables_folder': 'Folder that contains the .toml files (editable translation files). If not specified, a folder will be created in CWD where you put the command.', 
    'use_default_on_failure': 'When True, translation reference will be use in case one translation in one language fails. When False a FailedTranslation exception wil be raised.', 
    'revise_after_build': 'Allow to see and edit translated translations in case you want to modify some words or phrases after compile the files.', 
    'clean': 'Removes all runtime directories created (translatables & font_files folders) and keeps the folder that contains the final translations. Essentially a clean build.', 
    'debug_mode': 'Displays information about the state of the build.', 
    'verbose': 'Displays more information about the processes done. DEBUG_MODE must be True to enable that option.'
}

VALID_PYLUPDATE_OPTIONS = [
    ""
]
VALID_PYLRELEASE_OPTIONS = [
    ""
]


# @dataclass(init=False, repr=False, eq=False)
# class ConfigSectionDefinitions: 
#     """
#     Class that contains the definitions for each section in .INI file.
#     For now, we are using a ``consts.INI_FILE_TEMPLATE`` and this class is not used, but maintained just in case to switch to make .ini with dict
#     """
#     CONFIG_HEADER_DEFINITION: str = (
#         "================================    HEADER    =============================================\n"
#         "This file is auto-generated by qautolinguist.\n"
#         "Use caution when modifying this file and only modify or fill in the requested attributes.\n"
#         "Any unauthorised or improper modification may cause qautolinguist to malfunction.\n"
#         "==========================================================================================\n"
#     )
    
#     CONFIG_OPTIONALS_HEADER: str = (
#         "=============================   OPTIONALS    =====================================\n"
#         "Usually you will not need to edit this section.\n"
#         "Here you can adjust where the generated files are saved and some settings to\n"
#         "handle the behaviour of the QAutoLinguist\n"
#         "==================================================================================\n"
#     )
    
#     CONFIG_INTERNAL_HEADER : str = (
#         "=============================   INTERNAL    =====================================================\n"
#         "Section containing special values and attributes for the correct functioning of QAutoLinguist.\n" 
#         "Any changes to these values will prevent QAutoLinguist from working properly.\n"
#         "=================================================================================================\n"
#     )