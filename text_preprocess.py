# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import spacy
import unidecode
from word2number import w2n
import contractions
import re
import unicodedata
import inflect
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)

def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def remove_between_square_brackets(text):
    return re.sub('\[[^]]*\]', '', text)

def denoise_text(text):
    text = strip_html(text)
    text = remove_between_square_brackets(text)
    return text
def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words =''
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words+=new_word
    return new_words
def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = ''
    for word in words:
        new_word = word.lower()
        new_words+=new_word
    return new_words
def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words =''
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words+=new_word
    return new_words
def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = ''
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words+=new_word
        else:
            new_words+=word
    return new_words
def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = LancasterStemmer()
    stems = ''
    for word in words:
        stem = stemmer.stem(word)
        stems+=stem
    return stems

def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = ''
    for word in words:
        lemma = lemmatizer.lemmatize(word, pos='v')
        lemmas+=lemma
    return lemmas

def normalize(words):
    words = denoise_text(words)
    words = replace_contractions(words)
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    #words = replace_numbers(words)
    #words = stem_words(words)
    #words = lemmatize_verbs(words)
    #words = remove_stopwords(words)
    return words
#words ="I'd like to have three cups   of coffee<br /><br /> from your Café. #delicious"

# print(normalize(words))
