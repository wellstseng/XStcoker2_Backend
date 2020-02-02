#%%
# -*- encoding: utf8-*-
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from datetime import datetime, timedelta
import gspread_dataframe as gd

class GoogleSheetHandler:
    AUTH_PATH = '/auth/auth.json'
    __client = None
    __spread = None
    __sheetNames = []
    def __init__(self, spread_id):
        self.open(spread_id)        

    def open(self, spread_id):
        scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
           
        root_path = os.path.abspath(os.path.dirname(__file__)).replace('\\','/')
        auth_path = root_path + self.AUTH_PATH
        creds = ServiceAccountCredentials.from_json_keyfile_name(auth_path, scope)
        self.__client = gspread.authorize(creds)
        self.__spread = self.__client.open_by_key(spread_id)
        
    def get_sheet(self, sheet_name):
        if self.__spread == None:
            print("Client didn't init yet")
            return None
        if sheet_name not in self.get_sheet_names():
            return None
        return self.__spread.worksheet(sheet_name)

    def get_sheet_names(self):
        if self.__spread == None:
            print("Client didn't init yet")
            return
        if not self.__sheetNames:
            sheets = self.__spread.worksheets()
            self.__sheetNames = [f.title for f in sheets]
        return self.__sheetNames
        

    def get_sheet_as_dataframe(self, sheet_name):
        worksheet = self.get_sheet(sheet_name)
        if not worksheet:
            return False, None
        df = gd.get_as_dataframe(worksheet)
        return True, df
    
    def set_sheet_as_dataframe(self, sheetName, df):
        sheet = self.get_sheet(sheetName)
        if not sheet:
            sheet = self.__spread.add_worksheet(title=sheetName, cols=len(df.columns), rows=len(df.index))  
            self.__sheetNames.append(sheetName)          
        gd.set_with_dataframe(sheet, df)

    def get_spread(self):
        return self.__spread

if __name__ == "__main__":
    handler = GoogleSheetHandler('1emt4I1yb_rOksiKuj46PxxCekiRVumytIBYpmfNNIFU')
    l = handler.get_sheet_names()

   
    pprint.pprint(l)