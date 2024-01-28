import translators as Translators
import translators.exceptions as api_exceptions                
import exceptions

from typing import List, Tuple, Union

__all__: list[str] = ["Translator"]

class Translator:
    """
    Top-level translator impl class.
    
    This class lets you choose the api_translator and also adds a extra method _check_connection to verify the machine have connection
    before translation process starts. 
    """

    def __init__(self, api_translator = Translators.GoogleTranslator):
        self._translator = api_translator()

        if not self._check_connection():
            raise exceptions.TranslatorConnectionError("You don't have internet connection. QAutoLinguist requires internet connection")
    
    def _check_connection(self):
        import requests
        print("Check connection...Trying to connect with translator API")
        return requests.get("https://www.google.com", timeout=5).status_code == 200
        
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
        except (
            api_exceptions.InvalidResource,
            api_exceptions.TranslationNotFound
        ) as e:
            raise exceptions.TranslationFailed(f"Error translating batch. Detailed error: {e}") from None
    




    
    
        

        
