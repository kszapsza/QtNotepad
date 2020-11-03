from gui.replace_gui import Ui_Replace

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog


class Replace(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.ui = Ui_Replace()
        self.ui.setupUi(self)

        self.dialog_icon = QIcon('.\\icon.png')
        self.setWindowIcon(self.dialog_icon)

        self.setWindowModality(QtCore.Qt.NonModal)
        self.setFixedSize(self.width(), self.height())

        # noinspection PyTypeChecker
        self.setWindowFlags(self.windowFlags() & (
                QtCore.Qt.Tool
                | QtCore.Qt.FramelessWindowHint
                | QtCore.Qt.WindowStaysOnTopHint
                | ~QtCore.Qt.WindowContextHelpButtonHint))

        self.ui.wrap_around_checkbox.setChecked(True)
        self.ui.find_what_lineedit.setFocus(True)

        self.find_text_changed()
        self.replace_text_changed()

        self.ui.find_what_lineedit.textChanged.connect(lambda: self.find_text_changed())
        self.ui.replace_with_lineedit.textChanged.connect(lambda: self.replace_text_changed())

    def find_text_changed(self):
        if len(self.ui.find_what_lineedit.text()) == 0:
            self.ui.find_button.setDisabled(True)
            self.ui.replace_button.setDisabled(True)
            self.ui.replace_all_button.setDisabled(True)
        else:
            self.ui.find_button.setDisabled(False)
            if len(self.ui.replace_with_lineedit.text()) != 0:
                self.ui.replace_button.setDisabled(False)
                self.ui.replace_all_button.setDisabled(False)

    def replace_text_changed(self):
        if len(self.ui.replace_with_lineedit.text()) == 0:
            self.ui.replace_button.setDisabled(True)
            self.ui.replace_all_button.setDisabled(True)
        else:
            if len(self.ui.find_what_lineedit.text()) != 0:
                self.ui.replace_button.setDisabled(False)
                self.ui.replace_all_button.setDisabled(False)
