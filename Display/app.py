import os
from instagrapi import Client
from flask import Flask, jsonify,render_template
from flask_pymongo import pymongo
from utility import NewsScraper
from get_json import get_json
from datetime import date
from dotenv import load_dotenv
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from indic_transliteration import sanscript
from deep_translator import GoogleTranslator
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

load_dotenv()

app = Flask(__name__)
MONGO_URI = os.environ.get('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)
app.config['MONGO_URI'] = MONGO_URI
db = client.get_database("Newsdata")

today = date.today()
# current_time = datetime.datetime.now()
# hour = current_time.hour

trans = []
date = '04/11/2023'

hindi_comments = db.hindi_comments.find_one({})["comments"]
for com in hindi_comments:
    trans.append(com)

hindi_text = []
senti = []
english = []
sentiment = []

for text in trans:
  hindi_text = transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
  translated_text = GoogleTranslator(source='auto', target='en').translate(hindi_text)
  english.append(translated_text)

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

eng = [i for i in english if i is not None]

for comment in eng:
  sentiment_dict = analyzer.polarity_scores(comment)
  if sentiment_dict['compound']<0:
    sentiment.append("Negative")
  elif sentiment_dict['compound']>0:
    sentiment.append("Positive")
  else:
    sentiment.append("Neutral")

print(sentiment)


hindi_base_url = "https://www.aajtak.in"
kaanda_base_url = "https://www.kannadaprabha.com"
telugu_base_url = "https://www.sakshi.com/"

base_urls = { "hindi": hindi_base_url, "kannada": kaanda_base_url, "telugu": telugu_base_url}

hindi_urls = db.hindi_news.find_one({})["urls"]
kannada_urls = db.kannada_news.find_one({})["urls"]
telugu_urls = db.telugu_news.find_one({})["urls"]

urls = { "hindi": hindi_urls, "kannada": kannada_urls, "telugu": telugu_urls }


# Setting Flask routes
def get_comments(url):
  load_dotenv()
  baseUrl = "https://www.instagram.com/"
  
  INSTA_USERNAME = os.environ.get('INSTA_USERNAME')
  INSTA_PASSWORD = os.environ.get('INSTA_PASSWORD')
  
  cl = Client()
  cl.login(INSTA_USERNAME, INSTA_PASSWORD)
  
  media_id = cl.media_id(cl.media_pk_from_url(baseUrl+url))
  
  return cl.media_comments(media_id, 20)

@app.route("/",methods=['GET'])
def index():
    return render_template('index.html',**locals())

@app.route("/<lang>/headlines", methods=['GET'])
def read_headlines(lang):
    scraper = NewsScraper(base_urls[lang])
    headlines = scraper.getHeadingsWithLinks()
    return jsonify(headlines) 

@app.route('/<lang>/news', methods=['GET'])
def get_json_data(lang:str):
    data = []
    for url in urls[lang]:
        data.append(get_json(base_urls[lang] + url, lang))
    return data

@app.route("/add_headlines",methods=['GET'])
def add_headlines():
    hindiScraper = NewsScraper(base_urls["hindi"])
    kannadaScraper = NewsScraper(base_urls["kannada"])
    teluguScraper = NewsScraper(base_urls["telugu"])

    hindiHeadlines = hindiScraper.getHeadingsWithLinks()
    kannadaHeadlines = kannadaScraper.getHeadingsWithLinks()
    teluguHeadlines = teluguScraper.getHeadingsWithLinks()
    
    db.hindi.insert_one({today.strftime('%m/%d/%Y'): hindiHeadlines})
    db.kannada.insert_one({today.strftime('%m/%d/%Y'): kannadaHeadlines})
    db.telugu.insert_one({today.strftime('%m/%d/%Y'): teluguHeadlines})
    return jsonify(message="success")

@app.route("/add_news", methods=['GET'])
def add_news():
    db.hindi_news.insert_one({"urls": hindi_urls})
    db.kannada_news.insert_one({"urls": kannada_urls})
    db.telugu_news.insert_one({"urls": telugu_urls})
    return jsonify(message="success")

@app.route("/add_comments",methods=['GET'])
def add_comments():
    hindi_comments = []
    hindi_com = get_comments("p/Cqzy-IOrTyD")
    for c in hindi_com:
        # print(vars(c)["text"])
        hindi_comments.append(vars(c)["text"])
    
    db.hindi_comments.insert_one({"comments": hindi_comments})
    return jsonify(message="success")

if __name__ == "__main__":
    app.run(debug=True)