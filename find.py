import core
from find_gui import Ui_Find

from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtWidgets import QDialog, QMainWindow, QMessageBox


class Find(QDialog):
    def __init__(self, parent: core.Notepad):
        super().__init__()

        self.ui = Ui_Find()
        self.ui.setupUi(self)

        self.parent = parent
        self.dialog_icon = QIcon('.\\icon.png')
        self.setWindowIcon(self.dialog_icon)

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
        self.ui.find_line_edit.textChanged.connect(lambda: self.disable_buttons())
        self.ui.find_line_edit.setFocus()

    def disable_buttons(self):
        if len(self.ui.find_line_edit.text()) == 0:
            self.ui.find_button.setDisabled(True)
        else:
            self.ui.find_button.setEnabled(True)

    def find_text(self):
        file_text = self.parent.ui.textField.toPlainText()
        query_text = self.ui.find_line_edit.text()
        result = file_text.find(query_text)

        if result == -1 or len(file_text) == 0:
            not_found_msg = QMessageBox(QMessageBox.Information,
                                        'Notepad', 'Cannot find: "' + query_text + '"',
                                        QMessageBox.Ok, self)
            not_found_msg.setWindowIcon(self.dialog_icon)
            not_found_msg.setMinimumWidth(300)
            not_found_msg.show()
        else:
            new_cursor = self.parent.ui.textField.textCursor()
            new_cursor.setPosition(result)
            new_cursor.setPosition(result + len(query_text), QTextCursor.KeepAnchor)
            self.parent.ui.textField.setTextCursor(new_cursor)
