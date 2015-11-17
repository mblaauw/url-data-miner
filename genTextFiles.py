import os
from bs4 import BeautifulSoup

for i in os.listdir('raw_html'):
    if i.endswith(".html"):
        o = i.replace('.html','.txt')

        file = open('raw_html/' + i, "r",)

        doc = file.read()

        soup = BeautifulSoup(doc, 'lxml')

        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        doc_text = soup.get_text()

        file = open('raw_txt/' + o, "w",)
        file.write(doc_text.encode('UTF-8'))

        continue
    else:
        continue