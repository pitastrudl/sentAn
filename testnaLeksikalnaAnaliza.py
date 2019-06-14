#!/usr/bin/env python3
import sys
import unidecode
import json

import pandas as pd
# For reading input files in CSV format
import csv

# For doing cool regular expressions
import re


def in_dictlist(key, value, my_dictlist):
    for this in my_dictlist:
        if this[key] == value:
            return this
    return {}

def readAndClean(row):
    tweets = []
    #row = sys.argv[1]
    tweet = dict()
    row = row.split("^")
    tweet['date'] = row[0]
    tweet['username'] = row[1]
    tweet['to'] = row[2]
    tweet['replies'] = row[3]
    tweet['retweets'] = int(row[4])
    tweet['favorites'] = int(row[5])
    tweet['text'] = row[6]
    tweet['geo'] = row[7]
    tweet['mentions'] = row[8]
    tweet['hashtags'] = row[9]
    tweet['id'] = row[10]
    tweet['permalink'] = row[11]
    tweet['cleanText'] = tweet['text'];  # copy original

    tweet['cleanText'] = re.sub(r'(#[^\s]+|@[^\s]+|'
                                '[\w \W \s]*http[s]*[a-zA-Z0-9 : \. \/ ; % " \W]*|'
                                'pic.twitter.com[^\s]+|'
                                '\?utm_source=ig_twitter[^s]\+|'
                                '_source=ig_twitter_share&igshid=[^\s]+)', "", tweet['cleanText'])
    tweet['cleanText'] = re.sub(r'[^0-9a-zA-ZščćžđČĆŽŠĐ\ ]+', "",
                                tweet[
                                    'cleanText'])  # at the end clear out special chars otherwise the previous regex wont work
    tweet['cleanText'] = tweet['cleanText'].strip()
    tweet['cleanText'] = tweet['cleanText'].lower()  #nekaj zjebe tukaj

    #tweet['cleanText'] = unidecode.unidecode(tweet['cleanText']) # ni pametno.
    tweets.append(tweet)
    return tweets

def buildLexicon():
    # build leksicon
    lexicon = dict()
    #with open(sys.argv[2], "r", encoding='UTF-8') as csvfile:
    with open('velik.csv', "r", encoding='UTF-8') as csvfile:
        # with open('kadunclexicon.csv', "r", encoding='UTF-8') as csvfile:
        # depending on lexicon
        reader = csv.reader(csvfile, delimiter=',')
        # reader = csv.reader(csvfile, delimiter='\t')
        next(reader)
        for row in reader:
            #lexicon[row[0].strip()] = int(row[1].strip())
            lexicon[row[0]] = int(row[1])
    return lexicon;


def scoreTweets(tweets, lexicon):
    foundInLeksicon = 0;
    csv_file = "testanaliza.csv"
    # score the tweets
    for tweet in tweets:
        tweet['score'] = ''
        score = 0
        for word in tweet['cleanText'].split(" "):
            if word in lexicon:
                foundInLeksicon += 1;
                score = score + lexicon[word]
                print(str(lexicon[word]) + ' ' + word)
                tweet['score'] = score / len(tweet['cleanText'].split()) #narobe??
    tempCheck = []
    csv_columns = ['date', 'username', 'to', 'replies', 'retweets', 'favorites', 'text',
                   'geo', 'mentions', 'hashtags', 'id', 'permalink', 'cleanText', 'score']
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter="^", fieldnames=csv_columns)
            writer.writeheader()
            for data in tweets:
                # check if it already exists(duplicate removing)
                if ((in_dictlist('date', data["date"], tempCheck)) == {} and (
                        in_dictlist('id', data["id"], tempCheck)) == {}):
                    tempCheck.append(data)
                    writer.writerow(data)
                # else:
                #     print("not writing")
    except IOError:
        print("I/O error")
    print("found:" +  str(foundInLeksicon))
    return tempCheck

#tweet = readAndClean("2019-03-23 10:58:59^vecer^^0^1^3^(PLANICA) Slovenski skakalci tekmo končali na tretjem mestu. Zmagali so Poljaki, na drugem mestu Nemci. -slovenski-selektor-napoveduje-borbo-kranjcu-bo-za-zadnji-polet-z-zastavo-zamahhnila-hci-pika-6680994 …^^^^1.10940919979513E+018^https://twitter.com/vecer/status/1109409199795130368")
tweet = readAndClean("2019-03-02 10:51:06^frelihu^^0^0^0^at Olimpijski Športni Center, Planica …^^^^1.10179707105148E+018^https://twitter.com/frelihu/status/1101797071051476992")
leksikon = buildLexicon()
scored = scoreTweets(tweet,leksikon)
print(scored[0]['score'])
print(scored[0]['cleanText'])

