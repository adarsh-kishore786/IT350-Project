import json
import os
from flask import Flask, jsonify,render_template,url_for, request, make_response
# import connexion
from flask_pymongo import pymongo
from pymongo import MongoClient
from utility import NewsScraper
from get_json import get_json
from datetime import date
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# MONGO_URI = os.environ.get('MONGO_URI')
# client = pymongo.MongoClient(MONGO_URI)
# app.config['MONGO_URI'] = MONGO_URI
# # mongo = PyMongo(app)
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


hindi_base_url = "https://www.aajtak.in" # "https://www.bhaskar.com"
kaanda_base_url = "https://www.kannadaprabha.com"
telugu_base_url = "https://www.eenadu.net"

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
        "/telugu-news/movies/samantha-suffers-with-fever/0210/123066515",
        "/telugu-news/crime/im-reduced-to-dust-spare-my-family-pleads-gangster-politician-atiq-ahmad/0300/123066566"
    ]

urls = { "hindi": hindi_urls, "kannada": kannada_urls, "telugu": telugu_urls }

scraper = NewsScraper(base_urls["hindi"])

hindiUrl, hindiScraper = "https://www.aajtak.in", NewsScraper("https://www.aajtak.in")
kannadaUrl, kannadaScraper = "https://www.kannadaprabha.com", NewsScraper("https://www.kannadaprabha.com")
teluguUrl, teluguScraper = "https://www.eenadu.net", NewsScraper("https://www.eenadu.net")

title = scraper.getTitle()

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