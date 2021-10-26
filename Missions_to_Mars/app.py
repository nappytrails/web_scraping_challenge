# Import dependencies
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
mars_col = mongo.db.mars_col

@app.route("/")
def index():
    mars_display = mars_col.find_one()
    return render_template("index.html", mars_display=mars_display)


@app.route("/scrape")
def scraper():

    # Web scrape various sites about Mars and add results to "mars_col"
    mars_info = scrape_mars.scrape()
    mars_col.update({}, mars_info, upsert=True)
    
    
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)