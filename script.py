# import re
# from deep_translator import GoogleTranslator
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# import pandas as pd
# import datetime
# import snscrape.modules.twitter as sntwitter
# import psycopg2

# hoy = datetime.date.today()
# ayer = hoy - datetime.timedelta(days=1)

# scraper = sntwitter.TwitterSearchScraper(
#     f"lang:es #JH since:{ayer} until:{hoy}")
# lista = []
# for i, tweet in enumerate(scraper.get_items()):
#     if (tweet.user.username != "somosgamave"):
#         print(tweet.user.username)
#         data = [tweet.id, tweet.date, 'Twiter', tweet.url, tweet.rawContent, ]
#         lista.append(data)
#         if i > 100:
#             break

# df = pd.DataFrame(
#     lista, columns=['id', 'date', 'origen', 'direccion', 'Texto'])
# df = df.rename(columns={'Texto': 'texto'})


# def limpiar_texto(texto):
#     # Eliminar menciones
#     texto = re.sub(r'@[A-Za-z0-9_]+', '', texto)
#     # Eliminar URLs
#     texto = re.sub(r'http\S+', '', texto)
#     # Eliminar caracteres especiales y signos de puntuación
#     texto = re.sub(r'[^\w\s]', '', texto)
#     # Convertir texto a minúsculas
#     texto = texto.lower()
#     # Eliminar espacios en blanco adicionales
#     texto = re.sub(r'\s+', ' ', texto).strip()
#     return texto


# df['texto_limpio'] = df['texto'].apply(
#     lambda x: limpiar_texto(x))


# def analisis_de_sentimientos(texto):
#     textoTraducido = traduccion(texto)
#     analisis = SentimentIntensityAnalyzer()
#     vs = analisis.polarity_scores(textoTraducido)
#     valor_sub = vs['compound']
#     varlorR = round(valor_sub, 2)

#     print(varlorR)

#     if varlorR >= 0.25 and varlorR <= 1:
#         return list(["positivo", varlorR])
#     elif varlorR > -0.25 and varlorR < 0.25:
#         return list(["neutro", varlorR])
#     else:
#         return list(["negativo", varlorR])


# def traduccion(texto):
#     traductor = GoogleTranslator(source='es', target='en')
#     resultado = traductor.translate(texto)
#     return resultado.replace("range", "gama")


# df['sentimiento'] = df['texto_limpio'].apply(
#     lambda x: analisis_de_sentimientos(x))

# sentimientos = df['sentimiento'].apply(pd.Series)
# sentimientos.columns = ['sentimiento', 'puntaje']
# df = df.drop("sentimiento", axis=1)
# df = df.join(sentimientos).reset_index()
# df = df.drop("index", axis=1)

# try:
#     conn = psycopg2.connect(
#         database="pruebas_sql_py",
#         user="postgres",
#         password="francisco01"
#     )
#     cursor = conn.cursor()
#     for fila in df.itertuples():
#         cursor.execute("INSERT INTO practica (claveId, fecha, origen, direccion, texto, sentimiento, puntaje) VALUES (%s, %s, %s,%s, %s, %s, %s)",
#                        (fila.id, fila.date, fila.origen, fila.direccion, fila.texto, fila.sentimiento, fila.puntaje))
#     conn.commit()
# except Exception as err:
#     print("error", err)

# else:
#     print("se conecto exitosamente")

# conn.close()


import snscrape.modules.instagram as sninstagram
import pandas as pd
import numpy as np

data = pd.DataFrame(sninstagram.InstagramUserScraper(
    'rlozinski').get_items())
