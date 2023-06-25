import main
import re
import time
import vlc
import win32con
import win32gui
from threading import Thread
from PyQt5.QtCore import Qt
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow
from gaze_data_creator import gaze_data_creator
from results_info import init_result_info_screen
from user import user
from validations import is_exam_form_valid
from PyQt5 import QtCore

global current_user


def run_exam(mw: main.MyWindow):
    # check validation of the form
    # try:
    #     if not is_exam_form_valid(mw):
    #         pass
    # except Exception as e:
    #     print("An error occurred:", str(e))
    #     return

    # change screen page
    mw.ui.screens_stack.setCurrentIndex(2)

    # create gaze data file
    name = mw.ui.name_lineEdit.text()
    age = mw.ui.age_lineEdit.text()
    gender = mw.ui.gender_cb.currentText()
    email = mw.ui.email_lineEdit.text()

    current_user = user(name, age, gender, email)
    GDC = gaze_data_creator(current_user)

    layout = QVBoxLayout()
    mw.ui.videoWidget.setLayout(layout)

    # create a video widget and add it to the layout
    video_widget = QVideoWidget()
    layout.addWidget(video_widget)

    # create a VLC instance and a media player
    vlc_instance = vlc.Instance()
    media_player = vlc_instance.media_player_new()

    # set the video output to the video widget
    media_player.set_hwnd(video_widget.winId())

    # create a media object and set its location
    media = vlc_instance.media_new("digVid.mp4")
    media_player.set_media(media)

    # start recording gaze data & minimize the screen
    GDC.start_record()

    # play the video
    media_player.play()

    # show the widget in full screen mode
    mw.ui.videoWidget.setWindowFlags(
        Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)

    # get the video screen in front
    time.sleep(0.1)
    fgwin = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(fgwin, win32con.SW_MINIMIZE)
    bgwin = win32gui.FindWindow(None, "capstone project")
    win32gui.ShowWindow(bgwin, win32con.SW_MAXIMIZE)

    # stop recording
    thread = Thread(target=stop_vid_and_change_page, args=(fgwin, mw, current_user))
    thread.start()


def stop_vid_and_change_page(fgwin, mw, current_user):
    time.sleep(119)
    mw.ui.videoWidget.children().clear()
    win32gui.SendMessage(fgwin, win32con.WM_CLOSE, 0, 0)
    # signal the main thread to run the results
    QtCore.QMetaObject.invokeMethod(mw, "run_result_info_screen", QtCore.Qt.QueuedConnection)
