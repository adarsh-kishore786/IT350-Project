# print("hello world")
import json
# import db
import os
from flask import Flask, jsonify,render_template,url_for, request, make_response
import connexion
from flask_pymongo import pymongo
from pymongo import MongoClient
from utility import NewsScraper
# import datetime
from datetime import date


app = Flask(__name__)
MONGO_URI = os.environ.get('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)
app.config['MONGO_URI'] = MONGO_URI
# mongo = PyMongo(app)
db = client.get_database("Newsdata")
# headlines = pymongo.collection.Collection(db,"headlines")

hindi = pymongo.collection.Collection(db,"hindi")
kannada = pymongo.collection.Collection(db,"kannada")
telugu = pymongo.collection.Collection(db,"telugu")

today = date.today()
# current_time = datetime.datetime.now()
# hour = current_time.hour

@app.route("/add_one")
def add_one():
    db.todos.insert_one({'title': "todo title", 'body': "todo body"})
    return jsonify(message="success")

@app.route("/add_news",methods=['POST','GET'])
def add_news():
    hindiHeadlines = hindiScraper.getHeadingsWithLinks()
    kannadaHeadlines = kannadaScraper.getHeadingsWithLinks()
    teluguHeadlines = teluguScraper.getHeadingsWithLinks()
    if request.method == 'GET':
        db.hindi.insert_one({today.strftime('%m/%d/%Y'): hindiHeadlines})
        db.kannada.insert_one({today.strftime('%m/%d/%Y'): kannadaHeadlines})
        db.telugu.insert_one({today.strftime('%m/%d/%Y'): teluguHeadlines})
        return jsonify(message="success")



@app.route("/add_headlines_hindi", methods=['POST','GET'])
def add_headlines_hindi():
    hindiHeadlines = hindiScraper.getHeadingsWithLinks()
    if request.method == 'GET':
        db.hindi.insert_one({today.strftime('%m/%d/%Y'): hindiHeadlines})
        return jsonify(message="success")
    
    else:
        return "Error"

@app.route("/add_headlines_kannada", methods=['POST','GET'])
def add_headlines_kannada():
    kannadaHeadlines = kannadaScraper.getHeadingsWithLinks()
    if request.method == 'GET':
        db.kannada.insert_one({today.strftime('%m/%d/%Y'): kannadaHeadlines})
        return jsonify(message="success")
    
    else:
        return "Error"

@app.route("/add_headlines_telugu", methods=['POST','GET'])
def add_headlines_telugu():
    teluguHeadlines = teluguScraper.getHeadingsWithLinks()
    if request.method == 'GET':
        db.telugu.insert_one({today.strftime('%m/%d/%Y'): teluguHeadlines})
        return jsonify(message="success")
    
    else:
        return "Error"

# client = MongoClient('localhost', 27017)
# db = client.userDB
# users = db.users


baseUrl = "https://www.aajtak.in" # "https://www.bhaskar.com"
# baseUrl = "https://www.kannadaprabha.com"
# baseUrl = "https://www.eenadu.net"
scraper = NewsScraper(baseUrl)

hindiUrl, hindiScraper = "https://www.aajtak.in", NewsScraper("https://www.aajtak.in")
kannadaUrl, kannadaScraper = "https://www.kannadaprabha.com", NewsScraper("https://www.kannadaprabha.com")
teluguUrl, teluguScraper = "https://www.eenadu.net", NewsScraper("https://www.eenadu.net")

title = scraper.getTitle()
# print(title)

# @app.route("/read",methods=['Post','GET'])
# def read_news():
#     cursor = users.find()
#     for record in cursor:
#         print(record)
#     return "Hello"

@app.route("/",methods=['POST','GET'])
def index():
    title = scraper.getTitle()
    # headings = scraper.getHeadingsWithLinks()
    if request.method == 'GET':
        # return jsonify(title)
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

if __name__ == "__main__":
    app.run(debug=True)