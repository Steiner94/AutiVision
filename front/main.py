import os
import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QLabel

import exam
from mainwindow import Ui_MainWindow
from results_info import download_PDF, init_result_info_screen


# exit program with code 0
def exit_program():
    sys.exit()


# swap screen
def swap_screen(mw, page_num):
    mw.ui.screens_stack.setCurrentIndex(page_num)


# clear the ui for second run
def clear_ui(mw):
    mw.ui.screens_stack.setCurrentIndex(0)
    mw.ui.name_lineEdit.clear()
    mw.ui.gender_cb.setCurrentIndex(0)
    mw.ui.checkBox.setChecked(False)
    mw.ui.email_lineEdit.clear()
    mw.ui.age_lineEdit.clear()


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the UI window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("AutiVision")
        self.setWindowState(Qt.WindowFullScreen)

        # Connect signals and slots
        self.ui.exitBtn.clicked.connect(exit_program)
        self.ui.startExamBtn.clicked.connect(lambda: swap_screen(self, 1))
        self.ui.back_start_exam1_btn.clicked.connect(lambda: swap_screen(self, 1))
        self.ui.terms_condition_btn.clicked.connect(lambda: swap_screen(self, 4))
        self.ui.start_exam_btn.clicked.connect(lambda: exam.run_exam(self))
        self.ui.donwloadPDF_button.clicked.connect(lambda: download_PDF(self))
        self.ui.main_menu_btn.clicked.connect(lambda: clear_ui(self))
        self.ui.setGearBtn.clicked.connect(lambda: swap_screen(self, 6))
        self.ui.back_start_exam1_btn_2.clicked.connect(lambda: swap_screen(self, 0))

        # Set mainMenu eyes animation
        self.setMouseTracking(True)
        self.ui.centralwidget.setMouseTracking(True)

        # Add loading gif label
        self.ui.label = QLabel(self)
        self.ui.label.setGeometry(720, 310, 480, 360)

        movie = QMovie(os.path.abspath("icons/loading_gif.gif"))
        self.ui.label.setMovie(movie)
        movie.start()
        self.ui.label.hide()

    def mouseMoveEvent(self, event):
        cursor_pos_x, cursor_pos_y = event.pos().x(), event.pos().y()
        self.update_eye_position(self.ui.left_eye_lens, cursor_pos_x, cursor_pos_y, 'left')
        self.update_eye_position(self.ui.right_eye_lens, cursor_pos_x, cursor_pos_y, 'right')

    def update_eye_position(self, eye_label, cursor_pos_x, cursor_pos_y, side):
        if side == 'left':
            if cursor_pos_x > 1070:
                new_x = 230
            elif cursor_pos_x > 1020:
                new_x = 190
            else:
                new_x = 150

        if side == 'right':
            if cursor_pos_x > 1070:
                new_x = 75
            elif cursor_pos_x > 900:
                new_x = 40
            else:
                new_x = 10

        if cursor_pos_y > 170:
            new_y = 80
        else:
            new_y = 10
        eye_label.move(QPoint(new_x, new_y))

    @QtCore.pyqtSlot()
    def run_result_info_screen(self):
        init_result_info_screen(self)

    @QtCore.pyqtSlot()
    def stop_loading_gif(self):
        self.ui.main_menu_btn.show()
        self.ui.results_frame.show()
        self.ui.directD_label.hide()

    @QtCore.pyqtSlot()
    def PDF_file_created(self):
        # hide loading gif to indicate the user calculations are made
        self.ui.label.hide()

        # hide the object on the screen until calculations are done
        self.ui.main_menu_btn.show()
        self.ui.results_frame.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
