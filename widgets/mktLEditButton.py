from PyQt5.QtWidgets import (QWidget, QToolButton, QVBoxLayout, QHBoxLayout, QLineEdit)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (Qt, pyqtSignal)

class MktLEditButton(QWidget):

    clicked = pyqtSignal(bool)

    def __init__(self, icon=QIcon(''),
                 toolTip = '',
                 statusToolTip='',
                 width=25,
                 height=25,
                 default='<Dosya seçiniz>'):
        super().__init__()
        hbox = QHBoxLayout()
        hbox.setContentsMargins(1,1,1,1)
        self.__lineEdit = QLineEdit()
        self.__lineEdit.setText(default)
        button = QToolButton()
        button.setIcon(icon)
        button.setToolTip(toolTip)
        button.setStatusTip(statusToolTip)
        button.setFixedWidth(width)
        button.setFixedHeight(height)
        button.clicked[bool].connect(self.clicked[bool])
        self.clicked.connect(self.__mktLineEditButtonClickedSignal)
        hbox.addWidget(self.__lineEdit)
        hbox.addWidget(button)
        self.setLayout(hbox)

    def __mktLineEditButtonClickedSignal(self):
        self.clicked()

    def setText(self, text: str):
        self.__lineEdit.setText(text)

    def text(self):
        return self.__lineEdit.text()