import subprocess
import time
import sys
import os


command = "TobiiStream.exe >../gaze_data_textFiles/1212.txt"

# Needs to be shell since start isn't an executable, its a shell cmd
p = subprocess.Popen(["start", "cmd", "/k", command], shell=True)

time.sleep(3)
p.terminate()
