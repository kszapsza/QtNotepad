from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QPushButton
from PyQt5.QtGui import QCloseEvent, QTextCursor

from gui import Ui_MainWindow
import sys


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # File menu tab bindings
        self.ui.actionNew.triggered.connect(lambda: self.file_new_pressed())
        self.ui.actionFinish.triggered.connect(lambda: self.file_finish_pressed())

        # Edit menu tab bindings
        self.ui.actionSelect_all.triggered.connect(lambda: self.ui.textField.selectAll())

    def closeEvent(self, evnt: QCloseEvent):
        self.file_finish_pressed()

    def ask_if_to_save(self):
        unsaved = QMessageBox(self)

        unsaved.setIcon(QMessageBox.Warning)
        unsaved.setWindowTitle('Notepad')
        unsaved.setText('Do you wish to save changes in file?')

        unsaved.addButton(QPushButton('Save'), QMessageBox.YesRole)
        unsaved.addButton(QPushButton('Don\'t save'), QMessageBox.NoRole)
        unsaved.addButton(QMessageBox.Cancel)

        return unsaved.exec_()

    def file_new_pressed(self):
        if len(self.ui.textField.toPlainText()) != 0:
            unsaved_decision = self.ask_if_to_save()

            if unsaved_decision == QMessageBox.Yes:
                print('saved')
            if unsaved_decision != QMessageBox.Cancel:
                self.ui.textField.clear()

    def file_finish_pressed(self):
        if len(self.ui.textField.toPlainText()) == 0:
            self.close()
        else:
            unsaved_decision = self.ask_if_to_save()

            if unsaved_decision == QMessageBox.Yes:
                print('saved')
            elif unsaved_decision != QMessageBox.Cancel:
                self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    notepad = Notepad()
    notepad.show()

    sys.exit(app.exec_())
