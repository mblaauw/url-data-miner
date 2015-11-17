import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from stop_words import get_stop_words
import textmining
import sklearn.feature_extraction.text as text
import numpy as np  # a conventional alias
import gensim

stop_words = get_stop_words('en')

key = 'www.ambitiouspeoplecareers.com'
url = 'raw_html/' + key + '.html'
f = open(url, 'r')

# load the html doc
doc = file.read(f)

# make pure textfile
soup = BeautifulSoup(doc, 'lxml')
for script in soup(["script", "style"]):
    script.extract()    # rip it out

doc_text = soup.get_text()
file = open("raw_txt/tmp.txt", "w",)
file.write(doc_text.encode('UTF-8'))

import sklearn.feature_extraction.text as text
import os
from sklearn import decomposition

CORPUS_PATH = os.path.join('raw_txt')

filenames = sorted([os.path.join(CORPUS_PATH, fn) for fn in os.listdir(CORPUS_PATH)])

vectorizer = text.CountVectorizer(input='filename', stop_words='english', min_df=1)

dtm = vectorizer.fit_transform(filenames).toarray()

vocab = np.array(vectorizer.get_feature_names())

num_topics = 5

num_top_words = 20

clf = decomposition.NMF(n_components=num_topics, random_state=1)

doctopic = clf.fit_transform(dtm)

topic_words = []

for topic in clf.components_:
    word_idx = np.argsort(topic)[::-1][0:num_top_words]
    topic_words.append([vocab[i] for i in word_idx])

doctopic = doctopic / np.sum(doctopic, axis=1, keepdims=True)


for t in range(len(topic_words)):
    print(u"Topic {}: {}".format(t, ' '.join(topic_words[t][:15])))

url_names = []

for fn in filenames:
    basename = os.path.basename(fn)
    name, ext = os.path.splitext(basename)
    url_names.append(name)

url_names = np.asarray(url_names)

print url_names

doctopic_orig = doctopic.copy()

num_groups = len(set(url_names))

doctopic_grouped = np.zeros((num_groups, num_topics))

for i, name in enumerate(sorted(set(url_names))):
    doctopic_grouped[i, :] = np.mean(doctopic[url_names == name, :], axis=0)

doctopic = doctopic_grouped

urls = sorted(set(url_names))

print("Top NMF topics in...")

for i in range(len(doctopic)):
   top_topics = np.argsort(doctopic[i,:])[::-1][0:3]
   top_topics_str = ' '.join(str(t) for t in top_topics)
   print("{}: {}".format(urls[i], top_topics_str))

# show the top 15 words
for t in range(len(topic_words)):
   print(u"Topic {}: {}".format(t, ' '.join(topic_words[t][:15])))


exit()


# make a wordcloud
wordcloud = WordCloud(
    font_path='/Users/blaauw/Library/Fonts/CabinSketch-Bold.ttf',
    stopwords=stop_words,
    background_color='white',
    width=800,
    height=600).generate(doc_text)

plt.imshow(wordcloud)
plt.axis('off')
plt.savefig('./www.gea.nl.png', dpi=150)
#plt.show()

# keyword detection


# basic info detection
email = re.findall('([A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+[a-zA-Z])', doc)
phone = re.findall('(\d{1,4}[\s-]\d{6,8})', doc)
zipcode = re.findall('([1-9][0-9]{3}\s?[a-zA-Z]{2})\s', doc)
btwnr = re.findall('([NL]{2}[0-9]{2,}[B][0-9]{2})', doc)


# social detections
linkedin = re.findall('(?:https?:\/\/)?(?:www\.)?linkedin\.com\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)', doc)
facebook = re.findall('(?:https?:\/\/)?(?:www\.)?facebook\.com\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)', doc)
twitter = re.findall('(?:https?:\/\/)?(?:www\.)?twitter\.com\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)', doc)
youtube = re.findall('(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)', doc)
pinterest = re.findall('(?:https?:\/\/)?(?:www\.)?pinterest\.com\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)', doc)


# technology detection
v_googleAnalytics = re.findall('(google-analytics)', doc)
v_openGraphProtocol = re.findall('(ogp.me)', doc)
v_googleTagService = re.findall('(www.googletagmanager.com)', doc)
v_googleLeadServices = re.findall('(googleadservices)', doc)
v_quoteCast = re.findall('(quotecast.vwdservices.com)', doc)
v_chartBeat = re.findall('(chartbeat.com)', doc)
v_adobeDpm = re.findall('(dpm.demdex.bet)', doc)
v_messagent = re.findall('(messagent.)', doc)
v_graydonLeadInsights = re.findall('(leadinsights.graydon-global.com)', doc)
v_visualRevenue = re.findall('(visualrevenue.com)', doc)
v_brightCove = re.findall('(brightcove.com)', doc)
v_hotJar = re.findall('(hotjar.com)', doc)
v_usaBilla = re.findall('(usabilla.com)', doc)
v_shoppingMinds = re.findall('(shoppingminds.com)', doc)
v_celeraOne = re.findall('(celeraone.com)', doc)
v_adHese = re.findall('(adhese.com)', doc)

v_wordPress = re.findall('(wp-content)', doc)


# DEBUG PRINT - NEED DB STORAGE
print filter(None, list(set(email)))
print filter(None, list(set(phone)))
print filter(None, list(set(zipcode)))
print filter(None, list(set(btwnr)))
print filter(None, list(set(linkedin)))
print filter(None, list(set(facebook)))
print filter(None, list(set(twitter)))
print filter(None, list(set(youtube)))
print filter(None, list(set(pinterest)))
print filter(None, list(set(v_googleAnalytics)))
print filter(None, list(set(v_openGraphProtocol)))
print filter(None, list(set(v_googleTagService)))
print filter(None, list(set(v_googleLeadServices)))
print filter(None, list(set(v_quoteCast)))
print filter(None, list(set(v_chartBeat)))
print filter(None, list(set(v_adobeDpm)))
print filter(None, list(set(v_messagent)))
print filter(None, list(set(v_graydonLeadInsights)))
print filter(None, list(set(v_visualRevenue)))
print filter(None, list(set(v_brightCove)))
print filter(None, list(set(v_hotJar)))
print filter(None, list(set(v_usaBilla)))
print filter(None, list(set(v_shoppingMinds)))
print filter(None, list(set(v_celeraOne)))
print filter(None, list(set(v_adHese)))
print filter(None, list(set(v_wordPress)))


