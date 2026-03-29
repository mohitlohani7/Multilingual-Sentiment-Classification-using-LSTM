# src/data_cleaning.py
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords', quiet=True)

def clean_text(text):
    ps = PorterStemmer()
    text = re.sub('[^a-zA-Z]', ' ', str(text))
    text = text.lower().split()
    # "not" ko mat hatao, sentiment ke liye zaroori hai!
    all_stopwords = stopwords.words('english')
    all_stopwords.remove('not') 
    
    text = [ps.stem(word) for word in text if word not in all_stopwords]
    return ' '.join(text)