import json
import os
from instagrapi import Client
from flask import Flask, jsonify,render_template,url_for, request, make_response
# import connexion
from flask_pymongo import pymongo
from pymongo import MongoClient
from utility import NewsScraper
from get_json import get_json
from datetime import date
from dotenv import load_dotenv
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from indic_transliteration import sanscript
# from textblob import TextBlob
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


load_dotenv()

app = Flask(__name__)
# MONGO_URI = os.environ.get('MONGO_URI')
# client = pymongo.MongoClient(MONGO_URI)
# app.config['MONGO_URI'] = MONGO_URI
# db = client.get_database("Newsdata")

# hindi = pymongo.collection.Collection(db,"hindi")
# kannada = pymongo.collection.Collection(db,"kannada")
# telugu = pymongo.collection.Collection(db,"telugu")

# today = date.today()
# # current_time = datetime.datetime.now()
# # hour = current_time.hour

# @app.route("/add_news",methods=['POST','GET'])
# def add_news():
#     hindiHeadlines = hindiScraper.getHeadingsWithLinks()
#     kannadaHeadlines = kannadaScraper.getHeadingsWithLinks()
#     teluguHeadlines = teluguScraper.getHeadingsWithLinks()
#     if request.method == 'GET':
#         db.hindi.insert_one({today.strftime('%m/%d/%Y'): hindiHeadlines})
#         db.kannada.insert_one({today.strftime('%m/%d/%Y'): kannadaHeadlines})
#         db.telugu.insert_one({today.strftime('%m/%d/%Y'): teluguHeadlines})
#         return jsonify(message="success")

trans = []
# date = '04/11/2023'

# hindi_comments = db.hindi_comments.find_one({})["comments"]
# for com in hindi_comments:
#     trans.append(com)

# # trans = ["हद्द है यार , अब सब काम भी प्रधानमंत्री जी को करना पड रहा है... सरकारी तंत्र क्या कर रहा है। 😀 😂","🙏🏻","Pm Desh chala rahe hai ki jangal me nokari pa Gaye hai jai bhim jai sambidhan","😂😂 animal Jan sankhya kaanon bnao 😂 q badh rhi population cantrol karne bolo 😂","@kuldeepyuvraj berozgari bhukhmari ginna nahin aata Q ki anpad h 😂modi😂😂😂","Media ka to blo mt Pakistan or afghanistan se bhi gya guzra hua hai","Bhukmari me top pe","Sarso tel k blo","Diesel k blo","Petrol k daam blo","Gas k daam blo","अरे अंदभगत बेरोजगारी की संख्या पर भी ध्यान दे ले चुतिया 😂","ये तो ठीक है पर ये बाघों के फोटो की जगह मोदी जी क्यू लगा रखा बाघों की संख्या बड़ी ना","Sir aap Yogi ji ko gin na bhul gaye sayad😂😂😂","आप अपनी डिग्री दिखावे बस","Ab Insan ki kimat janvaron se kam ho gai isliye rojgar per Dhyan Nahin dete","Rojgar per Dhyan Nahin janvaron ko per Dhyan dete Ho","Andhbhakto me bhi teji ankde badte ja rahe  h Modiji","Entire political science 😂😂😂","Farzi degree"]
# hindi_text = []
# senti = []
# english = []
# sentiment = []

# for text in trans:
#   hindi_text = transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
#   translated_text = GoogleTranslator(source='auto', target='en').translate(hindi_text)
#   english.append(translated_text)

# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
# analyzer = SentimentIntensityAnalyzer()

# eng = [i for i in english if i is not None]

# for comment in eng:
#   sentiment_dict = analyzer.polarity_scores(comment)
#   if sentiment_dict['compound']<0:
#     sentiment.append("Negative")
#   elif sentiment_dict['compound']>0:
#     sentiment.append("Positive")
#   else:
#     sentiment.append("Neutral")

# print(sentiment)


hindi_base_url = "https://www.aajtak.in" # "https://www.bhaskar.com"
kaanda_base_url = "https://www.kannadaprabha.com"
telugu_base_url = "https://www.sakshi.com/"

base_urls = { "hindi": hindi_base_url, "kannada": kaanda_base_url, "telugu": telugu_base_url}

hindi_urls = \
    [
        "/elections/karnataka-assembly-election-2023/story/karnataka-election-bjp-candidate-ex-bbmp-commissioner-anil-kumar-koratagere-constituency-ntc-1673020-2023-04-12",
        "/elections/karnataka-assembly-election-2023/story/karnataka-election-ks-eshwarappa-quit-election-politics-bjp-ntc-1672461-2023-04-11"
    ]
    
kannada_urls = \
    [
        "/nation/2023/apr/12/fir-against-union-minister-arjun-munda-and-40-others-over-protest-in-ranchi-491543.html",
        "/nation/2023/apr/12/chinese-buildup-close-to-doklam-plateau-a-grave-security-threat-congress-491552.html"
    ]
telugu_urls = \
    [
        "/telugu-news/sports/jos-buttler-met-his-lucky-fan-intresting-conversation-viral-gt-vs-rr-1587163",
        "/telugu-news/andhra-pradesh/ys-avinash-reddy-key-comments-over-bhaskar-reddy-arrest-1587119"
    ]

urls = { "hindi": hindi_urls, "kannada": kannada_urls, "telugu": telugu_urls }

scraper = NewsScraper(base_urls["hindi"])

hindiUrl, hindiScraper = "https://www.aajtak.in", NewsScraper("https://www.aajtak.in")
kannadaUrl, kannadaScraper = "https://www.kannadaprabha.com", NewsScraper("https://www.kannadaprabha.com")
teluguUrl, teluguScraper = "https://www.sakshi.com/", NewsScraper("https://www.sakshi.com/")

title = scraper.getTitle()

# @app.route("/add_comments",methods=['POST','GET'])
# def add_comments():
#     hindi_comments = []
#     hindi_com = get_comments("p/Cqzy-IOrTyD")
#     for c in hindi_com:
#         # print(vars(c)["text"])
#         hindi_comments.append(vars(c)["text"])
#     if request.method == 'GET':
#         db.hindi_comments.insert_one({"comments": hindi_comments})
#         return jsonify(message="success")


def get_comments(url):
  load_dotenv()
  baseUrl = "https://www.instagram.com/"
  
  INSTA_USERNAME = os.environ.get('INSTA_USERNAME')
  INSTA_PASSWORD = os.environ.get('INSTA_PASSWORD')
  
  cl = Client()
  cl.login(INSTA_USERNAME, INSTA_PASSWORD)
  
  media_id = cl.media_id(cl.media_pk_from_url(baseUrl+url))
  
  return cl.media_comments(media_id, 20)

@app.route("/",methods=['POST','GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html',**locals())
    else:
        return "Hello"

@app.route("/headlines", methods=['POST','GET'])
def read_headlines():
    headlines = scraper.getHeadingsWithLinks()
    if request.method == 'GET':
        return jsonify(headlines) 
    else:
        return "Error"

@app.route('/<lang>/news', methods=['GET'])
def get_json_data(lang:str):
    data = []
    for url in urls[lang]:
        data.append(get_json(base_urls[lang] + url, lang))
    return data

if __name__ == "__main__":
    app.run(debug=True)