from find_memory import FindDirection
from gui.find_gui import Ui_Find

from PyQt5 import QtCore
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QDialog


# Edit > Find...QDialog class.
class Find(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # Initalize Find window UI.
        self.ui = Ui_Find()
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

        self.ui.find_line_edit.setText(self.parent.find_memory.query_text)
        self.ui.wrap_around_checkbox.setChecked(self.parent.find_memory.wrap_around)
        self.ui.down_radio.setChecked(True)

        self.ui.find_button.released.connect(lambda: self.find_next_pressed())
        self.ui.cancel_button.released.connect(lambda: self.close())

        self.ui.find_button.setDisabled(not bool(len(self.ui.find_line_edit.text())))
        self.ui.find_line_edit.textChanged.connect(lambda: self.text_changed())
        self.ui.find_line_edit.setFocus()

        self.ui.down_radio.toggled.connect(lambda: self.direction_changed())
        self.ui.wrap_around_checkbox.toggled.connect(lambda: self.wrap_mode_changed())
        self.ui.match_case_checkbox.toggled.connect(lambda: self.case_mode_changed())

        # Initialize search indexes (start for down search, end for up search).
        self.cursor_position = 0

    def closeEvent(self, event: QCloseEvent):
        self.parent.find_memory.cursor_position = self.cursor_position

    def text_changed(self):
        self.parent.find_memory.auto_wrap_count = 0
        self.parent.find_memory.query_text = self.ui.find_line_edit.text()

        if len(self.ui.find_line_edit.text()) == 0:
            self.ui.find_button.setDisabled(True)
        else:
            self.ui.find_button.setEnabled(True)

    def direction_changed(self):
        if self.ui.down_radio.isChecked():
            self.parent.find_memory.direction = FindDirection.DOWN
        else:
            self.parent.find_memory.direction = FindDirection.UP

    def wrap_mode_changed(self):
        if self.ui.wrap_around_checkbox.isChecked():
            self.parent.find_memory.wrap_around = True
        else:
            self.parent.find_memory.wrap_around = False

            # If cursor is at 0, the direction is UP, and we switch to "no wrap around"
            # no results would be found, although there are. That's why we want to
            # move cursor to the end in such a situation:
            if (self.parent.find_memory.direction == FindDirection.UP
                    and self.parent.find_memory.cursor_position == 0):
                self.parent.find_memory.cursor_position \
                    = len(self.parent.ui.textField.toPlainText())

    def case_mode_changed(self):
        if self.ui.match_case_checkbox.isChecked():
            self.parent.find_memory.match_case = True
        else:
            self.parent.find_memory.match_case = False

    def find_next_pressed(self):
        self.parent.find_memory.auto_wrap_count = 0
        self.find_text()

    def find_text(self):
        self.parent.find_memory.query_text = self.ui.find_line_edit.text()
        self.parent.find_memory.find()
