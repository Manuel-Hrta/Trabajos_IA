import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Cargar los tweets desde el archivo CSV
df = pd.read_csv('tweets.csv')
tweets = df['tweet'].to_list()

# Tokenización de palabras
text = ''.join(tweets)
tokens = nltk.word_tokenize(text)
text2 = nltk.Text(tokens)

# Análisis de sentimientos con NLTK
analizador = SentimentIntensityAnalyzer()

for twit in text2:
    print(twit)
    scores = analizador.polarity_scores(twit)
    for key in scores:
        print(f"{key}: {scores[key]}")
    print()
