# print("hello world")
from flask import Flask,jsonify,render_template,url_for, request
from flask_pymongo import PyMongo
from utility import NewsScraper
# from .extensions import mongo

app = Flask(__name__)
# app.config['MONGO_URI'] = 'mongodb+srv://nikhil:password@cluster0.ibesdda.mongodb.net/?retryWrites=true&w=majority'
# mongo = PyMongo()
# mongo.init_app(app)

baseUrl = "https://www.aajtak.in" # "https://www.bhaskar.com"
scraper = NewsScraper(baseUrl)

title = scraper.getTitle()
print(title)

@app.route("/",methods=['POST','GET'])
def index():
    title = scraper.getTitle()
    headings = scraper.getHeadingsWithLinks()
    if request.method == 'GET':
        return render_template('index.html',**locals())
    else:
        return "Hello"

if __name__ == "__main__":
    app.run(debug=True)