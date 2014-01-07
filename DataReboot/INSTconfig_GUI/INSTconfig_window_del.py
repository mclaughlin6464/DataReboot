# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiFiles\INSTconfig_window_del.ui'
#
# Created: Thu Jul 11 09:34:27 2013
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_window_del(object):
    def setupUi(self, window_del):
        window_del.setObjectName(_fromUtf8("window_del"))
        window_del.setWindowModality(QtCore.Qt.ApplicationModal)
        window_del.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(window_del)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(window_del)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.combo_name = QtGui.QComboBox(window_del)
        self.combo_name.setObjectName(_fromUtf8("combo_name"))
        self.horizontalLayout.addWidget(self.combo_name)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.text_display = QtGui.QTextBrowser(window_del)
        self.text_display.setObjectName(_fromUtf8("text_display"))
        self.verticalLayout_2.addWidget(self.text_display)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.button_del = QtGui.QPushButton(window_del)
        self.button_del.setObjectName(_fromUtf8("button_del"))
        self.verticalLayout.addWidget(self.button_del)
        self.button_cancel = QtGui.QPushButton(window_del)
        self.button_cancel.setObjectName(_fromUtf8("button_cancel"))
        self.verticalLayout.addWidget(self.button_cancel)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.retranslateUi(window_del)
        QtCore.QObject.connect(self.button_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), window_del.close)
        QtCore.QMetaObject.connectSlotsByName(window_del)

    def retranslateUi(self, window_del):
        window_del.setWindowTitle(QtGui.QApplication.translate("window_del", "INST Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("window_del", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.button_del.setText(QtGui.QApplication.translate("window_del", "Delete", None, QtGui.QApplication.UnicodeUTF8))
        self.button_cancel.setText(QtGui.QApplication.translate("window_del", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

