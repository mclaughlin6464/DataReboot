# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiFiles\INSTconfig_window_add.ui'
#
# Created: Thu Jul 11 09:34:14 2013
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.combo_name = QtGui.QComboBox(Form)
        self.combo_name.setObjectName(_fromUtf8("combo_name"))
        self.horizontalLayout.addWidget(self.combo_name)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.edit_resAd = QtGui.QLineEdit(Form)
        self.edit_resAd.setObjectName(_fromUtf8("edit_resAd"))
        self.horizontalLayout_2.addWidget(self.edit_resAd)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.text_display = QtGui.QTextBrowser(Form)
        self.text_display.setEnabled(False)
        self.text_display.setObjectName(_fromUtf8("text_display"))
        self.verticalLayout.addWidget(self.text_display)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.button_add = QtGui.QPushButton(Form)
        self.button_add.setObjectName(_fromUtf8("button_add"))
        self.verticalLayout_2.addWidget(self.button_add)
        self.button_cancel = QtGui.QPushButton(Form)
        self.button_cancel.setObjectName(_fromUtf8("button_cancel"))
        self.verticalLayout_2.addWidget(self.button_cancel)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.button_cancel, QtCore.SIGNAL(_fromUtf8("clicked()")), Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "INST Add", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Reource Address", None, QtGui.QApplication.UnicodeUTF8))
        self.button_add.setText(QtGui.QApplication.translate("Form", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.button_cancel.setText(QtGui.QApplication.translate("Form", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

