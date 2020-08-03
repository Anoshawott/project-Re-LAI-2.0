from window_cap import WindowCapture
from RealRecognition import Detection
import time
import subprocess
from pynput.mouse import Button, Controller
from DirectKeys import PressKey, ReleaseKey, O, P, BACK, SPACE

class EnvReset:
    def game_reset(self):
        mouse = Controller()

        # Exiting Game
        for i in list(range(4))[::-1]:
            print(i+1)
            time.sleep(1)

        # Exiting Game
        PressKey(BACK)
        time.sleep(0.2)
        ReleaseKey(BACK)

        time.sleep(1)

        PressKey(O)
        time.sleep(0.2)
        PressKey(P)
        time.sleep(0.2)
        PressKey(BACK)
        time.sleep(0.2)

        time.sleep(2)

        ReleaseKey(O)
        ReleaseKey(P)
        ReleaseKey(BACK)

        time.sleep(6)

        mouse.position=(737, 227)
        mouse.click(Button.left, 1)

        time.sleep(0.5)

        PressKey(SPACE)
        ReleaseKey(SPACE)

        time.sleep(0.5)

        mouse.position=(338, 401)
        mouse.click(Button.left,1)

        time.sleep(4)

        print('Reset done!')