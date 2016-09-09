# -*- coding: utf-8 -*-
"""
Python Fundamental Analysis with Quandl

This script is based on a spreadsheet I found in a Stocks & Commodities article. 
The author of the sheet is Jacob Singer. I was able to replicate most of the 
formulas and calculations with the data available from Quandl.com. The database 
used it the Free US Stock Data.  

This queries one quote at a time in the console.

Licensed under GNU GPLv3. 

@author: Weston Hinton 
github:wbhinton
email:wbhinton@gmail.com
"""

import quandl as ql
import pandas as pd
import ystockquote
import datetime

"""This sets the Quandl API Key"""

ql.ApiConfig.api_key="YOUR API KEY"

"""Set stock symbol"""
tic=input('Please enter stock symbol:') 

"""Set current date and 1yr prior"""
now=datetime.date.today()
year=datetime.timedelta(365)
yearago=now-year
lastyear=yearago.strftime("%Y-%m-%d")

"""Collect the Data"""
CurrentPrice=float(ystockquote.get_price(tic))
LastYearQuote=ystockquote.get_historical_prices(tic,lastyear,lastyear)
LastYearPrice=float(LastYearQuote.get(lastyear).get('Close'))

"""YearAgoPrice="""
Receivables=pd.DataFrame(ql.get("SF0/%s_RECEIVABLES_MRY"%tic))
Inventory=pd.DataFrame(ql.get("SF0/%s_INVENTORY_MRY"%tic))
TotalCurrentAssets=pd.DataFrame(ql.get("SF0/%s_ASSETSC_MRY"%tic))
TotalCurrentLiabilities=pd.DataFrame(ql.get("SF0/%s_LIABILITIESC_MRY"%tic))
Debt=pd.DataFrame(ql.get("SF0/%s_DEBTUSD_MRY"%tic))
Equity=pd.DataFrame(ql.get("SF0/%s_EQUITYUSD_MRY"%tic))
GrossProfit=pd.DataFrame(ql.get("SF0/%s_GP_MRY"%tic))
DeclaredDividend=pd.DataFrame(ql.get("SF0/%s_DPS_MRY"%tic))
EPS=pd.DataFrame(ql.get("SF0/%s_EPS_MRY"%tic))
Revenue=pd.DataFrame(ql.get("SF0/%s_REVENUEUSD_MRY"%tic))
EBITDA=pd.DataFrame(ql.get("SF0/%s_EBITDAUSD_MRY"%tic))
EBT=pd.DataFrame(ql.get("SF0/%s_EBT_MRY"%tic))
IncomeTax=pd.DataFrame(ql.get("SF0/%s_TAXEXP_MRY"%tic))
DepAmmort=pd.DataFrame(ql.get("SF0/%s_DEPAMOR_MRY"%tic))
DilutedShares=pd.DataFrame(ql.get("SF0/%s_SHARESWADIL_MRY"%tic))
Cash=pd.DataFrame(ql.get("SF0/%s_CASHNEQUSD_MRY"%tic))
CostOfRevenue=(ql.get("SF0/%s_COR_MRY"%tic))
NetIncome=pd.DataFrame(ql.get("SF0/%s_NETINC_MRY"%tic))
CurrentRatio=pd.DataFrame(ql.get("SF0/%s_CURRENTRATIO_MRY"%tic))
DebtToEquity=pd.DataFrame(ql.get("SF0/%s_DE_MRY"%tic))

"""Calculations-- BuyRating is how we are rating the stock on a scale of 1-8"""
BuyRating=0

"""Profit Margin--- CNPM is Current Net Profit Margin"""
GrossProfitMargin=GrossProfit/Revenue+100
NetProfitMargin=NetIncome/Revenue*100
CNPM=NetProfitMargin.iat[0,0]
if CNPM<15:
    BuyRating=BuyRating-8
 
"""If CurrentEPS is greater than zero, then the acceptable
price for stock is given by:"""   
CurrentEPS=EPS.iat[0,0]
PreviousEPS=EPS.iat[1,0]
AcceptablePrice=0
if CurrentEPS>0 :
    AcceptablePrice=(CurrentEPS/PreviousEPS)*CurrentPrice
if AcceptablePrice>CurrentPrice:
    BuyRating=BuyRating+1
    
"""PE Ratio Comparison"""
CurrentPE=CurrentPrice/CurrentEPS
PreviousPE=LastYearPrice/PreviousEPS  
if CurrentEPS>0:
    BuyRating=BuyRating+int((CurrentPE/PreviousPE)*100)/100

"""Quick Ratio Calc"""
TCA=TotalCurrentAssets.iat[0,0]
Inv=Inventory.iat[0,0]
TCL=TotalCurrentLiabilities.iat[0,0]
QuickRatio=(TCA-Inv)/TCL
if QuickRatio>.7:
    BuyRating=BuyRating+1

"""Current Ratio Test"""
CurRatio=CurrentRatio.iat[0,0]
if CurRatio>1.5:
    BuyRating=BuyRating+1

"""Efficiency of Operation"""
CapitalEmployed=TCA-TCL-Receivables.iat[0,0]
OpEff=(EBT.iat[0,0]/CapitalEmployed)*100
if OpEff>15:
    BuyRating=BuyRating+1

"""Debt to Equity"""
if DebtToEquity.iat[0,0]<20:
    BuyRating=BuyRating+1
    
"""Debt to Capital"""
DC=TCL/CapitalEmployed
if DC<20:
    BuyRating=BuyRating+1

"""Cash to Share Price"""
CashToShare=Cash.iat[0,0]/CurrentPrice
if CashToShare<5:
    BuyRating=BuyRating+1    

"""Dividend Payout Ratio"""
DPR=(DeclaredDividend.iat[0,0]/CurrentEPS)*100
if DPR>40:
    BuyRating=BuyRating+1

"""Company Performance"""
ChangeInSales=(Revenue.iat[0,0]-Revenue.iat[1,0])/Revenue.iat[1,0]    
CoPerform=(ChangeInSales/((Inventory.iat[0,0]+Receivables.iat[0,0])-(Inventory.iat[1,0]+Receivables.iat[1,0])))/(Inventory.iat[1,0]+Receivables.iat[1,0])
if CoPerform>ChangeInSales:
    Performance="Underperform"
Performance="OK"

"""Print and Write Out Data"""
print("./n")    
print("Buy Rating: "+str(BuyRating)) 
if BuyRating<5:
    print("Not Interested")

elif 5<=BuyRating<6:
    print("Watch for Future Buy")

elif 6<=BuyRating<7:
    print("Buy with Available Cash")

elif 7<=BuyRating<8:
    print("Consider Buying on Margin")    

elif BuyRating>=8:
    print("BUY BUY BUY")

print("EBITDA: "+str(EBITDA.iat[0,0]))
print("Current PE: "+str(CurrentPE) )
print("Last Year's PE: "+str(PreviousPE))
print("Current Net Profit Margin: "+str(CNPM))
print("Acceptable Price: "+str(AcceptablePrice))
print("Current Price: "+str(CurrentPrice))
print("Quick Ratio: "+str(QuickRatio))
print("Current Ratio: "+str(CurRatio))
print("Company Performance: "+Performance)
    



