import json
import pandas
import requests
from bs4 import BeautifulSoup

def solveByJson():
    jsonRequestUrl = 'https://www.ica.se/Templates/GlobalSearch/Handlers/GlobalSearchHandler.ashx?CommandName=GetAllStoresInProfile&Profile=all'
    jsonRequest = requests.get(jsonRequestUrl)
    jsonConversionToListOfDictionary = jsonRequest.json()
    
    listOfDictionary = []
    for Store in jsonConversionToListOfDictionary:
        listOfDictionary.append({"MarketingName": Store['MarketingName'],
        "VisitingAddress": Store['VisitingAddress'],
        "PostCode": Store['PostCode'],
        "TelephoneNumber" : Store['TelephoneNumber']})

    pandas.DataFrame(listOfDictionary).to_excel('output.xlsx', header=False, index=False)

def solveBySoup():
    URL = 'https://www.ica.se/butiker/'
    URL2 = 'https://www.ica.se'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    allLiItems = soup.findAll('li')

    liItemHrefValue = []
    for item in allLiItems:
        aElement = item.find('a')
        liItemHrefValue.append(aElement.get('href'))
    
    #Get all store links
    storeLinks =  [URL2 + l for l in liItemHrefValue if '/butiker' in l]

    #Store info start at 7
    for i in range(7):
        storeLinks.pop(0)
    
    #Ale
    #print(storeLinks[0])

    # for link in storeLinks:
    #     page2 = requests.get(link)
    #     soup2 = BeautifulSoup(page2.content , 'html.parser')
    #     store = soup2.findAll("class", class_="store-card-main-content")
    #     print(store)

    page2 = requests.get(storeLinks[0])
    soup2 = BeautifulSoup(page2.content, 'html.parser')
    stores = soup2.findAll("div", class_="store-card-main-content")
    
    print(stores)

    testList = []
    for item in stores:
        aElement = item.find("div")
        testList.append(aElement.get('class'))

    print(testList)

    #storeName =  soup2.select_one('class', class_="card-heading column size20of20 md_size2of3")


def main():
    #solveByJson()
    solveBySoup()
   





if __name__ == "__main__":
    main()

   

    
    # #<div class="store-card-main-content">
	# 		                    <header class="card-header grid_fluid no_padding">
	# 			                    <div class="card-heading column size20of20 md_size2of3 ">ICA Kvantum Ale</div>
	# 			                    <div class="card-open-hours column size1of3 md_lte_hidden">Öppet idag: 7-23</div>
	# 		                    </header>
	# 		                    <div class="store-card-content grid_fluid no_padding">
	# 			                    <div class="column size20of20 md_size1of3">
	# 				                    <div class="store-address">
	# 					                    <div class="street-name">Ale Torg 7</div>
	# 					                    <span class="zip-code">44931</span>
	# 					                    <span>NÖDINGE</span>
    #                                         <span class="card-open-hours card-open-hours--small md_gte_hidden">Öppet idag: 7-23</span>
	# 				                    </div>
    #                                     <div class="store-quick-contact">
	# 				                        <a href="#" class="store-card-navigation-link sprite2-p" target="_blank">Hitta hit</a>
    #                                         <a href="/Templates/Stores/Views/Pages/0303-97500" class="store-card-phone-number sprite2-p">0303-97500</a>
    #                                     </div>