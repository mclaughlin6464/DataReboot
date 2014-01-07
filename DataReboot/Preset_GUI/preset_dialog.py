# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiFiles\preset_dialog_2.ui'
#
# Created: Mon Jul 29 10:46:56 2013
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

class Ui_presetDialog(object):
    def setupUi(self, presetDialog):
        presetDialog.setObjectName(_fromUtf8("presetDialog"))
        presetDialog.resize(400, 165)
        presetDialog.setMinimumSize(QtCore.QSize(400, 165))
        presetDialog.setMaximumSize(QtCore.QSize(400, 165))
        presetDialog.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(presetDialog)
        self.buttonBox.setGeometry(QtCore.QRect(40, 130, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.layoutWidget = QtGui.QWidget(presetDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 101))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.combo_preset = QtGui.QComboBox(self.layoutWidget)
        self.combo_preset.setObjectName(_fromUtf8("combo_preset"))
        self.verticalLayout.addWidget(self.combo_preset)

        self.retranslateUi(presetDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), presetDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), presetDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(presetDialog)

    def retranslateUi(self, presetDialog):
        presetDialog.setWindowTitle(_translate("presetDialog", "Preset", None))
        self.label.setText(_translate("presetDialog", "Please select which preset you would like.", None))

