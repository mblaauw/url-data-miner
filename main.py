#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import scrapeHtmlFile as s
import config



if __name__ == '__main__':

    for i in os.listdir('raw_html'):
        try:
            s.parseHtmlDump('raw_html/' + i, config.WORDS_TO_REMOVE_CONCAT, config.DB_CONNECTION, i)
        except ImportError:
            print 1

