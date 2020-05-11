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
from sqlalchemy import create_engine
from urllib.request import Request, urlopen
import pymysql
import datetime
import requests
import json
 
def search_places_by_coordinate(query, url):
        
        params = {
            'query': query,
            'types': 'university',
            'key': 'AIzaSyB0cJMuJGmoGDCS3GP3Yo3hPriPRxYDWsE'
        }
        res = requests.get(url, params = params)
        if res.status_code == 200:
            response, name, lat, lng = None, None, None, None
            json_results = json.loads(res.content)
            
    #        print(json_results)
            if json_results.get("results", []):
                name = json_results["results"][0]["name"]
                location = json_results["results"][0]["geometry"]["location"]
                lat = location["lat"]
                lng = location["lng"]
            response = {"query": query, "name": name, "lat": lat, "lng": lng}
        return response
    
    


 



pageurls = ["https://amchainitiative.org/search-by-incident#incident/search/display-by-date/search/?view_279_per_page=1000&view_279_page=1", "https://amchainitiative.org/search-by-incident#incident/search/display-by-date/search/?view_279_per_page=1000&view_279_page=2", "https://amchainitiative.org/search-by-incident#incident/search/display-by-date/search/?view_279_per_page=1000&view_279_page=3", "https://amchainitiative.org/search-by-incident#incident/search/display-by-date/search/?view_279_per_page=1000&view_279_page=4"]

data = []
dfs = []
uni_location = {}
i = 1
for pageurl in pageurls:
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
    
    
    
    for incident in incident_containers[1:]:
        
        # If the movie has Metascore, then extract:
        if incident.find('span', class_ = 'col-0') is not None:
            school_name = incident.find('span', class_ = 'col-0').span.text
            if school_name not in uni_location:
                
                r = search_places_by_coordinate(school_name, "https://maps.googleapis.com/maps/api/place/textsearch/json")
                lat, lng = r["lat"], r["lng"]
                uni_location[school_name] = [lat, lng]
            else:
                lat = uni_location[school_name][0]
                lng = uni_location[school_name][1]
            
            
            
        if incident.find('span', class_ = 'col-1') is not None:
            date = incident.find('span', class_ = 'col-1').text
            
        if incident.find('span', class_ = 'col-2') is not None:
            category = incident.find('span', class_ = 'col-2').text
            
        if incident.find('span', class_ = 'col-3') is not None:
            description = incident.find('span', class_ = 'col-3').text
            
        if (incident.find('span', class_ = 'col-4') != None) and (incident.find('span', class_ = 'col-4').a != None):
            details = incident.find('span', class_ = 'col-4').a['href']
        
        data.append([school_name, date, category, description, details, lat, lng])
    
#    df_int = pd.DataFrame(data, columns=["school", "date", "category", "description", "details", "lat", "lng"])
#    path = "/Users/jessicajakoby/Documents/WN_2020/INFO5330_TMD/Hackathon Anti-Semitism/amchaFull" + str(i) + ".csv"
#    df_int.to_csv (path, index = None, header=True)
#    print("saved", df_int.size, i)
#    dfs.append(df_int)
#    i= i +1
    i = i+1
    print("page ", i , " ", len(data))


df = pd.DataFrame(data, columns=["school", "date", "category", "description", "details", "lat", "lng"]) 

df.to_csv ("/Users/jessicajakoby/Documents/WN_2020/INFO5330_TMD/Hackathon Anti-Semitism/amchaFullComp.csv", index = None, header=True)
print("done") 

#db_data = 'mysql+pymysql://admin:tastmaster@database-1.c8zq0mtv01cc.us-east-2.rds.amazonaws.com:3306/sys'
#
#engine = create_engine(db_data)
#
#start = datetime.datetime.now()
#df1.to_sql(con=engine, name='Incidents', if_exists='replace', chunksize=10000)
#print("The query executed in: " + str((datetime.datetime.now() - start).total_seconds()) + "s")



