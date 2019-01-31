import pandas as pd
from pandas import DataFrame, Series
import re
import os
import googlemaps
apikey=open("APIkey.txt").readline()
# Get API key from prepared file
gmaps=googlemaps.Client(key=apikey)

dirlist=os.listdir(path="./another/")
for filename in dirlist:
    filepath="./another/"+filename
    ori_data = pd.read_excel(filepath,header=3,sheet_name=0,index_col=0) #打开当前文件
    # Import data
    citylist=list(ori_data.columns.str.strip())
    # Extract columns names as string (strip for blanks), and then convert them into list.  
    latitude=[]
    longtitude=[]
    for city in citylist:
        citycoding=gmaps.geocode(city) # Geocoding 当前城市
        if not citycoding==[]:
            city_lat=citycoding[0]["geometry"]["location"]["lat"] # Extract latitude from result   
            city_lng=citycoding[0]["geometry"]["location"]["lng"] # Extract longtitude from result
            if 3<city_lat<60 and 70<city_lng<140:   # Select results that located in China
                latitude.append(city_lat)
                longtitude.append(city_lng)
            else:
                print(city) # Check with city that failed to code and the index of this city
            #index_ll=count-1
                #print(index_ll)
                latitude.append(0)
                longtitude.append(0)
        else:   # Check with city that failed to code and the index of this city
            print(city)
        #index_ll=count-1
            #print(index_ll)
            latitude.append(0)
            longtitude.append(0)
    
    datadict={"city":citylist,"latitude":latitude,"longtitude":longtitude} # Setup dictionary to apply DataFrame method
    datareconstruct=DataFrame(datadict, columns=["city","latitude","longtitude"])
    print(datareconstruct)