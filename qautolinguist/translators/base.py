"""base translator class"""

import qautolinguist.translators.exceptions as exceptions
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Union

from qautolinguist.translators.constants import GOOGLE_LANGUAGES_TO_CODES, SILENT_SEPARATORS


class BaseTranslator(ABC):
    """
    Abstract class that serve as a base translator for other different translators
    """

    def __init__(
        self,
        base_url: str = None,
        languages: dict = GOOGLE_LANGUAGES_TO_CODES,
        source: str = "auto",
        target: str = "en",
        payload_key: Optional[str] = None,
        element_tag: Optional[str] = None,
        element_query: Optional[dict] = None,
        **url_params,
    ):
        """
        @param source: source language to translate from
        @param target: target language to translate to
        """
        self._base_url = base_url
        self._languages = languages
        self._supported_languages = list(self._languages.keys())
        if not source:
            raise exceptions.InvalidSourceOrTargetLanguage(source)
        if not target:
            raise exceptions.InvalidSourceOrTargetLanguage(target)

        self._source, self._target = self._map_language_to_code(source, target)
        self._url_params = url_params
        self._element_tag = element_tag
        self._element_query = element_query
        self.payload_key = payload_key
        super().__init__()

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, lang):
        self._source = lang

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, lang):
        self._target = lang

    def _type(self):
        return self.__class__.__name__

    def _map_language_to_code(self, *languages):
        """
        map language to its corresponding code (abbreviation) if the language was passed
        by its full name by the user
        @param languages: list of languages
        @return: mapped value of the language or raise an exception if the language is
        not supported
        """
        for language in languages:
            if language in self._languages.values() or language == "auto":
                yield language
            elif language in self._languages.keys():
                yield self._languages[language]
            else:
                raise exceptions.LanguageNotSupportedException(
                    language,
                    message=f"No support for the provided language.\n"
                    f"Please select on of the supported languages:\n"
                    f"{self._languages}",
                )

    def _same_source_target(self) -> bool:
        return self._source == self._target

    def get_supported_languages(
        self, as_dict: bool = False, **kwargs
    ) -> Union[list, dict]:
        """
        return the supported languages by the Google translator
        @param as_dict: if True, the languages will be returned as a dictionary
        mapping languages to their abbreviations
        @return: list or dict
        """
        return self._languages if as_dict else self._supported_languages

    def is_language_supported(self, language: str, **kwargs) -> bool:
        """
        check if the language is supported by the translator
        @param language: a string for 1 language
        @return: bool or raise an Exception
        """
        return (
            language == "auto"
            or language in self._languages.keys()
            or language in self._languages.values()
        )

    @abstractmethod
    def translate(self, text: str, **kwargs) -> str:
        """
        translate a text using a translator under the hood and return
        the translated text
        @param text: text to translate
        @param kwargs: additional arguments
        @return: str
        """
        return NotImplemented("You need to implement the translate method!")


    def _translate_file(self, path: str, **kwargs) -> str:
        """
        translate directly from file
        @param path: path to the target file
        @type path: str
        @param kwargs: additional args
        @return: str
        """
        if not isinstance(path, Path):
            path = Path(path)

        if not path.exists():
            print("Path to the file is wrong!")
            exit(1)
        else:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read().strip()

        return self.translate(text)


    def _translate_batch(
        self,
        batch: List[str],
        target_lang: str,
        source_lang: str = "en",
        *,
        fast_translation: bool = True,
        allow_unresolved_sources: bool = False,
        never_fail: bool = True
    ) -> List[str]:
        """
        Translate a list of texts.
        @param batch: List of texts you want to translate.
        @param fast_translation: When True, tries to unify all elements in batch into a single text with separators.
        @param allow_unresolved_sources: When True, returns empty translations if unable to translate a source. 
        @param never_fail: When using ``fast_translation`` and not ``allow_unresolved_sources``, always tries to resolve a translation 
        even if the translation losses quality.
        NOTE: This param can increase the time of execution of this func since it tries to translate one by one.
        """
        if not batch:
            raise exceptions.InvalidResource("Enter your text list that you want to translate")

        if not isinstance(batch, (list, tuple)) or not all(isinstance(item, str) for item in batch):
            raise exceptions.InvalidResource("Batch must be a list/tuple containing str items")

        self.source = source_lang
        self.target = target_lang
        
        if not fast_translation:
            print(f"Using slow each-one translation for '{target_lang.upper()}'")
            return self._translate_batch_each(batch)
        
        if allow_unresolved_sources:
            shadow = []
            for idx, item in enumerate(batch):
                try:
                    resolve = self.translate(item)
                except exceptions.BaseError:
                    shadow.insert(idx, "")
                else:
                    shadow.append(idx, resolve)     
            return shadow
        

        for sep in SILENT_SEPARATORS:
            joined_batch = sep.join(batch)
            result = self.translate(joined_batch) #, separator = " "
            to_batch = result.split(sep)
            print(f"Checking joiner {sep!r}, same chars to {self.source}->{self.target}: O:{len(batch)} -- T:{len(to_batch)}")
            
            if len(to_batch) == len(batch):
                print(f"Batch joint worked with {target_lang.upper()}\n")
                return to_batch
       
        if never_fail:
            print(f"Joint batch translation failed with {self.source}->{self.target}: Using each-item translation instead.")
            print("[WARNING]:: This translation process may take a while to process.....")
            return self._translate_batch_each(batch)
            
        raise exceptions.TranslationNotFound(f"Internal error during translating batch.\nInform this error to the developers: 'Invalid unicode separators: {SILENT_SEPARATORS}' didn-t worked")


    def _translate_batch_each(self, batch):
        "Method called when failed to translate a batch using separators in a single text"
        try:
            return [self.translate(item) for item in batch]
        except (
            exceptions.TranslationNotFound,
            exceptions.RequestError,
            exceptions.TooManyRequests
        ) as e:
            raise exceptions.TranslationNotFound(f"Translation cannot be done for this batch. Tried each-one translation for {self.source}->{self.target}") from e

    
            
        
        
