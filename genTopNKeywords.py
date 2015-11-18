import os
import codecs
from langdetect import detect

for i in os.listdir('raw_txt'):
    if i.endswith(".txt"):
        with codecs.open ("raw_txt/" + i, "r", "utf-8") as f:
            data=f.read().replace('\n', ' ')

        print data
        lang = detect(data)
        print lang


        #vectorizer = text.CountVectorizer(input='raw_html/' + i, stop_words='english', min_df=1)


        continue
    else:
        continue