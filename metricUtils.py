import numpy as np

class MultiLabelPerformanceMetrics:

    def __init__(self):
        pass

    def acc(self, mlcm):
        accs = []
        for cm in mlcm:
            tn, fp, fn, tp = cm.ravel()
            if (tn + fp + fn +tp) != 0:
                c1 = (tp + tn) / (tn + fp + fn +tp)
            else:
                c1 = 0
            accs.append(c1)
        return np.asarray(accs)

    def mcc(self, mlcm):
        mccs = []
        for cm in mlcm:
            tn, fp, fn, tp = cm.ravel()
            p1 = (tp * tn) - (fp * fn)
            p2 = np.sqrt(
                (tp + fp) *
                (tp + fn) *
                (tn + fp) *
                (tn + fn)
            )
            if p2 != 0:
                mccs.append(p1 / p2)
            else:
                mccs.append(0)
        return np.asarray(mccs)

    def sen(self, mlcm):
        sens = []
        for cm in mlcm:
            tn, fp, fn, tp = cm.ravel()
            p1 = tp
            p2 = tp + fn
            if p2 != 0:
                sens.append(p1 / p2)
            else:
                sens.append(0)
        return np.asarray(sens)

    def spe(self, mlcm):
        spes = []
        for cm in mlcm:
            tn, fp, fn, tp = cm.ravel()
            p1 = tn
            p2 = tn + fp
            if p2 != 0:
                spes.append(p1 / p2)
            else:
                spes.append(0)
        return np.asarray(spes)

    def f1(self, mlcm):
        f1s = []
        for cm in mlcm:
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
                f1s.append(2 * (recall1 * precision1) / (recall1 + precision1))
            else:
                f1s.append(0)
        return f1s