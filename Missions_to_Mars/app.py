from flask import Flask, render_template, redirect, url_for
import pymongo
from scrape_mars import scrape

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
collection = db.data

@app.route("/")
def home():
    data = {}
    data = collection.find_one()
    print(data)
    return render_template("index.html", data=data)

@app.route("/scrape")
def scrape_page():
    collection.insert_one(scrape())
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug = True)