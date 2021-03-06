#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import scrapeHtmlFile as s
import config as c
import codecs
import requests
from datetime import timedelta
import re

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.101 Chrome/45.0.2454.101 Safari/537.36',
           'Accept-Language': 'en-US,en;q=0.8,nl;q=0.6',
           'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

f = open('urlList.txt','r')

for line in f.read().split('\n'):
    url = 'http://' + line

    try:
        r = requests.get(url, headers=headers, timeout=5, allow_redirects=True)

        codePage = unicode( r.encoding )
        serverType = unicode( r.headers.get('server') )
        redirectUrl = unicode( r.url )
        timeElapsed = unicode( timedelta(microseconds=r.elapsed.microseconds) )

        html = r.content
        technology = s.parseHtml_technology( html )

        html_text = s.htmlToTxt_object( html )

        keywords = s.parseHtml_topwords(html_text, c.WORDS_TO_REMOVE_CONCAT)

        # store in the database
        s.storeBasicUrlInfo(c.DB_FILE_PATH, url, redirectUrl, codePage, serverType, timeElapsed)
        #print url, redirectUrl, codePage, serverType, timeElapsed

        print redirectUrl
        for tech in technology:
            if tech[1] == ['TRUE']:
                print tech[0]

        print keywords

        links_dirty = s.getLocalLinksFromHtml( html )
        links_clean = []

        # for link in links_dirty:
        #     if link[:1] == '/':
        #         links_clean.append( redirectUrl + link )
        #     elif link.find(line) != -1:
        #         links_clean.append(link)
        #
        # totalLinks = len(links_clean)
        #
        # for link in links_clean:
        #     print link
        #     r = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        #     html = r.content
        #
        #     html_text = s.htmlToTxt_object( html )




        #print analytics

    except requests.exceptions.ConnectionError as e:
        x = 1
        #print "BOOM!" + str(e)




    # open home page html

        # detect technology
        # store in database

    # collect all links

    # make unique

    # take a sample of links N

    # crawl links one by one

        # parse per page
        # keep adding to lists

    # store list in db

    #print line

f.close()






exit()
if __name__ == '__main__':

    for i in os.listdir('raw_html'):
        try:
            #s.parseHtmlDump('raw_html/' + i, config.WORDS_TO_REMOVE_CONCAT, config.DB_CONNECTION, i)
            print i


            doc = s.htmlToCleanTxt("raw_html/" + i)
            html = codecs.open("raw_html/" + i, 'r').read()

            topwords = s.parseHtml_topwords(doc, c.WORDS_TO_REMOVE_CONCAT)
            socials =  s.parseHtml_social(doc)
            generics =  s.parseHtml_generic(doc)
            analytics = s.parseHtml_technology(html)

            topwords

            for social in socials:
                print social[0],social[1]

            for generic in generics:
                print generic[0],generic[1]

            for analytic in analytics:
                print analytic[0],analytic[1]



        except ImportError:
            print 1


