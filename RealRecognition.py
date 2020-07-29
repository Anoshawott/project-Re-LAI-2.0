#cd C:\Users\anosh\Documents\GitHub\project-Re-LAI-lite
# Resolution: 640 x 361

import numpy as np
import cv2
from window_cap import WindowCapture
import time
import math
import os
import pickle

# Maybe consider gpu accelerated python compiling...
from numba import jit, cuda

##### SUCCESS!!!!!!!
# NOTE: 0.8 = get_coins, GET_HP WILL NEED ITS OWN SET OF NUMBERS TO COMPARE, ALSO NUMBERS FOR
# METRICS MAY BE DIFFERENT AND MAY NEED EXTRA SET 

class Detection:

    # screenshot() returns an image of some given area
    def screenshot(self):
        wincap = WindowCapture('Super Smash Flash 2 Beta')
        img = wincap.get_screenshot()
        return img  

    # returns digit and position
    # @jit(target='cuda')
    def match_res(self, img, template):
        # Convert to grayscale and apply Gaussian filtering; was COLOR_BGR2GRAY
        im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # w, h = template.shape[::-1]
        return cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)

    def digit_detect(self, img=None, region=None, x=0, y=0, width=640, height=361):
        tmp_numbers = {}
        # Read and crop the input image 
        crop_img = img[y:y+height, x:x+width]
        # cv2.imshow('crop', crop_img)
        # cv2.waitKey()

        # if x == 146 and y==20 and width==30 and height==15:
        #     cv2.imwrite('hp_test.jpg', crop_img)
        pickle_in = open('imgNames.pickle', 'rb')
        new_names = pickle.load(pickle_in)

        max_res = 0.75
        max_res2 = 0.95
        nums = []
        for img in new_names:
            template = cv2.imread('images/numbers/image_write/'+ region +'/done_images/'+ str(img) + '.jpg', 0)
            res = self.match_res(crop_img, template)

            if region!='enemy_damage':
                if res > max_res:
                    max_res = res
                    nums.append(img)
                else:
                    continue
            else:
                if res > max_res2:
                    max_res2 = res
                    nums.append(img)
                else:
                    continue
            
            

            count = 0
            # for pt in zip(*loc[::-1]):
            #     count+=1

            # if count > 0 and region=='enemy_damage':
            #     nums.append(img)
            # elif count > 0:
            #     nums.append(img)
        try:
            return nums[-1]
        except:
            return None

        # cv2.imshow('crop', crop_img)
        # cv2.waitKey()
        # print(copy)

        return tmp_numbers


    def img_save(self, number=None):
        img = self.screenshot()
        # cv2.imwrite('turret_display.jpg', img)
        input_data = {'enemy_damage':[217,312,58,33]}
        
        for area in input_data:
            # print(area,'----------')
            x_coor = input_data[area][0]
            y_coor = input_data[area][1]
            w = input_data[area][2]
            h = input_data[area][3]
            returned_numbers = self.img_crop(img = img, copy = number, region = area,
                                            x = x_coor, y = y_coor, width = w, height = h)
    
    def img_crop(self, img=None, copy=None, region=None, x=0, y=0, width=640, height=361):
        crop_img = img[y:y+height, x:x+width]
        cv2.imwrite('images/numbers/image_write/'+ region +'/'+ str(copy) + '.jpg', crop_img)
        print(copy,': Saved!')
        return

    # returns turret state and distance from player from mini-map
    # def turret_detect(self, img, copy=None, region=None, x=0, y=0, width=1270, height=711):
    #     tmp_numbers = {}
    #     # Read and crop the input image 
    #     crop_img = img[y:y+height, x:x+width]

    #     # Convert to grayscale and apply Gaussian filtering; was COLOR_BGR2GRAY
    #     im_gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    #     template = cv2.imread('images/players/player_control.jpg', 0)

    #     w, h = template.shape[::-1]
    #     res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)
        
    #     threshold = 0.45
        
    #     loc = np.where(res >= threshold)
    #     x_pos = None
    #     y_pos = None

    #     for pt in zip(*loc[::-1]):
    #         # cv2.rectangle(crop_img, pt, (pt[0]+w, pt[1]+h), (0,255,255), 2)
    #         x_pos = pt[0]/2
    #         y_pos = pt[1]/2
    #     return x_pos, y_pos, crop_img


    # put output_data variable for last_digits when initiating function; turret':[146,20,30,15],
    def get_data(self, data_checked=None, last_digits = None, last_pos = None, time = 0):
        img = self.screenshot()
        cv2.imwrite('test.jpg', img)
        # cv2.imwrite('turret_display.jpg', img)
        input_data = {'enemy_damage':[217,312,58,33], 
                'player_damage':[67,312,58,33]} #62,36
        output_data = {}
        
        for area in input_data:
            # print(area,'----------')
            x_coor = input_data[area][0]
            y_coor = input_data[area][1]
            w = input_data[area][2]
            h = input_data[area][3]
            numbers = {} 

            returned_number = self.digit_detect(check=None, img = img, region = area,
                                        x = x_coor, y = y_coor, width = w, height = h)
            output_data[area]=returned_number  

        return {'output_data':output_data, 'img': img}


# Following attempts to read and interpret on-screen information 
#### (Digit Recognition 3.0)

# for i in list(range(3))[::-1]:
#     print(i+1)
#     time.sleep(1)

# start = time.time()
# count = 0
# while True:
#     if count == 0:
#         print('Time elapsed:', time.time()-start)
#         print(DigitDetect().get_data())
#         print('-------------')
#         last_data = DigitDetect().get_data()

#         count += 1
#     else:
#         print('Time elapsed:', time.time()-start)
#         start_1 = time.time()
#         print(DigitDetect().get_data(last = last_data))
#         print(time.time()-start_1)
#         print('-------------')
#         last_data = DigitDetect().get_data()


#     time.sleep(5)



# Digit recognition 2.5 --> with new windowed coordinates but with inefficient data collection

# for i in list(range(3))[::-1]:
#     print(i+1)
#     time.sleep(1)

# start = time.time()
# count = 0
# while True:
#     if count == 0:
#         print('Time elapsed:', time.time()-start)
#         print('Coins: ', DigitDetect().get_data(797,691,51,17, where = 'coins'))
#         print('CP: ', DigitDetect().get_data(1178,0,25,16, where = 'cp'))
#         print('KDA: ', DigitDetect().get_data(1103,0,43,13, where = 'kda'))
#         print('-------------')
#         last_coins = DigitDetect().get_data(797,691,51,17, where = 'coins')
#         last_cp = DigitDetect().get_data(1178,0,25,16, where = 'cp')
#         last_kda = DigitDetect().get_data(1103,0,43,13, where = 'kda')

#         count += 1
#     else:
#         print('Time elapsed:', time.time()-start)
#         start_1 = time.time()
#         print('Coins: ', DigitDetect().get_data(797,691,51,17, where = 'coins', last = last_coins))
#         print(time.time()-start_1)
#         print('CP: ', DigitDetect().get_data(1178,0,25,16, where = 'cp', last = last_cp))
#         print('KDA: ', DigitDetect().get_data(1103,0,43,13, where = 'kda', last = last_kda))
#         print('-------------')
#         last_coins = DigitDetect().get_data(797,691,51,17, where = 'coins')
#         last_cp = DigitDetect().get_data(1178,0,25,16, where = 'cp')
#         last_kda = DigitDetect().get_data(1103,0,43,13, where = 'kda')


#     time.sleep(5)

#below uses coordinates when the whole screen was being read...

# start = time.time()
# count = 0
# while True:
#     if count == 0:
#         print('Time elapsed:', time.time()-start)
#         coins = DigitDetect().get_data(1117,868,51,17, where = 'coins')
#         cp = DigitDetect().get_data(1504,173,25,16, where = 'cp')
#         kda = DigitDetect().get_data(1427,172,43,13, where = 'kda')
#         print('-------------')
#         last_coins = coins
#         last_cp = cp
#         last_kda = kda

#         count += 1
#     else:
#         print('Time elapsed:', time.time()-start)
#         coins = DigitDetect().get_data(1117,868,51,17, where = 'coins', last = last_coins)
#         cp = DigitDetect().get_data(1504,173,25,16, where = 'cp', last = last_cp)
#         kda = DigitDetect().get_data(1427,172,43,13, where = 'kda', last = last_kda)
#         print('-------------')
#         last_coins = coins
#         last_cp = cp
#         last_kda = kda
        
#     time.sleep(5)


# MAKE SCREENSHOT FASTER USE DIRECT WINDOWS METHOD!!!! get each screengrab down to 0.01 then we can total 
# time with each detection with 0.05 = 20fps
