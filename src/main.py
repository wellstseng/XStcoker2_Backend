import define
import global_func
import pprint
from downloader.stocklist import StockListHolder
from downloader.daily_price import DailyPriceFetcher
from importer.daily_price_importer import DailyPriceImporter

# StockListHolder.get_list(define.MarketTypeId.TWSE)
# StockListHolder.get_list(define.MarketTypeId.TPEX)  

dailyPriceFetcher = DailyPriceFetcher()
#dailyPriceFetcher.load_range("twse", define.Define.TWSE_DAILY_PRICE_URL_FMT, define.Define.TWSE_DAILY_PRICE_HEADERS)
#dailyPriceFetcher.load_range("tpex", define.Define.TPEX_DAILY_PRICE_URL_FMT, define.Define.TPEX_DAILY_PRICE_HEADERS)

dailyPriceImporter = DailyPriceImporter()
dailyPriceImporter.import_to_mongo("twse")
dailyPriceImporter.import_to_mongo("tpex")


'''
date import 
'''
# dailyPriceImporter = DailyPriceImporter()
# dailyPriceImporter.import_to_mongo("twse", '2019/12/23', '2019/12/22')
# dailyPriceImporter.import_to_mongo("tpex", '2019/12/23', '2019/12/22')