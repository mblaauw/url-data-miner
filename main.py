#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import scrapeHtmlFile as s
import config as c
import codecs


if __name__ == '__main__':

    for i in os.listdir('raw_html'):
        try:
            #s.parseHtmlDump('raw_html/' + i, config.WORDS_TO_REMOVE_CONCAT, config.DB_CONNECTION, i)
            print i


            doc = s.htmlToCleanTxt("raw_html/" + i)
            html = codecs.open("raw_html/" + i, 'r').read()

            socials =  s.parseHtml_social(doc)
            generics =  s.parseHtml_generic(doc)
            analytics = s.parseHtml_analytics(html)
            topwords = s.parseHtml_topwords(doc, c.WORDS_TO_REMOVE_CONCAT)

            for social in socials:
                print social[0],social[1]

            for generic in generics:
                print generic[0],generic[1]

            for analytic in analytics:
                print analytic[0],analytic[1]

            print topwords

        except ImportError:
            print 1


