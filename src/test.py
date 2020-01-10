#%%
# basic
import numpy as np
import pandas as pd

#get data
from mongo.mongo import MongoManager
import pandas as pd

# visual
import matplotlib.pyplot as plt
import mpl_finance as mpf
import seaborn as sns
# %matplotlib inline
#time
import datetime as datetime

#talib
import talib

from pprint import pprint

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