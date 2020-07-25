#cd C:\Users\anosh\Documents\GitHub\project-Re-LAI-lite
# Resolution: 640 x 361

import numpy as np
import cv2
from window_cap import WindowCapture
import time
import math

# Maybe consider gpu accelerated python compiling...
# from numba import jit, cuda

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
    def digit_detect(self, img=None, copy=None, region=None, x=0, y=0, width=1270, height=711):
        tmp_numbers = {}
        # Read and crop the input image 
        crop_img = img[y:y+height, x:x+width]
        # cv2.imshow('crop', crop_img)
        # cv2.waitKey()

        # if x == 146 and y==20 and width==30 and height==15:
        #     cv2.imwrite('hp_test.jpg', crop_img)

        # Convert to grayscale and apply Gaussian filtering; was COLOR_BGR2GRAY
        im_gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('images/numbers/'+ region +'/' + str(copy) + '.jpg', 0)

        w, h = template.shape[::-1]
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)
        
        threshold = 0.82
        
        loc = np.where(res >= threshold)

        count = 0
        for pt in zip(*loc[::-1]):
            cv2.rectangle(crop_img,pt,(pt[0]+w, pt[1]+h), (0,255,255), 2)
            if count == 1:
                tmp_numbers[str(copy)+'_!'] = pt[0]
                count += 1
            elif count == 2:
                tmp_numbers[str(copy)+'_@'] = pt[0]
                count += 1
            elif count == 3:
                tmp_numbers[str(copy)+'_#'] = pt[0]
            else:
                tmp_numbers[str(copy)] = pt[0]
                count += 1

        # cv2.imshow('crop', crop_img)
        # cv2.waitKey()
        # print(copy)

        return tmp_numbers


    # returns player position from mini-map
    # @jit(target='cuda')
    def player_detect(self, img=None, copy=None, region=None, x=0, y=0, width=1270, height=711, last = None):
        tmp_numbers = {}
        # Read and crop the input image 
        crop_img = img[y:y+height, x:x+width]
        # cv2.imwrite('mini_map.jpg', crop_img)

        # Convert to grayscale and apply Gaussian filtering; was COLOR_BGR2GRAY
        im_gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('images/players/player_control.jpg', 0)

        w, h = template.shape[::-1]
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)
        
        threshold = 0.45
        
        loc = np.where(res >= threshold)
        x_pos = last[0]
        y_pos = last[1]

        for pt in zip(*loc[::-1]):
            # cv2.rectangle(crop_img, pt, (pt[0]+w, pt[1]+h), (0,255,255), 2)
            x_pos = pt[0]+w/2
            y_pos = pt[1]+h/2
        return x_pos, y_pos
    
    # returns enemy position from surroundings
    # @jit(target='cuda')
    def enemy_detect(self, img=None, copy=None, region=None, x=0, y=0, width=1270, height=711, last = None):
        tmp_numbers = {}
        # Read and crop the input image 
        # crop_img = img[y:y+height, x:x+width]
        # cv2.imwrite('mini_map.jpg', crop_img)

        # Convert to grayscale and apply Gaussian filtering; was COLOR_BGR2GRAY
        im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template = cv2.imread('images/enemy/6.jpg', 0)

        w, h = template.shape[::-1]
        res = cv2.matchTemplate(im_gray, template, cv2.TM_CCOEFF_NORMED)
        
        threshold = 0.8
        
        loc = np.where(res >= threshold)
        # x_pos = last[0]
        # y_pos = last[1]

        count = 0
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), (0,255,255), 1)
            count+=1
        
        if count > 1:
            return 1
        else:
            return 0
            
        

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
    def get_data(self, last_digits = None, last_pos = None, time = 0):
        img = self.screenshot()
        cv2.imwrite('test.jpg', img)
        # cv2.imwrite('turret_display.jpg', img)
        input_data = {'enemy_damage':[217,312,58,33], 
                'player_damage':[67,309,62,36]}
        output_data = {}
        
        for area in input_data:
            # print(area,'----------')
            x_coor = input_data[area][0]
            y_coor = input_data[area][1]
            w = input_data[area][2]
            h = input_data[area][3]
            numbers = {} 
            for number in range(10):
                # print(number)
                returned_numbers = self.digit_detect(img = img, copy = number, region = area,
                                            x = x_coor, y = y_coor, width = w, height = h)
                z = numbers.copy()
                z.update(returned_numbers)
                print(z)
            numbers = z
            num = {k: v for k, v in sorted(numbers.items(), key=lambda item: item[1])}
            num_str = ''
            for key in num:
                num_str = num_str + key
            remove = ['_', '!', '@', "#"]
            for i in remove:
                num_str = num_str.replace(i, '')
            if num_str == '':
                output_data[area]=None
            else:
                output_data[area]=num_str
            
        return {'output_data':output_data, 'img': img}

Detection().get_data()


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
