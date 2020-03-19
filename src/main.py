'''
import define
import global_func
import pprint
from downloader.stocklist import StockListHolder
from downloader.daily_price import DailyPriceFetcher
from importer.daily_price_importer import DailyPriceImporter
'''
# StockListHolder.get_list(define.MarketTypeId.TWSE)
# StockListHolder.get_list(define.MarketTypeId.TPEX)  
'''
dailyPriceFetcher = DailyPriceFetcher()
#dailyPriceFetcher.load_range("twse", define.Define.TWSE_DAILY_PRICE_URL_FMT, define.Define.TWSE_DAILY_PRICE_HEADERS)
#dailyPriceFetcher.load_range("tpex", define.Define.TPEX_DAILY_PRICE_URL_FMT, define.Define.TPEX_DAILY_PRICE_HEADERS)

dailyPriceImporter = DailyPriceImporter()
dailyPriceImporter.import_to_mongo("twse")
dailyPriceImporter.import_to_mongo("tpex")
'''

'''
date import 
'''
# dailyPriceImporter = DailyPriceImporter()
# dailyPriceImporter.import_to_mongo("twse", '2019/12/23', '2019/12/22')
# dailyPriceImporter.import_to_mongo("tpex", '2019/12/23', '2019/12/22')

'''
Google Sheet Statement of Account
'''
from gs.GoogleSheetHandler import GoogleSheetHandler
import pandas as pd
import collections, os
StagementOfAccountSheetId = "1e68G7v-G-Dv9r9J0q1uhoasLtuZvVUQVq_ziy-lEX_c" #對帳單的spread sheet id
ProsAndLossSheetId = "1NPa9fsgRSIT1I6Fs33OjcUsGhKGw6hUtgS-cmavqWnY"
sheetHandler = GoogleSheetHandler(StagementOfAccountSheetId)

sheetNames = sheetHandler.get_sheet_names()
stockDataframe = {}
sheetNames.sort()

for name in sheetNames:
    if '#' not in name:
        continue
    print("sheet name :{}".format(name))
    success, df = sheetHandler.get_sheet_as_dataframe(name)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.dropna(subset=['股票代碼'], inplace=True)
    df = df.astype({'股票代碼':str, '成交股數':int, '成交價金':int})    
    df['股票代碼'] = df['股票代碼'].str.replace(r"(.*)\.0",r"\1", regex=True)
    df["成交日期"] = pd.to_datetime(df["成交日期"],infer_datetime_format=True, format="%Y/%m/%d")
    df = df.sort_values(by =['成交日期','委託書號'] )    

    for id, row in df.iterrows():
        stockId = row['股票代碼']
        if stockId not in stockDataframe:
            newDf = pd.DataFrame(columns=df.columns)
            stockDataframe[stockId] = newDf
        stockDataframe[stockId] = stockDataframe[stockId].append(row, ignore_index=True)

def _getQueueData(result,mainQ,  now, total):
    if now >= total or mainQ == None or len(mainQ) == 0:
        return result
    else:
        q = mainQ[0]
        
        transaction = q["成交股數"]
        if transaction > total:     
            cnt = total
        else:
            cnt = transaction
        n = now + cnt
        cp = q.copy()
        
        avg = q["淨付金額"] / q["成交股數"]
        cp["淨付金額"] = avg * cnt
        cp["成交股數"] = cnt
        result.append(cp)
        q["成交股數"] = transaction - cnt
        q["淨付金額"] -= cp["淨付金額"]
        if (q["成交股數"] == 0) :
            del mainQ[0]
        return _getQueueData(result, mainQ, n, total)

def _calcCost(records):  
    total = 0  
    for i in records:
        total += abs(i["淨付金額"])

    return int(total)



def writeToExcel(dfs):
    sortDict = collections.OrderedDict(sorted(dfs.items()))
    filePath = 'D:/歷史損益.xlsx'
    try:
        if os.path.isfile(filePath):
            os.remove(filePath)
    
        with pd.ExcelWriter(filePath, engine='xlsxwriter') as writer:  # doctest: +SKIP
            for stkId, df in sortDict.items():
                print("write stock data:{}".format(stkId))                
                df.to_excel(writer, sheet_name=stkId) 
                book = writer.book
                worksheet = writer.sheets[stkId]
                worksheet.set_column(1, 1, 20)
            writer.save()
    except IOError:
        print ("Could not open file! Please close Excel!")

for stkId, df in stockDataframe.items():
    # if '1513' not in stkId:
    #     continue
   
    df["損益"] = pd.Series(index=df.index, dtype=int)
    df["買進總成本"] = pd.Series(0, index=df.index, dtype=int)
   
    buy = []
    for idx, row in df.iterrows():
        if row["交易別"] == "現股":
            if row["買賣"] == "買":
                buy.append(row)
            elif row["買賣"] == "賣":
                
                transactionAmount = row["成交股數"]
                q = []
                buyRecord = _getQueueData(q, buy, 0, transactionAmount)
                
                cost = _calcCost(buyRecord)
                if cost > 0:
                    profAndLoss = row["淨收金額"] - cost
                    df.at[idx, "損益"] = profAndLoss
                    df.at[idx, "買進總成本"] =cost
        

    #合併資料
    #df = df.loc[(df['淨收金額'] >0)] 
    df = df.groupby(by=["成交日期", "股票代碼", "交易別", "買賣"], as_index=False).agg(
        {'成交股數':sum, 
        "成交價金":sum,
        "淨收金額":sum,
        "買進總成本":sum,  
        "損益":sum,               
        })
    df["分攤成本"] = pd.Series([x["成交價金"]/x["成交股數"] for _, x in df.iterrows()], index=df.index, dtype=float)    
    df["報酬率%"] = pd.Series(["{}%".format(round(x["損益"]/x["買進總成本"]*100, 2)) if x["買進總成本"] > 0 else "" for _, x in df.iterrows() ], index=df.index, dtype=str)
    df['成交日期'] = df['成交日期'].dt.date
    stockDataframe[stkId] = df
    
    
    
    
writeToExcel(stockDataframe)


