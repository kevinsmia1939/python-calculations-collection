from mpl_toolkits import mplot3d
import numpy as np
from PIL import Image
import IPython.display as display
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from scipy.interpolate import CubicSpline
from scipy.signal import savgol_filter
import cv2

vid = cv2.VideoCapture("vid.mp4")
img_width = 30
def getFrame(sec):
    global image
    vid.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vid.read()
    if hasFrames:
        image = image[500:600, :, :]
    return [hasFrames, image]

sec = 0
frameRate = 20
count=1
success = getFrame(sec)
cap_list = []
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success, cap_img = getFrame(sec)
    if success == True:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(image, dsize=(img_width, 1), interpolation=cv2.INTER_LINEAR)
        image = savgol_filter(image, 10, 3)
        image = np.squeeze(image)
        cap_list.append(image)
cap_array = np.array(cap_list, dtype=int)
cap_array = np.squeeze(cap_array).T

fig, ax = plt.subplots()
im = ax.imshow(cap_array, cmap='gray')
plt.show()

plt.plot(cap_array)
plt.show()

