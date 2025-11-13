import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout,
                             QFrame, QLineEdit, QTextEdit, QAction, QFormLayout)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.Qt import (Qt, QSize)
from widgets.mktColor import MktColor
from widgets.mktTable import MktTable

class BookmarkManager(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Yerimi yönetim formu')
        self.setWindowIcon(QIcon('./icons/bookmark.png'))
        self.statusBar().showMessage('Kullanıma hazır.')
        self.setFont(QFont('Calibri', 8))
        self.__vbox = QVBoxLayout()
        self.__vbox.setContentsMargins(2,2,2,2)
        frame = QFrame()
        frame.setLayout(self.__vbox)
        self.__menu()
        self.__form()
        self.__table = MktTable(headers=['No','Ad','Etiket','Plan','Arkaplan','Yazı rengi','Açıklma'])
        self.__table.clicked = self.tableClicked
        self.__vbox.addWidget(self.__table)
        self.setCentralWidget(frame)

    def __form(self):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel|QFrame.Sunken)
        formlayout = QFormLayout()
        formlayout.setLabelAlignment(Qt.AlignRight)
        formlayout.setSpacing(2)
        self.__id = QLabel('Henüz atanmadı')
        self.__name = QLineEdit()
        self.__label = QLineEdit()
        self.__plan = QLineEdit()
        self.__color = MktColor(mktDefaultBackgrundColor='#ffffff',
                                mktDefaultForegrundColor='#000000',
                                icon=QIcon('./icons/color.png'))
        self.__definition = QTextEdit()
        formlayout.addRow(QLabel('No:'), self.__id)
        formlayout.addRow(QLabel('Yerimi adı:'), self.__name)
        formlayout.addRow(QLabel('Etiket:'), self.__label)
        formlayout.addRow(QLabel('Plan:'), self.__plan)
        formlayout.addRow(QLabel('Renkler:'), self.__color)
        formlayout.addRow(QLabel('Açıklama:'), self.__definition)
        frame.setLayout(formlayout)
        self.__vbox.addWidget(frame)

    def __menu(self):
        toolbar = self.addToolBar('main')
        toolbar.setIconSize(QSize(16,16))
        toolbar.setMovable(False)
        openAction = QAction(QIcon('./icons/open.png'),'Yerimi dosyaları', self)
        openAction.setStatusTip('Yerimi dosyası yüklemek için kullanabilirsiniz.')
        openAction.triggered.connect(self.openActionClicked)
        saveAction = QAction(QIcon('./icons/save.png'),'Yerimi dosyası olarak kaydeder', self)
        saveAction.setStatusTip('Tanımlanmış yerimi listesini kaydetmek için kullanabilirsiniz.')
        saveAction.triggered.connect(self.saveActionClicked)
        addAction = QAction(QIcon('./icons/add.png'),'Listeye ekle', self)
        addAction.setStatusTip('Tanımlanmış yerimini, yerimi listesine eklemek için kullanabilirsiniz.')
        addAction.triggered.connect(self.addActionClicked)
        editAction = QAction(QIcon('./icons/edit.png'),'Değiştir', self)
        editAction.setStatusTip('Tanımlanmış yerimi özelliklerimi için kullanabilirsiniz.')
        editAction.triggered.connect(self.editActionClicked)
        delAction = QAction(QIcon('./icons/del.png'),'Listeden kaldır', self)
        delAction.setStatusTip('Seçilmiş yerimi listeden kaldırmak için kullanabilirsiniz.')
        delAction.triggered.connect(self.delActionClicked)
        removeAction = QAction(QIcon('./icons/remove.png'),'Listeyi temizle', self)
        removeAction.setStatusTip('Yerimi listesini temizlemek için kullanabilirsiniz.')
        removeAction.triggered.connect(self.removeActionClicked)
        toolbar.addAction(openAction)
        toolbar.addAction(saveAction)
        toolbar.addSeparator()
        toolbar.addAction(addAction)
        toolbar.addAction(editAction)
        toolbar.addAction(delAction)
        toolbar.addAction(removeAction)


    def openActionClicked(self):
        try:
            self.__table.openList(title='Yerimi olarak kaydet',
                                  extention='sbf',
                                  explain='Yerimi dosyası',
                                  directory='./thesis/')
            data = self.__table.getRowDataFromIndex(0)
            self.__id.setText(data[0])
            self.__name.setText(data[1])
            self.__label.setText(data[2])
            self.__plan.setText(data[3])
            self.__color.setBackgroundColor(data[4])
            self.__color.setForegoundColor(data[5])
            self.__definition.setPlainText(data[6])
            self.statusBar().showMessage('Yerimi listesi yüklendi.')
        except:
            self.statusBar().showMessage('Yükleme işlemi esnasında hata')

    def saveActionClicked(self):
        try:
            self.__table.saveList(title='Yerimi olarak kaydet',
                              extention='sbf',
                              explain='Yerimi dosyası',
                              directory='./thesis/')
            self.statusBar().showMessage('Liste yerimi listesi olarak kaydedildi.')
        except:
            self.statusBar().showMessage('Kaydetme işlemi esnasında hata')

    def addActionClicked(self):
        try:
            data = [self.__name.text(),
                    self.__label.text(),
                    self.__plan.text(),
                    self.__color.backgroundColor(),
                    self.__color.foregroundColor(),
                    self.__definition.toPlainText()]
            id = self.__table.addRow(data)
            self.__id.setText(str(id))
            self.statusBar().showMessage('Tanımlanmış yerimi listeye aktarıldı.')
        except:
            self.statusBar().showMessage('Ekleme işlemi esnasında hata')

    def editActionClicked(self):
        try:
            data = [self.__name.text(),
                    self.__label.text(),
                    self.__plan.text(),
                    self.__color.backgroundColor(),
                    self.__color.foregroundColor(),
                    self.__definition.toPlainText()]
            result = self.__table.editRow(data)
            if result == 1:
                self.statusBar().showMessage('Seçilen kayıt düzenlendi')
            else:
                self.statusBar().showMessage('Herhngi bir kayıt seçilmeden düzenleme yapılamaz.')
        except:
            self.statusBar().showMessage('Düzeltme işlemi esnasında hata')

    def delActionClicked(self):
        try:
            self.__table.delRow()
            self.__table.reNumbered()
            self.statusBar().showMessage('Seçilen kayıt listeden kaldırıldı')
        except:
            self.statusBar().showMessage('Silme işlemi esnasında hata')

    def removeActionClicked(self):
        try:
            self.__table.removeAllItems()
            self.statusBar().showMessage('Liste temizlendi.')
        except:
            self.statusBar().showMessage('Silme işlemi esnasında hata')

    def tableClicked(self):
        try:
            data = self.__table.getSelectedRowData()
            self.__id.setText(data[0])
            self.__name.setText(data[1])
            self.__label.setText(data[2])
            self.__plan.setText(data[3])
            self.__color.setBackgroundColor(data[4])
            self.__color.setForegoundColor(data[5])
            self.__definition.setPlainText(data[6])
            self.statusBar().showMessage('{} nolu kayıt aktarıldı'.format(self.__id.text()))
        except:
            self.statusBar().showMessage('Aktarma işlemi esnasında hata')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BookmarkManager()
    ex.show()
    sys.exit(app.exec_())