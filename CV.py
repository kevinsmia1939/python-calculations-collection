import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
CV_file = 'data/NEW CV and EIS/Sample2_400C3h_correct/CV_V4_0to1.2V_30mVs.txt'

# plt.figure(figsize=(8,8))

# Read CV file

df=pd.read_table(CV_file, skiprows=1, sep='\t', header=None, usecols=[0,1])
df = np.array(df)
volt = df[15:,0] # exclude first 15 index to remove artifacts
current = df[15:,1]


##############################################################################
x = volt
y = current
def onpick(event):
    ind = event.ind
    volt = np.take(x, ind)[0]
    current = np.take(y, ind)[0]
    print(ind[0])
    print('volt',volt,'current',current)
    return volt, current
    
fig, ax = plt.subplots()
col = ax.plot(volt, current, picker=1)
fig.canvas.mpl_connect('pick_event', onpick)
##############################################################################

# Function to fit linear line starting from index start_idx to end_idx
def lnfit(x,y,start_idx,end_idx):
    return np.polyfit(x[start_idx:end_idx],y[start_idx:end_idx], 1)

v_vertex = max(volt)
jpa_peak = max(current)

# Calculate jpa
jpa_lns = 200
jpa_lne = 545
jpa_lnfit = lnfit(volt,current,jpa_lns,jpa_lne)
idx_jpa_max = np.argmax(current)
jpa_base = volt[idx_jpa_max]*jpa_lnfit[0]+jpa_lnfit[1]
jpa_abs = current[idx_jpa_max]
jpa = jpa_abs - jpa_base

print("jpa value is",jpa,"A")
jpa_ref_ln = np.linspace(volt[jpa_lns],volt[idx_jpa_max],100)
jpa_ref = jpa_ref_ln*jpa_lnfit[0]+jpa_lnfit[1]

# part of CV to fit jpa
plt.plot(volt[jpa_lns:jpa_lne],current[jpa_lns:jpa_lne],linewidth=4,linestyle='-',color='red')
plt.plot(jpa_ref_ln,jpa_ref,linewidth=2,linestyle='--')
plt.plot(volt[idx_jpa_max],jpa_abs,'bo')
plt.plot(volt[idx_jpa_max],jpa_base,'go')
plt.annotate(text='', xy=(volt[idx_jpa_max],jpa_base), xytext=(volt[idx_jpa_max],jpa_abs), arrowprops=dict(arrowstyle='<-'))

#Calculate jpc
jpc_lns = 1150
jpc_lne = 1253
jpc_lnfit = lnfit(volt,current,jpc_lns,jpc_lne)
idx_jpc_min = np.argmin(current) #Find index of jpc peak
jpc_base = volt[idx_jpc_min]*jpc_lnfit[0]+jpc_lnfit[1]
jpc_abs = current[idx_jpc_min]
jpc = jpc_base - jpc_abs

print("jpc value is",jpc,"A")
jpc_ref_ln = np.linspace(volt[jpc_lns],volt[idx_jpc_min],100)
jpc_ref = jpc_ref_ln*jpc_lnfit[0]+jpc_lnfit[1]

# part of CV to fit jpc
plt.plot(volt[jpc_lns:jpc_lne],current[jpc_lns:jpc_lne],linewidth=4,linestyle='-',color='red')
plt.plot(jpc_ref_ln,jpc_ref,linewidth=2,linestyle='--')
plt.plot(volt[idx_jpc_min],jpc_abs,'bo')
plt.plot(volt[idx_jpc_min],jpc_base,'go')
plt.annotate(text='', xy=(volt[idx_jpc_min],jpc_abs), xytext=(volt[idx_jpc_min],jpc_base), arrowprops=dict(arrowstyle='<-'))

print("Reversibility = ",jpa/jpc)


####
# yaxis = np.zeros(current.shape[0])
# idx = np.argwhere(np.diff(np.sign(yaxis - current))).flatten()
# x_0inter = volt[idx]
# y_0inter = yaxis[idx]

# plt.rcParams['axes.autolimit_mode'] = 'round_numbers'

# plt.plot(x_0inter, y_0inter, 'ro')
# plt.hlines(0,0,v_vertex,linestyle='--')
# plt.hlines(jpa_peak,0,1.2,linestyle='--')
# plt.hlines(jpc,0,1.2,linestyle='--')
plt.xlim(left=np.floor(min(volt)),right=np.ceil(max(volt) * 100)/100)
plt.grid()
plt.show()


# plt.clf()

# Tefel Plot

# vtafel = volt - max(x_0inter)
# logi = np.log(np.absolute(current))

# itaf_min = (np.abs(logi-min(logi))).argmin()

# tafel_branch_range = 0.2
# ln1s_v = -0.05
# ln1e_v = -0.16
# ln2s_v = 0.16
# ln2e_v = 0.1

# branch_range = np.abs((np.abs(vtafel-tafel_branch_range)).argmin() - (np.abs(vtafel)).argmin())
# s_pr = itaf_min - branch_range
# e_pr = itaf_min + branch_range

# v_tafpart = vtafel[s_pr:e_pr]
# logi_tafpart = logi[s_pr:e_pr]

# ln1s = np.abs(v_tafpart-ln1s_v).argmin()
# ln1e = np.abs(v_tafpart-ln1e_v).argmin()
# ln2s = np.abs(v_tafpart-ln2s_v).argmin()
# ln2e = np.abs(v_tafpart-ln2e_v).argmin()

# # polyfit
# linfit1 = lnfit(v_tafpart,logi_tafpart,ln1s,ln1e)
# print("line 1: y =",linfit1[0],"x +",linfit1[1])

# linfit2 = lnfit(v_tafpart,logi_tafpart,ln2s,ln2e)
# print("line 2: y =",linfit2[0],"x +",linfit2[1])


# # Find intersect of 2 lines
# x_inter = (linfit1[1]-linfit2[1])/(linfit2[0]-linfit1[0])
# y_inter = x_inter*linfit1[0]+linfit1[1]

# # Draw lines
# x1 = np.linspace(min(v_tafpart),x_inter,40)
# linfit_line1 = x1*linfit1[0]+linfit1[1]
# plt.plot(x1,linfit_line1,'--')

# x2 = np.linspace(x_inter,max(v_tafpart),40)
# linfit_line2 = x2*linfit2[0]+linfit2[1]
# plt.plot(x2,linfit_line2,'--')

# # plt.rcParams['axes.autolimit_mode'] = 'round_numbers'
# plt.plot(x_inter, y_inter, 'ro')

# plt.plot(v_tafpart,logi_tafpart)
# # plt.plot(vtafel,logi)
# plt.plot(v_tafpart[ln1s:ln1e],logi_tafpart[ln1s:ln1e])
# plt.plot(v_tafpart[ln2s:ln2e],logi_tafpart[ln2s:ln2e])

# plt.xlim(left=np.floor(min(v_tafpart) * 10)/10,right=np.ceil(max(v_tafpart) * 10)/10)
# plt.ylim(bottom=np.floor(min(logi_tafpart)),top=np.ceil(max(logi_tafpart)))
# plt.show()


