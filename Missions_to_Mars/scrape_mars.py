#!/usr/bin/env python
# coding: utf-8

# In[52]:


# Dependencies
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import pymongo
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager 


# In[53]:


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# NASA News

# In[54]:


# URL of page to be scraped
url = 'https://redplanetscience.com/'

## Retrieve page
browser.visit(url)


# In[55]:


# Create BeautifulSoup object; parse with 'html.parser'
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[56]:


#Find Latest News Title
# Examine the results and look for a div with the class 'content_title'
news_title = soup.find_all('div', class_='content_title')[0].text
news_title


# In[57]:


#Find Latest news Paragraph text
# Examine the results and look for a div with the class 'article_teaser_body'
news_p = soup.find_all('div', class_='article_teaser_body')[0].text
news_p


# JPL image

# In[58]:


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

# In[59]:


#get url
url = 'https://galaxyfacts-mars.com/'
#Use the read_html function in Pandas to automatically scrape any tabular data from a page.
tables = pd.read_html(url)
tables


# In[60]:


type(tables)


# In[61]:


#Create dataframe
df = tables[0]
df.head()


# In[63]:


#generate html table
html_table = df.to_html()
html_table


# Mars Hemispheres

# In[64]:


#get url
mars_url = 'https://marshemispheres.com/'
browser.visit(mars_url)
html=browser.html
soup=BeautifulSoup(html,'html.parser')


# In[65]:


# get hemisphere elements
mars_hemi = soup.find ('div',class_= 'collapsible results')
mars_item=mars_hemi.find_all('div',class_='item')


# In[66]:


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


# In[67]:


browser.quit()

