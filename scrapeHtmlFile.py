#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import sqlite3 as lite
import html2text
from stop_words import get_stop_words
import codecs
import re



###########################################################################################################
## CONFIG VARS
###########################################################################################################

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


###########################################################################################################
## PARSE THE URL
###########################################################################################################

# open file
doc = codecs.open(FILE_TO_PARSE, 'r').read()

# load the html doc
h = html2text.HTML2Text()
doc_text = h.handle(doc.decode('utf8'))

print doc_text
#print doc_text
for word in WORDS_STOP_NL:
    doc_text = doc_text.replace(word, '')

print doc_text

exit()

# cleanup the text
pattern = re.compile("(" + WORDS_TO_REMOVE_EN_NL + ")\W", re.I)
pattern = re.compile("(" + WORDS_STOP_EN + ")\W", re.I)
pattern = re.compile("(" + WORDS_STOP_NL + ")\W", re.I)




#print map(lambda phrase: pattern.sub("", phrase),  doc_text)

doc_text.replace(WORDS_TO_REMOVE_EN_NL, '')
doc_text.replace(WORDS_STOP_NL, '')
doc_text.replace(WORDS_STOP_EN, '')



exit()





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





def detectTechnology(find_string, input_doc):
    found = re.findall(find_string, input_doc)
    if len(found) != 0:
        return ['TRUE']
    else:
        return []


# technology detection
v_googleAnalytics = detectTechnology('(google-analytics)', doc)
v_openGraphProtocol = detectTechnology('(ogp.me)', doc)
v_googleTagService = detectTechnology('(www.googletagmanager.com)', doc)
v_googleLeadServices = detectTechnology('(googleadservices)', doc)
v_quoteCast = detectTechnology('(quotecast.vwdservices.com)', doc)
v_chartBeat = detectTechnology('(chartbeat.com)', doc)
v_adobeDpm = detectTechnology('(dpm.demdex.bet)', doc)
v_messagent = detectTechnology('(messagent.)', doc)
v_graydonLeadInsights = detectTechnology('(leadinsights.graydon-global.com)', doc)
v_visualRevenue = detectTechnology('(visualrevenue.com)', doc)
v_brightCove = detectTechnology('(brightcove.com)', doc)
v_hotJar = detectTechnology('(hotjar.com)', doc)
v_usaBilla = detectTechnology('(usabilla.com)', doc)
v_shoppingMinds = detectTechnology('(shoppingminds.com)', doc)
v_celeraOne = detectTechnology('(celeraone.com)', doc)
v_adHese = detectTechnology('(adhese.com)', doc)
v_wordPress = detectTechnology('(wp-content)', doc)


###########################################################################################################
## STORE IN DATABASE
###########################################################################################################

def addToKeyDim(key_name, connection_name, table_name):
    query_create_table = "create table if not exists " + table_name + " (key CHAR(120) PRIMARY KEY)"
    query_delete = "DELETE FROM " + table_name + " WHERE key = '" + key_name + "'"
    query_insert = "INSERT INTO " + table_name + "(key) VALUES (?)"

    params = (key_name,)

    with connection_name:
        cur = connection_name.cursor()
        cur.execute(query_create_table)
        cur.execute(query_delete)
        cur.execute(query_insert, params)
        cur.close()


def storeInDb(key_name, data, connection_name, table_name):

    data = set(data)

    if len(data) != 0:
        query_insert = "INSERT INTO " + table_name + "(key, value) VALUES (?,?)"
        query_delete = "DELETE FROM " + table_name + " WHERE key = '" + key_name + "'"
        query_create_table = "create table if not exists " + table_name + " (key CHAR(120) PRIMARY KEY, value TEXT)"

        params = (key_name, "|".join(data))

        with connection_name:
            cur = connection_name.cursor()
            cur.execute(query_create_table)
            cur.execute(query_delete)
            cur.execute(query_insert, params)
            cur.close()


addToKeyDim(KEY_NAME, DB_CONNECTION, "d_urlKeys")

storeInDb(KEY_NAME, email, DB_CONNECTION, "f_email")
storeInDb(KEY_NAME, phone, DB_CONNECTION, "f_phone")
storeInDb(KEY_NAME, zipcode, DB_CONNECTION, "f_zipcode")
storeInDb(KEY_NAME, btwnr, DB_CONNECTION, "f_btwnr")
storeInDb(KEY_NAME, linkedin, DB_CONNECTION, "f_linkedin")
storeInDb(KEY_NAME, facebook, DB_CONNECTION, "f_facebook")
storeInDb(KEY_NAME, twitter, DB_CONNECTION, "f_twitter")
storeInDb(KEY_NAME, youtube, DB_CONNECTION, "f_youtube")
storeInDb(KEY_NAME, pinterest, DB_CONNECTION, "f_pinterest")

storeInDb(KEY_NAME, v_googleAnalytics, DB_CONNECTION, "f_googleAnalytics")
storeInDb(KEY_NAME, v_openGraphProtocol, DB_CONNECTION, "f_openGraphProtocol")
storeInDb(KEY_NAME, v_googleTagService, DB_CONNECTION, "f_googleTagService")
storeInDb(KEY_NAME, v_googleLeadServices, DB_CONNECTION, "f_googleLeadServices")
storeInDb(KEY_NAME, v_quoteCast, DB_CONNECTION, "f_quoteCast")
storeInDb(KEY_NAME, v_chartBeat, DB_CONNECTION, "f_chartBeat")
storeInDb(KEY_NAME, v_adobeDpm, DB_CONNECTION, "f_adobeDpm")
storeInDb(KEY_NAME, v_messagent, DB_CONNECTION, "f_messagent")
storeInDb(KEY_NAME, v_graydonLeadInsights, DB_CONNECTION, "f_graydonLeadInsights")
storeInDb(KEY_NAME, v_visualRevenue, DB_CONNECTION, "f_visualRevenue")
storeInDb(KEY_NAME, v_brightCove, DB_CONNECTION, "f_brightCove")
storeInDb(KEY_NAME, v_hotJar, DB_CONNECTION, "f_hotJar")
storeInDb(KEY_NAME, v_usaBilla, DB_CONNECTION, "f_usaBilla")
storeInDb(KEY_NAME, v_shoppingMinds, DB_CONNECTION, "f_shoppingMinds")
storeInDb(KEY_NAME, v_celeraOne, DB_CONNECTION, "f_celeraOne")
storeInDb(KEY_NAME, v_adHese, DB_CONNECTION, "f_adHese")
storeInDb(KEY_NAME, v_wordPress, DB_CONNECTION, "f_wordPress")
storeInDb(KEY_NAME, v_hotJar, DB_CONNECTION, "f_hotJar")
