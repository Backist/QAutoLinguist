_This project uses [semantic versioning](https://semver.org/)_
<br>

📖 **README version:** _0.1.1_

![GitHub issues](https://img.shields.io/github/issues/Backist/QAutoLinguist?style=for-the-badge)
![GitHub closed issues](https://img.shields.io/github/issues-closed/Backist/QAutoLinguist?style=for-the-badge)
![GitHub License](https://img.shields.io/github/license/Backist/QAutoLinguist?style=for-the-badge)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Backist/QAutoLinguist?style=for-the-badge)
![Static Badge](https://img.shields.io/badge/python-3.7_%7C_3.8_%7C_3.9_%7C_3.10_%7C_3.11-blue?style=for-the-badge)


# 🏷️ QAutoLinguist

QAutoLinguist is a CLI with the aim to **automate**, **manage** and **facilitate** the process of internationalising a _Qt_ application through an easy-to-use CLI. 
the internationalisation process of a Qt_application through an easy-to-use CLI.
QAutoLinguist offers a simple and user-friendly approach to translate your application into other languages automatically using the ``Google Translator API`` by default. 

### Why use QAutoLinguist and not Qt Linguist?
The Qt development environment offers a tool designed to facilitate the translation of Qt applications that use the Qt internationalisation system (i18n)
internationalisation system, namely [Qt Linguist](https://doc.qt.io/qt-5/qtlinguist-index.html), which provides a GUI for performing translations.

In many occasions, using this tool provided by Qt may be a very professional or complex option, 
as it is a highly customisable program with various parameters and can be a somewhat tedious option for small to medium sized projects that are simply
small or medium-sized projects that simply want to be able to simply translate their application into other languages.

Therefore, QAutoLinguist proposes a simple and fast way, based on a CLI, to internationalise your Qt application without the need of previous knowledge of the translation system.
knowledge of the Qt translation system and with the advantage of not having to install a separate program to perform this task.

<br>

## 💡 When to use QAutoLinguist:
- [x] Fast internationalisation for any language in the world (133 available) quickly and without performing any tasks.
- [x] Compatible with the entire ``Qt`` environment.
- [x] No previous experience or documentation required.
- [x] Ability to use your favourite translator, such as ``Deepl``, ``MicrosoftTranslator`` or ``MyMemoryTranslator`` to perform your translations automatically.
- [x] Region support.
- [x] Review and modification of translations before compilation.
- [ ] *Guarantees (partially) accurated translations.
- [ ] Need to work with translation files other than ``.ts``.
- [ ] Supports disambiguation
- [ ] Plurality and gender management
- [ ] Supports context editing or modification.
- [ ] Translation suggestions

> __*__ QAutoLinguist gives the possibility to modify the automatic translations before they are compiled.

> [!NOTE]
> QAutoLinguist is not a professional solution or intended to provide all the flexibility and customisation that Qt Linguist can offer.
> If your Qt application requires contextualisation, plural translations or disambiguations, it is recommended that you use the tool provided by Qt.

<br>

## ⚙️ How QAutoLinguist do the process
Regarding the automation process, as a summary, it creates the translation files ``.ts`` for each language and from them the fonts are extracted to introduce them 
in a more user-friendly syntax file, ``TOML``, created with the intention of providing the user with a view of the source and the translation made by the user. 
files with a more user-friendly syntax, ``TOML``, created with the intention of providing the user with a view of the source and the translation made by 
the third-party translator so that the translations, despite being automatic, are as accurate as possible.
Once the sources are translated, they are extracted from the ``TOML`` to be inserted into the .ts and compiled into the translation file to be used, the .qm (compiled files).

<br>

## 🛠️ Use:
QAutoLinguist is based on a ``.ini`` configuration file where you specify the parameters needed to perform the translations.
In general cases this is what you are looking for:
If you have specified to include QAutoLinguist in the PATH environment variable:

1. **Initialize the configuration file**:
This command will create a configuration file in the command run CWD with the name ``.qal-config.ini`` by default, unless ``[<config_file_name>]``
is specified.
You can see the configuration file structure below.

  ```bash
  >>> qautolinguist build init [<config_file_name>]                # UNIX
  >>> python3 -m qautolinguist build init  [<config_file_name>]    # POSIX
  ```
  
2. **Complete the configuration file**:
Once the configuration file is created, fill in the required parameters to perform the translations.

3. **Create the build**:
Once the configuration file is correctly filled in, the only thing left to do is to start the translation process.
Specify ``[<config_path>]`` if you are in a different directory than the one used to create the configuration file or you have set a different name than the default one.

  ```bash
  >>> qautolinguist build run [<config_path>]              # UNIX
  >>> python3 -m qautolinguist build run [<config_path>]   # POSIX
  ```

<br>

## Rebuilds and Isolated cases

#### CASE 1: If you want to change or touch up some translation (.toml files):
- ``Simply recreate the binaries:```
```bash
    # If <config_file_path> is not specified, CWD will be searched for a TOML file named [.config.toml].
    # If the file is missing
    >>> qautolinguist rebuild bundles [<config_file_path>] # UNIX
    >>> python3 -m qautolinguist rebuild bundles [<config_file_path>] # POSIX
    # if the configuration file is not in the directory where the command is executed, specify its path
```

#### CASE 2: If the application sources have been modified:
- ``You need to create a new build.
    Be sure to change the .config.toml if you want to change any parameters for this new build.

#### CASE 3: If you want to create a new build for another application:
- ``If a build already exists in the working directory:``` ```.
```bash
>>> qautolinguist build -new [<config_file_name>] # windows
<config_file_name> CANNOT be the SAME as another config file.
>>> python3 -m qautolinguist build -new [<config_file_path>] # linux
```

> [!IMPORTANT]
> Caso 3 no disponible por ahora.

<br>

## Configuration file
Regarding the ``.config.toml`` that is generated when you run ``**qautotranslator build init**``.
It will look something like this:

> [!TIP]
> **If you are looking for a quick and easy build, just fill in the required parameters in [REQUIRED]**.

```ini
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
# ========================================================================================================

[Required]
# .ui or .py file to search for "tr" funcs.
source_file= 

# Reference locale, took as a reference to make other translations.
default_language= en   

# A list of languages/locales that your aplication will support. Langs or loc
# ales can be put either as <xx_XX> or typing the lang directly (english, spa
# nish, etc) or its acronym.
available_languages= []


# =============================   OPTIONALS    =====================================
# Usually you will not need to edit this section.
# Here you can adjust where the generated files are saved and some settings to
# handle the behaviour of the QAutoLinguist
# ==================================================================================

[Optionals]
# Folder that contains the .qm files (Final translation files that your app w
# ill use). If not specified, a folder will be created in CWD where you put t
# he command.
translations_folder= 

# Folder that contains the .ts files (Qt translation Files). If not specified
# , a folder will be created in CWD where you put the command.
source_files_folder= 
     
# Folder that contains the .toml files (editable translation files). If not s
# pecified, a folder will be created in CWD where you put the command.
translatables_folder= 
        
# When True, translation reference will be use in case one translation in one
#  language fails. When False a FailedTranslation exception wil be raised.
use_default_on_failure= true     

# Allow to see and edit translated translations in case you want to modify so
# me words or phrases after compile the files.
revise_after_build= false      

# Removes all runtime directories created (translatables & font_files folders
# ) and keeps the folder that contains the final translations. Essentially a 
# clean build.
clean= true            

# Displays information about the state of the build.
debug_mode= true               

# Displays more information about the processes done. DEBUG_MODE must be True
#  to enable that option.
verbose= true   


# =============================   INTERNAL    ====================================================
# Section containing special values and attributes for the correct functioning of QAutoLinguist. 
# Any changes to these values will prevent QAutoLinguist from working properly.
# ================================================================================================

[Internal]
# 
cwd = <COMMAND_CWD>  

```


