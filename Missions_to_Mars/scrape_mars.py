
# Dependencies
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
def scrape_all():
    mars_data={}
# NASA News
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find_all('div', class_='content_title')[0].text
    news_title

    news_p = soup.find_all('div', class_='article_teaser_body')[0].text
    news_p


# JPL image
#find the image url for the current Featured Mars Image 
    jpl_url = "https://spaceimages-mars.com/"
    browser.visit(jpl_url)

    mars_img = browser.html
    soup = BeautifulSoup(mars_img, 'html.parser')

    jpl_src = soup.find('img', class_='headerimage fade-in')['src']
 
#assign the url string to a variable called featured_image_url
    featured_image_url = jpl_url+jpl_src
    featured_image_url


# Mars Facts

    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    tables
    type(tables)
#Create dataframe
    df = tables[0]
    df.head()
#generate html table
    html_table = df.to_html(classes="table table-striped")
    html_table


# Mars Hemispheres

#get url
    mars_url = 'https://marshemispheres.com/'
    browser.visit(mars_url)
    html=browser.html
    soup=BeautifulSoup(html,'html.parser')




# get hemisphere elements
    mars_hemi = soup.find ('div',class_= 'collapsible results')
    mars_item=mars_hemi.find_all('div',class_='item')



# create empty list and loop through items
    hemi_image_urls=[]
#loop 
    for item in mars_item:
        try:
            hemi=item.find('div',class_='description')
            title=hemi.h3.text
            img_urls=hemi.a['href']
            browser.visit(mars_url+img_urls)
            html=browser.html
            soup=BeautifulSoup(html,'html.parser')
            image_src=soup.find('li').a['href']
            if (title and image_src):
                print(title)
                print(image_src)
        except Exception as e:
            print(e)

    # create mars_data dict that we can insert into mongo
    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "facts": html_table,
        "hemispheres": hemi_image_urls
        }

browser.quit()