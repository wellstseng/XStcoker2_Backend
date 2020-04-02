#%%
# # basic
# import numpy as np
# import pandas as pd

# #get data
# from mongo.mongo import MongoManager
# import pandas as pd

# visual
# import matplotlib.pyplot as plt
# import mpl_finance as mpf
# import seaborn as sns
# %matplotlib inline
#time
# import datetime as datetime

# #talib
# import talib

# from pprint import pprint
'''
mongoMgr = MongoManager("mongodb://stock:stock@192.168.1.27:27017/stock")
result = mongoMgr.find_one('stock', 'Stock_3665', {'date':'2019'})
df = pd.DataFrame.from_dict(result['items'], orient='index')
df.sort_index(inplace=True)
# pprint(df)
fig = plt.figure(figsize=(24, 8))

ax = fig.add_subplot(1, 1, 1)
ax.set_xticks(range(0, len(df.index), 10))
ax.set_xticklabels(df.index[::10])
mpf.candlestick2_ochl(ax, df['open'], df['close'], df['high'],
                      df['low'], width=0.6, colorup='r', colordown='g', alpha=0.75); 
                      '''
# converter
import re
import numpy as np
import pandas as pd
from os import listdir
from os.path import isfile, join
dir_root = "D:/data"
onlyfiles = [join(dir_root,f) for f in listdir(dir_root) if isfile(join(dir_root, f))]

print(onlyfiles)
dfs = []
for ff in onlyfiles:
    df = pd.read_csv(ff, index_col=None, header=0 , encoding="big5")
    df.columns = [ x.replace('\t', '') for x in df.columns ]
    
    df['成交日期'].replace(' ', np.nan, inplace=True)
    df.dropna(subset=['成交日期'], inplace=True) 

    df['成交日期'] = df['成交日期'].str.replace("\t", "")
    df["成交日期"] = pd.to_datetime(df["成交日期"],infer_datetime_format=True, format="%Y/%m/%d")
    df['交易類別'] = df['交易類別'].str.replace("\t", "")
    df['股票名稱'] = df['股票名稱'].str.replace("\t", "")
    dfs.append(df)
total = pd.concat(dfs, axis=0, ignore_index=True)


new = pd.DataFrame(columns = ['成交日期','股票代碼','股票名稱','交易別','買賣','成交股數','成交價',
'成交價金','手續費','交易稅','淨付金額','淨收金額',
'融券擔保款','融資金額','融券保證金','債息','利息','融券手續費','委託書號'])

for index, row in total.iterrows():
    m = re.match(r"(.*)\((.*)\)", row['股票名稱'])
    stockName = m.group(1)
    stockId = m.group(2)
    tradeType = row['交易類別'][:2]
    if tradeType == "當沖":
        tradeType = "現沖"

    values = [
        row['成交日期'],
        stockId,
        stockName,
        tradeType,
        row['交易類別'][2],
        row['成交股數'],
        row['成交單價'],
        row['成交價金'],
        row['手續費'],
        row['交易稅'],
        row['淨收付金額'] if int(row['淨收付金額']) <= 0 else "0",
        row['淨收付金額'] if int(row['淨收付金額']) >= 0 else "0",
        row['融資金/擔保金'] if tradeType == "融券" else "0",
        row['融資金/擔保金'] if tradeType == "融資" else "0",
        row['自備款/保證金'] if tradeType == "融券" else "0",
        "0",
        row['利息'],
        row['融券費'],
        "-"
    ]
    s = pd.Series(values, index=new.columns )
    new = new.append(s, ignore_index=True)
new = new.sort_values(by =['成交日期'] )  
new.to_csv("D:/merge.csv")
print(new)