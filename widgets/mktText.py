import pandas as pd
from PyQt5.QtWidgets import (QWidget, QTextEdit, QVBoxLayout, QLabel, QTreeView, QFrame, QFileDialog, QHeaderView)
from PyQt5.QtGui import (QIcon, QPixmap)
from PyQt5.QtCore import (Qt)

class MktText(QWidget):

    def __init__(self):
        super().__init__()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(1, 1, 1, 1)
        self.__result = QTextEdit()
        self.__result.clear()
        vbox.addWidget(self.__result)
        self.setLayout(vbox)
        self.cursor = self.__result.textCursor()


    def addTitle(self, title):
        html = '<p><h3 style="color:blue; text-align:center;">{}</h3></p>'.format(title)
        self.cursor.insertHtml(html)

    def addDataFrame(self, df, title=''):
        html = '<p><h4 style="color:black; text-align:center;">{}</h3></p>'.format(title)
        self.cursor.insertHtml(html)
        self.cursor.insertHtml(df.to_html())

    def addImage(self, path):
        icon = QPixmap(path)
        image = icon.toImage()
        self.cursor.insertImage(image)

