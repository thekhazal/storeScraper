import json
import pandas
import requests
from bs4 import BeautifulSoup

def populateListOfDictionary(listOfDictionary, marketingName, visitingAddress, postCode, telephoneNumber ):
    listOfDictionary.append(
        {"MarketingName": marketingName,
        "VisitingAddress": visitingAddress,
        "PostCode": postCode,
        "TelephoneNumber" : telephoneNumber})

def solveByJson():
    jsonRequestUrl = 'https://www.ica.se/Templates/GlobalSearch/Handlers/GlobalSearchHandler.ashx?CommandName=GetAllStoresInProfile&Profile=all'
    jsonRequest = requests.get(jsonRequestUrl)
    jsonConversionToListOfDictionary = jsonRequest.json()

    listOfDictionary = []
    for Store in jsonConversionToListOfDictionary:
        populateListOfDictionary(listOfDictionary,
            Store['MarketingName'],
            Store['VisitingAddress'],
            Store['PostCode'],
            Store['TelephoneNumber'])

    pandas.DataFrame(listOfDictionary).to_excel('solveByJson.xlsx', header=False, index=False)

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
    for i_ in range(7):
        storeLinks.pop(0)

    listOfDictionary = []
    for storeLink in storeLinks:
        page2 = requests.get(storeLink)
        soup2 = BeautifulSoup(page2.content, 'html.parser')

        for store in soup2.findAll("div", class_="store-card-main-content"):
            populateListOfDictionary(listOfDictionary,
                store.find("div", class_="card-heading column size20of20 md_size2of3").text,
                store.find("div", class_="street-name").text,
                store.find("span", class_="zip-code").text,
                store.find("a", class_="store-card-phone-number sprite2-p").text)

    pandas.DataFrame(listOfDictionary).to_excel('solveBySoup.xlsx', header=False, index=False)

def main():
    solveByJson()
    solveBySoup()

if __name__ == "__main__":
    main()