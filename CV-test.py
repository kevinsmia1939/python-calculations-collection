import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
CV_file = 'data/CV and EIS/Sample 1(500C3h)/CV_V3_0to1.2V.txt'

df=pd.read_table(CV_file, skiprows=1, sep='\t', header=None, usecols=[0,1])
df = np.array(df)
volt = df[:,0]
current = df[:,1]


def lnfit(x,y,start_idx,end_idx):
    return np.polyfit(x[start_idx:end_idx],y[start_idx:end_idx], 1)

#jpc and jpa not correct
v_vertex = max(volt)
jpa = max(current)
jpc_sq = np.squeeze(current)
jpc = min(jpc_sq[500:current.shape[0]])

jpa_lns = 200
jpa_lne = 400
jpa_lnfit = lnfit(volt,current,jpa_lns,jpa_lne)
# jpa_lnfit = np.polyfit(volt[jpa_lns:jpa_lne],current[jpa_lns:jpa_lne], 1)
# print(jpa_lnfit)

yaxis = np.zeros(current.shape[0])
idx = np.argwhere(np.diff(np.sign(yaxis - current))).flatten()
x_0inter = volt[idx]
y_0inter = yaxis[idx]

# plt.rcParams['axes.autolimit_mode'] = 'round_numbers'
plt.figure(figsize=(8,8))
plt.plot(volt,current)

plt.plot(volt[jpa_lns:jpa_lne],current[jpa_lns:jpa_lne])

plt.plot(x_0inter, y_0inter, 'ro')
plt.hlines(0,0,v_vertex,linestyle='--')
plt.hlines(jpa,0,1.2,linestyle='--')
plt.hlines(jpc,0,1.2,linestyle='--')
plt.xlim(left=np.floor(min(volt)),right=np.ceil(max(volt) * 100)/100)
plt.show()
plt.clf()

# Tefel Plot

vtafel = volt - max(x_0inter)
logi = np.log(np.absolute(current))

itaf_min = (np.abs(logi-min(logi))).argmin()

tafel_branch_range = 0.2
ln1s_v = -0.05
ln1e_v = -0.16
ln2s_v = 0.16
ln2e_v = 0.1

branch_range = np.abs((np.abs(vtafel-tafel_branch_range)).argmin() - (np.abs(vtafel)).argmin())
s_pr = itaf_min - branch_range
e_pr = itaf_min + branch_range

v_tafpart = vtafel[s_pr:e_pr]
logi_tafpart = logi[s_pr:e_pr]

ln1s = np.abs(v_tafpart-ln1s_v).argmin()
ln1e = np.abs(v_tafpart-ln1e_v).argmin()
ln2s = np.abs(v_tafpart-ln2s_v).argmin()
ln2e = np.abs(v_tafpart-ln2e_v).argmin()

# polyfit
linfit1 = lnfit(v_tafpart,logi_tafpart,ln1s,ln1e)
print("line 1: y =",linfit1[0],"x +",linfit1[1])

linfit2 = lnfit(v_tafpart,logi_tafpart,ln2s,ln2e)
print("line 2: y =",linfit2[0],"x +",linfit2[1])


# Find intersect of 2 lines
x_inter = (linfit1[1]-linfit2[1])/(linfit2[0]-linfit1[0])
y_inter = x_inter*linfit1[0]+linfit1[1]

# Draw lines
x1 = np.linspace(min(v_tafpart),x_inter,40)
linfit_line1 = x1*linfit1[0]+linfit1[1]
plt.plot(x1,linfit_line1,'--')

x2 = np.linspace(x_inter,max(v_tafpart),40)
linfit_line2 = x2*linfit2[0]+linfit2[1]
plt.plot(x2,linfit_line2,'--')

# plt.rcParams['axes.autolimit_mode'] = 'round_numbers'
plt.plot(x_inter, y_inter, 'ro')

plt.plot(v_tafpart,logi_tafpart)
# plt.plot(vtafel,logi)
plt.plot(v_tafpart[ln1s:ln1e],logi_tafpart[ln1s:ln1e])
plt.plot(v_tafpart[ln2s:ln2e],logi_tafpart[ln2s:ln2e])

plt.xlim(left=np.floor(min(v_tafpart) * 10)/10,right=np.ceil(max(v_tafpart) * 10)/10)
plt.ylim(bottom=np.floor(min(logi_tafpart)),top=np.ceil(max(logi_tafpart)))
plt.show()
# print(np.ceil(max(v_tafpart) * 100)/100)

