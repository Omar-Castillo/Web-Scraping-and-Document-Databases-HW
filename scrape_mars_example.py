import pandas as pd
# Import BeautifulSoup
from bs4 import BeautifulSoup
import requests
# Import Splinter and set the chromedriver path
from splinter import Browser


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    scrape_results = {}


    # NASA MARS NEWS
    # Scrape the NASA Mars News Site (https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text.
    # Assign the text to variables that you can reference later.
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    # Retrieve page html into a variable
    news_html = browser.html

    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(news_html, 'lxml')

    # Retrieve news title and paragraph
    news_title = soup.find('div', class_='content_title')

    #news_paragrph = soup.find('div', class_='rollover_description_inner')
    news_paragrph = soup.find('div', class_='article_teaser_body')

    news_title = str(news_title.text)
    news_paragrph = str(news_paragrph.text)

    scrape_results["news_title"] = news_title
    scrape_results["news_p"] = news_paragrph


    browser.quit()
    return scrape_results