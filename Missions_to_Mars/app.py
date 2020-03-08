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

    try:
        mars_new_data =  mars_data.find_one()

        news_title = mars_new_data['news_data']['title']
        news_story = mars_new_data['news_data']['story']
        featured_image_url = mars_new_data['image']['img_url']
        mars_weather_tweet = mars_new_data['twitter']['twitter_feed']
        mars_facts_table = mars_new_data['facts_table']['table']

        hemisphere_data_db = mars_new_data['hemisphere_data']
        hemisphere_data_list = list(hemisphere_data_db.keys())

        hem_t_0 = hemisphere_data_list[0]
        hem_i_0 = mars_new_data['hemisphere_data'][hemisphere_data_list[0]]
        hem_t_1 = hemisphere_data_list[1]
        hem_i_1 = mars_new_data['hemisphere_data'][hemisphere_data_list[1]]
        hem_t_2 = hemisphere_data_list[2]
        hem_i_2 = mars_new_data['hemisphere_data'][hemisphere_data_list[2]]
        hem_t_3 = hemisphere_data_list[3]
        hem_i_3 = mars_new_data['hemisphere_data'][hemisphere_data_list[3]]
    except (IndexError, TypeError) as error_handler:
        news_title = ""
        news_story = ""
        featured_image_url = ""
        mars_weather_tweet = ""
        mars_facts_table = ""
        hem_t_0 = ""
        hem_i_0 = ""
        hem_t_1 = ""
        hem_i_1 = ""
        hem_t_2 = ""
        hem_i_2 = ""
        hem_t_3 = ""
        hem_i_3 = ""
    return render_template("index.html",news_title=news_title, news_story=news_story, featured_image_url=featured_image_url,\
                            mars_weather_tweet=mars_weather_tweet, mars_facts_table=mars_facts_table,\
                            hem_t_0=hem_t_0, hem_i_0=hem_i_0, hem_t_1=hem_t_1, hem_i_1=hem_i_1,\
                            hem_t_2=hem_t_2,hem_i_2=hem_i_2, hem_t_3=hem_t_3, hem_i_3=hem_i_3)

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