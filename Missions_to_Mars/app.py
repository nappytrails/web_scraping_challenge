# Import dependencies
import pandas as pd
from pymongo import database
import requests
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template, redirect
# from flask_pymongo import PyMongo
import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

## Connect to MongoDB using pymongo to create database and collection
# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Drop existing "mars_db" database if any
try:
    client.drop_database("mars_db")
except:
    print("No database to drop")

# Create mars_db database
db = client.mars_db

# Creating the collection "mars_col"
mars_col = db.mars_col


@app.route("/")
def index():
    mars_display = mars_col.find()
    return render_template("index.html", mars_display=mars_display)


@app.route("/scrape")
def scraper():

    # Web scrape various sites about Mars and add results to "mars_col"
    mars_info = scrape_mars.scrape()
    mars_col.update({}, mars_info, upsert=True)
    
    # Close connection to MongoDB
    client.close()
    
    return redirect("/", code=302)

