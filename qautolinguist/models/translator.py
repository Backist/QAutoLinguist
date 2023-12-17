import deep_translator                          # Python module that handle +5 APIs-> DeepTranslator, MicrosoftTranslator y ChatGPTranslator require API KEY
import shutil
import os
from pathlib import Path
from time import time, strftime
Translators = deep_translator                   # Convenience Name to module deep_translator

__all__: list[str] = ["Translator"]

class Translator:
    
    def __init__(self, compatible_with_tsf_files: bool = True):
        self.translator                = Translators.GoogleTranslator
        self.compatible_with_tsf_files = compatible_with_tsf_files
        if not self._check_connection():
            raise Warning(
                DebugLogs.warning("There is no internet connection; This class needs internet connection to work")
            )
    
    def _check_connection(self):
        import requests
        try:
            print("Check connection...Trying to connect with API")
            response = requests.get("https://www.google.com", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def _make_temp_copy(self, _file: Path):
        """
        Makes a temporary copy of a file and returns the path of the temporary file.
        
        Args:
            _file: The path of the file to be copied (str).
        Returns:
            The path of the temporary file (str).
        """
        temp_file_path = _file.with_suffix(".temp")
        shutil.copyfile(_file, temp_file_path)
        return temp_file_path
        
    
    def _remove_temp_copy(self, _temp: Path, _file: Path):
        """
        Copy _temp file contents to _file, removes itself and returns the path of _file.
        Args:
            _temp: The path of the temporary file to copy content and then be removed (str).
            _file: The path of the destination file (str).
        Returns:
            The path of the copied file (str).
        """
        shutil.copyfile(_temp, _file)   
        os.remove(_temp)
        return _file
        

    def translate_to(self, _file: Path, to_lang: str, linear_translation: bool = False,  source_lang: str = "en", strict: bool = True):
        """Traduce el contenido de un archivo.
        Crea un archivo temporal automaticamente por si algo falla.
        Si algo falla devuelve la ruta de _file, restableciendo el _file con el temp file. Si strict es True raisea ValueError
        """
        temp_file_path = self._make_temp_copy(_file)            #? Esto se puede hacer usando contextmanager, para que se elimine auto el temp file
    
        try:         
            if self.compatible_with_tsf_files:
                translations = TsfComposer.get_translations(_file) 
            else:
                with _file.read_text('r', encoding='utf-8') as _f:
                    translations = (l.strip() for l in _f.readlines())      
            resolved_lines = self.translator(source_lang, to_lang).translate_batch(translations)
            
            if self.compatible_with_tsf_files:
                TsfComposer.insert_translations(_file, resolved_lines)
            else:
                with _file.open('w', encoding='utf-8') as _f:
                    _f.writelines((f"{line}\n" for line in resolved_lines))
            os.remove(temp_file_path)                                                # eliminamos el archivo de copia si todo ha ido bien
        except Exception as e:
            self._remove_temp_copy(temp_file_path, _file)   
            if strict:                                                              # Restablecemos el contenido por seguridad; Algo ha fallado
                raise Exception(
                    DebugLogs.error(
                        f"Unexpected error translating {_file}. Content has been loaded from temporally file. Detailed Error: {e}"
                    )
                )
        finally:
            return _file                # force to return the Path
        
        
    # def translate_from_batch(self, _batch: Iterable, target_lang: str =None, source_lang: str = "en", detect_lang: bool = False, strict: bool = False):
    #     """
    #     Translates a batch of strings or Path Object.

    #     Args:
    #         _batch: An iterable containing strings or Path objects to be translated.
    #         target_lang: The target language for translation. ``Note: If none, we try to get the target in file name, supposing Path files in batch with fileformat <xx_XX>.``.
    #         source_lang: The source language of the strings or files. Defaults to "en" (str).
    #         detect_lang: Whether to automatically detect the source language. Defaults to False.
    #     Raises:
    #         OSError: If a file could not be translated and a temporary file was used to preserve the original content.

    #     NOTE:
    #         ``This function performs multiple queries in a short period of time and may result in long execution times.
    #         As a reference, it takes approximately 14-17 seconds to translate a file of ~600 words.``
    #     """
    #     untranslated = []           # Here we store str/files that could not be translated

    #     if not all(isinstance(elem, Path) for elem in _batch):
    #         raise TypeError(
    #             DebugLogs.error("Invalid _batch type elements. Elements in _batch must be type str or Path")
    #         )
    #     for _file in _batch:
    #         self.translator.target = _file.name[2:] if target_lang is None else target_lang    # Avoid to create new instances, change target only.
    #         try:
    #             self.translate_to(_file, _file.name[:2], "auto" if detect_lang else source_lang)
    #         except Exception as e:      # Toma la excepcion causada por translate_to
    #             if strict:
    #                 raise Exception(
    #                     DebugLogs.error(
    #                         f"Unexpected error during translating {_file}; Restored content from temp file tp remain original content"
    #                     )
    #                 ) from e
    #             DebugLogs.warning(
    #                 f"Skipped {_file} during translating; Error: {e}"
    #             )
    #             untranslated.append(_file)
    #     return untranslated or None
    

if __name__ == "__main__":
    import re
    trans = Translators.GoogleTranslator("es", "en")

    LIST = [
    "Esto es un texto de prueba 1.",
    "Nombre de un botón 2",
    "<html><p>Simbolos html<p><html> 3",
    "      Corto 4",
    "Texto largo para comprobar efectividad 5",
    "Mas símbolos raros <>~!@#$%^&&*(()&*^%) \\n (saltos de línea) 6",
    "Quiero saber cuanto tarda en traducir 7",
    "Otro texto de prueba 8",
    "Un nombre diferente para un botón 9",
    "<html><p>Otros símbolos html<p><html> 10",
    "Texto corto 11",
    "Un texto más largo para evaluar la eficacia 12",
    "Más símbolos raros <>~!@#$%^&&*(()&*^%) \\n (saltos de línea) 13",
    "Quiero ver cuánto tiempo tarda en traducir esto 14",
    "Texto de ejemplo 15",
    "Botón de muestra 16",
    "<html><p>Símbolos html de muestra<p><html> 17",
    "Esto es un texto de prueba 1.",
    "Nombre de un botón 2",
    "<html><p>Simbolos html<p><html> 3",
    "      Corto 4",
    "Texto largo para comprobar efectividad 5",
    "Mas símbolos raros <>~!@#$%^&&*(()&*^%) \\n (saltos de línea) 6",
    "Quiero saber cuanto tarda en traducir 7",
    "Otro texto de prueba 8",
    "Un nombre diferente para un botón 9",
    "<html><p>Otros símbolos html<p><html> 10",
    "Texto corto 11",
    "Un texto más largo para evaluar la eficacia 12",
    "Más símbolos raros <>~!@#$%^&&*(()&*^%) \\n (saltos de línea) 13",
    "Quiero ver cuánto tiempo tarda en traducir esto 14",
    "Texto de ejemplo 15",
    "Botón de muestra 16",
    "<html><p>Símbolos html de muestra<p><html> 17",
    "Esto es un texto de prueba 1.",
    "Nombre de un botón 2",
    "<html><p>Simbolos html<p><html> 3",
    "      Corto 4",
    "Texto largo para comprobar efectividad 5",
    "Mas símbolos raros <>~!@#$%^&&*(()&*^%) \\n (saltos de línea) 6",
    "Quiero saber cuanto tarda en traducir 7",
    "Otro texto de prueba 8",
    "Un nombre diferente para un botón 9",
    "<html><p>Otros símbolos html<p><html> 10",
    "Texto corto 11",
    "Un texto más largo para evaluar la eficacia 12",
    "Más símbolos raros <>~!@#$%^&&*(()&*^%) \\n (saltos de línea) 13",
    "Quiero ver cuánto tiempo tarda en traducir esto 14",
    "Texto de ejemplo 15",
    "Botón de muestra 16",
    "<html><p>Símbolos html de muestra<p><html> 17",
    "Esto es un texto de prueba 1.",
    "Nombre de un botón 2",
    "<html><p>Simbolos html<p><html> 3",
    "      Corto 4",
    "Texto largo para comprobar efectividad 5",
    "Mas símbolos raros <>~!@#$%^&&*(()&*^%) \\n (saltos de línea) 6",
    "Quiero saber cuanto tarda en traducir 7",
    "Otro texto de prueba 8",
    "Un nombre diferente para un botón 9",
    "<html><p>Otros símbolos html<p><html> 10",
    "Texto corto 11",
    "Un texto más largo para evaluar la eficacia 12",
    "Más símbolos raros <>~!@#$%^&&*(()&*^%) \\n (saltos de línea) 13",
    "Quiero ver cuánto tiempo tarda en traducir esto 14",
    "Texto de ejemplo 15",
    "Botón de muestra 16",
    "<html><p>Símbolos html de muestra<p><html> 17",
    ]
    
    TEXT= "\u2002".join(LIST)
    
    AVAILABLE_LANGS: dict = {
        "English": "en",
        # "Spanish": "es",
        # "Italian": "it",
        # "Catalan": "ca",
        # "French": "fr",
        # "German": "de",
        # "Russian": "ru",        
        # "Ukrainian": "uk",
        # "Portuguese": "pt",
        # "Japanese": "ja",
        # "Korean": "ko",
        # "Mandarin": "zh",
        # "Chinese (simplified)": "zh-CN",
        # "Indian": "hi", 
        # "Turkish": "tr",
        # "Greek": "el",
        # "Swedish": "sv",
        # "Norwegian": "no",
        # "Danish": "da",
        # "Indonesian": "id",
    }
    test_langs=AVAILABLE_LANGS.values()
    
    def partir_texto(texto, n):
        return [texto[i:i+n] for i in range(0, len(texto), n)]
    
            
    def run_tests(test, test_langs):
        print(f"TEXTO DE PRUEBA: {TEXT}\n\n\n\n")
        times = []
        results={}
        for lang in test_langs:
            trans.source="es"
            trans.target=lang
            start = time()
            translation = trans.translate(test)
            finish=time()-start
            times.append(finish)
            results[lang]= translation.split("\u2002")
        return sum(times), times, results
    
    print(run_tests(TEXT, test_langs))
            
        
