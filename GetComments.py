from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains # <--- helpful!
from selenium.webdriver.common.by import By
import configparser

from bs4 import BeautifulSoup

import pandas as pd
from pandas.io.json import json_normalize

import os
from time import sleep
#import tqdm
import sys

print('-'*60)

# Using one example image
# url = 'https://www.instagram.com/p/BS7Jq4dFiqf'# <-- no trailing slash on url
url = sys.argv[1] # <-- Second argument of the dockerfile CMD (first argument is the python script name itself!)
if not url.startswith('https://'):
    url = 'https://' + url

# Raw HTML file outdir
raw_outfile = "/data/{}.html".format(url.split('/')[-1]) # <--- outdir html file
print('Raw html outfile prepared as: {}'.format(raw_outfile))

# ETL (extracted from raw HTML) file outdir 
etl_outfile = "/data/{}.json".format(url.split('/')[-1]) # <--- outdir json file
print('ETL outfile prepared as: {}'.format(etl_outfile))

# Instagram HTML element
xpath_aria_label_button = 'Load more comments' # <--- inspect & find class name for button click

# Optimization parameters
threshold_for_failed_click = 10  # <-- Int
time_to_wait_for_nxt_click = 0.25 # <-- Int

##############################################
# Setup Selenium Driver

# driver = webdriver.Chrome(executable_path='/Users/etiennejacquot/Downloads/chromedriver_v84') 
# driver = webdriver.Firefox()  # 

options = webdriver.ChromeOptions()
selenium_url = 'http://localhost:4444/wd/hub' # <-- docker standalonee selenium chrome browser
options.add_argument('--headless')
    
driver = webdriver.Remote(command_executor=selenium_url,desired_capabilities=options.to_capabilities())

# Navigate to instagram post url
driver.get(url) 
  
i = 0 # <--- USED FOR CLICK COUNT
j = 0 # <--- THRESHOLD FOR FAILED CLICKED 

while j < threshold_for_failed_click:
    #print('J value is --> {}'.format(j))
    ##############################################
    # Sleep and give browser a chance to refresh
    sleep(time_to_wait_for_nxt_click) # <--- Time to wait until next click

    ##############################################
    # Try to find button to load more comments
    try: 
        element = driver.find_element(By.XPATH, '//button[./span[@aria-label="{}"]]'.format(xpath_aria_label_button))
    except:
        print("\nUnexpected error:", sys.exc_info()[0])
        j = j+1 # <--- Plus one for failed click
        continue
        
    ##############################################
    # Try to click button to load more comments
    print('Trying to click & load more comments --> {}'.format(i))

    try:
        ActionChains(driver).move_to_element(element).click().perform()
    except:
        print("\nUnexpected error:", sys.exc_info()[0])
        j=j+1 # <--- Plus one for failed click
        continue
    
    i=i+1 # <--- Successful cycle for clicked account, +1
    j = 0 # <--- FAILED CLICK COUNTER RESET
    
    if i > 500:
        print('oops! clicked 500 times apparently... not sure why this is happening so exiting this container to continue onward!')
        j=threshold_for_failed_click+1
    
    
##############################################
# Exporting HTML raw data

with open (raw_outfile,"w+") as f:
    print('Exporting to .html file --> {}'.format(raw_outfile))
    f.write(driver.page_source)
    
##############################################
# ETL conversion
driver.quit() # close out of chrome tab (or browser?)

comment_df = pd.DataFrame()

with open(raw_outfile, "r") as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')    

# Comments are ul objects in HTML
comments_html = soup.find_all('ul')

# Loop through comments in html file to extract ETL
for x in comments_html:

    a = x.find('div') 

    # get author name
    try:
        author = a.get_text(separator=' ').split(' ')[0] # <--- No spaces in Instagram usernames!
    except:
        author = None
        pass 

    # get comment on post
    try:
        comment = a.get_text(separator=' ').split(' ')[1:]   
        comment = " ".join(comment) 
    except:
        comment = None
        pass

    comment_df = comment_df.append(pd.DataFrame({'url':[url],'author':[author],'comment':[comment]}))

print('Done! Number of comments extracted --> {}'.format(comment_df.shape[0]))
print('Exporting ETL json file --> {}'.format(etl_outfile))

comment_df.reset_index(drop=True).to_json('{}'.format(etl_outfile)) 

print('Complete!')
print('-'*75)
