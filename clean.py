#!/usr/bin/python3
import sys,re


file = open(sys.argv[1], "r",encoding='UTF-8')
for line in file:

	templine = re.sub(r'(#[^\s]+|@[^\s]+|'
						'[\w \W \s]*http[s]*[a-zA-Z0-9 : \. \/ ; % " \W]*|'
						'pic.twitter.com[^\s]+|'
						'\?utm_source=ig_twitter[^s]\+|'
						'_source=ig_twitter_share&igshid=[^\s]+)', "", line)
	templine = re.sub(r'[^0-9a-zA-ZščćžđČĆŽŠĐ\ ]+', "", templine) # at the end clear out special chars otherwise the previous regex wont work

	print(templine.strip().lower())


