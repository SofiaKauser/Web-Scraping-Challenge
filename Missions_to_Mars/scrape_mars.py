 
 # Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
# from splinter.exceptions import ElementDoesNotExist
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests 
import pandas as pd


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


 # visit the red planet science web page
url_1 = 'https://redplanetscience.com/'
browser.visit(url_1)


 # HTML object
html = browser.html
 # Parse HTML with Beautiful Soup as bs
soup_1 = bs(html, 'html.parser')

 # NASA Mars News
text = soup.select_one("div.list_text")

 #Scrape and collect the latest News Title and Paragraph Text

news_title=text.find("div", class_="content_title").get_text()
news_p =text.find("div", class_="article_teaser_body").get_text()

 # result to mongoDB dictionary
mars_data['news_title'] = news_title
mars_data['news_p'] = news_p


 # JPL Mars Space Images - Featured Image

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

 # visit site and inspect 
url_2 = "https://spaceimages-mars.com"
browser.visit(url_2)

browser.find_by_css('.fancybox-thumbs').click() 

 # HTML object
html = browser.html
 # Parse HTML with Beautiful Soup
soup_2 = bs(html, 'html.parser')

partial_img_url=soup.select_one("img.fancybox-image" ).get("src")
img_url = f"https://spaceimages-mars.com/{partial_img_url}"

 # result to mongoDB dictionary
mars_data['featured_image'] = image_url

 # Mars Facts

 # visit site and scrape table data into Pandas
url_3 = 'https://galaxyfacts-mars.com/'
browser.visit(url_3)

 # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
mars_facts_df = pd.read_html("https://space-facts.com/mars/")[0]

 # Clean up DataFrame, set index
mars_facts_df.columns=["Planet Profile", "Value"]
mars_facts_df.set_index("Planet Profile", inplace=True)
mars_facts_html_table = mars_facts_df.to_html()
mars_facts_html_table = mars_facts_html_table.replace('\n','')


 # result to mongoDB dictionary
mars_data['mars_facts'] = mars_facts_html_table


 # Mars Hemispheres

 # visit site and scrape pictures of the hemispheres 
url_4 = "https://marshemispheres.com/"
browser.visit(url_4)

 # Parse Results HTML with BeautifulSoup
html = browser.html
mars_weather_soup = bs(html, "html.parser")


 # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name

  soup_3 = bs(html, "html.parser")
  items = soup_3.find_all("div", class_="item")

  hemisphere_img_urls = []

  for item in items:

      title = item.find("h3").text
      link = item.find("a", class_="itemLink")["href"]
      hemispherelink = url_4 + link
      browser.visit(hemispherelink)
      hemispherehtml = browser.html

      soup_4 = bs(hemispherehtml, "lxml")
      image = soup_4.find("img", class_="wide-image")["src"]
      imageurl = url_4 + image
      hemisphere = {}

      hemisphere_img_urls.append({"title":title,"img_url":imageurl})

      browser.back()
        
 # result to mongoDB dictionary
  mars_data["hemispheres"] = hemisphere_img_urls

  browser.quit()

  return mars_data

mars_data = scrape_all()

 # Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

 # Define database and collection
db = client.mars
collection = db.mars

 # Dictionary to be inserted as a MongoDB document
collection.update_one({}, {"$set": mars_data}, upsert=True)






































































