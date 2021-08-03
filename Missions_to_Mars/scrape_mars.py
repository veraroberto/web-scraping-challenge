from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

import time


def scrape():
   
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Scrap NASA Mars News
    mars_url = 'https://redplanetscience.com/'
    browser.visit(mars_url)
    # time.sleep(5)
    soup = bs(browser.html, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text
    news_date = soup.find_all('div', class_="list_date")[0].text
    #print(news_title)
    #print(paragraph)




    # JPL Mars Space Images - Featured Image
    mars_images = 'https://spaceimages-mars.com/'
    browser.visit(mars_images)
    featured_image_url = browser.find_by_css('img.thumbimg').first['src']

    #Mars Facts
    mars_facts = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(mars_facts)
    comparison_df = tables[0]
    comparison_df.columns= comparison_df.iloc[0]
    comparison_df
    mars_earth = comparison_df.loc[1:]
    mars_earth
    mars_earth_comparison = mars_earth.set_index('Mars - Earth Comparison')
    mars_earth_html = mars_earth_comparison.to_html(classes='table')


    #Mars Hemispheres
    mars_hemishperes = 'https://marshemispheres.com/'
    browser.visit(mars_hemishperes)
    soup = bs(browser.html, 'html.parser')
    images = soup.find_all('div', class_= 'description')
    hemisphere_image_urls = []
    for img in images:
        dict_img = {}
        #Gets the title of the Photo
        dict_img['title'] = img.find('h3').text
    
        #Gets the new URL to get the Photo
        temp_url = img.find('a', class_='itemLink product-item')['href']
        vist_url =  mars_hemishperes + temp_url
    
    
        browser.visit(vist_url)
        soup = bs(browser.html, 'html.parser')
        sample_url = browser.links.find_by_partial_text('Sample')['href']

        dict_img['img_url'] = sample_url
        hemisphere_image_urls.append(dict_img)
    

    mission_mars = {
        'news_title': news_title,
        'news_p' : news_p,
        'news_date': news_date,
        'featured_image_url' : featured_image_url,
        'mars_earth_comparison': mars_earth_html,
        'hemisphere_image_urls' : hemisphere_image_urls

    }
    



    browser.quit()



    return mission_mars


#########
# Dictionary scrape_dict
# scrape_dcit['news_title']
# scrape_dcit['news_p']
# scrape_dcit['featured_image_url']
# scrape_dcit['mars_earth_comparison']
# scrape_dcit['hemisphere_image_urls'] is a list that contain 4 dictionaries 



