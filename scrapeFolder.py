import re

f = open('raw_html/www.gpgroot.nl.html', 'r')

# load the html doc
doc = file.read(f)

# Delete Python-style comments
email = re.findall('([A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+[a-zA-Z])', doc)
print "email : ", set(email)

phone = re.findall('(\d{1,4}[\s-]\d{6,8})', doc)
print "phone : ", set(phone)

linkedin = re.findall('(?:https?:\/\/)?(?:www\.)?linkedin\.com\/(?:(?:\w\.)*#!\/)?(?:pages\/)?(?:[\w\-\.]*\/)*([\w\-\.]*)', doc)
print "linkedin : ", set(linkedin)