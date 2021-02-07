import pyautogui as pgui
from PIL import ImageGrab
import pytesseract
import time
import threading
import signal
import os

class Typer():
    def __init__(self):
        self.first_text = None
        self.future_text = None

        threading.Thread(target=self._end).start()
        threading.Thread(target=self._read_future_line).start()

    def start(self):
        pgui.moveTo(950, 460)
        pgui.click()
        time.sleep(.5)

        self.read_line(y1=460, y2=540)
        # print(repr(self.first_text))      # to print the text
        pgui.write(message=self.first_text, interval=.01)
        while True:
            # print(repr(self.future_text))     # to print the text
            pgui.write(message=self.future_text, interval=.01)

    def read_line(self, y1:int, y2:int, x1=450, x2=1490, future=False):
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        rawtext = pytesseract.image_to_string(screenshot)
        if future:
            self.future_text = str(rawtext.rstrip()) + ' '
        else:
            self.first_text = (str(rawtext.rstrip()) + ' ').replace('\n', ' ')

    def _read_future_line(self):
        while True:
            self.read_line(y1=540, y2=580, future=True)

    def _end(self):
        while True:
            screenshot = ImageGrab.grab(bbox=(440, 340, 505, 370))
            if str(pytesseract.image_to_string(screenshot)).rstrip() == 'wpm':
                os.kill(os.getpid(), signal.SIGINT)

MonkeyTyper = Typer()
MonkeyTyper.start()