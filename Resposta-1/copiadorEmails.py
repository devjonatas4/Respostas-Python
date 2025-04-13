import re

def extrair_e_separar_email(texto):
    padrao_email = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    email = re.search(padrao_email, texto)

    if email:
        email_extraido = email.group()
        texto_sem_email = texto.replace(email_extraido, '').strip()
        usuario, dominio = email_extraido.split("@")
        return {
            "email": email_extraido,
            "usuario": usuario,
            "dominio": dominio,
            "texto_sem_email": texto_sem_email
        }
    else:
        return {
            "email": None,
            "usuario": None,
            "dominio": None,
            "texto_sem_email": texto
        }
    
