import requests
import json
from pandas import DataFrame as df

class CarsData():
    apikey = "CO7UX79Q1LX1B1IG"
    tickers = {"Tesla":"TSLA", "Ford Motors":"F", "Honda Motors":"HMC", "Volkswagen":"VWAGY", "Mercedes-Benz":"MBGYY", "BMW":"BMWYY", "Nissan Motors":"NSAYY", "Toyota":"TM", "Ferrari":"RACE", "MARUTI SUZUKI INDIA LTD.":"MARUTI.BSE", "Tata Motors Limited":"TATAMOTORS.BSE", "Mahindra & Mahindra Ltd":"MAHMF"}
    tickerItems = list(tickers.items())

    functions = ["TIME_SERIES_INTRADAY", "TIME_SERIES_MONTHLY", "TIME_SERIES_WEEKLY"]

    url = f'https://www.alphavantage.co/query?'
    
    def __init__(self):
        print("Fuck you")

    def getData(self):
        i=1
        for key,value in self.tickers.items():
            print(f'{i}. {key} - {value}')
            i+=1

        option = int(input("Enter index of tickers - (1->tesla, 2->ford) - "))
        ticker = self.tickerItems[option-1]

        dataType = int(input("1.Get Monthly data(of each day)\n2. Get Monthly data (for 20 years but one day of each month)\n3. Get weekend data only for 20 years\n- "))
        interval=0
        month=0
        if (dataType == 1):
            month = input("Month - (Ex - 2024-05 - years-2024, month-may) - ")
            interval = input("Interval(Gap of stocks in minutes) - (For 60,30) - ")
            newUrl = f'function={self.functions[0]}&symbol={ticker[1]}&interval={interval}min&month={month}&outputsize=full&apikey={self.apikey}'

        elif (dataType==2):
            newUrl=f'function={self.functions[1]}&symbol={ticker[1]}&apikey={self.apikey}'

        elif (dataType==3):
            newUrl=f'function={self.functions[2]}&symbol={ticker[1]}&apikey={self.apikey}'


        finalUrl = self.url+newUrl
        print()
        print(finalUrl)
        print("if any error,, first check the above url in web. If a error message is shown then choose different type of functions like monthly, weekly")
        dataObject = self.sendRequest(finalUrl)

        if dataObject!=False:
            self.storeData(dataType, dataObject, ticker[0], month, interval=interval)
        else:
            print("No internet")
        with open("data.json", "w") as f:
            f.write(dataObject)

    def storeData(self, dataType, jsonObject, tickerName, month, interval=0):
        data = json.loads(jsonObject)
        filteredData = []

        if (dataType==1):
            if (interval=='60'):
                newJsonData = data['Time Series (60min)']


                itemsObj = list(newJsonData.items())

                for i in range(len(newJsonData)):
                    itemObj= list(itemsObj[i][1].items())
                    testObject={"date/time":itemsObj[i][0], "open":itemObj[0][1], "high":itemObj[1][1], "low":itemObj[2][1], "close":itemObj[3][1], "volume":itemObj[4][1]}
                    filteredData.append(testObject)

            elif (interval=='30'): 
                newJsonData = data['Time Series (30min)']


                itemsObj = list(newJsonData.items())

                for i in range(len(newJsonData)):
                    itemObj= list(itemsObj[i][1].items())
                    testObject={"date/time":itemsObj[i][0], "open":itemObj[0][1], "high":itemObj[1][1], "low":itemObj[2][1], "close":itemObj[3][1], "volume":itemObj[4][1]}
                    filteredData.append(testObject)       

            convertedObject = df(filteredData)
            csv_file = f'{tickerName}_{interval}min_{month}.csv'
            convertedObject.to_csv(csv_file, index=False)

        elif dataType==2:
            newJsonData = data['Monthly Time Series']

            itemsObj = list(newJsonData.items())

            for i in range(len(newJsonData)):
                itemObj= list(itemsObj[i][1].items())
                testObject={"date/time":itemsObj[i][0], "open":itemObj[0][1], "high":itemObj[1][1], "low":itemObj[2][1], "close":itemObj[3][1], "volume":itemObj[4][1]}
                filteredData.append(testObject)

            convertedObject = df(filteredData)
            csv_file = f'{tickerName}_20yearsmonthly.csv'
            convertedObject.to_csv(csv_file, index=False)

        elif dataType==3:
            newJsonData = data['Weekly Time Series']

            itemsObj = list(newJsonData.items())

            for i in range(len(newJsonData)):
                itemObj= list(itemsObj[i][1].items())
                testObject={"date/time":itemsObj[i][0], "open":itemObj[0][1], "high":itemObj[1][1], "low":itemObj[2][1], "close":itemObj[3][1], "volume":itemObj[4][1]}
                filteredData.append(testObject)

            convertedObject = df(filteredData)
            csv_file = f'{tickerName}_20yearsweekly.csv'
            convertedObject.to_csv(csv_file, index=False)

    def sendRequest(self, url):
        try:
            request = requests.get(url)
            data = request.json()
            dataObject = json.dumps(data, indent=5)
            return dataObject
        
        except Exception as e:
            return 0

def main():
    cars = CarsData()
    
    cars.getData()

if __name__=="__main__":
    main()
