# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiFiles/microwaveAmp.ui'
#
# Created: Fri Aug 09 16:01:56 2013
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.combo_MSobj = QtGui.QComboBox(Form)
        self.combo_MSobj.setObjectName(_fromUtf8("combo_MSobj"))
        self.horizontalLayout.addWidget(self.combo_MSobj)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.edit_amp = QtGui.QLineEdit(Form)
        self.edit_amp.setObjectName(_fromUtf8("edit_amp"))
        self.horizontalLayout_2.addWidget(self.edit_amp)
        self.combo_unit = QtGui.QComboBox(Form)
        self.combo_unit.setObjectName(_fromUtf8("combo_unit"))
        self.combo_unit.addItem(_fromUtf8(""))
        self.combo_unit.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.combo_unit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.button_confirm = QtGui.QPushButton(Form)
        self.button_confirm.setObjectName(_fromUtf8("button_confirm"))
        self.horizontalLayout_3.addWidget(self.button_confirm)
        self.button_cancel = QtGui.QPushButton(Form)
        self.button_cancel.setObjectName(_fromUtf8("button_cancel"))
        self.horizontalLayout_3.addWidget(self.button_cancel)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.button_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Set Microwave Amplitude", None))
        self.label.setText(_translate("Form", "setMicrowaveSource Object", None))
        self.label_2.setText(_translate("Form", "Amplitude", None))
        self.combo_unit.setItemText(0, _translate("Form", "mV", None))
        self.combo_unit.setItemText(1, _translate("Form", "dBm", None))
        self.button_confirm.setText(_translate("Form", "Confirm", None))
        self.button_cancel.setText(_translate("Form", "Cancel", None))

