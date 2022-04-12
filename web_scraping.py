#importing required packages/modules
import requests,openpyxl
import csv
import pandas as pd
from bs4 import BeautifulSoup
import json
from sqlalchemy import create_engine

#for saving data in excel(xlsx) 
excel=openpyxl.Workbook()
sheet=excel.active
sheet.title='Flipkart mobiles'
sheet.append(['url','mobile_name','mobile_price','mobile_details'])

#append data into lists
list=[]
links_list=[]
names_list=[]
prices_list=[]
details_list=[]
id=1

#scraping data from many pages
for i in range(6):
    url='https://www.flipkart.com/search?q=mobiles&sid=tyy%2C4io&as=on&as-show=on&otracker=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&otracker1=AS_QueryStore_OrganicAutoSuggest_1_3_na_na_na&as-pos=1&as-type=RECENT&suggestionId=mobiles%7CMobiles&requestId=a99c7971-3954-4f9c-be34-ff3bcf0a9aa0&as-searchtext=mob&page='+str(i)    
    
    #getting response from url
    reqs = requests.get(url)
    
    #parsing html data
    soup = BeautifulSoup(reqs.text, 'html.parser')
    
    #getting urls data
    links=soup.find_all('img',class_='_396cs4 _3exPp9')
    
    #getting mobile names data
    names=soup.find_all('div',class_='_4rR01T')
    
    #getting mobile price data
    prices=soup.find_all('div',class_='_30jeq3 _1_WHN1')
    
    #getting mobile imformation data
    details=soup.find_all('ul',class_='_1xgFaf')
    
    #all required data stored in one zip file
    all=zip(links,names,prices,details)
    
    for link,name,price,detail in all:
        links_list.append(link.get('src'))#every single url link is stored into list
        names_list.append(name.text)
        prices_list.append(price.text)
        details_list.append(detail.text)
        
        #taking dictionary keys with empty valus for adding new values
        dic={'id':id,'img_url':'','mobile_name':'','mobile_price':'','mobile_details':''}
        dic['id']=id
        dic['img_url']=link.get('src')
        dic['mobile_name']=name.text
        dic['mobile_price']=price.text
        dic['mobile_details']=detail.text
        id=id+1
        
        #storing every dictionary into list(LIST OF DICTIONARIES)
        list.append(dic)
        
        #storing every record into excell sheet
        sheet.append([link.get('src'),name.text,price.text,detail.text])
        
#save the excell sheet     
excel.save('flipkart_mobiles_data.xlsx')
        
#final data convering into JSON 
json_data=json.dumps(list,indent=4)

#conncetion for mySQL database
my_connection=create_engine('mysql+mysqldb://root:@localhost/flipkart_data')


#data stored into dataframe
data={'url_name':links_list,'mobile_name':names_list,'mobile_price':prices_list,'mobile_details':details_list}
df=pd.DataFrame(data=data)

#importing data into database table
df.to_sql(con=my_connection,name='mobiles_data',if_exists='append',index=False)
