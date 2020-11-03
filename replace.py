from find_memory import FindDirection
from gui.replace_gui import Ui_Replace

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog


class Replace(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.ui = Ui_Replace()
        self.ui.setupUi(self)

        self.setWindowIcon(self.parent.notepad_icon)

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

        # Finding start point
        self.start_index = 0

        # Replace only allows finding down, so let us set it first:
        self.parent.find_memory.direction = FindDirection.DOWN

        self.find_text_changed()
        self.replace_text_changed()

        self.ui.find_what_lineedit.textChanged.connect(lambda: self.find_text_changed())
        self.ui.replace_with_lineedit.textChanged.connect(lambda: self.replace_text_changed())

        self.ui.wrap_around_checkbox.toggled.connect(lambda: self.wrap_mode_changed())
        self.parent.find_memory.wrap_around = True
        self.ui.match_case_checkbox.toggled.connect(lambda: self.case_mode_changed())

        self.ui.find_button.released.connect(lambda: self.find_button_pressed())
        self.ui.cancel_button.released.connect(lambda: self.close())

    def find_text_changed(self):
        self.parent.find_memory.query_text = self.ui.find_what_lineedit.text()

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

    def wrap_mode_changed(self):
        if self.ui.wrap_around_checkbox.isChecked():
            self.parent.find_memory.wrap_around = True
        else:
            self.parent.find_memory.wrap_around = False

    def case_mode_changed(self):
        if self.ui.match_case_checkbox.isChecked():
            self.parent.find_memory.match_case = True
        else:
            self.parent.find_memory.match_case = False

    def find_button_pressed(self):
        self.parent.find_memory.query_text = self.ui.find_what_lineedit.text()
        self.parent.find_memory.find()
