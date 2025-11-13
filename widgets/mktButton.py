from PyQt5.QtWidgets import (QWidget, QToolButton, QVBoxLayout)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (Qt, pyqtSignal)

class MktButton(QWidget):

    clicked = pyqtSignal(bool)

    def __init__(self, icon=QIcon(''),
                 toolTip = '',
                 statusToolTip='',
                 width=25,
                 height=25):
        super().__init__()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(1,1,1,1)
        button = QToolButton()
        button.setFixedWidth(width)
        button.setFixedHeight(height)
        button.setCursor(Qt.PointingHandCursor)
        button.setToolTip(toolTip)
        button.setStatusTip(statusToolTip)
        button.setIcon(icon)
        vbox.addWidget(button)
        button.clicked[bool].connect(self.clicked[bool])
        self.clicked.connect(self.__mktButtonClickedSignal)
        self.setLayout(vbox)

    def __mktButtonClickedSignal(self):
        self.clicked()