#!/usr/bin/env python3
#helped with https://github.com/stepthom/lexicon-sentiment-analysis/blob/master/doAnalysis.py
#first argument is the csv filed delimited with a caret and the second is the lexicon, delimited with a comma
import sys

import json

import pandas as pd
# For reading input files in CSV format
import csv

# For doing cool regular expressions
import re

# For sorting dictionaries
import operator

# Intialize an empty list to hold all of our tweets
def isindictArray(array,item):
    if item in array:
        print("yes, its here!")
        print(item)

def in_dictlist(key, value, my_dictlist):
    for this in my_dictlist:
        if this[key] == value:
            return this
    return {}

def readAndClean():
    tweets = []
    #with open(sys.argv[1], "r", encoding='UTF-8') as csvfile:
    with open('alltweets_modified_caret.csv', "r", encoding='UTF-8') as csvfile:
        reader = csv.reader(csvfile, delimiter='^')
        next(reader)
        for row in reader:
            tweet= dict()

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
            tweet['cleanText'] = tweet['text']; # copy original

            tweet['cleanText'] = re.sub(r'(#[^\s]+|@[^\s]+|'
                              '[\w \W \s]*http[s]*[a-zA-Z0-9 : \. \/ ; % " \W]*|'
                              'pic.twitter.com[^\s]+|'
                              '\?utm_source=ig_twitter[^s]\+|'
                              '_source=ig_twitter_share&igshid=[^\s]+)', "", tweet['cleanText'])
            tweet['cleanText'] = re.sub(r'[^0-9a-zA-ZščćžđČĆŽŠĐ\ ]+', "",
                              tweet['cleanText'])  # at the end clear out special chars otherwise the previous regex wont work
            tweets.append(tweet)
    return tweets

def analyzeWithLeksicon(tweets):

    #build leksicon
    lexicon = dict()
    #with open(sys.argv[2], "r", encoding='UTF-8') as csvfile:
    #with open('/home/arun/jezikovne/korpusi/kadunclexicon.csv', "r", encoding='UTF-8') as csvfile:
    with open('kadunclexicon.csv', "r", encoding='UTF-8') as csvfile:
        #depending on lexicon
        reader = csv.reader(csvfile, delimiter=',')
        #reader = csv.reader(csvfile, delimiter='\t')
        next(reader)
        for row in reader:
            lexicon[row[0]] = int(row[1])

    #score the tweets
    for tweet in tweets:
        tweet['score'] = ''
        score = 0
        for word in tweet['cleanText'].split(" "):
            if word in lexicon:
                score = score + lexicon[word]
                tweet['score']= score / len(tweet['cleanText'].split())

    #set some parameters
    csv_columns = ['date','username','to','replies','retweets','favorites','text',
                   'geo','mentions','hashtags','id','permalink','cleanText','score']
    csv_file = "output.csv"

    #start saving the tweets
    tempCheck = []
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, delimiter="^",fieldnames=csv_columns)
            writer.writeheader()
            for data in tweets:
                #check if it already exists(duplicate removing)
                if((in_dictlist('date', data["date"], tempCheck)) == {} and (in_dictlist('id', data["id"], tempCheck)) == {}):
                    tempCheck.append(data)
                    writer.writerow(data)
                # else:
                #     print("not writing")
    except IOError:
        print("I/O error")


    return tempCheck

cleanTweets = readAndClean();
analyzeWithLeksicon(cleanTweets)

#clean out duplicates just in case
df = pd.read_csv('output.csv', sep='^')
df.drop_duplicates(inplace=True)
df.to_csv('output.csv', sep='^',index=False)


