import translators as Translators                
import exceptions
from typing import List, Tuple, Union
from time import time, strftime

__all__: list[str] = ["Translator"]



class Translator:

    def __init__(self, translator = Translators.GoogleTranslator):
        self._translator = translator()

        if not self._check_connection():
            raise exceptions.TranslatorConnectionError("You don't have internet connection. QAutoLinguist requires internet connection")
    
    def _check_connection(self):
        import requests
        try:
            print("Check connection...Trying to connect with translator API")
            response = requests.get("https://www.google.com", timeout=5)
            return response.status_code == 200
        except:
            return False
        
    def validate_languages(self, languages: List[str]):
        return all(self.validate_language(lang) for lang in languages)

    def validate_language(self, language: str):
        "Comprueba que el lenguaje es compatible por GoogleTranslate y por nuestro algoritmo verificado de unicodes"
        return self._translator.is_language_supported(language)
    
    def available_langs(self):
        return self._translator.get_supported_languages()
     
    def translate_batch(
            self,
            batch: Union[List[str], Tuple[str]],
            **kwargs
        ):
        """
        Translates a batch of strings or Path Object.

        Args:
            batch: An iterable containing strings or Path objects to be translated.
            target_lang: The target language for translation. ``Note: If None, target lang is auto-detected
            source_lang: The source language of the strings or files. Defaults to "en" (str).
            stop_on_failure: When True, stops if cannot be translated the text and raise an error, otherwise will be tried to translate one by one.
        Raises:
            TranslationFailed: If a file could not be translated and a temporary file was used to preserve the original content.

        NOTE:
            ``This function performs multiple queries in a short period of time and may result in long execution times
            for long translations.``
        """

        try:
            return self._translator.translate_batch(batch, **kwargs)
        except Exception as e:
            raise exceptions.TranslationFailed(f"Error translating batch. Detailed error: {e}")
    

if __name__ == "__main__":
    from time import time
    LIST = [
        ":   Esto es un texto de prueba 1.  ",
        "Nombre de un botón 2",
        "<html><p>Simbolos html<p><html> 3",
        "      Corto 4",
        "Texto largo para comprobar efectividad 5",
        "Mas símbolos raros <>~!@#$%^&&*(()&*^%) \\n (saltos de línea) 6  \ asd \ dsads?|\\",
        "Quiero saber cuanto tarda en asatgaetae684-64068472hwrtraducir 7",
        "Otro texto de prueba 8",
        "Un nombre diferente para un botón 9   Äayhn adyasyashflswkr ",
    ]
    
    # if len("".join(LIST)) > 5000:
    #     raise Exception("Menos longitud")
    # if len("".join(LIST)) < 4800:
    #     raise Exception("Anade mas translations")
    
    
    def run_tests(
        languages_to_test: List[str], 
        sample: List[str] = LIST, 
        seps: List[str] = Translators.SILENT_SEPARATORS
        ):
        traductor = Translator()
        times = {lang: None for lang in languages_to_test}
        traductions = {lang: None for lang in languages_to_test}
        
        for lang in languages_to_test:
            traductor.translator.source = "es"
            traductor.translator.target = lang
            for unicode_sep in seps:
                joined_batch = unicode_sep.join(sample)
                start = time()
                result = traductor.translator.translate(joined_batch)    
                finish = time() - start
                print(f"Original: {len(sample)} ==== Result: {len(result.split(unicode_sep))}\n")
                if len(result.split(unicode_sep)) == len(sample):
                    print(f"Sep item [{seps.index(unicode_sep)}] YES with [{lang}]\n")
                    times[lang] = finish
                    traductions[lang] = result.split(unicode_sep)
                else:
                    print(f"Sep item [{seps.index(unicode_sep)}] NO with [{lang}]\n")
        
        return traductions, "\n\n", sum(times.values()) if all(time_ is not None for time_ in times.values()) else None, "\n\n", times
        
    # run_tests()
    




    
    
        

        
