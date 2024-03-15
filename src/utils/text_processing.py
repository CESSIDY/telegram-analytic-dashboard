import os
import re
import string

import pandas as pd

stopwords_path = os.path.abspath(os.path.join(os.path.realpath(__file__), "..", "..", "..", "data", "stopwords"))
stopwords_custom_languages = ['ukrainian']


def custom_stopwords(language):
    files_paths = {'ukrainian': os.path.join(stopwords_path, 'stopwords_ua.txt')}
    if language not in stopwords_custom_languages:
        return []
    stopwords = pd.read_csv(files_paths[language], header=None, names=['words'])
    return list(stopwords.words)


def clean_text_from_stopwords(text, stopwords):
    text = "".join([word for word in text if word not in string.punctuation])
    tokens = re.split('\W+', text)
    test_words = [word for word in tokens if word not in stopwords]
    return ' '.join(test_words).strip()
