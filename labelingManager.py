import os
import sys
import qimage2ndarray
import numpy as np
import pandas as pd
from pydicom.tag import Tag
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout,
                             QFrame, QListWidget, QAction, QFileDialog, QTabWidget, QScrollArea, QSplitter,
                             QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem,
                             QGraphicsSceneMouseEvent, QMessageBox, QFormLayout, QPushButton)
from PyQt5.QtGui import (QIcon, QPixmap)
from PyQt5.QtCore import (Qt, QSize)
from widgets.mktTable import MktTable
from widgets.dicom import Dicom, Dose

class Bookmark(QGraphicsTextItem):

    def __init__(self, main_table:MktTable, scene:QGraphicsScene, x, y, title, colors):
        self.__text = QGraphicsTextItem()
        self.__text.mousePressEvent = self.__mousePressEvent
        self.__text.setX(x)
        self.__text.setY(y)
        self.__title = title
        self.__text.setHtml(f"<div style='background-color:{colors[0]};color:{colors[1]};'>{self.__title}</div>")
        self.__scene = scene
        self.__table = main_table


    def __mousePressEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if event.button() == 4:
            for i in range(0, self.__table.rowCount()):
                data = self.__table.getRowDataFromIndex(i)
                if data[2] == self.__title:
                    data[4] = -1
                    data[5] = -1
                    self.__table.editRowWithIndex(data, i)
            self.__scene.removeItem(self.__text)

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, value):
        self.__text = value

class LabelingManager(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__x_factor = 1
        self.__y_factor = 1
        self.setWindowTitle('Çok planlı görüntü etikleme modülü sürüm 6.0')
        self.__tb = self.addToolBar('Main')
        self.__tb.setIconSize(QSize(18,18))
        self.menu()
        tab = QTabWidget()
        image_screen = self.image_screen()
        coordinate_screen = self.coordinate_screen()
        tab.addTab(image_screen, 'Görüntü')
        tab.addTab(coordinate_screen, 'Koordinatlar')
        self.__scene_item_list = []
        self.setCentralWidget(tab)

    def menu(self):
        open_image = QAction(QIcon('./icons/openimage.png'), 'Bir görüntü yükler', self)
        open_image.triggered.connect(self.open_image_button_clicked)
        self.__tb.addAction(open_image)
        open_scf = QAction(QIcon('./icons/open.png'), 'Bir koordinatg dosyası yükler', self)
        open_scf.triggered.connect(self.open_scf_button_clicked)
        self.__tb.addAction(open_image)
        self.__tb.addAction(open_scf)
        self.__tb.addSeparator()
        transfer_coordinate = QAction(QIcon('./icons/add.png'), 'Koordinatları aktar', self)
        transfer_coordinate.triggered.connect(self.transfer_coordinate_clicked)
        remove_coordinate = QAction(QIcon('./icons/del.png'), 'Seçili koordinatı sil', self)
        remove_coordinate.triggered.connect(self.remove_coordinate_clicked)
        self.__tb.addAction(transfer_coordinate)
        self.__tb.addAction(remove_coordinate)
        self.__tb.addSeparator()
        save_coordinate = QAction(QIcon('./icons/save.png'), 'Koordinat dosyasını kaydet', self)
        save_coordinate.triggered.connect(self.save_coordinate_button_clicked)
        self.__tb.addAction(save_coordinate)

    def open_scf_button_clicked(self):
        try:
            dialog = QFileDialog()
            dialog.setDefaultSuffix('scf')
            dialog.setAcceptMode(QFileDialog.AcceptOpen)
            dialog.setNameFilters(['Sekazu koordinat dosyası (*.scf)'])
            dialog.setDirectory('./')
            if dialog.exec_() == QFileDialog.Accepted:
                fname = dialog.selectedFiles()[0]
                scf = pd.read_csv(fname)
                for i in scf.values:
                    self.__coordinate_table.addRow([str(x) for x in i[2:]])
        except:
            print(sys.exc_info())


    def save_coordinate_button_clicked(self):
        try:
            dialog = QFileDialog()
            dialog.setDefaultSuffix('*.scf')
            dialog.setAcceptMode(QFileDialog.AcceptSave)
            if dialog.exec_() == QFileDialog.Accepted:
                fname = dialog.selectedFiles()[0]
                all_data = []
                for i in range(0, self.__coordinate_table.rowCount()):
                    data = self.__coordinate_table.getRowDataFromIndex(i)
                    all_data.append(data)
                headers = self.__coordinate_table.getHeaders()
                df = pd.DataFrame(data=all_data, columns=headers)
                df.to_csv(fname)
                self.statusBar().showMessage('Liste koordinat dosyası olarak kaydedildi.')
        except:
            self.statusBar().showMessage(f'Kaydetme işlemi esnasında hata {sys.exc_info()}')

    def remove_coordinate_clicked(self):
        self.__coordinate_table.delRow()

    def transfer_coordinate_clicked(self):
        # ['No', 'Protokol', 'Ad', 'Yaş', 'Boy', 'Cinsiyet', 'Kaynak']
        data = [self.__patient_protokol.text(),
                self.__patient_name.text(),
                self.__patient_age.text(),
                self.__patient_stature.text(),
                self.__patient_gender.currentText(),
                self.__saf_file_name.text()
                ]
        for i in range(0, self.__bookmark_table.rowCount()):
            temp = self.__bookmark_table.getRowDataFromIndex(i)
            coor = f"{temp[4]}:{temp[5]}"
            data.append(coor)
        self.__coordinate_table.addRow(data)
        # NE VARSA SİL
        for item in self.__scene.items():
            if isinstance(item, QGraphicsTextItem):
                self.__scene.removeItem(item)
        self.__bookmark_table.removeAllItems()
        self.__bookmark_table.changeHeaders(['No', 'Ad', 'Etiket', 'Plan', 'X', 'Y'])
        for i in self.__sbf[['No', 'Ad', 'Etiket', 'Plan']].values:
            temp = list(i)
            temp.append(-1)
            temp.append(-1)
            self.__bookmark_table.addRow(temp[1:])

    def coordinate_screen(self):
        frame = QFrame()
        vbox = QVBoxLayout()
        frame.setLayout(vbox)
        self.__coordinate_table = MktTable()
        self.__coordinate_table.clicked = self.coordinate_table_clicked
        vbox.addWidget(self.__coordinate_table)
        return frame

    def coordinate_table_clicked(self):
        pass

    def image_screen(self):
        splitter = QSplitter()
        # Image
        self.__scene = QGraphicsScene()
        self.__view = QGraphicsView()
        self.__image = QGraphicsPixmapItem()
        self.__image.setCursor(Qt.CrossCursor)
        self.__image.mousePressEvent = self.image_mouse_press_event
        self.__scene.addItem(self.__image)
        self.__view.setScene(self.__scene)
        splitter.addWidget(self.__view)
        #Form
        frame = QFrame()
        vbox = QVBoxLayout()
        frame.setLayout(vbox)

        frame_patient = QFrame()
        self.__patient_name = QLineEdit()
        self.__patient_gender = QComboBox()
        self.__patient_gender.addItems(['Kadın','Erkek'])
        self.__patient_age = QLineEdit('0')
        self.__patient_stature = QLineEdit('0')
        self.__patient_protokol = QLineEdit('1')
        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.addRow(QLabel(''), QLabel('Parametre listesi'))
        hbox_param = QHBoxLayout()
        self.__saf_file_open = QPushButton()
        self.__saf_file_open.setCursor(Qt.PointingHandCursor)
        self.__saf_file_open.clicked.connect(self.saf_file_open_clicked)
        self.__saf_file_open.setIcon(QIcon('./icons/open.png'))
        self.__saf_file_name = QLineEdit()
        hbox_param.addWidget(self.__saf_file_name)
        hbox_param.addWidget(self.__saf_file_open)
        form_layout.addRow('Nitelik dosyası:', hbox_param)

        form_layout.addRow(QLabel(''),QLabel('Hasta bilgileri'))
        form_layout.addRow(QLabel('Hastanın adı:'), self.__patient_name)
        form_layout.addRow(QLabel('Cinsiyeti:'), self.__patient_gender)
        form_layout.addRow(QLabel('Yaşı:'), self.__patient_age)
        form_layout.addRow(QLabel('Boyu:'), self.__patient_stature)
        form_layout.addRow(QLabel('Protokol:'), self.__patient_protokol)

        frame_patient.setLayout(form_layout)
        self.__bookmark_table = MktTable()
        self.__bookmark_table.clicked = self.bookmark_table_clicked
        vbox.addWidget(frame_patient)
        vbox.addWidget(self.__bookmark_table)

        splitter.addWidget(frame)

        return splitter

    def image_mouse_press_event(self, event:QGraphicsSceneMouseEvent):
        if event.button() == 1:
            data = self.__bookmark_table.getSelectedRowData()
            if data:
                etiket = data[2]
                colors = self.__sbf[ self.__sbf['Etiket']==etiket][['Arkaplan','Yazı rengi']].values[0]
                x = event.pos().x()
                y = event.pos().y()
                text = Bookmark(self.__bookmark_table, self.__scene, x, y, etiket, colors)
                flag = False
                for item in self.__scene.items():
                    if isinstance(item, QGraphicsTextItem):
                        if item.toPlainText() == etiket:
                            flag = True
                if flag == False:
                    self.__scene.addItem(text.text)
                    data[4] = "{0:0.5f}".format(x * self.__x_factor)
                    data[5] = "{0:0.5f}".format(y * self.__y_factor)
                    self.__bookmark_table.editRow(data)
                else:
                    QMessageBox.information(self,'Dikkat','Daha önceden bu yerimini resim üzerinde kullandınız.')
            else:
                QMessageBox.information(self, 'Dikkat', 'Tablodan bir yerimi seçmeden bu işlemi gerçekleştiremezsiniz.')

    def open_image_button_clicked(self):
        dialog = QFileDialog()
        dialog.setDefaultSuffix('dcm')
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilters(['Dicom dosyası (*.dcm)'])
        dialog.setDirectory('./')
        if dialog.exec_() == QFileDialog.Accepted:
            fname = dialog.selectedFiles()[0]
            dcmRead = Dicom.read(fname)
            self.__x_factor, self.__y_factor = [float(x) for x in dcmRead[0x0028, 0x0030].value]
            print(self.__x_factor, self.__y_factor)
            img = Dicom.windowed_slice(dcmRead, Dose.BONE)
            nimage = qimage2ndarray.array2qimage(img, normalize=(np.min(img), np.max(img)))
            pixmap = QPixmap(nimage)
            self.__image.setPixmap(pixmap)
            # NAME
            if Tag(0x0010, 0x0010) in dcmRead.keys():
                self.__patient_name.setText(str(dcmRead[0x010, 0x0010].value))
            else:
                self.__patient_name.setText('John Doe')
            if Tag(0x0010, 0x0040) in dcmRead.keys():
                if str(dcmRead[0x010, 0x0040].value) == 'M':
                    self.__patient_gender.setCurrentIndex(1)
                else:
                    self.__patient_gender.setCurrentIndex(0)
            for item in self.__scene.items():
                if isinstance(item, QGraphicsTextItem):
                    item.hide()

    def saf_file_open_clicked(self):
        dialog = QFileDialog()
        dialog.setDefaultSuffix('saf')
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilters(['Sekazu nitelik dosyası (*.saf)'])
        dialog.setDirectory('./')
        if dialog.exec_() == QFileDialog.Accepted:
            fname = dialog.selectedFiles()[0]
            self.__saf_file_name.setText(fname)
            self.__saf = pd.read_csv(fname, index_col=None)
            self.__sbf = pd.read_csv(self.__saf['Kaynak'].values[0], index_col=None)
            self.__bookmark_table.changeHeaders(['No', 'Ad', 'Etiket', 'Plan', 'X', 'Y'])
            for i in self.__sbf[['No', 'Ad', 'Etiket', 'Plan']].values:
                temp = list(i)
                temp.append(-1)
                temp.append(-1)
                self.__bookmark_table.addRow(temp[1:])
            headers = ['No', 'Protokol', 'Ad', 'Yaş', 'Boy', 'Cinsiyet', 'Kaynak']
            for i in self.__sbf['Etiket'].values:
                headers.append(i)
            self.__coordinate_table.changeHeaders(headers)

    def bookmark_table_clicked(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LabelingManager()
    ex.show()
    sys.exit(app.exec_())