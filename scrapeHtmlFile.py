#!/usr/bin/python
# -*- coding: utf-8 -*-

import html2text

import codecs
import re
from collections import Counter



###########################################################################################################
## PARSE THE URL
###########################################################################################################
def detectTechnology(find_string, input_doc):
    found = re.findall(find_string, input_doc)
    if len(found) != 0:
        return ['TRUE']
    else:
        return []

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

def parseHtmlDump(file_to_parse, words_to_remove, db_connection, key_name):

    doc = codecs.open(file_to_parse, 'r').read()

    # load the html doc
    h = html2text.HTML2Text()

    try:
        doc_text = h.handle(doc.decode('utf-8'))
    except IOError:
        try:
            doc_text = h.handle(doc.decode('latin-1'))
        except IOError:
            print "do nothing"

    # avoid having to regexp html
    doc = doc_text

    # remove links, remove strange chars, remove numbers, split in one big string
    doc_text = re.sub(u'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', doc_text, flags=re.MULTILINE)
    doc_text = re.sub(u'[^\w]+', ' ', doc_text, flags=re.UNICODE)
    doc_text = re.sub(u'[0-9]+', ' ', doc_text, flags=re.UNICODE)
    doc_text = doc_text.split(" ")

    # make a wordlist and remove cleanup words
    words = []
    for word in doc_text:
        if not any(word.lower() in s for s in words_to_remove):
            words.append(word)


    top20words = Counter(words).most_common(20)

    top_words = []
    for i, item in enumerate(top20words):
        top_words.append(tuple(item)[0])

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

    # Store it all in the database
    addToKeyDim(key_name, db_connection, "d_urlKeys")
    storeInDb(key_name, top_words, db_connection, "f_topwords")
    storeInDb(key_name, email, db_connection, "f_email")
    storeInDb(key_name, phone, db_connection, "f_phone")
    storeInDb(key_name, zipcode, db_connection, "f_zipcode")
    storeInDb(key_name, btwnr, db_connection, "f_btwnr")
    storeInDb(key_name, linkedin, db_connection, "f_linkedin")
    storeInDb(key_name, facebook, db_connection, "f_facebook")
    storeInDb(key_name, twitter, db_connection, "f_twitter")
    storeInDb(key_name, youtube, db_connection, "f_youtube")
    storeInDb(key_name, pinterest, db_connection, "f_pinterest")

    storeInDb(key_name, v_googleAnalytics, db_connection, "f_googleAnalytics")
    storeInDb(key_name, v_openGraphProtocol, db_connection, "f_openGraphProtocol")
    storeInDb(key_name, v_googleTagService, db_connection, "f_googleTagService")
    storeInDb(key_name, v_googleLeadServices, db_connection, "f_googleLeadServices")
    storeInDb(key_name, v_quoteCast, db_connection, "f_quoteCast")
    storeInDb(key_name, v_chartBeat, db_connection, "f_chartBeat")
    storeInDb(key_name, v_adobeDpm, db_connection, "f_adobeDpm")
    storeInDb(key_name, v_messagent, db_connection, "f_messagent")
    storeInDb(key_name, v_graydonLeadInsights, db_connection, "f_graydonLeadInsights")
    storeInDb(key_name, v_visualRevenue, db_connection, "f_visualRevenue")
    storeInDb(key_name, v_brightCove, db_connection, "f_brightCove")
    storeInDb(key_name, v_hotJar, db_connection, "f_hotJar")
    storeInDb(key_name, v_usaBilla, db_connection, "f_usaBilla")
    storeInDb(key_name, v_shoppingMinds, db_connection, "f_shoppingMinds")
    storeInDb(key_name, v_celeraOne, db_connection, "f_celeraOne")
    storeInDb(key_name, v_adHese, db_connection, "f_adHese")
    storeInDb(key_name, v_wordPress, db_connection, "f_wordPress")
    storeInDb(key_name, v_hotJar, db_connection, "f_hotJar")


def htmlToCleanTxt(html_file):

    f = codecs.open(html_file, 'r').read()

    # load the html doc
    h = html2text.HTML2Text()

    try:
        doc_text = h.handle(f.decode('utf-8'))
    except Exception:
        doc_text = h.handle(f.decode('windows-1252'))
    else:
        doc_text = h.handle(f.decode('latin-1'))

    return unicode(h)


def parseHtml_social(text):
    linkedin = re.findall('(?:https?:\/\/)?(?:www\.)?linkedin\.com\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)', text)
    facebook = re.findall('(?:https?:\/\/)?(?:www\.)?facebook\.com\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)', text)
    twitter = re.findall('(?:https?:\/\/)?(?:www\.)?twitter\.com\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)', text)
    youtube = re.findall('(?:https?:\/\/)?(?:www\.)?youtube\.com\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)', text)
    pinterest = re.findall('(?:https?:\/\/)?(?:www\.)?pinterest\.com\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)', text)

    l = []
    l.append([u"linkedin","|".join(set(linkedin))])
    l.append([u"facebook","|".join(set(facebook))])
    l.append([u"twitter","|".join(set(twitter))])
    l.append([u"youtube","|".join(set(youtube))])
    l.append([u"pinterest","|".join(set(pinterest))])

    return l


def parseHtml_generic(text):
    # basic info detection
    email = re.findall('([A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+[a-zA-Z])', text)
    phone = re.findall('(\d{1,4}[\s-]\d{6,8})', text)
    zipcode = re.findall('([1-9][0-9]{3}\s?[a-zA-Z]{2})\s', text)
    btwnr = re.findall('([NL]{2}[0-9]{2,}[B][0-9]{2})', text)

    l = []
    l.append([u"email","|".join(set(email))])
    l.append([u"phone","|".join(set(phone))])
    l.append([u"zipcode","|".join(set(zipcode))])
    l.append([u"btwnr","|".join(set(btwnr))])

    return l


def parseHtml_analytics(html):
    # technology detection
    googleAnalytics = detectTechnology('(google-analytics)', html)
    openGraphProtocol = detectTechnology('(ogp.me)', html)
    googleTagService = detectTechnology('(www.googletagmanager.com)', html)
    googleLeadServices = detectTechnology('(googleadservices)', html)
    quoteCast = detectTechnology('(quotecast.vwdservices.com)', html)
    chartBeat = detectTechnology('(chartbeat.com)', html)
    adobeDpm = detectTechnology('(dpm.demdex.bet)', html)
    messagent = detectTechnology('(messagent.)', html)
    graydonLeadInsights = detectTechnology('(leadinsights.graydon-global.com)', html)
    visualRevenue = detectTechnology('(visualrevenue.com)', html)
    brightCove = detectTechnology('(brightcove.com)', html)
    hotJar = detectTechnology('(hotjar.com)', html)
    usaBilla = detectTechnology('(usabilla.com)', html)
    shoppingMinds = detectTechnology('(shoppingminds.com)', html)
    celeraOne = detectTechnology('(celeraone.com)', html)
    adHese = detectTechnology('(adhese.com)', html)
    wordPress = detectTechnology('(wp-content)', html)

    l = []
    l.append([u"googleAnalytics",googleAnalytics])
    l.append([u"openGraphProtocol",openGraphProtocol])
    l.append([u"googleTagService",googleTagService])
    l.append([u"googleLeadServices",googleLeadServices])
    l.append([u"quoteCast",quoteCast])
    l.append([u"chartBeat",chartBeat])
    l.append([u"adobeDpm",adobeDpm])
    l.append([u"messagent",messagent])
    l.append([u"graydonLeadInsights",graydonLeadInsights])
    l.append([u"visualRevenue",visualRevenue])
    l.append([u"brightCove",brightCove])
    l.append([u"hotJar",hotJar])
    l.append([u"usaBilla",usaBilla])
    l.append([u"shoppingMinds",shoppingMinds])
    l.append([u"celeraOne",celeraOne])
    l.append([u"adHese",adHese])
    l.append([u"wordPress",wordPress])

    return l


def parseHtml_topwords(text, words_to_remove):

    # remove overhead
    text = re.sub(u'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text, flags=re.MULTILINE)
    text = re.sub(u'[^\w]+', ' ', text, flags=re.UNICODE)
    text = re.sub(u'[0-9]+', ' ', text, flags=re.UNICODE)
    text = text.split(" ")


    # make a wordlist and remove cleanup words
    words = []
    for word in text:
        if not any(word.lower() in s for s in words_to_remove):
            words.append(word)

    top20words = Counter(words).most_common(25)

    top_words = []
    for i, item in enumerate(top20words):
        top_words.append(tuple(item)[0])

    return top_words