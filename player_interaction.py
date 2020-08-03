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
        self.choices = {0:[[W], 1, True], 1:[[A], 1, True], 2:[[D], 1, True], 
                        3:[[W], 2, False], 4:[[A], 2, True], 5:[[D], 2, True], 6:[[O], 1, False],
                        7:[[P], 1, False], 8:[[A, O], [1, 4], [True, False]], 9:[[D, O], [1, 4], [True, False]],
                        10:[[A, O], [1, 12], [True, False]], 11:[[D, O], [1, 12], [True, False]]} 
                        # pickle.load(open('choices.pickle', 'rb'))
                        
                        #, 3:[[S], 1, True],
                        # 14:[[A, O, S], [1, 4, 1], [True, False, True]], 15:[[D, O, S], [1, 4, 1], [True, False, True]],
                        # 16:[[I, A], [1, 1], [True, False]], 17:[[I, D], [1, 1], [True, False]],
                        # 18:[[W, O], [1 ,1], [True, False]]

        # self.x, self.y = '' --> maybe something to think about later...
    
    def new_data(self):
        return Detection().get_data()

    def action(self, choice):
        if choice < 6:
            self.move(direction=self.choices[choice][0][0],
                     keypress_num=self.choices[choice][1])
        else:
            self.attack_actions(choice=self.choices[choice], choice_num=choice)
        
    def attack_actions(self, choice=None, choice_num=None):
        dir_num = len(choice[0])

        if dir_num > 1:
            for i in range(0, dir_num):
                PressKey(choice[0][i])
                if choice[2][i] == True:
                    continue
                count = 0
                press_s = False
                if choice[1][i] > 1:
                    for k in range(0, choice[1][i]):
                        try:
                            if count == 2 and choice[0][2] == S:
                                PressKey(S)
                                press_s = True
                        except:
                            None
                        time.sleep(0.05)
                        ReleaseKey(choice[0][i])
                        time.sleep(0.05)
                        PressKey(choice[0][i])
                        count += 1
                    if press_s == True:    
                        ReleaseKey(S)
                    if 12 <= choice_num <= 15:
                        time.sleep(0.6)
                    else:
                        time.sleep(0.5)
                    ReleaseKey(choice[0][i])
                else:
                    ReleaseKey(choice[0][i])
                ReleaseKey(choice[0][0])
        else:
            PressKey(choice[0][0])
            time.sleep(0.05)
            ReleaseKey(choice[0][0])
        return

    def move(self, direction=None, keypress_num=None):
        PressKey(direction)

        if keypress_num > 1:
            for i in range(0, keypress_num):
                time.sleep(0.1)
                ReleaseKey(direction)
                time.sleep(0.1)
                PressKey(direction)
            if direction == W:
                ReleaseKey(direction)
            time.sleep(0.5)
            ReleaseKey(direction)
        else:
            time.sleep(1)
            ReleaseKey(direction)
        return
