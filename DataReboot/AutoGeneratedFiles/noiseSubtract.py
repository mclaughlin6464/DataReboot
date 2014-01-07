# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiFiles\noiseSubtract.ui'
#
# Created: Fri Jul 19 15:22:39 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_noiseSubtract(object):
    def setupUi(self, noiseSubtract):
        noiseSubtract.setObjectName(_fromUtf8("noiseSubtract"))
        noiseSubtract.setWindowModality(QtCore.Qt.ApplicationModal)
        noiseSubtract.resize(562, 378)
        self.gridLayout = QtGui.QGridLayout(noiseSubtract)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(noiseSubtract)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.combo_noiseSubtractObj = QtGui.QComboBox(noiseSubtract)
        self.combo_noiseSubtractObj.setObjectName(_fromUtf8("combo_noiseSubtractObj"))
        self.horizontalLayout.addWidget(self.combo_noiseSubtractObj)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(noiseSubtract)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(noiseSubtract)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.edit_start = QtGui.QLineEdit(noiseSubtract)
        self.edit_start.setObjectName(_fromUtf8("edit_start"))
        self.horizontalLayout_2.addWidget(self.edit_start)
        self.combo_startUnit = QtGui.QComboBox(noiseSubtract)
        self.combo_startUnit.setObjectName(_fromUtf8("combo_startUnit"))
        self.horizontalLayout_2.addWidget(self.combo_startUnit)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(noiseSubtract)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.edit_stop = QtGui.QLineEdit(noiseSubtract)
        self.edit_stop.setObjectName(_fromUtf8("edit_stop"))
        self.horizontalLayout_3.addWidget(self.edit_stop)
        self.combo_stopUnit = QtGui.QComboBox(noiseSubtract)
        self.combo_stopUnit.setObjectName(_fromUtf8("combo_stopUnit"))
        self.horizontalLayout_3.addWidget(self.combo_stopUnit)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.horizontalLayout_7, 1, 0, 1, 1)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_4 = QtGui.QLabel(noiseSubtract)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_5.addWidget(self.label_4)
        self.edit_points = QtGui.QLineEdit(noiseSubtract)
        self.edit_points.setObjectName(_fromUtf8("edit_points"))
        self.horizontalLayout_5.addWidget(self.edit_points)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_5 = QtGui.QLabel(noiseSubtract)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_4.addWidget(self.label_5)
        self.edit_stepSize = QtGui.QLineEdit(noiseSubtract)
        self.edit_stepSize.setObjectName(_fromUtf8("edit_stepSize"))
        self.horizontalLayout_4.addWidget(self.edit_stepSize)
        self.combo_stepSize = QtGui.QComboBox(noiseSubtract)
        self.combo_stepSize.setObjectName(_fromUtf8("combo_stepSize"))
        self.horizontalLayout_4.addWidget(self.combo_stepSize)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.horizontalLayout_8, 2, 0, 1, 1)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.button_takeSpectrum = QtGui.QPushButton(noiseSubtract)
        self.button_takeSpectrum.setEnabled(False)
        self.button_takeSpectrum.setObjectName(_fromUtf8("button_takeSpectrum"))
        self.horizontalLayout_6.addWidget(self.button_takeSpectrum)
        self.button_cancel = QtGui.QPushButton(noiseSubtract)
        self.button_cancel.setObjectName(_fromUtf8("button_cancel"))
        self.horizontalLayout_6.addWidget(self.button_cancel)
        self.gridLayout.addLayout(self.horizontalLayout_6, 3, 0, 1, 1)

        self.retranslateUi(noiseSubtract)
        QtCore.QObject.connect(self.button_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), noiseSubtract.close)
        QtCore.QObject.connect(self.combo_startUnit, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.combo_stopUnit.setCurrentIndex)
        QtCore.QObject.connect(self.combo_startUnit, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.combo_stepSize.setCurrentIndex)
        QtCore.QObject.connect(self.combo_stopUnit, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.combo_startUnit.setCurrentIndex)
        QtCore.QObject.connect(self.combo_stopUnit, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), self.combo_stepSize.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(noiseSubtract)

    def retranslateUi(self, noiseSubtract):
        noiseSubtract.setWindowTitle(_translate("noiseSubtract", "Take New Noise Subtract", None))
        self.label.setText(_translate("noiseSubtract", "Noise Subtract Object", None))
        self.label_2.setText(_translate("noiseSubtract", "Start", None))
        self.label_3.setText(_translate("noiseSubtract", "Stop", None))
        self.label_4.setText(_translate("noiseSubtract", "Points", None))
        self.label_5.setText(_translate("noiseSubtract", "Step Size", None))
        self.button_takeSpectrum.setText(_translate("noiseSubtract", "Take Spectrum", None))
        self.button_cancel.setText(_translate("noiseSubtract", "Cancel", None))

