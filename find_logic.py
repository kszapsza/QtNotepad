from PyQt5.QtGui import QTextCursor, QIcon
from PyQt5.QtWidgets import QMessageBox


# Class realising searching for text from menu level
# (Find Next/Find Previous)
class FindMemory:
    def __init__(self, parent):
        self.parent = parent

        self.wrap_around = True
        self.query_text = ''
        self.start_index = 0

        self.auto_wrap_count = 0

    @staticmethod
    def not_found(mbox_parent, query_text):
        not_found_msg = QMessageBox(QMessageBox.Information, 'Notepad',
                                    'Cannot find: "' + query_text + '"', QMessageBox.Ok, mbox_parent)
        not_found_msg.setWindowIcon(QIcon('.\\icon.png'))
        not_found_msg.setMinimumWidth(300)
        not_found_msg.show()

    # Used to find next/previous from menubar
    def find_next_pressed(self):
        self.auto_wrap_count = 0

        if self.query_text == '':
            self.parent.edit_find()
        else:
            self.find_down()

    def find_down(self):
        file_text = self.parent.ui.textField.toPlainText()

        if self.wrap_around:
            result = file_text.find(self.query_text, self.start_index)
        else:
            result = file_text.lower().find(self.query_text.lower(), self.start_index)

        self.start_index = result + 1

        # Not found:
        if result == -1:
            # Wrap around - only once automatically
            if self.wrap_around and self.auto_wrap_count < 1:
                self.start_index = 0
                self.auto_wrap_count += 1  # count the cycle to prevent infinite recursion
                self.find_down()  # call only once again recursively

            # Do not wrap around:
            # either wrapping is set to off, or there are NO results in WHOLE text
            else:
                FindMemory.not_found(self.parent, self.query_text)

        # Found a record:
        else:
            new_cursor = self.parent.ui.textField.textCursor()
            new_cursor.setPosition(result)
            new_cursor.setPosition(result + len(self.query_text), QTextCursor.KeepAnchor)

            self.parent.ui.textField.setTextCursor(new_cursor)
            self.parent.query_text = self.query_text

    def find_previous_pressed(self):
        # If no text in memory, open Edit > Find in parent window:
        if self.query_text == '':
            self.parent.edit_find()
        else:
            self.find_up()

    def find_up(self):
        pass

