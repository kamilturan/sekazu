import pandas as pd
from PyQt5.QtWidgets import (QWidget, QToolButton, QVBoxLayout, QLabel, QTreeView, QFrame, QFileDialog, QHeaderView)
from PyQt5.QtGui import (QIcon, QStandardItemModel, QStandardItem)
from PyQt5.QtCore import (Qt, pyqtSignal, QModelIndex)

class MktTable(QWidget):

    clicked = pyqtSignal(QModelIndex )

    def __init__(self, headers=[]):
        super().__init__()
        self.__headers = headers
        self.__table = QTreeView()
        self.__table.clicked[QModelIndex].connect(self.clicked[QModelIndex])
        self.clicked.connect(self.__mktTableClickedSignal)
        vbox = QVBoxLayout()
        vbox.addWidget(self.__table)
        self.__prepared()
        vbox.setContentsMargins(1,1,1,1)
        self.setLayout(vbox)

    def getHeaders(self):
        return self.__headers

    def __mktTableClickedSignal(self):
        self.clicked()

    def __prepared(self):
        self.__model = QStandardItemModel(0, len(self.__headers))
        for index, i in enumerate(self.__headers):
            self.__model.setHeaderData(index, Qt.Horizontal, i)
        self.__table.setModel(self.__model)

    def rowCount(self):
        return self.__model.rowCount()

    def changeHeaders(self, headers):
        self.__headers = headers
        #for index, i in enumerate(self.__headers):
        #    self.__model.setHeaderData(index, Qt.Horizontal, i)
        self.__prepared()

    def addRow(self, data=[]):
        n = self.__model.rowCount()
        if n != 0:
            ids = []
            for i in range(self.__model.rowCount()):
                t1 = self.__model.data(self.__model.index(i, 0), Qt.DisplayRole)
                ids.append(int(t1))
            id = max(ids) + 1
        else:
            id = 1
        data.insert(0, str(id))
        for index, i in enumerate(data):
            item = QStandardItem(str(i))
            self.__model.setItem(n, index, item)
        return id

    def editRow(self, data=[]):
        index = self.__table.selectedIndexes()
        if len(index) != 0:
            for indexi, i in enumerate(data):
                item = QStandardItem(str(i))
                self.__model.setItem(index[0].row(), indexi, item)
            return 1
        else:
            return 0

    def editRowWithIndex(self, data=[], index:int=0):
        for indexi, i in enumerate(data):
            item = QStandardItem(str(i))
            self.__model.setItem(index, indexi, item)

    def reNumbered(self):
        n = self.__model.rowCount()
        for i in range(n):
            item = QStandardItem(str(i+1))
            self.__model.setItem(i, 0, item)

    def delRow(self):
        indices = self.__table.selectionModel().selectedRows()
        for index in sorted(indices):
            self.__model.removeRow(index.row())

    def removeAllItems(self):
        self.__model.clear()
        self.__model = QStandardItemModel(0, len(self.__headers))
        for index, i in enumerate(self.__headers):
            self.__model.setHeaderData(index, Qt.Horizontal, i)
        self.__table.setModel(self.__model)

    def saveList(self, title='', extention='', explain='', directory=''):
        dialog = QFileDialog()
        dialog.setDefaultSuffix(extention)
        dialog.setAcceptMode(QFileDialog.AcceptSave)
        dialog.setNameFilters(['{}(*.{})'.format(explain, extention)])
        dialog.setDirectory(directory)
        if dialog.exec_() == QFileDialog.Accepted:
            fname = dialog.selectedFiles()[0]
            data = []
            for i in range(self.__model.rowCount()):
                temp = []
                for j in range(self.__model.columnCount()):
                    temp.append(self.__model.data(self.__model.index(i, j), Qt.DisplayRole))
                data.append(temp)
            df = pd.DataFrame(data, columns=self.__headers)
            df.to_csv(fname, index=False)

    def saveListWhitOutSaveDialog(self, fname=''):
        data = []
        for i in range(self.__model.rowCount()):
            temp = []
            for j in range(self.__model.columnCount()):
                temp.append(self.__model.data(self.__model.index(i, j), Qt.DisplayRole))
            data.append(temp)
        df = pd.DataFrame(data, columns=self.__headers)
        df.to_csv(fname, index=False)

    def openList(self,title='', extention='', explain='', directory=''):
        dialog = QFileDialog()
        dialog.setDefaultSuffix(extention)
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilters(['{}(*.{})'.format(explain, extention)])
        dialog.setDirectory(directory)
        if dialog.exec_() == QFileDialog.Accepted:
            fname = dialog.selectedFiles()[0]
            temp = pd.read_csv(fname)
            self.__headers = temp.columns.values
            self.__model = QStandardItemModel(0, len(self.__headers))
            self.__table.setModel(self.__model)
            for index, i in enumerate(self.__headers):
                self.__model.setHeaderData(index, Qt.Horizontal, i)
            for i in temp.values:
                n = self.__model.rowCount()
                self.__model.insertRow(n)
                for index, j in enumerate(i):
                    item = QStandardItem(str(j))
                    self.__model.setItem(n, index, item)

    def openListWhitOutDialog(self, fname=''):
        temp = pd.read_csv(fname)
        self.__headers = temp.columns.values
        self.__model = QStandardItemModel(0, len(self.__headers))
        self.__table.setModel(self.__model)
        for index, i in enumerate(self.__headers):
            self.__model.setHeaderData(index, Qt.Horizontal, i)
        for i in temp.values:
            n = self.__model.rowCount()
            self.__model.insertRow(n)
            for index, j in enumerate(i):
                item = QStandardItem(str(j))
                self.__model.setItem(n, index, item)

    def getRowDataFromIndex(self, index):
        temp = []
        for i in range(len(self.__headers)):
            temp.append(self.__model.data(self.__model.index(index, i), Qt.DisplayRole))
        return temp

    def getSelectedRowData(self):
        index = self.__table.currentIndex()
        if index != None:
            temp = []
            for i in range(len(self.__headers)):
                temp.append(self.__model.data(self.__model.index(index.row(), i), Qt.DisplayRole))
            return temp