#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser


# In[2]:

def init_browser():
    #actual path to chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)


# In[3]:

def scrape():

    browser = init_browser()
    #create a mars_data dict
    mars_data = {}
    #visit mars.nasa.gov/news/
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)


    # In[4]:
    html = browser.html
    soup = bs(html, 'html.parser')


    #tested html
    #html
    # In[6]:
    #scrape for the most recent news title and article teaser on nasa page. using find gives you first instance
    news_title = soup.find('div', class_= "content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text


    #upload our news_title and news_p variables to mars_data dict
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p


    # recent_news = []
    # for title in news_title:
    #     recent_news.append(title.text)
        
    # recent_news



    #Time to scrape the featured Mars image page 
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)


    #bring in html for Nasa Mars image page
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')


    #find the featured image on web page
    featured_image_button = soup2.find('a', class_="button fancybox")


    # test featured_image
    featured_image_button


    #pull the full size image url
    image_url = featured_image_button['data-fancybox-href']


    # test image_url
    image_url

    #combine the home path url to the image url that was scraped
    full_image_url = f'https://www.jpl.nasa.gov{image_url}'
    full_image_url

    #upload the 'full_image_url' to mars_data dict
    mars_data['full_image_url'] = full_image_url

    #visit Mars Weather Twitter Page
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)

    #bring in Twitter Html , use Beautiful Soup again
    html3 = browser.html
    soup3 = bs(html3, 'html.parser')

    # #find the tweet section, then locate the latest tweet with weather information
    # # go to first p tag where class= "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"
    latest_tweet = soup3.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    latest_tweet

    #mars weather
    mars_weather = latest_tweet.text.strip('InSight ')
    mars_weather
    #upload mars_weather to mars_data dict
    mars_data["mars_weather"] = mars_weather

    #Time to start working on new site for Mars Facts
    url4 = 'https://space-facts.com/mars/'
    browser.visit(url4)

    #This time we are going to use Pandas to pull any tabular data located on our url4 for Mars facts
    facts_table = pd.read_html(url4)

    # we get a list of any tabular data in our page
    facts_table

    #covert our list into a dataframe
    mars_df = facts_table[0]
    mars_df.head()

    #rename our columns, and set our index
    mars_final = mars_df.rename(columns={0:"Description", 1:"Values"})
    mars_final = mars_final.set_index("Description")

    #test final table
    mars_final

    # mars_table = {"mars_table":mars_final}
    # mars_data.append(mars_table)

    #send our table to html format
    mars_table_html = mars_final.to_html()
    mars_data["mars_table_html"] = mars_table_html



    #Time to start working on final web scrape for pictures of 4 hemispheres of Mars
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)

    #bring in html from astrogeology.usgs.gov
    html5 = browser.html
    soup5 = bs(html5, 'html.parser')


    #We need to first identify the container with the link new page, with enhanced image download
    # define the 'home url' that will be added to all links later on
    astro_home_url = "https://astrogeology.usgs.gov"
    link_container = soup5.find_all('div', class_='description')


    link_container

    #create an empty list for the 'enhanced image' urls and run a loop on the link container to pull the links
    enhanced_url_list = []
    for item in link_container:
        a_link = item.find('a')['href']
        final_url = f'{astro_home_url}{a_link}'
        enhanced_url_list.append(final_url)
        
    #check our new list of links to each of the Mars Hemisphere 
    enhanced_url_list

    #test out the code we will need to run inside our loop
    # response = requests.get(enhanced_url_list[0])
    # soup_test = bs(response.text, 'lxml')
    # download_container = soup_test.find('div', class_='downloads')
    # download_container

    #final test to scrape the link to the 'Original' full size image
    # download_list = download_container.find('a', string='Original')['href']
    # download_list

    #now we'll need to create a new loop that goes though our enhanced_url_list, and downloads individual enhanced images
    #we will use our code that was tested above within our loop 

    hemisphere_images_url = []

    for link in enhanced_url_list:
        response = requests.get(link)
        soup = bs(response.text, 'lxml')
        title = soup.find('h2', class_='title').text.strip('Enhanced')
        download_container = soup.find('div', class_='downloads')
        full_image = download_container.find('a', string='Sample')['href']
        
        images_dict = {"title": title,
                    "image_url": full_image}
        hemisphere_images_url.append(images_dict)

    # #our final list of dictionary to add to mars_data dic
    mars_data["hemisphere_images_url"] = hemisphere_images_url


    browser.quit()
    return mars_data
