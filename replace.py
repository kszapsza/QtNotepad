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
