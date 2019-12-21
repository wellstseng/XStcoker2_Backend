import define
import global_func
import pprint
from downloader.daily_price import DailyPriceFetcher
dailyPriceFetcher = DailyPriceFetcher()

#dailyPriceFetcher.load_range("twse", define.Define.TWSE_DAILY_PRICE_URL_FMT, define.Define.TWSE_DAILY_PRICE_HEADERS)
#dailyPriceFetcher.load_range("tpex", define.Define.TPEX_DAILY_PRICE_URL_FMT, define.Define.TPEX_DAILY_PRICE_HEADERS)

from importer.daily_price_importer import DailyPriceImporter
dailyPriceImporter = DailyPriceImporter()
dailyPriceImporter.import_to_mongo("twse", '2017/09/07', '2004/02/10')


# from datetime import timedelta, date, datetime
# start_date = date(2019, 12,21)
# end_date = date(2019, 8,15)
# date_batch = []
# temp_end = None
# temp_start = start_date
# while (temp_end != end_date):
#     temp_end = temp_start - timedelta(days=30)
#     if temp_end < end_date:
#         temp_end = end_date
#     date_batch.append({'start':temp_start, 'end':temp_end})
    
#     temp_start = temp_end
# pprint.pprint(date_batch)