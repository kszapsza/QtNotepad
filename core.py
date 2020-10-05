import gui
import find

from PyQt5 import QtWidgets
from PyQt5.QtCore import QStandardPaths, QUrl
from PyQt5.QtWidgets import QFileDialog, QFontDialog, QMainWindow, QMessageBox
from PyQt5.QtGui import QCloseEvent, QIcon, QFont, QDesktopServices, QTextCursor

import ntpath
import sys


# QtNotepad
# 2020, Karol Szapsza

# This software utilizes the PyQt5 framework, released under the GPL v3 license and under
# a commercial license that allows for the development of proprietary applications.

# Window icon (icon.png) made by Freepik, http://flaticon.com/.


# Main Notepad window class.
class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = gui.Ui_MainWindow()
        self.ui.setupUi(self)

        self.notepad_icon = QIcon('.\\icon.png')
        self.setWindowIcon(self.notepad_icon)

        self.last_path = QStandardPaths.displayName(QStandardPaths.DesktopLocation)
        self.zoom_amnt = 0

        # Find/replace data need to be stored in parent window class in order to
        # make possibility for calling Find previous/Find next from the main window menu bar.

        self.query_text = None

        # Opened file data
        self.opened_filepath = 'Untitled'
        self.changes_made = False

        # Text changing bindings
        self.ui.textField.textChanged.connect(lambda: self.set_changes_made())
        self.ui.textField.selectionChanged.connect(lambda: self.disable_selection_dependent())
        self.disable_selection_dependent()

        # File menu tab bindings
        self.ui.actionNew.triggered.connect(lambda: self.file_new_pressed())
        self.ui.actionOpen.triggered.connect(lambda: self.file_open_pressed())
        self.ui.actionSave.triggered.connect(lambda: self.file_save_pressed())
        self.ui.actionSave_as.triggered.connect(lambda: self.file_save_as_pressed())
        self.ui.actionFinish.triggered.connect(lambda: self.file_finish_pressed())

        # Edit menu tab bindings
        self.ui.actionUndo.triggered.connect(lambda: self.ui.textField.undo())
        self.ui.actionRedo.triggered.connect(lambda: self.ui.textField.redo())
        self.ui.actionCut.triggered.connect(lambda: self.ui.textField.cut())
        self.ui.actionCopy.triggered.connect(lambda: self.ui.textField.copy())
        self.ui.actionPaste.triggered.connect(lambda: self.ui.textField.paste())
        self.ui.actionDelete.triggered.connect(lambda: self.ui.textField.textCursor().removeSelectedText())
        self.ui.actionFind.triggered.connect(lambda: self.edit_find())
        self.ui.actionSearch_in_Google.triggered.connect(lambda: self.edit_search_with_google())
        self.ui.actionSelect_all.triggered.connect(lambda: self.ui.textField.selectAll())

        # Format menu tab bindings
        self.ui.actionWord_wrap.setChecked(True)
        self.ui.actionWord_wrap.triggered.connect(
            lambda: self.ui.textField.setLineWrapMode(self.ui.actionWord_wrap.isChecked()))
        self.ui.actionFont.triggered.connect(lambda: self.font_menu())

        # View menu tab bindings
        self.ui.actionZoom_in.triggered.connect(lambda: self.zoom_in())
        self.ui.actionZoom_out.triggered.connect(lambda: self.zoom_out())
        self.ui.actionRestore_default_zoom.triggered.connect(lambda: self.restore_zoom())
        self.ui.actionStatus_bar.setChecked(True)
        self.ui.actionStatus_bar.triggered.connect(lambda: self.hide_show_status_bar())

        # Help menu tab bindings
        self.ui.actionNotepad_info.triggered.connect(lambda: self.help_about_pressed())

    # Class variables cannot be modified inside lambda, so this method is necessary
    # Besides controlling changes_made flag, adds asterisk to window title as well
    def set_changes_made(self):
        self.changes_made = True

        if self.windowTitle()[0] != '*':
            self.setWindowTitle('*' + self.windowTitle())

    def reset_changes_made(self):
        self.changes_made = False

        if self.windowTitle()[0] == '*':
            self.setWindowTitle(self.windowTitle()[1:])

    def disable_selection_dependent(self):
        if len(self.ui.textField.textCursor().selectedText()) == 0:
            self.ui.actionCut.setDisabled(True)
            self.ui.actionCopy.setDisabled(True)
            self.ui.actionDelete.setDisabled(True)
            self.ui.actionSearch_in_Google.setDisabled(True)
        else:
            self.ui.actionCut.setEnabled(True)
            self.ui.actionCopy.setEnabled(True)
            self.ui.actionDelete.setEnabled(True)
            self.ui.actionSearch_in_Google.setEnabled(True)

    # Prompts if user wants to save unsaved changes
    def ask_if_to_save(self):
        unsaved_text = 'Do you wish to save changes in file ' + self.opened_filepath + '?'
        unsaved = QMessageBox(QMessageBox.Warning, 'Notepad', unsaved_text,
                              QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
        unsaved.setMaximumWidth(200)
        unsaved.setWindowIcon(self.notepad_icon)
        return unsaved.exec_()

    # Overriden closeEvent() method prompting if to save if unsaved changes were made
    def closeEvent(self, event: QCloseEvent):
        if self.changes_made:
            unsaved_decision = self.ask_if_to_save()

            if unsaved_decision == QMessageBox.Save:
                self.file_save_pressed()
            elif unsaved_decision == QMessageBox.Cancel:
                event.ignore()
        else:
            self.close()

    # File > New
    # Asks if to save unsaved changes, clears text field.
    def file_new_pressed(self):
        unsaved_decision = None

        if self.changes_made:
            unsaved_decision = self.ask_if_to_save()

            if unsaved_decision == QMessageBox.Save:
                self.file_save_pressed()

        if not self.changes_made or unsaved_decision == QMessageBox.Discard:
            self.ui.textField.clear()
            self.opened_filepath = 'Untitled'
            self.setWindowTitle('Untitled — Notepad')
            self.reset_changes_made()

    # File > Open...
    # Opens file dialog, loads file contents to text field.
    def file_open_pressed(self):
        unsaved_decision = None

        if self.changes_made:
            unsaved_decision = self.ask_if_to_save()
            if unsaved_decision == QMessageBox.Save:
                self.file_save_pressed()

        if not self.changes_made or unsaved_decision == QMessageBox.Discard:
            open_dialog = QFileDialog()

            open_dialog.setWindowTitle("Open…")
            open_dialog.setFileMode(QFileDialog.ExistingFile)
            open_dialog.setNameFilter('Text files (*.txt)')
            open_dialog.setViewMode(QFileDialog.List)
            open_dialog.setDirectory(self.last_path)
            open_dialog.setProxyModel(None)

            if open_dialog.exec_():
                filepaths = open_dialog.selectedFiles()
                self.opened_filepath = filepaths[0]

                with open(filepaths[0], mode='r', encoding='utf-8') as opened_file:
                    opened_text = opened_file.read()
                    self.ui.textField.setPlainText(opened_text)

                base_filename = ntpath.basename(filepaths[0])
                self.setWindowTitle(base_filename + ' — Notepad')
                self.reset_changes_made()

    # File > Save
    def file_save_pressed(self):
        if self.changes_made:
            if self.opened_filepath == 'Untitled':
                self.file_save_as_pressed()
            else:
                with open(self.opened_filepath, mode='w+', encoding='utf-8') as opened_file:
                    opened_file.write(self.ui.textField.toPlainText())
                    self.reset_changes_made()

    # File > Save as...
    def file_save_as_pressed(self):
        save_as_dialog = QFileDialog()

        save_as_dialog.setWindowTitle("Save as…")
        save_as_dialog.setAcceptMode(QFileDialog.AcceptSave)
        save_as_dialog.setFileMode(QFileDialog.AnyFile)
        save_as_dialog.setNameFilter('Text files (*.txt)')
        save_as_dialog.setViewMode(QFileDialog.List)
        save_as_dialog.setDirectory(self.last_path)
        save_as_dialog.setProxyModel(None)

        if save_as_dialog.exec_():
            save_as_filename = save_as_dialog.selectedFiles()

            with open(save_as_filename[0], mode='w+', encoding='utf-8') as opened_file:
                opened_file.write(self.ui.textField.toPlainText())

            base_filename = ntpath.basename(save_as_filename[0])
            self.opened_filepath = save_as_filename
            self.setWindowTitle(base_filename + ' — Notepad')
            self.reset_changes_made()

    # File > Finish
    # Same behaviour as if [X] was pressed.
    def file_finish_pressed(self):
        self.close()

    # Edit > Search with Google
    def edit_search_with_google(self):
        original_text = self.ui.textField.textCursor().selectedText()
        raw_text = original_text.replace(' ', '+')
        raw_text = raw_text.replace('&', '+')
        QDesktopServices.openUrl(QUrl('http:://google.com/search?q=' + raw_text))

    # Edit > Find...
    def edit_find(self):
        find_dialog = find.Find(parent=self)
        find_dialog.exec_()

    # Format > Font
    def font_menu(self):
        font_dialog = QFontDialog(self)
        font_dialog.setCurrentFont(self.ui.textFieldWidget.font())
        font_dialog.setWindowTitle('Font…')

        if font_dialog.exec_():
            if font_dialog.currentFontChanged:
                self.ui.textFieldWidget.setFont(font_dialog.currentFont())

    # View > Zoom > Zoom in
    def zoom_in(self):
        self.ui.textField.zoomIn(2)
        self.zoom_amnt += 1

    # View > Zoom > Zoom out
    def zoom_out(self):
        if self.zoom_amnt > -5:
            self.ui.textField.zoomOut(2)
            self.zoom_amnt -= 1

    # View > Zoom > Restore default zoom
    def restore_zoom(self):
        if self.zoom_amnt < 0:
            while self.zoom_amnt != 0:
                self.zoom_in()
        elif self.zoom_amnt > 0:
            while self.zoom_amnt != 0:
                self.zoom_out()

    # View > Status bar
    def hide_show_status_bar(self):
        if self.ui.statusbar.isHidden():
            self.ui.statusbar.show()
        else:
            self.ui.statusbar.hide()

    # Help > About Notepad
    def help_about_pressed(self):
        QMessageBox.about(self, 'About Notepad',
                          """QtNotepad
© 2020 Karol Szapsza

This software utilizes the PyQt5 framework,
released under the GPL v3 license and under
a commercial license that allows for the
development of proprietary applications.

Window icon (icon.png) made by Freepik,
http://flaticon.com/.""")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    notepad = Notepad()
    notepad.show()

    sys.exit(app.exec_())
