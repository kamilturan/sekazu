import sys
import pandas as pd
import math
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QComboBox,
                             QFrame, QLineEdit, QTextEdit, QAction, QFormLayout, QFileDialog)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.Qt import (Qt, QSize)
from widgets.mktTable import MktTable
from widgets.mktLEditButton import MktLEditButton


class CalculateManager(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hesaplama yönetim formu')
        self.setWindowIcon(QIcon('./icons/calc.png'))
        self.statusBar().showMessage('Kullanıma hazır.')
        self.setFont(QFont('Calibri', 8))
        self.__vbox = QVBoxLayout()
        self.__vbox.setContentsMargins(2, 2, 2, 2)
        frame = QFrame()
        frame.setLayout(self.__vbox)
        self.__menu()
        self.__form()
        self.__table = MktTable(headers=[])
        self.__table.clicked = self.tableClicked
        self.__vbox.addWidget(self.__table)
        self.setCentralWidget(frame)
        self.__dfSaf = None
        self.__dfSbf = None
        self.__dfScf = None

    def __menu(self):
        toolbar = self.addToolBar('main')
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)
        saveAction = QAction(QIcon('./icons/save.png'), 'Hesaplanmıoş nitelikler dosyası olarak kaydeder', self)
        saveAction.setStatusTip('Listeyi hesaplanmış nitelikler olarak kaydetmek için kullanabilirsiniz.')
        saveAction.triggered.connect(self.saveActionClicked)
        toolbar.addAction(saveAction)

    def __form(self):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        formlayout = QFormLayout()
        formlayout.setLabelAlignment(Qt.AlignRight)
        formlayout.setSpacing(2)
        self.__source = MktLEditButton(QIcon('./icons/open.png'))
        self.__source.clicked = self.sourceClicked
        formlayout.addRow(QLabel('Kaynak:'), self.__source)
        frame.setLayout(formlayout)
        self.__vbox.addWidget(frame)

    def saveActionClicked(self):
        try:
            self.__table.saveList(title='Hesaplanmış nitelik olarak kaydet',
                                  extention='sca',
                                  explain='Hesaplanmış nitelik dosyası',
                                  directory='./thesis/')
            self.statusBar().showMessage('Liste Hesaplanmış nitelik dosyası olarak kaydedildi.')
        except:
            self.statusBar().showMessage('Kaydetme işlemi esnasında hata')

    def sourceClicked(self):
        dialog = QFileDialog()
        dialog.setDefaultSuffix('scf')
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilters(['Koordinat dosyaları (*.scf)'])
        dialog.setDirectory('./')
        try:
            if dialog.exec_() == QFileDialog.Accepted:
                fname = dialog.selectedFiles()[0]
                self.__source.setText(fname)
                self.__dfScf = pd.read_csv(fname)
                fname = self.__dfScf['Kaynak'].values[0]
                self.__dfSaf = pd.read_csv(fname)
                fname = self.__dfScf['Kaynak'].values[0]
                self.__dfSbf = pd.read_csv(fname)
                headers = ['No', 'Protokol', 'Ad', 'Yaş', 'Boy', 'Cinsiyet', 'Kaynak']
                labels = self.__dfSaf['Etiket'].values
                for i in labels:
                    headers.append(i)
                self.__table.changeHeaders(headers)
                self.__calculate()
                self.statusBar().showMessage('Tüm nitelikler hesaplanarak listeye aktarıldı. Kayıt içim hazır.')
        except:
            print(sys.exc_info())

    def tableClicked(self):
        pass

    def __convertToPoint(self, text):
        h1 = text.split(':')
        x = float(h1[0])
        y = float(h1[1])
        return (x, y)

    def __attr_length(self, point1, point2):
        point1 = self.__convertToPoint(point1)
        point2 = self.__convertToPoint(point2)
        uz = math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        return uz

    def __attr_angle(self, p0, p1, p2):
        p0 = self.__convertToPoint(p0)
        p1 = self.__convertToPoint(p1)
        p2 = self.__convertToPoint(p2)
        a = (p1[0] - p0[0]) ** 2 + (p1[1] - p0[1]) ** 2
        b = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
        c = (p2[0] - p0[0]) ** 2 + (p2[1] - p0[1]) ** 2
        payda = math.sqrt(4 * a * b)
        if payda !=  0:
            angle = math.acos((a + b - c) / payda) * 180 / math.pi
        else:
            angle = 0
        return angle

    def __attr_area(self, points):
        ps = []
        for i in points:
            ps.append(self.__convertToPoint(i))
        n = len(ps)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += ps[i][0] * ps[j][1]
            area -= ps[j][0] * ps[i][1]
        area = abs(area) / 2.0
        return area

    def __attr_circularArea(self, p0, p1):
        r = self.__attr_length(p0, p1)
        carea = math.pi * r ** 2
        return carea

    def __attr_circularPerimeter(self, p0, p1):
        r = self.__attr_length(p0, p1)
        cperimeter = 2 * math.pi * r
        return cperimeter

    def __calculate(self):
        data = []
        for i in list(self.__dfSaf.values):
            bookmarks = i[4].split('|')
            labels = []
            types = i[3]
            for k in bookmarks:
                if k != '':
                    labels.append(k[k.index(':') + 1:])
            coordinates = self.__dfScf[labels].values
            temp = []
            for index, coors in enumerate(coordinates):
                result = -1
                if types == 'Uzunluk':
                    result = self.__attr_length(coors[0], coors[1])
                if types == 'Açı':
                    result = self.__attr_angle(coors[0], coors[1], coors[2])
                if types == 'Alan':
                    result = self.__attr_area(coors)
                if types == 'Dairesel alan':
                    result = self.__attr_circularArea(coors[0], coors[1])
                if types == 'Dairesel çevre':
                    result = self.__attr_circularPerimeter(coors[0], coors[1])
                temp.append(result)
            data.append(temp)
        data = np.transpose(np.asarray(data)).tolist()
        demog = list(self.__dfScf[['Protokol', 'Ad', 'Yaş', 'Boy', 'Cinsiyet', 'Kaynak']].values)
        temp = []
        for indexi, i in enumerate(demog):
            temp1 = []
            for k in i:
                temp1.append(k)
            for j in data[indexi]:
                temp1.append("{0:0.5f}".format(j))
            temp.append(temp1)
        for i in temp:
            self.__table.addRow(i)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CalculateManager()
    ex.show()
    sys.exit(app.exec_())