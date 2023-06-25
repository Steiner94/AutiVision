import re
from PyQt5.QtWidgets import QMessageBox, QApplication


def is_exam_form_valid(mw):
    error_log = "Please note the following errors:\n"

    # name field errors
    if mw.ui.name_lineEdit.text() == "":
        error_log += "\u2022 Name field is empty\n"

    # age field errors
    if mw.ui.age_lineEdit.text() == "":
        error_log += "\u2022 Age field is empty\n"

    # email field errors
    if not (re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', mw.ui.email_lineEdit.text())):
        error_log += "\u2022 Email field is not valid\n"

    # terms and condition field
    if not mw.ui.checkBox.isChecked():
        error_log += "\u2022 Terms and conditions needs to be checked\n"

    if not error_log == "Please note the following errors:\n":
        pop_error_message(error_log, "Invalid Input")
        return False  # fail

    return True  # pass


def pop_error_message(main_text, title_text):

    app = QApplication([])
    # create a QMessageBox object with the appropriate icon and message text

    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText(main_text)
    msg_box.setWindowTitle(title_text)

    # display the message box
    msg_box.exec_()
