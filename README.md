# How to generate a short story

## Step One: Find a Corpus
The corpus is the set of texts that you will be using to base your short story on. For this project, you can base your short story on just one book or you can grab a whole selection of texts from various sources to be your corpus.

If you want to base your short story on another book, try the public domain section of [Feedbooks](http://www.feedbooks.com/publicdomain). Another good site to check out is [Project Gutenberg](https://www.gutenberg.org/), which is home to over 50,000 ebooks. All of the public domain section on Feedbooks as well as most of the content on Project Gutenberg is available for you to use without infringing on copyright law. Other interesting corpuses that folks have used as a base for their generative fiction include software license agreements, personal journals, public speeches, or Wikipedia articles. It's really up to you to choose what you find most interesting!

If you use just one book or text source, your resulting generated short story will be much more similar to the original work than if you combine multiple text sources. Same goes for the corpus length. Since we are doing short stories, using a smaller corpus is just fine.

## Step Two: Generate Trigrams

Now let's get to work. The first thing you want to do with the text you have chosen is to make sure that it's in a pretty clean state. If the book or other text you've slected has copyright notices, table of contents, or other text that won't be needed in your short story, go ahead and remove that so you end up with a `.txt` file containing only the text you want to base your story on.

I decided to make a little short story based on [*Right Ho, Jeeves* by P.G. Wodehouse](https://en.wikipedia.org/wiki/Right_Ho,_Jeeves). I grabbed the book from Project Gutenberg, so there was a little bit of cleanup to do. I used [Guten-gutter](https://github.com/catseye/Guten-gutter), a python tool for cleaning up Project Gutenberg texts. 

We want to take our text and create a trigram file that we will use in step three to generate new text. The trigram model that we are building is essentially a list of word sequences, in our case sequences of 3 words, that appear in the text. [Read more about n-grams](https://en.wikipedia.org/wiki/N-gram) to get a deeper understanding of what the algorithm is constructing.

Let's walk through a short python script based on the one that I used to generate a novel for [NaNoGenMo](https://github.com/dariusk/NaNoGenMo-2015) last month. You can find the [full script here](https://github.com/algorithmiaio/shorties/tree/master/python%20examples), which you with run with `python generate-trigrams.py`. While I chose to do this in python, feel free to use the langugage you feel the most comfortable working in!

First things first, we need to import the Algorithmia client. If you haven't used Algorithmia before, give the [python docs](http://docs.algorithmia.com/?python#python-client) a quick glance. Short version: install the client with `pip install algorithmia`.

```
import Algorithmia
import os

client              = Algorithmia.client('YOUR_API_KEY_HERE')
trigram_file_name   = "right-ho-trigrams.txt"
```

As you can see, we've also set up a few variables at the start of our script to help keep things neat. Be sure to replace `YOUR_API_KEY_HERE` with the API key from your account. Find this key in your Algorithmia profile by clicking on your username in the top right-hand side of the Algorithmia site. 

To create our short story, we're going to use the algorithms [Generate Trigram Frequencies](https://algorithmia.com/algorithms/ngram/GenerateTrigramFrequencies) and [Sentence Split](https://algorithmia.com/algorithms/StanfordNLP/SentenceSplit). Because Generate Trigram Frequencies takes an array of strings, we'll run our entire text file through Sentence Split which conveniently take a block of text and returns the sentences as an array of strings. 

We first open the file and set the content as our `input` variable. On the next line, we send that input to Algorithmia by piping the input to the algorithm with `client.algo('StanfordNLP/SentenceSplit/0.1.0').pipe(input)`. This will return 
the array of sentences we need to pass into the Generate Trigram algorithm.

```
# generate array of sentences
with open('rightho.txt', 'r') as content_file:
    input   = content_file.read()
    corpus  = client.algo('StanfordNLP/SentenceSplit/0.1.0').pipe(input)
```

Now that we have the sentences, we'll pass those into the Generate Trigram Frequencies algorithm along with two tags that mark the beginning and ends of the data. The final paramater is the address of the output file in your Data section on Algorithmia (no need to modify the last three parameters, the tags can be copied and the data URL will automatically put the file into your Data!).

```
#  generate trigrams
input = [corpus,
        "xxBeGiN142xx",
        "xxEnD142xx",
        "data://.algo/temp/" + trigram_file_name]

trigrams_file = client.algo('ngram/GenerateTrigramFrequencies/0.1.1').pipe(input)

print "Done! Your trigrams file is now available on Algorithmia."
print trigrams_file
```

Ok, cool! Now we've got a trigram model that we can use to generate our short story.

## Step Three: Generate Paragraphs

While you can download the trigram file if you want, the Data API makes it easy to use it directly as an argument to the algorithm that we'll use to generate text. The algorithm to generate the trigrams returns the address of the trigram file in your Data collection. Navigate to the "My Data" section on Algorithmia where you'll find the a section for the algorithm on the left hand side. 

![my data screenshot](https://github.com/algorithmiaio/shorties/blob/master/img/Mydata.png)

You'll see the newly created trigram file already there for you to use! Copy the full address of the file listed right below the filename. We'll pass this file location to the algorithms we use next.

First, let's make sure that our trigram model will generate some text for us. I like to do a quick sanity check by going to the algorithm [Random Text From Trigram](https://algorithmia.com/algorithms/ngram/RandomTextFromTrigram) and inserting the Data address of my trigram model right in the in-broswer sample code runner. When I stuck in my trigram model, Random Text From Trigram returned "It will be killing two birds with one stone, sir.". Looks good!

Now let's set up a script to generate a whole short story:

```
import Algorithmia
import os
import re
from random import randint

client            = Algorithmia.client('YOUR_API_KEY_HERE')
trigrams_file     = 'data://.algo/ngram/GenerateTrigramFrequencies/temp/right-ho-trigrams.txt'
book_title        = 'full_book.txt'
book              = ''
book_word_length  = 7500

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
```

Be sure to update the `trigrams_file` varible with the address of your trigram file. It will look very similar, with the exception of what your named it!

Following this script, you can see that we have constructed a simple loop that checks the book length and if it is less than 7,500 words, will make a call to the algorithm [Generate Paragraph From Trigram](https://algorithmia.com/algorithms/lizmrush/GenerateParagraphFromTrigram). Again we pass in the beginning and ending tags from our trigram model, and this time we specify a paragraph length in sentences as the final parameter to our call. I let my program pick a random number between 1 and 9 with `(randint(1,9))`. 

Finally the script will write the entire book to a `.txt` file in the same directory and you're ready to start reading!

## Moving Beyond the Trigram

Now that you've got the basics down, feel free to make changes to the scripts or come up with something totally different. If you need inspiration on what kinds of books you can generate, be sure to check out the [NaNoGenMo 2015](https://github.com/dariusk/NaNoGenMo-2015) repo to see what other fiction generating programmers have come up with!

Where can you take this next? Here are some other algorithms available in the Marketplace that you might consider trying out to add some extra spice to your short story:

* [Generate Random Love Letter](https://algorithmia.com/algorithms/ngram/GenerateRandomLoveLetter)
* [Retrieve Tweets With Keyword](https://algorithmia.com/algorithms/diego/RetrieveTweetsWithKeyword) & [Retrieve Tweets By User](https://algorithmia.com/algorithms/diego/RetrieveTweetsByUser)
* [Website Summary](https://algorithmia.com/algorithms/hotels/WebsiteSummary)
* [Do Words Rhyme](https://algorithmia.com/algorithms/WebPredict/DoWordsRhyme)
* [Scrabble Anagrams](https://algorithmia.com/algorithms/faddishworm/ScrableAlgorithm) 

Spend a few minutes browsing the marketplace for other text and language related algorithms. You might find an unexpected algorithm that inspires you to try something new!

## How to submit

Ready to share? We've set up a [repository on GitHub](https://github.com/algorithmiaio/shorties) so we can read one another's stories! All you need to do is [open an issue](https://github.com/algorithmiaio/shorties/issues) on the repo with a link to your code reposity and book if you choose to host it somewhere else. You can also use the issues as a means to get help with your short story. Just comment on your issue if you are stuck or have any questions and we'll help out!
