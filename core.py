from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QPushButton, QMainWindow
from PyQt5.QtGui import QCloseEvent

from gui import Ui_MainWindow
import sys


class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.actionFinish.triggered.connect(lambda: self.close())

    def closeEvent(self, evnt: QCloseEvent):
        self.check_if_unsaved()

    def check_if_unsaved(self):
        if len(self.ui.textField.toPlainText()) == 0:
            self.close()
        else:
            unsaved = QMessageBox(self)

            unsaved.setIcon(QMessageBox.Warning)
            unsaved.setWindowTitle('Notepad')
            unsaved.setText('Do you wish to save changes in file?')

            unsaved.addButton(QPushButton('Save'), QMessageBox.YesRole)
            unsaved.addButton(QPushButton('Don\'t save'), QMessageBox.NoRole)
            unsaved.addButton(QMessageBox.Cancel)

            unsaved_decision = unsaved.exec_()

            if unsaved_decision == QMessageBox.YesRole:
                print('saved')
            elif unsaved_decision == QMessageBox.NoRole:
                self.close()
            else:
                unsaved.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    notepad = Notepad()
    notepad.show()

    sys.exit(app.exec_())
