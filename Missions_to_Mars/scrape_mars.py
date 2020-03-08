# Dependencies
from bs4 import BeautifulSoup as bs
import requests as req
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import pandas as pd
import time

def scrape():
    mars_data = {}

    mars_data["news_data"] = news_scrape()

    mars_data["image"] = image_scrape()

    mars_data["twitter"] = twitter_scrape()

    mars_data["facts_table"] = table_scrape()

    mars_data["hemisphere_data"] = hemisphere_scrape()

    return(mars_data)
    

def news_scrape():
    # Scrape using BeautifulSoup
    # Scrape Nasa for top news story
    #----------
    news = {}

    url = "https://mars.nasa.gov/news/"

    response = req.get(url)
    soup = bs(response.text, 'html.parser')
    #getting title and text from most recent news article
    soup_split = soup.find(class_='slide')
    soup_split1 = soup_split.find_all('a')

    #title
    news_title = soup_split1[1].get_text().strip()

    #news story
    news_p = soup_split1[0].get_text().strip()

    news["title"] = news_title
    news["story"] = news_p

    return(news)
    #----------

def image_scrape():
    # Scrape using Splinter
    # Scrape JPL for top image
    #----------
    image_dic = {}

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    time.sleep(2)

    base_url_2 = "https://www.jpl.nasa.gov"

    url_2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(url_2)

    time.sleep(2)

    html = browser.html

    soup = bs(html, 'html.parser')

    img = soup.find('a', class_='button fancybox')

    #getting top image url
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)
    new_url = browser.url
    browser.visit(new_url)
    time.sleep(2)
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')
    img = soup2.find('figure')
    img = img.find('a')['href']

    #image url
    featured_image_url = base_url_2 + img

    image_dic["img_url"] = featured_image_url

    #quit spliter application
    browser.quit()
    
    return(image_dic)
    #----------

def twitter_scrape():
    # Scrape using BeautifulSoup
    # Scrape Nasa's twitter for mose recent tweet
    #----------
    twitter_dict = {}

    url3 = "https://twitter.com/marswxreport?lang=en"

    response3 = req.get(url3)

    soup3 = bs(response3.text, 'html.parser')

    tweet = soup3.find(class_='js-tweet-text-container')

    #weather tweet
    mars_weather = tweet.find('p').get_text()

    twitter_dict["twitter_feed"] = mars_weather

    return(twitter_dict)
    #----------

def table_scrape():
    # Scrape using Pandas
    # Scrape space-facts website for Mars data table and convert table to html string
    #----------
    table_dict = {}
    url4 = "https://space-facts.com/mars/"

    tables = pd.read_html(url4)

    #table
    html_table = tables[0].to_html()

    table_dict["table"] = html_table

    return(table_dict)
    #----------

def hemisphere_scrape():
    # Scrape using BeautifulSoup
    # Scrape astrogeology.usgs.gov website for pictures and description of each hemisphere
    #----------
    base_url4 = "https://astrogeology.usgs.gov"

    url4 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    response4 = req.get(url4)

    soup4 = bs(response4.text, 'html.parser')

    list_items = soup4.find_all(class_="item")
    img_url = []
    title = []
    for image in list_items:
        image = image.find('a')['href']

        respons = req.get(base_url4+image)

        soup5 = bs(respons.text, 'html.parser')
        title_text = soup5.find(class_="title").get_text()
        title.append(title_text)
        pic = soup5.find('li')
        pic = pic.find('a')['href']
        img_url.append(pic)

    #dictionary with picture link and description 
    hemisphere_image_urls = {}

    for key in title: 
        for value in img_url: 
            hemisphere_image_urls[key] = value 
            img_url.remove(value) 
            break  
    
    return(hemisphere_image_urls)
    #----------
