import pandas as pd

# Criar dados para o CSV
data = {
    'v1': ['ham', 'spam', 'ham', 'spam', 'ham'],
    'v2': [
        'Hello, how are you?',
        'Win $1000 now!',
        'Let’s meet tomorrow.',
        'Congratulations, you’ve won a prize!',
        'Can you call me later?'
    ]
}

# Criar um DataFrame
df = pd.DataFrame(data)

# Salvar o DataFrame como arquivo CSV
df.to_csv('spam.csv', index=False, encoding='latin-1')

print("Arquivo CSV criado com sucesso!")
