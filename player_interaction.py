import pickle
import time
import math
from pynput.mouse import Button, Controller
from RealRecognition import Detection
from window_cap import WindowCapture
from DirectKeys import PressKey, ReleaseKey, W, A, S, D, U, I, O, P, ESC, BACK 

class PlayerAI:
    def __init__(self):
        self.data = Detection().get_data()

        # Action 8 and above are attacks
        self.win_prop = WindowCapture('Super Smash Flash 2 Beta').get_screen_position()
        self.choices = {1:[[W], 1, True], 2:[[A], 1, True], 3:[[S], 1, True], 4:[[D], 1, True], 
                        5:[[W], 2, False], 6:[[A], 2, True], 7:[[D], 2, True], 8:[[O], 1, False],
                        9:[[P], 1, False], 10:[[A, O], [1, 2], [True, False]], 11:[[D, O], [1, 2], [True, False]],
                        12:[[A, O], [1, 4], [True, False]], 13:[[D, O], [1, 4], [True, False]],
                        14:[[A, O, S], [1, 4, 1], [True, False, True]], 15:[[D, O, S], [1, 4, 1], [True, False, True]],
                        16:[[I, A], [1, 1], [True, False]], 17:[[I, D], [1, 1], [True, False]],
                        18:[[W, O], [1 ,1], [True, False]]} 
                        # pickle.load(open('choices.pickle', 'rb'))
        # self.x, self.y = '' --> maybe something to think about later...
    
    def new_data(self):
        return Detection().get_data()

    def action(self, choice):
        if choice < 8:
            self.move(direction=self.choices[choice][0][0],
                     keypress_num=self.choices[choice][1])
        else:
            self.attack_actions(choice=self.choices[choice])
        
    def attack_actions(self, choice=None):
        dir_num = len(choice[0])

        if dir_num > 1:
            for i in range(0, dir_num):
                PressKey(choice[0][i])
                if choice[2][i] == True:
                    continue
                if choice[1][i] > 1:
                    for k in range(0, choice[1][i]):
                        time.sleep(0.5)
                        ReleaseKey(choice[0][i])
                        time.sleep(0.5)
                        PressKey(choice[0][i])
                    time.sleep(2)
                    ReleaseKey(choice[0][i])
                else:
                    ReleaseKey(choice[0][i])
                ReleaseKey(choice[0][0])
        else:
            PressKey(choice[0][0])
            ReleaseKey(choice[0][0])
        return

    def move(self, direction=None, keypress_num=None):
        PressKey(direction)

        if keypress_num > 1:
            for i in range(0, keypress_num):
                time.sleep(0.5)
                ReleaseKey(direction)
                time.sleep(0.5)
                PressKey(direction)
            if direction == W:
                ReleaseKey(direction)
            else:
                time.sleep(2)
                ReleaseKey(direction)
        return
