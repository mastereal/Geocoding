# -*- coding: UTF-8 -*-
import pandas as pd # pd is abbreviation of Pandas, easy to remember
from pandas import DataFrame, Series

ori_data = pd.read_excel("./data/flood_drought_CN.xlsx",header=0,sheet_name=0)
# Input data from excel, since csv need encoding and would not drop vacant columns)
#print(ori_data) # Check for the data

citylist=list(ori_data.columns.str.strip()) 
# Extract columns names as string (strip for blanks), and then convert them into list.
print(citylist)


import googlemaps
apikey=open("APIkey.txt").readline()
gmaps=googlemaps.Client(key=apikey)
# Setup python client for geocoding API
latitude=[]
longtitude=[]
count=0
for city in citylist:
    citycoding=gmaps.geocode(city)
    count+=1
    #print(count)
    #print(citycoding)
    #keylist=citycoding[0].keys()
    #print(keylist)
    if not citycoding==[]:
        city_lat=citycoding[0]["geometry"]["location"]["lat"] # Extract latitude from result   
        city_lng=citycoding[0]["geometry"]["location"]["lng"] # Extract longtitude from result
        if 3<city_lat<60 and 70<city_lng<140:   # Select results that located in China
            latitude.append(city_lat)
            longtitude.append(city_lng)
        else:
            print(city) # Check with city that failed to code and the index of this city
            index_ll=count-1
            print(index_ll)
            latitude.append(0)
            longtitude.append(0)
    else:   # Check with city that failed to code and the index of this city
        print(city)
        index_ll=count-1
        print(index_ll)
        latitude.append(0)
        longtitude.append(0)


datadict={"city":citylist,"latitude":latitude,"longtitude":longtitude} # Setup dictionary to apply DataFrame method
datareconstruct=DataFrame(datadict, columns=["city","latitude","longtitude"])
print(datareconstruct)

#datareconstruct.to_csv("./geocoding_flood_drought_CN.csv")
datareconstruct.to_excel("./geocoding_flood_drought_CN.xlsx")