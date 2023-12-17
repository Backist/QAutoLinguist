# Funcionamiento/Idea de ejecuccion:

## En casos generales esto es lo que estás buscando:
#### Si se ha especificado incluir QAutoLinguist en la variable de entorno PATH:
  - **Windows**:
    ```bash
    #Crea un .config.toml en CWD 
    #Si no se especifica un nombre, por defecto se crea un archivo [.config.toml] en CWD para poder introducir los atributos para hacer la build.
    >>> qautolinguist build -init [<config_file_name>]   
    >>> qautolinguist build [<config_file_path>]         
    # si el archivo de configuracion no esta en el directorio donde se ejecuta el comando, especificar su ruta
    # se buscara un archivo .config.toml en CWD si no se especifica su ruta.
    ```

  - **Linux**:
    ```bash
    >>> python3 -m qautolinguist build -init  [<config_file_name>]
    >>> python3 -m qautolinguist build [<config_file_path>]
    ```

## Modificaciones o rebuilds
#### CASO 1: Si se desea cambiar o retocar alguna traduccion (archivos .toml):
- ``Simplemente volvemos a crear los binarios:``
```bash
    # Si no se especifica <config_file_path>, se buscará en CWD un archivo TOML con nombre [.config.toml]
    # Si el archivo no está
    >>> qautolinguist build -bundles  [<config_file_path>]           # windows
    >>> python3 -m qautolinguist build -bundles [<config_file_path>] # linux
    # si el archivo de configuracion no esta en el directorio donde se ejecuta el comando, especificar su ruta
```
> [!WARNING]
> _Esto creará de nuevo los binarios con los archivos de traduccion retocados._
---
#### CASO 2: Si se han modificado las fuentes de la aplicacion:
- ``Es necesario crear una build nueva.``
    Asegurate de cambiar el .config.toml si deseas cambiar algun parametro para esta build nueva.

> [!WARNING]
> _Crear una build cuando se ha creado otra anteriormente sobreesbirá los archivos ya creados._
---
####  CASO 3: Si se desea crear una build nueva para otra aplicación:
- ``Si ya existe una build en el directorio de trabajo:``
```bash
>>> qautolinguist build --new [<config_file_name>]            # windows
# <config_file_name> NO puede ser IGUAL a otro archivo de configuración.
>>> python3 -m qautolinguist build --new [<config_file_path>] # linux
```
---
> [!IMPORTANT]
> Caso 3 no disponible por ahora.



## Archivo de configuracion :: Vista previa
Respeto al ``.config.toml`` que se genera cuando se ejecuta ``**qautotranslator build -init**``,
se verá algo asi:

> [!TIP]
> **Si buscas una build rapida y sencilla, solo completa los parametros exigidos en [REQUIRED]**

```toml
[Required]

# archivo .ui o el que contiene los tr() o QCoreAplication.Translate
source_file=""  

#lenguaje de referencia, normalmente el de tu aplicación; Por defecto, es inglés. 
#En caso de fallo de traduccion de algun lenguage, se usará el source de este lenguaje.
#Si stop_on_failure en la sección [Optionals] es true, la build será detenida en caso de fallo.
default_language="english"   # tambíen se acepta "en_En" o "en"    

# lenguajes a traducir
available_languages=[

]


# =============================   OPTIONALS    =====================================
# Usualmente no necesitarás editar esta sección.
# Aquí puedes ajustar donde se guardan los archivos generados y algunos ajustes para
# manejar el comportamiento del QAutoLinguist
# ==================================================================================
[Optionals]

#Ubicación del directorio que contiene los binarios finales. 
#Por defecto se crea en CWD 
translations_folder_path=""

#Ruta del directorio que contiene los translation_sources (las fuentes de la aplicación).
#Por defecto se crea en CWD
source_files_folder_path=""
     
# Ruta del directorio que contiene los editables (.toml (translatable files)). 
#Por defecto se crea en CWD 
translatables_folder_path=""

skip_exceptions=false          

# finaliza la ejecucción de build si el traductor no ha sido posible traducir un lenguaje.
stop_on_failure=true            
# [PARA EL MAINTAINER] el stop_on_failure se puede quitar si antes de hacer la build se verifican si los lenguajes pasados 
# [PARA EL MAINTAINER] estan disponibles en el traductor que usamos. Probaremos 3 traductores, si ninguno permite el lenguaje,

# Capacidad de revisar los .toml traducidos  con los que se va a crear el binario
revise_before_bundle=true      

# Una vez finalizada la build, se eliminan todos los directorios usados por QAutoLinguist.
# El directorio que contiene los binarios finales NO sera eliminado.
clean_build=true                

# output en consola informando sobre los procesos realizados en runtime
debug_mode=true                 

# si debug_mode es True, muestra mas detalles del debug.
verbose=false     

```

