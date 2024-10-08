# from time import time
# import translator

# LIST = [
#     ":   Esto es un texto de prueba 1.  ",
#     "Nombre de un botón 2",
#     "<html><p>Simbolos html<p><html> 3",
#     "      Corto 4",
#     "Texto largo para comprobar efectividad 5",
#     "Mas símbolos raros <>~!@#$%^&&*(()&*^%) \\n (saltos de línea) 6  \ asd \ dsads?|\\",
#     "Quiero saber cuanto tarda en asatgaetae684-64068472hwrtraducir 7",
#     "Otro texto de prueba 8",
#     "Un nombre diferente para un botón 9   Äayhn adyasyashflswkr ",
# ]

# # if len("".join(LIST)) > 5000:
# #     raise Exception("Menos longitud")
# # if len("".join(LIST)) < 4800:
# #     raise Exception("Anade mas translations")


# def run_tests(
#     languages_to_test: List[str], 
#     sample: List[str] = LIST, 
#     seps: List[str] = Translators.SILENT_SEPARATORS
#     ):
#     traductor = Translator()
#     times = {lang: None for lang in languages_to_test}
#     traductions = {lang: None for lang in languages_to_test}
    
#     for lang in languages_to_test:
#         traductor.translator.source = "es"
#         traductor.translator.target = lang
#         for unicode_sep in seps:
#             joined_batch = unicode_sep.join(sample)
#             start = time()
#             result = traductor.translator.translate(joined_batch)    
#             finish = time() - start
#             print(f"Original: {len(sample)} ==== Result: {len(result.split(unicode_sep))}\n")
#             if len(result.split(unicode_sep)) == len(sample):
#                 print(f"Sep item [{seps.index(unicode_sep)}] YES with [{lang}]\n")
#                 times[lang] = finish
#                 traductions[lang] = result.split(unicode_sep)
#             else:
#                 print(f"Sep item [{seps.index(unicode_sep)}] NO with [{lang}]\n")
    
#     return traductions, "\n\n", sum(times.values()) if all(time_ is not None for time_ in times.values()) else None, "\n\n", times
    
# run_tests()
