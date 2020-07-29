from RealRecognition import Detection
import time

##image capture
time.sleep(2)
for i in range(60):
    Detection().img_save(number=i)
    time.sleep(1)