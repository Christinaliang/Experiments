#!/usr/bin/env python


from urllib2 import Request, urlopen, URLError
import sys

if len(sys.argv) <= 1:
    print "no input text provided"
    exit()

text = sys.argv[1]

channel = "C02HUEW3J"
botName = "Robot"
icon = "http://i.imgur.com/7LNFbCX.png"

try:
    keyFile = open("slackKey.private", "r")
    slackKey = keyFile.read()
    keyFile.close()
except IOError:
    print "slackKey.private was not found"
    print "You must create a file named slackKey.private in this directory and place your slack token in it"
    exit()

formatedText = text.replace(" ", "%20")

url = "https://slack.com/api/chat.postMessage?token=" + slackKey +"&channel=" + channel +"&text=" + formatedText + "&username=" + botName + "&icon_url=" + icon

request = Request(url)

try:
    response = urlopen(request)
except URLError, e:
    print 'Got an error code:', e