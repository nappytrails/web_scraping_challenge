# Import dependencies
import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    def init_browser():
        '''Launches a Chrome browser using splinter and ChromeDriverManager'''
        executable_path = {'executable_path': ChromeDriverManager().install()}
        return Browser('chrome', **executable_path, headless=True)

    def browse(url):
        '''Function to scrape a single webpage'''
        browser = init_browser()
        browser.visit(url)

        # Scrape html code
        html = browser.html    

        # Create BeautifulSoup object; parse with 'html.parser'
        soup = BeautifulSoup(html, "html.parser")
    
        # Quit browser
        browser.quit()
    
        return soup

    # Create an empty dictionary to hold web scraping resutls
    mars_scrape_dict = {}


    ##### NASA Mars News #####

    # URL for NASA Mars News Site 
    nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # Scrape html of nasa_url
    nasa_soup = browse(nasa_url)

    # Find title and teaser text of first article and store them to variables
    first_article_title = nasa_soup.find("div", class_="bottom_gradient").text
    first_article_teaser = nasa_soup.find("div", class_="article_teaser_body").text

    # Append the article variables to mars_scrape_dict
    mars_scrape_dict["article_title"] = first_article_title
    mars_scrape_dict["article_teaser"] = first_article_teaser


    ##### JPL Mars Space Images - Featured Image #####

    # URL to JPL Mars image website
    jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"

    # Scrape jpl_url
    jpl_soup = browse(jpl_url)

    # Scrape the link to the featured image
    jpl_image_link = jpl_soup.find("a", class_="showimg fancybox-thumbs")["href"]

    # Assign the full image url to a variable
    featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{jpl_image_link}"

    mars_scrape_dict["featured_image"] = featured_image_url


    ##### Mars Facts #####

    # Scrape url using pandas and assign scraped tables to a variable
    space_facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(space_facts_url)

    # Create a dataframe from the first table
    stats_table_df = pd.DataFrame(tables[0])

    # Rename the columns
    stats_table_df = stats_table_df.rename(columns={0:"", 1:"values"}, inplace=False)

    # Set the index to the first column
    stats_table_new_index_df = stats_table_df.set_index(keys="")

    # Generate html code for the table and remove "\n" from the code
    stats_table_html = stats_table_new_index_df.to_html()
    stats_table_html = stats_table_html.replace("\n", "")

    # Append the table to mars_scrape_dict
    mars_scrape_dict["table_html"] = stats_table_html


    ##### Mars Hemispheres #####

    # USGS Mars website url
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # Initiate browswer instance
    usgs_browser = init_browser()
    usgs_browser.visit(usgs_url)

    # Scrape image Mars hemispheres pages
    hemispheres = ["Cerberus", "Schiaparelli", "Syrtis", "Valles"]
    soup_objects = []

    for hemisphere in hemispheres:
        usgs_browser.links.find_by_partial_text(hemisphere).click()

        # Scrape html code
        usgs_html = usgs_browser.html    

        # Create BeautifulSoup object; parse with 'html.parser'
        usgs_soup = BeautifulSoup(usgs_html, "html.parser")

        # Assign BeautifulSoup object to unique variable; print variable name
        locals()["soup_" + hemisphere] = usgs_soup

        # Append soup object to list
        soup_objects.append(locals()["soup_" + hemisphere])
                            
        # Go back to previous page
        usgs_browser.back()
        
    usgs_browser.quit()

    # Find title and url for hemispheres images
    hemispheres_list = []

    for soup_object in soup_objects:

        hemispheres_dict = {}

        title = soup_object.find("h2", class_="title").text.replace(" Enhanced", "")
        img_url = soup_object.find_all("a", target="_blank")[3]["href"]
        
        hemispheres_dict["title"] = title
        hemispheres_dict["img_url"] = img_url
        
        hemispheres_list.append(hemispheres_dict)

    mars_scrape_dict["hemispheres"] = hemispheres_list

    return mars_scrape_dict