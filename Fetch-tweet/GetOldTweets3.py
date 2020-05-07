#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""To use this script you can pass the following attributes:
       querysearch: a query text to be matched
          username: a username or a list of usernames (comma or space separated)
                    of a specific twitter account(s) (with or without @)
username-from-file: a file with a list of usernames,
             since: a lower bound date in UTC (yyyy-mm-dd)
             until: an upper bound date in UTC (yyyy-mm-dd) (not included)
              near: a reference location area from where tweets were generated
            within: a distance radius from "near" location (e.g. 15mi)
         toptweets: only the tweets provided as top tweets by Twitter (no parameters required)
         maxtweets: the maximum number of tweets to retrieve
              lang: the language of tweets
            output: a filename to export the results (default is "output_got.csv")

Examples:

python3 GetOldTweets3.py
"""

import os, sys, re, getopt
import traceback
import GetOldTweets3 as got
import pandas as pd
import time
from datetime import date, timedelta

columns = ["Date", "Username","To","Replies",
                        "Retweets","Favorites","Text","Geo",
                       "Mentions","Hashtags","Id","Permalink"]

argv = sys.argv[1:]

# parameter
sdate = date(2020, 5, 5)   # start date
edate = date(2020, 5, 5)   # end date
delta = edate - sdate       # as timedelta
keyword_list = ["coronavirus","Covid-19","corona virus"]
for i in range(delta.days + 1):
    for keyword in keyword_list:
        start_day = sdate + timedelta(days=i)
        end_day = sdate + timedelta(days=i+1)
        start_day = start_day.strftime("%Y-%m-%d")
        end_day = end_day.strftime("%Y-%m-%d")
        print()
        print("Day:" ,start_day)
        outputFileName = "data/"+keyword+"/output_"+start_day+".csv"
        try:
            opts, args = getopt.getopt(argv, "", ("within=","debug"))

            debug = False

            tweetCriteria = got.manager.TweetCriteria()
            tweetCriteria.querySearch = keyword
            tweetCriteria.since = start_day
            tweetCriteria.until = end_day
            tweetCriteria.lang = "en"
            tweetCriteria.maxTweets = 14000
            tweetCriteria.near = 'New York, US'

            for opt, arg in opts:
                if opt == '--near':
                    geocode = arg.split(',')
                    try:
                        if len(geocode) != 2:
                            raise
                        lat, lon = geocode[0].strip(), geocode[1].strip()
                        if lat[-1].lower() == 'n':
                            lat = float(lat[:-1])
                        elif lat[-1].lower() == 's':
                            lat = -float(lat[:-1])
                        else:
                            lat = float(lat)

                        if lon[-1].lower() == 'e':
                            lon = float(lon[:-1])
                        elif lon[-1].lower() == 'w':
                            lon = -float(lon[:-1])
                        else:
                            lon = float(lon)
                        if lat < -180 or lat > 180:
                            raise
                        if lon < -90 or lon > 90:
                            raise
                        tweetCriteria.lat = lat
                        tweetCriteria.lon = lon
                    except:
                        tweetCriteria.near = arg

                elif opt == '--within':
                    tweetCriteria.within = arg

            cnt = 0
            df = pd.DataFrame([], columns = columns) 
            def receiveBuffer(tweets):
                global cnt, df
                for t in tweets:
                    df = df.append({"Date": t.date.strftime("%Y-%m-%d %H:%M:%S"),
                                    "Username": t.username,
                                    "To": t.to,
                                    "Replies": t.replies,
                                    "Retweets": t.retweets,
                                    "Favorites": t.favorites,
                                    "Text": '"'+t.text.replace('"','""')+'"',
                                    "Geo": t.geo,
                                    "Mentions": t.mentions,
                                    "Hashtags": t.hashtags,
                                    "Id": t.id,
                                    "Permalink": t.permalink},
                            ignore_index=True)

                cnt += len(tweets)
                if sys.stdout.isatty():
                    print("\rSaved %i"%cnt, end='', flush=True)
                else:
                    print(cnt, end=' ', flush=True)
            print("Downloading tweets...")
            got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer, debug=debug)
            if cnt !=0:
                df.to_csv(outputFileName)
                print()
                print('Done. Output file generated "%s".' % outputFileName)

        except KeyboardInterrupt:
            print("\r\nInterrupted.\r\n")
        print("Done. Wait for next operation...")

        time.sleep(900)



