import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer,WordNetLemmatizer
from word2number import w2n

nltk.download('wordnet')
nltk.download('omw-1.4')

string="The weather isn't good, it's raining, two three 3 four"
words=word_tokenize(string)
stemmer=PorterStemmer()
lemmatizer=WordNetLemmatizer()

stemmed_words=[stemmer.stem(word) for word in words]

lemmatized_words=[lemmatizer.lemmatize(word) for word in stemmed_words]

normalized_words=[]
for word in lemmatized_words:
    try:
        normalized_words.append(str(w2n.word_to_num(word)))
    except ValueError:
        normalized_words.append(word)

print(normalized_words)