from find_logic import FindMemory
from gui.replace_gui import Ui_Replace

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QDialog, QMessageBox


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

    def find_button_pressed(self):
        self.find_text()

    def find_text(self):
        file_text = self.parent.ui.textField.toPlainText()
        query_text = self.ui.find_what_lineedit.text()

        if self.ui.match_case_checkbox.isChecked():
            result = file_text.find(query_text, self.start_index)
        else:
            result = file_text.lower().find(query_text.lower(), self.start_index)

        self.start_index = result + 1

        # Not found, if empty:
        if len(file_text) == 0:
            FindMemory.not_found(query_text)

        # Not found:
        elif result == -1:
            # Wrap around - only once automatically
            if self.ui.wrap_around_checkbox.isChecked() and self.auto_wrap_count < 1:
                self.start_index = 0
                self.auto_wrap_count += 1  # count the cycle to prevent infinite recursion
                self.find_text()  # call only once again recursively

            # Do not wrap around:
            # either wrapping is set to off, or there are NO results in WHOLE text
            else:
                self.not_found(query_text)

        # Found a record:
        else:
            new_cursor = self.parent.ui.textField.textCursor()
            new_cursor.setPosition(result)
            new_cursor.setPosition(result + len(query_text), QTextCursor.KeepAnchor)

            self.parent.ui.textField.setTextCursor(new_cursor)
            self.parent.query_text = query_text
