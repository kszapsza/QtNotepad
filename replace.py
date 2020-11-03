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
        self.parent.find_memory.cursor_position = 0

        # Replace only allows finding down, so let us set it first:
        self.parent.find_memory.direction = FindDirection.DOWN

        self.find_text_changed()
        self.replace_text_changed()

        self.ui.find_what_lineedit.textChanged.connect(lambda: self.find_text_changed())
        self.ui.replace_with_lineedit.textChanged.connect(lambda: self.replace_text_changed())

        self.ui.wrap_around_checkbox.toggled.connect(lambda: self.wrap_mode_changed())
        self.parent.find_memory.wrap_around = True
        self.ui.match_case_checkbox.toggled.connect(lambda: self.case_mode_changed())
        self.parent.find_memory.match_case = False

        self.ui.find_button.released.connect(lambda: self.find_button_pressed())
        self.ui.replace_button.released.connect(lambda: self.replace_button_pressed())
        self.ui.replace_all_button.released.connect(lambda: self.replace_all_button_pressed())
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
        self.parent.find_memory.wrap_around = self.ui.wrap_around_checkbox.isChecked()

    def case_mode_changed(self):
        self.parent.find_memory.match_case = self.ui.match_case_checkbox.isChecked()

    def find_button_pressed(self):
        self.parent.find_memory.auto_wrap_count = 0
        self.parent.find_memory.query_text = self.ui.find_what_lineedit.text()
        self.parent.find_memory.find()

    def replace_button_pressed(self):
        self.parent.find_memory.auto_wrap_count = 0
        self.parent.find_memory.query_text = self.ui.find_what_lineedit.text()

        curr_txt = self.parent.ui.textField.toPlainText()
        replace_txt = self.ui.replace_with_lineedit.text()
        #
        # query_len = len(self.parent.find_memory.query_text)
        # cursor_pos = self.parent.find_memory.cursor_position

        was_found = self.parent.find_memory.find()

        curr_cursor = self.parent.ui.textField.textCursor()
        curr_selection_start = curr_cursor.selectionStart()
        curr_selection_end = curr_cursor.selectionEnd()

        if was_found:
            if curr_selection_end >= len(curr_txt):
                new_txt = curr_txt[0:curr_selection_start] + replace_txt
            else:
                new_txt = curr_txt[0:curr_selection_start] + replace_txt + curr_txt[curr_selection_end:]

            self.parent.ui.textField.setPlainText(new_txt)

    def replace_all_button_pressed(self):
        pass
