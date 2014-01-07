# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiFiles\calibrateBfield.ui'
#
# Created: Fri Jul 19 10:18:23 2013
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

class Ui_widget_calibrateBField(object):
    def setupUi(self, widget_calibrateBField):
        widget_calibrateBField.setObjectName(_fromUtf8("widget_calibrateBField"))
        widget_calibrateBField.setWindowModality(QtCore.Qt.ApplicationModal)
        widget_calibrateBField.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(widget_calibrateBField)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(widget_calibrateBField)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.combo_getBField = QtGui.QComboBox(widget_calibrateBField)
        self.combo_getBField.setObjectName(_fromUtf8("combo_getBField"))
        self.horizontalLayout.addWidget(self.combo_getBField)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(widget_calibrateBField)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.combo_setBField = QtGui.QComboBox(widget_calibrateBField)
        self.combo_setBField.setObjectName(_fromUtf8("combo_setBField"))
        self.horizontalLayout_2.addWidget(self.combo_setBField)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_3 = QtGui.QLabel(widget_calibrateBField)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_3.addWidget(self.label_3)
        self.edit_calibration = QtGui.QLineEdit(widget_calibrateBField)
        self.edit_calibration.setObjectName(_fromUtf8("edit_calibration"))
        self.horizontalLayout_3.addWidget(self.edit_calibration)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 2)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.button_calibrate = QtGui.QPushButton(widget_calibrateBField)
        self.button_calibrate.setObjectName(_fromUtf8("button_calibrate"))
        self.horizontalLayout_4.addWidget(self.button_calibrate)
        self.button_confirm = QtGui.QPushButton(widget_calibrateBField)
        self.button_confirm.setObjectName(_fromUtf8("button_confirm"))
        self.horizontalLayout_4.addWidget(self.button_confirm)
        self.button_cancel = QtGui.QPushButton(widget_calibrateBField)
        self.button_cancel.setObjectName(_fromUtf8("button_cancel"))
        self.horizontalLayout_4.addWidget(self.button_cancel)
        self.gridLayout.addLayout(self.horizontalLayout_4, 2, 0, 1, 2)

        self.retranslateUi(widget_calibrateBField)
        QtCore.QObject.connect(self.button_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), widget_calibrateBField.close)
        QtCore.QMetaObject.connectSlotsByName(widget_calibrateBField)

    def retranslateUi(self, widget_calibrateBField):
        widget_calibrateBField.setWindowTitle(_translate("widget_calibrateBField", "Calibrate B-Field", None))
        self.label.setText(_translate("widget_calibrateBField", "getBField", None))
        self.label_2.setText(_translate("widget_calibrateBField", "setBField", None))
        self.label_3.setText(_translate("widget_calibrateBField", "Calibration (T/V)", None))
        self.button_calibrate.setText(_translate("widget_calibrateBField", "Calibrate", None))
        self.button_confirm.setText(_translate("widget_calibrateBField", "Confirm", None))
        self.button_cancel.setText(_translate("widget_calibrateBField", "Cancel", None))

