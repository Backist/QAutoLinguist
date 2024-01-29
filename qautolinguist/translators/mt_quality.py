"File that checks the quality of automatic translations."

from nltk.translate.bleu_score import sentence_bleu
from nltk.translate.gleu_score import sentence_gleu

# Ejemplo de uso de BLEU
reference = 'Inner padding.'
candidate = 'Paping inferiore.'
gleu_score = sentence_gleu([reference.split()], candidate.split())
bleu_score = sentence_bleu([reference.split()], candidate.split())
# print(f"Puntuación BLEU: {bleu_score}")
# print(f"Puntuación BLEU: {gleu_score}")
