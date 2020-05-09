#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 11:46:19 2020

@author: jessicajakoby
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
from requests import get
import time

from urllib.request import Request, urlopen



pageurl = "https://amchainitiative.org/search-by-incident#incident/search/display-by-date/search/?view_279_per_page=1000&view_279_page=1"

options = webdriver.FirefoxOptions()
options.add_argument('headless')
capa = DesiredCapabilities.FIREFOX
capa["pageLoadStrategy"] = "none"
driver = webdriver.Firefox(firefox_options=options, desired_capabilities=capa, executable_path = '/usr/local/bin/geckodriver')
driver.set_window_size(1440,900)
driver.get(pageurl)
time.sleep(15)

plain_text = driver.page_source
soup = BeautifulSoup(plain_text, 'lxml')

incident_containers = soup.find_all('tr')

data = []
print(len(incident_containers))

for incident in incident_containers[1:]:
    
    # If the movie has Metascore, then extract:
    if incident.find('span', class_ = 'col-0') is not None:
        school_name = incident.find('span', class_ = 'col-0').span.text
        
    if incident.find('span', class_ = 'col-1') is not None:
        date = incident.find('span', class_ = 'col-1').text
        
    if incident.find('span', class_ = 'col-2') is not None:
        category = incident.find('span', class_ = 'col-2').text
        
    if incident.find('span', class_ = 'col-3') is not None:
        description = incident.find('span', class_ = 'col-3').text
        
    if incident.find('span', class_ = 'col-4') is not None:
        details = incident.find('span', class_ = 'col-4').a['href']
    
    data.append([school_name, date, category, description, details])
    
    
df1 = pd.DataFrame(data, columns=["school", "date", "category", "description", "details"])
df1.to_csv ("/Users/jessicajakoby/Documents/WN_2020/INFO5330_TMD/Hackathon Anti-Semitism/amcha.csv", index = None, header=True)



