import re
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from stop_words import get_stop_words
import textmining


stop_words = get_stop_words('dutch')


key = 'www.gea.nl'
url = 'raw_html/' + key + '.html'
f = open(url, 'r')

# load the html doc
doc = file.read(f)

# make pure textfile
soup = BeautifulSoup(doc, 'lxml')
for script in soup(["script", "style"]):
    script.extract()    # rip it out

doc_text = soup.get_text()

# check top 20 keywords
tdm = textmining.TermDocumentMatrix()
tdm.add_doc(doc_text)

for row in tdm.rows(cutoff=1):
    print row

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


