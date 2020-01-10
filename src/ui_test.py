
# 导入必要的模块
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtCore, QtWidgets,QtGui
import matplotlib.pyplot as plt
import sys
from PyQt5.uic import loadUi
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
from datetime import timedelta, date, datetime

#talib
import talib
class My_Main_window(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super(My_Main_window,self).__init__(parent)
        # 重新调整大小
        self.resize(800, 659)
        # 添加菜单中的按钮
        self.menu = QtWidgets.QMenu("绘图")
        self.menu_action = QtWidgets.QAction("绘制",self.menu)
        self.menu.addAction(self.menu_action)
        self.menuBar().addMenu(self.menu)
        # 添加事件
        self.menu_action.triggered.connect(self.plot_)
        self.setCentralWidget(QtWidgets.QWidget())

    # 绘图方法
    def plot_(self):
        # 清屏
        plt.cla()
        # 获取绘图并绘制
        fig = plt.figure()
        ax =fig.add_axes([0.1,0.1,0.8,0.8])
        ax.set_xlim([-1,6])
        ax.set_ylim([-1,6])
        ax.plot([0,1,2,3,4,5],'o--')
        cavans = FigureCanvas(fig)
        # 将绘制好的图像设置为中心 Widget
        self.setCentralWidget(cavans)
def plot():
        plt.cla()
        fig = plt.figure()
        ax =fig.add_axes([0.1,0.1,0.8,0.8])
        ax.set_xlim([-1,6])
        ax.set_ylim([-1,6])
        ax.plot([0,1,2,3,4,5],'o--')
        return FigureCanvas(fig)

def plot2():
    mongoMgr = MongoManager("mongodb://stock:stock@192.168.1.27:27017/stock")
    result = mongoMgr.find_one('stock', 'Stock_3665', {'date':'2019'})
    df = pd.DataFrame.from_dict(result['items'], orient='index')
    df.sort_index(inplace=True)
    # pprint(df)
    fig = plt.figure(figsize=(800,600))

    part = df.iloc[-60::]

    ax = fig.add_subplot(1, 1, 1)
    ax.set_xticks(range(0, len(part.index.values)))

    xlabels = []
    for d in part.index.values:
        v = str(d[4:6])            
        xlabels.append(v) if v not in xlabels else xlabels.append('')
    if len(xlabels) > 0:
        fd = part.index.values[0]
        xlabels[0] = datetime.strptime(fd, '%Y%m%d').strftime('%Y/%m/%d') 
        
    ax.set_xticklabels(xlabels)
    ax.tick_params(axis='x', which='major', width=1)
    mpf.candlestick2_ochl(ax, part['open'], part['close'], part['high'],
    part['low'], width=1, colorup='r', colordown='g', alpha=0.75); 
    return FigureCanvas(fig)

from views.MainWindow import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow

class MainWindowController():
    view = None

    def __init__(self, view):
        self.view = view
        


class MainWindowView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.view = Ui_MainWindow()
        self.view.setupUi(self)

        self.view.figureLayout.addWidget(plot2(), 0, 0)

class MainApp(QApplication):
    def __init__(self, sys_argv):
        super(MainApp, self).__init__(sys_argv)
        
        self.mainView = MainWindowView()
        self.mainCtrl = MainWindowController(self.mainView)
        self.mainView.show()

if __name__ == '__main__':
    # app = QtWidgets.QApplication(sys.argv)
    # main_window = My_Main_window()
    # main_window.show()
    # app.exec()
    app = MainApp(sys.argv)    
    sys.exit(app.exec_())
