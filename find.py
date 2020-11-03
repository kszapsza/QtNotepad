from gui.find_gui import Ui_Find

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QDialog, QMessageBox


# Edit > Find...QDialog class.
class Find(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.ui = Ui_Find()
        self.ui.setupUi(self)

        self.dialog_icon = QIcon('.\\icon.png')
        self.setWindowIcon(self.dialog_icon)

        self.start_index = 0
        self.rfind_end_index = 0

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

        self.ui.down_radio.setChecked(True)
        self.ui.wrap_around_checkbox.setChecked(True)

        self.ui.find_button.released.connect(lambda: self.find_next_pressed())
        self.ui.cancel_button.released.connect(lambda: self.close())

        self.ui.find_button.setDisabled(True)  # disabled on startup
        self.ui.find_line_edit.textChanged.connect(lambda: self.text_changed())
        self.ui.find_line_edit.setFocus()

    def text_changed(self):
        self.auto_wrap_count = 0
        self.rfind_end_index = 0

        if len(self.ui.find_line_edit.text()) == 0:
            self.ui.find_button.setDisabled(True)
            self.start_index = 0  # reset find index data when new query was given
        else:
            self.ui.find_button.setEnabled(True)

    def not_found(self, query_text):
        not_found_msg = QMessageBox(QMessageBox.Information, 'Notepad',
                                    'Cannot find: "' + query_text + '"',
                                    QMessageBox.Ok, self)
        not_found_msg.setWindowIcon(self.dialog_icon)
        not_found_msg.setMinimumWidth(300)
        not_found_msg.show()

    def find_next_pressed(self):
        self.auto_wrap_count = 0
        self.find_text()

    def find_text(self):
        file_text = self.parent.ui.textField.toPlainText()
        query_text = self.ui.find_line_edit.text()

        if self.rfind_end_index == 0:
            self.rfind_end_index = len(file_text) - 1

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

            self.rfind_end_index = result - 1

        # Not found, if empty:
        if len(file_text) == 0:
            self.not_found(query_text)

        # Not found:
        elif result == -1:
            # Wrap around - only once automatically
            # TODO: analyse recursion behavior
            if self.ui.wrap_around_checkbox.isChecked() and self.auto_wrap_count < 1:
                self.start_index = 0
                self.rfind_end_index = len(file_text) - 1
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
