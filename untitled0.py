import numpy as np
from PIL import Image
import IPython.display as display
from matplotlib import pyplot as plt
from matplotlib import image as mpimg
from scipy.interpolate import CubicSpline
from scipy.signal import savgol_filter

image = Image.open("spectrum.jpg")
# display.display(Image.open('spectrum.jpg'))
# print(image.size)
new_size = tuple(int(0.1*x) for x in image.size)
image = image.resize(new_size)
x = np.linspace(0,image.size[0]-1,image.size[0])
# plt.imshow(image)
# plt.show()

image = image.crop((0, 150, image.size[0], 190))
image = image.convert("L")

print("Cropped image size:",image.size)
img_as_array = np.asarray(image)

vert_slice_list = []
for i in range(0,image.size[0]):
    vert_slice = np.average(img_as_array[:,i])
    vert_slice_list.append(vert_slice)
grey_avg = np.squeeze(vert_slice_list)

# grey_spline = CubicSpline(x,grey_avg)
# grey = grey_spline(x)

grey_sav = savgol_filter(grey_avg, 100, 2)
# plt.plot(grey_avg,"-")
# plt.figure(figsize=(8,8))
# plt.imshow(image, cmap='gray')
# plt.show()

plt.figure(figsize=(8,8))
plt.plot(grey_sav)
plt.show()

# normalize_ref = 1/grey_sav
# plt.plot(normalize_ref)




