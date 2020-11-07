from stop_words import get_stop_words
from wordcloud import WordCloud

texto = "Quijote.txt"

text = open(texto, "r", encoding="utf-8").read()
palabras_no = get_stop_words("es")

wc = WordCloud(max_words=25, stopwords=palabras_no, background_color="black")
wc.generate(text)
wc.to_file("worldcloud.png")
