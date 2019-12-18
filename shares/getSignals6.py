### get ticker daya from yahoo api service
### use library functions to calculate RSI, SMA
### develope functions for calculating ATR, Choppines
### save data in csv format, print logs

# import statements
import pandas as pd
import pandas_datareader.data as web
import datetime
from datetime import timedelta,date
from talib import RSI
from talib import SMA
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc

# note execution start time
start_time = datetime.datetime.now()

# currently input data is hardcoded below, which can later be configured
# loop for each symbol within list
#listTickerSymbol = ['^NSEI','^NSEBANK','UPL.NS','BAJAJFINSV.NS','ZEEL.NS','TATASTEEL.NS','VEDL.NS','YESBANK.NS','GRASIM.NS','JSWSTEEL.NS','HINDALCO.NS','TECHM.NS','BPCL.NS','BHARTIARTL.NS','HEROMOTOCO.NS','BAJFINANCE.NS','SBIN.NS','INDUSINDBK.NS','M&M.NS','AXISBANK.NS','BAJAJ-AUTO.NS','ICICIBANK.NS','TITAN.NS','LT.NS','MARUTI.NS','INFY.NS','RELIANCE.NS','ITC.NS','CIPLA.NS','ULTRACEMCO.NS','POWERGRID.NS','HDFC.NS','INFRATEL.NS','GAIL.NS','HDFCBANK.NS','TCS.NS','HINDUNILVR.NS','IOC.NS','NTPC.NS','HCLTECH.NS','ASIANPAINT.NS','EICHERMOT.NS','ADANIPORTS.NS','TATAMOTORS.NS','ONGC.NS','KOTAKBANK.NS','BRITANNIA.NS','DRREDDY.NS','COALINDIA.NS','WIPRO.NS','IBULHSGFIN.NS','SUNPHARMA.NS']
# listTickerSymbol =['TVSMOTOR.NS','YESBANK.NS','^NSEI']
listTickerSymbol = ['^NSEI','TVSMOTOR.NS']

# baseLocation = "Z:\\Automation\\Python\\Technical Analysis\\data\\"
baseLocation = "C:\\Abhishek\\Automation\\TechnicalAnalysis\\pkTechAnalysis\\data\\"
logFileName = "TechnicalCalls.txt"
fileMode = "w+"
outputFileName = "TechnicalCallsData.csv"

logFile = open(baseLocation+logFileName, fileMode)


def calATR(close, high, low, prd):
    trueMaxDHL = []
    trueDiff = []
    trueHigh = []
    trueLow = []
    trueRange = []
    avgTrueRange = []
    atr = 0
    for i in range(len(close)):
        if i == 0:
            trueDiff.append(0)
            trueHigh.append(0)
            trueLow.append(0)
            # trueMaxDHL.append(0)
            trueRange.append(trueHigh[i] - trueLow[i])
            # atr = (trueRange[i - 1] * (prd - 1) + trueRange[i]) / prd
            atr =0
            avgTrueRange.append(atr)
        else:
            trDiff = high[i]-low[i]
            trHigh = abs(high[i]-close[i-1])
            trLow = abs(close[i-1]-low[i])
            trueDiff.append(trDiff)
            trueHigh.append(trHigh)
            trueLow.append(trLow)
            # trueMaxDHL.append(max(trueDiff[i],trueHigh[i],trueLow[i]))
            # trueHigh.append(max(high[i],close[i-1]))
            # trueLow.append(min(low[i],close[i-1]))
            # trueRange.append(trueHigh[i]-trueLow[i])
            # atr = (trueRange[i-1]*(prd-1)+trueRange[i])/prd
            atr = max(trDiff,trHigh, trLow)
            avgTrueRange.append(atr)
    # print(avgTrueRange)
    return avgTrueRange

def choppiness(close, high, low, prd, avgTrueReturn):
    tp = prd
    ATR = avgTrueReturn
    CP = []
    Timestamp = []
    sumATR = 0
    maxHigh = 0
    minLow = 0
    for i in range(len(close)):
        if i < tp*2:
            CP.append(0)
        else:
            sumATR = sum(ATR[i-tp+1:i+1])
            maxHigh = max(high[i-tp+1:i+1])
            minLow = min(low[i-tp+1:i+1])
            # print('i, tp, i-tp, sumATR, maxHigh, minLow, ATR', i, tp, i-tp, sumATR, maxHigh, minLow, ATR[i])
            nmrt = np.log10(sumATR/abs(maxHigh-minLow))
            # nmrt = np.log10(np.sum(ATR[i - tp :i]) / (max(high[i - tp:i]) - min(low[i - tp:i])))
            dnmnt = np.log10(tp)
            CP.append(100*nmrt/dnmnt)
            print(i,ATR[i], sumATR, maxHigh - minLow, nmrt, dnmnt, sep=' / ')
    return CP

def findSignal(lstIndicators):
    prevCall = ''
    todayCall = ''
    countSignal = 0
    # toPrint = 'The signal(s) for symbol: ' + tickerSymbol + ' between ' + sDate + ' and ' + eDate + ' are as follows: '
    # print(toPrint)

    for day in lstIndicators:
        lstSignal = []

        if day[8] < day[9]:
            sma_call = 'SELL'
        elif day[8] >= day[9]:
            sma_call = 'BUY'
        todayCall = sma_call

        today = day[0]
        if todayCall == 'BUY':
            if prevCall == 'SELL':
                lstSignal.append(today)
                lstSignal.append(todayCall)
                lstSignal.append(day[4])
                lstSignal.append(day[7])
                lstSignal.append(day[11])
        if todayCall == 'SELL':
            if prevCall == 'BUY':
                lstSignal.append(today)
                lstSignal.append(todayCall)
                lstSignal.append(day[4])
                lstSignal.append(day[7])
                lstSignal.append(day[11])
        prevCall = todayCall
        if len(lstSignal) > 0:
            countSignal += 1
            print(lstSignal[0], lstSignal[2], lstSignal[1], lstSignal[3], lstSignal[4], sep=' | ', end= '\n')
            # toPrint = 'Date: ' + lstSignal[0] +  ', Close: ' + str(round(lstSignal[2],2)) + ', Call: ' + lstSignal[1]
            # print(toPrint)
            # x.write(toPrint)
            # x.write('\n')
            #print()

    if countSignal == 0:
        print('No Signal for given period!')
        x.write('No Signal for given period!')
        x.write('\n\n')

    print()
    #print(lstIndicators[2])


def plotCandleStick(allDays, allDates, listRSI, listChop, listSMA1, listSMA2, periodChop, periodSMA1, periodSMA2, periodRSI, symbol, filePath):
    # plotCandleStick(listCandlestickMaster, listDates, listRSI, listChop, listSMA1, listSMA2, periodChop, periodSMA1,
    #                 periodSMA2, periodRSI, tickerSymbol, baseLocation + outputChartName)
    # print("inside plotCandleStick: ", filePath )
    strDateFormat = '%m/%d/%Y'

    # fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1)
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
    candlestick_ohlc(ax1, allDays, width=0.5, colorup='g', colordown='r')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter(strDateFormat))
    title = symbol
    # ax1.plot(allDates[14:], listSMA1[14:])
    # ax1.plot(allDates[14:], listSMA2[14:])
    ax1.set_title(title)
    ax1.set_ylabel('Candlestick')

    # plt.show()
    # plt.savefig("C:\\Abhishek\\Automation\\TechnicalAnalysis\\data\\abc.png")
    ax2.plot(allDates[periodRSI*3:], listRSI[periodRSI*3:],label='RSI')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter(strDateFormat))
    ax2.set_ylabel('RSI (14) / Choppiness (14)')

    ax2.plot(allDates[periodChop*2:], listChop[periodChop*2:],label='Choppiness')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter(strDateFormat))
    # ax2.set_ylabel('CHOPPINESS (14)')
    ax2.legend()

    ax1.plot(allDates[periodSMA1:], listSMA1[periodSMA1:],label= 'SMA(5)',color ='g')
    ax1.plot(allDates[periodSMA2:], listSMA2[periodSMA2:],label='SMA(20)',color='r')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter(strDateFormat))
    ax1.set_ylabel('SMA (5 & 20)')
    ax1.legend()

    plt.show()
    plt.savefig(filePath)
    plt.close()


# for loop for each symbol within list
for tickerSymbol in listTickerSymbol:
    apiService = 'yahoo'

    strDateFormat = '%m/%d/%Y'
    strDateFormat1 = '%m%d%Y'
    sDate = '5/1/2019'
    eDate = '8/31/2019'

    intPeriod = 1
    strPeriod = 'D'

    periodRSI = 14
    lowRSI = 20
    highRSI = 80
    periodSMA1 = 5
    periodSMA2 = 20
    periodChop = 14
    lowChop = 38.2
    highChop = 61.8
    midChop = 50
    periodBollinger = 14
    periodVortex = 14
    periodMax = 36  ### max of all above

    toPrint = ''

    listCandlestickToday = []
    listCandlestickMaster = []
    listMaster = []
    listDay = []
    listDates = []
    listOpen = []
    listHigh = []
    listLow = []
    listClose = []
    listAdjClose = []
    listVolume = []

    rsi_today = 0

    start = datetime.datetime.strptime(sDate, strDateFormat)
    end = datetime.datetime.strptime(eDate, strDateFormat)
    thisDate = start

    outputFileName = 'TechnicalCallsData_'+tickerSymbol+'_'+start.strftime(strDateFormat1)+'_To_'+end.strftime(strDateFormat1)+'.CSV'
    outputChartName = 'TechnicalCallsData_'+tickerSymbol+'_'+start.strftime(strDateFormat1)+'_To_'+end.strftime(strDateFormat1)+'.png'

    if strPeriod == 'D':
        delta = timedelta(days=intPeriod)

    # retrieve OHLCV data from api service for given symbol
    try:
        dataTicker = web.DataReader(tickerSymbol, apiService, start, end)
    except:
        toPrint = 'ERROR: Could not read data from api for ' + tickerSymbol + ' !!!\n'
        print(toPrint)

    listDates = dataTicker.index
    listHigh = dataTicker.High
    listLow = dataTicker.Low
    listOpen = dataTicker.Open
    listClose = dataTicker.Close
    listVolume = dataTicker.Volume
    listAdjClose = dataTicker.Close # change it to Adj Close
    listRSI = []
    listSMA1 = []
    listSMA2 = []
    listATR = []
    listChop = []

    lenTicker = len(listClose)
    print('lenTicker', lenTicker)

    for i in range(lenTicker):
        listDay = []
        listDay.append(listDates[i].strftime(strDateFormat))
        listDay.append((listHigh[i]))
        listDay.append((listLow[i]))
        listDay.append((listOpen[i]))
        listDay.append((listClose[i]))
        listDay.append((listVolume[i]))
        listDay.append((listAdjClose[i]))
        listMaster.append(listDay)

        listCandlestickToday =[]
        listCandlestickToday.append(mdates.date2num(listDates[i])) #.strftime(strDateFormat))
        listCandlestickToday.append((listOpen[i]))
        listCandlestickToday.append((listHigh[i]))
        listCandlestickToday.append((listLow[i]))
        listCandlestickToday.append((listClose[i]))
        listCandlestickToday.append((listVolume[i]))
        listCandlestickMaster.append(listCandlestickToday)

    # calculate RSI
    for i in range(lenTicker):
        if i < periodMax:
            rsi_today = 0
            listRSI.append((rsi_today))
        else:
            rsi = RSI(dataTicker.Close[i-periodMax+1:i+1], periodRSI)
            rsi_today = rsi[-1]
            listRSI.append((rsi_today))

    # calculate SMA 1
    for i in range(lenTicker):
        if i < periodSMA1:
            sma1_today = 0
            listSMA1.append((sma1_today))
        else:
            sma1 = SMA(dataTicker.Close[i-periodSMA1+1:i+1], periodSMA1)
            sma1_today = sma1[-1]
            listSMA1.append((sma1_today))

    # calculate SMA 2
    for i in range(lenTicker):
        if i < periodSMA2:
            sma2_today = 0
            listSMA2.append((sma2_today))
        else:
            sma2 = SMA(dataTicker.Close[i-periodSMA2+1:i+1], periodSMA2)
            sma2_today = sma2[-1]
            listSMA2.append((sma2_today))

    # calculate ATR
    # for i in range(lenTicker):
    avgTrueReturn = calATR(dataTicker.Close, dataTicker.High, dataTicker.Low, periodChop)
    # valATR = avgTrueReturn[-1]

    # calculate Choppiness index
    CP = choppiness(dataTicker.Close, dataTicker.High, dataTicker.Low, periodChop,avgTrueReturn)
    listChop = CP

    smi_call = ''
    rsi_call = ''
    chop_call = ''

    rsiCallOB = 'OVERBOUGHT'
    rsiCallOS = 'OVERSOLD'
    rsiCallNeu = 'NEUTRAL'

    callBuy = 'BUY'
    callSell = 'SELL'
    callExit = 'EXIT'

    chopCallTrend = 'TREND'
    chopCallTrendWk = 'WEAK TREND'
    chopCallConsolidation = 'CONSOLIDATION'
    chopCallConsolidationWk = 'WEAK CONSOLIDATION'

    callErr = 'ERROR'

    finalCall = ''

    ctrSignal = 0
    for day in listMaster:
        day.append(listRSI[ctrSignal])
        day.append(listSMA1[ctrSignal])
        day.append(listSMA2[ctrSignal])
        day.append((avgTrueReturn[ctrSignal]))
        day.append((CP[ctrSignal]))

        # add Calls based on RSI, SMA, Choppiness
        # RSI Call
        if listRSI[ctrSignal] == 0:
            rsi_call = callErr
        elif listRSI[ctrSignal] <= 20:
            rsi_call = rsiCallOS
        elif listRSI[ctrSignal] >= 80:
            rsi_call = rsiCallOB
        else:
            rsi_call = rsiCallNeu
        day.append(rsi_call)


        # SMA Call
        if listSMA1[ctrSignal] == 0 or listSMA2[ctrSignal] ==0:
            sma_call = callErr
        elif listSMA1[ctrSignal] < listSMA2[ctrSignal]:
            sma_call = callSell
        elif listSMA1[ctrSignal] >= listSMA2[ctrSignal]:
            sma_call = callBuy
        day.append(sma_call)

        # Choppiness Call
        if listChop[ctrSignal] == 0:
            chop_call = callErr
        elif listChop[ctrSignal] <= lowChop:
            chop_call = chopCallTrend
        elif listChop[ctrSignal] <= midChop:
            chop_call = chopCallTrendWk
        elif listChop[ctrSignal] <= highChop:
            chop_call = chopCallConsolidationWk
        elif listChop[ctrSignal] >= highChop:
            chop_call = chopCallConsolidation
                   
        day.append(chop_call)

        # Final Call
        
        if rsi_call == callErr or sma_call == callErr or chop_call == callErr:
            finalCall = callErr
        elif sma_call == callBuy:
            if (chop_call == chopCallTrend ) and (rsi_call != rsiCallOB ):
                finalCall = callBuy
            elif (chop_call == chopCallConsolidation or chop_call == chopCallConsolidationWk):
                finalCall = callExit
        elif sma_call == callSell:
            if (chop_call == chopCallTrend) and (rsi_call != rsiCallOS ):
                finalCall = callSell
            elif (chop_call == chopCallConsolidation or chop_call == chopCallConsolidationWk):
                finalCall = callExit
        else:
            finalCall = ''

        day.append(finalCall)
        
        # increment counter
        ctrSignal += 1
    print(listMaster)




    with open(baseLocation+outputFileName,fileMode) as fileData:
        fileData.write('Date,High,Low,Open,Close,Volume,AdjClose,RSI,SMA1,SMA2,ATR,Chop,RSICall,SMACall,ChopCall,FinalCall')
        fileData.write('\n')
        for list in listMaster:
            for col in list:
                fileData.write(str(col))
                fileData.write(',')
            fileData.write('\n')
    fileData.close()
    # get signals based on OHLCV, RSI, SMA(s), ATR, Choppiness
    # listMaster indices: 0-Date, 1-High, 2-Low, 3-Open, 4-Close, 5-Volume, 6-Adj Close, 7-RSI, 8-SMA1, 9-SMA2, 10-ATR, 11-Choppiness Index,/
    # 12-RSI Call, 13-SMA Call, 14-Choppiness Call, 15-Final Call
    findSignal(listMaster)

    plotCandleStick(listCandlestickMaster, listDates, listRSI, listChop, listSMA1, listSMA2, periodChop, periodSMA1, periodSMA2, periodRSI,  tickerSymbol, baseLocation+outputChartName)


# note execution end time
end_time = datetime.datetime.now()
logFile.close()
