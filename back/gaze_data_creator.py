import subprocess
from PyQt5.QtCore import pyqtSignal
from PySide2.QtCore import QObject
from user import user


class gaze_data_creator(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def __init__(self, current_user: user):
        self.name = current_user.name
        self.age = current_user.age
        self.gender = current_user.gender
        self.email = current_user.email

    def start_record(self):
        print("Start TobiiStream..")
        command = "cd back/TobiiStream & TobiiStream.exe >../gaze_data_textFiles/"
        command += self.name + "_"
        command += self.age + "_"
        command += self.gender + "_"
        command += self.email + ".txt"
        self.p = subprocess.Popen(["start", "cmd", "/k", command], shell=True)

