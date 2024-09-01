import requests
import json
from pandas import DataFrame as df
import asyncio
import aiohttp

class CarsData():
   
    apikey=""
    
    newKeys=[]
    tickers = {"Tesla":"TSLA", "Ford Motors":"F", "Honda Motors":"HMC", "Volkswagen":"VWAGY", "Mercedes-Benz":"MBGYY", "BMW":"BMWYY", "Nissan Motors":"NSAYY", "Toyota":"TM", "Ferrari":"RACE", "MARUTI SUZUKI INDIA LTD.":"MARUTI.BSE", "Tata Motors Limited":"TATAMOTORS.BSE", "Mahindra & Mahindra Ltd":"MAHMF"}
    tickerItems = list(tickers.items())

    functions = ["TIME_SERIES_INTRADAY", "TIME_SERIES_MONTHLY", "TIME_SERIES_WEEKLY"]

    url = f'https://www.alphavantage.co/query?'
    
    def __init__(self, newKeys=[]):
        self.newKeys=newKeys

    async def fetch(self, session, url):
        async with session.get(url) as response:
            return await response.json()

    # running more than  one api request simulataneously to gather data quickly for core month data
    async def efficientGetData(self, ticker, tickerName):
        selectMonths = input("Do you want to select months manually or auto select months(one after other) ? (1or2) - ")
        months =[]

        newUrl = self.url+f'function={self.functions[0]}&symbol={ticker[1]}&interval=60min' 
        urls=[]
        print(f'The apikey already provided will be used and has capacity of 5 requests.\nYou have provided {len(self.newKeys)} keys.\nSo total no. of months data that can be gathered is {5+5*len(self.newKeys)}\n(Time limit of 5 capacity is 1 minute for each key.)\n')
        if selectMonths=='1':
            print("Month format - 2024-04 -> YYYY-MM")
            j,k=0,0
            for i in range(len(self.newKeys)*5+5):
                month=input("Enter month - ")
                months.append(month)
                if j<5:
                    urls.append(newUrl+f'&month={month}&outputsize=full&apikey={self.apikey}')
                    j+=1
                else:
                    if len(self.newKeys)!=0 and k<len(self.newKeys):
                        urls.append(newUrl+f'&month={month}&outputsize=full&apikey={self.newKeys[k]}')
                        j+=1
                        if(j%5==0):
                            k+=1
            
            async with aiohttp.ClientSession() as session:
                tasks = [self.fetch(session, url) for url in urls]
                results = await asyncio.gather(*tasks)

                for s in range(len(months)):
                    self.storeData(1,json.dumps(results[s], indent=5), ticker[0], month=months[s], interval='60', eff=1)

        elif selectMonths=='2':
            print(f'Select the starting month. {5+5*len(self.newKeys) } will be selected after it')
            print("Month format - 2024-04 -> YYYY-MM")
            startMonth=input("Enter month - ")
            monthEntered = int(startMonth[5:])
            yearEntered = int(startMonth[0:4])
            newMonth=1
            k,j=0,0
            for i in range(len(self.newKeys)*5+5):
                if i==0:
                    months.append(startMonth)
                    urls.append(newUrl+f'&month={startMonth}&outputsize=full&apikey={self.apikey}')
                    # print(startMonth)
                elif i>=1:
                    if (monthEntered+1)<=12:
                        monthEntered+=1
                        if (len(str(monthEntered))==1):
                            newDate = str(yearEntered) +'-0'+str(monthEntered)
                        else:
                            newDate = str(yearEntered) +'-'+str(monthEntered)
                        print(newDate)
                        months.append(newDate)
                        if (i>=5):
                            urls.append(newUrl+f'&month={newDate}&outputsize=full&apikey={self.newKeys[k]}')
                            # print(k,j)
                            # print(newDate)
                            if (j>5 and j%5==0):
                                k+=1
                        else:
                            urls.append(newUrl+f'&month={newDate}&outputsize=full&apikey={self.apikey}')


                    elif (monthEntered+1)>12:
                        yearEntered+=1
                        newDate = str(yearEntered) +'-0'+str(newMonth) 
                        monthEntered=newMonth
                        

                        print(newDate)
                        if (i>=5):
                            urls.append(newUrl+f'&month={newDate}&outputsize=full&apikey={self.newKeys[k]}')
                            if (j%5==0):
                                k+=1
                        else:
                            urls.append(newUrl+f'&month={newDate}&outputsize=full&apikey={self.apikey}')
                j+=1    
            # print(urls)
            results=None
            async with aiohttp.ClientSession() as session:
                tasks = [self.fetch(session, url) for url in urls]
                results = await asyncio.gather(*tasks)

            for s in range(len(urls)-1):
                 
                # print(f'{months[s]}:-\n{results[s]}\n\n\n\n')
                self.storeData(1,json.dumps(results[s], indent=5), tickerName, month=months[s], interval='60', eff=2)
                
    # to get data in 3 types
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
        efficientWay = 0
        if (dataType == 1):
            moreDataGather = input("Do you want to gather more than one months core data and store it(Y/N)? ")
            if moreDataGather=='Y':
                efficientWay=1
                asyncio.run(self.efficientGetData(ticker[1], ticker[0]))
            else:
                month = input("Month - (Ex - 2024-05 - years-2024, month-may) - ")
                interval = input("Interval(Gap of stocks in minutes) - (For 60,30) - ")
                newUrl = f'function={self.functions[0]}&symbol={ticker[1]}&interval={interval}min&month={month}&outputsize=full&apikey={self.apikey}'


        elif (dataType==2):
            newUrl=f'function={self.functions[1]}&symbol={ticker[1]}&apikey={self.apikey}'

        elif (dataType==3):
            newUrl=f'function={self.functions[2]}&symbol={ticker[1]}&apikey={self.apikey}'

        if efficientWay==0:
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

    def storeData(self, dataType, jsonObject, tickerName, month, interval=0, eff=0):
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
            if eff==0:
                csv_file = f'{tickerName}_{interval}min_{month}.csv'
                convertedObject.to_csv(csv_file, index=False)
            elif eff==1:
                csv_file = f'{tickerName}_{interval}min_selectedMonths.csv'
                convertedObject.to_csv(csv_file, mode='a', index=False)
            elif eff==2:
                csv_file = f'{tickerName}_{interval}min_selectedMonthsAUTO.csv'
                convertedObject.to_csv(csv_file, mode='a', index=False)


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

    cars = CarsData(newKeys=[])
    cars.getData()

if __name__=="__main__":
    main()
