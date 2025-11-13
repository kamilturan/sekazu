from PyQt5.QtWidgets import (QWidget, QToolButton, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (Qt, pyqtSignal)

class MktSelectList(QWidget):

    def __init__(self, items=[], icons=[]):
        super().__init__()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.__comboBox = QComboBox()
        self.__listView = QListWidget()
        self.__comboBox.addItems(items)
        vbox.addWidget(self.__comboBox)
        hbox.addWidget(self.__listView)
        vbox1 = QVBoxLayout()
        buttonAdd = QToolButton()
        buttonAdd.setIcon(icons[0])
        buttonAdd.clicked.connect(self.__buttonAddClicked)
        buttonDel = QToolButton()
        buttonDel.setIcon(icons[1])
        buttonDel.clicked.connect(self.__buttonDelClicked)
        buttonClear = QToolButton()
        buttonClear.setIcon(icons[2])
        buttonClear.clicked.connect(self.__buttonClearClicked)
        vbox1.addWidget(buttonAdd)
        vbox1.addWidget(buttonDel)
        vbox1.addWidget(buttonClear)
        vbox1.addStretch(1)
        hbox.addLayout(vbox1)
        vbox.addLayout(hbox)
        vbox.setContentsMargins(1,1,1,1)
        self.setLayout(vbox)

    def __buttonAddClicked(self):
        self.__listView.addItem(self.__comboBox.currentText())

    def __buttonDelClicked(self):
        listItems = self.__listView.selectedItems()
        if listItems:
            for item in listItems:
                self.__listView.takeItem(self.__listView.row(item))

    def __buttonClearClicked(self):
        self.__listView.clear()

    def getListItems(self):
        data = []
        for i in range(self.__listView.count()):
            data.append(self.__listView.item(i).text())
        return data

    def setListItems(self, items):
        self.__listView.clear()
        for i in items:
            self.__listView.addItem(i)

    def changeItems(self, newItems):
        self.__comboBox.clear()
        self.__comboBox.addItems(newItems)



