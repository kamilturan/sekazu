from PyQt5.QtWidgets import (QWidget, QToolButton, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
                             QColorDialog)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (Qt, pyqtSignal)

class MktColor(QWidget):

    def __init__(self, icon=QIcon(''),
                 mktDefaultBackgrundColor = '',
                 mktDefaultForegrundColor = '',
                 width=25,
                 height=25):
        super().__init__()
        hboxBColor = QHBoxLayout()
        hboxBColor.setContentsMargins(1,1,1,1)
        hboxFColor = QHBoxLayout()
        hboxFColor.setContentsMargins(1,1,1,1)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0,0,0,0)
        self.__bcolor = QLineEdit()
        self.__bcolor.setEnabled(False)
        self.__bcolor.setText(mktDefaultBackgrundColor)
        self.__fcolor = QLineEdit()
        self.__fcolor.setEnabled(False)
        self.__fcolor.setText(mktDefaultForegrundColor)
        bcolorButton = QToolButton()
        bcolorButton.setIcon(icon)
        bcolorButton.setCursor(Qt.PointingHandCursor)
        bcolorButton.clicked.connect(self.__bcolorClicked)
        hboxBColor.addWidget(self.__bcolor)
        hboxBColor.addWidget(bcolorButton)
        fcolorButton = QToolButton()
        fcolorButton.setIcon(icon)
        fcolorButton.setCursor(Qt.PointingHandCursor)
        fcolorButton.clicked.connect(self.__fcolorClicked)
        hboxFColor.addWidget(self.__fcolor)
        hboxFColor.addWidget(fcolorButton)
        self.__examples = QLabel('+ Örnek +')
        self.__examples.setAlignment(Qt.AlignCenter)
        vbox.addLayout(hboxBColor)
        vbox.addLayout(hboxFColor)
        mainhbox = QHBoxLayout()
        mainhbox.addLayout(vbox)
        mainhbox.setContentsMargins(1,1,1,1)
        mainhbox.addWidget(self.__examples)
        mainhbox.setContentsMargins(0,0,0,0)
        self.__applyColors()
        self.setLayout(mainhbox)

    def __applyColors(self):
        self.__examples.setStyleSheet(
            "QLabel { background-color : " + self.__bcolor.text() + "; color : " + self.__fcolor.text() + "; }")

    def __bcolorClicked(self):
        color = QColorDialog.getColor()
        if color:
            self.__bcolor.setText(color.name())
            self.__applyColors()

    def __fcolorClicked(self):
        color = QColorDialog.getColor()
        if color:
            self.__fcolor.setText(color.name())
            self.__applyColors()

    def backgroundColor(self):
        return self.__bcolor.text()

    def foregroundColor(self):
        return self.__fcolor.text()

    def setBackgroundColor(self, color):
        self.__bcolor.setText(color)
        self.__applyColors()

    def setForegoundColor(self, color):
        self.__fcolor.setText(color)
        self.__applyColors()


