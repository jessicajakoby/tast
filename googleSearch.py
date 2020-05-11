#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 18:54:52 2020

@author: jessicajakoby
"""
import requests
import json
import pandas as pd


#class GooglePlaces(object):
#    def __init__(self, apiKey):
#        super(GooglePlaces, self).__init__()
#        self.apiKey = 'AIzaSyB0cJMuJGmoGDCS3GP3Yo3hPriPRxYDWsE'
#    
#    def search_places_by_coordinate(self, query, types):
#        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
#        params = {
#            'query': query,
#            'types': 'university',
#            'key': self.apiKey
#        }
#        res = requests.get(endpoint_url, params = params)
#        results = json.loads(res.content)
#        return results
#
#googleAPI = GooglePlaces
from geopy.geocoders import GoogleV3
import csv

def get_component(location, component_type):
    for component in location.raw['address_components']:
        if component_type in component['types']:
            return component['long_name']
        

key = 'AIzaSyB0cJMuJGmoGDCS3GP3Yo3hPriPRxYDWsE'
geolocator = GoogleV3(key)
file_path = "/Users/jessicajakoby/Documents/WN_2020/INFO5330_TMD/Hackathon Anti-Semitism/amchaFullComp.csv"

coord_state = []
seen = set()

with open(file_path, "r") as f_in:
    records = csv.reader(f_in)
    next(records)
    
    for record in records:
        city, state, lat, lng = None, None, None, None
        name = record[0]
        if name not in seen:
            if record[5] and record[6]:
                lat, lng = float(record[5]), float(record[6])
                loc = tuple([lat, lng])
                location = geolocator.reverse(loc, timeout = 10,  exactly_one=True)
    #            print(location.raw)
                location = location.address.split(', ')
                if len(location)==4:
                    city = location[1]
                    state = location[2].split()[0]
                elif len(location)==5:
                    city = location[2]
                    state = location[3].split()[0]
            entry = [name, city, state]
            seen.add(name)
            coord_state.append(entry)

df1 = pd.DataFrame(coord_state, columns = ['Name', 'City', 'State'])
df1.to_csv ("/Users/jessicajakoby/Documents/WN_2020/INFO5330_TMD/Hackathon Anti-Semitism/school_locationFullComp.csv", index = None, header=True)




#
#
#search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
#endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
#def search_places_by_coordinate(query, url):
#        response,  = None
#        params = {
#            'query': query,
#            'types': 'university',
#            'key': 'AIzaSyB0cJMuJGmoGDCS3GP3Yo3hPriPRxYDWsE'
#        }
#        res = requests.get(url, params = params)
#        if r.status_code == 200:
#            json_results = json.loads(res.content)
#    #        print(json_results)
#            if data.get("results", []):
#                name = json_results["results"][0]["name"]
#                location = json_results["results"][0]["geometry"]["location"]
#                lat = location["lat"]
#                long = location["lng"]
#                response = {"query": query, "name": name, "lat": lat, "long": long}
#                return response
#        return response
#    
#    
#
#r = search_places_by_coordinate("CSU Chico", "https://maps.googleapis.com/maps/api/place/textsearch/json")
#print(r)