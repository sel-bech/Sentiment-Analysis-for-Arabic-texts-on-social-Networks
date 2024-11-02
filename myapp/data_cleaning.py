import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.arlstem2 import ARLSTem2

nltk.download('wordnet')

# Define stop words including more common ones
additional_stop_words = ['هذا', 'هذه', 'هما', 'هم', 'هن', 'هنا', 'هناك']
stop_words = set(stopwords.words('arabic') + additional_stop_words)

# Define lemmatizer
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    if isinstance(text, str):  # Check if the input is a string
        # Remove punctuations
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        # Tokenize
        tokens = word_tokenize(text)
        # Remove stop words and lemmatize
        tokens = [lemmatizer.lemmatize(word) for word in tokens if word.lower() not in stop_words]
        # Remove numbers and single characters
        tokens = [word for word in tokens if word.isalpha() and len(word) > 1]
        return ' '.join(tokens)
    else:
        return ''
    

def process_text(text):
    stemmer = ARLSTem2()
    word_list = nltk.word_tokenize(text)
    
    # Light normalization before stemming (optional)
    word_list = [w.replace("أ", "ا").replace("ة", "ه") for w in word_list]  

    # Stemming
    word_list = [stemmer.stem(w) for w in word_list]
    return ' '.join(word_list)