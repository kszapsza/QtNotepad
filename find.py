from find_logic import FindMemory
from gui.find_gui import Ui_Find

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QTextCursor, QCloseEvent
from PyQt5.QtWidgets import QDialog, QMessageBox


# Edit > Find...QDialog class.
class Find(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.ui = Ui_Find()
        self.ui.setupUi(self)

        self.setWindowIcon(self.parent.notepad_icon)

        self.start_index = 0
        self.rfind_end_index = -1

        # This stops the recursive call of Find after one cycle - when there are
        # no results. This flag is being reset when user manually presses Find button,
        # or when the query text has changed.
        self.auto_wrap_count = 0

        self.setWindowModality(QtCore.Qt.NonModal)
        self.setFixedSize(self.width(), self.height())

        # noinspection PyTypeChecker
        self.setWindowFlags(self.windowFlags() & (
                              QtCore.Qt.Tool
                            | QtCore.Qt.FramelessWindowHint
                            | QtCore.Qt.WindowStaysOnTopHint
                            | ~QtCore.Qt.WindowContextHelpButtonHint))

        self.ui.find_line_edit.setText(self.parent.find_memory.query_text)
        self.ui.wrap_around_checkbox.setChecked(self.parent.find_memory.wrap_around)
        self.ui.down_radio.setChecked(True)

        self.ui.find_button.released.connect(lambda: self.find_next_pressed())
        self.ui.cancel_button.released.connect(lambda: self.close())

        self.ui.find_button.setDisabled(not bool(len(self.ui.find_line_edit.text())))
        self.ui.find_line_edit.textChanged.connect(lambda: self.text_changed())
        self.ui.find_line_edit.setFocus()

    # Stores last search data in FindMemory obj:
    def closeEvent(self, event: QCloseEvent):
        self.parent.find_memory.query_text = self.ui.find_line_edit.text()
        self.parent.find_memory.wrap_around = self.ui.wrap_around_checkbox.isChecked()
        self.parent.find_memory.start_index = self.start_index

    def text_changed(self):
        self.auto_wrap_count = 0
        self.rfind_end_index = -1

        if len(self.ui.find_line_edit.text()) == 0:
            self.ui.find_button.setDisabled(True)
            self.start_index = 0  # reset find index data when new query was given
        else:
            self.ui.find_button.setEnabled(True)

    def find_next_pressed(self):
        self.auto_wrap_count = 0
        self.find_text()

    def find_text(self):
        file_text = self.parent.ui.textField.toPlainText()
        query_text = self.ui.find_line_edit.text()

        # Set reversed find begin index, if it was -1 (undefined).
        if self.rfind_end_index == -1:
            self.rfind_end_index = len(file_text)

        # Find direction: down
        if self.ui.down_radio.isChecked():
            if self.ui.match_case_checkbox.isChecked():
                result = file_text.find(query_text, self.start_index)
            else:
                result = file_text.lower().find(query_text.lower(), self.start_index)

            self.start_index = result + 1

        # Find direction: up
        else:
            if self.ui.match_case_checkbox.isChecked():
                result = file_text.rfind(query_text, 0, self.rfind_end_index)
            else:
                result = file_text.lower().rfind(query_text.lower(), 0, self.rfind_end_index)

            self.rfind_end_index = result

        # Not found:
        if result == -1:
            # Wrap around - only once automatically
            if self.ui.wrap_around_checkbox.isChecked() and self.auto_wrap_count < 1:
                self.start_index = 0
                self.rfind_end_index = len(file_text)
                self.auto_wrap_count += 1  # count the cycle to prevent infinite recursion
                self.find_text()  # call only once again recursively

            # Do not wrap around:
            # either wrapping is set to off, or there are NO results in WHOLE text
            else:
                self.start_index = len(file_text) + 1
                self.rfind_end_index = 0
                FindMemory.not_found(self, query_text)

        # Found a record:
        else:
            new_cursor = self.parent.ui.textField.textCursor()
            new_cursor.setPosition(result)
            new_cursor.setPosition(result + len(query_text), QTextCursor.KeepAnchor)

            self.parent.ui.textField.setTextCursor(new_cursor)
            self.parent.query_text = query_text
