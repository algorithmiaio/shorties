import Algorithmia
import os

client            = Algorithmia.client('simfxr2fI6g9qElSIhzTJ1BM9DV1')
trigram_file_name	= "right-ho-trigrams.txt"

corpus  = []

# generate array of sentences
with open('rightho.txt', 'r') as content_file:
    input = content_file.read()
    corpus = client.algo('StanfordNLP/SentenceSplit/0.1.0').pipe(input)

#  generate trigrams
input = [corpus,
        "xxBeGiN142xx",
        "xxEnD142xx",
        "data://.algo/temp/" + trigram_file_name]

trigrams_file = client.algo('ngram/GenerateTrigramFrequencies/0.1.1').pipe(input)

print "Done! Your trigrams file is now available on Algorithmia."
print trigrams_file