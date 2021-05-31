import pyautogui as pgui
from PIL import Image, ImageGrab
import pytesseract
import time
import threading
import signal
import os

class Typer():
    def __init__(self, speed:float):
        self._speed = speed
        self.first_text = None
        self.future_text = None

        threading.Thread(target=self._end).start()
        threading.Thread(target=self._read_future_line).start()

    def start(self):
        pgui.moveTo(980, 320)
        pgui.click()
        pgui.write(message='a', interval=self._speed)
        time.sleep(.5)

        self.read_line(y1=460, y2=560)
        # print(repr(self.first_text))      # to print the text
        pgui.write(message=self.first_text, interval=self._speed)
        while True:
            # print(repr(self.future_text))     # to print the text
            pgui.write(message=self.future_text, interval=self._speed)

    def read_line(self, y1:int, y2:int, x1=450, x2=1490, future=False):
        screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        rawtext = pytesseract.image_to_string(self._modify_image(screenshot))
        if future:
            self.future_text = (str(rawtext.rstrip()) + ' ')
        else:
            self.first_text = (str(rawtext.rstrip()) + ' ').replace('\n', ' ')

    def _read_future_line(self):
        while True:
            self.read_line(y1=560, y2=600, future=True)

    def _end(self):
        while True:
            screenshot = ImageGrab.grab(bbox=(480, 370, 550, 408))
            if str(pytesseract.image_to_string(screenshot)).rstrip() == 'wpm':
                os.kill(os.getpid(), signal.SIGINT)

    def _modify_image(self, image):
        image_data = image.load()
        height,width = image.size
        for loop1 in range(height):
            for loop2 in range(width):
                r,g,b = image_data[loop1,loop2]
                image_data[loop1,loop2] = 0,0,b
        return image