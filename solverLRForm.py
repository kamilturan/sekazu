import sys
import pandas as pd
import numpy as np
import itertools
from widgets.mktTable import MktTable
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, QProgressBar,
                             QFrame, QLineEdit, QTextEdit, QAction, QFormLayout, QFileDialog)
from PyQt5.QtGui import (QIcon, QFont, QIntValidator)
from PyQt5.Qt import (Qt, QSize)
from widgets.mktLEditButton import MktLEditButton
from sklearn.metrics import multilabel_confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import (KFold, cross_val_predict)
from metricUtils import MultiLabelPerformanceMetrics

class SolverForDT(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('RF hesaplayıcı')
        self.setWindowIcon(QIcon('./icons/solver.png'))
        self.statusBar().showMessage('Kullanıma hazır.')
        self.setFont(QFont('Calibri', 8))
        self.__vbox = QVBoxLayout()
        self.__vbox.setContentsMargins(2, 2, 2, 2)
        frame = QFrame()
        frame.setLayout(self.__vbox)
        self.__classifier = RandomForestClassifier()
        self.__progressbar = QProgressBar()
        self.__progressbar.setMinimum(0)
        self.__progressbar.setTextVisible(False)
        self.__progressbar.setFixedHeight(14)
        self.__progressbar2 = QProgressBar()
        self.__progressbar2.setMinimum(0)
        self.__progressbar2.setTextVisible(False)
        self.__progressbar2.setFixedHeight(14)
        self.__menu()
        self.__form()
        self.__report()
        self.setCentralWidget(frame)

    def __menu(self):
        toolbar = self.addToolBar('main')
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)
        runAction = QAction(QIcon('./icons/run.png'), 'Makina öğrenme algoritmasını uygula', self)
        runAction.setStatusTip('Makina öğrenme algoritmasını uygulamak için kullanabilirsiniz')
        runAction.triggered.connect(self.runActionClicked)
        delAction = QAction(QIcon('./icons/del.png'),'Argümanları temizle', self)
        delAction.setStatusTip('Argüman listesini temizlemek için kullanabilirsiniz.')
        delAction.triggered.connect(self.delActionClicked)
        saveAction = QAction(QIcon('./icons/save.png'), 'Rapor dosyası olarak kaydeder', self)
        saveAction.setStatusTip('Rapor dosyası olarak kaydetmek için kullanabilirsiniz')
        saveAction.triggered.connect(self.saveActionClicked)
        toolbar.addAction(runAction)
        toolbar.addAction(delAction)
        toolbar.addSeparator()
        toolbar.addAction(saveAction)

    def __form(self):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        formlayout = QFormLayout()
        formlayout.setLabelAlignment(Qt.AlignRight)
        formlayout.setSpacing(2)
        self.__source = MktLEditButton(QIcon('./icons/open.png'))
        self.__source.clicked = self.sourceClicked
        formlayout.addRow(QLabel('Kaynak:'), self.__source)
        self.__args = QTextEdit()
        params = self.__classifier.get_params(deep=True)
        text = ''
        for i in params.keys():
            text = text + '{}:{}\n'.format(i, params[i])
        text = text[:-1]
        self.__args.setPlainText(text)
        formlayout.addRow(QLabel('Argümanlar:'), self.__args)
        self.__rcount = QLineEdit()
        self.__rcount.setText('10')
        intval = QIntValidator()
        self.__rcount.setValidator(intval)
        formlayout.addRow(QLabel('k-Fold Doğrulama:'), self.__rcount)
        frame.setLayout(formlayout)
        self.__vbox.addWidget(frame)

    def __report(self):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        vbox = QVBoxLayout()
        vbox.setContentsMargins(1,1,1,1)
        label = QLabel('Rapor')
        label.setAlignment(Qt.AlignCenter)
        self.__result =  MktTable(title='Sonuç Dosyası',
                                headers=['No', 'Sınıf', 'Acc', 'Mcc', 'Sen', 'Spe', 'F1', 'Ppv', 'Npv', 'Fmi', 'TN', 'FP',
                                        'FN', 'TP','Parametreler','Parametre sayısı','İncelenen model'])
        self.__result.clicked = self.tableClicked

        vbox.addWidget(label)
        vbox.addWidget(self.__result)
        vbox.addWidget(self.__progressbar)
        vbox.addWidget(self.__progressbar2)
        frame.setLayout(vbox)
        self.__vbox.addWidget(frame)

    def tableClicked(self):
        pass

    def delActionClicked(self):
        params = self.__classifier.get_params(deep=True)
        text = ''
        for i in params.keys():
            text = text + '{}:{}\n'.format(i, params[i])
        text = text[:-1]
        self.__args.setPlainText(text)
        self.statusBar().showMessage('Argüman listesi orjinal hale geri getirildi.')

    def __is_int(self, value):
        try:
            i = int(value)
            return True
        except:
            return False

    def __is_float(self, value):
        try:
            i = float(value)
            return True
        except:
            return False

    def set_args(self):
        params = {}
        paramsText = self.__args.toPlainText()
        try:
            for i in paramsText.split('\n'):
                if ':' in i:
                    indexi = i.index(':')
                    p1 = i[:indexi]
                    p2 = i[indexi + 1:]
                    if p2 == 'None':
                        params[p1] = None
                    elif self.__is_int(p2) == True:
                        params[p1] = int(p2)
                    elif self.__is_float(p2) == True:
                        params[p1] = float(p2)
                    elif p2 == 'True':
                        params[p1] = True
                    elif p2 == 'False':
                        params[p1] = False
                    else:
                        params[p1] = p2
            self.__classifier.set_params(**params)
            self.__progressbar.setMaximum(int(self.__rcount.text()))
            self.statusBar().showMessage('Argüman listesi başarıyla aktarıldı.')

        except:
            self.statusBar().showMessage('Parametre aktarımında hata.')
            print(sys.exc_info())

    def saveActionClicked(self):
        try:
            self.__result.saveList(title='Sonuç olarak kaydet',
                                  extention='res',
                                  explain='Sonuç dosyası',
                                  directory='./thesis/')
            self.statusBar().showMessage('Sonuç dosyası olarak kaydedildi.')
        except:
            self.statusBar().showMessage('Kaydetme işlemi esnasında hata')

    def sourceClicked(self):
        dialog = QFileDialog()
        dialog.setDefaultSuffix('sca')
        dialog.setAcceptMode(QFileDialog.AcceptOpen)
        dialog.setNameFilters(['Hesaplanmış nitelik dosyası (*.sca)'])
        dialog.setDirectory('./')
        try:
            if dialog.exec_() == QFileDialog.Accepted:
                fname = dialog.selectedFiles()[0]
                self.__source.setText(fname)
                self.__dfSca = pd.read_csv(fname)
                fname = list(self.__dfSca['Kaynak'].values)[0]
                self.__dfSaf = pd.read_csv(fname)
                fname = self.__dfSaf['Kaynak'].values[0]
                self.__dfSbf = pd.read_csv(fname)
                self.statusBar().showMessage('Makina öğrenme algoritmasının uygulaması için şu an hazır.')
        except:
            print(sys.exc_info())

    def accValues(self, cm):
        tn, fp, fn, tp = cm.ravel()
        if (tn + fp + fn + tp) != 0:
            c1 = (tp + tn) / (tn + fp + fn + tp)
        else:
            c1 = 0
        return c1

    def mccValues(self, cm):
        tn, fp, fn, tp = cm.ravel()
        p1 = (tp * tn) - (fp * fn)
        p2 = np.sqrt(
            (tp + fp) *
            (tp + fn) *
            (tn + fp) *
            (tn + fn)
        )
        return p1 / p2

    def senValues(self, cm):
        tn, fp, fn, tp = cm.ravel()
        p1 = tp
        p2 = tp + fn
        if p2 != 0:
            return p1 / p2
        else:
            return 0

    def speValues(self, cm):
        tn, fp, fn, tp = cm.ravel()
        p1 = tn
        p2 = tn + fp
        if p2 != 0:
            return p1 / p2
        else:
            return 0

    def f1Values(self, cm):
        tn, fp, fn, tp = cm.ravel()
        if tp + fn != 0:
            recall1 = tp / (tp + fn)
        else:
            recall1 = 0
        if tp + fp != 0:
            precision1 = tp / (tp + fp)
        else:
            precision1 = 0
        if recall1 + precision1 != 0:
            return 2 * (recall1 * precision1) / (recall1 + precision1)
        else:
            return 0

    def ppvValues(self, cm):
        tn, fp, fn, tp = cm.ravel()
        p1 = tp
        p2 = tp + fp
        if p2 != 0:
            return p1 / p2
        else:
            return 0

    def npvValues(self, cm):
        tn, fp, fn, tp = cm.ravel()
        p1 = tn
        p2 = tn + fn
        if p2 != 0:
            return p1 / p2
        else:
            return 0

    def fmiValues(self, cm):
        return np.sqrt(self.senValues(cm) * self.ppvValues(cm))

    def fit_ml(self):
        classes = ['Erkek','Kadın']
        self.__dfSca = self.__dfSca.sample(frac=1)
        all_labels = list(self.__dfSca.keys()[7:])
        rcount = int(self.__rcount.text())
        self.__progressbar.setMaximum(len(all_labels))
        for k in range(len(all_labels), 1 , -1):
            self.__progressbar.setValue(k+1)
            labels = list(itertools.combinations(all_labels, k))
            self.__progressbar2.setMaximum(len(labels))
            max_mcc = -1
            res_label = None
            res_predict = None
            self.statusBar().showMessage('{} parametreli tesler başladı.'.format(k))
            scores = []
            for indexL, label in enumerate(labels):
                self.__progressbar2.setValue(indexL+1)
                parameters = list(label)
                X = self.__dfSca[parameters].values
                y = self.__dfSca['Cinsiyet'].values
                # ----------------------------------
                k_fold = rcount
                kf = KFold(n_splits=k_fold)
                fold = 1
                foldResults = []
                for train_index, test_index in kf.split(X):
                    X_train, X_test = X[train_index], X[test_index]
                    y_train, y_test = y[train_index], y[test_index]
                    self.__classifier.fit(X_train, y_train)
                    predict = self.__classifier.predict(X_test)
                    mlcm = multilabel_confusion_matrix(y_test, predict, labels=classes)
                    for indecm, cm in enumerate(mlcm):
                        tn, fp, fn, tp = cm.ravel()
                        foldResults.append((fold, classes[indecm], self.accValues(cm),
                                            self.mccValues(cm),
                                            self.senValues(cm),
                                            self.speValues(cm),
                                            self.f1Values(cm),
                                            self.ppvValues(cm),
                                            self.npvValues(cm),
                                            self.fmiValues(cm), tn, fp, fn, tp
                                            ))
                    fold = fold + 1
                QApplication.processEvents()
                df4 = pd.DataFrame(foldResults,
                                   columns=['Fold', 'Sınıf', 'Acc', 'Mcc', 'Sen', 'Spe', 'F1', 'Ppv', 'Npv', 'Fmi',
                                            'TN', 'FP', 'FN', 'TP'])
                mean_mcc = np.mean(df4['Mcc'])
                if mean_mcc > max_mcc:
                    max_mcc = mean_mcc
                    res_predict = df4
                    res_label = parameters
            endOfResult = []
            for c in classes:
                roi = res_predict[(df4['Sınıf'] == c)]
                temp = []
                for m in ['Acc', 'Mcc', 'Sen', 'Spe', 'F1', 'Ppv', 'Npv', 'Fmi', 'TN', 'FP', 'FN', 'TP']:
                    mean = np.mean(roi[m].values)
                    std = np.std(roi[m].values)
                    temp.append('{0:.2f}±{1:.2f}'.format(mean, std))
                temp.insert(0, c)
                temp.insert(len(temp), ','.join(res_label))
                temp.insert(len(temp), k)
                temp.insert(len(temp), self.__progressbar2.maximum())
                endOfResult.append(temp)
            df5 = pd.DataFrame(endOfResult,
                               columns=['Sınıf', 'Acc', 'Mcc', 'Sen', 'Spe', 'F1', 'Ppv', 'Npv', 'Fmi', 'TN', 'FP',
                                        'FN', 'TP','Parametreler','Parametre sayısı','İncelenen model'])
            for data in df5.values:
                self.__result.addRow(list(data))
        self.statusBar().showMessage('İşlemler tamamlandı. Sonuçlarınızı kaydediniz.')
        self.__progressbar.setValue(0)
        self.__progressbar2.setValue(0)

    def runActionClicked(self):
        if self.__source.text() != '<Dosya seçiniz>':
            try:
                self.set_args()
                self.fit_ml()
            except:
                print(sys.exc_info())
        else:
            self.statusBar().showMessage('Kaynak ismi boş olamaz.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SolverForDT()
    ex.show()
    sys.exit(app.exec_())