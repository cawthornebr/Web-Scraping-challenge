from flask import Flask, jsonify, redirect, render_template
import pymongo
import scrape_mars


# The default port used by MongoDB is 27017
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define the 'web_scrapeDB' database and collection in Mongo
db = client.web_scrapeDB
mars_data = db.mars_data

# Initializes initialize flask
app = Flask(__name__)

@app.route("/")
def index():
    print("********************")
    print("---Index selected---")
    print("********************")
    return (
        f"Available Routes:<br/>"
        f"/scrape")

@app.route("/scrape")
def precipitation():
    print("********************")
    print("---Scrape selected---")
    print("********************")
    scrape_data = scrape_mars.scrape()
    mars_data.replace_one({}, scrape_data, upsert=True)
    return redirect('http://localhost:5000/', code=302)

if __name__ == "__main__":
    app.run(debug=True)