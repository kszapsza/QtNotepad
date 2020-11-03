from PyQt5.QtGui import QTextCursor, QIcon
from PyQt5.QtWidgets import QMessageBox
from enum import Enum


class FindDirection(Enum):
    UP = 0
    DOWN = 1


# Class realising searching for text from menu level
# (Find Next/Find Previous)
class FindMemory:
    def __init__(self, parent):
        self.parent = parent

        self.wrap_around = True
        self.query_text = ''
        self.cursor_position = 0

        self.direction = FindDirection.DOWN
        self.match_case = False

        # This stops the recursive call of Find after one cycle - when there are
        # no results. This flag is being reset when user manually presses Find button,
        # or when the query text has changed.
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
            self.find()

    def find(self):
        file_text = self.parent.ui.textField.toPlainText()

        # Find direction: down
        if self.direction == FindDirection.DOWN:
            if self.match_case:
                result = file_text.find(self.query_text, self.cursor_position)
            else:
                result = file_text.lower().find(self.query_text.lower(), self.cursor_position)

            self.cursor_position = result + 1

        # Find direction: up
        else:
            if self.match_case:
                result = file_text.rfind(self.query_text, 0, self.cursor_position)
            else:
                result = file_text.lower().rfind(self.query_text.lower(), 0, self.cursor_position)

            self.cursor_position = result

        # Not found:
        if result == -1:
            # Wrap around - only once automatically
            if self.wrap_around and self.auto_wrap_count < 1:
                self.cursor_position = 0 if (self.direction == FindDirection.DOWN) else len(file_text)
                self.auto_wrap_count += 1  # count the cycle to prevent infinite recursion
                self.find()  # call only once again recursively

            # Do not wrap around:
            # either wrapping is set to off, or there are NO results in WHOLE text
            else:
                FindMemory.not_found(self.parent, self.query_text)

                # "Stuck" the cursor in the end/beginning, when no wrap mode is set
                if self.direction == FindDirection.DOWN:
                    self.cursor_position = len(file_text) + 1
                else:
                    self.cursor_position = 0

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
            self.find()

