import os, codecs
from bs4 import BeautifulSoup
import chardet
import urllib

rawdata = urllib.urlopen('http://yahoo.co.jp/').read()
print chardet.detect(rawdata)


for i in os.listdir('raw_html'):
    if i.endswith(".html"):
        o = i.replace('.html','.txt')

        url = "http://" + "raw_html/" + i.replace('.html','')

        codepage = chardet.detect(urllib.urlopen(url).read())['encoding']

        if codepage == 'utf-8':
            f = codecs.open("raw_html/" + i, "rb","utf-8")
        if codepage == 'ISO-8859-2':
            f = codecs.open("raw_html/" + i, "rb","ISO-8859-2")
        else:
            f = codecs.open("raw_html/" + i, "rb","ascii")

        doc = f.read()

        print i, codepage

        # make soup, strip scripts and convert to text
        soup = BeautifulSoup(str(doc), 'lxml')
        for script in soup(["script", "style"]):
            script.extract()

        doc_text = soup.get_text()

        if codepage == 'utf-8':
            f = codecs.open('raw_txt/' + o, "w","utf-8")
        if codepage == 'ISO-8859-2':
            f = codecs.open('raw_txt/' + o, "w","ISO-8859-2")
        else:
            f = codecs.open('raw_txt/' + o, "w","ascii")

        f.write(doc_text)
