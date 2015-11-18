import os
from langdetect import detect

for i in os.listdir('raw_txt'):
    if i.endswith(".txt"):


        file = open('raw_txt/' + i, "r",)
        lang = detect(file.read().encode('UTF-8'))
        print lang


        #vectorizer = text.CountVectorizer(input='raw_html/' + i, stop_words='english', min_df=1)


        continue
    else:
        continue