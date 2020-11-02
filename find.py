import core
from find_gui import Ui_Find

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox


# Edit > Find...QDialog class.
class Find(QDialog):
    def __init__(self, parent: core.Notepad):
        super().__init__()

        self.ui = Ui_Find()
        self.ui.setupUi(self)

        self.parent = parent
        self.dialog_icon = QIcon('.\\icon.png')
        self.setWindowIcon(self.dialog_icon)

        self.start_index = 0
        self.rfind_end_index = 0

        self.setModal(True)

        # noinspection PyTypeChecker
        self.setWindowFlags(self.windowFlags()
                            & QtCore.Qt.WindowStaysOnTopHint
                            & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.ui.down_radio.setChecked(True)
        self.ui.wrap_around_checkbox.setChecked(True)

        self.ui.find_button.released.connect(lambda: self.find_text())
        self.ui.cancel_button.released.connect(lambda: self.close())

        self.ui.find_button.setDisabled(True)  # disabled on startup
        self.ui.find_line_edit.textChanged.connect(lambda: self.text_changed())
        self.ui.find_line_edit.setFocus()

    def text_changed(self):
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

        # Result if empty
        if len(file_text) == 0:
            self.not_found(query_text)

        # Not found (end)
        elif result == -1:
            # Wrap around
            if self.ui.wrap_around_checkbox.isChecked():
                self.start_index = 0
                self.rfind_end_index = len(file_text) - 1
                self.find_text()
            # Do not wrap around
            else:
                self.not_found(query_text)

        # Found
        else:
            new_cursor = self.parent.ui.textField.textCursor()
            new_cursor.setPosition(result)
            new_cursor.setPosition(result + len(query_text), QTextCursor.KeepAnchor)

            self.parent.ui.textField.setTextCursor(new_cursor)
            self.parent.query_text = query_text
