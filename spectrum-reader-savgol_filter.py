from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
import pandas as pd
import altair as alt
import seaborn as sns

img = Image.open(r"spectrum.jpg")
img_width, img_height = img.size

crop_width = 300
crop_height = 200
crop_right = (img_width+crop_width)/2
crop_left = (img_width-crop_width)/2
crop_top = (img_height+crop_height)/2
crop_bot = (img_height-crop_height)/2
img_crop = img.crop((crop_left, crop_bot, crop_right , crop_top))
img_crop_w, img_crop_h = img_crop.size

img_bw = img_crop.convert("L")
# img_bw.show() 
img_res = img_bw.resize((img_crop_w,1), Image.Resampling.BILINEAR)
img_np = np.asarray(img_res).T

x = np.arange(0, img_crop_w)
# x = np.array([x]).T

y_sf = savgol_filter(img_np.T, 200, 2)
y_sf = np.concatenate(y_sf.T)
df_alt = pd.DataFrame({'x': x, 'y_sf': y_sf, 'img_np': np.concatenate(img_np)})

sns.lineplot(x = "x", y = "img_np", data = df_alt)
sns.lineplot(x = "x", y = "y_sf", data = df_alt)
plt.xlim(0,img_np.size)
plt.ylim(0,250)

print([img_np.T])