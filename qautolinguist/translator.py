import deep_translator                          # Python module that handle +5 APIs-> DeepTranslator, MicrosoftTranslator y ChatGPTranslator require API KEY
import exceptions
import consts
from typing import List, Tuple, Union, Optional
from pathlib import Path
from time import time, strftime
Translators = deep_translator                   # Convenience Name to module deep_translator

__all__: list[str] = ["Translator"]


class Translator:

    
    def __init__(self, translator = Translators.GoogleTranslator):
        self.translator = translator()

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
        return (
            language.lower() in consts.AVAILABLE_ALGORITHM_LANGS.keys() or 
            language.lower() in consts.AVAILABLE_ALGORITHM_LANGS.values()
        )
    
    def available_langs(self):
        return consts.AVAILABLE_ALGORITHM_LANGS.values()
    
    def _get_unicode_sep(self, lang: str):
        "Devuelve el unicode correspondiente para el lenguaje, que será usado para unir frases a un único texto"
        for unicode, langs in consts.UNICODES_MATCHES.items():
            if lang.lower() in langs:
                return unicode
        return None
        
    def translate_batch(
            self, batch: 
            Union[List[str], Tuple[str]], 
            target_lang: str, 
            source_lang: str = "en", 
        ):
        """
        Translates a batch of strings or Path Object.

        Args:
            batch: An iterable containing strings or Path objects to be translated.
            target_lang: The target language for translation. ``Note: If None, target lang is auto-detected
            source_lang: The source language of the strings or files. Defaults to "en" (str).
        Raises:
            TranslationFailed: If a file could not be translated and a temporary file was used to preserve the original content.

        NOTE:
            ``This function performs multiple queries in a short period of time and may result in long execution times
            for long translations.``
        """

        unicode_sep = self._get_unicode_sep(target_lang)
        if unicode_sep is None:
            raise exceptions.TranslationFailed(f"Invalid language passed, call available_langs to get a list of available languages.")
        
        joined_content = unicode_sep.join(batch)
        check_length = len(batch)

        self.translator.source = source_lang
        self.translator.target = target_lang

        try:
            result = self.translator.translate(joined_content)
        except Exception as e:
            raise exceptions.TranslationFailed(f"Error translating batch. Detailed error: {e}")
        
        dejoin = result.strip(unicode_sep)
        if len(dejoin) == check_length:
            return dejoin
            
        raise exceptions.TranslationFailed(f"Something internally failed and the amount of items of batch does not match with the new translated batch length")
    


class _UnicodeSepCheck:
    """Clase de uso exclusivo interno para comprobar si la API usada es compatible con el sistema basado en 
    codigos unicode para traducir listas o iterables.
    ``Translator`` usa caracteres unicode como separadores de elementos del iterable en base a buscar una solución rápida y efectiva
    para traducir. 
    
    Este metodo propone menos peticiones a la API, ya que junta todos elementos en un único texto el cual contiene
    las frases o palabras separadas por el caracter unicode  .
    """

    GOOGLE_TRANSLATOR_LANGUAGES = {
        "afrikaans": "af",
        "albanian": "sq",
        "amharic": "am",
        "arabic": "ar",
        "armenian": "hy",
        "assamese": "as",
        "aymara": "ay",
        "azerbaijani": "az",
        "bambara": "bm",
        "basque": "eu",
        "belarusian": "be",
        "bengali": "bn",
        "bhojpuri": "bho",
        "bosnian": "bs",
        "bulgarian": "bg",
        "catalan": "ca",
        "cebuano": "ceb",
        "chichewa": "ny",
        "chinese (simplified)": "zh-CN",
        "chinese (traditional)": "zh-TW",
        "corsican": "co",
        "croatian": "hr",
        "czech": "cs",
        "danish": "da",
        "dhivehi": "dv",
        "dogri": "doi",
        "dutch": "nl",
        "english": "en",
        "esperanto": "eo",
        "estonian": "et",
        "ewe": "ee",
        "filipino": "tl",
        "finnish": "fi",
        "french": "fr",
        "frisian": "fy",
        "galician": "gl",
        "georgian": "ka",
        "german": "de",
        "greek": "el",
        "guarani": "gn",
        "gujarati": "gu",
        "haitian creole": "ht",
        "hausa": "ha",
        "hawaiian": "haw",
        "hebrew": "iw",
        "hindi": "hi",
        "hmong": "hmn",
        "hungarian": "hu",
        "icelandic": "is",
        "igbo": "ig",
        "ilocano": "ilo",
        "indonesian": "id",
        "irish": "ga",
        "italian": "it",
        "japanese": "ja",
        "javanese": "jw",
        "kannada": "kn",
        "kazakh": "kk",
        "khmer": "km",
        "kinyarwanda": "rw",
        "konkani": "gom",
        "korean": "ko",
        "krio": "kri",
        "kurdish (kurmanji)": "ku",
        "kurdish (sorani)": "ckb",
        "kyrgyz": "ky",
        "lao": "lo",
        "latin": "la",
        "latvian": "lv",
        "lingala": "ln",
        "lithuanian": "lt",
        "luganda": "lg",
        "luxembourgish": "lb",
        "macedonian": "mk",
        "maithili": "mai",
        "malagasy": "mg",
        "malay": "ms",
        "malayalam": "ml",
        "maltese": "mt",
        "maori": "mi",
        "marathi": "mr",
        "meiteilon (manipuri)": "mni-Mtei",
        "mizo": "lus",
        "mongolian": "mn",
        "myanmar": "my",
        "nepali": "ne",
        "norwegian": "no",
        "odia (oriya)": "or",
        "oromo": "om",
        "pashto": "ps",
        "persian": "fa",
        "polish": "pl",
        "portuguese": "pt",
        "punjabi": "pa",
        "quechua": "qu",
        "romanian": "ro",
        "russian": "ru",
        "samoan": "sm",
        "sanskrit": "sa",
        "scots gaelic": "gd",
        "sepedi": "nso",
        "serbian": "sr",
        "sesotho": "st",
        "shona": "sn",
        "sindhi": "sd",
        "sinhala": "si",
        "slovak": "sk",
        "slovenian": "sl",
        "somali": "so",
        "spanish": "es",
        "sundanese": "su",
        "swahili": "sw",
        "swedish": "sv",
        "tajik": "tg",
        "tamil": "ta",
        "tatar": "tt",
        "telugu": "te",
        "thai": "th",
        "tigrinya": "ti",
        "tsonga": "ts",
        "turkish": "tr",
        "turkmen": "tk",
        "twi": "ak",
        "ukrainian": "uk",
        "urdu": "ur",
        "uyghur": "ug",
        "uzbek": "uz",
        "vietnamese": "vi",
        "welsh": "cy",
        "xhosa": "xh",
        "yiddish": "yi",
        "yoruba": "yo",
        "zulu": "zu",
    }

    TARGET = [
        "  :Otro texto de prueba 8: ",
        r" \ Un nombre diferente para un botón 9// sdfd /   \   \   /",
        "*<html><p>Otros símbolos html<p><html> #$%%#^#@342$@24@$ \\\\34 10",
        "\nn",
        """''""",
        "!@#$%^&*(*)(Rompecabezas de boro, químicamente majestuoso.)"
        "s",
        "'sds'\n/ ''''''",
        "Esto es un texto de prueba 1. Aquí queremos ver como procesa los bytes como \r\t\b\\",
        "Esta es una frase mucho más larga que se agrega para aumentar la longitud total de la lista y probar el traductor con textos extensos. Aquí hay más contenido para evaluar la eficacia de la traducción en casos de entrada grandes. Además, se están incorporando caracteres especiales, números y simbolos para asegurar una variedad completa de casos. ¡Esperamos que esta extensión sea útil para tus pruebas!",
    ]


    def __init__(self, langs: List[str], separators: List[str] = consts.SILENT_SEPARATORS):
        self.seps = separators
        self.languages_to_test = langs

    def run_test(self):
        d = {lang: [] for lang in self.languages_to_test}
        valid_tests = {char: [] for char in self.seps}  
        for lang in self.languages_to_test:
            trans.source="es"
            trans.target=lang
            for char in self.seps:
                text = char.join(self.TARGET)
                start = time()
                translation = trans.translate(text)
                finish=time()-start
                if len(translation.split(char)) == len(self.TARGET):
                    print(f"Unicode at item {self.seps.index(char)} WORKED with lang {lang}")
                    d[lang].insert(0, finish)  
                    d[lang].insert(1, translation.split(char))
                    valid_tests[char].append(lang)
                    break
                else:
                    print(f"Unicode at item {self.seps.index(char)} NO WORKED with lang {lang}")

        if valid_tests:         
            return d, valid_tests
        else:
            print("Ningun char fué valido en ningun lenguaje")
    


if __name__ == "__main__":
    from time import time
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
        "Texto de ejemplo 15",
        "Botón de muestra 16",
        "<html><p>Símbolos html de muestra<p><html> 17",
        "<html><p>Simbolos html<p><html> 3",
        "<html><p>Símbolos html de muestra<p><html> 17",
        "Esto es un texto de prueba 1.",
        "Nombre de un botón 2",
        "Texto de ejemplo 15",
        "Botón de muestra 16",
        "<html><p>Símbolos html de muestra<p><html> 17",
        "Esta es una frase mucho más larga que se agrega para aumentar la longitud total de la lista y probar el traductor con textos extensos. Aquí hay más contenido para evaluar la eficacia de la traducción en casos de entrada grandes. Además, se están incorporando caracteres especiales, números y simbolos para asegurar una variedad completa de casos. ¡Esperamos que esta extensión sea útil para tus pruebas!",
        "Esta es una frase mucho más larga que se agrega para aumentar la longitud total de la lista y probar el traductor con textos extensos. Aquí hay más contenido para evaluar la eficacia de la traducción en casos de entrada grandes. Además, se están incorporando caracteres especiales, números y simbolos para asegurar una variedad completa de casos. ¡Esperamos que esta extensión sea útil para tus pruebas!",
        "Esta es una frase mucho más larga que se agrega para aumentar la longitud total de la lista y probar el traductor con textos extensos. Aquí hay más contenido para evaluar la eficacia de la traducción en casos de entrada grandes. Además, se están incorporando caracteres especiales, números y simbolos para asegurar una variedad completa de casos. ¡Esperamos que esta extensión sea útil para tus pruebas!",
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
        "Esta es una frase mucho más larga que se agrega para aumentar la longitud total de la lista y probar el traductor con textos extensos. Aquí hay más contenido para evaluar la eficacia de la traducción en casos de entrada grandes. Además, se están incorporando caracteres especiales, números y simbolos para asegurar una variedad completa de casos. ¡Esperamos que esta extensión sea útil para tus pruebas!",
        "Esta es una frase mucho más larga que se agrega para aumentar la longitud total de la lista y probar el traductor con textos extensos. Aquí hay más contenido para evaluar la eficacia de la traducción en casos de entrada grandes. Además, se están incorporando caracteres especiales, números y simbolos para asegurar una variedad completa de casos. ¡Esperamos que esta extensión sea útil para tus pruebas!",
        "Esta es una frase mucho más larga que se agrega para aumentar la longitud total de la lista y probar el traductor con textos extensos. Aquí hay más contenido para evaluar la eficacia de la traducción en casos de entrada grandes. Además, se están incorporando caracteres especiales, números y simbolos para asegurar una variedad completa de casos. ¡Esperamos que esta extensión sea útil para tus pruebas!",
        "Esta es una frase mucho más larga que se agrega para aumentar la longitud total de la lista y probar el traductor con textos extensos. Aquí hay más contenido para evaluar la eficacia de la traducción en casos de entrada grandes. Además, se están incorporando caracteres especiales, números y simbolos para asegurar una variedad completa de casos. ¡Esperamos que esta extensión sea útil para tus pruebas!",
    ]
    
    t = Translator()
    times = []
    results = []
    for lang in consts.AVAILABLE_ALGORITHM_LANGS.values():
        init = time()
        r = t.translate_batch(LIST, lang) 
        final = time()-init
        
        times.append(final)
        results.append(r)

    print(times, "\n\n\n\n\n", results, "\n\n\n\n\n", sum(times))




    
    
        

        
