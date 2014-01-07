# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uiFiles/INSTconfig_GUI.ui'
#
# Created: Mon Jul 01 16:07:35 2013
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_window_INST(object):
    def setupUi(self, window_INST):
        window_INST.setObjectName(_fromUtf8("window_INST"))
        window_INST.resize(499, 350)
        window_INST.setMaximumSize(QtCore.QSize(499, 350))
        self.centralwidget = QtGui.QWidget(window_INST)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_6.addWidget(self.label_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.edit_INSTconfig = QtGui.QLineEdit(self.centralwidget)
        self.edit_INSTconfig.setEnabled(True)
        self.edit_INSTconfig.setObjectName(_fromUtf8("edit_INSTconfig"))
        self.horizontalLayout_4.addWidget(self.edit_INSTconfig)
        self.button_INSTconfig = QtGui.QPushButton(self.centralwidget)
        self.button_INSTconfig.setEnabled(True)
        self.button_INSTconfig.setObjectName(_fromUtf8("button_INSTconfig"))
        self.horizontalLayout_4.addWidget(self.button_INSTconfig)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)
        self.gridLayout_2.addLayout(self.horizontalLayout_6, 0, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.combo_INST = QtGui.QComboBox(self.centralwidget)
        self.combo_INST.setEnabled(False)
        self.combo_INST.setObjectName(_fromUtf8("combo_INST"))
        self.horizontalLayout_2.addWidget(self.combo_INST)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.text_display = QtGui.QTextBrowser(self.centralwidget)
        self.text_display.setEnabled(False)
        self.text_display.setObjectName(_fromUtf8("text_display"))
        self.verticalLayout_2.addWidget(self.text_display)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.verticalLayout.addWidget(self.line_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.button_add = QtGui.QPushButton(self.centralwidget)
        self.button_add.setEnabled(False)
        self.button_add.setObjectName(_fromUtf8("button_add"))
        self.horizontalLayout.addWidget(self.button_add)
        self.button_edit = QtGui.QPushButton(self.centralwidget)
        self.button_edit.setEnabled(False)
        self.button_edit.setObjectName(_fromUtf8("button_edit"))
        self.horizontalLayout.addWidget(self.button_edit)
        self.button_del = QtGui.QPushButton(self.centralwidget)
        self.button_del.setEnabled(False)
        self.button_del.setObjectName(_fromUtf8("button_del"))
        self.horizontalLayout.addWidget(self.button_del)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)
        window_INST.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(window_INST)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 499, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        window_INST.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(window_INST)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        window_INST.setStatusBar(self.statusbar)

        self.retranslateUi(window_INST)
        QtCore.QMetaObject.connectSlotsByName(window_INST)

    def retranslateUi(self, window_INST):
        window_INST.setWindowTitle(QtGui.QApplication.translate("window_INST", "INST config", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("window_INST", "Instrument Config File", None, QtGui.QApplication.UnicodeUTF8))
        self.button_INSTconfig.setText(QtGui.QApplication.translate("window_INST", "Open", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("window_INST", "INST Objects", None, QtGui.QApplication.UnicodeUTF8))
        self.button_add.setText(QtGui.QApplication.translate("window_INST", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.button_edit.setText(QtGui.QApplication.translate("window_INST", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.button_del.setText(QtGui.QApplication.translate("window_INST", "Delete", None, QtGui.QApplication.UnicodeUTF8))

