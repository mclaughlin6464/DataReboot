# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiFiles\MainWindow.ui'
#
# Created: Thu Jul 25 11:21:57 2013
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(MainWindow)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.button_measurement = QtGui.QPushButton(MainWindow)
        self.button_measurement.setMinimumSize(QtCore.QSize(0, 75))
        self.button_measurement.setObjectName(_fromUtf8("button_measurement"))
        self.horizontalLayout_2.addWidget(self.button_measurement)
        self.button_analysis = QtGui.QPushButton(MainWindow)
        self.button_analysis.setMinimumSize(QtCore.QSize(0, 75))
        self.button_analysis.setObjectName(_fromUtf8("button_analysis"))
        self.horizontalLayout_2.addWidget(self.button_analysis)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line = QtGui.QFrame(MainWindow)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.button_GAS = QtGui.QPushButton(MainWindow)
        self.button_GAS.setMinimumSize(QtCore.QSize(0, 50))
        self.button_GAS.setObjectName(_fromUtf8("button_GAS"))
        self.horizontalLayout.addWidget(self.button_GAS)
        self.button_INST = QtGui.QPushButton(MainWindow)
        self.button_INST.setMinimumSize(QtCore.QSize(0, 50))
        self.button_INST.setObjectName(_fromUtf8("button_INST"))
        self.horizontalLayout.addWidget(self.button_INST)
        self.button_presets = QtGui.QPushButton(MainWindow)
        self.button_presets.setMinimumSize(QtCore.QSize(0, 50))
        self.button_presets.setObjectName(_fromUtf8("button_presets"))
        self.horizontalLayout.addWidget(self.button_presets)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Main Window", None))
        self.button_measurement.setText(_translate("MainWindow", "Measurement", None))
        self.button_analysis.setText(_translate("MainWindow", "Analysis", None))
        self.button_GAS.setText(_translate("MainWindow", "GAS Config", None))
        self.button_INST.setText(_translate("MainWindow", "INST Config", None))
        self.button_presets.setText(_translate("MainWindow", "Presets Config", None))

