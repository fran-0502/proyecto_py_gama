from sentiment_analysis_spanish import sentiment_analysis
from deep_translator import GoogleTranslator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from tqdm.notebook import tqdm
import snscrape.modules.twitter as sntwitter
import plotly.graph_objects as go
from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSequenceClassification

#  ============================================================================
#  =========================== text mining =============================
#  ============================================================================


# scraper = sntwitter.TwitterSearchScraper("lang:es #HogwartsLegacy")
# lista = []
# for i, tweet in enumerate(scraper.get_items()):
#     if (tweet.user.username != "somosgamave"):
#         print(tweet.user.username)
#         data = tweet.rawContent
#         lista.append(data)
#         if i > 400:
#             break

# df = pd.DataFrame(lista, columns=['Texto'])
# df.to_excel('hogward.xlsx', index=False)


df = pd.read_excel("hogward.xlsx")
df = df.rename(columns={'Texto': 'texto'})


def analisis_de_sentimientos(texto):
    textoTraducido = traduccion(texto)
    analisis = SentimentIntensityAnalyzer()
    vs = analisis.polarity_scores(textoTraducido)
    valor_sub = vs['compound']
    varlorR = round(valor_sub, 2)

    print(varlorR)

    if varlorR >= 0.25 and varlorR <= 1:
        return list(["positivo", varlorR])
    elif varlorR > -0.25 and varlorR < 0.25:
        return list(["neutro", varlorR])
    else:
        return list(["negativo", varlorR])


def traduccion(texto):
    traductor = GoogleTranslator(source='es', target='en')
    resultado = traductor.translate(texto)
    return resultado.replace("range", "gama")


df['sentimiento'] = df['texto'].apply(
    lambda x: analisis_de_sentimientos(x))

sentimientos = df['sentimiento'].apply(pd.Series)
sentimientos.columns = ['sentimiento', 'puntaje']
df = df.drop("sentimiento", axis=1)
df = df.join(sentimientos).reset_index()
df = df.drop("index", axis=1)

df.to_excel('hogward.xls', index=False)
