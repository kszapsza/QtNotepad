# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'replace.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Replace(object):
    def setupUi(self, Replace):
        Replace.setObjectName("Replace")
        Replace.setWindowModality(QtCore.Qt.WindowModal)
        Replace.resize(400, 149)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Replace.sizePolicy().hasHeightForWidth())
        Replace.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Replace)
        self.gridLayout.setObjectName("gridLayout")
        self.checks_and_radios_layout = QtWidgets.QHBoxLayout()
        self.checks_and_radios_layout.setObjectName("checks_and_radios_layout")
        self.checkbox_layout = QtWidgets.QVBoxLayout()
        self.checkbox_layout.setObjectName("checkbox_layout")
        self.match_case_checkbox = QtWidgets.QCheckBox(Replace)
        self.match_case_checkbox.setObjectName("match_case_checkbox")
        self.checkbox_layout.addWidget(self.match_case_checkbox)
        self.wrap_around_checkbox = QtWidgets.QCheckBox(Replace)
        self.wrap_around_checkbox.setObjectName("wrap_around_checkbox")
        self.checkbox_layout.addWidget(self.wrap_around_checkbox)
        self.checks_and_radios_layout.addLayout(self.checkbox_layout)
        self.gridLayout.addLayout(self.checks_and_radios_layout, 4, 0, 3, 1)
        self.find_button = QtWidgets.QPushButton(Replace)
        self.find_button.setObjectName("find_button")
        self.gridLayout.addWidget(self.find_button, 0, 1, 1, 1)
        self.replace_button = QtWidgets.QPushButton(Replace)
        self.replace_button.setObjectName("replace_button")
        self.gridLayout.addWidget(self.replace_button, 1, 1, 1, 1)
        self.replace_all_button = QtWidgets.QPushButton(Replace)
        self.replace_all_button.setObjectName("replace_all_button")
        self.gridLayout.addWidget(self.replace_all_button, 2, 1, 1, 1)
        self.cancel_button = QtWidgets.QPushButton(Replace)
        self.cancel_button.setObjectName("cancel_button")
        self.gridLayout.addWidget(self.cancel_button, 4, 1, 1, 1)
        self.replace_form_layout = QtWidgets.QGridLayout()
        self.replace_form_layout.setObjectName("replace_form_layout")
        self.find_what_label = QtWidgets.QLabel(Replace)
        self.find_what_label.setObjectName("find_what_label")
        self.replace_form_layout.addWidget(self.find_what_label, 0, 0, 1, 1)
        self.replace_with_label = QtWidgets.QLabel(Replace)
        self.replace_with_label.setObjectName("replace_with_label")
        self.replace_form_layout.addWidget(self.replace_with_label, 1, 0, 1, 1)
        self.find_what_lineedit = QtWidgets.QLineEdit(Replace)
        self.find_what_lineedit.setObjectName("find_what_lineedit")
        self.replace_form_layout.addWidget(self.find_what_lineedit, 0, 1, 1, 1)
        self.replace_with_lineedit = QtWidgets.QLineEdit(Replace)
        self.replace_with_lineedit.setObjectName("replace_with_lineedit")
        self.replace_form_layout.addWidget(self.replace_with_lineedit, 1, 1, 1, 1)
        self.gridLayout.addLayout(self.replace_form_layout, 0, 0, 2, 1)

        self.retranslateUi(Replace)
        QtCore.QMetaObject.connectSlotsByName(Replace)

    def retranslateUi(self, Replace):
        _translate = QtCore.QCoreApplication.translate
        Replace.setWindowTitle(_translate("Replace", "Replace"))
        self.match_case_checkbox.setText(_translate("Replace", "Match case"))
        self.wrap_around_checkbox.setText(_translate("Replace", "Wrap around"))
        self.find_button.setText(_translate("Replace", "Find Next"))
        self.replace_button.setText(_translate("Replace", "Replace"))
        self.replace_all_button.setText(_translate("Replace", "Replace All"))
        self.cancel_button.setText(_translate("Replace", "Cancel"))
        self.find_what_label.setText(_translate("Replace", "Find what:"))
        self.replace_with_label.setText(_translate("Replace", "Replace with:"))
