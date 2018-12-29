#from googletrans import Translator # "googletrans" is not stable
from google.cloud import translate  # Use google cloud API instead
import pandas as pd # pd is abbreviation of Pandas, easy to remember
from pandas import DataFrame, Series

print("Every thing is OK. Programe is operated approximately") # A test for the script

translate_client=translate.Client()

ori_data = pd.read_excel("./data/flood_drought_CN.xlsx",header=0,sheet_name=0)
# Input data from excel, since csv need encoding and would not drop vacant columns)
print(ori_data) # Check for the data

citylist=list(ori_data.columns.str.strip()) 
# Extract columns names as string (strip for blanks), and then convert them into list.
#print(citylist)



citylist_EN=[]  # Prepare an empty list
count=0
def is_chinese(uchar):         
    if '\u4e00' <= uchar<='\u9fff':
        return True
    else:
        return False
# Check if the variable is Chinese
def is_other(uchar):
    if not is_chinese(uchar):
        return True
    else:
        return False
# Check if the variable is not Chinese
for city in citylist:
    #translator=Translator() # Try to initialize
    count +=1 # count in case some missing translation
    dic_city=translate_client.translate(city)
    # Translate very city in citylist
    #print(t_city.text)
    #print(type(t_city))
    #print(count)
    t_city=dic_city["translatedText"]
    citylist_EN.append(str(t_city))
        # Add translations into new list. Convert translations into string
    #else:
        #citylist_EN.append("0")
        # Some words are not translated. Replace them with "0"
       
        # This try was failed in this sample 
print(citylist_EN)

i_replace_1=citylist_EN.index("Shijiazhuang")+1
i_replace_2=citylist_EN.index("Fuyang")+1
i_replace_3=citylist_EN.index("Xinyang")+1
i_replace_4=citylist_EN.index("Ji County")
i_replace_5=citylist_EN.index("Zhang Wei")
i_replace_6=citylist_EN.index("Bailing Temple")
i_replace_7=citylist_EN.index("Shaanxi Dam")
i_replace_8=citylist_EN.index("Parry")
i_replace_9=citylist_EN.index("Yue Yang")
# Obtain the index, of which the translation did not success
citylist_EN[i_replace_1]="Handan"
citylist_EN[i_replace_2]="Bengbu"
citylist_EN[i_replace_3]="Dezhou"
citylist_EN[i_replace_4]="Yun County"
citylist_EN[i_replace_5]="Zhangye"
citylist_EN[i_replace_6]="Bailingmiao"
citylist_EN[i_replace_7]="Shanbazhen"
citylist_EN[i_replace_8]="Palizhen"
citylist_EN[i_replace_9]="Yueyang"
# Replace with correct translation
print(citylist_EN)
print(ori_data.columns)

ori_data.columns=citylist_EN
print(ori_data)
# Change column names into English

# Then all the cities were translated into English, and were in the list.
# Next part is to Geocoding

#ori_data.to_csv("./data/flood_drought_EN.csv")
#ori_data.to_excel("./data/flood_drought_EN.xlsx")
# In case of API failed. The data would be export to csv

import googlemaps
gmaps=googlemaps.Client(key="AIzaSyC5OpS9gqtZqG1zWLsqs_sa8CuKysTpt3g")
# Setup python client for geocoding API
latitude=[]
longtitude=[]
count=0
for city in citylist_EN:
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



datadict={"city":citylist_EN,"latitude":latitude,"longtitude":longtitude} # Setup dictionary to apply DataFrame method
datareconstruct=DataFrame(datadict, columns=["city","latitude","longtitude"])
print(datareconstruct)