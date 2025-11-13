import pydicom
import os
import numpy as np
from enum import Enum


class Dose(Enum):
    LUNG = (-500, 1500)
    BONE = (300, 2000)
    SOFT_TISSUE = (40, 400)
    ABDOMEN = (50, 250)
    BRAIN = (50, 150)
    SPINE = (40, 400)
    VERTEBRAE = (530, 2300)
    LIVER = (80, 150)
    SINUS = (400, 4000)
    MEDIASTINUM = (50, 350)
    AUTO = (0, 0)
    MKT = (-650, 250)


class Dicom:

    @staticmethod
    def read(file):
        return pydicom.read_file(file)

    def reads(path, callback=None):
        slices = []
        files = os.listdir(path)
        if callback != None:
            callback.setMaximum(len(files))
        for index, s in enumerate(files):
            slices.append(pydicom.read_file(path + '/' + s))
            if callback != None:
                callback.setValue(index)
                callback.repaint()
        if callback != None:
            callback.setValue(0)
        slices.sort(key=lambda x: int(x.InstanceNumber))
        try:
            slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
        except:
            slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
        for s in slices:
            s.SliceThickness = slice_thickness
        return slices

    @staticmethod
    def windowed_slice(slice, window=Dose.LUNG):
        slope = float(slice[0x0028, 0x1053].value)
        intercept = float(slice[0x0028, 0x1052].value)
        hu = slice.pixel_array * slope + intercept
        center, level = window.value
        low = center - level / 2
        high = center + level / 2
        windowedHuImage = np.copy(hu)
        windowedHuImage[windowedHuImage <= low] = low
        windowedHuImage[windowedHuImage > high] = high
        return windowedHuImage