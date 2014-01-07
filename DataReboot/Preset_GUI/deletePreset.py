# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiFiles\deletePreset.ui'
#
# Created: Tue Jul 30 11:22:02 2013
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

class Ui_deletePreset(object):
    def setupUi(self, deletePreset):
        deletePreset.setObjectName(_fromUtf8("deletePreset"))
        deletePreset.setWindowModality(QtCore.Qt.ApplicationModal)
        deletePreset.resize(400, 300)
        self.combo_preset = QtGui.QComboBox(deletePreset)
        self.combo_preset.setGeometry(QtCore.QRect(300, 40, 69, 22))
        self.combo_preset.setObjectName(_fromUtf8("combo_preset"))
        self.button_del = QtGui.QPushButton(deletePreset)
        self.button_del.setGeometry(QtCore.QRect(190, 260, 75, 23))
        self.button_del.setObjectName(_fromUtf8("button_del"))
        self.button_cancel = QtGui.QPushButton(deletePreset)
        self.button_cancel.setGeometry(QtCore.QRect(300, 260, 75, 23))
        self.button_cancel.setObjectName(_fromUtf8("button_cancel"))
        self.textBrowser = QtGui.QTextBrowser(deletePreset)
        self.textBrowser.setGeometry(QtCore.QRect(30, 40, 256, 192))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))

        self.retranslateUi(deletePreset)
        QtCore.QObject.connect(self.button_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), deletePreset.close)
        QtCore.QMetaObject.connectSlotsByName(deletePreset)

    def retranslateUi(self, deletePreset):
        deletePreset.setWindowTitle(_translate("deletePreset", "Delete Preset", None))
        self.button_del.setText(_translate("deletePreset", "Delete", None))
        self.button_cancel.setText(_translate("deletePreset", "Cancel", None))

