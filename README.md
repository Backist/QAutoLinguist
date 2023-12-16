<<<<<<< HEAD
# Funcionamiento/Idea de ejecuccion:

## En casos generales esto es lo que estás buscando:
#### Si se ha especificado incluir QAutoLinguist en la variable de entorno PATH:
  - **Windows**:
  ```bash
  >>> qautolinguist build -init [<config_file_path>]   #crea un .config.toml en CWD para poder editar los atributos de la build. Si no se especifica ruta, el archivo config se crea en el directorio de trabajo (CWD)
  >>> qautolinguist build [<config_file_path>]         # en caso de que el archivo .config.toml no esté en el directorio donde se ejecuta el comando
  ```

  - **Linux**:
  ```bash
  >>> python3 -m qautolinguist build -init  [<config_file_path>]
  >>> python3 -m qautolinguist build [<config_file_path>]
  ```

## Modificaciones o rebuilds
#### Si se desea cambiar o retocar alguna traduccion (archivos .toml):
  - ``Simplemente volvemos a crear los binarios:``
    ```bash
    >>> qautolinguist build -bundles  [<config_file_path>]  # windows
    >>> python3 -m qautolinguist build -bundles [<config_file_path>] # linux
  ```
  > Esto creará de nuevo los binarios con los archivos de traduccion retocados.

  #### Si han habido modificaciones en las fuentes de la aplicacion:
  - ``Es necesario crear una build nueva:``
    ```bash
    >>> qautolinguist build [<config_file_path>]  # windows
    >>> python3 -m qautolinguist build [<config_file_path>] # linux
    ```
    > Esto sobreescribirá los archivos de traduccion (no se crearán nuevos)


Respeto al ``.config.toml`` que se genera cuando se ejecuta ``**qautotranslator build -init``,
se verá algo asi:

```toml
[Required]

# archivo .ui o el que contiene los tr() o QCoreAplication.Translate
source_file=""  

#lenguaje de referencia, normalmente el de tu aplicación. En caso de fallo de traduccion de algun lenguage, se usará el source de este lenguaje, a menos que stop_on_failure en la sección [Optionals] sea true.
# por defecto, es inglés.
default_language="english"     

# incluye en esta lista los lenguajes a traducir
available_languages=[

]


# Usualmente no necesitarás editar esta sección.
# Aquí puedes ajustar donde se guardan los archivos generados y algunos ajustes para
# manejar el comportamiento del QAutoLinguist
[Optionals]

#Ubicación de la carpeta que contiene los binarios finales. 
#Por defecto se crea en CWD 
translations_path=""
     
# Ruta específica de la carpeta que contiene los editables (.toml (translatable files)). 
#Por defecto se crea en CWD 
translatables_path=""

skip_exceptions=false          

# finaliza la ejecucción de build si el traductor no ha sido posible traducir un lenguaje.
stop_on_failure=true            
#el stop_on_failure se puede quitar si antes de hacer la build se verifican si los lenguajes pasados 
estan disponibles en el traductor que usamos. Probaremos 3 traductores, si ninguno permite el lenguaje,

# Capacidad de revisar los .toml traducidos  con los que se va a crear el binario
revise_before_bundle=true      

# Se eliminan todos los directorios con los archivos .ts y .toml creados por la build. Se conservará la que contiene los binarios finales
clean_build=true                

# output en consola informando sobre los procesos realizados en runtime
debug_mode=true                 

# si debug_mode es True, muestra mas detalles del debug.
verbose=false                   
```

