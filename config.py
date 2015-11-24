#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
from stop_words import get_stop_words
import sqlite3 as lite

DB_FILE_PATH            = 'db/data.db'
DB_CONNECTION           = lite.connect(DB_FILE_PATH)

with codecs.open('word_lists/wordsToRemove_en_nl.txt','r', 'UTF-8') as f:
    WORDS_TO_REMOVE_EN_NL = f.read().splitlines()

WORDS_STOP_NL           = get_stop_words('nl')
WORDS_STOP_EN           = get_stop_words('en')

WORDS_TO_REMOVE_CONCAT  = WORDS_TO_REMOVE_EN_NL + WORDS_STOP_NL + WORDS_STOP_EN
WORDS_TO_REMOVE_CONCAT  = set(WORDS_TO_REMOVE_CONCAT)


KEY_NAME                = 'www.gea.nl'
FILE_TO_PARSE           = 'raw_html/' + KEY_NAME + '.html'

