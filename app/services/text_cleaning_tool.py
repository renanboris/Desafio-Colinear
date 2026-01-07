import re
import unicodedata

def clean_text(text):
    """
    Limpeza de texto do arquivo removendo acentos, pontuação e stopwords.
    """
    if not isinstance(text, str):
        return ""

    text = text.lower() 
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    text = re.sub(r'[^a-z0-9\s]', '', text)

    stopwords = {'de', 'do', 'da', 'dos', 'das', 'em', 'na', 'no', 'com', 'para', 'pelo', 'pela'}
    palavras = [p for p in text.split() if p not in stopwords]
    
    return " ".join(palavras)
