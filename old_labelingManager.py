import os
import sys
import qimage2ndarray
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QLineEdit, QComboBox, QVBoxLayout, QHBoxLayout,
                             QFrame, QListWidget, QAction, QFileDialog, QTabWidget, QScrollArea, QSplitter,
                             QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem,
                             QGraphicsSceneMouseEvent, QMessageBox)
from PyQt5.QtGui import (QIcon, QPixmap)
from PyQt5.QtCore import (Qt, QSize)
from widgets.mktTable import MktTable
from widgets.dicom import Dicom, Dose


class LabelingManager(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Çok planlı görüntü etiketleme sürüm 5.0')
        frame = QFrame()
        vbox = QVBoxLayout()
        frame.setLayout(vbox)

        self.__tb = self.addToolBar('Main')
        self.__tb.setIconSize(QSize(20,20))
        self.__create_tool_bar()

        tab = QTabWidget()
        image_screen = self.__create_image_screen()
        tab.addTab(image_screen, 'Görüntü')

        coordinate_list = self.__create_coordinate_list()
        tab.addTab(coordinate_list, 'Koordinatlar')

        vbox.addWidget(tab)
        self.__selected_bookmark = ''
        self.setCentralWidget(frame)

    def __create_image_screen(self):
        frame = QFrame()
        vbox = QHBoxLayout()
        frame.setLayout(vbox)
        self.__scene = QGraphicsScene()
        self.__view = QGraphicsView()
        self.__view.setScene(self.__scene)
        self.__image = QGraphicsPixmapItem()
        self.__image.setCursor(Qt.CrossCursor)
        self.__image.mousePressEvent = self.__image_clicked
        self.__scene.addItem(self.__image)
        vbox.addWidget(self.__view)
        # Bookmark list
        frame_bookmarks = QFrame()
        vbox_bookmarks = QVBoxLayout()
        frame_bookmarks.setLayout(vbox_bookmarks)
        self.__bookmark_list = MktTable(headers=['Id', 'Etiket','Plan', 'X', 'Y'], title='Yer imleri')
        self.__bookmark_list.clicked = self.__bookmark_list_clicked
        vbox_bookmarks.addWidget(self.__bookmark_list)

        splitter = QSplitter()
        splitter.addWidget(frame)
        splitter.addWidget(frame_bookmarks)
        return splitter

    def __bookmark_list_clicked(self):
        if self.__bookmark_list.getSelectedRowData():
            etiket = self.__bookmark_list.getSelectedRowData()[1]
            self.__selected_bookmark = self.__sbf[ self.__sbf['Etiket'] == etiket].values[0]


    def __create_coordinate_list(self):
        frame = QFrame()
        vbox = QVBoxLayout()
        frame.setLayout(vbox)
        self.__coordinate_table = MktTable()
        self.__coordinate_table.clicked = self.__coordinate_table_clicked
        vbox.addWidget(self.__coordinate_table)
        return frame

    """
            for item in self.scene_manager.scene.items():
            if isinstance(item, QGraphicsTextItem):
                self.scene_manager.scene.removeItem(item)
    """

    def __image_clicked(self, event:QGraphicsSceneMouseEvent):
        try:
            if len(self.__selected_bookmark) != 0:
                flag = False
                for i in self.__scene.items():
                    if isinstance(i, QGraphicsTextItem):
                        if i.toPlainText() == self.__selected_bookmark[2]:
                            flag = True
                if flag == False:
                    x = event.pos().x()
                    y = event.pos().y()
                    text = QGraphicsTextItem()
                    text.setHtml(f"<div style='background-color:{self.__selected_bookmark[4]};color:{self.__selected_bookmark[5]};'>{self.__selected_bookmark[2]}</div>")
                    text.setX(x)
                    text.setY(y)
                    self.__scene.addItem(text)

                    data = self.__bookmark_list.getSelectedRowData()
                    data[3] = str(x)
                    data[4] = str(y)
                    self.__bookmark_list.editRow(data)


                else:
                    QMessageBox.warning(
                        self,
                        'Dikkat',
                        'Daha önce bu etiketi görüntü üstüne konumlandırdınız. Silerek yeniden konumlandırmayı denemek isteyebilirsiniz.'
                    )

        except:
            print(sys.exc_info())

    def __coordinate_table_clicked(self):
        pass

    def __create_tool_bar(self):
        action = QAction(QIcon('./icons/open.png'), 'Yer imi dosyası yükle', self)
        action.triggered.connect(self.open_saf_file)
        self.__tb.addWidget(QLabel('Nitelik dosyası:'))
        self.__saf_file_name = QLineEdit()
        self.__tb.addWidget(self.__saf_file_name)
        self.__tb.addAction(action)
        self.__tb.addSeparator()

        open_image = QAction(QIcon('./icons/openimage.png'), 'Bir görüntü dosyası yükler', self)
        open_image.triggered.connect(self.open_image_button_clicked)
        self.__tb.addWidget(QLabel('Görüntü dosyası:'))
        self.__saf_image_name = QLineEdit()
        self.__tb.addWidget(self.__saf_image_name)
        self.__tb.addAction(open_image)
        self.__tb.addSeparator()

        self.__protocol = QLineEdit('')
        self.__protocol.setFixedWidth(60)
        self.__patient_name = QLineEdit()
        self.__patient_age = QLineEdit()
        self.__patient_stature = QLineEdit()
        self.__tb.addWidget(QLabel('Protokol:'))
        self.__tb.addWidget(self.__protocol)
        self.__tb.addWidget(QLabel('Adı:'))
        self.__tb.addWidget(self.__patient_name)
        self.__tb.addWidget(QLabel('Yaş:'))
        self.__tb.addWidget(self.__patient_age)
        self.__tb.addWidget(QLabel('Boy:'))
        self.__tb.addWidget(self.__patient_stature)
        self.__tb.addSeparator()
        self.__patient_gender = QComboBox()
        self.__patient_gender.addItems(['Kadın','Erkek'])
        self.__tb.addWidget(QLabel('Cinsiyet:'))
        self.__tb.addWidget(self.__patient_gender)
        self.__tb.addSeparator()

        transfer_coordinates = QAction(QIcon('./icons/add.png'), 'Koordinatları ekle', self)
        transfer_coordinates.triggered.connect(self.transfer_coordinates_button_clicked)
        self.__tb.addAction(transfer_coordinates)

        remove_coordinates = QAction(QIcon('./icons/del.png'), 'Koordinatı sil', self)
        remove_coordinates.triggered.connect(self.remove_coordinates_button_clicked)
        self.__tb.addAction(remove_coordinates)

        clear_coordinates = QAction(QIcon('./icons/remove.png'), 'Listeyi temizle', self)
        clear_coordinates.triggered.connect(self.clear_coordinates_button_clicked)
        self.__tb.addAction(clear_coordinates)
        self.__tb.addSeparator()

        save_coordinates = QAction(QIcon('./icons/save.png'), 'Koordinatları kaydet', self)
        save_coordinates.triggered.connect(self.save_coordinates_button_clicked)
        self.__tb.addAction(save_coordinates)

    def open_saf_file(self):
        dialog = QFileDialog()
        dialog.setDefaultSuffix('saf')
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilters(['Sekazu nitelik dosyası (*.saf)'])
        dialog.setDirectory('./')
        if dialog.exec_() == QFileDialog.Accepted:
            fname = dialog.selectedFiles()[0]
            filename, file_extension = os.path.splitext(fname)
            self.__saf_file_name.setText(fname)
            self.__saf = pd.read_csv(fname)
            self.__sbf = pd.read_csv(self.__saf['Kaynak'].values[0])
            self.__bookmark_list.removeAllItems()
            headers = ['Id','Adı','Görüntü','Adı','Yaşı','Boyu','Cinsiyeti']
            plans = self.__sbf[['Etiket', 'Plan']].values
            for i in plans:
                data = [i[0], i[1], 0, 0]
                self.__bookmark_list.addRow(data)
                headers.append(i[0])

            self.__coordinate_table.changeHeaders(headers)

    def clear_coordinates_button_clicked(self):
        pass

    def remove_coordinates_button_clicked(self):
        pass

    def open_image_button_clicked(self):
        dialog = QFileDialog()
        dialog.setDefaultSuffix('dcm')
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilters(['Dicom dosyası (*.dcm)'])
        dialog.setDirectory('./')
        if dialog.exec_() == QFileDialog.Accepted:
            fname = dialog.selectedFiles()[0]
            filename, file_extension = os.path.splitext(fname)
            self.__saf_image_name.setText(fname)
            self.__x_factor = 1
            self.__y_factor = 1

            dcmRead = Dicom.read(fname)
            self.__x_factor, self.__y_factor = [float(x) for x in dcmRead[0x0028, 0x0030].value]
            img = Dicom.windowed_slice(dcmRead, Dose.BONE)
            nimage = qimage2ndarray.array2qimage(img, normalize=(np.min(img), np.max(img)))
            pixmap = QPixmap(nimage)
            self.__image.setPixmap(pixmap)

    def save_coordinates_button_clicked(self):
        pass


    def transfer_coordinates_button_clicked(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LabelingManager()
    ex.show()
    sys.exit(app.exec_())


