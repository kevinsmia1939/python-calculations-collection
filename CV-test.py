import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
CV_file = 'data/CV and EIS/Sample 1(500C3h)/CV_V3_0to1.2V.txt'

df=pd.read_table(CV_file, skiprows=1, sep='\t', header=None, usecols=[0,1])
df = np.array(df)
volt = df[:,0]
current = df[:,1]
plt.plot(volt,current)

v_vertex = max(volt)
jpa = max(current)
jpc_sq = np.squeeze(current)
jpc = min(jpc_sq[500:current.shape[0]])
# print(jpc)
# print(jpa)


# yinter = interp1d(x, y)
# yinter = np.interp(0, current, volt)
# plt.vlines(yinter,0,0.004,colors='red')
# # plt.show()
# print(yinter)

yaxis = np.zeros(current.shape[0])
idx = np.argwhere(np.diff(np.sign(yaxis - current))).flatten()
x_0inter = volt[idx]
y_0inter = yaxis[idx]
plt.plot(x_0inter, y_0inter, 'ro')
print(max(x_0inter))

plt.hlines(0,0,v_vertex,linestyle='--')
plt.hlines(jpa,0,1.2,linestyle='--')
plt.hlines(jpc,0,1.2,linestyle='--')
plt.show()

vtafel = volt - max(x_0inter)
logi = np.log(np.absolute(current))




s_pr = 1050
e_pr = 1400

v_tafpart = vtafel[s_pr:e_pr]
logi_tafpart = logi[s_pr:e_pr]

ln1s = 1300
ln1e = 1400

ln2s = 1050
ln2e = 1200


linfit1 = np.polyfit(vtafel[ln1s:ln1e],logi[ln1s:ln1e], 1)
print("line 1: y =",linfit1[0],"x +",linfit1[1])
y1 = np.arange(min(v_tafpart),max(v_tafpart),0.01)
linfit_line1 = y1*linfit1[0]+linfit1[1]

linfit2 = np.polyfit(vtafel[ln2s:ln2e],logi[ln2s:ln2e], 1)
print("line 2: y =",linfit2[0],"x +",linfit2[1])
# y2 = np.arange(min(v_tafpart),max(v_tafpart),0.01)
linfit_line2 = y1*linfit2[0]+linfit2[1]

# Find intersect of 2 lines
x_inter_1 = (linfit1[1]-linfit2[1])/(linfit2[0]-linfit1[0])
y_inter_1 = x_inter_1*linfit1[0]+linfit1[1]


plt.plot(x_inter_1, y_inter_1, 'ro')

plt.plot(v_tafpart,logi_tafpart)
# plt.plot(vtafel[ln1s:ln1e],logi[ln1s:ln1e])
# plt.plot(vtafel[ln2s:ln2e],logi[ln2s:ln2e])
plt.plot(y1,linfit_line1)
plt.plot(y1,linfit_line2)
plt.show()

