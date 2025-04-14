import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.naive_bayes import MultinomialNB
import nltk


try:
    stopwords.words('portuguese')
except LookupError:
    nltk.download('stopwords')
try:
    word_tokenize("exemplo")
except LookupError:
    nltk.download('punkt')

try:
    df = pd.read_csv('spam.csv', encoding='latin-1')
except FileNotFoundError:
    print("Erro: O arquivo 'spam.csv' não foi encontrado. Certifique-se de que ele está no mesmo diretório do script ou forneça o caminho correto.")
    exit()

df = df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1)

df = df.rename(columns={'v1': 'label', 'v2': 'text'})


df['label_numeric'] = df['label'].map({'ham': 0, 'spam': 1})

stop_words = set(stopwords.words('portuguese'))

def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return " ".join(tokens)

df['processed_text'] = df['text'].apply(preprocess_text)

tfidf_vectorizer = TfidfVectorizer()

tfidf_matrix = tfidf_vectorizer.fit_transform(df['processed_text'])

model = MultinomialNB()
model.fit(tfidf_matrix, df['label_numeric'])

def classify_single_message(text, model, vectorizer):
    processed_text = preprocess_text(text)
    vectorized_text = vectorizer.transform([processed_text])
    prediction_numeric = model.predict(vectorized_text)[0]
    prediction_label = "spam" if prediction_numeric == 1 else "não spam"
    return prediction_label

df['predicted_label'] = df['text'].apply(lambda x: classify_single_message(x, model, tfidf_vectorizer))

print(df[['text', 'label', 'predicted_label']].head())

#df.to_csv('spam_classified.csv', index=False)

print("\nAs mensagens dentro do 'spam.csv' foram classificadas na coluna 'predicted_label'.")
print("As primeiras linhas com a classificação são mostradas acima.")
