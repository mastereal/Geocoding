import pandas as pd
from pandas import DataFrame, Series
ori_data = pd.read_excel("./data/flood_drought_EN.xlsx",header=0,sheet_name=0)
# Import data
citylist=list(ori_data.columns.str.strip())
# Extract columns names as string (strip for blanks), and then convert them into list.
import googlemaps
apikey=open("APIkey.txt").readline()
# Get API key from prepared file
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

latitude[14]=42.203591
longtitude[14]=116.485555

latitude[18]=39.08965
longtitude[18]=107.97616

latitude[26]=38.874434
longtitude[26]=115.464589

latitude[57]=27.087637
longtitude[57]=114.964696

latitude[97]=36.585445
longtitude[97]=109.489757

latitude[98]=34.341574
longtitude[98]=108.93977

latitude[112]=25.606486
longtitude[112]=100.267638

latitude[115]=22.78691
longtitude[115]=100.977164



datadict={"city":citylist,"latitude":latitude,"longtitude":longtitude} # Setup dictionary to apply DataFrame method
datareconstruct=DataFrame(datadict, columns=["city","latitude","longtitude"])
print(datareconstruct)

#datareconstruct.to_excel("./geocoding_result_floodanddrought.xlsx")
#datareconstruct.to_csv("./geocoding_result_floodanddrought.csv")

# Merge datareconstruct with ori_data
ori_data_T=ori_data.T   # Transpositon for the data
fin_data_coding=pd.merge(datareconstruct,ori_data_T,left_on="city",right_index=True)
# Merge coding and original data with respect of index "city"
print(fin_data_coding)
#fin_data_coding.to_excel("./geocoding_result_floodanddrought_fin.xlsx")
#fin_data_coding.to_csv("./geocoding_result_floodanddrought_fin.csv")