import Algorithmia
import os
import re
from random import randint

client            	= Algorithmia.client('YOUR_API_KEY_HERE')
trigrams_file 		= 'data://.algo/ngram/GenerateTrigramFrequencies/temp/right-ho-trigrams.txt'
book_title	 		= 'full_book.txt'
book 				= ''
book_word_length 	= 7500

while len(re.findall(r'\w+', book)) < book_word_length:
  print "Generating new paragraph..."
  input = [trigrams_file, "xxBeGiN142xx", "xxEnD142xx", (randint(1,9))]
  new_paragraph = client.algo('/lizmrush/GenerateParagraphFromTrigram').pipe(input)
  book += new_paragraph
  book += '\n\n'
  print "Updated word count:"
  print len(re.findall(r'\w+', book))

with open(book_title, 'w') as f:
    f.write(book.encode('utf8'))

f.close()

print "Done!"
print "You book is now complete. Give " + book_title + " a read now!"
