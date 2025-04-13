import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import nltk

# Certifique-se de ter o NLTK stopwords e punkt baixados
try:
    stopwords.words('portuguese')
except LookupError:
    nltk.download('stopwords')
try:
    word_tokenize('exemplo')
except LookupError:
    nltk.download('punkt')

# Carregar o dataset
df = pd.read_csv('spam.csv', encoding='latin-1')

# Remover colunas desnecessárias
df = df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'], axis=1)

# Renomear colunas para melhor entendimento
df = df.rename(columns={'v1': 'label', 'v2': 'text'})

# Converter a coluna 'label' para valores numéricos (spam: 1, ham: 0)
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

# Pré-processamento de texto
stop_words = set(stopwords.words('english')) # Usando stopwords em inglês, pois o dataset é em inglês

def preprocess_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
    return " ".join(tokens)

df['processed_text'] = df['text'].apply(preprocess_text)

# Divisão em conjuntos de treino e teste
X_train, X_test, y_train, y_test = train_test_split(df['processed_text'], df['label'], test_size=0.2, random_state=42)

# Vetorização do texto usando TF-IDF
tfidf_vectorizer = TfidfVectorizer()
X_train_tfidf = tfidf_vectorizer.fit_transform(X_train)
X_test_tfidf = tfidf_vectorizer.transform(X_test)

# Treinamento do modelo Naive Bayes
model = MultinomialNB()
model.fit(X_train_tfidf, y_train)

# Previsões no conjunto de teste
y_pred = model.predict(X_test_tfidf)

# Avaliação do modelo
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("Resultados da Avaliação:")
print(f"Acurácia: {accuracy:.4f}")
print(f"Precisão: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1-score: {f1:.4f}")

# Função para classificar novas mensagens
def classify_message(text):
    processed_text = preprocess_text(text)
    text_tfidf = tfidf_vectorizer.transform([processed_text])
    prediction = model.predict(text_tfidf)[0]
    return "spam" if prediction == 1 else "não spam"

# Exemplos de classificação de novas mensagens
new_messages = [
    "Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&Cs apply 08452810075over18s",
    "Hi how are you doing today?",
    "URGENT! You have won a 1 week FREE membership in our $100000 Prize Jackpot! Txt the word: CLAIM to No: 87239 to claim your prize!",
    "Okay, I'll call you later."
]

print("\nClassificação de Novas Mensagens:")
for message in new_messages:
    classification = classify_message(message)
    print(f"Mensagem: '{message}' -> Classificação: {classification}")