import sys
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QComboBox,
                             QFrame, QLineEdit, QTextEdit, QAction, QFormLayout, QFileDialog)
from PyQt5.QtGui import (QIcon, QFont)
from PyQt5.Qt import (Qt, QSize)
from widgets.mktTable import MktTable
from widgets.mktLEditButton import MktLEditButton
from widgets.mktSelectList import MktSelectList


class AttributeManager(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Nitelik yönetim formu')
        self.setWindowIcon(QIcon('./icons/attribute.png'))
        self.statusBar().showMessage('Kullanıma hazır.')
        self.setFont(QFont('Calibri', 8))
        self.__vbox = QVBoxLayout()
        self.__vbox.setContentsMargins(2, 2, 2, 2)
        frame = QFrame()
        frame.setLayout(self.__vbox)
        self.__menu()
        self.__form()
        self.__table = MktTable(headers=['No', 'Ad', 'Etiket', 'Tip', 'Yerimleri', 'Açıklama', 'Kaynak'])
        self.__table.clicked = self.tableClicked
        self.__vbox.addWidget(self.__table)
        self.setCentralWidget(frame)

    def __menu(self):
        toolbar = self.addToolBar('main')
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)
        openAction = QAction(QIcon('./icons/open.png'), 'Nitelik dosyaları', self)
        openAction.setStatusTip('Nitelik dosyası yüklemek için kullanabilirsiniz.')
        openAction.triggered.connect(self.openActionClicked)
        saveAction = QAction(QIcon('./icons/save.png'), 'Nitelik dosyası olarak kaydeder', self)
        saveAction.setStatusTip('Tanımlanmış niteliği listeye kaydetmek için kullanabilirsiniz.')
        saveAction.triggered.connect(self.saveActionClicked)
        addAction = QAction(QIcon('./icons/add.png'), 'Listeye ekle', self)
        addAction.setStatusTip('Tanımlanmış niteliği, yerimi listesine eklemek için kullanabilirsiniz.')
        addAction.triggered.connect(self.addActionClicked)
        editAction = QAction(QIcon('./icons/edit.png'), 'Değiştir', self)
        editAction.setStatusTip('Tanımlanmış niteliğin özelliklerimi için kullanabilirsiniz.')
        editAction.triggered.connect(self.editActionClicked)
        delAction = QAction(QIcon('./icons/del.png'), 'Listeden kaldır', self)
        delAction.setStatusTip('Seçilmiş niteliği listeden kaldırmak için kullanabilirsiniz.')
        delAction.triggered.connect(self.delActionClicked)
        removeAction = QAction(QIcon('./icons/remove.png'), 'Listeyi temizle', self)
        removeAction.setStatusTip('Nitelik listesini temizlemek için kullanabilirsiniz.')
        removeAction.triggered.connect(self.removeActionClicked)
        toolbar.addAction(openAction)
        toolbar.addAction(saveAction)
        toolbar.addSeparator()
        toolbar.addAction(addAction)
        toolbar.addAction(editAction)
        toolbar.addAction(delAction)
        toolbar.addAction(removeAction)

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

        frame1 = QFrame()
        frame1.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        formlayout1 = QFormLayout()
        formlayout1.setLabelAlignment(Qt.AlignRight)
        formlayout1.setSpacing(2)
        self.__id = QLabel('Henüz atanmadı')
        self.__name = QLineEdit()
        self.__label = QLineEdit()
        self.__type = QComboBox()
        self.__type.addItems(['Uzunluk','Alan','Açı','Dairesel çevre','Dairesel alan'])
        self.__bmks = MktSelectList(icons=[QIcon('./icons/add.png'),
                                           QIcon('./icons/del.png'),
                                           QIcon('./icons/remove.png')])
        self.__definition = QTextEdit()
        formlayout1.addRow(QLabel('Ad:'), self.__name)
        formlayout1.addRow(QLabel('Etiket:'), self.__label)
        formlayout1.addRow(QLabel('Tip:'), self.__type)
        formlayout1.addRow(QLabel('Yerimlerş:'), self.__bmks)
        formlayout1.addRow(QLabel('Açıklama:'), self.__definition)
        frame1.setLayout(formlayout1)
        self.__vbox.addWidget(frame)
        self.__vbox.addWidget(frame1)

    def sourceClicked(self):
        dialog = QFileDialog()
        dialog.setDefaultSuffix('sbf')
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilters(['Sekazu yer imi dosyası (*.sbf)'])
        dialog.setDirectory('./')
        if dialog.exec_() == QFileDialog.Accepted:
            fname = dialog.selectedFiles()[0]
            self.__source.setText(fname)
            df = pd.read_csv(fname)
            names = list(df['Ad'].values)
            labels = list(df['Etiket'].values)
            items = ['{}:{}'.format(f[0], f[1]) for f in list(zip(names, labels))]
            self.__bmks.changeItems(items)


    def openActionClicked(self):
        try:
            self.__table.openList(title='Nitelik olarak kaydet',
                                  extention='saf',
                                  explain='Nitelik dosyası',
                                  directory='./thesis/')
            data = self.__table.getRowDataFromIndex(0)
            self.__source.setText(data[6])
            df = pd.read_csv(self.__source.text(), encoding='utf-8')
            names = list(df['Ad'].values)
            labels = list(df['Etiket'].values)
            items = ['{}:{}'.format(f[0], f[1]) for f in list(zip(names, labels))]
            self.__bmks.changeItems(items)
            self.__id.setText(data[0])
            self.__name.setText(data[1])
            self.__label.setText(data[2])
            self.__type.setCurrentText(data[3])
            items = data[4].split('|')
            self.__bmks.setListItems(items)
            self.__definition.setPlainText(data[5])
            self.__source.setText(data[6])
            self.statusBar().showMessage('Nitelik listesi yüklendi.')
        except:
            self.statusBar().showMessage('Yükleme işlemi esnasında hata')
            print(sys.exc_info())

    def saveActionClicked(self):
        try:
            self.__table.saveList(title='Nitelik olarak kaydet',
                              extention='saf',
                              explain='Nitelik dosyası',
                              directory='./thesis/')
            self.statusBar().showMessage('Liste nitelik dosyası olarak kaydedildi.')
        except:
            self.statusBar().showMessage('Kaydetme işlemi esnasında hata')

    def addActionClicked(self):
        try:
            items = ''
            for i in self.__bmks.getListItems():
                items = items + i +'|'
            items = items[:-1]
            data = [self.__name.text(),
                    self.__label.text(),
                    self.__type.currentText(),
                    items,
                    self.__definition.toPlainText(),
                    self.__source.text()]
            id = self.__table.addRow(data)
            self.__id.setText(str(id))
            self.statusBar().showMessage('Tanımlanmış nitelik listeye aktarıldı.')
        except:
            self.statusBar().showMessage('Ekleme işlemi esnasında hata')

    def editActionClicked(self):
        try:
            items = ''
            for i in self.__bmks.getListItems():
                items = items + i + '|'
            items = items[:-1]
            data = [self.__id.text(),
                    self.__name.text(),
                    self.__label.text(),
                    self.__type.currentText(),
                    items,
                    self.__definition.toPlainText(),
                    self.__source.text()]
            result = self.__table.editRow(data)
            if result == 1:
                self.statusBar().showMessage('Seçilen kayıt düzenlendi.')
            else:
                self.statusBar().showMessage('Herhngi bir kayıt seçilmeden düzenleme yapılamaz.')
        except:
            self.statusBar().showMessage('Düzeltme işlemi esnasında hata')
            print(sys.exc_info())

    def delActionClicked(self):
        try:
            self.__table.delRow()
            self.__table.reNumbered()
            self.statusBar().showMessage('Seçilen nitelik listeden kaldırıldı')
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
            self.__type.setCurrentText(data[3])
            items = data[4].split('|')
            self.__bmks.setListItems(items)
            self.__definition.setPlainText(data[5])
            self.__source.setText(data[6])
            self.statusBar().showMessage('{} nolu kayıt aktarıldı'.format(self.__id.text()))
        except:
            self.statusBar().showMessage('Aktarma işlemi esnasında hata')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AttributeManager()
    ex.show()
    sys.exit(app.exec_())